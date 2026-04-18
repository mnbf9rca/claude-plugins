# mnbf9rca Claude Plugins

Custom Claude Code plugins for codebase analysis and PR review workflows.

## Installation

Add the marketplace:

```
/plugin marketplace add mnbf9rca/claude-plugins
```

## Dependencies

- [universal-ctags](https://github.com/universal-ctags/ctags) — required by `analyzing-codebase` and `day-1-review` (`brew install universal-ctags`). The ctags binary bundled with macOS/Xcode is a different, older project and will not work.
- [jq](https://jqlang.github.io/jq/) — used by the `as-designed-review` Bash intercept hook
- [gh](https://cli.github.com/) — GitHub CLI, used by `reviewing-analysis`, `process-review`, and `day-1-review` skills

### Optional, for Swift codebases

Universal-ctags has no native Swift parser. Both skills detect Swift at run time and present a three-tier choice to the user:

- **Tier 1 — SourceKit-LSP + index-store.** Semantic definitions **and** cross-file references (same data Xcode's "Find Call Hierarchy" uses). Requires `sourcekit-lsp` (ships with Xcode / swift.org toolchain) and a warm index-store from a prior `swift build` — or Swift 6.1+ background indexing, which each skill can opt into with an explicit wait. Driven by a bundled helper script (`scripts/swift-lsp-index.py`, invoked via `python3`; python3 is commonly available on macOS via the Xcode Command Line Tools, the swift.org toolchain, or Homebrew — install it with `brew install python` if it's missing).
- **Tier 2 — [SourceKitten](https://github.com/jpsim/SourceKitten)** (`brew install sourcekitten`). Syntactic definitions (class, struct, enum, protocol, extension, actor, func, var, typealias) without needing a build. Does not resolve cross-file references — those fall back to grep.
- **Tier 3 — grep only.** Approximate definitions via regex. Misses computed properties, property wrappers, and macro-generated code. Always available.

If your scope has no Swift files, none of these matter.

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
