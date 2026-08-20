# Grammar and word choice

This file covers sentence structure, abbreviations, contractions, inclusive language, writing for a global audience, and a word-choice reference list.

## Conditions before instructions

State the circumstance, condition, or goal before you state the action the reader should take. This order lets the reader skip the step if the condition doesn't apply to them, instead of reading the whole instruction only to discover it wasn't relevant.

| Recommended | Avoid |
|---|---|
| If the build fails, check the CI logs for a stack trace. | Check the CI logs for a stack trace if the build fails. |
| To rotate the API key, run `auth rotate-key`. | Run `auth rotate-key` if you want to rotate the API key. |
| If your cluster runs in a restricted VPC, add the egress rule before you deploy. | Add the egress rule before you deploy if your cluster runs in a restricted VPC. |

## Abbreviations

Spell out an abbreviation the first time you use it, and put the abbreviation in parentheses immediately after; use the abbreviation alone from then on. Skip this step for abbreviations your audience already knows well, such as URL or API, because spelling those out adds noise instead of clarity. Treat abbreviations as ordinary words for pluralization, and don't turn one into a verb.

| Recommended | Avoid |
|---|---|
| Configure the Border Gateway Protocol (BGP) session, then verify the BGP route table. | Configure the BGP session, then verify the route table. (BGP never expanded) |
| The API returns three HTTP status codes. | The API returns three HTTP status codes, or HTTPSCs for short. |
| Export the report as a PDF. | Export the report as a portable document format file. |

## Contractions

Common two-word contractions, including negation forms like "don't" and "isn't," fit the conversational tone of technical writing and are easier to scan than their spelled-out equivalents. Never invent a nonstandard contraction, and never stack two contractions into one, such as combining "might not" and "have" into a single word.

| Recommended | Avoid |
|---|---|
| The service doesn't retry failed requests automatically. | The service mightn't've retried the request. |
| If the token isn't valid, the request fails. | If the token's not valid (using 's to mean "is"), the request fails. |
| You don't need to restart the server after this change. | You do not need to restart the server after this change. |

## Inclusive language

Default to the gender-neutral singular "they" instead of "he," "she," or constructions like "he or she," and vary the names, backgrounds, and ages you use in examples so they reflect a broad audience. Drop ableist terms such as "sanity check" or "crazy," and terms that treat disability as loss or tragedy, in favor of precise, neutral alternatives. Replace socially charged terms for technical concepts, such as pairs built on "master/slave" or "whitelist/blacklist," with alternatives like "primary/replica" or "allowlist/denylist."

| Recommended | Avoid |
|---|---|
| When a developer opens a ticket, they receive a confirmation email. | When a developer opens a ticket, he receives a confirmation email. |
| Run a quick check on the config before you deploy. | Run a sanity check on the config before you deploy. |
| Add the account to the allowlist. | Add the account to the whitelist. |
| The primary node replicates writes to each replica. | The master node replicates writes to each slave. |

## Writing for a global audience

Write short, direct sentences in active voice, because long sentences and passive constructions are harder to translate accurately and often expand in length once translated. Avoid idioms, humor, and culturally specific references, and use one consistent term for each concept throughout a document instead of varying your word choice for style. Don't stack more than two nouns in front of another noun, because dense noun clusters force the reader to untangle which word modifies which.

| Recommended | Avoid |
|---|---|
| This guide uses the following terms. | This guide makes use of the following terms, so to speak. |
| A cloud-native pipeline in a hybrid environment | A hybrid cloud-native DevSecOps pipeline |
| Request only one token. | Request just the one token, no more, no less. |
| Click **Delete** to remove the project. | Hit **Delete** to nuke the project. |

## Word choices

| Term | Use instead / guidance |
|---|---|
| utilize, leverage | use |
| in order to | to |
| and/or | pick one, or rewrite the sentence |
| please, simply, just, easily | drop it |
| click on | click |
| hit | click, press, or type |
| kill, abort | stop, exit, cancel, or end |
| whitelist, blacklist | allowlist, denylist |
| master, slave | primary/replica, controller/worker |
| sanity check | quick check, confidence check |
| dummy variable | placeholder |
| the disabled, a quadriplegic | people with disabilities, a quadriplegic person |
| normal, healthy (vs. disability) | nondisabled, sighted, hearing, neurotypical |
| may | reserve for policy or legal permission |
| might, can | might for possibility, can for capability |
| since, as | because, unless you mean elapsed time |
| once, while | after, although, unless you mean simultaneous time |
| setup, login (as verbs) | set up, log in |
| man-hours, mankind | person-hours, humanity |
| the elderly, senior citizens | older adults |

Derived from the [Google developer documentation style guide](https://developers.google.com/style) (CC BY 4.0).
