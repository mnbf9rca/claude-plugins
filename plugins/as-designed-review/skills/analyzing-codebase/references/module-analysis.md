Analyze the module at {module_path} in this {tech_stack} codebase.

**Tool rules:** Use Glob to find files, Grep to search content, Read to read files. Bash is ONLY for `ctags`, `sourcekitten`, and `python3 ${CLAUDE_PLUGIN_ROOT}/skills/analyzing-codebase/scripts/swift-lsp-index.py` (which wraps `sourcekit-lsp`). No ls/find/cat/awk/wc/du or other shell commands.

**Indexer selection by language:**
- Non-Swift source (C/C++/ObjC/JS/TS/Python/Go/Rust/Ruby/etc.) → `ctags`.
- Swift source (`.swift`) → depends on the `swift_tier` input (`{swift_tier}`):
  - `none` → no Swift files in this module, ignore.
  - `1` → SourceKit-LSP tier 1 (semantic, with cross-file references):
    ```bash
    python3 ${CLAUDE_PLUGIN_ROOT}/skills/analyzing-codebase/scripts/swift-lsp-index.py \
      --workspace {workspace_root} \
      --files <swift file 1> <swift file 2> ... \
      --with-references \
      [--index-wait-seconds {swift_tier_wait}]   # only if {swift_tier_wait} > 0
    ```
    Parse the JSON output: `[{name, kind, file, line, column, namespace, references: [{file, line}]}]`. Use this as the authoritative definition + reference index for Swift in this module.
  - `2` → `sourcekitten structure --file <path>` per Swift file. Walk `key.substructure` to collect declarations (class, struct, enum, protocol, extension, actor, func, var, typealias). Convert `key.offset` to a line number by reading the file.
  - `3` → grep-only: match `^\s*(public|internal|private|fileprivate|open)?\s*(final\s+)?(class|struct|enum|protocol|extension|actor|func|let|var|typealias)\s+\w+`. Expect gaps (computed properties, property wrappers, macros).

The orchestrator already presented the Swift tier choice to the user at Phase 0 — do not re-prompt or probe for tools. Obey `{swift_tier}`.

**Context budget:** Do NOT read every file. Use Grep to find what matters, then Read only key files. Aim to read at most 15 files. For large files (200+ lines), read only relevant sections using offset/limit.

Use Grep for import/export patterns and business rule discovery across the module.
Read index files, entry points, and files where Grep found business rules.
Write the analysis as soon as you have enough — do not exhaustively read everything.

**Write your analysis** to: docs/codebase-analysis/.working/modules/{module_name}.md

Format:

# Module: {module_name}

## Purpose
1-2 sentences.

## Public API
Key exports, endpoints, or interfaces.

## Dependencies
Which other modules this imports from (with source file).

## User-Facing Behaviors
What end-user functionality does this module contribute to?

## Business Rules
Conditional logic, validation, thresholds, state-dependent behavior.
Be specific. Include source file and line number for each rule.

**Return ONLY this compact summary:**

MODULE: {module_name}
PURPOSE: {1 sentence}
DEPENDS_ON: {comma-separated module names}
CONTRIBUTES_TO: {comma-separated user-facing behaviors}
BUSINESS_RULES_COUNT: {number found}
