#!/usr/bin/env python3
"""
Replace inline-paragraph internal links on hub pages with clean bulleted lists.

Tool hubs:   strip paragraph from verdict_text, insert <ul> block
Profession hubs: strip paragraph from use_cases_intro, insert <ul> block

Idempotent: skips pages where a <ul> block with the sentinel href is already present.
"""

import urllib.request, json, ssl, re
from wp_creds import HEADERS, BASE

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Phrases that mark the old injected content (either run)
OLD_SENTINELS = ['profession-focused guides', 'profession-specific guide', 'tool-specific guide', 'tool-specific guidance']


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


def strip_injected(text):
    """Remove any injected block (paragraph or ul) we previously added."""
    if not text:
        return text
    for sentinel in OLD_SENTINELS:
        if sentinel not in text:
            continue
        # Walk backwards looking for the start of a <p> or <ul> block containing the sentinel
        for tag in ['\n<ul', '\n<p>']:
            idx = text.rfind(tag)
            while idx != -1:
                if sentinel in text[idx:]:
                    return text[:idx].rstrip()
                idx = text.rfind(tag, 0, idx)
    return text


def already_bulleted(text, sentinel_href):
    """Return True if text contains a <ul> block with the sentinel href."""
    return bool(text and '<ul>' in text and sentinel_href in text)


def ul_block(intro, items):
    """Build '<p>intro</p>\n<ul>\n<li>...</li>\n</ul>' block."""
    li_lines = '\n'.join(f'<li>{item}</li>' for item in items)
    return f'<p>{intro}</p>\n<ul>\n{li_lines}\n</ul>'


# ── Tool hub bullet blocks ─────────────────────────────────────────────────────

TOOL_BULLETS = {
    'chatgpt': ul_block(
        'If your work is specialized, I have profession-focused guides that go deeper:',
        [
            '<a href="/chatgpt/legal/">ChatGPT for lawyers</a>: contract drafting, case research, and document summarization.',
            '<a href="/chatgpt/physicians/">ChatGPT for physicians</a>: clinical documentation and patient communication.',
            '<a href="/chatgpt/finance/">ChatGPT for finance professionals</a>: memos, analysis, and client prep.',
            '<a href="/chatgpt/real-estate/">ChatGPT for real estate agents</a>: listing copy and market research.',
        ]
    ),
    'claude': ul_block(
        'I also have profession-focused breakdowns for specific fields:',
        [
            '<a href="/claude/legal/">Claude for contract review</a>: long-document analysis and confidentiality considerations.',
            '<a href="/claude/physicians/">Claude for clinical documentation</a>: SOAP notes, discharge summaries, and referral letters.',
            '<a href="/claude/engineers/">Claude for software engineers</a>: code review, refactoring, and technical writing.',
            '<a href="/claude/finance/">Claude for financial analysis</a>: fund memos, regulatory filings, and long-document work.',
        ]
    ),
    'perplexity': ul_block(
        'If your work involves research in a specific field, I have focused guides for each:',
        [
            '<a href="/perplexity/legal/">Perplexity AI for legal research</a>: case law lookup and regulatory updates.',
            '<a href="/perplexity/physicians/">Perplexity AI for physicians</a>: clinical literature and drug information.',
            '<a href="/perplexity/finance/">Perplexity AI for financial research</a>: earnings, filings, and market data.',
            '<a href="/perplexity/insurance/">Perplexity AI for insurance professionals</a>: policy research and claims documentation.',
        ]
    ),
    'gemini': ul_block(
        'I have profession-focused guides for fields where Gemini has a clear fit:',
        [
            '<a href="/gemini/legal/">Google Gemini for legal professionals</a>: document review and research in the Google Workspace context.',
            '<a href="/gemini/real-estate/">Google Gemini for real estate agents</a>: market research and listing prep.',
            '<a href="/gemini/finance/">Google Gemini for finance</a>: financial modeling and data analysis with Sheets integration.',
            '<a href="/gemini/architects/">Google Gemini for architects</a>: specification writing and project documentation.',
        ]
    ),
    'copilot': ul_block(
        'I have profession-focused guides for roles where Copilot fits into existing Microsoft workflows:',
        [
            '<a href="/copilot/legal/">Microsoft Copilot for legal professionals</a>: contract review and Teams meeting summaries.',
            '<a href="/copilot/physicians/">Microsoft Copilot for physicians</a>: clinical notes and referral letters inside Microsoft 365.',
            '<a href="/copilot/engineers/">Microsoft Copilot for software engineers</a>: GitHub Copilot and the broader developer workflow.',
            '<a href="/copilot/finance/">Microsoft Copilot for financial advisors</a>: Excel analysis and client-facing document prep.',
        ]
    ),
    'midjourney': ul_block(
        'I have profession-focused guides for fields where Midjourney sees the most professional use:',
        [
            '<a href="/midjourney/architects/">Midjourney for architectural visualization</a>: concept rendering and client presentations.',
            '<a href="/midjourney/creatives/">Midjourney for creative professionals</a>: brand identity, editorial, and commercial image work.',
        ]
    ),
    'cursor': (
        '<p>If you are a developer evaluating Cursor, my '
        '<a href="/cursor/engineers/">Cursor for software engineers</a> guide digs into the code completion, '
        'chat, and refactoring features that matter most in real workflows.</p>'
    ),
    'notion-ai': ul_block(
        'I have profession-focused breakdowns for roles where Notion AI adds the most value:',
        [
            '<a href="/notion-ai/legal/">Notion AI for legal teams</a>: knowledge management, playbook building, and contract templates.',
            '<a href="/notion-ai/engineers/">Notion AI for software engineers</a>: documentation, sprint planning, and runbooks.',
            '<a href="/notion-ai/creatives/">Notion AI for content creators</a>: editorial calendars, content briefs, and draft generation.',
        ]
    ),
    'grammarly': ul_block(
        'I have profession-focused breakdowns for roles where client-facing writing quality matters most:',
        [
            '<a href="/grammarly/legal/">Grammarly for legal writing</a>: briefs, memos, and client communications.',
            '<a href="/grammarly/real-estate/">Grammarly for real estate agents</a>: listing descriptions and client emails.',
            '<a href="/grammarly/insurance/">Grammarly for insurance professionals</a>: claims correspondence and policy explanations.',
            '<a href="/grammarly/creatives/">Grammarly for creative writers</a>: where it helps and where it gets in the way.',
        ]
    ),
    'otter': (
        '<p>For a profession-specific view, my '
        '<a href="/otter/physicians/">Otter.ai for physicians</a> guide covers clinical documentation, '
        'SOAP note generation, and how it compares to dedicated medical transcription tools.</p>'
    ),
}

# ── Profession hub bullet blocks ───────────────────────────────────────────────

PROF_BULLETS = {
    'legal': ul_block(
        'For tool-specific guidance, I have deep-dive guides for each major AI tool used in legal work:',
        [
            '<a href="/chatgpt/legal/">ChatGPT for lawyers</a>: the most comprehensive starting point for drafting, research, and summarization.',
            '<a href="/claude/legal/">Claude for contract review</a>: long-document analysis and confidentiality considerations.',
            '<a href="/perplexity/legal/">Perplexity AI for legal research</a>: cited sources and regulatory updates.',
            '<a href="/copilot/legal/">Microsoft Copilot for legal professionals</a>: Teams, Outlook, and Word integration for firms on Microsoft 365.',
        ]
    ),
    'physicians': ul_block(
        'For tool-specific guidance, I have deep-dive guides for each major AI tool used in clinical settings:',
        [
            '<a href="/chatgpt/physicians/">ChatGPT for physicians</a>: clinical documentation and patient education use cases.',
            '<a href="/claude/physicians/">Claude for clinical documentation</a>: SOAP notes, discharge summaries, and referral letters.',
            '<a href="/perplexity/physicians/">Perplexity AI for medical research</a>: literature review and drug information lookup.',
            '<a href="/otter/physicians/">Otter.ai for medical documentation</a>: AI transcription and ambient note-taking for clinic settings.',
        ]
    ),
    'real-estate': ul_block(
        'For tool-specific guidance, I have deep-dive guides for each major AI tool used in real estate:',
        [
            '<a href="/chatgpt/real-estate/">ChatGPT for real estate agents</a>: listing copy, client emails, and market summaries.',
            '<a href="/claude/real-estate/">Claude for real estate professionals</a>: longer documents and negotiation prep.',
            '<a href="/gemini/real-estate/">Google Gemini for real estate research</a>: market data, comps, and Workspace integration.',
            '<a href="/grammarly/real-estate/">Grammarly for real estate writing</a>: listing descriptions and client communication polish.',
        ]
    ),
    'engineers': ul_block(
        'For tool-specific guidance, I have deep-dive guides for each major AI tool used in software development:',
        [
            '<a href="/chatgpt/engineers/">ChatGPT for software engineers</a>: how LLMs fit into development workflows.',
            '<a href="/claude/engineers/">Claude for code review</a>: long-context code analysis and refactoring.',
            '<a href="/cursor/engineers/">Cursor for software development</a>: the dedicated AI code editor guide worth reading before committing to any tool.',
            '<a href="/copilot/engineers/">Microsoft Copilot for engineers</a>: GitHub Copilot and the Microsoft 365 developer stack.',
        ]
    ),
    'finance': ul_block(
        'For tool-specific guidance, I have deep-dive guides for each major AI tool used in finance:',
        [
            '<a href="/chatgpt/finance/">ChatGPT for finance professionals</a>: memos, analysis, and client prep.',
            '<a href="/claude/finance/">Claude for financial analysis</a>: fund memos, regulatory filings, and long-document work.',
            '<a href="/perplexity/finance/">Perplexity AI for financial research</a>: earnings lookups, market data, and cited sourcing.',
            '<a href="/copilot/finance/">Microsoft Copilot for financial advisors</a>: Excel, Outlook, and Teams integration.',
        ]
    ),
    'insurance': ul_block(
        'For tool-specific guidance, I have deep-dive guides for each major AI tool used in insurance:',
        [
            '<a href="/chatgpt/insurance/">ChatGPT for insurance professionals</a>: claims documentation, client communication, and coverage explanations.',
            '<a href="/claude/insurance/">Claude for insurance workflows</a>: policy analysis and long-document review.',
            '<a href="/perplexity/insurance/">Perplexity AI for insurance research</a>: regulatory updates and policy research.',
            '<a href="/grammarly/insurance/">Grammarly for insurance writing</a>: client-facing correspondence and claims letters.',
        ]
    ),
    'architects': ul_block(
        'For tool-specific guidance, I have deep-dive guides for each major AI tool used in architecture:',
        [
            '<a href="/chatgpt/architects/">ChatGPT for architects</a>: specifications, project narratives, and client communications.',
            '<a href="/claude/architects/">Claude for architectural projects</a>: long documents and complex project briefs.',
            '<a href="/gemini/architects/">Google Gemini for architectural research</a>: material research, building codes, and Workspace integration.',
            '<a href="/midjourney/architects/">Midjourney for architectural visualization</a>: concept renders and client presentations.',
        ]
    ),
    'creatives': ul_block(
        'For tool-specific guidance, I have deep-dive guides for each major AI tool used in creative work:',
        [
            '<a href="/chatgpt/creatives/">ChatGPT for creative professionals</a>: content strategy and copywriting workflows.',
            '<a href="/claude/creatives/">Claude for content creation</a>: long-form drafting, brand voice, and editing.',
            '<a href="/midjourney/creatives/">Midjourney for creative work</a>: visual generation for brand, editorial, and commercial projects.',
            '<a href="/grammarly/creatives/">Grammarly for creative writing</a>: where AI style tools help and where they constrain your voice.',
        ]
    ),
}


# ── Process tool hub pages ─────────────────────────────────────────────────────

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
    new_block = TOOL_BULLETS.get(slug)
    if not new_block:
        print(f"  SKIP {slug}: no block defined")
        tool_skipped += 1
        continue

    raw_content = p.get('content', {}).get('raw', '')
    try:
        data = json.loads(raw_content)
    except json.JSONDecodeError as e:
        print(f"  ERROR {slug}: {e}")
        tool_errors += 1
        continue

    verdict = data.get('verdict_text', '')

    # Idempotency: already has bullet list for this tool
    if already_bulleted(verdict, f'/{slug}/'):
        print(f"  SKIP {slug}: already has bullet list")
        tool_skipped += 1
        continue

    # Strip any previously injected block
    clean = strip_injected(verdict)

    if clean:
        data['verdict_text'] = clean.rstrip() + '\n' + new_block
    else:
        wir = strip_injected(data.get('who_its_right_for', ''))
        if wir:
            data['who_its_right_for'] = wir.rstrip() + '\n' + new_block
        else:
            print(f"  SKIP {slug}: no suitable field")
            tool_skipped += 1
            continue

    try:
        result = api_put(f'/tool_review/{post_id}', {'content': json.dumps(data)})
        if 'id' in result:
            print(f"  OK  {slug} (post {post_id})")
            tool_updated += 1
        else:
            print(f"  FAIL {slug}: {result.get('message', str(result)[:100])}")
            tool_errors += 1
    except Exception as e:
        print(f"  ERROR {slug}: {e}")
        tool_errors += 1


# ── Process profession hub pages ───────────────────────────────────────────────

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
    new_block = PROF_BULLETS.get(slug)
    if not new_block:
        print(f"  SKIP {slug}: no block defined")
        prof_skipped += 1
        continue

    raw_content = p.get('content', {}).get('raw', '')
    try:
        data = json.loads(raw_content)
    except json.JSONDecodeError as e:
        print(f"  ERROR {slug}: {e}")
        prof_errors += 1
        continue

    uci = data.get('use_cases_intro', '')

    # Idempotency: already has bullet list
    if already_bulleted(uci, f'/{slug}/'):
        print(f"  SKIP {slug}: already has bullet list")
        prof_skipped += 1
        continue

    # Strip any previously injected block
    clean_uci = strip_injected(uci)

    # Wrap original plain text in <p> if not already
    if clean_uci and not clean_uci.strip().startswith('<p>'):
        clean_uci = f'<p>{clean_uci.strip()}</p>'

    if clean_uci:
        data['use_cases_intro'] = clean_uci.rstrip() + '\n' + new_block
    else:
        lede = strip_injected(data.get('lede', ''))
        if lede and not lede.strip().startswith('<p>'):
            lede = f'<p>{lede.strip()}</p>'
        if lede:
            data['lede'] = lede.rstrip() + '\n' + new_block
        else:
            print(f"  SKIP {slug}: no suitable field")
            prof_skipped += 1
            continue

    try:
        result = api_put(f'/profession_hub/{post_id}', {'content': json.dumps(data)})
        if 'id' in result:
            print(f"  OK  {slug} (post {post_id})")
            prof_updated += 1
        else:
            print(f"  FAIL {slug}: {result.get('message', str(result)[:100])}")
            prof_errors += 1
    except Exception as e:
        print(f"  ERROR {slug}: {e}")
        prof_errors += 1


print()
print("=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Tool hub pages:       {tool_updated} updated, {tool_skipped} skipped, {tool_errors} errors")
print(f"Profession hub pages: {prof_updated} updated, {prof_skipped} skipped, {prof_errors} errors")
print(f"Total updated:        {tool_updated + prof_updated}")
