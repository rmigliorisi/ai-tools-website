"""
Restores the "Claude for Architects" cross_reference post (ID 375) content
from revision 983 (2026-07-16, last known-good JSON, includes the "1M token"
patch) — undoing the corruption caused by the 2026-07-22 manual WP Admin
resave (WordPress's editor auto-formatting mangled the raw JSON blob).

Confirms the revision content is still valid JSON before writing anything,
and re-checks the live page after the write.

Run:
    python3 restore_architects_content.py
"""

import json
import sys

import requests
from wp_creds import AUTH, WP_URL

POST_ID = 375       # claude-architects
GOOD_REVISION_ID = 983


def main():
    # 1. Fetch the known-good revision content.
    resp = requests.get(
        f"{WP_URL}/wp/v2/cross_reference/{POST_ID}/revisions/{GOOD_REVISION_ID}",
        params={"context": "edit", "_fields": "id,date,content"},
        auth=AUTH,
    )
    resp.raise_for_status()
    revision = resp.json()
    raw = revision["content"]["raw"]

    # 2. Validate it's actually parseable JSON before we do anything else.
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"ABORT — revision {GOOD_REVISION_ID} is not valid JSON: {e}")
        sys.exit(1)

    print(f"Revision {GOOD_REVISION_ID} ({revision['date']}) is valid JSON.")
    print(f"  publish_date: {data.get('publish_date')}")
    print(f"  bottom_line mentions 1M: {'1M' in data.get('consistency_blocks', {}).get('bottom_line', '')}")

    # 3. Write it back to the live post.
    put_resp = requests.post(
        f"{WP_URL}/wp/v2/cross_reference/{POST_ID}",
        headers={
            "X-HTTP-Method-Override": "PUT",
            "Content-Type": "application/json; charset=utf-8",
        },
        auth=AUTH,
        data=json.dumps({"content": raw}, ensure_ascii=False).encode("utf-8"),
    )
    put_resp.raise_for_status()
    print(f"\nWrote restored content back to post {POST_ID}.")

    # 4. Re-fetch and confirm it's valid JSON now.
    verify = requests.get(
        f"{WP_URL}/wp/v2/cross_reference/{POST_ID}",
        params={"context": "edit", "_fields": "id,modified,content"},
        auth=AUTH,
    )
    verify.raise_for_status()
    v_data = verify.json()
    try:
        json.loads(v_data["content"]["raw"])
        print(f"VERIFIED — live post (modified {v_data['modified']}) is now valid JSON.")
    except json.JSONDecodeError as e:
        print(f"WARNING — post-write content still doesn't parse: {e}")
        sys.exit(1)

    print("\nDone. Check https://aitoolsforpros.com/claude/architects/ in a minute or two")
    print("(WP.com/CDN caching may delay the visible update slightly).")


if __name__ == "__main__":
    main()
