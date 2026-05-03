#!/usr/bin/env python3
"""Push ChatGPT-generated missing content to 9 cross-reference pages."""

import urllib.request, json, ssl
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


# ── Content from ChatGPT ──────────────────────────────────────────────────

CONTENT = {
    'chatgpt-physicians': {
        'mini_workflow': (
            "Set up ChatGPT custom instructions for your specialty, reading level preferences, and preferred patient education tone. "
            "Then use GPT-4o to turn a redacted diagnosis, treatment plan, and follow-up timeline into a patient-friendly handout at a sixth-grade reading level. "
            "Keep every input de-identified unless your organization has approved a HIPAA-compliant workspace with a BAA."
        ),
        'reviews_miss': {
            'insights': [
                {
                    'insight_title': "Patient Education Needs More Than Plain English",
                    'insight_body': (
                        "The useful output is not just simpler wording. Physicians get better results when they ask ChatGPT to separate what the patient should do today, "
                        "what symptoms require a call, and what symptoms require urgent care."
                    ),
                },
                {
                    'insight_title': "Prior Authorization Drafts Still Need Clinical Judgment",
                    'insight_body': (
                        "ChatGPT can turn chart-neutral details into a cleaner prior authorization letter, but it cannot decide medical necessity. "
                        "The physician still needs to verify diagnosis codes, failed therapies, contraindications, and payer-specific requirements."
                    ),
                },
                {
                    'insight_title': "Templates Beat One-Off Prompts in Daily Practice",
                    'insight_body': (
                        "The biggest time savings come from reusable prompt patterns for common tasks like referral letters, after-visit summaries, and medication explanations. "
                        "Physicians who rebuild the prompt every time lose much of the administrative benefit."
                    ),
                },
            ],
            'insight_banner': "ChatGPT helps most when physicians standardize the administrative work around care.",
        },
    },

    'copilot-legal': {
        'mini_workflow': (
            "Open the relevant email thread in Outlook and the draft agreement in Word, then ask Copilot to summarize the open issues, "
            "identify the other side's requested changes, and draft a response email with three negotiation options. "
            "Review the summary against the actual thread before sending anything. "
            "This is where Copilot earns its place because the context is already inside Microsoft 365."
        ),
        'reviews_miss': {
            'insights': [
                {
                    'insight_title': "Copilot Is Better at Context Than Drafting",
                    'insight_body': (
                        "Copilot's strongest legal use case is not writing a perfect clause from scratch. "
                        "It is reading the email, document, and meeting context already sitting in Microsoft 365 and helping the lawyer move the matter forward faster."
                    ),
                },
                {
                    'insight_title': "Permissions Matter More Than Most Reviews Admit",
                    'insight_body': (
                        "Copilot can only work with content the user has permission to access, which makes firm information architecture a real issue. "
                        "If SharePoint, Teams, or matter folders are messy, Copilot may surface incomplete context or miss key documents."
                    ),
                },
                {
                    'insight_title': "Word Integration Helps, But Legal Style Still Wins",
                    'insight_body': (
                        "Copilot can revise tone, summarize comments, and draft first-pass language inside Word. "
                        "Lawyers still need to control defined terms, negotiation posture, privilege language, and jurisdiction-specific phrasing before anything leaves the firm."
                    ),
                },
            ],
            'insight_banner': "Copilot's legal advantage is context, not raw drafting power.",
        },
    },

    'cursor-engineers': {
        'mini_workflow': (
            "Use Composer on a contained refactor, not an open-ended rebuild. "
            "Select the relevant files, explain the intended behavior, ask Cursor to propose the multi-file changes first, and review the diff before applying. "
            "Save Agent Mode for tasks with clear tests, because vague goals can lead it into unnecessary edits."
        ),
        'reviews_miss': {
            'insights': [
                {
                    'insight_title': "Agent Mode Needs Guardrails Before Freedom",
                    'insight_body': (
                        "Agent Mode works best when the task has clear boundaries, failing tests, or a narrow acceptance condition. "
                        "When the goal is vague, it can edit too many files, introduce style drift, or solve a different problem than the one you intended."
                    ),
                },
                {
                    'insight_title': ".cursorrules Is Not Optional for Teams",
                    'insight_body': (
                        "Teams that skip .cursorrules get inconsistent output across frameworks, naming conventions, and testing patterns. "
                        "A short rules file that explains architecture, preferred libraries, and forbidden changes often saves more time than another model upgrade."
                    ),
                },
                {
                    'insight_title': "Model Selection Changes the Workflow",
                    'insight_body': (
                        "Fast models are better for autocomplete and small edits, while stronger models are better for architectural reasoning and complex debugging. "
                        "Daily Cursor users learn to switch models by task instead of assuming one model should handle everything."
                    ),
                },
            ],
            'insight_banner': "Cursor gets powerful only after engineers stop treating it like autocomplete.",
        },
    },

    'gemini-legal': {
        'bottom_line': (
            "Gemini is useful for legal intake triage, email thread compression, and turning messy notes into a cleaner issue list. "
            "I would not use it for legal reasoning, jurisdiction-specific conclusions, or any work that depends on primary authority. "
            "Treat Gemini as an organizer for redacted inputs, not as a legal analysis engine."
        ),
    },

    'gemini-real-estate': {
        'sources': [
            {'source_name': 'Google AI for Developers — Grounding with Google Search documentation for Gemini responses and real-time source grounding'},
            {'source_name': 'Google Cloud Vertex AI — Grounding Gemini with Google Search using publicly available web data'},
            {'source_name': 'Google Workspace — Gemini for Workspace feature documentation for Gmail, Docs, Drive, and productivity workflows'},
            {'source_name': 'National Association of Realtors — 2025 REALTORS® Technology Survey covering AI tool adoption among real estate professionals'},
            {'source_name': 'National Association of Realtors — Artificial Intelligence in Real Estate resource hub covering AI use, policy templates, and responsible adoption'},
        ],
    },

    'grammarly-legal': {
        'mini_workflow': (
            "Install Grammarly where you already write, especially Outlook, Word, Gmail, and Chrome. "
            "Draft the client email, demand letter cover note, or settlement summary in your normal workflow, "
            "then use Grammarly only for clarity, tone, and typo review before final attorney review. "
            "Do not let it rewrite legal substance or change defined legal terms without checking every edit."
        ),
        'reviews_miss': {
            'insights': [
                {
                    'insight_title': "Legal Tone Is Not Always Softer",
                    'insight_body': (
                        "Grammarly often nudges writing toward warmth and simplicity, which helps client emails but can weaken firm legal positioning. "
                        "Lawyers should treat tone suggestions as optional, especially in demand letters, preservation notices, or adversarial correspondence."
                    ),
                },
                {
                    'insight_title': "Citation Cleanup Is Still a Lawyer Task",
                    'insight_body': (
                        "Grammarly may catch punctuation and consistency issues around citations, but it does not understand Bluebook strategy or jurisdictional citation norms. "
                        "It can polish around legal citations, but it should not be trusted to validate them."
                    ),
                },
                {
                    'insight_title': "Firm-Wide Use Needs Admin Controls",
                    'insight_body': (
                        "The free tier may be fine for casual proofreading, but law firms need policy, account controls, and consistency across users. "
                        "Grammarly Business is more realistic for firm workflows because individual browser extensions create uneven data and style practices."
                    ),
                },
            ],
            'insight_banner': "Grammarly helps lawyers polish writing, but it should never control legal substance.",
        },
    },

    'grammarly-real-estate': {
        'mini_workflow': (
            "Turn Grammarly on for Gmail, your browser, and your phone keyboard, then use it as a final pass on buyer updates, "
            "seller check-ins, MLS remarks, and offer cover emails. "
            "Accept grammar and clarity fixes, but review any wording that touches neighborhood demographics, protected classes, schools, or buyer suitability. "
            "Grammarly can polish the message, but it is not a Fair Housing reviewer."
        ),
        'reviews_miss': {
            'insights': [
                {
                    'insight_title': "MLS Character Limits Change the Editing Job",
                    'insight_body': (
                        "Grammarly may suggest cleaner phrasing that is longer than the MLS field allows. "
                        "Agents should use it to catch mistakes first, then manually tighten the copy so abbreviations and required property details still fit."
                    ),
                },
                {
                    'insight_title': "Tone Should Change by Client Situation",
                    'insight_body': (
                        "A buyer losing out on offers needs a different tone than a seller reviewing a price reduction. "
                        "Grammarly can help soften or clarify the message, but the agent has to choose the relationship context before accepting suggestions."
                    ),
                },
                {
                    'insight_title': "Fair Housing Language Still Requires Human Review",
                    'insight_body': (
                        "Grammarly can improve grammar, but it does not reliably identify Fair Housing risk. "
                        "Agents should manually review language around people, neighborhoods, schools, safety, religion, family status, disability, and buyer fit."
                    ),
                },
            ],
            'insight_banner': "Grammarly is useful for polish, not compliance judgment.",
        },
    },

    'notion-ai-legal': {
        'bottom_line': (
            "Notion AI is useful for legal teams that already use Notion as a knowledge base, intake system, or internal playbook hub. "
            "It is a niche organization tool, not a replacement for ChatGPT, Claude, Westlaw, or attorney review. "
            "I would use it to structure sanitized notes and repeatable workflows, not to produce final legal advice."
        ),
    },

    'perplexity-legal': {
        'reviews_miss': {
            'insights': [
                {
                    'insight_title': "Citations Are Starting Points, Not Authority",
                    'insight_body': (
                        "Perplexity makes legal research feel cleaner because every answer comes with sources, but the citation is not the same as legal validation. "
                        "Lawyers still need to open the primary source, confirm jurisdiction, check procedural posture, and verify that the cited material says what the answer claims."
                    ),
                },
                {
                    'insight_title': "Secondary Sources Can Quietly Shape the Answer",
                    'insight_body': (
                        "Perplexity may blend law firm alerts, agency pages, news articles, and primary sources into one confident summary. "
                        "That is useful for orientation, but lawyers should separate primary authority from commentary before relying on the result."
                    ),
                },
                {
                    'insight_title': "Pro Search Helps With Narrow Legal Questions",
                    'insight_body': (
                        "Perplexity Pro is more useful when the query includes jurisdiction, date range, agency, and issue framing. "
                        "It can outperform a standard Google search for recent regulatory developments, but it still does not replace Westlaw, Lexis, or a citator."
                    ),
                },
            ],
            'insight_banner': "Perplexity speeds up legal orientation, but verification still decides whether it is usable.",
        },
    },
}


def main():
    posts = api_get('/cross_reference?per_page=100&context=edit&_fields=id,slug,content')
    post_map = {p['slug']: p for p in posts}

    for slug, updates in CONTENT.items():
        p = post_map.get(slug)
        if not p:
            print(f"  NOT FOUND: {slug}")
            continue

        data = json.loads(p['content']['raw'])
        blocks = data.setdefault('consistency_blocks', {})

        for field, value in updates.items():
            if field == 'mini_workflow':
                blocks['mini_workflow'] = value
            elif field == 'bottom_line':
                blocks['bottom_line'] = value
            elif field == 'reviews_miss':
                data['reviews_miss'] = value
            elif field == 'sources':
                data['sources'] = value

        api_put(f'/cross_reference/{p["id"]}', {'content': json.dumps(data)})
        print(f"  UPDATED: {slug} ({', '.join(updates.keys())})")


if __name__ == '__main__':
    main()
    print("\nDone.")
