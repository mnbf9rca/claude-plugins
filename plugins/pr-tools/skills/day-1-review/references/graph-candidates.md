# Graph-Dependent Candidate Selection (Group A)

You are running mechanical pattern queries against a dependency graph to identify structural debt candidates. You do NOT judge whether something is debt — you identify signals. Phase 3 makes the judgment calls.

## Input

You receive:
- A list of in-scope files
- Path to `.working/dependency-graph.json` (written by Phase 1)

Read the dependency graph first. Then run each pattern below.

## Patterns

### Dead Code

**Signal:** Symbol has 0 callers/importers in the graph.

**Detection:**
1. From `dependency-graph.json`, find nodes with no incoming edges of type `calls`, `imports`, or `references`
2. Exclude: entry points (main functions, exported module APIs, event handlers, test files)
3. Exclude: symbols with `@public`, `@api`, or `@export` markers
4. Verify with Grep: search the entire scope for the symbol name to catch dynamic references ctags missed

**Category:** `dead-code` | **Type:** Local

### Dead Shim (candidate)

**Signal:** Function with ≤5 callers whose edge pattern suggests it delegates to another function.

**Detection:**
1. From the graph, find functions with ≤5 incoming `calls` edges
2. Check outgoing edges: if the function has exactly 1 outgoing `calls` edge (suggesting delegation), flag as candidate
3. Look for additional graph signals: callers of this function also directly call the delegation target (bypass pattern)

This is a CANDIDATE — Phase 3 confirms pass-through by reading the function body.

**Category:** `dead-shim` | **Type:** MacGyver

### Spurious Import

**Signal:** Import statement where no imported symbol is used in the file.

**Detection:**
1. From ctags, identify imports per file
2. For each imported symbol, check if it appears elsewhere in the importing file
3. Flag imports where no imported symbol is referenced

Exclude: side-effect imports (CSS imports, polyfills, module augmentation).

**Category:** `spurious-import` | **Type:** Local

### Zombie Feature Flag

**Signal:** Conditional on a flag that never changes value.

**Detection:**
1. Grep for common feature flag patterns (config lookups, environment checks, boolean flags)
2. For each flag, check if it's ever set to a different value dynamically
3. If the flag is only ever set to one value (or only set at init and never toggled), flag it

This is a CANDIDATE — Phase 3 confirms whether the flag is truly dead.

**Category:** `zombie-feature-flag` | **Type:** MacGyver

### Naming Inconsistency

**Signal:** Same concept uses different naming conventions across the graph.

**Detection:**
1. From node names in the graph, identify clusters of related symbols
2. Check for mixed conventions: camelCase vs snake_case, abbreviated vs full names, singular vs plural
3. Flag cases where the same concept (e.g., "user ID") appears as both `userId` and `user_id`

Also check for API aliases — different names for the same underlying object used inconsistently across files.

**Category:** `naming-inconsistency` | **Type:** Local

## Connected Components Partitioning

**IMPORTANT:** In addition to candidates, you MUST produce a `components` array that maps candidates to connected components in the dependency graph. This drives Phase 3 dispatch.

For each connected component in the graph, list which candidate IDs belong to it and which files are in the component.

## Output Format

Return a JSON response:

```json
{
  "summary": {
    "files_expected": "<N>",
    "files_processed": "<N>",
    "skipped": [],
    "patterns_run": ["dead-code", "dead-shim", "spurious-import", "zombie-feature-flag", "naming-inconsistency"],
    "candidates_found": "<N>",
    "dynamic_reference_checks": true
  },
  "issues": [],
  "recommendations": [],
  "components": [
    {
      "id": "comp-1",
      "candidate_ids": ["c1", "c3"],
      "files": ["src/auth.ts", "src/session.ts"]
    }
  ],
  "candidates": [
    {
      "id": "c1",
      "title": "Short description",
      "files": ["path/to/file.ts:42"],
      "category": "dead-code|dead-shim|spurious-import|zombie-feature-flag|naming-inconsistency",
      "evidence": "Specific mechanical evidence from the graph",
      "caller_count": 0,
      "test_references": false,
      "phase3_needed": false
    }
  ]
}
```

Set `phase3_needed: true` for candidates marked as "candidate" above (dead shims, zombie flags) that need semantic judgment.

## Rules

- Read `.working/dependency-graph.json` to get the graph.
- Use Grep and Glob for verification queries.
- Do NOT assess whether something is debt. You identify signals; Phase 3 judges.
- Do NOT read full file contents for semantic analysis. Bounded reads for verification are fine.
- Report problems in `issues` and suggestions in `recommendations`.
