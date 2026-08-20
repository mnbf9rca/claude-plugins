# Voice and tone

This file covers how to sound like a knowledgeable colleague across person, tense, voice, and time references.

## Register: conversational but professional

Write the way a capable colleague would explain something to you at your desk: warm, direct, and free of stiffness, but never silly or dismissive. Skip slang, internet abbreviations, and pop-culture references, because they date quickly and don't travel across cultures. Drop exclamation marks and forced enthusiasm, and let the content's usefulness carry the energy instead. Never talk down to the reader by labeling a task easy; a step that stalls out on a reader doesn't feel easy to them. Reserve courtesy words for genuine requests, not for standard instructions.

| Recommended | Avoid |
|---|---|
| This flag lets you skip integration tests during a local build. | Yo, this flag basically nukes your integration tests, no cap. |
| Run `lint --fix` to resolve the formatting errors. | Just run `lint --fix` and boom, you're done! |
| To restart the worker, run `queue restart`. | To restart the worker, please run `queue restart`. |

## Second person, with first person for the organization

Address the reader directly as "you," and treat them as the one performing the task, not as a bystander being told what "we" will do. Reserve "the user" for the end user of the software the reader is building, not for the reader. Switch to third person only when describing what the software or an end user does, keeping "you" for what the reader does. First-person plural works when it clearly refers to the authoring organization, not to the reader.

| Recommended | Avoid |
|---|---|
| Configure your pipeline before you deploy it. | Let's configure our pipeline before we deploy it. |
| This guide shows you how to add a webhook to your service. | This guide shows the user how to add a webhook to their service. |
| Our support team replies to tickets within two business days. | Support tickets receive a reply within two business days from the relevant party. |

## Active voice, with narrow exceptions

Default to active voice, where the sentence's subject performs the action, so the reader always knows who or what is responsible. Passive voice tends to hide the actor and forces readers to guess whether a task falls to them, the tool, or the server. Reserve passive voice for cases where the object matters more than the actor, where naming the actor would unfairly blame the reader, or where the actor doesn't matter to the point being made.

| Recommended | Avoid |
|---|---|
| The CLI validates your config file before deploying. | Your config file is validated by the CLI before deploying. |
| Submit the request to the API. The server returns a token. | The request is submitted to the API, and a token is returned. |
| The build cache was cleared last night. | Someone on the infra team cleared the build cache last night. |

## Present tense, not future

Describe how a tool or system behaves using present tense, even when the behavior happens after a triggering action. Reserve "will" for events genuinely deferred to a later, distinguishable point in time, such as an asynchronous job, not for the routine, immediate result of a step. Avoid the hypothetical "would" as well, and state what happens rather than what would happen.

| Recommended | Avoid |
|---|---|
| Run the script. It writes the output to `build/`. | Run the script. It will write the output to `build/`. |
| Add the file to the manifest. The next sync job uploads it within an hour. | Add the file to the manifest. It will get uploaded eventually. |
| If you revoke the token, the API rejects further requests immediately. | If you revoke the token, the API would reject further requests. |

## Timeless writing

Write about the product as it exists right now, without anchoring the text to a moment in its history. Words like "currently," "now," "new," "soon," and "latest" go stale the moment the product changes again, leaving stranded claims in documentation that outlives the update. Skip forward-looking language too, and don't hint at plans, upcoming releases, or version promises inside reference material; state only what the product does today. To flag that a capability was recently added, anchor it to a concrete date or version number instead of a relative time word.

| Recommended | Avoid |
|---|---|
| The CLI supports `--dry-run` for preview builds. | The CLI now supports `--dry-run` for preview builds. |
| Batch exports aren't supported. | Batch exports aren't currently supported. |
| The v2.3 release (March 2026) adds a `--parallel` flag. | The latest release adds a shiny new `--parallel` flag. |
| The scheduler runs every five minutes. | The scheduler will soon run every five minutes. |

Derived from the [Google developer documentation style guide](https://developers.google.com/style) (CC BY 4.0).
