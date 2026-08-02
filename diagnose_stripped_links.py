"""
Read-only diagnostic — dumps the exact raw text (via repr(), so quote
characters and whitespace are unambiguous) around the 4 spots where
fix_stripped_links.py's safety check skipped a replacement, so the next
pass can be built from ground truth instead of another guess.

Does not modify anything.

Run:
    python3 diagnose_stripped_links.py
"""

import json

import requests
from wp_creds import AUTH, WP_URL

# post_id, slug, and an anchor substring (no apostrophes/quotes, stable
# across the whole run so far) to locate each unresolved spot.
TARGETS = [
    {
        "post_id": 373,
        "slug": "claude-finance",
        "anchor": "Code Interpreter",
    },
    {
        "post_id": 374,
        "slug": "claude-insurance",
        "anchor": "better integration",
    },
    {
        "post_id": 383,
        "slug": "gemini-finance",
        "anchor": "M365, Gemini",
    },
    {
        "post_id": 383,
        "slug": "gemini-finance",
        "anchor": "different suite",
    },
]


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


def main():
    seen_posts = {}
    for target in TARGETS:
        post_id = target["post_id"]
        slug = target["slug"]
        anchor = target["anchor"]

        if post_id not in seen_posts:
            resp = requests.get(
                f"{WP_URL}/wp/v2/cross_reference/{post_id}",
                params={"context": "edit", "_fields": "id,content"},
                auth=AUTH,
            )
            resp.raise_for_status()
            raw = resp.json()["content"]["raw"]
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as e:
                print(f"=== {slug} (post {post_id}) === ABORT — invalid JSON ({e})")
                seen_posts[post_id] = None
                continue
            seen_posts[post_id] = data

        data = seen_posts[post_id]
        print(f"\n=== {slug} (post {post_id}) — anchor: {anchor!r} ===")
        if data is None:
            continue

        strings = []
        flatten_strings(data, strings)

        found = False
        for s in strings:
            idx = s.find(anchor)
            if idx != -1:
                found = True
                start = max(0, idx - 100)
                end = min(len(s), idx + len(anchor) + 100)
                print(f"  repr window: {s[start:end]!r}")
        if not found:
            print("  ANCHOR NOT FOUND in any text field on this post.")


if __name__ == "__main__":
    main()
