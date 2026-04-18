#!/usr/bin/env python3
"""Dump Swift definitions + cross-file references via SourceKit-LSP.

Usage:
    swift-lsp-index.py --workspace <path> --files <f1> <f2> ...
                       [--with-references] [--sourcekit-lsp <bin>]
                       [--index-wait-seconds N]

Output: JSON array on stdout, one record per declaration.
Schema:
    [{"name": "MyClass",
      "kind": "class",            # mapped from LSP SymbolKind
      "file": "path/to/file.swift",
      "line": 10,                 # 1-indexed
      "column": 7,                # 0-indexed (LSP convention for columns)
      "namespace": "Outer.Inner", # dotted path of enclosing decls, or null
      "references": [             # only when --with-references
        {"file": "...", "line": 42}
      ]}]

Tier 1 of the day-1-review Swift indexing ladder. Requires sourcekit-lsp
(ships with Xcode / swift.org toolchain) and — for cross-file references —
a completed background-indexing pass (Swift 6.1+) or a prior `swift build`
with -index-store-path set.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

LSP_SYMBOL_KIND = {
    1: "file", 2: "module", 3: "namespace", 4: "package",
    5: "class", 6: "method", 7: "property", 8: "field",
    9: "constructor", 10: "enum", 11: "interface", 12: "function",
    13: "variable", 14: "constant", 15: "string", 16: "number",
    17: "boolean", 18: "array", 19: "object", 20: "key",
    21: "null", 22: "enummember", 23: "struct", 24: "event",
    25: "operator", 26: "typeparameter",
}


class LSPClient:
    def __init__(self, server_cmd, workspace_root):
        self.proc = subprocess.Popen(
            server_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        self.workspace_root = Path(workspace_root).resolve()
        self._next_id = 1

    def _write(self, msg):
        body = json.dumps(msg).encode("utf-8")
        header = f"Content-Length: {len(body)}\r\n\r\n".encode("ascii")
        self.proc.stdin.write(header + body)
        self.proc.stdin.flush()

    def _read(self):
        headers = {}
        while True:
            line = self.proc.stdout.readline()
            if not line:
                return None
            line = line.decode("ascii").rstrip("\r\n")
            if not line:
                break
            k, _, v = line.partition(":")
            headers[k.strip()] = v.strip()
        length = int(headers["Content-Length"])
        body = self.proc.stdout.read(length)
        return json.loads(body)

    def request(self, method, params):
        req_id = self._next_id
        self._next_id += 1
        self._write({"jsonrpc": "2.0", "id": req_id, "method": method, "params": params})
        while True:
            msg = self._read()
            if msg is None:
                raise RuntimeError("sourcekit-lsp closed the connection")
            if msg.get("id") == req_id and ("result" in msg or "error" in msg):
                if "error" in msg:
                    raise RuntimeError(f"LSP error on {method}: {msg['error']}")
                return msg.get("result")
            # Silently drop notifications and progress updates.

    def notify(self, method, params):
        self._write({"jsonrpc": "2.0", "method": method, "params": params})

    def initialize(self):
        root_uri = self.workspace_root.as_uri()
        self.request("initialize", {
            "processId": os.getpid(),
            "rootUri": root_uri,
            "workspaceFolders": [{"uri": root_uri, "name": self.workspace_root.name}],
            "capabilities": {
                "textDocument": {
                    "documentSymbol": {"hierarchicalDocumentSymbolSupport": True},
                    "references": {},
                },
            },
            "initializationOptions": {"backgroundIndexing": True},
        })
        self.notify("initialized", {})

    def did_open(self, path):
        path = Path(path).resolve()
        self.notify("textDocument/didOpen", {
            "textDocument": {
                "uri": path.as_uri(),
                "languageId": "swift",
                "version": 1,
                "text": path.read_text(encoding="utf-8", errors="replace"),
            },
        })

    def document_symbol(self, path):
        return self.request("textDocument/documentSymbol", {
            "textDocument": {"uri": Path(path).resolve().as_uri()},
        }) or []

    def references(self, path, line, character):
        return self.request("textDocument/references", {
            "textDocument": {"uri": Path(path).resolve().as_uri()},
            "position": {"line": line, "character": character},
            "context": {"includeDeclaration": False},
        }) or []

    def shutdown(self):
        try:
            self.request("shutdown", None)
            self.notify("exit", {})
        except Exception:
            pass
        try:
            self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.proc.kill()


def flatten_symbols(symbols, file_path, parent_chain=()):
    """Flatten hierarchical DocumentSymbol[] into a flat record list."""
    out = []
    for sym in symbols:
        name = sym.get("name", "")
        kind = LSP_SYMBOL_KIND.get(sym.get("kind"), "unknown")
        loc = sym.get("selectionRange") or sym.get("range") or {}
        start = loc.get("start", {"line": 0, "character": 0})
        namespace = ".".join(parent_chain) if parent_chain else None
        out.append({
            "name": name,
            "kind": kind,
            "file": file_path,
            "line": start["line"] + 1,
            "column": start["character"],
            "namespace": namespace,
        })
        for child in sym.get("children", []) or []:
            out.extend(flatten_symbols([child], file_path, parent_chain + (name,)))
    return out


def uri_to_path(uri):
    if uri.startswith("file://"):
        return uri[len("file://"):]
    return uri


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True,
                        help="Workspace root (project directory with Package.swift or .xcodeproj)")
    parser.add_argument("--files", nargs="+", required=True,
                        help="Swift files to index (absolute paths)")
    parser.add_argument("--with-references", action="store_true",
                        help="Also query cross-file references per symbol (slow; needs warm index)")
    parser.add_argument("--sourcekit-lsp", default="sourcekit-lsp",
                        help="Path to sourcekit-lsp binary")
    parser.add_argument("--index-wait-seconds", type=int, default=0,
                        help="Sleep N seconds after initialize to let background indexing warm up")
    args = parser.parse_args()

    client = LSPClient([args.sourcekit_lsp], args.workspace)
    try:
        client.initialize()
        if args.index_wait_seconds > 0:
            time.sleep(args.index_wait_seconds)

        records = []
        for file_path in args.files:
            try:
                client.did_open(file_path)
                syms = client.document_symbol(file_path)
                records.extend(flatten_symbols(syms, file_path))
            except Exception as exc:
                print(f"# documentSymbol failed for {file_path}: {exc}", file=sys.stderr)

        if args.with_references:
            for record in records:
                try:
                    refs = client.references(record["file"], record["line"] - 1, record["column"])
                    record["references"] = [
                        {
                            "file": uri_to_path(r["uri"]),
                            "line": r["range"]["start"]["line"] + 1,
                        }
                        for r in refs
                    ]
                except Exception as exc:
                    print(f"# references failed for {record['name']} @ {record['file']}: {exc}",
                          file=sys.stderr)
                    record["references"] = []

        json.dump(records, sys.stdout, indent=2)
        sys.stdout.write("\n")
    finally:
        client.shutdown()


if __name__ == "__main__":
    main()
