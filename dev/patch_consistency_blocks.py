#!/usr/bin/env python3
"""
Patch script: re-extracts consistency_blocks + quick_facts from HTML and updates WP posts.
Usage: python3 dev/patch_consistency_blocks.py chatgpt
       python3 dev/patch_consistency_blocks.py all
"""
import sys, json, requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from migrate_v2 import (extract_consistency_blocks, extract_quick_facts_tool,
                        extract_positioning_statement, extract_definition_sentence,
                        WP_URL, AUTH)

BASE_DIR = Path("/Users/rmigs/Projects/aitoolsforpros website")

TOOLS = [
    "chatgpt", "claude", "perplexity", "gemini", "copilot",
    "midjourney", "cursor", "notion-ai", "grammarly", "otter",
]


def get_post_id(slug):
    r = requests.get(f"{WP_URL}/wp/v2/tool_review", params={"slug": slug, "per_page": 1}, auth=AUTH)
    posts = r.json()
    return posts[0]["id"] if posts else None


def patch_tool(slug):
    html_file = BASE_DIR / f"{slug}.html"
    if not html_file.exists():
        print(f"  SKIP {slug} — {html_file} not found")
        return

    html = html_file.read_text(encoding="utf-8")
    blocks = extract_consistency_blocks(html)
    facts  = extract_quick_facts_tool(html)

    post_id = get_post_id(slug)
    if not post_id:
        print(f"  SKIP {slug} — no WordPress post found")
        return

    # Fetch current post_content JSON
    r = requests.get(f"{WP_URL}/wp/v2/tool_review/{post_id}?context=edit", auth=AUTH)
    data = json.loads(r.json()["content"]["raw"])

    # Patch consistency_blocks, quick_facts, and positioning_statement
    data["consistency_blocks"]    = blocks
    data["quick_facts"]           = facts
    data["positioning_statement"] = extract_positioning_statement(html)
    data["definition_sentence"]   = extract_definition_sentence(html)
    new_content = json.dumps(data, ensure_ascii=False)

    resp = requests.post(
        f"{WP_URL}/wp/v2/tool_review/{post_id}",
        auth=AUTH,
        json={"content": new_content},
    )
    if resp.status_code in (200, 201):
        print(f"  OK  {slug} (post {post_id})")
        print(f"      key_takeaway:   {len(blocks.get('key_takeaway',''))} chars")
        print(f"      best_for:       {len(blocks.get('best_for',''))} chars")
        print(f"      avoid_if:       {len(blocks.get('avoid_if',''))} chars")
        print(f"      mini_workflow:  {len(blocks.get('mini_workflow',''))} chars")
        print(f"      made_by:        {facts.get('made_by','(empty)')}")
        print(f"      best_for_fact:  {facts.get('best_for_fact','(empty)')}")
        print(f"      pricing_fact:   {facts.get('pricing_fact','(empty)')}")
        print(f"      custom_label:   {facts.get('custom_fact_label','(empty)')}")
        print(f"      custom_value:   {facts.get('custom_fact_value','(empty)')}")
        print(f"      hipaa_fact:     {facts.get('hipaa_fact','(empty)')}")
    else:
        print(f"  FAIL {slug} — {resp.status_code}: {resp.text[:200]}")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "chatgpt"
    slugs = TOOLS if target == "all" else [target]
    for slug in slugs:
        patch_tool(slug)
