---
name: working-in-agent-teams
description: Use when work is split across separate, long-lived coding-agent sessions (for example Herdr tabs or panes) acting as chief of staff, builder and reviewer. Triggers - the operator asks to get Codex, another Claude, "the builder" or "the reviewer" to build or review something; you are about to brief, prompt, wait on or relay between agents in other panes; another agent session sends you a brief, a review request, a verdict or a dispute to settle.
---

# Working in agent teams

## Overview

Three long-lived agent sessions share one repository. Each seat has its own context and its own job.

**Core principle:** paths travel between seats and content stays in files. The chief of staff carries the operator's intent and never carries artifacts.

**REQUIRED BACKGROUND:** superpowers:subagent-driven-development defines the plan workspace (`.superpowers/sdd/<plan>/`), the progress ledger, and the Critical, Important and Minor labels used here. The herdr skill defines the command syntax.

## Find your seat, then read its file

| Seat | Its job | It never | Read |
|---|---|---|---|
| Chief of staff | Talks to the operator. Interprets what they mean. Gets the brief agreed. Rules on escalations. | Dispatches before the operator agrees. Reads diffs, reviews or panes of working agents. Relays between the other two seats. | [references/chief-of-staff.md](references/chief-of-staff.md) |
| Builder | Writes the specification, the plan, the code and the documentation. Commits on its own worktree branch. | Pastes output into a message. Sends per-round updates to the chief of staff. | [references/builder.md](references/builder.md) |
| Reviewer | Reviews each artifact independently. Verifies read-only. | Changes files, branches or systems. | [references/reviewer.md](references/reviewer.md) |

The project's instructions say which agent fills which seat. If they do not, or `herdr agent list` shows none or several candidates for a seat, ask the operator and wait. Do not guess.
A generic subagent does not replace a seat.

Read [references/herdr.md](references/herdr.md) before you prompt or wait on another seat.

## Who talks to whom

- The operator talks to the chief of staff only.
- The chief of staff sends the builder the agreed brief, as a path.
- The builder and the reviewer talk to each other directly.
- The builder sends the chief of staff one line at task start, at task completion and at each escalation.
- A dispute reaches the chief of staff as one escalation file, never as a request to "have a look".

## A handover is one line

Every message between seats has this shape and nothing else:

```
Review /abs/.superpowers/sdd/<plan>/report-task3.md; brief /abs/.superpowers/sdd/<plan>/brief.md; range 77b0d13..a41c9e2; files scripts/migrate.sh tests/test_migrate.py
```

```
Review: /abs/.superpowers/sdd/<plan>/review-task3.md; verdict: CLEAN
```

The recipient gets everything else by opening the file. Test results, caveats, what to look at hardest and what you want back all go in the report file. If it is not in a file yet, write the file first.
Use absolute paths: the main checkout and a worktree can hold different files at the same relative path.

## Size the model to the task

Use the least capable model that can do the job. Most tasks do not need the top model.

| Work | Model |
|---|---|
| Searches, test runs, bulk or mechanical edits, a task whose plan already contains the code | Small and cheap |
| Multi-file implementation, debugging, task reviews, re-reviews of a fix diff | Mid-tier |
| Specification and plan review, whole-branch review, a subtle or high-risk diff, an escalation ruling | Strong, one tier below the top |

For Claude models those three sizes are Haiku, Sonnet and Opus. The reviewer seat runs on the strong tier, not on the top model.
Use the top model only where the project's instructions assign it, or for work a strong model has already failed at.

This applies to every seat, and to every subagent, headless run and helper session a seat starts.
**Always name the model when you start one.** An omitted model inherits your session's model, which is usually the most expensive.

superpowers:subagent-driven-development has the full guidance under Model Selection.

## Limits

These are defaults. The project's instructions may change them.

| Loop | Limit |
|---|---|
| Specification or plan review | Two rounds |
| Task review | Three fix rounds |
| Whole-branch review | One fix wave and one scoped re-review |
| Disputed finding | Escalate after two rounds |
| Silent seat | Re-prompt once after fifteen minutes, then escalate |
| Foreground wait on a seat or a job | About one minute, then use a background wait |

Only Critical and Important findings enter a loop. Minors go on the ledger's deferred list.
Escalate whatever is still open at a limit.

## What the project supplies

Look for these in the project's instructions before you start:

- Which agent or harness fills each seat, and which model each seat runs on.
- How each seat gets its worktree and its access, and any start-up check to run.
- What only the operator can do, such as a browser sign-in or approving publication.
- What counts as documentation-only work, which skips the brief and the reviewer round.
- Any extra escalation triggers and any changed limits.

## Red flags

Stop if you catch yourself doing any of these:

- Prompting another seat about work the operator has not agreed.
- Writing "otherwise I will proceed" to the operator.
- Composing a message to another seat that is longer than one line.
- Starting a subagent or a headless run without naming its model.
- Opening a diff, a review file or another agent's pane as chief of staff.
- Passing a finding, a fix or a ruling from one seat to another by hand.
