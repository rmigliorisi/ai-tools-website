#!/usr/bin/env python3
"""
Migrate static HTML content to WordPress via REST API.
Extracts content from existing HTML files and creates posts with ACF fields.
"""

import json
import re
import sys
import os
import requests
from html.parser import HTMLParser
from pathlib import Path

# WordPress credentials
WP_URL = "https://aitoolsforpros.com/wp-json"
WP_USER = "rmigliorisi"
WP_PASS = "W75u mqKN Rf9S lE4u PJn7 vQyd"
AUTH = (WP_USER, WP_PASS)

BASE_DIR = Path("/Users/rmigs/Projects/aitoolsforpros website")

# ── Tool definitions ──
TOOLS = [
    {"name": "ChatGPT", "slug": "chatgpt", "verdict": "recommended", "file": "chatgpt.html"},
    {"name": "Claude", "slug": "claude", "verdict": "recommended", "file": "claude.html"},
    {"name": "Perplexity AI", "slug": "perplexity", "verdict": "specialized", "file": "perplexity.html"},
    {"name": "Google Gemini", "slug": "gemini", "verdict": "recommended", "file": "gemini.html"},
    {"name": "Microsoft Copilot", "slug": "copilot", "verdict": "recommended", "file": "copilot.html"},
    {"name": "Midjourney", "slug": "midjourney", "verdict": "specialized", "file": "midjourney.html"},
    {"name": "Cursor", "slug": "cursor", "verdict": "recommended", "file": "cursor.html"},
    {"name": "Notion AI", "slug": "notion-ai", "verdict": "specialized", "file": "notion-ai.html"},
    {"name": "Grammarly", "slug": "grammarly", "verdict": "recommended", "file": "grammarly.html"},
    {"name": "Otter.ai", "slug": "otter", "verdict": "recommended", "file": "otter.html"},
]

PROFESSIONS = [
    {"name": "Legal Counsel", "slug": "legal", "file": "legal.html"},
    {"name": "Physicians", "slug": "physicians", "file": "physicians.html"},
    {"name": "Real Estate", "slug": "real-estate", "file": "real-estate.html"},
    {"name": "Engineers", "slug": "engineers", "file": "engineers.html"},
    {"name": "Finance", "slug": "finance", "file": "finance.html"},
    {"name": "Insurance", "slug": "insurance", "file": "insurance.html"},
    {"name": "Architects", "slug": "architects", "file": "architects.html"},
    {"name": "Creatives", "slug": "creatives", "file": "creatives.html"},
]


def strip_tags(html):
    """Remove HTML tags, decode entities."""
    if not html:
        return ""
    text = re.sub(r'<[^>]+>', '', html)
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&#8594;', '→').replace('&middot;', '·').replace('&nbsp;', ' ')
    text = text.replace('&#39;', "'").replace('&quot;', '"')
    return text.strip()


def extract_between(html, start_marker, end_marker):
    """Extract text between two markers."""
    idx1 = html.find(start_marker)
    if idx1 == -1:
        return ""
    idx1 += len(start_marker)
    idx2 = html.find(end_marker, idx1)
    if idx2 == -1:
        return html[idx1:]
    return html[idx1:idx2]


def extract_section_content(html, heading_text):
    """Extract content after an H2 heading until the next H2 or section end."""
    # Find the heading
    patterns = [
        rf'<h2[^>]*>[^<]*{re.escape(heading_text)}[^<]*</h2>',
        rf'<h2[^>]*>.*?{re.escape(heading_text)}.*?</h2>',
    ]
    for pattern in patterns:
        match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
        if match:
            start = match.end()
            # Find next h2 or section/div end
            next_h2 = re.search(r'<h2[^>]*>', html[start:], re.IGNORECASE)
            next_section = re.search(r'</section>', html[start:], re.IGNORECASE)

            end = len(html)
            if next_h2:
                end = min(end, start + next_h2.start())
            if next_section:
                end = min(end, start + next_section.start())

            return html[start:end].strip()
    return ""


def extract_faq(html):
    """Extract FAQ questions and answers."""
    faqs = []
    # Look for FAQ section
    faq_section = extract_between(html, 'Frequently Asked Questions', '</section>')
    if not faq_section:
        faq_section = extract_between(html, 'FAQ', '</section>')

    if faq_section:
        # Find all h3 questions and their answers
        q_pattern = r'<h3[^>]*>(.*?)</h3>'
        questions = list(re.finditer(q_pattern, faq_section, re.DOTALL))

        for i, q_match in enumerate(questions):
            question = strip_tags(q_match.group(1))
            # Get answer text between this h3 and the next
            start = q_match.end()
            if i + 1 < len(questions):
                end = questions[i + 1].start()
            else:
                end = len(faq_section)
            answer_html = faq_section[start:end]
            # Get just the paragraph content
            answer_paras = re.findall(r'<p[^>]*>(.*?)</p>', answer_html, re.DOTALL)
            answer = ' '.join(strip_tags(p) for p in answer_paras)
            if question and answer:
                faqs.append({"question": question, "answer": answer})

    return faqs[:6]


def extract_consistency_blocks(html):
    """Extract the 5 consistency blocks."""
    blocks = {}

    # Bottom Line
    bl = extract_between(html, '>Bottom Line</p>', '</div>')
    bl_match = re.search(r'<p[^>]*>(.*?)</p>', bl, re.DOTALL)
    blocks['bottom_line'] = strip_tags(bl_match.group(1)) if bl_match else ""

    # Key Takeaways
    kt_section = extract_between(html, '>Key Takeaway', '</div>\n</div>')
    if not kt_section:
        kt_section = extract_between(html, '>Key Takeaways', '</div>\n</div>')
    items = re.findall(r'<li[^>]*>.*?→\s*</span>\s*(.*?)</li>', kt_section, re.DOTALL)
    blocks['key_takeaway'] = '\n'.join(strip_tags(i) for i in items)

    # Best For
    bf_section = extract_between(html, '>Best Use Cases</p>', '</div>\n  </div>')
    if not bf_section:
        bf_section = extract_between(html, '>Best For</p>', '</div>\n  </div>')
    items = re.findall(r'<li[^>]*>(.*?)</li>', bf_section, re.DOTALL)
    blocks['best_for'] = '\n'.join(strip_tags(i) for i in items)

    # Avoid If
    av_section = extract_between(html, '>Avoid Using It For</p>', '</div>\n</div>')
    if not av_section:
        av_section = extract_between(html, '>Avoid If</p>', '</div>\n</div>')
    items = re.findall(r'<li[^>]*>(.*?)</li>', av_section, re.DOTALL)
    blocks['avoid_if'] = '\n'.join(strip_tags(i) for i in items)

    # Mini Workflow
    mw_section = extract_between(html, '>If You Only Do One Thing</p>', '</div>')
    lead_match = re.search(r'<p[^>]*>(.*?)</p>', mw_section, re.DOTALL)
    lead = strip_tags(lead_match.group(1)) if lead_match else ""
    steps = re.findall(r'<li[^>]*>(.*?)</li>', mw_section, re.DOTALL)
    blocks['mini_workflow'] = lead + '\n' + '\n'.join(strip_tags(s) for s in steps)

    return blocks


def extract_quick_facts_tool(html):
    """Extract quick facts for tool hub pages."""
    facts = {}
    fact_section = extract_between(html, 'class="fact-bar"', '</div>\n</div>')
    if not fact_section:
        fact_section = extract_between(html, 'fact-bar', '</div>\n  </div>')

    items = re.findall(r'<div class="fact-item">(.*?)</div>\s*</div>', fact_section, re.DOTALL)
    if not items:
        items = re.findall(r'class="fact-item"[^>]*>(.*?)</div>', fact_section, re.DOTALL)

    # Parse fact labels and values from the section
    labels = re.findall(r'fact-label[^>]*>(.*?)</p>', fact_section, re.DOTALL)
    values = re.findall(r'fact-value[^>]*>(.*?)</p>', fact_section, re.DOTALL)

    label_map = {}
    for i, label in enumerate(labels):
        label_text = strip_tags(label).upper()
        value_text = strip_tags(values[i]) if i < len(values) else ""
        label_map[label_text] = value_text

    facts['made_by'] = label_map.get('MADE BY', '')
    facts['best_for_fact'] = label_map.get('BEST FOR', '')
    facts['pricing_fact'] = label_map.get('PRICING', '')
    facts['hipaa_fact'] = label_map.get('HIPAA', label_map.get('HIPAA READY', ''))

    # Custom fact (4th column, varies by tool)
    known_labels = {'MADE BY', 'BEST FOR', 'PRICING', 'HIPAA', 'HIPAA READY'}
    for label_text, value_text in label_map.items():
        if label_text not in known_labels:
            facts['custom_fact_label'] = label_text.title()
            facts['custom_fact_value'] = value_text
            break

    return facts


def extract_sources(html):
    """Extract sources checked."""
    sources = []
    src_section = extract_between(html, 'Sources Checked', '</section>')
    if src_section:
        # Find source links or text
        links = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', src_section, re.DOTALL)
        for url, name in links:
            name = strip_tags(name)
            if name and 'editorial' not in name.lower():
                sources.append({"source_name": name, "source_url": url})

        # Also check for non-linked sources
        if not sources:
            items = re.findall(r'<(?:span|p|div)[^>]*>(\d+\.\s*.*?)</(?:span|p|div)>', src_section, re.DOTALL)
            for item in items:
                sources.append({"source_name": strip_tags(item), "source_url": ""})

    return sources[:5]


def extract_reviews_miss(html):
    """Extract What Most Reviews Miss insights."""
    insights = []
    section = extract_between(html, 'What Most Reviews Miss', '</section>')
    if section:
        titles = re.findall(r'<(?:h3|p)[^>]*font-weight:600[^>]*>(.*?)</(?:h3|p)>', section, re.DOTALL)
        bodies = re.findall(r'line-height:1\.7[^>]*>(.*?)</p>', section, re.DOTALL)

        for i in range(min(len(titles), len(bodies))):
            title = strip_tags(titles[i])
            body = strip_tags(bodies[i])
            if title and body and title != body:
                insights.append({"insight_title": title, "insight_body": body})

    return insights[:3]


def extract_subtitle(html):
    """Extract the subtitle paragraph after H1."""
    match = re.search(r'</h1>\s*<p[^>]*font-size:17px[^>]*>(.*?)</p>', html, re.DOTALL)
    if match:
        return strip_tags(match.group(1))
    return ""


def create_wp_post(post_type, title, slug, acf_fields, status='publish'):
    """Create a WordPress post via REST API."""
    endpoint = f"{WP_URL}/wp/v2/{post_type}"

    data = {
        "title": title,
        "slug": slug,
        "status": status,
        "acf": acf_fields,
    }

    resp = requests.post(endpoint, json=data, auth=AUTH)
    if resp.status_code in (200, 201):
        post = resp.json()
        print(f"  ✓ Created {post_type}: {title} (ID: {post['id']})")
        return post['id']
    else:
        print(f"  ✗ Failed to create {title}: {resp.status_code}")
        try:
            err = resp.json()
            print(f"    Error: {err.get('message', err)}")
        except:
            print(f"    Response: {resp.text[:200]}")
        return None


def migrate_tool_review(tool_def):
    """Migrate a single tool hub page."""
    filepath = BASE_DIR / tool_def['file']
    if not filepath.exists():
        print(f"  ✗ File not found: {filepath}")
        return None

    html = filepath.read_text(encoding='utf-8')

    # Extract content
    subtitle = extract_subtitle(html)
    blocks = extract_consistency_blocks(html)
    facts = extract_quick_facts_tool(html)
    faq = extract_faq(html)
    sources = extract_sources(html)
    reviews_miss = extract_reviews_miss(html)

    # Extract main content sections
    what_it_is = extract_section_content(html, "What It Is")
    who_right_for = extract_section_content(html, "Who It")
    verdict = extract_section_content(html, "Our Verdict")

    # Clean HTML for wysiwyg fields
    for tag in ['div', 'section']:
        what_it_is = re.sub(rf'</?{tag}[^>]*>', '', what_it_is)
        who_right_for = re.sub(rf'</?{tag}[^>]*>', '', who_right_for)
        verdict = re.sub(rf'</?{tag}[^>]*>', '', verdict)

    # Extract features
    features = []
    features_section = extract_section_content(html, "Features That Matter")
    if features_section:
        h3s = list(re.finditer(r'<h3[^>]*>(.*?)</h3>', features_section, re.DOTALL))
        for i, h3 in enumerate(h3s):
            name = strip_tags(h3.group(1))
            start = h3.end()
            end = h3s[i+1].start() if i+1 < len(h3s) else len(features_section)
            desc = features_section[start:end].strip()
            # Clean up
            desc = re.sub(r'</?div[^>]*>', '', desc)
            features.append({
                "feature_name": name,
                "feature_icon": "",
                "feature_description": desc
            })

    # Extract pricing tiers
    pricing = []
    pricing_section = extract_section_content(html, "Pricing")
    if pricing_section:
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', pricing_section, re.DOTALL)
        for row in rows:
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
            if len(cells) >= 2:
                pricing.append({
                    "tier_name": strip_tags(cells[0]),
                    "tier_price": strip_tags(cells[1]),
                    "tier_features": strip_tags(cells[2]) if len(cells) > 2 else ""
                })

    # Build ACF fields
    acf = {
        "tool_name": tool_def['name'],
        "tool_slug": tool_def['slug'],
        "verdict_type": tool_def['verdict'],
        "subtitle": subtitle,
        "publish_date": "2026-02-24",
        "consistency_blocks": blocks,
        "quick_facts": facts,
        "what_it_is": what_it_is[:5000] if what_it_is else "",
        "who_its_right_for": who_right_for[:5000] if who_right_for else "",
        "verdict_text": verdict[:5000] if verdict else "",
    }

    # Note: Repeater fields (features, pricing, faq, sources, reviews_miss)
    # require ACF Pro. We'll store the data but it may not save without Pro.
    if features:
        acf["features"] = features[:7]
    if pricing:
        acf["pricing_tiers"] = pricing
    if faq:
        acf["faq"] = faq
    if sources:
        acf["sources"] = sources
    if reviews_miss:
        acf["reviews_miss"] = reviews_miss

    return create_wp_post("tool_review", tool_def['name'], tool_def['slug'], acf)


def migrate_profession_hub(prof_def):
    """Migrate a profession hub page."""
    filepath = BASE_DIR / prof_def['file']
    if not filepath.exists():
        print(f"  ✗ File not found: {filepath}")
        return None

    html = filepath.read_text(encoding='utf-8')

    # Extract lede
    lede_match = re.search(r'<p[^>]*font-size:17px[^>]*>(.*?)</p>', html, re.DOTALL)
    lede = strip_tags(lede_match.group(1)) if lede_match else ""

    # Extract FAQ
    faq = extract_faq(html)

    acf = {
        "profession_name": prof_def['name'],
        "profession_slug": prof_def['slug'],
        "eyebrow_text": f"AI Tools for {prof_def['name']}",
        "lede": lede,
    }

    if faq:
        acf["faq"] = faq

    return create_wp_post("profession_hub", prof_def['name'], prof_def['slug'], acf)


def migrate_cross_reference(tool_slug, prof_slug, tool_id, prof_id, tool_name, prof_name, tool_verdict):
    """Migrate a cross-reference page."""
    filepath = BASE_DIR / tool_slug / f"{prof_slug}.html"
    if not filepath.exists():
        return None

    html = filepath.read_text(encoding='utf-8')

    subtitle = extract_subtitle(html)
    blocks = extract_consistency_blocks(html)
    faq = extract_faq(html)
    sources = extract_sources(html)
    reviews_miss = extract_reviews_miss(html)

    # Extract content sections
    content_sections = []
    h2_pattern = r'<h2[^>]*class="font-heading"[^>]*>(.*?)</h2>'
    h2s = list(re.finditer(h2_pattern, html, re.DOTALL))

    skip_headings = {'Frequently Asked Questions', 'FAQ', 'Sources Checked',
                     'What Most Reviews Miss', 'Related Guides', 'How It Compares'}

    for i, h2 in enumerate(h2s):
        title = strip_tags(h2.group(1))
        if title in skip_headings:
            continue
        start = h2.end()
        end = h2s[i+1].start() if i+1 < len(h2s) else len(html)
        body = html[start:end]
        # Trim at next section
        sec_end = body.find('</section>')
        if sec_end != -1:
            body = body[:sec_end]
        body = re.sub(r'</?(?:div|section)[^>]*>', '', body).strip()
        if title and body:
            content_sections.append({"section_title": title, "section_body": body[:3000]})

    # Extract verdict
    verdict = extract_section_content(html, "My Verdict")
    if not verdict:
        verdict = extract_section_content(html, "Our Verdict")
    verdict = re.sub(r'</?div[^>]*>', '', verdict) if verdict else ""

    acf = {
        "linked_tool": tool_id,
        "linked_profession": prof_id,
        "verdict_type": tool_verdict,
        "subtitle": subtitle,
        "consistency_blocks": blocks,
        "verdict_text": verdict[:5000],
    }

    if content_sections:
        acf["content_sections"] = content_sections[:8]
    if faq:
        acf["faq"] = faq
    if sources:
        acf["sources"] = sources
    if reviews_miss:
        acf["reviews_miss"] = reviews_miss

    title = f"{tool_name} for {prof_name}"
    slug = f"{tool_slug}-{prof_slug}"

    return create_wp_post("cross_reference", title, slug, acf)


def main():
    print("=" * 60)
    print("AI Tools for Pros — WordPress Content Migration")
    print("=" * 60)

    # Step 1: Migrate Tool Reviews
    print("\n── Step 1: Tool Reviews (10 pages) ──")
    tool_ids = {}
    for tool in TOOLS:
        print(f"\nMigrating: {tool['name']}...")
        post_id = migrate_tool_review(tool)
        if post_id:
            tool_ids[tool['slug']] = {
                'id': post_id,
                'name': tool['name'],
                'verdict': tool['verdict']
            }

    print(f"\n  Tool reviews created: {len(tool_ids)}/10")

    # Step 2: Migrate Profession Hubs
    print("\n── Step 2: Profession Hubs (8 pages) ──")
    prof_ids = {}
    for prof in PROFESSIONS:
        print(f"\nMigrating: {prof['name']}...")
        post_id = migrate_profession_hub(prof)
        if post_id:
            prof_ids[prof['slug']] = {
                'id': post_id,
                'name': prof['name']
            }

    print(f"\n  Profession hubs created: {len(prof_ids)}/8")

    # Step 3: Migrate Cross-Reference Pages
    print("\n── Step 3: Cross-Reference Pages ──")
    xref_count = 0
    for tool_slug, tool_info in tool_ids.items():
        for prof_slug, prof_info in prof_ids.items():
            filepath = BASE_DIR / tool_slug / f"{prof_slug}.html"
            if filepath.exists():
                print(f"\nMigrating: {tool_info['name']} for {prof_info['name']}...")
                post_id = migrate_cross_reference(
                    tool_slug, prof_slug,
                    tool_info['id'], prof_info['id'],
                    tool_info['name'], prof_info['name'],
                    tool_info['verdict']
                )
                if post_id:
                    xref_count += 1

    print(f"\n  Cross-reference pages created: {xref_count}")

    # Summary
    print("\n" + "=" * 60)
    print("Migration Complete!")
    print(f"  Tool Reviews:      {len(tool_ids)}")
    print(f"  Profession Hubs:   {len(prof_ids)}")
    print(f"  Cross-References:  {xref_count}")
    print(f"  Total:             {len(tool_ids) + len(prof_ids) + xref_count}")
    print("=" * 60)


if __name__ == "__main__":
    main()
