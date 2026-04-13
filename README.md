# mnbf9rca Claude Plugins

Custom Claude Code plugins for codebase analysis and PR review workflows.

## Installation

Add the marketplace:

```
/plugin marketplace add mnbf9rca/claude-plugins
```

## Dependencies

- [universal-ctags](https://github.com/universal-ctags/ctags) — required by `analyzing-codebase` and `day-1-review` (`brew install universal-ctags`)
- [jq](https://jqlang.github.io/jq/) — used by the `as-designed-review` Bash intercept hook
- [gh](https://cli.github.com/) — GitHub CLI, used by `reviewing-analysis`, `process-review`, and `day-1-review` skills

## Included skills

### as-designed-review

Analyze a codebase to create "as built" documentation of business rules, then compare against user-edited as-designed files to identify deviations. Can trace complex business logic across multiple modules to identify unexpected end to end rule combinations.

```
/plugin install as-designed-review@mnbf9rca-plugins
```

**Skills:**
- `/as-designed-review:analyzing-codebase` — Multi-phase codebase analysis producing as-built/as-designed documentation
- `/as-designed-review:reviewing-analysis` — Compare as-designed edits against as-built to find deviations

### pr-tools

PR review tools — process review comments and find structural debt.

```
/plugin install pr-tools@mnbf9rca-plugins
```

**Skills:**
- `/pr-tools:process-review` — Process PR review comments, triage them, provide recommended approach for approval, and automate response back to the commenter
- `/pr-tools:day-1-review` — Structural debt analysis with dependency graph tracing and [Riot Games-inspired](https://www.riotgames.com/en/news/taxonomy-tech-debt) taxonomy across PRs or an entire codebase

**Requires:** [superpowers](https://github.com/obra/superpowers) plugin (for process-review skill)

## Setup for editing

After cloning, configure git to use the shared hooks:

```
git config core.hooksPath .githooks
```

This enables the pre-commit hook that prevents direct commits to `main`.



## License

MIT
