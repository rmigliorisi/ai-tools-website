#!/usr/bin/env python3
"""
Patch script: re-extracts content from HTML and updates WP posts.
Usage: python3 dev/patch_consistency_blocks.py chatgpt
       python3 dev/patch_consistency_blocks.py all
       python3 dev/patch_consistency_blocks.py cursor notion-ai grammarly otter
"""
import sys, json, re, requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from migrate_v2 import (extract_consistency_blocks, extract_quick_facts_tool,
                        extract_positioning_statement, extract_definition_sentence,
                        extract_faq, extract_sources, extract_reviews_miss,
                        extract_section_clean_html, extract_section_by_label,
                        extract_section_html, extract_pricing_html, extract_comparison_html,
                        clean_html, sanitize,
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


def extract_features(html):
    """Extract features: h3-based (standard) or .feature-item (class-based)."""
    features = []
    features_section = extract_section_html(html, "Features That Matter")
    if features_section:
        h3s = list(re.finditer(r'<h3[^>]*>(.*?)</h3>', features_section, re.DOTALL))
        for i, h3 in enumerate(h3s):
            name = sanitize(h3.group(1))
            start = h3.end()
            end = h3s[i + 1].start() if i + 1 < len(h3s) else len(features_section)
            features.append({
                "feature_name": name,
                "feature_icon": "",
                "feature_description": clean_html(features_section[start:end]),
            })
    if not features:
        fi_items = re.findall(
            r'<li[^>]*class="feature-item"[^>]*>.*?'
            r'<div[^>]*class="feature-name"[^>]*>(.*?)</div>.*?'
            r'<div[^>]*class="feature-desc"[^>]*>(.*?)</div>.*?</li>',
            features_section or html, re.DOTALL
        )
        for name, desc in fi_items[:7]:
            features.append({
                "feature_name": sanitize(name),
                "feature_icon": "",
                "feature_description": sanitize(desc),
            })
    return features[:7]


def extract_what_it_is(html):
    w = extract_section_clean_html(html, "What .* Is")
    if not w:
        w = extract_section_clean_html(html, "What It Is")
    if not w:
        w = extract_section_by_label(html, "Overview")
    return w


def extract_who_right_for(html):
    w = extract_section_clean_html(html, "Who .* Right For")
    if not w:
        w = extract_section_clean_html(html, "Who It")
    if not w:
        w = extract_section_by_label(html, "Fit Assessment")
    return w


def extract_verdict(html):
    v = extract_section_clean_html(html, "My Verdict")
    if not v:
        v = extract_section_clean_html(html, "Our Verdict")
    if not v:
        v = extract_section_by_label(html, "My Verdict")
    return v


def patch_tool(slug):
    html_file = BASE_DIR / f"{slug}.html"
    if not html_file.exists():
        print(f"  SKIP {slug} — {html_file} not found")
        return

    html = html_file.read_text(encoding="utf-8")
    blocks   = extract_consistency_blocks(html)
    facts    = extract_quick_facts_tool(html)
    features = extract_features(html)
    faq      = extract_faq(html)
    sources  = extract_sources(html)
    rm       = extract_reviews_miss(html)
    what_it  = extract_what_it_is(html)
    who_for  = extract_who_right_for(html)
    verdict  = extract_verdict(html)

    post_id = get_post_id(slug)
    if not post_id:
        print(f"  SKIP {slug} — no WordPress post found")
        return

    r = requests.get(f"{WP_URL}/wp/v2/tool_review/{post_id}?context=edit", auth=AUTH)
    data = json.loads(r.json()["content"]["raw"])

    pricing_h  = extract_pricing_html(html)
    compare_h  = extract_comparison_html(html)

    data["consistency_blocks"]    = blocks
    data["quick_facts"]           = facts
    data["positioning_statement"] = extract_positioning_statement(html)
    data["definition_sentence"]   = extract_definition_sentence(html)
    data["features"]              = features
    data["faq"]                   = faq
    data["sources"]               = sources
    data["reviews_miss"]          = rm
    if what_it:
        data["what_it_is"]        = what_it[:10000]
    if who_for:
        data["who_its_right_for"] = who_for[:10000]
    if verdict:
        data["verdict_text"]      = verdict[:10000]
    if pricing_h:
        data["pricing_html"]      = pricing_h[:10000]
    if compare_h:
        data["comparison_html"]   = compare_h[:10000]

    new_content = json.dumps(data, ensure_ascii=False)

    resp = requests.post(
        f"{WP_URL}/wp/v2/tool_review/{post_id}",
        auth=AUTH,
        json={"content": new_content},
    )
    if resp.status_code in (200, 201):
        print(f"  OK  {slug} (post {post_id})")
        print(f"      key_takeaway:   {len(blocks.get('key_takeaway',''))} chars")
        print(f"      features:       {len(features)} items")
        print(f"      faq:            {len(faq)} items")
        print(f"      sources:        {len(sources)} items")
        insights = rm.get('insights', [])
        print(f"      insights:       {len(insights)} items")
        print(f"      banner:         {len(rm.get('insight_banner',''))} chars")
        print(f"      what_it_is:     {len(what_it)} chars")
        print(f"      who_right_for:  {len(who_for)} chars")
        print(f"      verdict_text:   {len(verdict)} chars")
    else:
        print(f"  FAIL {slug} — {resp.status_code}: {resp.text[:200]}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        target = "chatgpt"
    elif sys.argv[1] == "all":
        target = "all"
    else:
        target = None

    if target == "all":
        slugs = TOOLS
    elif target:
        slugs = [target]
    else:
        slugs = sys.argv[1:]

    for slug in slugs:
        patch_tool(slug)
