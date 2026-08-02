"""
Fixes the "stripped inline link" bug found on 6 cross_reference pages during
the internal-link audit. In each case, an <a> tag that used to wrap a tool
name lost its markup AND the surrounding whitespace, producing run-on text
like "usePerplexity AIor access primary literature directly" instead of
"use Perplexity AI or access primary literature directly" with a working link.

This restores both the missing link and the missing spaces. Link targets
follow the pattern already used for other inline (mid-paragraph) tool
mentions on the same pages: general tool overview pages (/perplexity/,
/chatgpt/, /copilot/), not profession-specific pages — matching the style
`color:#2563eb;text-decoration:none;font-weight:500;` used elsewhere in the
same documents for this kind of mention.

Safety: for each (old, new) pair, the script counts occurrences of `old` in
the page's decoded text fields first. It only applies the replacement if the
count is exactly 1 — if 0 (already fixed / text changed) or 2+ (ambiguous),
it skips that fix and reports it, rather than guessing.

Run:
    python3 fix_stripped_links.py
"""

import json

import requests
from wp_creds import AUTH, WP_URL

LINK_STYLE = "color:#2563eb;text-decoration:none;font-weight:500;"

# post_id, slug, and a list of (old_text, new_text) plain-text replacements
# to apply to the decoded JSON structure.
FIXES = [
    {
        "post_id": 370,
        "slug": "claude-physicians",
        "replacements": [
            (
                "For current evidence, usePerplexity AIor access primary literature directly.",
                f'For current evidence, use <a href="/perplexity/" style="{LINK_STYLE}">Perplexity AI</a> or access primary literature directly.',
            ),
        ],
    },
    {
        "post_id": 373,
        "slug": "claude-finance",
        "replacements": [
            (
                "For current market context, pair Claude withPerplexity AI, which provides Search-grounded, cited answers to current financial questions.",
                f'For current market context, pair Claude with <a href="/perplexity/" style="{LINK_STYLE}">Perplexity AI</a>, which provides Search-grounded, cited answers to current financial questions.',
            ),
            (
                "Claude cannot receive uploaded spreadsheet files and analyze the data directly (at least not in the same way asChatGPTPlus’s Code Interpreter).",
                f'Claude cannot receive uploaded spreadsheet files and analyze the data directly (at least not in the same way as <a href="/chatgpt/" style="{LINK_STYLE}">ChatGPT</a> Plus’s Code Interpreter).',
            ),
        ],
    },
    {
        "post_id": 374,
        "slug": "claude-insurance",
        "replacements": [
            (
                "For current regulatory guidance, usePerplexity AIto find and verify primary source documents.",
                f'For current regulatory guidance, use <a href="/perplexity/" style="{LINK_STYLE}">Perplexity AI</a> to find and verify primary source documents.',
            ),
            (
                "If you need AI assistance directly inside Word, Excel, or Outlook,Microsoft Copilotoffers better integration.",
                f'If you need AI assistance directly inside Word, Excel, or Outlook, <a href="/copilot/" style="{LINK_STYLE}">Microsoft Copilot</a> offers better integration.',
            ),
            (
                "Many professionals use both: Claude for document analysis,Copilotfor the M365 writing workflow.",
                f'Many professionals use both: Claude for document analysis, <a href="/copilot/" style="{LINK_STYLE}">Copilot</a> for the M365 writing workflow.',
            ),
        ],
    },
    {
        "post_id": 372,
        "slug": "claude-engineers",
        "replacements": [
            (
                "There is no inline autocomplete, no tab-to-accept suggestion, and no direct file editing. For that workflow, Cursor or GitHubCopilotis the right tool.",
                f'There is no inline autocomplete, no tab-to-accept suggestion, and no direct file editing. For that workflow, Cursor or GitHub <a href="/copilot/" style="{LINK_STYLE}">Copilot</a> is the right tool.',
            ),
        ],
    },
    {
        "post_id": 383,
        "slug": "gemini-finance",
        "replacements": [
            (
                "LikeMicrosoft Copilotfor M365, Gemini’s integration features only provide value if your practice already uses Google Workspace.",
                f'Like <a href="/copilot/" style="{LINK_STYLE}">Microsoft Copilot</a> for M365, Gemini’s integration features only provide value if your practice already uses Google Workspace.',
            ),
            (
                "If you’re on Microsoft 365 or a different suite,Copilotis more relevant.",
                f'If you’re on Microsoft 365 or a different suite, <a href="/copilot/" style="{LINK_STYLE}">Copilot</a> is more relevant.',
            ),
        ],
    },
    {
        "post_id": 371,
        "slug": "claude-real-estate",
        "replacements": [
            (
                "For real-time market lookups,Perplexity AIis the better tool in the stack.",
                f'For real-time market lookups, <a href="/perplexity/" style="{LINK_STYLE}">Perplexity AI</a> is the better tool in the stack.',
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

    print("\nDone. Give WP.com/CDN caching a minute, then spot-check the live pages:")
    for page in FIXES:
        print(f"  https://aitoolsforpros.com/{page['slug'].replace('-', '/', 1)}/")


if __name__ == "__main__":
    main()
