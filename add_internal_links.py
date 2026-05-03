#!/usr/bin/env python3
"""
Add contextual internal links to all cross-reference pages in WordPress.

Strategy per cross-reference page (tool × profession):
  1. Append a "Comparing your options?" paragraph to verdict_text with links to:
       - Parent tool hub  (/tool/)
       - Parent profession hub  (/profession/)
       - 2-3 competing tools that have the same profession page
  2. In comparison_notes: wrap the first bare occurrence of each competing tool name
     with a link to that tool's profession-specific page (where it exists).

Only modifies pages that haven't already had links injected (idempotent).
"""

import urllib.request, json, ssl, re
from wp_creds import HEADERS, BASE

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def api_get(path):
    req = urllib.request.Request(f'{BASE}{path}', headers=HEADERS)
    with urllib.request.urlopen(req, context=ctx) as r:
        return json.loads(r.read())


def api_put(path, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(f'{BASE}{path}', data=data, headers=HEADERS, method='POST')
    req.add_header('X-HTTP-Method-Override', 'PUT')
    with urllib.request.urlopen(req, context=ctx) as r:
        return json.loads(r.read())


# ── Site data ────────────────────────────────────────────────────────────────

# All existing cross-reference pages
EXISTING_XREFS = {
    'chatgpt':   ['architects', 'creatives', 'engineers', 'finance', 'insurance', 'legal', 'physicians', 'real-estate'],
    'claude':    ['architects', 'creatives', 'engineers', 'finance', 'insurance', 'legal', 'physicians', 'real-estate'],
    'perplexity':['finance', 'insurance', 'legal', 'physicians'],
    'gemini':    ['architects', 'finance', 'legal', 'real-estate'],
    'copilot':   ['engineers', 'finance', 'insurance', 'legal', 'physicians', 'real-estate'],
    'midjourney':['architects', 'creatives'],
    'cursor':    ['engineers'],
    'notion-ai': ['creatives', 'engineers', 'legal'],
    'grammarly': ['creatives', 'insurance', 'legal', 'real-estate'],
    'otter':     ['physicians'],
}

# All profession hubs that exist
EXISTING_PROF_HUBS = ['architects', 'creatives', 'engineers', 'finance', 'insurance', 'legal', 'physicians', 'real-estate']

TOOL_NAMES = {
    'chatgpt':   'ChatGPT',
    'claude':    'Claude',
    'perplexity':'Perplexity AI',
    'gemini':    'Google Gemini',
    'copilot':   'Microsoft Copilot',
    'midjourney':'Midjourney',
    'cursor':    'Cursor',
    'notion-ai': 'Notion AI',
    'grammarly': 'Grammarly',
    'otter':     'Otter.ai',
}

PROF_NAMES = {
    'architects': 'Architects',
    'creatives':  'Creatives',
    'engineers':  'Software Engineers',
    'finance':    'Finance Professionals',
    'insurance':  'Insurance Professionals',
    'legal':      'Legal Professionals',
    'physicians': 'Physicians',
    'real-estate':'Real Estate Agents',
}

# Varied anchor text for competing tool links (rotated by position)
ANCHOR_VARIANTS = {
    'chatgpt':   ['ChatGPT', 'ChatGPT for {prof}', 'ChatGPT in {prof} workflows'],
    'claude':    ['Claude', 'Claude for {prof}', 'Claude AI for {prof}'],
    'perplexity':['Perplexity AI', 'Perplexity for {prof}', 'Perplexity AI for {prof}'],
    'gemini':    ['Google Gemini', 'Google Gemini for {prof}', 'Gemini for {prof}'],
    'copilot':   ['Microsoft Copilot', 'Copilot for {prof}', 'Microsoft Copilot for {prof}'],
    'midjourney':['Midjourney', 'Midjourney for {prof}', 'Midjourney for {prof} work'],
    'cursor':    ['Cursor', 'Cursor for engineers', 'Cursor AI'],
    'notion-ai': ['Notion AI', 'Notion AI for {prof}', 'Notion AI for {prof} workflows'],
    'grammarly': ['Grammarly', 'Grammarly for {prof}', 'Grammarly for {prof} writing'],
    'otter':     ['Otter.ai', 'Otter.ai for {prof}', 'Otter.ai for {prof} documentation'],
}


def competing_tools(tool_slug, prof_slug, limit=3):
    """Return list of (slug, display_name) for tools that also have this profession page,
    excluding the current tool. Sorted by how common the tool is (most coverage first)."""
    competitors = []
    for t_slug, profs in EXISTING_XREFS.items():
        if t_slug != tool_slug and prof_slug in profs:
            competitors.append(t_slug)
    # Sort: tools with more profession coverage appear first (more established = better links)
    competitors.sort(key=lambda s: -len(EXISTING_XREFS[s]))
    return competitors[:limit]


def anchor_text(tool_slug, prof_slug, position=0):
    variants = ANCHOR_VARIANTS.get(tool_slug, [TOOL_NAMES[tool_slug]])
    text = variants[position % len(variants)]
    prof_short = PROF_NAMES.get(prof_slug, prof_slug).lower().rstrip('s')
    return text.replace('{prof}', prof_short)


def build_verdict_paragraph(tool_slug, prof_slug):
    """Build a contextual 'Comparing your options?' paragraph for verdict_text."""
    competitors = competing_tools(tool_slug, prof_slug)
    tool_name = TOOL_NAMES[tool_slug]
    prof_name = PROF_NAMES.get(prof_slug, prof_slug)

    if not competitors:
        # No competitors — just add parent hub links
        return (
            f'<p>For a broader look, see our full <a href="/{tool_slug}/">{tool_name} overview</a> '
            f'or browse all <a href="/{prof_slug}/">AI tools for {prof_name.lower()}</a>.</p>'
        )

    comp_links = []
    for i, c_slug in enumerate(competitors):
        c_name_anchor = anchor_text(c_slug, prof_slug, i)
        comp_links.append(f'<a href="/{c_slug}/{prof_slug}/">{c_name_anchor}</a>')

    if len(comp_links) == 1:
        comp_str = comp_links[0]
    elif len(comp_links) == 2:
        comp_str = f'{comp_links[0]} and {comp_links[1]}'
    else:
        comp_str = ', '.join(comp_links[:-1]) + f', and {comp_links[-1]}'

    return (
        f'<p>Comparing your options? Also see {comp_str}. '
        f'For the full picture, visit our <a href="/{tool_slug}/">{tool_name} overview</a> '
        f'or the complete <a href="/{prof_slug}/">AI tools for {prof_name.lower()} guide</a>.</p>'
    )


def add_comparison_links(html, tool_slug, prof_slug):
    """
    In comparison_notes HTML, wrap the first bare occurrence of each competing tool name
    with a link to their profession-specific page (where it exists).
    Only wraps text that is NOT already inside an <a> tag.
    """
    if not html:
        return html

    competitors = competing_tools(tool_slug, prof_slug)

    for c_slug in competitors:
        c_name = TOOL_NAMES[c_slug]
        href = f'/{c_slug}/{prof_slug}/'

        # Skip if this link is already present
        if href in html:
            continue

        # Build a regex that matches the tool name NOT already inside an <a> tag
        # Strategy: replace the first occurrence that is not preceded by href="
        # We look for the name surrounded by word boundaries / punctuation, not inside <a>
        escaped = re.escape(c_name)

        # Replace first occurrence of tool name that is NOT inside an anchor
        # Use a simple approach: split on existing <a ...>...</a> blocks, replace in non-link parts only
        def replace_first_outside_links(h, name, link_html):
            """Replace first occurrence of `name` that isn't inside an <a> tag."""
            parts = re.split(r'(<a\s[^>]*>.*?</a>)', h, flags=re.DOTALL)
            replaced = False
            for i, part in enumerate(parts):
                if replaced:
                    break
                if part.startswith('<a '):
                    continue  # skip existing link
                new_part, n = re.subn(re.escape(name), link_html, part, count=1)
                if n:
                    parts[i] = new_part
                    replaced = True
            return ''.join(parts)

        link_html = f'<a href="{href}">{c_name}</a>'
        html = replace_first_outside_links(html, c_name, link_html)

    return html


def already_linked(text):
    """Return True if the text already contains our internal links pattern."""
    return 'Comparing your options?' in (text or '') or \
           'For the full picture' in (text or '') or \
           'For a broader look' in (text or '')


# ── Main ────────────────────────────────────────────────────────────────────

print("Fetching all cross_reference posts...")
posts = api_get('/cross_reference?per_page=100&context=edit&_fields=id,slug,content')
print(f"Found {len(posts)} posts")

updated = 0
skipped = 0
errors = 0

for p in posts:
    slug = p['slug']            # e.g. "chatgpt-architects"
    post_id = p['id']

    # Parse tool_slug and prof_slug from the post slug
    # Slugs are "TOOL-PROFESSION" but tool or profession may have hyphens (notion-ai, real-estate)
    tool_slug = None
    prof_slug = None
    for t in EXISTING_XREFS:
        if slug.startswith(t + '-'):
            candidate_prof = slug[len(t) + 1:]
            if candidate_prof in EXISTING_PROF_HUBS:
                tool_slug = t
                prof_slug = candidate_prof
                break

    if not tool_slug or not prof_slug:
        print(f"  SKIP {slug}: could not parse tool/profession")
        skipped += 1
        continue

    # Get raw JSON content
    raw_content = p.get('content', {}).get('raw', '')
    if not raw_content:
        print(f"  SKIP {slug}: empty content")
        skipped += 1
        continue

    try:
        data = json.loads(raw_content)
    except json.JSONDecodeError as e:
        print(f"  ERROR {slug}: JSON parse failed: {e}")
        errors += 1
        continue

    # Check if already processed
    if already_linked(data.get('verdict_text', '')):
        print(f"  SKIP {slug}: already has internal links")
        skipped += 1
        continue

    changed = False

    # ── 1. Append contextual paragraph to verdict_text ──────────────────────
    verdict = data.get('verdict_text', '')
    if verdict:
        new_para = build_verdict_paragraph(tool_slug, prof_slug)
        data['verdict_text'] = verdict.rstrip() + '\n' + new_para
        changed = True
    else:
        # No verdict_text — append to last section_body
        sections = data.get('content_sections', [])
        if sections:
            last = sections[-1]
            body = last.get('section_body', '')
            new_para = build_verdict_paragraph(tool_slug, prof_slug)
            last['section_body'] = body.rstrip() + '\n' + new_para
            changed = True

    # ── 2. Add links in comparison_notes ────────────────────────────────────
    comp_notes = data.get('comparison_notes', '')
    if comp_notes:
        updated_comp = add_comparison_links(comp_notes, tool_slug, prof_slug)
        if updated_comp != comp_notes:
            data['comparison_notes'] = updated_comp
            changed = True

    if not changed:
        print(f"  SKIP {slug}: no suitable content fields found")
        skipped += 1
        continue

    # ── Push back to WordPress ───────────────────────────────────────────────
    try:
        result = api_put(f'/cross_reference/{post_id}', {'content': json.dumps(data)})
        if 'id' in result:
            comp_count = len(competing_tools(tool_slug, prof_slug))
            print(f"  OK  {slug} — +{comp_count + 2} links added (post {post_id})")
            updated += 1
        else:
            print(f"  FAIL {slug}: {result.get('message', str(result)[:100])}")
            errors += 1
    except Exception as e:
        print(f"  ERROR {slug}: {e}")
        errors += 1

print(f"\n{'='*50}")
print(f"INTERNAL LINKING REPORT")
print(f"{'='*50}")
print(f"Pages scanned:  {len(posts)}")
print(f"Pages updated:  {updated}")
print(f"Pages skipped:  {skipped}")
print(f"Errors:         {errors}")
