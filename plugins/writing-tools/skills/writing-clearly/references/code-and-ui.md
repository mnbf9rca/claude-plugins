# Code in text and UI elements

This file covers code font, code samples, command-line syntax, placeholders, and UI element references for developer documentation.

## What gets code font

Use code font for anything the reader enters or sees verbatim: filenames and paths, commands and flags, environment variable names, class and method names, HTTP verbs, HTTP status codes, and attribute names. Code font marks a boundary, telling the reader exactly what to type or expect.

| Recommended | Avoid |
|---|---|
| Open `deploy.yaml` and set the `TIMEOUT_SECONDS` variable. | Open deploy.yaml and set the TIMEOUT_SECONDS variable. |
| Send a `POST` request; the server returns an HTTP `404 Not Found` status code if the job doesn't exist. | Send a POST request; the server returns an HTTP 404 Not Found status code if the job doesn't exist. |

## What stays in ordinary font

Don't use code font for product, service, or organization names, even when one resembles a command-line tool's name. Don't use code font for a domain name or URL you want the reader to visit in a browser; reserve it for a domain or URL that appears as literal input or output.

| Recommended | Avoid |
|---|---|
| Install the CLI, then run `npm install`. | Install the `CLI`, then run npm install. |
| The `curl` command sends the request; the curl project maintains the library. | The curl command sends the request; the `curl` project maintains the library. |

## Introducing code samples

Precede every code sample with a sentence that says what the sample does. End the sentence with a colon when the sample follows immediately, and with a period when other material comes between the sentence and the sample.

| Recommended | Avoid |
|---|---|
| The following command lists all running containers: `docker ps -a` | The following command lists all running containers, run: `docker ps -a` |

Mark omitted code with a comment in the sample's own language, never with three dots or an ellipsis character.

## Command-line syntax

Put one command per line, formatted as a code block rather than inline text. Show a `$` prompt on every line when a block mixes multi-line and single-line commands; a lone one-line command can drop the prompt. Never include the current directory path before the prompt.

| Recommended | Avoid |
|---|---|
| `$ kubectl get pods`<br>`$ kubectl logs my-pod` | `me@laptop:~/project$ kubectl get pods` |

When a command line runs past 80 characters, break it before a hyphen or underscore, indent the continuation four spaces, and end every line except the last with the shell's continuation character — a backslash preceded by a space on Linux, a caret preceded by a space on Windows. Show output in its own block, separate from the input.

Use square brackets for an optional argument, braces with pipes for a mutually exclusive choice, and three dots for a repeatable argument, but strip all of these from an example meant to be copied and run as-is.

## Placeholders

Write a placeholder in code font using uppercase letters and underscores, with a descriptive name rather than a single letter or a bare `x`.

| Recommended | Avoid |
|---|---|
| `gcloud compute instances create INSTANCE_NAME` | `gcloud compute instances create <name>` |

Explain each placeholder after the sample, not before it. For a single placeholder, use the form "Replace PLACEHOLDER_NAME with ...". For two or more, list each one and explain what it represents.

| Recommended | Avoid |
|---|---|
| `gcloud builds log --stream=BUILD_ID`<br>Replace `BUILD_ID` with the ID of the build. | `gcloud builds log --stream=BUILD_ID` (no explanation follows) |

## UI element references

Bold the name of any UI element you reference — a button, menu, dialog, checkbox, or field — and match the label exactly as the interface shows it. Don't bold a product or feature name unless it's also the literal label of an on-screen element.

| Recommended | Avoid |
|---|---|
| In the **New project** dialog, enter a name and click **Create**. | In the New Project dialog, enter a name and click the "Create" button. |

Use "click" for a button, link, checkbox, or icon, and "select" for a menu item, list item, or radio button. Never write "click on" — "click" alone takes the object directly.

| Recommended | Avoid |
|---|---|
| Click **Deploy**. | Click on the Deploy button. |
| From the **Region** menu, select **us-central1**. | Click on us-central1 in the Region menu. |

When it doesn't hurt clarity, describe the reader's goal instead of the exact widget, because that keeps instructions accurate as the interface changes.

Derived from the [Google developer documentation style guide](https://developers.google.com/style) (CC BY 4.0).
