"""Generate Codex plugin manifests from the canonical Claude Code manifests.

Source of truth: plugins/<name>/.claude-plugin/plugin.json
Generated:       plugins/<name>/.codex-plugin/plugin.json

The Codex manifest is a deterministic projection of the Claude one: identity
and publisher metadata are copied verbatim, and a "skills" component pointer is
added when the plugin ships a skills/ directory (the skill tree itself is shared
byte-for-byte between the two ecosystems).

Hooks and allowed-tools are intentionally NOT ported — the Claude hook schema
(SKILL.md frontmatter) has no verified Codex equivalent. See AGENTS.md.

Usage:
    python3 scripts/generate_codex_manifests.py           # write manifests
    python3 scripts/generate_codex_manifests.py --check    # fail on drift (CI)
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGINS_DIR = REPO_ROOT / "plugins"

COPIED_FIELDS = ("name", "version", "description", "author", "repository", "license")


def render(manifest):
    """Deterministic JSON text: 2-space indent, trailing newline."""
    return json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"


def build_codex_manifest(claude, has_skills):
    codex = {}
    for field in COPIED_FIELDS:
        if field in claude:
            codex[field] = claude[field]
    if has_skills:
        codex["skills"] = "./skills"
    return codex


def generate(plugins_dir, check=False):
    """Project every Claude manifest under plugins_dir into a Codex manifest.

    In write mode, returns the list of Codex manifest paths that were written
    (empty when everything is already current). In check mode, writes nothing
    and returns the list of paths that are missing or stale (drift).
    """
    plugins_dir = Path(plugins_dir)
    changed = []
    for claude_manifest in sorted(plugins_dir.glob("*/.claude-plugin/plugin.json")):
        plugin_dir = claude_manifest.parent.parent
        claude = json.loads(claude_manifest.read_text())
        has_skills = (plugin_dir / "skills").is_dir()
        text = render(build_codex_manifest(claude, has_skills))

        out_path = plugin_dir / ".codex-plugin" / "plugin.json"
        current = out_path.read_text() if out_path.exists() else None
        if current == text:
            continue

        changed.append(out_path)
        if not check:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(text)
    return changed


def main(argv=None, plugins_dir=None):
    parser = argparse.ArgumentParser(description="Generate Codex plugin manifests.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify manifests are current; exit non-zero on drift instead of writing.",
    )
    args = parser.parse_args(argv)
    plugins_dir = PLUGINS_DIR if plugins_dir is None else plugins_dir

    changed = generate(plugins_dir, check=args.check)

    if args.check:
        if changed:
            print("Codex manifests are out of date. Run:", file=sys.stderr)
            print("    python3 scripts/generate_codex_manifests.py", file=sys.stderr)
            for path in changed:
                print(f"  drift: {path}", file=sys.stderr)
            return 1
        print("Codex manifests are up to date.")
        return 0

    if changed:
        for path in changed:
            print(f"wrote {path}")
    else:
        print("Codex manifests already up to date; nothing to write.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
