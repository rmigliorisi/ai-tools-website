#!/usr/bin/env python3
"""
Migration v2: Store all data as JSON in post_content + linked IDs as post meta.
Deletes existing posts and re-creates them with the correct data format.

This version preserves HTML formatting in content fields instead of stripping tags.

This works with ACF Free (no Pro needed) because:
- Templates read from post_content JSON via aifp_get_data() helper
- Cross-reference linking uses registered post meta (linked_tool, linked_profession)
- No ACF field groups needed for data storage
"""

import json
import re
import time
import requests
from pathlib import Path

from wp_creds import AUTH, WP_URL

BASE_DIR = Path("/Users/rmigs/Projects/aitoolsforpros website")

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

# Tags we want to keep in cleaned HTML
ALLOWED_TAGS = {
    'p', 'ul', 'ol', 'li', 'h3', 'h4', 'a', 'strong', 'em', 'span', 'div',
    'table', 'thead', 'tbody', 'tr', 'td', 'th', 'br', 'blockquote', 'code',
    'pre', 'sup', 'sub', 'b', 'i', 'hr',
}


def strip_tags(html):
    """Strip ALL HTML tags (used only for plain-text fields like titles)."""
    if not html:
        return ""
    text = re.sub(r'<[^>]+>', '', str(html))
    for old, new in [('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'), ('&#8594;', '->'),
                      ('&middot;', '.'), ('&nbsp;', ' '), ('&#39;', "'"), ('&quot;', '"'),
                      ('&mdash;', ' - '), ('&ndash;', ' - '), ('&rsquo;', "'"),
                      ('&lsquo;', "'"), ('&rdquo;', '"'), ('&ldquo;', '"'),
                      ('&hellip;', '...')]:
        text = text.replace(old, new)
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
    text = re.sub(r'  +', ' ', text)
    return text.strip()


def sanitize(text):
    """Strip tags and remove ../ patterns (WAF trigger). For plain-text fields only."""
    t = strip_tags(text)
    t = t.replace('../', '').replace('..\\', '')
    return t


def clean_html(html):
    """Clean HTML while preserving structure, formatting, and inline styles.

    - Keeps allowed tags (p, ul, ol, li, h3, a, strong, em, etc.)
    - KEEPS inline style attributes (needed for layout: grids, colors, etc.)
    - Removes only event handlers (onmouseover, onmouseout)
    - Converts relative links to absolute WordPress links
    - Removes ../ patterns that trigger WAF
    """
    if not html:
        return ""

    h = str(html)

    # Remove event handlers (hover effects not needed in WordPress)
    h = re.sub(r'\s+onmouseover="[^"]*"', '', h)
    h = re.sub(r'\s+onmouseout="[^"]*"', '', h)
    h = re.sub(r'\s+onclick="[^"]*"', '', h)

    # Convert relative links to absolute WordPress paths
    # Cross-reference links: href="chatgpt/legal.html" -> href="/chatgpt/legal/"
    h = re.sub(r'href="(\w[\w-]*)/([\w-]+)\.html"', r'href="/\1/\2/"', h)
    # Same with ../ prefix: href="../chatgpt/legal.html" -> href="/chatgpt/legal/"
    h = re.sub(r'href="\.\./(\w[\w-]*)/([\w-]+)\.html"', r'href="/\1/\2/"', h)
    # Root-level tool/page links: href="claude.html" -> href="/claude/"
    h = re.sub(r'href="([\w-]+)\.html"', r'href="/\1/"', h)
    # With ../ prefix: href="../claude.html" -> href="/claude/"
    h = re.sub(r'href="\.\./([\w-]+)\.html"', r'href="/\1/"', h)

    # Remove any remaining ../ patterns (WAF trigger)
    h = h.replace('../', '').replace('..\\', '')

    # Strip section-label divs (static HTML presentational labels — replaced by template headings in WP)
    h = re.sub(r'<div[^>]*class="section-label"[^>]*>.*?</div>', '', h, flags=re.DOTALL)

    # Remove SVG elements entirely (inline icons etc.)
    h = re.sub(r'<svg[^>]*>.*?</svg>', '', h, flags=re.DOTALL)

    # Remove img tags (logos, author avatars, etc.)
    h = re.sub(r'<img[^>]*/?>', '', h)

    # Remove empty anchor tags that only contained SVGs
    h = re.sub(r'<a[^>]*>\s*</a>', '', h)

    # Remove tags that are not in ALLOWED_TAGS but keep their content
    def replace_disallowed(match):
        tag = match.group(0)
        # Extract tag name
        m = re.match(r'</?(\w+)', tag)
        if m:
            tag_name = m.group(1).lower()
            if tag_name not in ALLOWED_TAGS:
                return ''
        return tag

    h = re.sub(r'</?[a-zA-Z][^>]*/?>', replace_disallowed, h)

    # Clean up excessive whitespace but preserve structure
    h = re.sub(r'\n\s*\n\s*\n', '\n\n', h)
    h = re.sub(r'  +', ' ', h)

    return h.strip()


def extract_between(html, start_marker, end_marker):
    """Extract raw HTML between two markers."""
    idx1 = html.find(start_marker)
    if idx1 == -1:
        return ""
    idx1 += len(start_marker)
    idx2 = html.find(end_marker, idx1)
    return html[idx1:idx2] if idx2 != -1 else html[idx1:]


def extract_subtitle(html):
    """Extract the first paragraph after H1 - the definition sentence.
    Original pages use font-size:16px (hub pages) or class="page-subtitle" (cross-ref pages).
    """
    # Try font-size:16px first (hub pages)
    match = re.search(r'</h1>\s*(?:<!--[^>]*-->\s*)?<p[^>]*font-size:16px[^>]*>(.*?)</p>', html, re.DOTALL)
    if not match:
        # Try font-size:17px as fallback
        match = re.search(r'</h1>\s*(?:<!--[^>]*-->\s*)?<p[^>]*font-size:17px[^>]*>(.*?)</p>', html, re.DOTALL)
    if not match:
        # Try class="page-subtitle" (cross-ref pages)
        match = re.search(r'</h1>\s*<p[^>]*class="page-subtitle"[^>]*>(.*?)</p>', html, re.DOTALL)
    if not match:
        # Fallback: first <p> after </h1>
        match = re.search(r'</h1>\s*<p[^>]*>(.*?)</p>', html, re.DOTALL)
    return sanitize(match.group(1)) if match else ""


def extract_definition_sentence(html):
    """Extract the definition sentence paragraph right after H1 (font-size:16px)."""
    match = re.search(r'</h1>\s*(?:<!--[^>]*-->\s*)?<p[^>]*font-size:16px[^>]*>(.*?)</p>', html, re.DOTALL)
    if not match:
        match = re.search(r'</h1>\s*(?:<!--[^>]*-->\s*)?<p[^>]*font-size:17px[^>]*>(.*?)</p>', html, re.DOTALL)
    return clean_html(match.group(1)) if match else ""


def extract_positioning_statement(html):
    """Extract the italic positioning statement after the definition sentence."""
    # Must start with <p to avoid matching CSS selectors that contain >
    match = re.search(r'<p[^>]*font-style:\s*italic[^>]*>(.*?)</p>', html, re.DOTALL)
    return clean_html(match.group(1)) if match else ""


def extract_publish_date(html):
    """Extract publish date from 'Independent Review . DATE' line or byline."""
    # Try "Independent Review · DATE" pattern
    match = re.search(r'Independent Review\s*(?:&middot;|·)\s*([A-Z][a-z]+ \d{1,2},? \d{4})', html)
    if match:
        return match.group(1)
    # Try byline date at end of byline paragraph
    match = re.search(r'(?:&middot;|·)\s*([A-Z][a-z]+ \d{1,2},? \d{4})\s*</p>', html)
    if match:
        return match.group(1)
    # Try datePublished in JSON-LD
    match = re.search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})"', html)
    if match:
        return match.group(1)
    return ""


def extract_verdict_description(html):
    """Extract the text next to the verdict badge (e.g. 'Strong default choice...')."""
    # Look for text span after verdict badge
    match = re.search(
        r'verdict-badge-(?:recommended|specialized)">[^<]*</span>\s*'
        r'<span[^>]*>(.*?)</span>',
        html, re.DOTALL
    )
    if match:
        return sanitize(match.group(1))
    # Alternative: it might be a sibling element without span wrapper
    match = re.search(
        r'verdict-badge-(?:recommended|specialized)">[^<]*</span>\s*'
        r'(?:<[^>]*>)?\s*([^<]+)',
        html, re.DOTALL
    )
    if match:
        return match.group(1).strip()
    return ""


def extract_consistency_blocks(html):
    """Extract the 5 consistency blocks from hub pages (inline styles),
    cross-reference pages (CSS classes like verdict-banner, cb-label, cb-text),
    and class-based hub pages (consistency-block / consistency-label / consistency-value)."""
    blocks = {}

    # ── Class-based hub format (cursor, notion-ai, grammarly, otter) ──
    # <div class="consistency-block">
    #   <div class="consistency-label">Bottom Line</div>
    #   <div class="consistency-value">text</div>
    # </div>
    cb_blocks = re.findall(
        r'<div[^>]*class="consistency-block"[^>]*>\s*'
        r'<div[^>]*class="consistency-label"[^>]*>(.*?)</div>\s*'
        r'<div[^>]*class="consistency-value"[^>]*>(.*?)</div>',
        html, re.DOTALL
    )
    if cb_blocks:
        label_map = {sanitize(label).strip().lower(): sanitize(value).strip()
                     for label, value in cb_blocks}
        blocks['bottom_line']  = label_map.get('bottom line', '')
        blocks['key_takeaway'] = label_map.get('key takeaway', label_map.get('key takeaways', ''))
        blocks['best_for']     = label_map.get('best for', label_map.get('best use cases', ''))
        blocks['avoid_if']     = label_map.get('avoid if', label_map.get('avoid using it for', ''))
        blocks['mini_workflow'] = label_map.get('mini workflow', label_map.get('if you only do one thing', ''))
        return blocks

    # ── Bottom Line ──
    # Hub format: >Bottom Line</p> ... <p>text</p>
    bl = extract_between(html, '>Bottom Line</p>', '</div>')
    bl_match = re.search(r'<p[^>]*>(.*?)</p>', bl, re.DOTALL)
    if bl_match:
        blocks['bottom_line'] = sanitize(bl_match.group(1))
    else:
        # Cross-ref format: <div class="verdict-banner"><p><strong>Bottom line:</strong> text</p></div>
        vb = re.search(r'class="verdict-banner"[^>]*>\s*<p[^>]*>(?:<strong>[^<]*</strong>\s*)?(.+?)</p>', html, re.DOTALL)
        blocks['bottom_line'] = sanitize(vb.group(1)) if vb else ""

    # ── Key Takeaway ──
    kt_css = re.search(r'>Key Takeaway[s]?</div>\s*<div[^>]*class="cb-text"[^>]*>(.*?)</div>', html, re.DOTALL)
    if kt_css:
        blocks['key_takeaway'] = sanitize(kt_css.group(1))
    else:
        kt_match = re.search(r'>Key Takeaway[s]?</p>\s*(<ul[^>]*>.*?</ul>)', html, re.DOTALL)
        blocks['key_takeaway'] = clean_html(kt_match.group(1)) if kt_match else ''

    # ── Best For ──
    bf_css = re.search(r'>Best For</div>\s*<div[^>]*class="cb-text"[^>]*>(.*?)</div>', html, re.DOTALL)
    if bf_css:
        blocks['best_for'] = sanitize(bf_css.group(1))
    else:
        bf_match = re.search(r'>Best Use Cases</p>\s*(<ul[^>]*>.*?</ul>)', html, re.DOTALL)
        if not bf_match:
            bf_match = re.search(r'>Best For</p>\s*(<ul[^>]*>.*?</ul>)', html, re.DOTALL)
        blocks['best_for'] = clean_html(bf_match.group(1)) if bf_match else ''

    # ── Avoid If ──
    av_css = re.search(r'>Avoid If</div>\s*<div[^>]*class="cb-text"[^>]*>(.*?)</div>', html, re.DOTALL)
    if av_css:
        blocks['avoid_if'] = sanitize(av_css.group(1))
    else:
        av_match = re.search(r'>Avoid Using It For</p>\s*(<ul[^>]*>.*?</ul>)', html, re.DOTALL)
        if not av_match:
            av_match = re.search(r'>Avoid If</p>\s*(<ul[^>]*>.*?</ul>)', html, re.DOTALL)
        blocks['avoid_if'] = clean_html(av_match.group(1)) if av_match else ''

    # ── Mini Workflow ──
    mw_css = re.search(r'>Mini Workflow</div>\s*<div[^>]*class="cb-text"[^>]*>\s*<div[^>]*class="cb-workflow-highlight"[^>]*>(.*?)</div>', html, re.DOTALL)
    if not mw_css:
        mw_css = re.search(r'>Mini Workflow</div>\s*<div[^>]*class="cb-text"[^>]*>(.*?)</div>', html, re.DOTALL)
    if mw_css:
        blocks['mini_workflow'] = sanitize(mw_css.group(1))
    else:
        mw_match = re.search(r'>If You Only Do One Thing</p>\s*(.*?)</div>', html, re.DOTALL)
        blocks['mini_workflow'] = clean_html(mw_match.group(1)) if mw_match else ''

    return blocks


def extract_faq(html):
    """Extract FAQ items, preserving HTML in answers."""
    faqs = []
    faq_start = html.find('Frequently Asked Questions')
    if faq_start == -1:
        faq_start = html.find('Common Questions')
    if faq_start == -1:
        return faqs
    faq_section = html[faq_start:]
    faq_end = faq_section.find('</section>')
    if faq_end > 0:
        faq_section = faq_section[:faq_end]
    else:
        # Class-based pages use divs, not <section> — cut at next natural boundary
        for stopper in ['Sources Checked', '<!-- Sources', 'class="source-item"', '<!-- What Most']:
            idx = faq_section.find(stopper)
            if idx > 0:
                faq_section = faq_section[:idx]
                break

    q_matches = list(re.finditer(r'<h3[^>]*>(.*?)</h3>', faq_section, re.DOTALL))
    for i, qm in enumerate(q_matches):
        question = sanitize(qm.group(1))
        start = qm.end()
        end = q_matches[i + 1].start() if i + 1 < len(q_matches) else len(faq_section)
        answer_html = faq_section[start:end]
        # Preserve HTML in answers
        answer = clean_html(answer_html)
        if question and answer:
            faqs.append({"question": question, "answer": answer})

    return faqs[:6]


def extract_sources(html):
    """Extract sources from numbered badge list items."""
    sources = []
    src_start = html.find('Sources Checked')
    if src_start == -1:
        return sources
    src_section = html[src_start:]
    # Skip past the section heading h2 before finding the end boundary.
    # Class-based pages have a separate .section-label + h2; standard pages have only the h2.
    first_h2_m = re.search(r'<h2[^>]*>.*?</h2>', src_section, re.DOTALL)
    search_from = first_h2_m.end() if first_h2_m else 20
    next_h2 = re.search(r'<h2[^>]*>', src_section[search_from:])
    if next_h2:
        src_section = src_section[:search_from + next_h2.start()]

    li_items = re.findall(
        r'<li[^>]*>\s*<span class="source-badge">\d+</span>\s*<span>(.*?)</span>\s*</li>',
        src_section, re.DOTALL
    )
    for item in li_items:
        name = sanitize(item)
        if name:
            sources.append({"source_name": name, "source_url": ""})

    if not sources:
        # Fallback: try numbered bracket format [1], [2], etc.
        li_items = re.findall(r'<li[^>]*>(.*?)</li>', src_section, re.DOTALL)
        for item in li_items:
            name = sanitize(item)
            if name and 'Read guide' not in name and len(name) > 10:
                sources.append({"source_name": name, "source_url": ""})

    if not sources:
        # Class-based format: <div class="source-item">...<span class="source-text">...</span>
        si_items = re.findall(
            r'<div[^>]*class="source-item"[^>]*>.*?<span[^>]*class="source-text"[^>]*>(.*?)</span>',
            src_section, re.DOTALL
        )
        for item in si_items:
            name = sanitize(item)
            if name:
                sources.append({"source_name": name, "source_url": ""})

    return sources[:5]


def extract_reviews_miss(html):
    """Extract 'What Most Reviews Miss' section, preserving HTML in insight bodies,
    insight banner, and the 'one thing better/wrong' paragraphs."""
    rm_start = html.find('What Most Reviews Miss')
    if rm_start == -1:
        return {"insights": [], "insight_banner": "", "one_thing_better": "", "one_thing_wrong": ""}

    section = html[rm_start:]
    # Cut at section end, author card, or footer — whichever comes first
    for stopper in ['</section>', 'class="author-card"', '<footer', '<!-- AUTHOR', '<!-- FOOTER']:
        idx = section.find(stopper)
        if idx > 0:
            section = section[:idx]
            break

    # --- Primary: class="insight-card" format (cross-reference pages) ---
    insights = []
    ic_matches = list(re.finditer(r'<div class="insight-card">', section))
    for j, m in enumerate(ic_matches):
        start = m.end()
        end = ic_matches[j + 1].start() if j + 1 < len(ic_matches) else len(section)
        block = section[start:end]
        title_m = re.search(r'<h4[^>]*>(.*?)</h4>', block, re.DOTALL)
        body_m = re.search(r'<p[^>]*>(.*?)</p>', block, re.DOTALL)
        insights.append({
            "insight_title": sanitize(title_m.group(1)) if title_m else "",
            "insight_body": clean_html(body_m.group(1)) if body_m else "",
        })

    # --- Fallback: inline background:#f9fafb style (hub pages) ---
    # Require border-radius so we don't match the outer section wrapper
    if not insights:
        insight_blocks = re.findall(
            r'<div[^>]*background:#f9fafb[^>]*border-radius[^>]*>(.*?)</div>',
            section, re.DOTALL
        )
        for block in insight_blocks:
            body = clean_html(block)
            if body and len(body) > 20:
                insights.append({"insight_title": "", "insight_body": body})

    # --- Fallback: class-based .prose format with numbered bold paragraphs ---
    if not insights:
        prose_m = re.search(r'<div[^>]*class="prose"[^>]*>(.*?)</div>', section, re.DOTALL)
        if prose_m:
            for p_m in re.finditer(r'<p[^>]*><strong>\d+\.\s*(.*?)</strong>(.*?)</p>',
                                   prose_m.group(1), re.DOTALL):
                title = sanitize(p_m.group(1)).rstrip('.')
                body = sanitize(p_m.group(2))
                if title:
                    insights.append({"insight_title": title, "insight_body": body})

    # --- Fallback: font-weight:600 titles + line-height:1.7 bodies ---
    if not insights:
        titles = re.findall(r'font-weight:\s*600[^>]*>(.*?)</(?:h3|p)>', section, re.DOTALL)
        bodies = re.findall(r'line-height:1\.7[^>]*>(.*?)</p>', section, re.DOTALL)
        for i in range(min(len(titles), len(bodies))):
            title = sanitize(titles[i])
            body = clean_html(bodies[i])
            if title and body and title != body:
                insights.append({"insight_title": title, "insight_body": body})

    # --- Insight banner: class="insight-banner" (cross-ref) or inline border-left style (hub) ---
    banner = ""
    banner_match = re.search(
        r'<div class="insight-banner"[^>]*>\s*<p[^>]*>(.*?)</p>',
        section, re.DOTALL
    )
    if banner_match:
        banner = clean_html(banner_match.group(1))
    else:
        banner_match = re.search(
            r'<p[^>]*border-left:\s*3px solid #f59e0b[^>]*>(.*?)</p>',
            section, re.DOTALL
        )
        if banner_match:
            banner = clean_html(banner_match.group(1))
    if not banner:
        # Class-based: insight-banner with inner .insight-text div (not a <p>)
        it_m = re.search(
            r'<div[^>]*class="insight-banner"[^>]*>.*?<div[^>]*class="insight-text"[^>]*>(.*?)</div>',
            section, re.DOTALL
        )
        if it_m:
            banner = sanitize(it_m.group(1))

    # Extract "One thing better" and "One thing wrong" paragraphs
    one_better = ""
    one_wrong = ""
    better_match = re.search(
        r'<strong>One thing[^<]*does better[^<]*</strong>(.*?)</p>',
        section, re.DOTALL
    )
    if better_match:
        one_better = clean_html(better_match.group(0))

    wrong_match = re.search(
        r'<strong>One thing[^<]*gets wrong[^<]*</strong>(.*?)</p>',
        section, re.DOTALL
    )
    if wrong_match:
        one_wrong = clean_html(wrong_match.group(0))

    return {
        "insights": insights[:3],
        "insight_banner": banner,
        "one_thing_better": one_better,
        "one_thing_wrong": one_wrong,
    }


def extract_quick_facts_tool(html):
    """Extract Quick Facts bar for tool hub pages."""
    facts = {}

    # ── Class-based format (cursor, notion-ai, grammarly, otter) ──
    fl_items = re.findall(
        r'<div[^>]*class="fact-item"[^>]*>\s*'
        r'<div[^>]*class="fact-label"[^>]*>(.*?)</div>\s*'
        r'<div[^>]*class="fact-value"[^>]*>(.*?)</div>',
        html, re.DOTALL
    )
    if fl_items:
        label_map = {sanitize(l).upper().strip(): sanitize(v).strip() for l, v in fl_items}
        facts['made_by']        = label_map.get('MADE BY', '')
        facts['best_for_fact']  = label_map.get('BEST FOR', '')
        facts['pricing_fact']   = label_map.get('PRICING', label_map.get('STARTING PRICE', ''))
        facts['hipaa_fact']     = label_map.get('HIPAA', label_map.get('HIPAA/COMPLIANCE', label_map.get('HIPAA READY', '')))
        known = {'MADE BY', 'BEST FOR', 'PRICING', 'STARTING PRICE', 'HIPAA', 'HIPAA/COMPLIANCE', 'HIPAA READY'}
        for lbl, val in label_map.items():
            if lbl not in known:
                facts['custom_fact_label'] = lbl.title()
                facts['custom_fact_value'] = val
                break
        return facts

    # Find class="fact-bar" in the HTML body (not in <style> blocks)
    # Search from after </style> or from the first class="fact-bar" occurrence
    fb_match = re.search(r'class="fact-bar"', html)
    if not fb_match:
        return facts
    fb_start = fb_match.start()
    fb_end = html.find('</section>', fb_start)
    if fb_end == -1:
        fb_end = html.find('</div>', fb_start + 500)
    fact_section = html[fb_start:fb_end] if fb_end > 0 else html[fb_start:fb_start + 2000]

    # Extract each fact-item: two <p> tags — first is label, second is value
    label_map = {}
    items = re.finditer(r'<div[^>]*class="fact-item"[^>]*>(.*?)</div>', fact_section, re.DOTALL)
    for item in items:
        block = item.group(1)
        ps = re.findall(r'<p[^>]*>(.*?)</p>', block, re.DOTALL)
        if len(ps) >= 2:
            label_text = sanitize(ps[0]).upper().strip('.')
            value_text = sanitize(ps[1])
            if label_text and value_text:
                label_map[label_text] = value_text

    facts['made_by'] = label_map.get('MADE BY', '')
    facts['best_for_fact'] = label_map.get('BEST FOR', '')
    facts['pricing_fact'] = label_map.get('PRICING', label_map.get('STARTING PRICE', ''))
    facts['hipaa_fact'] = label_map.get('HIPAA', label_map.get('HIPAA READY', label_map.get('HIPAA/COMPLIANCE', '')))

    known_labels = {'MADE BY', 'BEST FOR', 'PRICING', 'STARTING PRICE', 'HIPAA',
                    'HIPAA READY', 'HIPAA/COMPLIANCE'}
    for label_text, value_text in label_map.items():
        if label_text not in known_labels:
            facts['custom_fact_label'] = label_text.title()
            facts['custom_fact_value'] = value_text
            break

    return facts


def extract_section_by_label(html, label_text):
    """Extract content for class-based pages using .section-label div as the section marker."""
    label_pat = rf'<div[^>]*class="section-label"[^>]*>[^<]*{re.escape(label_text)}[^<]*</div>'
    label_m = re.search(label_pat, html, re.IGNORECASE)
    if not label_m:
        return ""
    after_label = html[label_m.end():]
    h2_m = re.search(r'<h2[^>]*>.*?</h2>', after_label, re.DOTALL)
    if not h2_m:
        return ""
    content_start = label_m.end() + h2_m.end()
    next_boundary = re.search(
        r'<h2[^>]*>|<div[^>]*class="section-label"|<div[^>]*background:#f9fafb',
        html[content_start:]
    )
    end = content_start + next_boundary.start() if next_boundary else len(html)
    return clean_html(html[content_start:end])


def extract_section_html(html, heading_text):
    """Extract a section by heading text, returning the raw inner HTML
    (everything between this H2 and the next H2 or </section>).
    """
    patterns = [
        rf'<h2[^>]*>[^<]*{re.escape(heading_text)}[^<]*</h2>',
        rf'<h2[^>]*>.*?{re.escape(heading_text)}.*?</h2>',
    ]
    for pattern in patterns:
        match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
        if match:
            start = match.end()
            next_h2 = re.search(r'<h2[^>]*>', html[start:], re.IGNORECASE)
            next_section = re.search(r'</section>', html[start:], re.IGNORECASE)
            end = len(html)
            if next_h2:
                end = min(end, start + next_h2.start())
            if next_section:
                end = min(end, start + next_section.start())
            return html[start:end].strip()
    return ""


def extract_section_clean_html(html, heading_text):
    """Extract a section and return cleaned HTML (preserving structure)."""
    raw = extract_section_html(html, heading_text)
    return clean_html(raw)


def extract_profession_cards(html):
    """Extract profession cards as array of {name, description, link_slug}."""
    cards = []
    cards_section = extract_section_html(html, "How .* Works for Your Profession")
    if not cards_section:
        cards_section = extract_section_html(html, "Your Profession")
    if not cards_section:
        # Try finding the profession cards section by the industry-card class
        prof_start = html.find('class="industry-card"')
        if prof_start > 0:
            # Go back to find the section start
            section_start = html.rfind('<section', 0, prof_start)
            section_end = html.find('</section>', prof_start)
            if section_start > 0 and section_end > 0:
                cards_section = html[section_start:section_end]

    if not cards_section:
        return cards

    card_blocks = re.findall(
        r'class="industry-card"[^>]*>(.*?)</div>',
        cards_section, re.DOTALL
    )

    for block in card_blocks:
        name_match = re.search(r'<h3[^>]*>(.*?)</h3>', block, re.DOTALL)
        desc_match = re.search(r'<p[^>]*>(.*?)</p>', block, re.DOTALL)
        link_match = re.search(r'href="([^"]*)"', block)

        name = sanitize(name_match.group(1)) if name_match else ""
        description = sanitize(desc_match.group(1)) if desc_match else ""
        link_slug = ""
        if link_match:
            href = link_match.group(1)
            # Convert "chatgpt/legal.html" to "chatgpt/legal"
            href = re.sub(r'\.html$', '', href)
            href = href.replace('../', '')
            link_slug = href

        if name:
            cards.append({
                "name": name,
                "description": description,
                "link_slug": link_slug,
            })

    return cards


def _inline_pricing_table(h):
    """Convert class-based pricing table to inline styles for reliable rendering in WordPress."""
    h = re.sub(
        r'<table[^>]*class="pricing-table"[^>]*>',
        '<table style="width:100%;border-collapse:collapse;font-size:0.9rem;">',
        h
    )
    h = re.sub(
        r'<th(\s[^>]*)?>',
        '<th style="text-align:left;padding:0.75rem 1rem;background:#f9fafb;font-size:0.75rem;'
        'font-weight:700;text-transform:uppercase;letter-spacing:0.06em;color:#6b7280;'
        'border-bottom:2px solid #e5e7eb;">',
        h
    )
    h = re.sub(
        r'<td(\s[^>]*)?>',
        '<td style="padding:0.75rem 1rem;border-bottom:1px solid #f3f4f6;color:#374151;vertical-align:top;">',
        h
    )
    h = re.sub(
        r'<span[^>]*class="tier-name"[^>]*>(.*?)</span>',
        r'<span style="font-weight:600;color:#111111;">\1</span>',
        h, flags=re.DOTALL
    )
    return h


def extract_pricing_html(html):
    """Extract the entire pricing section inner HTML (table + paragraphs below it)."""
    raw = extract_section_html(html, "Pricing")
    if raw:
        result = clean_html(raw)
        return _inline_pricing_table(result)
    return ""


def extract_comparison_html(html):
    """Extract the entire comparison table section inner HTML."""
    raw = extract_section_html(html, "vs. The Alternatives")
    if not raw:
        raw = extract_section_html(html, "Alternatives")
    if not raw:
        raw = extract_section_html(html, "Compare")
    if raw:
        return clean_html(raw)
    return ""


def extract_related_guides_html(html):
    """Extract the related guides section inner HTML."""
    raw = extract_section_html(html, "Related Guides")
    if raw:
        return clean_html(raw)
    return ""


def safe_json_content(data_dict):
    """Serialize data to JSON, ensuring no ../ patterns that trigger WAF."""
    json_str = json.dumps(data_dict, ensure_ascii=False)
    json_str = json_str.replace('../', '').replace('..\\\\', '')
    return json_str


# ── API functions ──

def delete_all_posts(post_type):
    """Delete all posts of a given type."""
    page = 1
    total = 0
    while True:
        resp = requests.get(f'{WP_URL}/wp/v2/{post_type}?per_page=100&page={page}', auth=AUTH)
        if resp.status_code != 200:
            break
        posts = resp.json()
        if not posts:
            break
        for p in posts:
            requests.delete(f'{WP_URL}/wp/v2/{post_type}/{p["id"]}?force=true', auth=AUTH)
            total += 1
        page += 1
    return total


def create_post(post_type, title, slug, data_dict, meta=None, status='publish'):
    """Create a post with JSON content and optional meta."""
    endpoint = f"{WP_URL}/wp/v2/{post_type}"

    payload = {
        "title": title,
        "slug": slug,
        "status": status,
        "content": safe_json_content(data_dict),
    }
    if meta:
        payload["meta"] = meta

    resp = requests.post(endpoint, json=payload, auth=AUTH)
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


# ── Tool Review Migration ──

def migrate_tool_review(tool_def):
    filepath = BASE_DIR / tool_def['file']
    if not filepath.exists():
        print(f"  File not found: {filepath}")
        return None

    html = filepath.read_text(encoding='utf-8')

    subtitle = extract_subtitle(html)
    definition_sentence = extract_definition_sentence(html)
    positioning_statement = extract_positioning_statement(html)
    publish_date = extract_publish_date(html)
    verdict_description = extract_verdict_description(html)
    blocks = extract_consistency_blocks(html)
    facts = extract_quick_facts_tool(html)
    faq = extract_faq(html)
    sources = extract_sources(html)
    reviews_miss = extract_reviews_miss(html)

    # Preserve full HTML for rich content sections
    what_it_is = extract_section_clean_html(html, "What .* Is")
    if not what_it_is:
        what_it_is = extract_section_clean_html(html, "What It Is")
    if not what_it_is:
        what_it_is = extract_section_by_label(html, "Overview")
    who_right_for = extract_section_clean_html(html, "Who .* Right For")
    if not who_right_for:
        who_right_for = extract_section_clean_html(html, "Who It")
    if not who_right_for:
        who_right_for = extract_section_by_label(html, "Fit Assessment")
    verdict_text = extract_section_clean_html(html, "My Verdict")
    if not verdict_text:
        verdict_text = extract_section_clean_html(html, "Our Verdict")
    if not verdict_text:
        verdict_text = extract_section_by_label(html, "My Verdict")

    # Features - preserve HTML in descriptions
    features = []
    features_section = extract_section_html(html, "Features That Matter")
    if features_section:
        h3s = list(re.finditer(r'<h3[^>]*>(.*?)</h3>', features_section, re.DOTALL))
        for i, h3 in enumerate(h3s):
            name = sanitize(h3.group(1))
            start = h3.end()
            end = h3s[i + 1].start() if i + 1 < len(h3s) else len(features_section)
            desc_html = features_section[start:end]
            features.append({
                "feature_name": name,
                "feature_icon": "",
                "feature_description": clean_html(desc_html),
            })
    # Fallback: class-based .feature-item format (cursor, notion-ai, grammarly, otter)
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

    # Pricing - preserve full HTML
    pricing_html = extract_pricing_html(html)

    # Pricing tiers (structured data, still useful for templates)
    pricing = []
    pricing_section = extract_section_html(html, "Pricing")
    if pricing_section:
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', pricing_section, re.DOTALL)
        for row in rows:
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
            if len(cells) >= 2:
                pricing.append({
                    "tier_name": sanitize(cells[0]),
                    "tier_price": sanitize(cells[1]),
                    "tier_features": sanitize(cells[2]) if len(cells) > 2 else ""
                })

    # Comparison - preserve full HTML
    comparison_html = extract_comparison_html(html)

    # Profession cards
    profession_cards = extract_profession_cards(html)

    # Related guides - preserve full HTML
    related_guides_html = extract_related_guides_html(html)

    data = {
        "tool_name": tool_def['name'],
        "tool_slug": tool_def['slug'],
        "verdict_type": tool_def['verdict'],
        "subtitle": subtitle,
        "definition_sentence": definition_sentence,
        "positioning_statement": positioning_statement,
        "publish_date": publish_date,
        "verdict_description": verdict_description,
        "consistency_blocks": blocks,
        "quick_facts": facts,
        "what_it_is": what_it_is[:10000],
        "who_its_right_for": who_right_for[:10000],
        "verdict_text": verdict_text[:10000],
        "features": features[:7],
        "pricing_tiers": pricing,
        "pricing_html": pricing_html[:10000],
        "comparison_html": comparison_html[:10000],
        "profession_cards": profession_cards,
        "related_guides_html": related_guides_html[:5000],
        "faq": faq,
        "sources": sources,
        "reviews_miss": reviews_miss,
    }

    return create_post("tool_review", tool_def['name'], tool_def['slug'], data)


# ── Profession Hub Migration ──

def migrate_profession_hub(prof_def):
    filepath = BASE_DIR / prof_def['file']
    if not filepath.exists():
        print(f"  File not found: {filepath}")
        return None

    html = filepath.read_text(encoding='utf-8')

    # Eyebrow badge text (e.g. "Architects. 4 Tools Reviewed")
    eyebrow_match = re.search(r'text-transform:uppercase[^>]*>\s*([^<]+?)\s*</div>', html)
    eyebrow = sanitize(eyebrow_match.group(1)) if eyebrow_match else f"AI Tools for {prof_def['name']}"

    # Lede paragraph (under H1)
    lede_match = re.search(r'</h1>\s*<p[^>]*>(.*?)</p>', html, re.DOTALL)
    lede = sanitize(lede_match.group(1)) if lede_match else ""

    # Publish date from byline
    pub_date = extract_publish_date(html)

    # Use cases section H2 title
    uc_h2_match = re.search(r'<h2[^>]*>(.*?)</h2>', html, re.DOTALL)
    use_cases_title = sanitize(uc_h2_match.group(1)) if uc_h2_match else ""

    # Use cases intro paragraph
    uc_intro = ""
    if uc_h2_match:
        after_h2 = html[uc_h2_match.end():]
        intro_match = re.search(r'<p[^>]*>(.*?)</p>', after_h2, re.DOTALL)
        if intro_match:
            uc_intro = sanitize(intro_match.group(1))

    # Use case cards (category, title, description, recommended tools)
    use_cases = []
    uc_cards = re.finditer(
        r'text-transform:uppercase[^>]*>([A-Z\s]+)</div>\s*'
        r'<h3[^>]*>(.*?)</h3>\s*'
        r'<p[^>]*>(.*?)</p>\s*'
        r'(?:<div[^>]*>\s*<span[^>]*>Try:</span>\s*<span[^>]*>(.*?)</span>)?',
        html, re.DOTALL
    )
    for uc in uc_cards:
        use_cases.append({
            "category": sanitize(uc.group(1)),
            "title": sanitize(uc.group(2)),
            "description": sanitize(uc.group(3)),
            "recommended": sanitize(uc.group(4)) if uc.group(4) else "",
        })

    # Caution/liability notice
    caution = ""
    caution_match = re.search(r'PROFESSIONAL LIABILITY.*?<p[^>]*>(.*?)</p>\s*</div>', html, re.DOTALL)
    if not caution_match:
        caution_match = re.search(r'(?:CAUTION|IMPORTANT).*?<p[^>]*>(.*?)</p>\s*</div>', html, re.DOTALL)
    if caution_match:
        caution = sanitize(caution_match.group(1))

    # Tool cards (name, verdict, maker, description, features, link)
    tool_cards = []
    tc_iter = re.finditer(
        r'<h3[^>]*>([\w\s.]+)</h3>\s*'
        r'<span[^>]*>(Recommended|Specialized)</span>\s*</div>\s*'
        r'<p[^>]*>Made by ([^<]+)</p>\s*'
        r'<p[^>]*>(.*?)</p>\s*'
        r'<ul[^>]*>(.*?)</ul>\s*'
        r'<a\s+href="([^"]*)"',
        html, re.DOTALL
    )
    for tc in tc_iter:
        features = [sanitize(li) for li in re.findall(r'<li[^>]*>(.*?)</li>', tc.group(5), re.DOTALL)]
        # Convert link from static to WP: "chatgpt/architects.html" -> "/chatgpt/architects/"
        link = tc.group(6)
        link = re.sub(r'^(\.\./)?([\w-]+)/([\w-]+)\.html$', r'/\2/\3/', link)
        tool_cards.append({
            "name": sanitize(tc.group(1)),
            "verdict": sanitize(tc.group(2)).lower(),
            "maker": sanitize(tc.group(3)),
            "description": sanitize(tc.group(4)),
            "features": features,
            "link": link,
        })

    faq = extract_faq(html)

    # Tools count
    tool_count = len(tool_cards) if tool_cards else 0

    data = {
        "profession_name": prof_def['name'],
        "profession_slug": prof_def['slug'],
        "eyebrow_text": eyebrow,
        "lede": lede,
        "publish_date": pub_date,
        "use_cases_title": use_cases_title,
        "use_cases_intro": uc_intro,
        "use_cases": use_cases,
        "caution_notice": caution,
        "tool_cards": tool_cards,
        "tool_count": tool_count,
        "faq": faq,
    }

    return create_post("profession_hub", prof_def['name'], prof_def['slug'], data)


# ── Cross-Reference Migration ──

def migrate_cross_reference(tool_slug, prof_slug, tool_id, prof_id, tool_name, prof_name, tool_verdict):
    filepath = BASE_DIR / tool_slug / f"{prof_slug}.html"
    if not filepath.exists():
        return None

    html = filepath.read_text(encoding='utf-8')

    subtitle = extract_subtitle(html)
    blocks = extract_consistency_blocks(html)
    faq = extract_faq(html)
    sources = extract_sources(html)
    reviews_miss = extract_reviews_miss(html)

    # Content sections - preserve HTML in section bodies
    content_sections = []
    h2s = list(re.finditer(r'<h2[^>]*>(.*?)</h2>', html, re.DOTALL))
    skip = {'Frequently Asked Questions', 'FAQ', 'Sources Checked', 'What Most Reviews Miss',
            'Related Guides', 'My Verdict', 'Our Verdict'}

    for i, h2 in enumerate(h2s):
        t = sanitize(h2.group(1))
        if t in skip or 'Prompts That Work' in t:
            continue
        if 'How' in t and 'Compare' in t:
            continue
        start = h2.end()
        end = h2s[i + 1].start() if i + 1 < len(h2s) else len(html)
        body_html = html[start:end]
        body = clean_html(body_html)[:5000]
        if t and body:
            content_sections.append({"section_title": t, "section_body": body})

    # Verdict - preserve HTML
    verdict = ""
    for h2 in h2s:
        t = sanitize(h2.group(1))
        if t in ('My Verdict', 'Our Verdict'):
            start = h2.end()
            next_h2 = re.search(r'<h2[^>]*>', html[start:])
            next_sec = re.search(r'</section>', html[start:])
            end = len(html)
            if next_h2:
                end = min(end, start + next_h2.start())
            if next_sec:
                end = min(end, start + next_sec.start())
            verdict = clean_html(html[start:end])[:5000]
            break

    # Comparison - preserve HTML
    comparison = ""
    for h2 in h2s:
        t = sanitize(h2.group(1))
        if 'How' in t and 'Compare' in t:
            start = h2.end()
            next_h2 = re.search(r'<h2[^>]*>', html[start:])
            next_sec = re.search(r'</section>', html[start:])
            end = len(html)
            if next_h2:
                end = min(end, start + next_h2.start())
            if next_sec:
                end = min(end, start + next_sec.start())
            comparison = clean_html(html[start:end])[:5000]
            break

    # Prompts - preserve HTML in prompt text
    prompts = []
    ps = extract_between(html, 'Prompts That Work', '</section>')
    if ps:
        pt = re.findall(r'font-weight:\s*600[^>]*>(.*?)</p>', ps, re.DOTALL)
        pb = re.findall(r'class="prompt-block"[^>]*>(.*?)</div>', ps, re.DOTALL)
        for j in range(min(len(pt), len(pb))):
            prompts.append({
                "prompt_title": sanitize(pt[j]),
                "prompt_text": clean_html(pb[j]),
            })

    # Also try extracting prompts from content sections (cross-ref pages
    # often have prompts inline within sections)
    if not prompts:
        prompt_titles = re.findall(r'class="prompt-label"[^>]*>(.*?)</(?:p|div)>', html, re.DOTALL)
        prompt_blocks = re.findall(r'class="prompt-block"[^>]*>(.*?)</div>', html, re.DOTALL)
        for j in range(min(len(prompt_titles), len(prompt_blocks))):
            prompts.append({
                "prompt_title": sanitize(prompt_titles[j]),
                "prompt_text": clean_html(prompt_blocks[j]),
            })

    # Publish date
    pub_date = extract_publish_date(html)

    # Quick facts
    quick_facts = {}
    fact_section = extract_between(html, 'fact-bar', '</section>')
    if not fact_section:
        fact_section = extract_between(html, 'fact-bar', '</div>\n  </div>')
    labels = re.findall(r'fact-label[^>]*>(.*?)</(?:p|div)>', fact_section, re.DOTALL)
    values = re.findall(r'fact-value[^>]*>(.*?)</(?:p|div)>', fact_section, re.DOTALL)
    subs = re.findall(r'fact-sub[^>]*>(.*?)</(?:p|div)>', fact_section, re.DOTALL)
    for j, label in enumerate(labels):
        lt = sanitize(label).upper()
        vt = sanitize(values[j]) if j < len(values) else ""
        st = sanitize(subs[j]) if j < len(subs) else ""
        if 'MADE BY' in lt:
            quick_facts['made_by'] = vt
            if st:
                quick_facts['made_by_sub'] = st
        elif 'BEST FOR' in lt:
            quick_facts['best_for'] = vt
            if st:
                quick_facts['best_for_sub'] = st
        elif 'PRICING' in lt or 'PRICE' in lt:
            quick_facts['pricing'] = vt
            if st:
                quick_facts['pricing_sub'] = st
        elif 'COMPLIANCE' in lt or 'HIPAA' in lt or 'CONFIDENTIALITY' in lt:
            quick_facts['compliance'] = vt
            if st:
                quick_facts['compliance_sub'] = st
        elif 'COMPARE' in lt or 'ALTERNATIVE' in lt or 'INSTEAD' in lt:
            quick_facts['compared_to'] = vt

    data = {
        "verdict_type": tool_verdict,
        "subtitle": subtitle,
        "publish_date": pub_date,
        "consistency_blocks": blocks,
        "quick_facts": quick_facts,
        "content_sections": content_sections[:8],
        "prompts": prompts[:6],
        "comparison_notes": comparison,
        "verdict_text": verdict,
        "faq": faq,
        "sources": sources,
        "reviews_miss": reviews_miss,
    }

    title = f"{tool_name} for {prof_name}"
    slug = f"{tool_slug}-{prof_slug}"
    meta = {"linked_tool": tool_id, "linked_profession": prof_id}

    return create_post("cross_reference", title, slug, data, meta=meta)


def main():
    print("=" * 60)
    print("AI Tools for Pros — Migration v2")
    print("Data stored as JSON in post_content")
    print("=" * 60)

    # Step 0: Delete existing posts
    print("\n── Step 0: Cleaning up existing posts ──")
    for pt in ['cross_reference', 'profession_hub', 'tool_review']:
        n = delete_all_posts(pt)
        print(f"  Deleted {n} {pt} posts")
        time.sleep(1)

    # Step 1: Tool Reviews
    print("\n── Step 1: Tool Reviews (10 pages) ──")
    tool_ids = {}
    for tool in TOOLS:
        print(f"\n  Migrating: {tool['name']}...")
        post_id = migrate_tool_review(tool)
        if post_id:
            tool_ids[tool['slug']] = {'id': post_id, 'name': tool['name'], 'verdict': tool['verdict']}
        time.sleep(0.5)

    print(f"\n  Tool reviews: {len(tool_ids)}/10")

    # Step 2: Profession Hubs
    print("\n── Step 2: Profession Hubs (8 pages) ──")
    prof_ids = {}
    for prof in PROFESSIONS:
        print(f"\n  Migrating: {prof['name']}...")
        post_id = migrate_profession_hub(prof)
        if post_id:
            prof_ids[prof['slug']] = {'id': post_id, 'name': prof['name']}
        time.sleep(0.5)

    print(f"\n  Profession hubs: {len(prof_ids)}/8")

    # Step 3: Cross-References
    print("\n── Step 3: Cross-Reference Pages ──")
    xref_count = 0
    xref_fail = 0
    for tool_slug, tool_info in tool_ids.items():
        for prof_slug, prof_info in prof_ids.items():
            filepath = BASE_DIR / tool_slug / f"{prof_slug}.html"
            if not filepath.exists():
                continue
            print(f"\n  {tool_info['name']} for {prof_info['name']}...")
            post_id = migrate_cross_reference(
                tool_slug, prof_slug,
                tool_info['id'], prof_info['id'],
                tool_info['name'], prof_info['name'],
                tool_info['verdict']
            )
            if post_id:
                xref_count += 1
            else:
                xref_fail += 1
            time.sleep(0.5)

    # Summary
    print("\n" + "=" * 60)
    print("Migration v2 Complete!")
    print(f"  Tool Reviews:      {len(tool_ids)}")
    print(f"  Profession Hubs:   {len(prof_ids)}")
    print(f"  Cross-References:  {xref_count}" + (f" ({xref_fail} failed)" if xref_fail else ""))
    print(f"  Total:             {len(tool_ids) + len(prof_ids) + xref_count}")
    print("=" * 60)


if __name__ == "__main__":
    main()
