# Claude Plugins Marketplace Design

## Overview

Convert three custom Claude Code skills from `~/.claude/skills/` into two plugins distributed via a custom GitHub marketplace at `mnbf9rca/claude-plugins`.

## Marketplace

- **Repository:** `mnbf9rca/claude-plugins`
- **Marketplace name:** `mnbf9rca-plugins`
- **Architecture:** Monorepo — marketplace manifest and all plugins in one repo, using relative `source` paths

### Install experience

```
/plugin marketplace add mnbf9rca/claude-plugins
/plugin install as-designed-review@mnbf9rca-plugins
/plugin install process-review@mnbf9rca-plugins
```

## Plugins

### 1. `as-designed-review` (v1.0.0)

Bundles two existing skills into one plugin:
- **analyzing-codebase** — Multi-phase subagent orchestration to produce as-built/as-designed codebase documentation
- **reviewing-analysis** — Compares user-edited as-designed files against as-built to find deviations

**Skill invocation:** `/as-designed-review:analyzing-codebase`, `/as-designed-review:reviewing-analysis`

### 2. `process-review` (v1.0.0)

Single skill that triages, addresses, and responds to code review comments on GitHub PRs.

**Skill invocation:** `/process-review:process-review`

**Runtime dependency:** Requires `superpowers` plugin for `superpowers:receiving-code-review` and `superpowers:subagent-driven-development`. Skill includes a Step 0 preflight check that fails with install instructions if these are unavailable.

## Directory Structure

```
claude-plugins/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── as-designed-review/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   └── skills/
│   │       ├── analyzing-codebase/
│   │       │   ├── SKILL.md
│   │       │   ├── references/
│   │       │   │   ├── discovery.md
│   │       │   │   ├── module-analysis.md
│   │       │   │   ├── synthesis.md
│   │       │   │   └── feature-analysis.md
│   │       │   └── scripts/
│   │       │       ├── intercept-file-ops.sh
│   │       │       └── copy-to-as-designed.sh
│   │       └── reviewing-analysis/
│   │           └── SKILL.md
│   └── process-review/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── skills/
│           └── process-review/
│               └── SKILL.md
├── docs/
│   └── specs/
│       └── 2026-04-07-claude-plugins-marketplace-design.md
└── README.md
```

## Key Conversions from Standalone Skills

### Path references

All hardcoded `~/.claude/skills/analyzing-codebase/` paths become `${CLAUDE_PLUGIN_ROOT}/skills/analyzing-codebase/`:
- `allowed-tools` in SKILL.md frontmatter
- Hook script comment block

### Hooks

The Bash intercept hook (`intercept-file-ops.sh`) is declared in the `analyzing-codebase` SKILL.md frontmatter `hooks` field, not in a plugin-level `hooks/hooks.json`. This scopes the hook to only fire during skill execution:

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "bash ${CLAUDE_PLUGIN_ROOT}/skills/analyzing-codebase/scripts/intercept-file-ops.sh"
```

### SKILL.md cleanup (analyzing-codebase)

- Remove manual hook installation instructions (Phase 0 section about adding to `~/.claude/settings.json`)
- Update `allowed-tools` paths from `~/.claude/skills/...` to `${CLAUDE_PLUGIN_ROOT}/skills/...`
- Add `hooks` to frontmatter

### SKILL.md addition (process-review)

Add Step 0 dependency check:

```markdown
## Step 0: Check Dependencies

Before proceeding, verify required skills are available:
- `superpowers:receiving-code-review`
- `superpowers:subagent-driven-development`

If either skill is not available, STOP and tell the user:
> "This skill requires the superpowers plugin. Install it with:
> `/plugin marketplace add obra/superpowers`
> `/plugin install superpowers@superpowers`"
```

### Files unchanged

- All four reference templates (`discovery.md`, `module-analysis.md`, `synthesis.md`, `feature-analysis.md`)
- `copy-to-as-designed.sh`
- `reviewing-analysis/SKILL.md`

## File Inventory

| File | Source | Changes |
|------|--------|---------|
| `.claude-plugin/marketplace.json` | New | Marketplace catalog |
| `README.md` | New | Install instructions |
| `plugins/as-designed-review/.claude-plugin/plugin.json` | New | Plugin metadata |
| `plugins/as-designed-review/skills/analyzing-codebase/SKILL.md` | `~/.claude/skills/analyzing-codebase/SKILL.md` | Path rewrites, hooks in frontmatter, remove manual hook instructions |
| `plugins/as-designed-review/skills/analyzing-codebase/references/*` | Copy unchanged | 4 files |
| `plugins/as-designed-review/skills/analyzing-codebase/scripts/intercept-file-ops.sh` | `~/.claude/skills/analyzing-codebase/scripts/intercept-file-ops.sh` | Update comment block paths |
| `plugins/as-designed-review/skills/analyzing-codebase/scripts/copy-to-as-designed.sh` | Copy unchanged | |
| `plugins/as-designed-review/skills/reviewing-analysis/SKILL.md` | `~/.claude/skills/reviewing-analysis/SKILL.md` | No changes |
| `plugins/process-review/.claude-plugin/plugin.json` | New | Plugin metadata |
| `plugins/process-review/skills/process-review/SKILL.md` | `~/.claude/skills/process-review/SKILL.md` | Add Step 0 dependency check |

## Future Plugins

The marketplace is designed to grow. Planned additions include:
- **day-1-design** — Reviews code/PRs from refactoring to ensure implementation looks as if done properly from day 1
