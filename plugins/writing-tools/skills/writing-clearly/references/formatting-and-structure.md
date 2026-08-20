# Formatting and structure

This file covers capitalization, headings, lists, tables, procedures, numbers, dates and times, link text, and notices.

## Capitalization

Use sentence case for headings, titles, table cells, captions, and list items — capitalize only the first word and proper nouns. Don't use all-uppercase or camelCase except in official names or literal code identifiers, and don't rely on capitalization alone to signal meaning.

| Recommended | Avoid |
|---|---|
| ## Configure your build pipeline | ## Configure Your Build Pipeline |
| a Pod runs one or more containers | a POD runs one or more containers |

## Headings and titles

Base a heading's wording on its content. For task-based sections, start with a bare infinitive (the base verb form). For conceptual sections, use a noun phrase that doesn't start with an "-ing" word. Give each page one H1, and don't number headings to show sequence.

| Recommended | Avoid |
|---|---|
| Configure a webhook | Configuring a webhook |
| Webhook retry behavior | Retrying webhooks |

## Lists

Use a numbered list only when order matters, such as steps in a sequence. Use a bulleted list for every other set of items. Introduce a list with a complete sentence, and keep every item in the same grammatical form as its siblings.

| Recommended | Avoid |
|---|---|
| 1. Open account settings. <br>2. Select **Reset**. | 1. Open account settings. <br>2. Selecting Reset. |
| Supported formats: JSON, YAML, TOML | Supported formats: JSON, files ending in .yaml, and you can also use TOML |

## Tables

Reach for a table when each item carries three or more related fields, such as a parameter's name, type, and description. If every item is a single value, use a list; if items are simple pairs, prefer a description list. Write concise column headings in sentence case, with no trailing punctuation.

| Recommended | Avoid |
|---|---|
| Table with columns Flag, Type, Description | A single flag name with no header row |
| Header: Default value | Header: Default value: |

## Procedures

State the goal before the steps. Write one action per step, and if the reader needs to know where to act (a specific tab, menu, or tool), say so at the start of the step. Bold the exact name of any button, menu, or field the reader must find.

| Recommended | Avoid |
|---|---|
| In the **Networking** tab, click **Add rule**. | Click Add rule. |
| 1. Enter a project name. <br>2. Click **Create**. | 1. Enter a project name and click Create. |

## Numbers

Spell out zero through nine, and use numerals from 10 up. Always use numerals for version numbers, technical quantities, measurements, and prices, and use numerals for any number in a sentence that also contains a number 10 or greater.

| Recommended | Avoid |
|---|---|
| The cluster has three nodes. | The cluster has 3 nodes. |
| The batch has 12 jobs but 4 failed. | The batch has 12 jobs but four failed. |
| version 4 | version four |

## Dates and times

Spell out the month name and give a four-digit year — never write a date as slash- or period-separated numerals in running text. For a numeric-only date, use YYYY-MM-DD. Use a 24-hour clock when the interface does; otherwise use a 12-hour clock with AM or PM, and spell out any time zone with its UTC offset.

| Recommended | Avoid |
|---|---|
| The update ships on March 3, 2027. | The update ships on 03/03/27. |
| Maintenance starts at 2 PM Pacific Time (UTC-8). | Maintenance starts at 2pm PT. |

## Link text

Write link text that describes the destination on its own, apart from the surrounding sentence — either the exact title of the target page or a short descriptive phrase with the key words first. Never link a bare URL or use a vague phrase as the visible text.

| Recommended | Avoid |
|---|---|
| See [Configure authentication](#) for setup steps. | Click [here](#) for setup steps. |
| Read the [rate limit reference](#) first. | See [this page](#) first. |

## Notices

Reserve a Note for information that helps the reader but isn't required. Use a Caution when the reader needs to proceed carefully, and a Warning when an action is risky or irreversible. Keep notices rare, and never stack two of them back to back — rewrite the surrounding text instead.

| Recommended | Avoid |
|---|---|
| **Warning:** Deleting a bucket permanently removes its objects. | **Note:** ...<br>**Caution:** ...<br>**Note:** ... (three notices in a row) |

Derived from the [Google developer documentation style guide](https://developers.google.com/style) (CC BY 4.0).
