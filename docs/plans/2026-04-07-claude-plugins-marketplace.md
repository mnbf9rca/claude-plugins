# Claude Plugins Marketplace Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert custom Claude Code skills into two plugins distributed via a GitHub marketplace.

**Architecture:** Monorepo marketplace at `mnbf9rca/claude-plugins`. Two plugins (`as-designed-review`, `process-review`) as subdirectories with relative source paths. Skills are copied from `~/.claude/skills/` with path rewrites and plugin-specific additions.

**Tech Stack:** Claude Code plugin system (JSON manifests, Markdown skills, Bash hooks)

**Spec:** `docs/specs/2026-04-07-claude-plugins-marketplace-design.md`

---

## File Structure

```
claude-plugins/
├── .claude-plugin/
│   └── marketplace.json                                    ← NEW: marketplace catalog
├── plugins/
│   ├── as-designed-review/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json                                 ← NEW: plugin manifest
│   │   └── skills/
│   │       ├── analyzing-codebase/
│   │       │   ├── SKILL.md                                ← MODIFIED: path rewrites, hooks in frontmatter, remove manual hook instructions
│   │       │   ├── references/
│   │       │   │   ├── discovery.md                        ← COPY: unchanged
│   │       │   │   ├── module-analysis.md                  ← COPY: unchanged
│   │       │   │   ├── synthesis.md                        ← COPY: unchanged
│   │       │   │   └── feature-analysis.md                 ← COPY: unchanged
│   │       │   └── scripts/
│   │       │       ├── intercept-file-ops.sh               ← MODIFIED: update comment block paths
│   │       │       └── copy-to-as-designed.sh              ← COPY: unchanged
│   │       └── reviewing-analysis/
│   │           └── SKILL.md                                ← COPY: unchanged
│   └── process-review/
│       ├── .claude-plugin/
│       │   └── plugin.json                                 ← NEW: plugin manifest
│       └── skills/
│           └── process-review/
│               └── SKILL.md                                ← MODIFIED: add Step 0 dependency check
├── README.md                                               ← NEW: install instructions
└── docs/
    ├── specs/
    │   └── 2026-04-07-claude-plugins-marketplace-design.md ← EXISTS
    └── plans/
        └── 2026-04-07-claude-plugins-marketplace.md        ← THIS FILE
```

---

### Task 1: Create marketplace manifest

**Files:**
- Create: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Create marketplace.json**

```json
{
  "name": "mnbf9rca-plugins",
  "owner": {
    "name": "mnbf9rca"
  },
  "metadata": {
    "description": "Custom Claude Code plugins for codebase analysis and PR review workflows"
  },
  "plugins": [
    {
      "name": "as-designed-review",
      "source": "./plugins/as-designed-review",
      "description": "Analyze a codebase into as-built documentation, then compare against user-edited as-designed files to identify deviations",
      "version": "1.0.0"
    },
    {
      "name": "process-review",
      "source": "./plugins/process-review",
      "description": "Triage, address, and respond to code review comments on GitHub PRs",
      "version": "1.0.0"
    }
  ]
}
```

- [ ] **Step 2: Commit**

```bash
git -C ~/Downloads/git/claude-plugins add .claude-plugin/marketplace.json
git -C ~/Downloads/git/claude-plugins commit -m "Add marketplace manifest"
```

---

### Task 2: Create as-designed-review plugin manifest

**Files:**
- Create: `plugins/as-designed-review/.claude-plugin/plugin.json`

- [ ] **Step 1: Create plugin.json**

```json
{
  "name": "as-designed-review",
  "description": "Analyze a codebase into as-built documentation, then compare against user-edited as-designed files to identify deviations",
  "version": "1.0.0",
  "author": {
    "name": "mnbf9rca"
  },
  "repository": "https://github.com/mnbf9rca/claude-plugins",
  "license": "MIT"
}
```

- [ ] **Step 2: Commit**

```bash
git -C ~/Downloads/git/claude-plugins add plugins/as-designed-review/.claude-plugin/plugin.json
git -C ~/Downloads/git/claude-plugins commit -m "Add as-designed-review plugin manifest"
```

---

### Task 3: Convert analyzing-codebase SKILL.md

**Files:**
- Create: `plugins/as-designed-review/skills/analyzing-codebase/SKILL.md`
- Source: `~/.claude/skills/analyzing-codebase/SKILL.md`

Three changes from the original:

1. **Frontmatter:** Replace `allowed-tools` Bash paths from `~/.claude/skills/analyzing-codebase/` to `${CLAUDE_PLUGIN_ROOT}/skills/analyzing-codebase/`. Add `hooks` section for the Bash intercept hook.
2. **Phase 0 body:** Remove the manual hook installation instructions (the JSON block telling users to add to `~/.claude/settings.json`). Replace with a brief note that the hook ships with the plugin.
3. **Phase 3 body:** Update the `copy-to-as-designed.sh` invocation path from `bash ~/.claude/skills/analyzing-codebase/scripts/copy-to-as-designed.sh` to `bash ${CLAUDE_PLUGIN_ROOT}/skills/analyzing-codebase/scripts/copy-to-as-designed.sh`.

- [ ] **Step 1: Read the source SKILL.md**

Read `~/.claude/skills/analyzing-codebase/SKILL.md` in full.

- [ ] **Step 2: Create the converted SKILL.md**

Apply these specific changes to the original content:

**Frontmatter replacement** — replace the entire frontmatter block:

Original:
```yaml
---
name: analyzing-codebase
description: Use when the user wants to understand, document, or audit what a codebase does — its features, components, and how they interact
allowed-tools:
  - "Bash(ctags:*)"
  - "Bash(bash ~/.claude/skills/analyzing-codebase/scripts/copy-to-as-designed.sh:*)"
---
```

New:
```yaml
---
name: analyzing-codebase
description: Use when the user wants to understand, document, or audit what a codebase does — its features, components, and how they interact
allowed-tools:
  - "Bash(ctags:*)"
  - "Bash(bash ${CLAUDE_PLUGIN_ROOT}/skills/analyzing-codebase/scripts/copy-to-as-designed.sh:*)"
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "bash ${CLAUDE_PLUGIN_ROOT}/skills/analyzing-codebase/scripts/intercept-file-ops.sh"
---
```

**Phase 0 body change** — replace the optional hook installation block. Find this text:

```
**Optional but recommended:** Tell the user about the Bash intercept hook. Subagents sometimes use `ls`, `find`, `awk` etc. despite instructions not to. The hook in `scripts/intercept-file-ops.sh` blocks these at runtime. To install, add this to `~/.claude/settings.json`:

\`\`\`json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/skills/analyzing-codebase/scripts/intercept-file-ops.sh"
          }
        ]
      }
    ]
  }
}
\`\`\`
```

Replace with:

```
**Bash intercept hook:** This plugin ships with a PreToolUse hook that blocks subagents from using shell commands (`ls`, `find`, `cat`, `awk`, etc.) when they should use dedicated tools. The hook is declared in this skill's frontmatter and activates automatically during skill execution.
```

**Phase 3 body change** — find and replace the copy-to-as-designed.sh invocation:

Original:
```
   bash ~/.claude/skills/analyzing-codebase/scripts/copy-to-as-designed.sh <project-root>
```

New:
```
   bash ${CLAUDE_PLUGIN_ROOT}/skills/analyzing-codebase/scripts/copy-to-as-designed.sh <project-root>
```

All other content remains identical.

- [ ] **Step 3: Commit**

```bash
git -C ~/Downloads/git/claude-plugins add plugins/as-designed-review/skills/analyzing-codebase/SKILL.md
git -C ~/Downloads/git/claude-plugins commit -m "Add analyzing-codebase skill with plugin path rewrites and frontmatter hooks"
```

---

### Task 4: Copy analyzing-codebase reference files

**Files:**
- Create: `plugins/as-designed-review/skills/analyzing-codebase/references/discovery.md`
- Create: `plugins/as-designed-review/skills/analyzing-codebase/references/module-analysis.md`
- Create: `plugins/as-designed-review/skills/analyzing-codebase/references/synthesis.md`
- Create: `plugins/as-designed-review/skills/analyzing-codebase/references/feature-analysis.md`
- Source: `~/.claude/skills/analyzing-codebase/references/`

All four files are copied unchanged.

- [ ] **Step 1: Copy reference files**

Read each file from `~/.claude/skills/analyzing-codebase/references/` and write to `plugins/as-designed-review/skills/analyzing-codebase/references/` with identical content.

- [ ] **Step 2: Commit**

```bash
git -C ~/Downloads/git/claude-plugins add plugins/as-designed-review/skills/analyzing-codebase/references/
git -C ~/Downloads/git/claude-plugins commit -m "Add analyzing-codebase reference templates"
```

---

### Task 5: Convert analyzing-codebase scripts

**Files:**
- Create: `plugins/as-designed-review/skills/analyzing-codebase/scripts/intercept-file-ops.sh`
- Create: `plugins/as-designed-review/skills/analyzing-codebase/scripts/copy-to-as-designed.sh`
- Source: `~/.claude/skills/analyzing-codebase/scripts/`

`copy-to-as-designed.sh` is copied unchanged.

`intercept-file-ops.sh` has one change: update the comment block at the top that shows the manual installation path. The functional code is unchanged.

- [ ] **Step 1: Read source scripts**

Read both files from `~/.claude/skills/analyzing-codebase/scripts/`.

- [ ] **Step 2: Copy copy-to-as-designed.sh unchanged**

Write `plugins/as-designed-review/skills/analyzing-codebase/scripts/copy-to-as-designed.sh` with identical content.

- [ ] **Step 3: Create converted intercept-file-ops.sh**

Replace the comment block at lines 1-17. Original:

```bash
#!/bin/bash
# PreToolUse hook: intercept Bash commands that should use dedicated tools
# Install by adding to ~/.claude/settings.json:
#
# "hooks": {
#   "PreToolUse": [
#     {
#       "matcher": "Bash",
#       "hooks": [
#         {
#           "type": "command",
#           "command": "bash ~/.claude/skills/analyzing-codebase/scripts/intercept-file-ops.sh"
#         }
#       ]
#     }
#   ]
# }
```

New:

```bash
#!/bin/bash
# PreToolUse hook: intercept Bash commands that should use dedicated tools
# This hook is declared in the analyzing-codebase SKILL.md frontmatter
# and activates automatically during skill execution.
```

All code after line 17 remains identical.

- [ ] **Step 4: Make scripts executable**

```bash
chmod +x ~/Downloads/git/claude-plugins/plugins/as-designed-review/skills/analyzing-codebase/scripts/intercept-file-ops.sh
chmod +x ~/Downloads/git/claude-plugins/plugins/as-designed-review/skills/analyzing-codebase/scripts/copy-to-as-designed.sh
```

- [ ] **Step 5: Commit**

```bash
git -C ~/Downloads/git/claude-plugins add plugins/as-designed-review/skills/analyzing-codebase/scripts/
git -C ~/Downloads/git/claude-plugins commit -m "Add analyzing-codebase scripts with updated path references"
```

---

### Task 6: Copy reviewing-analysis skill

**Files:**
- Create: `plugins/as-designed-review/skills/reviewing-analysis/SKILL.md`
- Source: `~/.claude/skills/reviewing-analysis/SKILL.md`

Copied unchanged — no path references to rewrite.

- [ ] **Step 1: Copy SKILL.md**

Read `~/.claude/skills/reviewing-analysis/SKILL.md` and write to `plugins/as-designed-review/skills/reviewing-analysis/SKILL.md` with identical content.

- [ ] **Step 2: Commit**

```bash
git -C ~/Downloads/git/claude-plugins add plugins/as-designed-review/skills/reviewing-analysis/SKILL.md
git -C ~/Downloads/git/claude-plugins commit -m "Add reviewing-analysis skill"
```

---

### Task 7: Create process-review plugin

**Files:**
- Create: `plugins/process-review/.claude-plugin/plugin.json`
- Create: `plugins/process-review/skills/process-review/SKILL.md`
- Source: `~/.claude/skills/process-review/SKILL.md`

- [ ] **Step 1: Create plugin.json**

```json
{
  "name": "process-review",
  "description": "Triage, address, and respond to code review comments on GitHub PRs",
  "version": "1.0.0",
  "author": {
    "name": "mnbf9rca"
  },
  "repository": "https://github.com/mnbf9rca/claude-plugins",
  "license": "MIT"
}
```

- [ ] **Step 2: Read source SKILL.md**

Read `~/.claude/skills/process-review/SKILL.md` in full.

- [ ] **Step 3: Create converted SKILL.md**

One change: insert a new Step 0 between the frontmatter and `## Step 1: Resolve the PR`. The frontmatter and all existing content remain identical.

Insert after the `**REQUIRED BACKGROUND:**` line and before `## Workflow`:

```markdown

## Step 0: Check Dependencies

Before proceeding, verify required skills are available:
- `superpowers:receiving-code-review`
- `superpowers:subagent-driven-development`

If either skill is not available, STOP and tell the user:

> This skill requires the superpowers plugin. Install it with:
> ```
> /plugin marketplace add obra/superpowers
> /plugin install superpowers@superpowers
> ```
```

- [ ] **Step 4: Commit**

```bash
git -C ~/Downloads/git/claude-plugins add plugins/process-review/
git -C ~/Downloads/git/claude-plugins commit -m "Add process-review plugin with dependency check"
```

---

### Task 8: Create README and validate

**Files:**
- Create: `README.md`

- [ ] **Step 1: Create README.md**

```markdown
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

## License

MIT
```

- [ ] **Step 2: Validate the marketplace**

```bash
claude plugin validate ~/Downloads/git/claude-plugins
```

Fix any validation errors before proceeding.

- [ ] **Step 3: Test locally**

```bash
claude --plugin-dir ~/Downloads/git/claude-plugins/plugins/as-designed-review --plugin-dir ~/Downloads/git/claude-plugins/plugins/process-review
```

Verify skills appear in `/help` output.

- [ ] **Step 4: Commit**

```bash
git -C ~/Downloads/git/claude-plugins add README.md
git -C ~/Downloads/git/claude-plugins commit -m "Add README with installation instructions"
```

---

### Task 9: Push to GitHub

- [ ] **Step 1: Create the GitHub repository**

```bash
gh repo create mnbf9rca/claude-plugins --public --source ~/Downloads/git/claude-plugins --description "Custom Claude Code plugins for codebase analysis and PR review workflows"
```

- [ ] **Step 2: Push**

```bash
git -C ~/Downloads/git/claude-plugins push -u origin main
```
