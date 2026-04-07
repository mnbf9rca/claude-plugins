Analyze the module at {module_path} in this {tech_stack} codebase.

**Tool rules:** Use Glob to find files, Grep to search content, Read to read files. Bash is ONLY for ctags. No ls/find/cat/awk/wc/du or other shell commands.

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
