"""
Corrected, narrower re-scan. The first pass (analyze_link_repetition.py)
flagged any inline body link whose target ALSO appeared in the comparison
table or footer — but on reflection that's normal content structure (an
aside link + a scannable table + a "see also" line each serve a different
reader moment), not spam. It also had a bug: when reporting context for a
specific occurrence, it used containing.find(href) which always returns
the FIRST occurrence's position, so if the same tool was linked twice in
different sentences, both report lines incorrectly showed the same
(first) snippet — making two legitimate, separate mentions look like a
literal duplicate.

This version only flags the pattern that's actually worth fixing: the
SAME tool linked TWO OR MORE times via the inline body-mention style
(color:#2563eb...) within the prose of a single page — i.e. a reader
would hit a blue link for the same tool twice while just reading the
paragraphs, not counting the table/footer at all. Context is taken from
each match's own actual position (m.start()), not a re-search.

Does not change anything.

Run:
    python3 analyze_inline_duplicates.py > inline_duplicates_report.txt
"""

import json
import re

import requests
from wp_creds import AUTH, WP_URL

A_TAG_RE = re.compile(
    r'<a\s+href=\\?"([^"\\]+)\\?"(?:\s+style=\\?"([^"\\]*)\\?")?[^>]*>(.*?)<\/a>',
    re.DOTALL,
)


def tool_slug(href):
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

    total_dupe_pairs = 0
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

        # tool_slug -> list of (containing_string, start, end)
        occurrences = {}

        for s in strings:
            for m in A_TAG_RE.finditer(s):
                href, style, text = m.group(1), m.group(2), m.group(3)
                slug_target = tool_slug(href)
                if not slug_target:
                    continue
                is_styled = style is not None and "2563eb" in style
                if not is_styled:
                    continue
                occurrences.setdefault(slug_target, []).append((s, m.start(), m.end(), text))

        dupes = {t: occs for t, occs in occurrences.items() if len(occs) >= 2}

        if dupes:
            pages_affected += 1
            print(f"=== {slug} (post {post_id}) ===")
            for tool_slug_name, occs in dupes.items():
                print(f"  [{tool_slug_name}] linked {len(occs)}x inline:")
                for s, start, end, text in occs:
                    ctx_start = max(0, start - 90)
                    ctx_end = min(len(s), end + 60)
                    same_string = all(occ[0] is s for occ in occs)
                    print(f"    text={text!r} same_paragraph={same_string}")
                    print(f"      {s[ctx_start:ctx_end]!r}")
                total_dupe_pairs += 1
            print()

    print(f"\nTOTAL: {total_dupe_pairs} tools with 2+ inline mentions, across {pages_affected} pages.")


if __name__ == "__main__":
    main()
