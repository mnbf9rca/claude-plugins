#!/usr/bin/env python3
"""PostToolUse hook: lint Markdown prose written via Write/Edit for common
style-guide violations. Reads the hook payload JSON on stdin, scans the
written file (code blocks excluded), and reports findings on stderr with
exit 2 so Claude sees them and can fix the prose. Never blocks the write."""

import json
import re
import sys


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    file_path = (payload.get("tool_input") or {}).get("file_path", "")
    if not file_path.lower().endswith((".md", ".mdx", ".markdown")):
        return 0

    try:
        with open(file_path, encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return 0

    # Strip YAML frontmatter, fenced code blocks, and inline code so only
    # prose is linted. Replace with blank lines to preserve line numbers.
    def blank(match: re.Match) -> str:
        return "\n" * match.group(0).count("\n")

    text = re.sub(r"\A---\n.*?\n---\n", blank, text, count=1, flags=re.DOTALL)
    text = re.sub(r"```.*?```", blank, text, flags=re.DOTALL)
    text = re.sub(r"`[^`\n]*`", "", text)

    checks = [
        (r"\bwhite[- ]?list", 'use "allowlist" instead of "whitelist"'),
        (r"\bblack[- ]?list", 'use "denylist" instead of "blacklist"'),
        (r"\bmaster/slave\b|\bslave\b", 'use "primary/replica" or similar instead of master/slave terms'),
        (r"\bsanity[- ]check", 'use "validation check" or "quick check" instead of "sanity check"'),
        (r"\bgrandfathered\b", 'use "legacy status" or "exempt" instead of "grandfathered"'),
        (r"\bman-hours\b|\bmanpower\b", 'use "person-hours" or "workforce" instead of gendered terms'),
        (r"\bplease\b", 'drop "please" — give the instruction directly'),
        (r"\bsimply\b|\beasily\b|\bjust\s+(?:click|run|add|type|use)\b", "drop difficulty-minimizing words (simply, easily, just)"),
        (r"\bobviously\b|\bof course\b", 'drop "obviously"/"of course" — if it were obvious, you would not document it'),
        (r"\bin order to\b", 'use "to" instead of "in order to"'),
        (r"\butiliz", 'use "use" instead of "utilize"'),
        (r"\band/or\b", 'avoid "and/or" — pick one, or write "x or y, or both"'),
        (r"\be\.g\.", 'use "for example" instead of "e.g."'),
        (r"\bi\.e\.", 'use "that is" instead of "i.e."'),
        (r"\bclick on\b", 'use "click" instead of "click on"'),
        (r"\bvia\b", 'prefer "by using" or "through" instead of "via"'),
        (r"\bwe\b|\blet's\b|\bour\b", 'use second person ("you") instead of first person ("we", "let\'s", "our")'),
        (r"\bshould\b", 'avoid "should" — either it is required ("must") or it is optional ("can"); be explicit'),
    ]

    findings = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        # Skip block quotes: often quoted material, not authored prose.
        if line.lstrip().startswith(">"):
            continue
        for pattern, advice in checks:
            if re.search(pattern, line, flags=re.IGNORECASE):
                findings.append(f"  line {lineno}: {advice}")

    if not findings:
        return 0

    shown = findings[:15]
    print(f"Style check ({file_path}):", file=sys.stderr)
    print("\n".join(shown), file=sys.stderr)
    if len(findings) > len(shown):
        print(f"  ...and {len(findings) - len(shown)} more", file=sys.stderr)
    print(
        "These are warnings from the writing-clearly skill, not errors. "
        "Fix the ones that apply to prose you authored; ignore matches in "
        "quoted or third-party text.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
