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

## Dependencies

- [jq](https://jqlang.github.io/jq/) — used by the `as-designed-review` Bash intercept hook

## License

MIT
