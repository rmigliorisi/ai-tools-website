"""
Read-only check: on cross_reference pages, the closing "Comparing your
options? Also see X, Y, and Z. For the full picture, visit our..." line
links to 3 sibling cross_reference pages (other tools for the same
profession). Observed pattern: the FIRST of the three links usually uses
the bare tool name as anchor text ("ChatGPT"), while the 2nd and 3rd
already use descriptive anchor text ("Copilot for finance professional").
Bare tool-name anchor text is weaker for SEO/AEO (no topical signal about
which specific page it points to) and inconsistent with its own siblings
on the same line.

This scans all 41 cross_reference pages for that "Comparing your options"
line and reports the anchor text used for each of the 3 links, so we can
see how consistent/widespread the pattern really is before fixing
anything.

Does not change anything.

Run:
    python3 scan_generic_anchor_text.py > anchor_text_report.txt
"""

import json
import re

import requests
from wp_creds import AUTH, WP_URL

# Captures the "Comparing your options? Also see A, B, and C." sentence,
# each of A/B/C being an <a href="...">anchor text</a>.
COMPARING_RE = re.compile(
    r"Comparing your options\? Also see (.*?)\.\s*For the full picture",
    re.DOTALL,
)
A_TAG_RE = re.compile(
    r'<a\s+href=\\?"([^"\\]+)\\?"[^>]*>(.*?)<\/a>',
    re.DOTALL,
)


def flatten_strings(value, out):
    if isinstance(value, str):
        if "Comparing your options" in value:
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

    first_bare_count = 0
    total_pages_matched = 0

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

        for s in strings:
            m = COMPARING_RE.search(s)
            if not m:
                continue
            sentence = m.group(1)
            links = A_TAG_RE.findall(sentence)
            if not links:
                continue
            total_pages_matched += 1
            anchor_texts = [text for _, text in links]
            first_is_bare = len(anchor_texts[0].split()) <= 2  # e.g. "Claude", "ChatGPT"
            others_descriptive = any(len(t.split()) > 2 for t in anchor_texts[1:])
            flag = " <-- first bare, others descriptive" if (first_is_bare and others_descriptive) else ""
            if flag:
                first_bare_count += 1
            print(f"{slug} (post {post_id}): {anchor_texts}{flag}")

    print(f"\n\nTOTAL pages with a 'Comparing your options' line: {total_pages_matched}")
    print(f"Pages matching the 'first bare, rest descriptive' pattern: {first_bare_count}")


if __name__ == "__main__":
    main()
