Explore this codebase and produce a structural summary.

**Tool rules:** Use Glob to find files, Grep to search content, Read to read files. Bash is ONLY for `ctags` and `sourcekitten`. No ls/find/cat/awk/wc/du or other shell commands.

**Context budget:** Discovery needs breadth, not depth. Do NOT read source code files — only package manifests, READMEs, config files, and index files.

Investigate:
1. **Structure** — Use Glob to map top-level directories and count files per directory
2. **Tech stack** — Read package.json, Cargo.toml, go.mod, requirements.txt, pyproject.toml, etc.
3. **Entry points** — Use Grep to find main/app/server/route definitions. List each by file path.
4. **Existing docs** — Read README, check docs/ directory
5. **Top-level modules** — Identify distinct directories for separate analysis

Skip node_modules/, vendor/, dist/, build/, .next/, __pycache__/, .git/.

**Write the full discovery report** to: docs/codebase-analysis/.working/discovery.md
Include the complete list of entry points with file paths.

**Return ONLY this compact summary:**

TECH_STACK: {languages, frameworks, infrastructure — one line}
MODULES: {comma-separated list of top-level module paths to analyze}
ENTRY_POINTS: {comma-separated list of entry point file paths}
MODULE_COUNT: {number}
TOTAL_FILES: {approximate count}
