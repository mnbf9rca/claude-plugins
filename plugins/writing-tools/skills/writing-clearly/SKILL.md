---
name: writing-clearly
description: Use when writing or editing prose that a person will read — documentation, READMEs, guides, tutorials, release notes, error messages, UI text, code comments, or long-form explanations and reports
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/skills/writing-clearly/scripts/lint_prose.py"
---

# Writing Clearly

## Overview

Write prose that readers can act on the first time they read it. These rules follow the [Google developer documentation style guide](https://developers.google.com/style) (CC BY 4.0), adapted for an AI assistant writing documentation and explanations.

**Core principle:** Every sentence either helps the reader act or understand. If it does neither, delete it.

## When to use

Use for any prose deliverable: docs, READMEs, guides, error messages, UI copy, reports, PR descriptions. Don't apply to code identifiers, quoted third-party text, or prose whose existing house style conflicts (match the project's style first).

## The seven rules

1. **Address the reader as "you".** Never "we" or "let's". The doc's author isn't in the room; the reader is.
2. **Active voice, present tense.** "The server sends a response", not "a response will be sent".
3. **State the goal or condition before the instruction.** "To free disk space, delete the logs" — readers skip instructions whose purpose they don't recognize.
4. **One idea per sentence; ~25 words or fewer.** Split anything longer.
5. **Don't minimize or editorialize.** No "simply", "easily", "just", "obviously", "please". If a step were simple, you wouldn't need to document it.
6. **Be specific and timeless.** Name the exact command, flag, or value. Avoid "currently", "soon", "new", and promises about future versions.
7. **Write for a global audience.** Standard American spelling, no idioms, no pop-culture references, unambiguous dates (January 19, 2026 — never 01/19/26).

## Quick reference

| Instead of | Write |
|---|---|
| in order to | to |
| utilize | use |
| e.g. / i.e. | for example / that is |
| via | by using, through |
| and/or | x or y, or both |
| click on | click |
| should | must (required) or can (optional) |
| whitelist / blacklist | allowlist / denylist |
| sanity check | validation check |

## Detailed references

Load only the file you need:

- [voice-and-tone.md](references/voice-and-tone.md) — person, tense, active voice, tone, timeless writing
- [grammar-and-word-choice.md](references/grammar-and-word-choice.md) — sentence structure, word list, abbreviations, inclusive language, global audience
- [punctuation.md](references/punctuation.md) — commas, colons, dashes, hyphens, quotation marks
- [formatting-and-structure.md](references/formatting-and-structure.md) — headings, lists, tables, procedures, numbers, dates, links, notices
- [code-and-ui.md](references/code-and-ui.md) — code font, code samples, command-line syntax, placeholders, UI elements

## Common mistakes

- **Restating the heading as the first sentence.** Start with information the heading doesn't already give.
- **Burying the instruction in a paragraph.** Use a numbered list for any sequence of two or more actions.
- **Describing the UI instead of the action.** "Click **Save**", not "There is a Save button that you can click".
- **Hedging.** "This may possibly cause issues in some cases" → "This causes X when Y".
- **Trailing conditions.** "Confirm the dry-run output before you prune" → "Before you prune, confirm the dry-run output". The reader must see the condition before acting.
- **Two actions joined by "and".** "Enter a value and click **Save**" is two steps — write it as a numbered list.

## Attribution

Derived from the [Google developer documentation style guide](https://developers.google.com/style), licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). This is an independent adaptation, not endorsed by Google.
