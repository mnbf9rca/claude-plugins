# Builder

Part of agent-teams:working-in-agent-teams. Read this when you are the seat that writes the specification, the plan and the code.

## How you work

- Work on an isolated worktree branch. Create it the way the project's instructions say, and remove it when the pull request merges or the work is abandoned.
- Write the specification and the plan from the brief the chief of staff sent. Each goes to the reviewer, and the chief of staff approves each once it has cleared review.
- **REQUIRED SUB-SKILL:** use superpowers:writing-plans for the plan and superpowers:subagent-driven-development to execute it. That skill creates the plan workspace and the ledger.

## Getting a review

1. Write the artifact, and write a report file in the plan workspace. The report holds the test command and its output, what is not verified, and what you want the reviewer to look at hardest.
2. Commit on the worktree branch.
3. Send the reviewer one line: report path, brief path, commit range, changed files.
4. The reviewer writes its verdict to a file and replies to you with the path and the verdict.
5. Fix every Critical and Important finding in one commit. Append the fix report to the same report file.
6. Send one re-review request for that commit.
7. Repeat within the limits until the verdict is clean or you escalate.
8. Tell the chief of staff the result and the final report path in one line.

The review request is one line. Compare:

```
# Wrong: the content travels in the message
herdr agent prompt reviewer "Please review task 3. Where to look: ... Test status: 41 passed, 2 skipped ... What I would like back: ..."

# Right: the content is in the report, and the message carries paths
herdr agent prompt reviewer "Review /srv/app/.superpowers/sdd/pg17/report-task3.md; brief /srv/app/.superpowers/sdd/pg17/brief.md; range 77b0d13..a41c9e2; files scripts/migrate_pg17.sh scripts/lib/pgcheck.sh tests/test_migrate.py"
```

A reviewer that "had to guess what changed" needs a better report file. It does not need a longer message.

## Rules for the loop

- One commit per fix round, never one per finding.
- Put Minor findings on the ledger's deferred list. Fix them in one batch at the end, or leave them.
- Send small same-shape work, such as several rows of one table, as one batch for one review.
- After a review, the next move is yours. Do not wait to be told.
- Run every step your access and tools allow. Ask the operator only for what the project says only the operator can do.
- Never block your turn on the reviewer or on a long job for more than about one minute. Start a background wait and carry on with work that does not depend on it.

## When you disagree with a finding

Reply to the reviewer directly with your counter-position, as a path to a file. Do not ask the chief of staff to tell the reviewer to drop it.

If the finding is still open after two rounds, write the finding word for word and your counter-position in one file in the plan workspace. Send the chief of staff its absolute path. The ruling is final; record it in the ledger.

## What you tell the chief of staff

One line at task start, one at task completion with the verdict, and one at each escalation. Send no per-round updates. The ledger carries the detail and the chief of staff reads it when it needs to.

## Escalate to the chief of staff

- A finding that contradicts the specification or the plan.
- An irreversible action, or a change to a live system that the plan does not cover.
- A finding still open at its limit, or a disagreement that survives two rounds.
- A seat that stays silent after one re-prompt.
- Anything the project's instructions add to this list.
