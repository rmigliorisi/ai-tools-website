"""
Second-round content fix — shortens quick_facts.hipaa_fact for three more
tools that got the same long-paragraph treatment as the July 25 System 1
live run (Grammarly/ChatGPT/Gemini were fixed in fix_quickfacts_length.py;
these three were found in a follow-up full-site scan and confirmed live via
the Weekly Update Log admin screen).

- Perplexity (345): the worst of the three — a ~35-word paragraph quoting
  Perplexity's Enterprise pages verbatim. Same severity as the original
  Grammarly/ChatGPT/Gemini bugs, just missed from the first patch script.
- Claude (344) and Otter (352): borderline-long (~20-24 words) rather than
  fully broken, but longer than the site's short-label style. Tightened for
  consistency now that we're doing a final pass before turning on the
  weekly schedule.

The underlying facts are unchanged and were already verified real — this
only rewrites the *display* value to match the site's short-label format.

Run:
    python3 fix_hipaa_facts_round2.py
"""

import json

import requests
from wp_creds import AUTH, WP_URL

FIXES = [
    {
        "post_id": 345,  # perplexity
        "name": "Perplexity",
        "changes": {
            "hipaa_fact": "BAA required (Enterprise, HIPAA-aligned)",
        },
    },
    {
        "post_id": 344,  # claude
        "name": "Claude",
        "changes": {
            "hipaa_fact": "BAA available (Enterprise only)",
        },
    },
    {
        "post_id": 352,  # otter
        "name": "Otter",
        "changes": {
            "hipaa_fact": "BAA available (Enterprise plan)",
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
