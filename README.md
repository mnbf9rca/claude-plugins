# mnbf9rca Claude Plugins

Custom Claude Code plugins for codebase analysis and PR review workflows.

## Installation

Add the marketplace:

```
/plugin marketplace add mnbf9rca/claude-plugins
```

### as-designed-review

Analyze a codebase into as-built documentation, then compare against user-edited as-designed files to identify deviations.

```
/plugin install as-designed-review@mnbf9rca-plugins
```

**Skills:**
- `/as-designed-review:analyzing-codebase` — Multi-phase codebase analysis producing as-built/as-designed documentation
- `/as-designed-review:reviewing-analysis` — Compare as-designed edits against as-built to find deviations

### process-review

Triage, address, and respond to code review comments on GitHub PRs.

```
/plugin install process-review@mnbf9rca-plugins
```

**Skills:**
- `/process-review:process-review` — Process PR review comments with categorization and automated responses

**Requires:** [superpowers](https://github.com/obra/superpowers) plugin

### day-1-review

Analyze code for structural debt — find what wouldn't exist if the codebase were correct from day 1.

```
/plugin install day-1-review@mnbf9rca-plugins
```

**Skills:**
- `/day-1-review:day-1-review` — Structural debt analysis with dependency graph tracing and Riot Games-inspired taxonomy

## Setup

After cloning, configure git to use the shared hooks:

```
git config core.hooksPath .githooks
```

This enables the pre-commit hook that prevents direct commits to `main`.

## Dependencies

- [universal-ctags](https://github.com/universal-ctags/ctags) — required by `analyzing-codebase` and `day-1-review` (`brew install universal-ctags`)
- [jq](https://jqlang.github.io/jq/) — used by the `as-designed-review` Bash intercept hook
- [gh](https://cli.github.com/) — GitHub CLI, used by `reviewing-analysis`, `process-review`, and `day-1-review`

## License

MIT
