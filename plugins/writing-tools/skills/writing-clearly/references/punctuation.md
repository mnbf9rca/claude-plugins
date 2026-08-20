# Punctuation

This file covers commas, colons, semicolons, dashes, hyphens, quotation marks, and exclamation points for developer documentation.

## Serial commas

Use a comma before the final "and" or "or" in a list of three or more items. Drop it and a reader can misread where one item ends and the next begins.

| Recommended | Avoid |
|---|---|
| The CLI supports flags, environment variables, and config files. | The CLI supports flags, environment variables and config files. |

## Commas after introductory phrases

Place a comma after an introductory word or phrase that precedes the main clause. When a coordinating conjunction (and, but, or, nor, for, so, yet) joins two independent clauses, put a comma before the conjunction unless both clauses are short. Skip the comma when the second clause shares the same subject and isn't independent.

| Recommended | Avoid |
|---|---|
| After you deploy the build, run the smoke tests. | After you deploy the build run the smoke tests. |
| The linter caught the error, and the pipeline failed before merge. | The linter caught the error and the pipeline failed before merge. |
| The service retries the request and logs the failure. | The service retries the request, and logs the failure. |

## Colons

Use a colon to introduce a list, an example, or closely related information, but only when the text before the colon could stand alone as a complete sentence. Lowercase the word after the colon unless it starts a proper noun. Never end an introduction with a construction like "are:" that leaves the sentence incomplete without the colon.

| Recommended | Avoid |
|---|---|
| The config file accepts three keys: host, port, and timeout. | The config file accepts: host, port, and timeout. |

## Semicolons

Prefer two shorter sentences over a semicolon. Reserve the semicolon for two closely related independent clauses that read better joined, or for separating list items that already contain commas.

| Recommended | Avoid |
|---|---|
| Retry the request. If it fails again, check your credentials. | Retry the request; if it fails again, check your credentials. |

## Dashes

Use an em dash to mark a break or an aside in a sentence, with no space on either side. Don't substitute a hyphen or a spaced en dash. Use an en dash, or the word "to," for a numeric range, and use a colon rather than a dash to separate an item from its description.

| Recommended | Avoid |
|---|---|
| The daemon restarts automatically—no manual intervention is needed. | The daemon restarts automatically - no manual intervention is needed. |
| Supported values are 1–100. | Supported values are 1-100. |
| Timeout: the number of seconds to wait before failing. | Timeout — the number of seconds to wait before failing. |

## Hyphens for compound modifiers

Hyphenate a compound modifier when it appears directly before the noun it modifies, so the reader groups the words correctly. Don't hyphenate the same modifier after the noun. When several modifiers share a final word, use a suspended hyphen and let a space follow it, not precede it.

| Recommended | Avoid |
|---|---|
| This is a well-known issue in the parser. | This is a well known issue in the parser. |
| The issue is well known among maintainers. | The issue is well-known among maintainers. |
| Configure the two- and three-node clusters separately. | Configure the two and three-node clusters separately. |

## Quotation marks

Use quotation marks sparingly: for titles of short works, direct quotes, and the rare metaphorical term. In American style, put commas and periods inside the closing quotation mark. The exception is a literal string, such as a keyword or command name, where surrounding punctuation stays outside so the string stays exact. Use straight quotation marks and apostrophes, never curly ones, so the text matches what appears in code.

| Recommended | Avoid |
|---|---|
| Click "Save changes." | Click "Save changes". |
| If you pass "verbose", the tool prints extra logs. | If you pass "verbose," the tool prints extra logs. |

## Exclamation points

Avoid exclamation points in reference and procedural documentation. They read as unprofessional and translate poorly. Use a plain period to report a completed step. Reserve an exclamation point for cases where syntax requires it, such as the `!=` operator, or for a sparing note of encouragement in a tutorial's final milestone.

| Recommended | Avoid |
|---|---|
| The deployment finished. | The deployment finished! |
| You've completed the tutorial! | Great job, you did it!!! |

Derived from the [Google developer documentation style guide](https://developers.google.com/style) (CC BY 4.0).
