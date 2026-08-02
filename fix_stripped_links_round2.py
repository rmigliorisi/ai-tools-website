"""
Round 2 — fixes the 4 stripped-link instances that fix_stripped_links.py
correctly skipped (its safety check found 0 occurrences rather than guess).

diagnose_stripped_links.py revealed why:
  - claude-finance & gemini-finance: the apostrophes in the actual stored
    text are straight quotes ('), not the curly quotes (') used in round 1's
    search strings. Same class of bug fixed in system3_monthly.py earlier
    this session (rendered/wptexturized text vs. raw stored text).
  - claude-insurance: the surrounding wording was genuinely different from
    what round 1 assumed ("correspondence workflow," not "or Outlook,").

Same safety pattern as round 1: each replacement only applies if the old
text is found exactly once in the page's decoded text fields.

Run:
    python3 fix_stripped_links_round2.py
"""

import json

import requests
from wp_creds import AUTH, WP_URL

LINK_STYLE = "color:#2563eb;text-decoration:none;font-weight:500;"

FIXES = [
    {
        "post_id": 373,
        "slug": "claude-finance",
        "replacements": [
            (
                "Claude cannot receive uploaded spreadsheet files and analyze the data directly (at least not in the same way asChatGPTPlus's Code Interpreter).",
                f'Claude cannot receive uploaded spreadsheet files and analyze the data directly (at least not in the same way as <a href="/chatgpt/" style="{LINK_STYLE}">ChatGPT</a> Plus\'s Code Interpreter).',
            ),
        ],
    },
    {
        "post_id": 374,
        "slug": "claude-insurance",
        "replacements": [
            (
                "or Outlook for your proposal and correspondence workflow,Microsoft Copilotoffers better integration.",
                f'or Outlook for your proposal and correspondence workflow, <a href="/copilot/" style="{LINK_STYLE}">Microsoft Copilot</a> offers better integration.',
            ),
        ],
    },
    {
        "post_id": 383,
        "slug": "gemini-finance",
        "replacements": [
            (
                "LikeMicrosoft Copilotfor M365, Gemini's integration features only provide value if your practice already uses Google Workspace.",
                f'Like <a href="/copilot/" style="{LINK_STYLE}">Microsoft Copilot</a> for M365, Gemini\'s integration features only provide value if your practice already uses Google Workspace.',
            ),
            (
                "If you're on Microsoft 365 or a different suite,Copilotis more relevant.",
                f'If you\'re on Microsoft 365 or a different suite, <a href="/copilot/" style="{LINK_STYLE}">Copilot</a> is more relevant.',
            ),
        ],
    },
]


def count_occurrences(value, needle, counter):
    if isinstance(value, str):
        counter[0] += value.count(needle)
    elif isinstance(value, list):
        for v in value:
            count_occurrences(v, needle, counter)
    elif isinstance(value, dict):
        for v in value.values():
            count_occurrences(v, needle, counter)


def replace_in_value(value, old, new):
    if isinstance(value, str):
        return value.replace(old, new)
    elif isinstance(value, list):
        return [replace_in_value(v, old, new) for v in value]
    elif isinstance(value, dict):
        return {k: replace_in_value(v, old, new) for k, v in value.items()}
    return value


def main():
    for page in FIXES:
        post_id = page["post_id"]
        slug = page["slug"]
        print(f"\n=== {slug} (post {post_id}) ===")

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
            print(f"  ABORT — existing content isn't valid JSON ({e}). Not touching this post.")
            continue

        applied_any = False
        for old, new in page["replacements"]:
            counter = [0]
            count_occurrences(data, old, counter)
            if counter[0] == 0:
                print(f"  SKIP — old text not found (may already be fixed): {old[:70]}...")
                continue
            if counter[0] > 1:
                print(f"  SKIP — old text found {counter[0]} times (ambiguous, needs manual review): {old[:70]}...")
                continue
            data = replace_in_value(data, old, new)
            applied_any = True
            print(f"  Fixed: {old[:70]}...")

        if not applied_any:
            print("  No changes applied for this post.")
            continue

        new_raw = json.dumps(data, ensure_ascii=False)
        put_resp = requests.post(
            f"{WP_URL}/wp/v2/cross_reference/{post_id}",
            headers={
                "X-HTTP-Method-Override": "PUT",
                "Content-Type": "application/json; charset=utf-8",
            },
            auth=AUTH,
            data=json.dumps({"content": new_raw}, ensure_ascii=False).encode("utf-8"),
        )
        put_resp.raise_for_status()
        print(f"  Saved post {post_id}.")

    print("\nDone. Give WP.com/CDN caching a minute, then spot-check:")
    print("  https://aitoolsforpros.com/claude/finance/")
    print("  https://aitoolsforpros.com/claude/insurance/")
    print("  https://aitoolsforpros.com/gemini/finance/")


if __name__ == "__main__":
    main()
