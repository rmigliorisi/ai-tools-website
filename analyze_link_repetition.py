"""
Read-only analysis for task: "internal linking feels repetitive/spammy."

On cross_reference pages, tool names get linked in three different spots
within a page: (1) inline, mid-sentence in the "Where X Falls Short"
limitation cards (these use the inline style
`color:#2563eb;text-decoration:none;font-weight:500;`), (2) the comparison
table (comparison_notes field), and (3) the "Comparing your options?"
footer line. (2) and (3) are structural/navigational — they belong in a
scannable table and a clear "see also" call-to-action. (1) is prose — a
reader hits a blue link for ChatGPT in a sentence, then sees ChatGPT again
in the table two paragraphs later, then again in the footer line right
after that. That repetition read is what prompted this task.

This script does NOT change anything. It reports, per cross_reference page,
every inline-styled body link (1) whose target tool ALSO appears as a link
somewhere else on the same page ((2) or (3)) — those are the redundant
candidates. The proposed fix (to be applied in a follow-up script, only
after review) would be: keep the anchor text, drop the <a> wrapper and
style, so the sentence reads naturally without an extra blue link that's
about to repeat.

Run:
    python3 analyze_link_repetition.py > link_repetition_report.txt
"""

import json
import re

import requests
from wp_creds import AUTH, WP_URL

STYLE_MARKER = 'style="color:#2563eb;text-decoration:none;font-weight:500;"'

# Matches any <a href="...">text</a>, capturing href and inner text, plus
# whether it carries the inline body-mention style.
A_TAG_RE = re.compile(
    r'<a\s+href=\\?"([^"\\]+)\\?"(?:\s+style=\\?"([^"\\]*)\\?")?[^>]*>(.*?)<\/a>',
    re.DOTALL,
)


def tool_slug(href):
    # "/chatgpt/finance/" -> "chatgpt", "/perplexity/" -> "perplexity"
    parts = [p for p in href.strip("/").split("/") if p]
    return parts[0] if parts else None


def flatten_strings(value, out):
    if isinstance(value, str):
        if "<a " in value or "<a\\ " in value:
            out.append(value)
    elif isinstance(value, list):
        for v in value:
            flatten_strings(v, out)
    elif isinstance(value, dict):
        for v in value.values():
            flatten_strings(v, out)


def fetch_all_cross_references():
    posts = []
    page = 1
    while True:
        resp = requests.get(
            f"{WP_URL}/wp/v2/cross_reference",
            params={
                "context": "edit",
                "_fields": "id,slug,content",
                "per_page": 100,
                "page": page,
            },
            auth=AUTH,
        )
        if resp.status_code == 400:
            break
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        posts.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return posts


def main():
    posts = fetch_all_cross_references()
    print(f"Fetched {len(posts)} cross_reference posts.\n")

    total_candidates = 0
    pages_affected = 0

    for post in posts:
        post_id = post["id"]
        slug = post["slug"]
        raw = post["content"]["raw"]

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"=== {slug} (post {post_id}) === INVALID JSON ({e}) — skipped")
            continue

        strings = []
        flatten_strings(data, strings)

        styled_links = []   # (tool_slug, href, text, containing_string)
        other_links = set() # tool_slug

        for s in strings:
            for m in A_TAG_RE.finditer(s):
                href, style, text = m.group(1), m.group(2), m.group(3)
                slug_target = tool_slug(href)
                if not slug_target:
                    continue
                is_styled = style is not None and "2563eb" in style
                if is_styled:
                    styled_links.append((slug_target, href, text, s))
                else:
                    other_links.add(slug_target)

        candidates = []
        for slug_target, href, text, containing in styled_links:
            if slug_target in other_links:
                candidates.append((slug_target, href, text, containing))

        if candidates:
            pages_affected += 1
            print(f"=== {slug} (post {post_id}) — {len(candidates)} redundant inline link(s) ===")
            for slug_target, href, text, containing in candidates:
                idx = containing.find(f'href="{href}"')
                if idx == -1:
                    idx = containing.find(f'href=\\"{href}\\"')
                start = max(0, idx - 80)
                end = min(len(containing), idx + 120)
                print(f"  [{slug_target}] href={href!r} text={text!r}")
                print(f"    context: {containing[start:end]!r}")
                total_candidates += 1
            print()

    print(f"\nTOTAL: {total_candidates} redundant inline links across {pages_affected} pages.")


if __name__ == "__main__":
    main()
