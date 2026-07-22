#!/usr/bin/env python3
"""
Follow-up fix: two more "200K" mentions on /claude/architects/ (post 375) that
were missed in the first pass — both in FAQ answers not covered by
patch_claude_architects_context_window.py. Same System 3 edit, just catching
the rest of it.

Run locally:
    python3 patch_claude_architects_context_window_2.py
"""

import json
from wp_creds import AUTH, WP_URL
import requests

POST_ID = 375
ENDPOINT = f"{WP_URL}/wp/v2/cross_reference/{POST_ID}"

REPLACEMENTS = [
    (
        "advantage is the 200K context window, for reviewing full specification packages",
        "advantage is the 1M token context window, for reviewing full specification packages",
    ),
    (
        "The 200K context advantage is more useful for review and analysis",
        "The 1M token context advantage is more useful for review and analysis",
    ),
]


def main():
    get_resp = requests.get(
        f"{WP_URL}/wp/v2/cross_reference",
        params={"slug": "claude-architects", "context": "edit", "_fields": "id,slug,content"},
        auth=AUTH,
        timeout=30,
    )
    get_resp.raise_for_status()
    posts = get_resp.json()
    if not posts:
        print("FAILED: no post found with slug 'claude-architects'")
        return

    post = posts[0]
    raw = post.get("content", {}).get("raw", "")
    if not raw:
        print("FAILED: content.raw was empty.")
        return

    data = json.loads(raw)
    content_str = json.dumps(data, ensure_ascii=False)

    applied = 0
    for old, new in REPLACEMENTS:
        if old in content_str:
            content_str = content_str.replace(old, new)
            applied += 1
        else:
            print(f"WARNING: expected text not found, skipped: {old[:60]}...")

    if applied == 0:
        print("FAILED: neither replacement matched — aborting without writing anything.")
        return

    data = json.loads(content_str)

    payload = {"content": json.dumps(data, ensure_ascii=False)}
    req = requests.Request("POST", ENDPOINT, json=payload, auth=AUTH)
    prepared = req.prepare()
    prepared.headers["X-HTTP-Method-Override"] = "PUT"

    with requests.Session() as s:
        resp = s.send(prepared, timeout=30)

    if resp.status_code in (200, 201):
        print(f"OK — applied {applied}/{len(REPLACEMENTS)} remaining replacements to post {POST_ID}.")
    else:
        print(f"FAILED: HTTP {resp.status_code}")
        try:
            print(resp.json())
        except Exception:
            print(resp.text[:500])


if __name__ == "__main__":
    main()
