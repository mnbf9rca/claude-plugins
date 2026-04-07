# Agent Guidance

## What this repo is

A Claude Code plugin marketplace. Contains two plugins (`as-designed-review`, `process-review`) distributed as a monorepo. See `docs/specs/2026-04-07-claude-plugins-marketplace-design.md` for the full design.

## Repo structure

- `.claude-plugin/marketplace.json` — marketplace catalog (lists all plugins)
- `plugins/<name>/.claude-plugin/plugin.json` — per-plugin manifest
- `plugins/<name>/skills/<skill>/SKILL.md` — skill definitions (Markdown with YAML frontmatter)
- `plugins/<name>/skills/<skill>/references/` — prompt templates used by subagents
- `plugins/<name>/skills/<skill>/scripts/` — shell scripts referenced by skills/hooks

## Key conventions

- **`${CLAUDE_PLUGIN_ROOT}`** — resolves to the plugin's root directory at runtime. Use this for all paths in `allowed-tools`, `hooks`, and skill body. Never use `~/.claude/skills/` or absolute paths.
- **Hooks in frontmatter** — declare hooks in SKILL.md frontmatter, not in a plugin-level `hooks.json`. This scopes hooks to skill execution only.
- **Scripts must be executable** — `chmod +x` any `.sh` files.

## Adding a new plugin

1. Create `plugins/<name>/.claude-plugin/plugin.json` with name, description, version, author, repository, license.
2. Create skills under `plugins/<name>/skills/<skill>/SKILL.md`.
3. Add the plugin entry to `.claude-plugin/marketplace.json`.
4. Update `README.md` with install instructions.

## Adding a skill to an existing plugin

1. Create `plugins/<plugin>/skills/<skill>/SKILL.md` with frontmatter (name, description, allowed-tools, hooks).
2. If the skill has reference files or scripts, add them as subdirectories.
3. No manifest changes needed — skills are discovered from the directory structure.

## Validation

```
claude plugin validate ~/path/to/claude-plugins
```

## Reference documentation

- Claude Code plugin system: https://docs.anthropic.com/en/docs/claude-code/plugins
- SKILL.md frontmatter fields: name, description, allowed-tools, hooks, argument-hint
- Hook types: PreToolUse, PostToolUse — declared in frontmatter `hooks` field
