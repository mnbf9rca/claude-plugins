# Manifest/Config Candidate Selection (Group C)

You are checking package manifests, config files, and project metadata for structural debt signals. You do NOT judge whether something is debt — you identify signals.

## Input

You receive:
- A list of in-scope files

## Patterns

### Vestigial Dependency

**Signal:** Package in manifest not imported by any in-scope source file.

**Detection:**
1. Find and read package manifests (package.json, requirements.txt, Cargo.toml, go.mod, pyproject.toml, etc.)
2. For each dependency, Grep for import/require/use of that package name across source files
3. If zero matches in source files (excluding lockfiles and the manifest itself), flag it

Exclude: build tools, dev dependencies used only in config files (webpack, eslint, prettier, etc.), plugins loaded by name, peer dependencies.

**Category:** `vestigial-dependency` | **Type:** Local

### Orphaned Config

**Signal:** Config key defined but never read.

**Detection:**
1. Find config files (*.env, *.yaml, *.toml, *.json config files, *.ini)
2. For each key, Grep for usage in source code
3. Flag keys with zero source references

Exclude: keys consumed by frameworks that read config files by convention (e.g., DATABASE_URL for ORMs, PORT for web frameworks).

**Category:** `orphaned-config` | **Type:** Local

### Bloated Gitignore

**Signal:** `.gitignore` rules for file types that cannot exist in the project.

**Detection:**
1. Read `.gitignore`
2. Identify rules for languages/tools not used in the project (e.g., Fortran rules in a JavaScript project, Office temporary files in an embedded C++ project)
3. Flag rules that will never match any file the project could produce

**Category:** `orphaned-config` | **Type:** Local

## Output Format

Return a JSON response:

```json
{
  "summary": {
    "files_expected": "<N>",
    "files_processed": "<N>",
    "skipped": [],
    "patterns_run": ["vestigial-dependency", "orphaned-config", "bloated-gitignore"],
    "candidates_found": "<N>"
  },
  "issues": [],
  "recommendations": [],
  "candidates": [
    {
      "id": "m1",
      "title": "Short description",
      "files": ["package.json:15"],
      "category": "vestigial-dependency|orphaned-config",
      "evidence": "Specific evidence (e.g., 'package X has 0 imports in source')",
      "phase3_needed": false
    }
  ]
}
```

## Rules

- Read manifest and config files directly (Read tool). These are small metadata files.
- Use Grep to search for references across source files.
- Do NOT read source files beyond what Grep returns.
- Be conservative with framework-convention exclusions — when in doubt, flag it and note the uncertainty.
- Report problems in `issues` and suggestions in `recommendations`.
