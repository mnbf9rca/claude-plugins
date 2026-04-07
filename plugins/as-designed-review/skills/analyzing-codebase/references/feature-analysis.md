Analyze the "{feature_name}" feature in this codebase.

Contributing modules: {module_list}
Entry points: {entry_points}

**Tool rules:** Use Glob to find files, Grep to search content, Read to read files. Bash is ONLY for ctags. No ls/find/cat/awk/wc/du or other shell commands.

**Context budget:** Read at most 15-20 source files. Use Grep to trace flows, then Read only files with key logic. For large files, read only relevant sections.

**Step 1:** Read the module analysis files for context:
{module_files}

**Step 2:** Read entry point files, then use Grep to trace user flows through the contributing modules. Read only the files that contain business rules or key logic.

**Step 3:** Write the feature document to: docs/codebase-analysis/as-built/feature-{feature_slug}.md

Format:

# Feature: {feature_name}

## What It Does
Plain-language description from a user's perspective.

## User Flows
Mermaid sequence diagrams for request/response flows.
ASCII art for UI state descriptions.

## Business Rules
Every conditional rule, validation, threshold. Be exhaustive and specific.
Include source file and line number for each rule.

## How It Works
Components involved, data flow, key algorithms, error handling.

## Key Files
| File | Role |
|------|------|

## Dependencies
- Depends on: other features this relies on
- Depended on by: features that rely on this

**Return ONLY:**

FEATURE: {feature_name}
STATUS: complete
BUSINESS_RULES_COUNT: {number found}
ISSUES: {any concerns or ambiguities, or "none"}
