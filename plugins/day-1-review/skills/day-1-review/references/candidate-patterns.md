# Candidate Selection Patterns

Reference for Phase 2 mechanical queries against the dependency graph. Each pattern describes a graph signal and how to detect it.

## Pattern: Dead Code

**Signal:** Symbol has 0 callers/importers in the graph.

**Detection:**
1. From `dependency-graph.json`, find nodes with no incoming edges of type `calls`, `imports`, or `references`
2. Exclude: entry points (main functions, exported module APIs, event handlers, test files)
3. Exclude: symbols with `@public`, `@api`, or `@export` markers
4. Verify with Grep: search the entire scope for the symbol name to catch dynamic references ctags missed

**Category:** `dead-code` | **Type:** Local

## Pattern: Commented-Out Code

**Signal:** Multi-line comments containing code-like syntax.

**Detection:** Grep for patterns like:
- `// .*function\s` or `// .*class\s` or `// .*import\s`
- `/* ... */` blocks containing assignment operators, function calls, or control flow
- `# .*def\s` or `# .*class\s` (Python)

Exclude: documentation comments, license headers, example code in docstrings.

**Category:** `commented-out-code` | **Type:** Local

## Pattern: Unresolved TODOs

**Signal:** Comment markers in code.

**Detection:** Grep for `TODO|FIXME|HACK|XXX|TEMP|WORKAROUND` in comments.

**Category:** `todo-fixme` | **Type:** Local

## Pattern: Vestigial Dependency

**Signal:** Package in manifest not imported by any in-scope source file.

**Detection:**
1. Parse package manifest (package.json, requirements.txt, Cargo.toml, etc.)
2. For each dependency, Grep for import/require/use of that package name
3. If zero matches in source files (excluding lockfiles and the manifest itself), flag it

Exclude: build tools, dev dependencies used only in config files, plugins loaded by name.

**Category:** `vestigial-dependency` | **Type:** Local

## Pattern: Orphaned Config

**Signal:** Config key defined but never read.

**Detection:**
1. Find config files (*.env, *.yaml, *.toml, *.json config files)
2. For each key, Grep for usage in source code
3. Flag keys with zero source references

Exclude: keys consumed by frameworks that read config files by convention.

**Category:** `orphaned-config` | **Type:** Local

## Pattern: Spurious Import

**Signal:** Import statement where no imported symbol is used in the file.

**Detection:**
1. From ctags, identify imports per file
2. For each imported symbol, check if it appears elsewhere in the importing file
3. Flag imports where no imported symbol is referenced

Exclude: side-effect imports (CSS imports, polyfills, module augmentation).

**Category:** `spurious-import` | **Type:** Local

## Pattern: Dead Shim (candidate)

**Signal:** Function with ≤5 callers whose body primarily delegates to another function.

**Detection:**
1. From the graph, find functions with ≤5 incoming `calls` edges
2. Read the function body (this is the one case where Phase 2 reads source)
3. If the body is primarily a call to another function (possibly with argument remapping), flag as candidate

This is a CANDIDATE — Phase 3 confirms whether it's actually a shim worth removing.

**Category:** `dead-shim` | **Type:** MacGyver

## Pattern: Naming Inconsistency

**Signal:** Same concept uses different naming conventions across the graph.

**Detection:**
1. From node names in the graph, identify clusters of related symbols
2. Check for mixed conventions: camelCase vs snake_case, abbreviated vs full names, singular vs plural
3. Flag cases where the same concept (e.g., "user ID") appears as both `userId` and `user_id`

Also check for API aliases — different names for the same underlying object used inconsistently across files (e.g., `M5.Lcd` in one file and `M5.Display` in another when both resolve to the same instance).

**Category:** `naming-inconsistency` | **Type:** Local

## Pattern: Hardcoded Credentials

**Signal:** Passwords, tokens, secrets, or API keys hardcoded in source files.

**Detection:** Grep for patterns like:
- `password\s*=\s*"`, `PASSWORD\s+"`, `secret\s*=\s*"`
- `token\s*=\s*"`, `api_key\s*=\s*"`
- Comments like "Change this for better security" or "TODO: move to env" near string literals

Exclude: test fixtures with obviously fake values, environment variable reads.

**Category:** `hidden-default-magic` | **Type:** Foundational

## Pattern: Bloated Gitignore

**Signal:** `.gitignore` rules for file types that cannot exist in the project.

**Detection:**
1. Read `.gitignore`
2. Identify rules for languages/tools not used in the project (e.g., Fortran rules in a JavaScript project, Office temporary files in an embedded C++ project)
3. Flag rules that will never match any file the project could produce

**Category:** `orphaned-config` | **Type:** Local

## Pattern: Stale Documentation

**Signal:** Doc file references symbols that were modified or removed in the diff.

**Detection:**
1. From the diff, get list of removed/renamed symbols
2. Grep doc files (*.md, *.rst, *.txt, docstrings) for those symbol names
3. Flag matches — the doc may now be wrong

**Category:** `stale-docs` | **Type:** Local

## Pattern: Missing Documentation

**Signal:** Public/exported symbol with no doc coverage.

**Detection:**
1. From the graph, identify exported/public symbols (hop 0 only)
2. Check for: docstrings/JSDoc/type annotations on the symbol, mentions in doc files
3. Flag symbols with neither

**Category:** `missing-docs` | **Type:** Local

## Pattern: Zombie Feature Flag

**Signal:** Conditional on a flag that never changes value.

**Detection:**
1. Grep for common feature flag patterns (config lookups, environment checks, boolean flags)
2. For each flag, check if it's ever set to a different value dynamically
3. If the flag is only ever set to one value (or only set at init and never toggled), flag it

This is a CANDIDATE — Phase 3 confirms whether the flag is truly dead.

**Category:** `zombie-feature-flag` | **Type:** MacGyver
