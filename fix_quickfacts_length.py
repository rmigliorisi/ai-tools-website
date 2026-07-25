"""
One-off content fix — shortens three quick_facts values that the July 25
System 1 live run wrote as full explanatory sentences instead of short
labels, which visibly broke the Quick Facts card grid (confirmed live on
Grammarly's page via screenshot: the "Made By" and "HIPAA/Compliant" cards
stretched to ~14 lines while their siblings stayed at 2-3 lines).

The underlying facts are correct and were verified real (Grammarly's rebrand
to Superhuman, its new BAA availability, ChatGPT for Healthcare, Google's
Plus/Pro/Ultra restructuring) — this script only rewrites the *display*
value to match the site's existing short-label style, matching the
now-updated schema instructions and length guardrail in
automation/weekly_tool_update.py.

Run:
    python3 fix_quickfacts_length.py
"""

import json

import requests
from wp_creds import AUTH, WP_URL

FIXES = [
    {
        "post_id": 351,  # grammarly
        "name": "Grammarly",
        "changes": {
            "made_by": "Superhuman (Grammarly's parent)",
            "hipaa_fact": "BAA available (Business/Enterprise)",
        },
    },
    {
        "post_id": 343,  # chatgpt
        "name": "ChatGPT",
        "changes": {
            "hipaa_fact": "Enterprise or Healthcare plan (BAA)",
        },
    },
    {
        "post_id": 346,  # gemini
        "name": "Google Gemini",
        "changes": {
            "pricing_fact": "Google AI Plus/Pro/Ultra (~$19.99+/mo)",
        },
    },
]


def main():
    for fix in FIXES:
        post_id = fix["post_id"]
        print(f"\n=== {fix['name']} (post {post_id}) ===")

        resp = requests.get(
            f"{WP_URL}/wp/v2/tool_review/{post_id}",
            params={"context": "edit", "_fields": "id,content"},
            auth=AUTH,
        )
        resp.raise_for_status()
        raw = resp.json()["content"]["raw"]
        data = json.loads(raw)

        qf = data.setdefault("quick_facts", {})
        for key, new_value in fix["changes"].items():
            old_value = qf.get(key, "")
            print(f"  {key}:")
            print(f"    old ({len(old_value)} chars): {old_value[:80]}{'...' if len(old_value) > 80 else ''}")
            print(f"    new ({len(new_value)} chars): {new_value}")
            qf[key] = new_value

        put_resp = requests.post(
            f"{WP_URL}/wp/v2/tool_review/{post_id}",
            headers={
                "X-HTTP-Method-Override": "PUT",
                "Content-Type": "application/json; charset=utf-8",
            },
            auth=AUTH,
            data=json.dumps({"content": json.dumps(data, ensure_ascii=False)}, ensure_ascii=False).encode("utf-8"),
        )
        put_resp.raise_for_status()
        print(f"  Wrote update to post {post_id}.")

    print("\nDone. Give WP.com/CDN caching a minute, then check each page.")


if __name__ == "__main__":
    main()
