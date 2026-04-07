# pr-tools

PR review tools — process review comments and find structural debt.

## Philosophy

Code evolves. Features get added, APIs change, migrations happen partway. The result is a codebase that works but carries scars of its history: shims nobody remembers why they exist, defaults buried in code instead of configuration, documentation that describes last quarter's architecture.

This skill finds those scars systematically by building a dependency graph and reasoning about what should and shouldn't be there.

### Why not just review the code?

Without a dependency graph, reviewers analyze files in isolation. A shim in `adapters/legacy.ts` looks fine on its own -- you only realize it's debt when you trace its callers and find they've all been updated to use the new API directly. A hidden default of `timeout = 30` seems reasonable until you trace the code path and realize three services read it but none document what happens when it's changed.

Structural debt is relational. This skill treats it that way.

### Agentic-era reframing

Traditional tech debt prioritization weighs "fix cost" heavily. With agents, coding cost is approximately zero -- inlining a shim, removing dead code, or updating documentation is trivial. What's still expensive is **verification**: proving the change is safe without human judgment.

This skill adapts [Riot Games' taxonomy of tech debt](https://www.riotgames.com/en/news/taxonomy-tech-debt), replacing "fix cost" with **confidence** -- how certain can we be that removal is safe?

## Usage

```
/pr-tools:process-review [PR#]       # Triage PR review comments
/pr-tools:day-1-review              # Analyze current PR for structural debt
/pr-tools:day-1-review abc123       # Diff against specific SHA
/pr-tools:day-1-review --all        # Full repo scan
```

## What it finds

- Backwards-compatibility shims and compat layers
- Dead code (unused functions, unreachable branches, commented-out code)
- Stale, missing, or orphaned documentation
- Unresolved TODOs/FIXMEs
- Naming inconsistencies
- Zombie feature flags
- Orphaned configuration and vestigial dependencies
- Hidden defaults (magic values and implicit behavior)

## Output

Produces two specs compatible with `superpowers:writing-plans`:

1. **Ready to fix** -- high-confidence findings the agent can handle
2. **Needs your call** -- findings requiring human judgment, with clear explanation of what's unknown

## Dependencies

- [universal-ctags](https://github.com/universal-ctags/ctags) (`brew install universal-ctags`)
- [gh](https://cli.github.com/) (GitHub CLI, for PR resolution)
