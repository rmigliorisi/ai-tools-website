#!/usr/bin/env python3
"""
Retry failed cross-reference migrations.
Root cause: WordPress.com WAF blocks ../ in POST bodies (path traversal detection).
Fix: Extract sources from <li> badges (not <a> links), sanitize all ../ patterns.
"""

import json
import re
import time
import requests
from pathlib import Path

from wp_creds import AUTH, WP_URL

BASE_DIR = Path("/Users/rmigs/Projects/aitoolsforpros website")

TOOL_IDS = {
    "chatgpt": {"id": 34, "name": "ChatGPT", "verdict": "recommended"},
    "claude": {"id": 35, "name": "Claude", "verdict": "recommended"},
    "perplexity": {"id": 36, "name": "Perplexity AI", "verdict": "specialized"},
    "gemini": {"id": 37, "name": "Google Gemini", "verdict": "recommended"},
    "copilot": {"id": 38, "name": "Microsoft Copilot", "verdict": "recommended"},
    "midjourney": {"id": 39, "name": "Midjourney", "verdict": "specialized"},
    "cursor": {"id": 40, "name": "Cursor", "verdict": "recommended"},
    "notion-ai": {"id": 41, "name": "Notion AI", "verdict": "specialized"},
    "grammarly": {"id": 42, "name": "Grammarly", "verdict": "recommended"},
    "otter": {"id": 43, "name": "Otter.ai", "verdict": "recommended"},
}

PROF_IDS = {
    "legal": {"id": 44, "name": "Legal Counsel"},
    "physicians": {"id": 45, "name": "Physicians"},
    "real-estate": {"id": 46, "name": "Real Estate"},
    "engineers": {"id": 47, "name": "Engineers"},
    "finance": {"id": 48, "name": "Finance"},
    "insurance": {"id": 49, "name": "Insurance"},
    "architects": {"id": 50, "name": "Architects"},
    "creatives": {"id": 51, "name": "Creatives"},
}

EXISTING_SLUGS = {
    'otter-physicians', 'grammarly-real-estate', 'notion-ai-legal',
    'cursor-engineers', 'copilot-engineers', 'copilot-real-estate',
    'copilot-physicians', 'copilot-legal', 'gemini-real-estate',
    'gemini-legal', 'perplexity-legal', 'claude-engineers',
    'claude-real-estate', 'claude-physicians', 'chatgpt-engineers',
    'chatgpt-physicians'
}


def strip_tags(html):
    """Remove ALL HTML tags and decode entities."""
    if not html:
        return ""
    text = re.sub(r'<[^>]+>', '', str(html))
    for old, new in [('&amp;','&'),('&lt;','<'),('&gt;','>'),('&#8594;','->'),
                      ('&middot;','.'),('&nbsp;',' '),('&#39;',"'"),('&quot;','"'),
                      ('&mdash;',' - '),('&ndash;',' - '),('&rsquo;',"'"),
                      ('&lsquo;',"'"),('&rdquo;','"'),('&ldquo;','"'),
                      ('&hellip;','...')]:
        text = text.replace(old, new)
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
    text = re.sub(r'  +', ' ', text)
    return text.strip()


def sanitize_payload(obj):
    """Recursively strip HTML and remove ../ from all string values."""
    if isinstance(obj, str):
        val = strip_tags(obj)
        # Remove ../ patterns that trigger WAF
        val = val.replace('../', '').replace('..\\', '')
        return val
    elif isinstance(obj, dict):
        return {k: sanitize_payload(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_payload(item) for item in obj]
    return obj


def extract_between(html, start_marker, end_marker):
    idx1 = html.find(start_marker)
    if idx1 == -1:
        return ""
    idx1 += len(start_marker)
    idx2 = html.find(end_marker, idx1)
    return html[idx1:idx2] if idx2 != -1 else html[idx1:]


def extract_subtitle(html):
    match = re.search(r'</h1>\s*<p[^>]*>(.*?)</p>', html, re.DOTALL)
    return strip_tags(match.group(1)) if match else ""


def extract_consistency_blocks(html):
    blocks = {}

    bl = extract_between(html, '>Bottom Line</p>', '</div>')
    bl_match = re.search(r'<p[^>]*>(.*?)</p>', bl, re.DOTALL)
    blocks['bottom_line'] = strip_tags(bl_match.group(1)) if bl_match else ""

    kt_section = extract_between(html, '>Key Takeaway', '</div>\n</div>')
    if not kt_section:
        kt_section = extract_between(html, '>Key Takeaways', '</div>\n</div>')
    items = re.findall(r'<li[^>]*>.*?→\s*</span>\s*(.*?)</li>', kt_section, re.DOTALL)
    if not items:
        items = re.findall(r'<li[^>]*>(.*?)</li>', kt_section, re.DOTALL)
    blocks['key_takeaway'] = '\n'.join(strip_tags(i) for i in items)

    bf_section = extract_between(html, '>Best Use Cases</p>', '</div>\n  </div>')
    if not bf_section:
        bf_section = extract_between(html, '>Best For</p>', '</div>\n  </div>')
    items = re.findall(r'<li[^>]*>(.*?)</li>', bf_section, re.DOTALL)
    blocks['best_for'] = '\n'.join(strip_tags(i) for i in items)

    av_section = extract_between(html, '>Avoid Using It For</p>', '</div>\n</div>')
    if not av_section:
        av_section = extract_between(html, '>Avoid If</p>', '</div>\n</div>')
    items = re.findall(r'<li[^>]*>(.*?)</li>', av_section, re.DOTALL)
    blocks['avoid_if'] = '\n'.join(strip_tags(i) for i in items)

    mw_section = extract_between(html, '>If You Only Do One Thing</p>', '</div>')
    lead_match = re.search(r'<p[^>]*>(.*?)</p>', mw_section, re.DOTALL)
    lead = strip_tags(lead_match.group(1)) if lead_match else ""
    steps = re.findall(r'<li[^>]*>(.*?)</li>', mw_section, re.DOTALL)
    blocks['mini_workflow'] = lead + '\n' + '\n'.join(strip_tags(s) for s in steps)

    return blocks


def extract_faq(html):
    faqs = []
    faq_start = html.find('Frequently Asked Questions')
    if faq_start == -1:
        return faqs

    faq_section = html[faq_start:]
    faq_end = faq_section.find('</section>')
    if faq_end > 0:
        faq_section = faq_section[:faq_end]

    q_matches = list(re.finditer(r'<h3[^>]*>(.*?)</h3>', faq_section, re.DOTALL))
    for i, qm in enumerate(q_matches):
        question = strip_tags(qm.group(1))
        start = qm.end()
        end = q_matches[i+1].start() if i+1 < len(q_matches) else len(faq_section)
        answer_html = faq_section[start:end]
        answer_paras = re.findall(r'<p[^>]*>(.*?)</p>', answer_html, re.DOTALL)
        answer = ' '.join(strip_tags(p) for p in answer_paras)
        if question and answer:
            faqs.append({"question": question, "answer": answer})

    return faqs[:6]


def extract_sources(html):
    """Extract sources from numbered badge list items (NOT from <a> links)."""
    sources = []
    src_start = html.find('Sources Checked')
    if src_start == -1:
        return sources

    src_section = html[src_start:]
    # End at next h2 or section end
    next_h2 = re.search(r'<h2[^>]*>', src_section[20:])
    if next_h2:
        src_section = src_section[:20 + next_h2.start()]

    # Find <li> items with source-badge spans
    li_items = re.findall(r'<li[^>]*>\s*<span class="source-badge">\d+</span>\s*<span>(.*?)</span>\s*</li>', src_section, re.DOTALL)
    for item in li_items:
        name = strip_tags(item)
        if name:
            sources.append({"source_name": name, "source_url": ""})

    # Fallback: any <li> in the sources section
    if not sources:
        li_items = re.findall(r'<li[^>]*>(.*?)</li>', src_section, re.DOTALL)
        for item in li_items:
            name = strip_tags(item)
            # Skip items that look like they're from Related Guides
            if name and 'Read guide' not in name and len(name) > 10:
                sources.append({"source_name": name, "source_url": ""})

    return sources[:5]


def extract_reviews_miss(html):
    insights = []
    rm_start = html.find('What Most Reviews Miss')
    if rm_start == -1:
        return insights

    section = html[rm_start:]
    sec_end = section.find('</section>')
    if sec_end > 0:
        section = section[:sec_end]

    titles = re.findall(r'font-weight:\s*600[^>]*>(.*?)</(?:h3|p)>', section, re.DOTALL)
    bodies = re.findall(r'line-height:1\.7[^>]*>(.*?)</p>', section, re.DOTALL)

    for i in range(min(len(titles), len(bodies))):
        title = strip_tags(titles[i])
        body = strip_tags(bodies[i])
        if title and body and title != body:
            insights.append({"insight_title": title, "insight_body": body})

    return insights[:3]


def create_wp_post(post_type, title, slug, acf_fields, status='publish'):
    """Create a WordPress post with sanitized payload."""
    endpoint = f"{WP_URL}/wp/v2/{post_type}"

    # Sanitize everything (strip HTML + remove ../)
    safe_acf = sanitize_payload(acf_fields)

    # Preserve integer fields
    for key in ('linked_tool', 'linked_profession'):
        if key in acf_fields:
            safe_acf[key] = acf_fields[key]

    data = {
        "title": title,
        "slug": slug,
        "status": status,
        "acf": safe_acf,
    }

    # Final safety check: ensure no ../ in serialized JSON
    payload_str = json.dumps(data)
    if '../' in payload_str:
        payload_str = payload_str.replace('../', '')
        data = json.loads(payload_str)

    resp = requests.post(endpoint, json=data, auth=AUTH)
    if resp.status_code in (200, 201):
        post = resp.json()
        print(f"  OK {title} (ID: {post['id']})")
        return post['id']
    else:
        print(f"  FAIL {title}: HTTP {resp.status_code}")
        try:
            err = resp.json()
            print(f"    {err.get('message', str(err)[:200])}")
        except:
            print(f"    {resp.text[:200]}")
        return None


def migrate_cross_reference(tool_slug, prof_slug):
    tool_info = TOOL_IDS[tool_slug]
    prof_info = PROF_IDS[prof_slug]

    filepath = BASE_DIR / tool_slug / f"{prof_slug}.html"
    if not filepath.exists():
        return None

    html = filepath.read_text(encoding='utf-8')

    subtitle = extract_subtitle(html)
    blocks = extract_consistency_blocks(html)
    faq = extract_faq(html)
    sources = extract_sources(html)
    reviews_miss = extract_reviews_miss(html)

    # Extract content sections using plain <h2> tags
    content_sections = []
    h2s = list(re.finditer(r'<h2[^>]*>(.*?)</h2>', html, re.DOTALL))

    skip_headings = {'Frequently Asked Questions', 'FAQ', 'Sources Checked',
                     'What Most Reviews Miss', 'Related Guides', 'My Verdict',
                     'Our Verdict'}

    for i, h2 in enumerate(h2s):
        title_text = strip_tags(h2.group(1))
        if title_text in skip_headings or 'Prompts That Work' in title_text:
            continue
        # Also skip if title contains "How" and "Compare" (handled separately)
        if 'How' in title_text and 'Compare' in title_text:
            continue
        start = h2.end()
        end = h2s[i+1].start() if i+1 < len(h2s) else len(html)
        body = strip_tags(html[start:end])[:3000]
        if title_text and body:
            content_sections.append({"section_title": title_text, "section_body": body})

    # Verdict
    verdict = ""
    for h2 in h2s:
        t = strip_tags(h2.group(1))
        if t in ('My Verdict', 'Our Verdict'):
            start = h2.end()
            next_h2 = re.search(r'<h2[^>]*>', html[start:])
            next_sec = re.search(r'</section>', html[start:])
            end = len(html)
            if next_h2: end = min(end, start + next_h2.start())
            if next_sec: end = min(end, start + next_sec.start())
            verdict = strip_tags(html[start:end])[:5000]
            break

    # Comparison
    comparison = ""
    for h2 in h2s:
        t = strip_tags(h2.group(1))
        if 'How' in t and 'Compare' in t:
            start = h2.end()
            next_h2 = re.search(r'<h2[^>]*>', html[start:])
            next_sec = re.search(r'</section>', html[start:])
            end = len(html)
            if next_h2: end = min(end, start + next_h2.start())
            if next_sec: end = min(end, start + next_sec.start())
            comparison = strip_tags(html[start:end])[:5000]
            break

    # Prompts
    prompts = []
    prompts_section = extract_between(html, 'Prompts That Work', '</section>')
    if prompts_section:
        p_titles = re.findall(r'font-weight:\s*600[^>]*>(.*?)</p>', prompts_section, re.DOTALL)
        p_blocks = re.findall(r'class="prompt-block"[^>]*>(.*?)</div>', prompts_section, re.DOTALL)
        for j in range(min(len(p_titles), len(p_blocks))):
            prompts.append({
                "prompt_title": strip_tags(p_titles[j]),
                "prompt_text": strip_tags(p_blocks[j])
            })

    # Quick facts
    quick_facts = {}
    fact_section = extract_between(html, 'fact-bar', '</section>')
    labels = re.findall(r'fact-label[^>]*>(.*?)</p>', fact_section, re.DOTALL)
    values = re.findall(r'fact-value[^>]*>(.*?)</p>', fact_section, re.DOTALL)
    for j, label in enumerate(labels):
        lt = strip_tags(label).upper()
        vt = strip_tags(values[j]) if j < len(values) else ""
        if 'BEST FOR' in lt:
            quick_facts['best_for'] = vt
        elif 'PRICING' in lt or 'PRICE' in lt:
            quick_facts['pricing'] = vt
        elif 'COMPLIANCE' in lt or 'HIPAA' in lt:
            quick_facts['compliance'] = vt
        elif 'COMPARE' in lt or 'ALTERNATIVE' in lt or 'INSTEAD' in lt:
            quick_facts['compared_to'] = vt

    # Build ACF payload
    acf = {
        "linked_tool": tool_info['id'],
        "linked_profession": prof_info['id'],
        "verdict_type": tool_info['verdict'],
        "subtitle": subtitle,
        "consistency_blocks": blocks,
        "verdict_text": verdict,
    }

    if quick_facts:
        acf["quick_facts"] = quick_facts
    if content_sections:
        acf["content_sections"] = content_sections[:8]
    if prompts:
        acf["prompts"] = prompts[:6]
    if comparison:
        acf["comparison_notes"] = comparison
    if faq:
        acf["faq"] = faq
    if sources:
        acf["sources"] = sources
    if reviews_miss:
        acf["reviews_miss"] = reviews_miss

    title = f"{tool_info['name']} for {prof_info['name']}"
    slug = f"{tool_slug}-{prof_slug}"

    return create_wp_post("cross_reference", title, slug, acf)


def main():
    print("=" * 60)
    print("Retry: 25 Failed Cross-Reference Pages")
    print("=" * 60)

    success = 0
    failed = 0
    failed_list = []

    for tool_slug in TOOL_IDS:
        for prof_slug in PROF_IDS:
            slug = f"{tool_slug}-{prof_slug}"
            if slug in EXISTING_SLUGS:
                continue

            filepath = BASE_DIR / tool_slug / f"{prof_slug}.html"
            if not filepath.exists():
                continue

            print(f"\n  {TOOL_IDS[tool_slug]['name']} for {PROF_IDS[prof_slug]['name']}...")
            post_id = migrate_cross_reference(tool_slug, prof_slug)

            if post_id:
                success += 1
            else:
                failed += 1
                failed_list.append(slug)

            time.sleep(1)

    print("\n" + "=" * 60)
    print(f"Results: {success} created, {failed} failed")
    if failed_list:
        print(f"Still failing: {', '.join(failed_list)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
