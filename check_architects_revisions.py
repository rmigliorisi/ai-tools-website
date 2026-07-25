"""
Read-only diagnostic — does NOT change anything on the site.

Lists every stored revision of the "Claude for Architects" cross_reference
post (ID 375) and checks whether each revision's content still parses as
valid JSON. The live post_content is currently corrupted (WordPress's editor
auto-formatting mangled the raw JSON blob during a manual admin save on
2026-07-22), so this script finds the most recent revision from BEFORE that
happened, so we know exactly what to restore.

Run:
    python3 check_architects_revisions.py
"""

import json
import sys

import requests
from wp_creds import AUTH, WP_URL

POST_ID = 375  # claude-architects


def try_parse(raw_html):
    """WP wraps content in a <p> sometimes; strip outer tags before parsing."""
    text = raw_html.strip()
    try:
        json.loads(text)
        return True, None
    except json.JSONDecodeError as e:
        return False, str(e)


def main():
    resp = requests.get(
        f"{WP_URL}/wp/v2/cross_reference/{POST_ID}/revisions",
        params={"context": "edit", "_fields": "id,date,modified,content"},
        auth=AUTH,
    )
    resp.raise_for_status()
    revisions = resp.json()

    if not revisions:
        print("No revisions found (or not authorized to view them).")
        sys.exit(1)

    print(f"Found {len(revisions)} revision(s) for post {POST_ID}.\n")

    # Also check the live/current post itself for reference.
    live = requests.get(
        f"{WP_URL}/wp/v2/cross_reference/{POST_ID}",
        params={"context": "edit", "_fields": "id,modified,content"},
        auth=AUTH,
    )
    live.raise_for_status()
    live_data = live.json()
    live_ok, live_err = try_parse(live_data["content"]["raw"])
    print(f"LIVE POST — modified {live_data['modified']} — valid JSON: {live_ok}")
    if not live_ok:
        print(f"    parse error: {live_err}")
    print()

    print(f"{'ID':<8}{'Date':<22}{'Valid JSON':<12}Notes")
    print("-" * 70)

    first_valid_from_top = None  # revisions are newest-first

    for rev in revisions:
        raw = rev.get("content", {}).get("raw", "")
        ok, err = try_parse(raw)
        note = ""
        if ok:
            note = "1M token" in raw and "publish_date" in raw and "2026-07-16" in raw
            note = "has July 16 patch" if note else "valid, check content"
            if first_valid_from_top is None:
                first_valid_from_top = rev["id"]
        else:
            note = (err or "")[:50]
        print(f"{rev['id']:<8}{rev['date']:<22}{str(ok):<12}{note}")

    print()
    if first_valid_from_top:
        print(f"--> Most recent VALID revision: ID {first_valid_from_top}")
        print("    This is the one we'd restore from.")
    else:
        print("--> No valid revision found at all — would need manual reconstruction.")


if __name__ == "__main__":
    main()
