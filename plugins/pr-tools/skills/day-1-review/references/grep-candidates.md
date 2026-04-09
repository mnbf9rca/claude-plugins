# Grep-Only Candidate Selection (Group B)

You are running text pattern queries against source files to identify structural debt candidates. You do NOT judge whether something is debt — you identify signals. Phase 3 makes the judgment calls where needed.

## Input

You receive:
- A list of in-scope files

Run each pattern below against these files using Grep and Read.

## Patterns

### Commented-Out Code

**Signal:** Multi-line comments containing code-like syntax.

**Detection:** Grep for patterns like:
- `// .*function\s` or `// .*class\s` or `// .*import\s`
- `/* ... */` blocks containing assignment operators, function calls, or control flow
- `# .*def\s` or `# .*class\s` (Python)

Exclude: documentation comments, license headers, example code in docstrings.

**Category:** `commented-out-code` | **Type:** Local

### Unresolved TODOs

**Signal:** Comment markers in code.

**Detection:** Grep for `TODO|FIXME|HACK|XXX|TEMP|WORKAROUND` in comments.

**Category:** `todo-fixme` | **Type:** Local

### Hardcoded Credentials

**Signal:** Passwords, tokens, secrets, or API keys hardcoded in source files.

**Detection:** Grep for patterns like:
- `password\s*=\s*"`, `PASSWORD\s+"`, `secret\s*=\s*"`
- `token\s*=\s*"`, `api_key\s*=\s*"`
- Comments like "Change this for better security" or "TODO: move to env" near string literals

Exclude: test fixtures with obviously fake values, environment variable reads.

**Category:** `hidden-default-magic` | **Type:** Foundational

### Stale Documentation

**Signal:** Doc file references symbols that were modified or removed in the diff.

**Detection:**
1. From the diff (if available), get list of removed/renamed symbols
2. Grep doc files (*.md, *.rst, *.txt, docstrings) for those symbol names
3. Flag matches — the doc may now be wrong

For `--all` mode without a diff, skip this pattern.

**Category:** `stale-docs` | **Type:** Local

### Missing Documentation

**Signal:** Public/exported symbol with no doc coverage.

**Detection:**
1. Grep for exported/public symbols (export statements, public keywords)
2. For each, check if it has a docstring/JSDoc/type annotation above it
3. Grep doc files for the symbol name
4. Flag symbols with neither

**Category:** `missing-docs` | **Type:** Local

### Orphaned Documentation

**Signal:** Doc files referencing code that doesn't exist.

**Detection:**
1. Find doc files (*.md, *.rst) in the file list
2. Extract code references (function names, file paths, class names mentioned in docs)
3. Grep source files for those references
4. Flag doc references with zero matches in source

**Category:** `orphaned-docs` | **Type:** Local

### Hidden Defaults (magic values) — candidate

**Signal:** Hardcoded literals that look like configuration values.

**Detection:** Grep for patterns like:
- Numeric literals in function parameters or assignments (timeouts, retry counts, limits)
- String literals that look like URLs, hostnames, paths
- Repeated magic numbers across files

This is a CANDIDATE — Phase 3 confirms whether the value is truly a hidden default or intentional.

**Category:** `hidden-default-magic` | **Type:** Foundational

### Undocumented Defaults — candidate

**Signal:** Default parameter values or fallback values with no documentation.

**Detection:**
1. Grep for default parameter values in function signatures
2. Check if any have a doc comment explaining the choice
3. Flag undocumented defaults

This is a CANDIDATE — Phase 3 judges significance.

**Category:** `undocumented-default` | **Type:** Local

## Output Format

Return a JSON response:

```json
{
  "summary": {
    "files_expected": "<N>",
    "files_processed": "<N>",
    "skipped": [],
    "patterns_run": ["commented-out-code", "todo-fixme", "hardcoded-credentials", "stale-docs", "missing-docs", "orphaned-docs", "hidden-default-magic", "undocumented-default"],
    "candidates_found": "<N>"
  },
  "issues": [],
  "recommendations": [],
  "candidates": [
    {
      "id": "b1",
      "title": "Short description",
      "files": ["path/to/file.ts:42"],
      "category": "commented-out-code|todo-fixme|hidden-default-magic|stale-docs|missing-docs|orphaned-docs|undocumented-default",
      "evidence": "Specific text evidence (the matched line/pattern)",
      "phase3_needed": false
    }
  ]
}
```

Set `phase3_needed: true` for candidates marked as "candidate" above (magic values, undocumented defaults).

## Rules

- Use Grep to search file contents, Read to read specific sections for context.
- Do NOT read entire files. Use targeted grep patterns and bounded reads.
- Do NOT assess whether something is debt. You identify signals; Phase 3 judges.
- Report problems in `issues` and suggestions in `recommendations`.
