#!/usr/bin/env python3
"""
Add contextual internal links to all 10 tool hub pages and 8 profession hub pages.

Tool hub pages: append a paragraph to verdict_text listing the profession-specific xref children.
Profession hub pages: append a paragraph to use_cases_intro listing the tool-specific xref children.

Idempotent: skips pages that already contain the sentinel phrase.
"""

import urllib.request, json, ssl, base64

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

CREDS = base64.b64encode(b'rmigliorisi:pj60 SqmD OSRD pSe1 9DsV BEeh').decode()
HEADERS = {'Authorization': f'Basic {CREDS}', 'Content-Type': 'application/json'}
BASE = 'https://aitoolsforpros.com/wp-json/wp/v2'


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


# ── Existing xref matrix ─────────────────────────────────────────────────────

EXISTING_XREFS = {
    'chatgpt':    ['architects', 'creatives', 'engineers', 'finance', 'insurance', 'legal', 'physicians', 'real-estate'],
    'claude':     ['architects', 'creatives', 'engineers', 'finance', 'insurance', 'legal', 'physicians', 'real-estate'],
    'perplexity': ['finance', 'insurance', 'legal', 'physicians'],
    'gemini':     ['architects', 'finance', 'legal', 'real-estate'],
    'copilot':    ['engineers', 'finance', 'insurance', 'legal', 'physicians', 'real-estate'],
    'midjourney': ['architects', 'creatives'],
    'cursor':     ['engineers'],
    'notion-ai':  ['creatives', 'engineers', 'legal'],
    'grammarly':  ['creatives', 'insurance', 'legal', 'real-estate'],
    'otter':      ['physicians'],
}

# Descriptive anchor text for each tool × profession combo
# Used when linking FROM a tool hub TO its xref children
TOOL_XREF_ANCHORS = {
    'chatgpt': {
        'architects':  'ChatGPT for architects',
        'creatives':   'ChatGPT for creative professionals',
        'engineers':   'ChatGPT for software engineers',
        'finance':     'ChatGPT for finance professionals',
        'insurance':   'ChatGPT for insurance professionals',
        'legal':       'ChatGPT for lawyers',
        'physicians':  'ChatGPT for physicians',
        'real-estate': 'ChatGPT for real estate agents',
    },
    'claude': {
        'architects':  'Claude for architects',
        'creatives':   'Claude for creative professionals',
        'engineers':   'Claude for software engineers',
        'finance':     'Claude for finance professionals',
        'insurance':   'Claude for insurance workflows',
        'legal':       'Claude for contract review and legal work',
        'physicians':  'Claude for clinical documentation',
        'real-estate': 'Claude for real estate agents',
    },
    'perplexity': {
        'finance':    'Perplexity AI for financial research',
        'insurance':  'Perplexity AI for insurance professionals',
        'legal':      'Perplexity AI for legal research',
        'physicians': 'Perplexity AI for physicians',
    },
    'gemini': {
        'architects':  'Google Gemini for architects',
        'finance':     'Google Gemini for finance professionals',
        'legal':       'Google Gemini for legal professionals',
        'real-estate': 'Google Gemini for real estate agents',
    },
    'copilot': {
        'engineers':   'Microsoft Copilot for software engineers',
        'finance':     'Microsoft Copilot for financial advisors',
        'insurance':   'Microsoft Copilot for insurance professionals',
        'legal':       'Microsoft Copilot for legal professionals',
        'physicians':  'Microsoft Copilot for physicians',
        'real-estate': 'Microsoft Copilot for real estate agents',
    },
    'midjourney': {
        'architects': 'Midjourney for architectural visualization',
        'creatives':  'Midjourney for creative professionals',
    },
    'cursor': {
        'engineers': 'Cursor for software engineers',
    },
    'notion-ai': {
        'creatives': 'Notion AI for content creators',
        'engineers': 'Notion AI for software engineers',
        'legal':     'Notion AI for legal teams',
    },
    'grammarly': {
        'creatives':   'Grammarly for creative writers',
        'insurance':   'Grammarly for insurance professionals',
        'legal':       'Grammarly for legal writing',
        'real-estate': 'Grammarly for real estate agents',
    },
    'otter': {
        'physicians': 'Otter.ai for physicians',
    },
}

# Descriptive anchor text for each profession × tool combo
# Used when linking FROM a profession hub TO its xref children
PROF_XREF_ANCHORS = {
    'architects': {
        'chatgpt':    'ChatGPT for architects',
        'claude':     'Claude for architectural projects',
        'gemini':     'Google Gemini for architectural research',
        'midjourney': 'Midjourney for architectural visualization',
    },
    'creatives': {
        'chatgpt':    'ChatGPT for creative professionals',
        'claude':     'Claude for content creation',
        'grammarly':  'Grammarly for creative writing',
        'midjourney': 'Midjourney for creative work',
        'notion-ai':  'Notion AI for content creators',
    },
    'engineers': {
        'chatgpt':   'ChatGPT for software engineers',
        'claude':    'Claude for code review',
        'copilot':   'Microsoft Copilot for engineers',
        'cursor':    'Cursor for software development',
        'notion-ai': 'Notion AI for engineering documentation',
    },
    'finance': {
        'chatgpt':    'ChatGPT for finance professionals',
        'claude':     'Claude for financial analysis',
        'copilot':    'Microsoft Copilot for financial advisors',
        'gemini':     'Google Gemini for financial research',
        'perplexity': 'Perplexity AI for financial research',
    },
    'insurance': {
        'chatgpt':    'ChatGPT for insurance professionals',
        'claude':     'Claude for insurance workflows',
        'copilot':    'Microsoft Copilot for insurance',
        'grammarly':  'Grammarly for insurance writing',
        'perplexity': 'Perplexity AI for insurance research',
    },
    'legal': {
        'chatgpt':    'ChatGPT for lawyers',
        'claude':     'Claude for contract review',
        'copilot':    'Microsoft Copilot for legal professionals',
        'grammarly':  'Grammarly for legal writing',
        'notion-ai':  'Notion AI for legal knowledge management',
        'perplexity': 'Perplexity AI for legal research',
    },
    'physicians': {
        'chatgpt':    'ChatGPT for physicians',
        'claude':     'Claude for clinical documentation',
        'copilot':    'Microsoft Copilot for physicians',
        'otter':      'Otter.ai for medical documentation',
        'perplexity': 'Perplexity AI for medical research',
    },
    'real-estate': {
        'chatgpt':   'ChatGPT for real estate agents',
        'claude':    'Claude for real estate professionals',
        'copilot':   'Microsoft Copilot for real estate agents',
        'gemini':    'Google Gemini for real estate research',
        'grammarly': 'Grammarly for real estate writing',
    },
}

TOOL_NAMES = {
    'chatgpt':    'ChatGPT',
    'claude':     'Claude',
    'perplexity': 'Perplexity AI',
    'gemini':     'Google Gemini',
    'copilot':    'Microsoft Copilot',
    'midjourney': 'Midjourney',
    'cursor':     'Cursor',
    'notion-ai':  'Notion AI',
    'grammarly':  'Grammarly',
    'otter':      'Otter.ai',
}

PROF_NAMES = {
    'architects':  'architects',
    'creatives':   'creative professionals',
    'engineers':   'software engineers',
    'finance':     'finance professionals',
    'insurance':   'insurance professionals',
    'legal':       'legal professionals',
    'physicians':  'physicians',
    'real-estate': 'real estate agents',
}

SENTINEL = 'profession-specific guide'   # idempotency check for tool hubs
PROF_SENTINEL = 'tool-specific guide'    # idempotency check for profession hubs


def build_tool_hub_paragraph(tool_slug):
    """Build a paragraph for a tool hub page linking to all its xref children."""
    children = EXISTING_XREFS.get(tool_slug, [])
    if not children:
        return None
    tool_name = TOOL_NAMES[tool_slug]
    anchors = TOOL_XREF_ANCHORS.get(tool_slug, {})
    links = []
    for prof_slug in sorted(children):
        anchor = anchors.get(prof_slug, f'{tool_name} for {PROF_NAMES.get(prof_slug, prof_slug)}')
        links.append(f'<a href="/{tool_slug}/{prof_slug}/">{anchor}</a>')

    if len(links) == 1:
        link_str = links[0]
    elif len(links) == 2:
        link_str = f'{links[0]} and {links[1]}'
    else:
        link_str = ', '.join(links[:-1]) + f', and {links[-1]}'

    return (
        f'<p>I have a profession-specific guide for each major field. '
        f'You can go deeper with {link_str}.</p>'
    )


def build_prof_hub_paragraph(prof_slug):
    """Build a paragraph for a profession hub page linking to all its xref children."""
    anchors = PROF_XREF_ANCHORS.get(prof_slug, {})
    if not anchors:
        return None
    prof_name = PROF_NAMES.get(prof_slug, prof_slug)
    links = []
    # Sort by tool slug for consistent ordering
    for tool_slug, anchor in sorted(anchors.items()):
        links.append(f'<a href="/{tool_slug}/{prof_slug}/">{anchor}</a>')

    if len(links) == 1:
        link_str = links[0]
    elif len(links) == 2:
        link_str = f'{links[0]} and {links[1]}'
    else:
        link_str = ', '.join(links[:-1]) + f', and {links[-1]}'

    return (
        f'<p>I have a tool-specific guide for each major AI tool used by {prof_name}: '
        f'{link_str}.</p>'
    )


# ── Process tool hub pages ───────────────────────────────────────────────────

print("=" * 60)
print("TOOL HUB PAGES")
print("=" * 60)

tool_posts = api_get('/tool_review?per_page=100&context=edit&_fields=id,slug,content')
print(f"Found {len(tool_posts)} tool_review posts\n")

tool_updated = 0
tool_skipped = 0
tool_errors = 0

for p in tool_posts:
    slug = p['slug']
    post_id = p['id']

    raw_content = p.get('content', {}).get('raw', '')
    if not raw_content:
        print(f"  SKIP {slug}: empty content")
        tool_skipped += 1
        continue

    try:
        data = json.loads(raw_content)
    except json.JSONDecodeError as e:
        print(f"  ERROR {slug}: JSON parse failed: {e}")
        tool_errors += 1
        continue

    # Idempotency check
    verdict = data.get('verdict_text', '')
    if SENTINEL in verdict:
        print(f"  SKIP {slug}: already has profession links")
        tool_skipped += 1
        continue

    new_para = build_tool_hub_paragraph(slug)
    if not new_para:
        print(f"  SKIP {slug}: no xref children defined")
        tool_skipped += 1
        continue

    # Append to verdict_text; if empty, fall back to who_its_right_for
    if verdict:
        data['verdict_text'] = verdict.rstrip() + '\n' + new_para
    else:
        wir = data.get('who_its_right_for', '')
        if wir:
            data['who_its_right_for'] = wir.rstrip() + '\n' + new_para
        else:
            print(f"  SKIP {slug}: no verdict_text or who_its_right_for to append to")
            tool_skipped += 1
            continue

    try:
        result = api_put(f'/tool_review/{post_id}', {'content': json.dumps(data)})
        if 'id' in result:
            child_count = len(EXISTING_XREFS.get(slug, []))
            print(f"  OK  {slug} — +{child_count} child links added (post {post_id})")
            tool_updated += 1
        else:
            print(f"  FAIL {slug}: {result.get('message', str(result)[:100])}")
            tool_errors += 1
    except Exception as e:
        print(f"  ERROR {slug}: {e}")
        tool_errors += 1


# ── Process profession hub pages ─────────────────────────────────────────────

print()
print("=" * 60)
print("PROFESSION HUB PAGES")
print("=" * 60)

prof_posts = api_get('/profession_hub?per_page=100&context=edit&_fields=id,slug,content')
print(f"Found {len(prof_posts)} profession_hub posts\n")

prof_updated = 0
prof_skipped = 0
prof_errors = 0

for p in prof_posts:
    slug = p['slug']
    post_id = p['id']

    raw_content = p.get('content', {}).get('raw', '')
    if not raw_content:
        print(f"  SKIP {slug}: empty content")
        prof_skipped += 1
        continue

    try:
        data = json.loads(raw_content)
    except json.JSONDecodeError as e:
        print(f"  ERROR {slug}: JSON parse failed: {e}")
        prof_errors += 1
        continue

    # Idempotency check
    uci = data.get('use_cases_intro', '')
    if PROF_SENTINEL in uci:
        print(f"  SKIP {slug}: already has tool links")
        prof_skipped += 1
        continue

    new_para = build_prof_hub_paragraph(slug)
    if not new_para:
        print(f"  SKIP {slug}: no xref children defined for this profession")
        prof_skipped += 1
        continue

    # Append to use_cases_intro; if empty, try lede
    if uci:
        data['use_cases_intro'] = uci.rstrip() + '\n' + new_para
    else:
        lede = data.get('lede', '')
        if lede:
            data['lede'] = lede.rstrip() + '\n' + new_para
        else:
            print(f"  SKIP {slug}: no use_cases_intro or lede to append to")
            prof_skipped += 1
            continue

    try:
        result = api_put(f'/profession_hub/{post_id}', {'content': json.dumps(data)})
        if 'id' in result:
            child_count = len(PROF_XREF_ANCHORS.get(slug, {}))
            print(f"  OK  {slug} — +{child_count} child links added (post {post_id})")
            prof_updated += 1
        else:
            print(f"  FAIL {slug}: {result.get('message', str(result)[:100])}")
            prof_errors += 1
    except Exception as e:
        print(f"  ERROR {slug}: {e}")
        prof_errors += 1


# ── Summary ──────────────────────────────────────────────────────────────────

print()
print("=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Tool hub pages:       {tool_updated} updated, {tool_skipped} skipped, {tool_errors} errors")
print(f"Profession hub pages: {prof_updated} updated, {prof_skipped} skipped, {prof_errors} errors")
print(f"Total updated:        {tool_updated + prof_updated}")
