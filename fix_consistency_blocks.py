#!/usr/bin/env python3
"""
Fix consistency_blocks (key_takeaway, best_for, avoid_if) that are either:
 - severely corrupted (concatenated multiple fields / includes nav links)
 - all three fields set to the same value (migration bug)
 - individual fields too long or too short
Target length: key_takeaway ~250-300 chars, best_for ~160-210 chars, avoid_if ~180-240 chars
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


# All values derived from original static HTML + target ~chatgpt/architects/ length
FIXES = {
    # SEVERELY CORRUPTED (concatenated multiple fields / nav links)
    'gemini-legal': {
        'key_takeaway': (
            "Strong at email thread compression and issue lists. Useful for first-pass clause "
            "structure and checklists, but risky with citations unless you verify every reference "
            "against primary sources."
        ),
        'best_for': (
            "Legal professionals who need to turn messy email threads, deposition transcripts, "
            "and meeting notes into structured issue lists, checklists, and first-pass drafts "
            "for attorney review."
        ),
        'avoid_if': (
            "Unverified legal conclusions or jurisdiction-specific calls; copying privileged facts "
            "into a consumer workspace; submitting citations without checking primary sources; "
            "anything that replaces attorney judgment."
        ),
    },

    'perplexity-legal': {
        'key_takeaway': (
            "Real-time web access gives you current case law and regulatory news with cited sources "
            "attached. Always click through citations before using in work product; summaries can "
            "misrepresent what the source actually says."
        ),
        'best_for': (
            "Lawyers who need preliminary case law research with citations, regulatory lookups, or "
            "monitoring recent circuit opinions before opening Westlaw or Lexis for a full "
            "research pass."
        ),
        'avoid_if': (
            "Entering any confidential client information; drafting contracts, briefs, or legal "
            "memos; citing cases in work product without independent verification through "
            "Westlaw or Lexis."
        ),
    },

    'notion-ai-legal': {
        'key_takeaway': (
            "Best for organizing existing legal knowledge inside Notion: summarizing intake notes, "
            "structuring playbooks, and turning meeting notes into action items. Only useful if "
            "Notion is already your team's primary workflow tool."
        ),
        'best_for': (
            "Legal teams already using Notion as their primary knowledge base for matter intake, "
            "contract playbooks, clause libraries, and internal policy documentation."
        ),
        'avoid_if': (
            "Final legal advice without primary authority review; entering privileged facts in "
            "non-approved workspaces; generating citations you cannot independently verify; "
            "any output going to clients without attorney review."
        ),
    },

    # SAME-VALUE CORRUPTION (all three fields were set to key_takeaway text)
    'claude-legal': {
        # key_takeaway is correct as-is (277 chars)
        'best_for': (
            "Lawyers who need long-document analysis, contract drafting, and clause-level review. "
            "Claude holds full contracts in context and reasons across hundreds of pages without "
            "losing track of defined terms."
        ),
        'avoid_if': (
            "Real-time case law lookups (Claude has a training cutoff); entering privileged facts "
            "without checking your firm's AI policy; citing cases without independent "
            "Westlaw verification."
        ),
    },

    'chatgpt-legal': {
        # key_takeaway is correct as-is (305 chars)
        'best_for': (
            "Lawyers who need first-draft writing, contract clause generation, prior authorization "
            "templates, client communication drafts, and document summarization without needing "
            "real-time case law."
        ),
        'avoid_if': (
            "Citing cases in filed documents without Westlaw verification; entering "
            "client-identifiable information without a BAA; expecting substantive legal research "
            "or real-time regulatory data."
        ),
    },

    # MODERATELY TOO LONG — trim to match chatgpt/architects reference
    'chatgpt-physicians': {
        'key_takeaway': (
            "Physicians spend 2 to 3 hours per day on documentation and administrative tasks. "
            "ChatGPT does not reduce clinical time but materially reduces administrative time "
            "for referral letters, prior auth templates, and patient education drafts."
        ),
        'best_for': (
            "Physicians who need to reduce administrative burden outside direct patient care: "
            "referral letters, prior authorization templates, patient education materials, "
            "and after-visit communication drafts."
        ),
        # avoid_if (242 chars) is fine — leave it
    },

    'cursor-engineers': {
        'key_takeaway': (
            "Most engineers underutilize Cursor by treating it as fancier autocomplete. "
            "The productivity jump comes from Composer for multi-file edits and Agent Mode "
            "for autonomous task execution."
        ),
        'best_for': (
            "Software engineers who write code daily and want AI-native multi-file editing "
            "with Composer and Agent Mode, not just single-line autocomplete suggestions."
        ),
        # avoid_if (234 chars) is fine — leave it
    },

    'copilot-legal': {
        'key_takeaway': (
            "Copilot's core advantage is workflow integration, not AI capability. ChatGPT and "
            "Claude write better, but Copilot reads your email thread and knows what you are "
            "actually working on inside Microsoft 365."
        ),
        'best_for': (
            "Lawyers already working in Microsoft 365 Business or Enterprise who want AI that "
            "reads their email and document context without switching to a separate tool."
        ),
        # avoid_if (223 chars) is fine — leave it
    },

    'grammarly-real-estate': {
        'key_takeaway': (
            "Real estate agents write dozens of short communications daily: emails, MLS remarks, "
            "offer cover letters, and social captions. Grammarly catches errors passively "
            "without a prompt or app switch."
        ),
        'best_for': (
            "Agents who send high volumes of client emails, MLS listing remarks, offer cover "
            "letters, and social content and want passive quality improvement with zero "
            "workflow change."
        ),
        # avoid_if (204 chars) is fine — leave it
    },
}


def main():
    posts = api_get('/cross_reference?per_page=100&context=edit&_fields=id,slug,content')
    post_map = {p['slug']: p for p in posts}

    for slug, field_fixes in FIXES.items():
        p = post_map.get(slug)
        if not p:
            print(f"  NOT FOUND: {slug}")
            continue

        data = json.loads(p['content']['raw'])
        blocks = data.setdefault('consistency_blocks', {})

        for field, value in field_fixes.items():
            blocks[field] = value

        api_put(f'/cross_reference/{p["id"]}', {'content': json.dumps(data)})
        print(f"  FIXED: {slug} ({', '.join(field_fixes.keys())})")

    print("\nDone.")


if __name__ == '__main__':
    main()
