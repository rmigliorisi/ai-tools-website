"""
Read-only, mechanical (regex-based) scan for the "stripped inline link" bug
across ALL 59 tool_review / profession_hub / cross_reference pages — not
just the 7 pages a subagent's visual read flagged earlier. That visual
audit already missed at least one live instance (found by spot-checking
/claude/finance/ directly), so this scan checks every page with pattern
matching instead of relying on a human/LLM skim.

The bug: an <a> tag wrapping a tool name lost its markup AND the single
space on either side, producing run-on text like "asChatGPTPlus's" or
"Outlook,Microsoft Copilotoffers". This scan looks for every occurrence of
a known tool name that is NOT preceded/followed by whitespace, start-of-
string, or normal sentence punctuation+space — i.e. glued directly to an
adjacent letter or comma with no space.

Does not modify anything. Prints a report grouped by page, with a repr()
context window for each hit so exact text can be used to build a precise
fix (same pattern as diagnose_stripped_links.py).

Run:
    python3 scan_stripped_links.py
"""

import json
import re

import requests
from wp_creds import AUTH, WP_URL

POST_TYPES = ["tool_review", "profession_hub", "cross_reference"]

# Longest names first so "Microsoft Copilot" is checked before bare "Copilot", etc.
TOOL_NAMES = [
    "Microsoft Copilot",
    "Perplexity AI",
    "Google Gemini",
    "Notion AI",
    "Otter.ai",
    "ChatGPT",
    "Claude",
    "Copilot",
    "Gemini",
    "Midjourney",
    "Cursor",
    "Grammarly",
    "Otter",
]


def fetch_all_posts(post_type):
    posts = []
    page = 1
    while True:
        resp = requests.get(
            f"{WP_URL}/wp/v2/{post_type}",
            params={
                "context": "edit",
                "_fields": "id,slug,content",
                "per_page": 100,
                "page": page,
            },
            auth=AUTH,
        )
        if resp.status_code == 400:  # past last page
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


def flatten_strings(value, out):
    if isinstance(value, str):
        if value.strip():
            out.append(value)
    elif isinstance(value, list):
        for v in value:
            flatten_strings(v, out)
    elif isinstance(value, dict):
        for v in value.values():
            flatten_strings(v, out)


def find_glued_occurrences(text, tool_name):
    """Yield (start, end) spans where tool_name appears glued to adjacent
    text with no separating space (i.e. the stripped-link symptom)."""
    hits = []
    for m in re.finditer(re.escape(tool_name), text):
        start, end = m.start(), m.end()
        before_ok = start == 0 or text[start - 1] in " \n\t\"'([>“‘—-"
        after_ok = end == len(text) or text[end] in " \n\t.,;:!?\"')]<’—-"
        if not before_ok or not after_ok:
            hits.append((start, end))
    return hits


def main():
    total_hits = 0
    for post_type in POST_TYPES:
        print(f"\n\n########## {post_type} ##########")
        posts = fetch_all_posts(post_type)
        print(f"(fetched {len(posts)} posts)")

        for post in posts:
            post_id = post["id"]
            slug = post["slug"]
            raw = post["content"]["raw"]

            try:
                data = json.loads(raw)
            except json.JSONDecodeError as e:
                print(f"\n=== {slug} (post {post_id}) === INVALID JSON ({e}) — skipping")
                continue

            strings = []
            flatten_strings(data, strings)

            page_hits = []
            for s in strings:
                for tool_name in TOOL_NAMES:
                    for start, end in find_glued_occurrences(s, tool_name):
                        ctx_start = max(0, start - 60)
                        ctx_end = min(len(s), end + 60)
                        page_hits.append((tool_name, s[ctx_start:ctx_end]))

            if page_hits:
                print(f"\n=== {slug} (post {post_id}) — {len(page_hits)} hit(s) ===")
                for tool_name, ctx in page_hits:
                    print(f"  [{tool_name}] {ctx!r}")
                total_hits += len(page_hits)

    print(f"\n\nTOTAL HITS ACROSS ALL PAGES: {total_hits}")


if __name__ == "__main__":
    main()
