# Graph Extraction Subagent

You are building a dependency graph for structural debt analysis. Your job is purely mechanical — map structure, don't judge debt.

## Input

You receive:
- A list of in-scope files (from the diff or full repo)
- The scope mode (PR, SHA, or full repo)
- An **indexing capability map** from the orchestrator's honesty gate, e.g.:
  ```
  indexing_capability: {
    ctags: true,
    sourcekitten: true,
    sourcekit_lsp: true,
    swift_index_store: "/abs/path/.build/.../index/store"  # null if not warm
  }
  swift_tier: 1            # 1 = sourcekit-lsp, 2 = sourcekitten, 3 = grep-only
  swift_tier_wait: 0       # seconds to wait for background indexing (tier 1 only)
  workspace_root: "/abs/path/to/repo"
  ```
  Obey this map — do not probe for or install tools yourself, and do not upgrade the tier. The only permitted downgrade is the explicit tier-1 error-recovery fallback documented below; any such downgrade must be recorded in `issues`.

## Process

### Step 1: Symbol Index (per-language dispatch)

Partition the file list by extension and run the chosen indexer for each partition.

**Non-Swift files** (`.c/.h/.cpp/.hpp/.m/.mm/.js/.ts/.tsx/.py/.go/.rs/.rb/.java`, etc.) → ctags, if available.

  Full repo mode (`--all`): `ctags --output-format=json --fields=+n+r+S+K --extras=+r -R .`

  PR/SHA mode: `ctags --output-format=json --fields=+n+r+S+K --extras=+r <file1> <file2> ...`

  Parse the output to build a symbol-to-file mapping (name, file, line, kind).

**Swift files** (`.swift`) — behaviour depends on `swift_tier`:

- **Tier 1 (`sourcekit-lsp` + driver script):** Run the plugin's LSP driver, which spawns `sourcekit-lsp` under the hood and dumps semantic symbols with cross-file references:
  ```bash
  python3 ${CLAUDE_PLUGIN_ROOT}/skills/day-1-review/scripts/swift-lsp-index.py \
    --workspace <workspace_root> \
    --files <swift-file-1> <swift-file-2> ... \
    --with-references \
    [--index-wait-seconds <swift_tier_wait>]
  ```
  Output is a JSON array: `[{name, kind, file, line, column, namespace, references: [{file, line}]}, ...]`. Parse it and merge into the symbol-to-file mapping — the `references` array is the authoritative cross-file usage list for Swift symbols at this tier (use it instead of grep when building edges).
  - Pass `--index-wait-seconds` **only** if `swift_tier_wait > 0` (set by the orchestrator when no warm index-store was detected but the user chose to rely on background indexing).
  - **Error recovery (the only allowed tier change):** If the script exits non-zero, capture the stderr in `issues`, mark the affected files as downgraded from tier 1 to tier 3 (also recorded in `issues`), and re-index those files with tier 3's grep-only rules. Do not silently skip them, and do not try tier 2 as an intermediate step.
  - **Note in `issues`:** "Swift indexed with SourceKit-LSP (tier 1) — semantic definitions and cross-file references via `scripts/swift-lsp-index.py`."

- **Tier 2 (`sourcekitten` available):** Run `sourcekitten structure --file <path>` per Swift file. The output is JSON with a recursive `key.substructure` tree; walk it and emit a symbol record for each declaration whose `key.kind` starts with `source.lang.swift.decl.`. Map Swift kinds to the ctags-style schema:
  - `decl.class` → `class`, `decl.struct` → `struct`, `decl.enum` → `enum`, `decl.protocol` → `protocol`, `decl.extension*` → `extension`, `decl.function.free` / `decl.function.method.*` → `function`, `decl.var.*` → `variable`, `decl.actor` → `class` (tagged `actor`), `decl.typealias` → `typealias`.
  - Convert `key.offset` to a line number by reading the file and counting newlines.
  - Record `namespace`: the chain of enclosing struct/class/enum/extension names (from the substructure parents) so `Foo.bar` calls can be resolved.
  - Cross-file references: fall back to Grep scoped to `*.swift` (match `\b<SymbolName>\b`).
  - **Note in `issues`:** "Swift indexed with SourceKitten (tier 2) — definitions captured, cross-file references resolved by grep only."

- **Tier 3 (no Swift indexer):** Do not invoke ctags on `.swift` files (the bundled Swift parser is absent or useless). Capture Swift definitions by Grep only: match `^\s*(public|internal|private|fileprivate|open)?\s*(final\s+)?(class|struct|enum|protocol|extension|actor|func|let|var|typealias)\s+\w+`. This is a floor — it will miss computed properties, property wrappers, macros, and anything clever.
  - **Note in `issues`:** "Swift indexed with grep only (tier 3) — definitions approximate, no reference resolution. Install SourceKitten or build the project + use SourceKit-LSP for better coverage."

Merge all partitions into a single symbol-to-file mapping before Step 2.

### Step 2: Import/Reference Tracing

For each in-scope file, use Grep to find:
- Import/include/require statements (language-appropriate patterns)
- References to symbols defined in other files (cross-reference with ctags output)
- Config key reads (patterns like `getConfig`, `process.env`, `Settings.get`, etc.)

Build edges: file A imports from file B, function X calls function Y.

### Step 3: Two-Hop Expansion (PR/SHA mode only)

Starting from changed files (hop 0):
- **Hop 1:** Find all files that import from or are imported by hop-0 files. Find all functions that call or are called by functions in hop-0 files.
- **Hop 2:** Find files that connect hop-1 nodes to each other — the bridging context.

For full-repo mode, skip this — everything is already in scope.

### Step 4: Output

Write `.working/dependency-graph.json` with this structure:

```json
{
  "scope": {
    "mode": "pr|sha|all",
    "base": "<base ref>",
    "files_analyzed": "<N>",
    "files_in_graph": "<N>"
  },
  "nodes": [
    {
      "id": "<unique symbol or file identifier>",
      "file": "<path>",
      "line": "<N>",
      "type": "function|class|variable|constant|config|import",
      "hop": 0
    }
  ],
  "edges": [
    {
      "from": "<node id>",
      "to": "<node id>",
      "type": "calls|imports|extends|references|reads_config"
    }
  ]
}
```

### Step 5: Return Summary

Return a JSON response to the orchestrator with this structure:

```json
{
  "summary": {
    "files_expected": "<N>",
    "files_processed": "<N>",
    "skipped": [],
    "nodes_created": "<N>",
    "edges_created": "<N>"
  },
  "issues": [],
  "recommendations": []
}
```

Report any problems in `issues` (e.g., "ctags not installed — fell back to grep-based tracing, precision may be lower", "3 files exceeded 10k lines, symbol tracing may be incomplete"). Include suggestions in `recommendations` (e.g., "Re-run with --all to catch cross-module dependencies").

## Rules

- Use Glob to find files, Grep to search content, Read to read files.
- Bash is ONLY for `ctags`, `sourcekitten`, and `python3 ${CLAUDE_PLUGIN_ROOT}/skills/day-1-review/scripts/swift-lsp-index.py` (which wraps `sourcekit-lsp`). No ls, find, cat, or other shell commands.
- Do NOT assess whether anything is debt. Map structure only.
- Do NOT read file contents beyond what's needed for indexer output parsing and import/reference tracing. Reading a Swift file to convert `key.offset` to a line number is fine.
- Obey the `indexing_capability` input. Do not probe for tools or attempt to install them.
- If the capability map shows a language is in grep-only tier, that is a conscious user decision made at the honesty gate — do not re-flag it as an error, just note the tier in `issues`.
- Write output to `.working/dependency-graph.json` using the Write tool. The `.working/` directory will be created automatically.
