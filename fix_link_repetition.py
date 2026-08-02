"""
Fixes the 5 confirmed "same breath" link-repetition instances found by
analyze_inline_duplicates.py — cases where the same tool gets an inline
blue link twice within one paragraph/limitation card, restating the same
point. The fix de-links only the SECOND mention (converts it to plain
text, keeping the tool name visible) so the sentence still reads
naturally; the first mention keeps its link.

Deliberately excludes the other 4 pages the analysis flagged, where the
same tool is mentioned in two different sections making two different
specific points (e.g. one comparison about code review depth, a separate
one about IDE integration) — that's normal editorial structure, not
repetition, and shouldn't be touched.

Same safety pattern as previous rounds: each replacement only applies if
the exact old text is found exactly once.

Run:
    python3 fix_link_repetition.py
"""

import json

import requests
from wp_creds import AUTH, WP_URL

STYLE = "color:#2563eb;text-decoration:none;font-weight:500;"


def link(href, text):
    return f'<a href="{href}" style="{STYLE}">{text}</a>'


FIXES = [
    {
        "post_id": 389,
        "slug": "copilot-finance",
        "replacements": [
            (
                f'Like Claude and {link("/chatgpt/", "ChatGPT")}, Copilot does not have live market data or current regulatory information. For current rates and recent regulatory guidance, use {link("/perplexity/", "Perplexity AI")}. Copilot handles the writing and analysis work; {link("/perplexity/", "Perplexity")} handles the current-information layer.',
                f'Like Claude and {link("/chatgpt/", "ChatGPT")}, Copilot does not have live market data or current regulatory information. For current rates and recent regulatory guidance, use {link("/perplexity/", "Perplexity AI")}. Copilot handles the writing and analysis work; Perplexity handles the current-information layer.',
            ),
        ],
    },
    {
        "post_id": 383,
        "slug": "gemini-finance",
        "replacements": [
            (
                f'Like {link("/copilot/", "Microsoft Copilot")} for M365, Gemini\'s integration features only provide value if your practice already uses Google Workspace. If you\'re on Microsoft 365 or a different suite, {link("/copilot/", "Copilot")} is more relevant.',
                f'Like {link("/copilot/", "Microsoft Copilot")} for M365, Gemini\'s integration features only provide value if your practice already uses Google Workspace. If you\'re on Microsoft 365 or a different suite, Copilot is more relevant.',
            ),
        ],
    },
    {
        "post_id": 374,
        "slug": "claude-insurance",
        "replacements": [
            (
                f'for your proposal and correspondence workflow, {link("/copilot/", "Microsoft Copilot")} offers better integration. Many professionals use both: Claude for document analysis, {link("/copilot/", "Copilot")} for the M365 writing workflow.',
                f'for your proposal and correspondence workflow, {link("/copilot/", "Microsoft Copilot")} offers better integration. Many professionals use both: Claude for document analysis, Copilot for the M365 writing workflow.',
            ),
        ],
    },
    {
        "post_id": 371,
        "slug": "claude-real-estate",
        "replacements": [
            (
                f'Claude has fewer native integrations with CRM and email platforms than ChatGPT or {link("/copilot/", "Microsoft Copilot")}. Most workflows involve copy-paste. If you need an AI tool that lives inside your email client or CRM, {link("/copilot/", "Copilot")} or a ChatGPT-based integration may be more practical.',
                f'Claude has fewer native integrations with CRM and email platforms than ChatGPT or {link("/copilot/", "Microsoft Copilot")}. Most workflows involve copy-paste. If you need an AI tool that lives inside your email client or CRM, Copilot or a ChatGPT-based integration may be more practical.',
            ),
        ],
    },
    {
        "post_id": 362,
        "slug": "chatgpt-physicians",
        "replacements": [
            (
                f'For real-time encounter transcription, use {link("/otter/", "Otter.ai")} or a dedicated ambient documentation tool. The strongest documentation workflow combines both: {link("/otter/", "Otter.ai")} captures the spoken encounter, ChatGPT formats the transcript into a structured clinical document.',
                f'For real-time encounter transcription, use {link("/otter/", "Otter.ai")} or a dedicated ambient documentation tool. The strongest documentation workflow combines both: Otter.ai captures the spoken encounter, ChatGPT formats the transcript into a structured clinical document.',
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
    total_fixed = 0
    total_skipped = 0
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
                total_skipped += 1
                continue
            if counter[0] > 1:
                print(f"  SKIP — old text found {counter[0]} times (ambiguous, needs manual review): {old[:70]}...")
                total_skipped += 1
                continue
            data = replace_in_value(data, old, new)
            applied_any = True
            total_fixed += 1
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

    print(f"\n\nDone. Fixed: {total_fixed}, Skipped: {total_skipped}.")


if __name__ == "__main__":
    main()
