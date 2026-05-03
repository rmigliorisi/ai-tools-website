#!/usr/bin/env python3
"""
Fix internal link paragraphs on all 18 hub pages.
  - Strip old comma-list paragraph (SENTINEL phrases from add_hub_links.py)
  - Re-add clean paragraphs: 1 link per sentence, 3-4 total links per hub
  - Profession hubs: wrap existing use_cases_intro in <p> so the new <div> template renders correctly

Idempotent: running twice is safe (new sentinel phrase won't be present the second time since
we check for the FIXED_SENTINEL before adding).
"""

import urllib.request, json, ssl, base64, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

CREDS = base64.b64encode(b'rmigliorisi:pj60 SqmD OSRD pSe1 9DsV BEeh').decode()
HEADERS = {'Authorization': f'Basic {CREDS}', 'Content-Type': 'application/json'}
BASE = 'https://aitoolsforpros.com/wp-json/wp/v2'

OLD_TOOL_SENTINEL  = 'profession-specific guide'  # old paragraph to strip
OLD_PROF_SENTINEL  = 'tool-specific guide'         # old paragraph to strip
FIXED_TOOL_SENTINEL = 'profession-focused guides'   # new sentinel (idempotency)
FIXED_PROF_SENTINEL = 'tool-specific guidance'      # new sentinel (idempotency)


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


def strip_old_paragraph(text, sentinel):
    """Remove the old injected paragraph that starts with or contains `sentinel`."""
    if not text or sentinel not in text:
        return text
    # Strip from the last `\n<p>` that contains the sentinel to end
    idx = text.rfind('\n<p>')
    while idx != -1:
        candidate = text[idx:]
        if sentinel in candidate:
            return text[:idx].rstrip()
        idx = text.rfind('\n<p>', 0, idx)
    return text


# ── New clean paragraphs: 1 link per sentence ─────────────────────────────────

TOOL_PARAGRAPHS = {
    'chatgpt': (
        '<p>If your work is specialized, I have profession-focused guides that go deeper. '
        '<a href="/chatgpt/legal/">ChatGPT for lawyers</a> covers contract drafting, case research, and document summarization. '
        '<a href="/chatgpt/physicians/">ChatGPT for physicians</a> digs into clinical documentation and patient communication. '
        '<a href="/chatgpt/finance/">ChatGPT for finance professionals</a> covers memos, analysis, and client prep. '
        '<a href="/chatgpt/real-estate/">ChatGPT for real estate agents</a> covers listing copy and market research.</p>'
    ),
    'claude': (
        '<p>I also have profession-focused breakdowns for specific fields. '
        '<a href="/claude/legal/">Claude for contract review</a> is where Claude stands out most for legal professionals. '
        '<a href="/claude/physicians/">Claude for clinical documentation</a> covers how it compares to dedicated medical dictation tools. '
        '<a href="/claude/engineers/">Claude for software engineers</a> looks at code review, refactoring, and technical writing. '
        '<a href="/claude/finance/">Claude for financial analysis</a> covers long-document work like fund memos and regulatory filings.</p>'
    ),
    'perplexity': (
        '<p>If your work involves research in a specific field, I have focused guides for each. '
        '<a href="/perplexity/legal/">Perplexity AI for legal research</a> covers case law lookup and regulatory updates. '
        '<a href="/perplexity/physicians/">Perplexity AI for physicians</a> focuses on clinical literature and drug information. '
        '<a href="/perplexity/finance/">Perplexity AI for financial research</a> covers earnings, filings, and market data. '
        '<a href="/perplexity/insurance/">Perplexity AI for insurance professionals</a> covers policy research and claims documentation.</p>'
    ),
    'gemini': (
        '<p>I have profession-focused guides for fields where Gemini has a clear fit. '
        '<a href="/gemini/legal/">Google Gemini for legal professionals</a> covers document review and research in the Google Workspace context. '
        '<a href="/gemini/real-estate/">Google Gemini for real estate agents</a> focuses on market research and listing prep. '
        '<a href="/gemini/finance/">Google Gemini for finance</a> covers financial modeling and data analysis with Sheets integration. '
        '<a href="/gemini/architects/">Google Gemini for architects</a> looks at specification writing and project documentation.</p>'
    ),
    'copilot': (
        '<p>I have profession-focused guides for roles where Copilot fits into existing Microsoft workflows. '
        '<a href="/copilot/legal/">Microsoft Copilot for legal professionals</a> covers contract review and Teams meeting summaries. '
        '<a href="/copilot/physicians/">Microsoft Copilot for physicians</a> focuses on clinical notes and referral letters inside Microsoft 365. '
        '<a href="/copilot/engineers/">Microsoft Copilot for software engineers</a> covers GitHub Copilot and the broader developer workflow. '
        '<a href="/copilot/finance/">Microsoft Copilot for financial advisors</a> covers Excel analysis and client-facing document prep.</p>'
    ),
    'midjourney': (
        '<p>I have two profession-focused guides for fields where Midjourney sees the most professional use. '
        '<a href="/midjourney/architects/">Midjourney for architectural visualization</a> covers concept rendering and client presentations. '
        '<a href="/midjourney/creatives/">Midjourney for creative professionals</a> covers brand identity, editorial, and commercial image work.</p>'
    ),
    'cursor': (
        '<p>If you are a developer evaluating Cursor, my <a href="/cursor/engineers/">Cursor for software engineers</a> guide digs into the code completion, chat, and refactoring features that matter most in real workflows.</p>'
    ),
    'notion-ai': (
        '<p>I have profession-focused breakdowns for roles where Notion AI adds the most value. '
        '<a href="/notion-ai/legal/">Notion AI for legal teams</a> covers knowledge management, playbook building, and contract templates. '
        '<a href="/notion-ai/engineers/">Notion AI for software engineers</a> looks at documentation, sprint planning, and runbooks. '
        '<a href="/notion-ai/creatives/">Notion AI for content creators</a> covers editorial calendars, content briefs, and draft generation.</p>'
    ),
    'grammarly': (
        '<p>I have profession-focused breakdowns for roles where client-facing writing quality matters most. '
        '<a href="/grammarly/legal/">Grammarly for legal writing</a> covers briefs, memos, and client communications. '
        '<a href="/grammarly/real-estate/">Grammarly for real estate agents</a> focuses on listing descriptions and client emails. '
        '<a href="/grammarly/insurance/">Grammarly for insurance professionals</a> covers claims correspondence and policy explanations. '
        '<a href="/grammarly/creatives/">Grammarly for creative writers</a> looks at where it helps and where it gets in the way.</p>'
    ),
    'otter': (
        '<p>For a profession-specific view, my <a href="/otter/physicians/">Otter.ai for physicians</a> guide covers clinical documentation, SOAP note generation, and how it compares to dedicated medical transcription tools.</p>'
    ),
}

PROF_PARAGRAPHS = {
    'legal': (
        '<p>For tool-specific guidance, my <a href="/chatgpt/legal/">ChatGPT for lawyers</a> guide is the most comprehensive starting point. '
        '<a href="/claude/legal/">Claude for contract review</a> covers long-document analysis and confidentiality considerations. '
        '<a href="/perplexity/legal/">Perplexity AI for legal research</a> is worth reading if cited sources matter to your workflow. '
        '<a href="/copilot/legal/">Microsoft Copilot for legal professionals</a> covers Teams, Outlook, and Word integration for firms already on Microsoft 365.</p>'
    ),
    'physicians': (
        '<p>For tool-specific guidance, start with <a href="/chatgpt/physicians/">ChatGPT for physicians</a> for a broad overview of clinical documentation and patient education use cases. '
        '<a href="/claude/physicians/">Claude for clinical documentation</a> digs into SOAP notes, discharge summaries, and referral letters. '
        '<a href="/perplexity/physicians/">Perplexity AI for medical research</a> is useful for literature review and drug information lookup. '
        '<a href="/otter/physicians/">Otter.ai for medical documentation</a> covers AI transcription and ambient note-taking for clinic settings.</p>'
    ),
    'real-estate': (
        '<p>For tool-specific guidance, my <a href="/chatgpt/real-estate/">ChatGPT for real estate agents</a> guide covers listing copy, client emails, and market summaries. '
        '<a href="/claude/real-estate/">Claude for real estate professionals</a> is worth reading if you handle longer documents and negotiations. '
        '<a href="/gemini/real-estate/">Google Gemini for real estate research</a> covers market data, comps, and Workspace integration. '
        '<a href="/grammarly/real-estate/">Grammarly for real estate writing</a> focuses on listing descriptions and client communication polish.</p>'
    ),
    'engineers': (
        '<p>For tool-specific guidance, start with <a href="/chatgpt/engineers/">ChatGPT for software engineers</a> for a broad overview of how LLMs fit into development workflows. '
        '<a href="/claude/engineers/">Claude for code review</a> covers long-context code analysis and refactoring. '
        '<a href="/cursor/engineers/">Cursor for software development</a> is the dedicated AI code editor guide worth reading before committing to any tool. '
        '<a href="/copilot/engineers/">Microsoft Copilot for engineers</a> covers GitHub Copilot and the Microsoft 365 developer stack.</p>'
    ),
    'finance': (
        '<p>For tool-specific guidance, my <a href="/chatgpt/finance/">ChatGPT for finance professionals</a> guide covers memos, analysis, and client prep. '
        '<a href="/claude/finance/">Claude for financial analysis</a> focuses on long-document work like fund memos and regulatory filings. '
        '<a href="/perplexity/finance/">Perplexity AI for financial research</a> covers earnings lookups, market data, and cited sourcing. '
        '<a href="/copilot/finance/">Microsoft Copilot for financial advisors</a> covers Excel, Outlook, and Teams integration for firms already on Microsoft 365.</p>'
    ),
    'insurance': (
        '<p>For tool-specific guidance, my <a href="/chatgpt/insurance/">ChatGPT for insurance professionals</a> guide covers claims documentation, client communication, and coverage explanations. '
        '<a href="/claude/insurance/">Claude for insurance workflows</a> covers policy analysis and long-document review. '
        '<a href="/perplexity/insurance/">Perplexity AI for insurance research</a> is worth reading for regulatory updates and policy research. '
        '<a href="/grammarly/insurance/">Grammarly for insurance writing</a> focuses on client-facing correspondence and claims letters.</p>'
    ),
    'architects': (
        '<p>For tool-specific guidance, my <a href="/chatgpt/architects/">ChatGPT for architects</a> guide covers specifications, project narratives, and client communications. '
        '<a href="/claude/architects/">Claude for architectural projects</a> is the better option for long documents and complex project briefs. '
        '<a href="/gemini/architects/">Google Gemini for architectural research</a> covers material research, building codes, and Workspace integration. '
        '<a href="/midjourney/architects/">Midjourney for architectural visualization</a> covers AI-generated concept renders and client presentations.</p>'
    ),
    'creatives': (
        '<p>For tool-specific guidance, my <a href="/chatgpt/creatives/">ChatGPT for creative professionals</a> guide is the broad starting point for content strategy and copywriting workflows. '
        '<a href="/claude/creatives/">Claude for content creation</a> covers long-form drafting, brand voice, and editing. '
        '<a href="/midjourney/creatives/">Midjourney for creative work</a> is the guide to read if visual generation is part of your toolkit. '
        '<a href="/grammarly/creatives/">Grammarly for creative writing</a> covers where AI style tools help and where they constrain your voice.</p>'
    ),
}


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
    new_para = TOOL_PARAGRAPHS.get(slug)
    if not new_para:
        print(f"  SKIP {slug}: no paragraph defined")
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

    # Already fixed
    if FIXED_TOOL_SENTINEL in verdict:
        print(f"  SKIP {slug}: already has clean links")
        tool_skipped += 1
        continue

    # Strip old comma-list paragraph
    clean_verdict = strip_old_paragraph(verdict, OLD_TOOL_SENTINEL)

    # Append new clean paragraph
    if clean_verdict:
        data['verdict_text'] = clean_verdict.rstrip() + '\n' + new_para
    else:
        # Fall back to who_its_right_for
        wir = data.get('who_its_right_for', '')
        clean_wir = strip_old_paragraph(wir, OLD_TOOL_SENTINEL)
        if clean_wir:
            data['who_its_right_for'] = clean_wir.rstrip() + '\n' + new_para
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
    new_para = PROF_PARAGRAPHS.get(slug)
    if not new_para:
        print(f"  SKIP {slug}: no paragraph defined")
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

    # Already fixed
    if FIXED_PROF_SENTINEL in uci:
        print(f"  SKIP {slug}: already has clean links")
        prof_skipped += 1
        continue

    # Strip old bad paragraph
    clean_uci = strip_old_paragraph(uci, OLD_PROF_SENTINEL)

    # Wrap original text in <p> so the new <div> template renders it as a paragraph
    # If it already has <p> tags, don't double-wrap
    if clean_uci and not clean_uci.strip().startswith('<p>'):
        clean_uci = f'<p>{clean_uci.strip()}</p>'

    # Append new clean paragraph
    if clean_uci:
        data['use_cases_intro'] = clean_uci.rstrip() + '\n' + new_para
    else:
        # Fall back to lede
        lede = data.get('lede', '')
        clean_lede = strip_old_paragraph(lede, OLD_PROF_SENTINEL)
        if clean_lede and not clean_lede.strip().startswith('<p>'):
            clean_lede = f'<p>{clean_lede.strip()}</p>'
        if clean_lede:
            data['lede'] = clean_lede.rstrip() + '\n' + new_para
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
