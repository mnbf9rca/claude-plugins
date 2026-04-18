Synthesize module analyses into a feature map.

**Tool rules:** Use Glob to find files, Grep to search content, Read to read files. Bash is ONLY for `ctags` and `sourcekitten`. No ls/find/cat/awk/wc/du or other shell commands.

**Context budget:** Read all module analysis files (they're concise). Use Grep for import analysis — do NOT read source files directly.

Steps:
1. Glob `docs/codebase-analysis/.working/modules/*.md`, then Read each module analysis file
2. Read docs/codebase-analysis/.working/discovery.md for entry points
3. Use Grep for import/require/use/from patterns to map cross-module dependencies
4. Build dependency graph from module Dependencies sections + Grep results
5. Cluster related User-Facing Behaviors into features (e.g., "Authentication", "Billing")
6. Map entry points to features

**Write the dependency graph** to: docs/codebase-analysis/.working/dependency-graph.md

**Write the feature map** to: docs/codebase-analysis/.working/feature-map.md

Feature map format:

# Feature Map

## Features

### {Feature Name}
- **Description:** 1 sentence
- **Contributing modules:** {list}
- **Entry points:** {list}
- **Key business rules:** {count from module analyses}

## Unmapped Modules
Infrastructure, utilities, or modules needing manual classification.

**Return ONLY:**

FEATURES: {comma-separated feature names}
UNMAPPED: {comma-separated module names, or "none"}
