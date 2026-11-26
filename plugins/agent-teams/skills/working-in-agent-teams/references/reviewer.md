# Reviewer

Part of agent-teams:working-in-agent-teams. Read this when you are the seat that reviews the builder's work.

## How you work

- You are independent. Read the brief, the specification and the plan yourself, and judge the work against them, not against the builder's summary.
- You verify read-only. Any access you hold to live systems is for checking. It does not authorize a change.
- Match the model to the review. Use the most capable model at high effort for a specification, a plan, a whole branch or a subtle, high-risk diff. A small mechanical diff or a scoped re-review takes a mid-tier model.

## Answering a review request

1. Open the report file and the brief from the request. Read the commit range it names.
2. Write one ranked report to a verdict file in the plan workspace. Label each finding Critical, Important or Minor, with file and line.
3. For a task review, give two separate verdicts: does it meet the specification, and is the quality acceptable.
4. Reply to the builder in one line: verdict path and verdict.

```
herdr agent prompt builder "Review: /srv/app/.superpowers/sdd/pg17/review-task3.md; verdict: FINDINGS"
```

Reply to the builder, not to the chief of staff.

## Rules for the loop

- Send one report per request.
- On a re-review, read only the fix diff. Mark each earlier finding as addressed or not addressed, and flag new breakage in that diff only.
- Do not raise a deferred Minor again.
- Review a batch of small same-shape changes once, as a batch.

## Design reviews include a deletion pass

When you review a specification or a plan, look for machinery that exists to feel rigorous. For each item, say what to delete and what would be lost by deleting it.

## When the builder disputes a finding

Answer the builder directly. Hold the finding if you can name a concrete scenario it prevents; withdraw it in the verdict file if you cannot.

If it is still open after two rounds, the builder writes the escalation file. Check that it quotes your finding word for word. The chief of staff's ruling is final.
