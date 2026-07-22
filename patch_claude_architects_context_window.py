#!/usr/bin/env python3
"""
System 3 (Monthly Cross-Reference Editorial Review) — first approved edit.

Updates the /claude/architects/ cross_reference page (post 375) to reflect
Claude Sonnet 5's 1M token context window (up from 200K), confirmed on
Anthropic's own Help Center / platform docs as available on Claude.ai Pro
plans, not just via API. This is the exact, human-approved edit from the
first System 3 report — see docs/AIFORPROS-AUTOMATED-CONTENT.md "System 3"
for the process this came from. Four targeted text replacements only; nothing
else on the page changes.

Run locally:
    python3 patch_claude_architects_context_window.py
"""

import json
from wp_creds import AUTH, WP_URL
import requests

POST_ID = 375
ENDPOINT = f"{WP_URL}/wp/v2/cross_reference/{POST_ID}"

REPLACEMENTS = [
    (
        "200K context window is the key differentiator for architectural practice.",
        "1M token context window is the key differentiator for architectural practice.",
    ),
    (
        "200K context, processes entire spec packages",
        "1M token context, processes entire spec packages and then some",
    ),
    (
        "200K context window accommodates very large documents.",
        "1M token context window accommodates very large documents.",
    ),
    (
        "the 200K context window matters more than prose style",
        "the 1M token context window matters more than prose style",
    ),
]

NEW_PUBLISH_DATE = "2026-07-16"


def main():
    # 1. Fetch current raw content (context=edit gives the unprocessed JSON string)
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
        print("FAILED: content.raw was empty — check that the request used context=edit and the "
              "authenticated user has edit rights on this post type.")
        return

    # 2. Apply the four approved text replacements, decode->modify->re-encode so we
    #    never hand-type the full JSON blob back (this page's content object is large).
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
        print("FAILED: none of the expected replacements matched — page may have changed since "
              "the report was generated. Aborting without writing anything.")
        return

    data = json.loads(content_str)
    data["publish_date"] = NEW_PUBLISH_DATE

    # 3. Write back
    payload = {"content": json.dumps(data, ensure_ascii=False)}
    req = requests.Request("POST", ENDPOINT, json=payload, auth=AUTH)
    prepared = req.prepare()
    prepared.headers["X-HTTP-Method-Override"] = "PUT"

    with requests.Session() as s:
        resp = s.send(prepared, timeout=30)

    if resp.status_code in (200, 201):
        print(f"OK — applied {applied}/{len(REPLACEMENTS)} replacements to post {POST_ID} "
              f"(/claude/architects/), publish_date set to {NEW_PUBLISH_DATE}.")
    else:
        print(f"FAILED: HTTP {resp.status_code}")
        try:
            print(resp.json())
        except Exception:
            print(resp.text[:500])


if __name__ == "__main__":
    main()
