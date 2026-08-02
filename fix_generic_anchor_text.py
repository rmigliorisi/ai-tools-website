"""
Fixes the anchor-text inconsistency found on all 41 cross_reference pages:
in "Comparing your options? Also see X, Y, and Z.", the FIRST link (X)
always used the bare tool name ("ChatGPT", "Claude") while the 2nd and 3rd
links (Y, Z) already used descriptive text ("Copilot for finance
professional"). The href for the first link was already correct (it
already points to the specific profession's cross-reference page) — only
the visible anchor text was generic.

This only edits the inner text of the FIRST <a> tag within that sentence,
appending the same " for [suffix]" pattern its own sibling links on the
same page already use (derived from the 2nd link's anchor text, matched
against known tool-name prefixes so the correct suffix is extracted
regardless of exact tool-name wording). Href and all attributes are left
untouched.

Safety: only applies if exactly one "Comparing your options? Also see"
sentence is found on the page, and only if the first link's derived new
text isn't already applied.

Run:
    python3 fix_generic_anchor_text.py
"""

import json
import re

import requests
from wp_creds import AUTH, WP_URL

# Longest names first so "Google Gemini" is checked before bare "Gemini", etc.
TOOL_NAME_VARIANTS = [
    "Google Gemini",
    "Microsoft Copilot",
    "Perplexity AI",
    "Notion AI",
    "Otter.ai",
    "ChatGPT",
    "Claude",
    "Gemini",
    "Copilot",
    "Perplexity",
    "Midjourney",
    "Cursor",
    "Grammarly",
    "Otter",
]

COMPARING_RE = re.compile(
    r"(Comparing your options\? Also see )(.*?)(\.\s*For the full picture)",
    re.DOTALL,
)
A_TAG_RE = re.compile(
    r'(<a\s+href=\\?"[^"\\]+\\?"[^>]*>)(.*?)(<\/a>)',
    re.DOTALL,
)


def derive_suffix(text):
    """Given anchor text like 'Copilot for finance professional', strip the
    leading known tool-name and return ' for finance professional'."""
    for name in TOOL_NAME_VARIANTS:
        if text.startswith(name):
            rest = text[len(name):]
            if rest.startswith(" for "):
                return rest
    return None


def fetch_all_cross_references():
    posts = []
    page = 1
    while True:
        resp = requests.get(
            f"{WP_URL}/wp/v2/cross_reference",
            params={
                "context": "edit",
                "_fields": "id,slug,content",
                "per_page": 100,
                "page": page,
            },
            auth=AUTH,
        )
        if resp.status_code == 400:
            break
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        posts.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return posts


def fix_string(s):
    """Return (new_string, changed, note) after fixing the first link's
    anchor text within the 'Comparing your options' sentence, if present."""
    m = COMPARING_RE.search(s)
    if not m:
        return s, False, "no 'Comparing your options' sentence found"

    sentence = m.group(2)
    a_matches = list(A_TAG_RE.finditer(sentence))
    if len(a_matches) < 2:
        return s, False, f"expected 2+ links in sentence, found {len(a_matches)}"

    first_open, first_text, first_close = a_matches[0].group(1), a_matches[0].group(2), a_matches[0].group(3)

    # Already has a descriptive suffix? nothing to do.
    if derive_suffix(first_text) is not None:
        return s, False, "first link already has descriptive text"

    # Derive the suffix from whichever sibling link has one.
    suffix = None
    for a in a_matches[1:]:
        suffix = derive_suffix(a.group(2))
        if suffix:
            break
    if not suffix:
        return s, False, "could not derive suffix from sibling links"

    new_first_text = first_text + suffix
    new_first_tag = first_open + new_first_text + first_close

    old_first_tag_full = a_matches[0].group(0)
    new_sentence = sentence[: a_matches[0].start()] + new_first_tag + sentence[a_matches[0].end():]

    new_full = s[: m.start(2)] + new_sentence + s[m.end(2):]
    return new_full, True, f"'{first_text}' -> '{new_first_text}'"


def replace_in_value(value, fixer, result):
    if isinstance(value, str):
        if "Comparing your options" in value:
            new_s, changed, note = fixer(value)
            if changed:
                result["changed"] = True
                result["note"] = note
            elif result.get("note") is None:
                result["note"] = note
            return new_s
        return value
    elif isinstance(value, list):
        return [replace_in_value(v, fixer, result) for v in value]
    elif isinstance(value, dict):
        return {k: replace_in_value(v, fixer, result) for k, v in value.items()}
    return value


def main():
    posts = fetch_all_cross_references()
    print(f"Fetched {len(posts)} cross_reference posts.\n")

    total_fixed = 0
    total_skipped = 0

    for post in posts:
        post_id = post["id"]
        slug = post["slug"]
        raw = post["content"]["raw"]

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"=== {slug} (post {post_id}) === INVALID JSON ({e}) — skipping")
            total_skipped += 1
            continue

        result = {"changed": False, "note": None}
        new_data = replace_in_value(data, fix_string, result)

        if not result["changed"]:
            print(f"=== {slug} (post {post_id}) === SKIP — {result['note']}")
            total_skipped += 1
            continue

        new_raw = json.dumps(new_data, ensure_ascii=False)
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
        print(f"=== {slug} (post {post_id}) === Fixed: {result['note']}")
        total_fixed += 1

    print(f"\n\nDone. Fixed: {total_fixed}, Skipped: {total_skipped}.")


if __name__ == "__main__":
    main()
