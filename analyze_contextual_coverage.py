"""
Checks a specific premise before deciding whether to de-link the
comparison table / "Comparing your options" footer: for each sibling tool
a cross_reference page links to in the table/footer, is that same tool
ALSO linked contextually somewhere in the actual analysis prose (the
content_sections body — limitation cards, feature discussion, etc.), not
just in the table or footer?

If yes for all siblings, trimming the table/footer links would be safe
(a genuine, relevant, contextual link already exists elsewhere for a
reader to click through). If a sibling has NO contextual link anywhere on
the page, that's a real gap worth filling with an actual in-prose
mention — not something to fix by deleting the only link that exists.

Does not change anything.

Run:
    python3 analyze_contextual_coverage.py > contextual_coverage_report.txt
"""

import json
import re

import requests
from wp_creds import AUTH, WP_URL

STYLE_MARKER = "2563eb"  # inline body-link style used for contextual mentions

COMPARING_RE = re.compile(
    r"Comparing your options\? Also see (.*?)\.\s*For the full picture",
    re.DOTALL,
)
A_TAG_RE = re.compile(
    r'<a\s+href=\\?"([^"\\]+)\\?"(?:\s+style=\\?"([^"\\]*)\\?")?[^>]*>(.*?)<\/a>',
    re.DOTALL,
)


def tool_slug(href):
    parts = [p for p in href.strip("/").split("/") if p]
    return parts[0] if parts else None


def collect_all_links(value, out):
    """out: list of (tool_slug, is_contextual, source_field_hint)"""
    if isinstance(value, str):
        for m in A_TAG_RE.finditer(value):
            href, style, text = m.group(1), m.group(2), m.group(3)
            slug = tool_slug(href)
            if not slug:
                continue
            is_contextual = style is not None and STYLE_MARKER in style
            out.append((slug, is_contextual, value[:40]))
    elif isinstance(value, list):
        for v in value:
            collect_all_links(v, out)
    elif isinstance(value, dict):
        for v in value.values():
            collect_all_links(v, out)


def get_table_footer_targets(data):
    """Returns the set of tool slugs linked in the table or the
    'Comparing your options' footer specifically (the non-contextual
    structural spots)."""
    targets = set()

    comparison_notes = data.get("comparison_notes", "")
    for m in A_TAG_RE.finditer(comparison_notes if isinstance(comparison_notes, str) else ""):
        slug = tool_slug(m.group(1))
        if slug:
            targets.add(slug)

    for section in data.get("content_sections", []):
        body = section.get("section_body", "")
        if not isinstance(body, str):
            continue
        cm = COMPARING_RE.search(body)
        if cm:
            for m in A_TAG_RE.finditer(cm.group(1)):
                slug = tool_slug(m.group(1))
                if slug:
                    targets.add(slug)

    return targets


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


def main():
    posts = fetch_all_cross_references()
    print(f"Fetched {len(posts)} cross_reference posts.\n")

    fully_covered = 0
    gaps_total = 0

    for post in posts:
        post_id = post["id"]
        slug = post["slug"]
        raw = post["content"]["raw"]

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"=== {slug} (post {post_id}) === INVALID JSON ({e}) — skipped")
            continue

        table_footer_targets = get_table_footer_targets(data)

        all_links = []
        collect_all_links(data, all_links)
        contextual_slugs = {s for s, is_ctx, _ in all_links if is_ctx}

        missing = sorted(table_footer_targets - contextual_slugs)

        if missing:
            gaps_total += len(missing)
            print(f"=== {slug} (post {post_id}) === GAP — no contextual link for: {missing}")
        else:
            fully_covered += 1
            print(f"=== {slug} (post {post_id}) === OK — all {sorted(table_footer_targets)} have contextual links elsewhere")

    print(f"\n\nPages fully covered (safe to trim table/footer links): {fully_covered}")
    print(f"Total missing contextual-link gaps across all pages: {gaps_total}")


if __name__ == "__main__":
    main()
