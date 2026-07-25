"""
One-off fix: the on-page date badge reads data['publish_date'] (a static
field baked into the JSON blob), not WordPress's real post_modified
timestamp. Every tool_review page edited today (2026-07-25) — via the live
System 1 run and the two follow-up quick_facts patch scripts — still shows
its old, stale publish_date even though the content genuinely changed.

This script uses each post's real `modified` timestamp (ground truth) to
decide which pages were actually touched today, and bumps publish_date to
match for those only — untouched pages (e.g. Copilot, Midjourney, if no
change applied to them today) are left alone.

Going forward, automation/weekly_tool_update.py now bumps publish_date
itself whenever it writes a real change, so this script should not need to
be re-run for future weekly runs.

Run:
    python3 fix_stale_publish_dates.py
"""

import json
from datetime import date

import requests
from wp_creds import AUTH, WP_URL

TODAY = date.today().isoformat()  # 2026-07-25


def main():
    resp = requests.get(
        f"{WP_URL}/wp/v2/tool_review",
        params={"per_page": 100, "context": "edit", "_fields": "id,slug,modified,content"},
        auth=AUTH,
    )
    resp.raise_for_status()
    posts = resp.json()

    for post in posts:
        modified_date = post["modified"][:10]  # "2026-07-25T09:49:12" -> "2026-07-25"
        if modified_date != TODAY:
            print(f"SKIP {post['slug']} — last modified {modified_date}, not today")
            continue

        raw = post["content"]["raw"]
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"SKIP {post['slug']} — content isn't valid JSON ({e}), needs manual look")
            continue

        old_pub_date = data.get("publish_date", "")
        if old_pub_date == TODAY:
            print(f"SKIP {post['slug']} — publish_date already {TODAY}")
            continue

        data["publish_date"] = TODAY
        put_resp = requests.post(
            f"{WP_URL}/wp/v2/tool_review/{post['id']}",
            headers={
                "X-HTTP-Method-Override": "PUT",
                "Content-Type": "application/json; charset=utf-8",
            },
            auth=AUTH,
            data=json.dumps({"content": json.dumps(data, ensure_ascii=False)}, ensure_ascii=False).encode("utf-8"),
        )
        put_resp.raise_for_status()
        print(f"UPDATED {post['slug']} — publish_date: {old_pub_date!r} -> {TODAY!r}")

    print("\nDone. Give WP.com/CDN caching a minute, then spot-check a page or two.")


if __name__ == "__main__":
    main()
