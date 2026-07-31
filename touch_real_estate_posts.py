"""
Diagnostic "touch" — re-saves chatgpt-real-estate and claude-real-estate with
their EXACT existing content, unchanged. This is a true no-op write: nothing
about the page's content or meta changes.

Why: both cross-reference pages are consistently missing from their sibling
pages' "Related Guides" grids (confirmed live on /chatgpt/legal/ and other
siblings), even though their linked_tool/linked_profession post meta is
verified correct and the template's query logic (aifp_get_cross_references_
for_tool() in inc/helpers.php) has no code path that would exclude them.
That combination — correct data, correct code, wrong live behavior — points
at a stale cache somewhere between the database and the rendered page
(likely a persistent object cache on WP.com's end), not a real bug.

A save/update fires WordPress's standard cache-invalidation hooks
(clean_post_cache, meta cache group busting) regardless of whether the
content actually changed. If that's the real cause, this resave should
clear it. If Real Estate is STILL missing from sibling pages' Related
Guides after this runs, that rules out simple caching and means the next
step is a real code-level debug, not more cache-clearing attempts.

Run:
    python3 touch_real_estate_posts.py

Then check https://aitoolsforpros.com/chatgpt/legal/ and
https://aitoolsforpros.com/claude/legal/ (or any sibling) for a Real Estate
entry in Related Guides — give WP.com/CDN caching a minute or two first.
"""

import json

import requests
from wp_creds import AUTH, WP_URL

POSTS_TO_TOUCH = [
    {"post_id": 363, "slug": "chatgpt-real-estate"},
    {"post_id": 371, "slug": "claude-real-estate"},
]


def main():
    for item in POSTS_TO_TOUCH:
        post_id = item["post_id"]
        print(f"\n=== {item['slug']} (post {post_id}) ===")

        resp = requests.get(
            f"{WP_URL}/wp/v2/cross_reference/{post_id}",
            params={"context": "edit", "_fields": "id,content"},
            auth=AUTH,
        )
        resp.raise_for_status()
        raw = resp.json()["content"]["raw"]

        # Validate it's parseable before touching anything — abort rather
        # than resave something that's already broken.
        try:
            json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"  ABORT — existing content isn't valid JSON ({e}). Not touching this post.")
            continue

        put_resp = requests.post(
            f"{WP_URL}/wp/v2/cross_reference/{post_id}",
            headers={
                "X-HTTP-Method-Override": "PUT",
                "Content-Type": "application/json; charset=utf-8",
            },
            auth=AUTH,
            # Re-send the exact same raw string, unmodified — a true no-op write.
            data=json.dumps({"content": raw}, ensure_ascii=False).encode("utf-8"),
        )
        put_resp.raise_for_status()
        print(f"  Re-saved post {post_id} with unchanged content (cache-busting touch).")

    print("\nDone. Give WP.com/CDN caching a minute, then check /chatgpt/legal/ and")
    print("/claude/legal/ (or any sibling) for Real Estate in Related Guides.")


if __name__ == "__main__":
    main()
