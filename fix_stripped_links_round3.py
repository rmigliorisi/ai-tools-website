"""
Round 3 — fixes all remaining stripped-link instances found by the full
mechanical scan (scan_stripped_links.py) across all 66 pages, confirmed
with wide, unambiguous context via dump_full_context.py.

This covers 17 pages the original 7-page visual audit never flagged at
all. Excludes confirmed false positives from the scan: "OtterPilot" and
"GrammarlyGO" are real product names (not broken links), and "Claude/
ChatGPT" slash notation is intentional shorthand, not squished text.

Same safety pattern as rounds 1 and 2: each replacement only applies if
the exact old text is found exactly once in the page's decoded text
fields; otherwise it's skipped and reported rather than guessed.

Run:
    python3 fix_stripped_links_round3.py
"""

import json

import requests
from wp_creds import AUTH, WP_URL

STYLE = "color:#2563eb;text-decoration:none;font-weight:500;"


def link(href, text):
    return f'<a href="{href}" style="{STYLE}">{text}</a>'


FIXES = [
    {
        "post_id": 398,
        "slug": "grammarly-real-estate",
        "replacements": [
            (
                "For content generation from scratch, use ChatGPT orClaude. Grammarly improves what you have already written; it cannot produce it.",
                f'For content generation from scratch, use ChatGPT or {link("/claude/", "Claude")}. Grammarly improves what you have already written; it cannot produce it.',
            ),
        ],
    },
    {
        "post_id": 395,
        "slug": "notion-ai-engineers",
        "replacements": [
            (
                "Notion AI cannot run code, access your IDE, understand your repository structure, or provide the kind of code-aware assistance thatCursoror GitHubCopilotprovide. It can generate code snippets in a Notion page, but this is a marginal use case compared to purpose-built coding tools.",
                f'Notion AI cannot run code, access your IDE, understand your repository structure, or provide the kind of code-aware assistance that {link("/cursor/", "Cursor")} or GitHub {link("/copilot/", "Copilot")} provide. It can generate code snippets in a Notion page, but this is a marginal use case compared to purpose-built coding tools.',
            ),
        ],
    },
    {
        "post_id": 393,
        "slug": "cursor-engineers",
        "replacements": [
            (
                "For engineers who also need general AI assistance for communication, documentation strategy, or non-technical tasks, supplement Cursor withChatGPTorClaude.",
                f'For engineers who also need general AI assistance for communication, documentation strategy, or non-technical tasks, supplement Cursor with {link("/chatgpt/", "ChatGPT")} or {link("/claude/", "Claude")}.',
            ),
        ],
    },
    {
        "post_id": 390,
        "slug": "copilot-insurance",
        "replacements": [
            (
                "Like Claude andChatGPT, Copilot has no live market or regulatory information. For current state regulatory guidance, carrier appetite changes, or recent market news, usePerplexity AIto find current primary source information.",
                f'Like Claude and {link("/chatgpt/", "ChatGPT")}, Copilot has no live market or regulatory information. For current state regulatory guidance, carrier appetite changes, or recent market news, use {link("/perplexity/", "Perplexity AI")} to find current primary source information.',
            ),
            (
                "For detailed commercial policy review, coverage gap identification, and comparing expiring to renewal across complex programs,Claudeis significantly more capable. Copilot handles the M365 writing and productivity work",
                f'For detailed commercial policy review, coverage gap identification, and comparing expiring to renewal across complex programs, {link("/claude/", "Claude")} is significantly more capable. Copilot handles the M365 writing and productivity work',
            ),
        ],
    },
    {
        "post_id": 389,
        "slug": "copilot-finance",
        "replacements": [
            (
                "Like Claude andChatGPT, Copilot does not have live market data or current regulatory information. For current rates and recent regulatory guidance, usePerplexity AI. Copilot handles the writing and analysis work;Perplexityhandles the current-information layer.",
                f'Like Claude and {link("/chatgpt/", "ChatGPT")}, Copilot does not have live market data or current regulatory information. For current rates and recent regulatory guidance, use {link("/perplexity/", "Perplexity AI")}. Copilot handles the writing and analysis work; {link("/perplexity/", "Perplexity")} handles the current-information layer.',
            ),
            (
                "For reviewing a full prospectus, synthesizing multiple documents, or complex financial plan analysis,Claudesignificantly outperforms Copilot.",
                f'For reviewing a full prospectus, synthesizing multiple documents, or complex financial plan analysis, {link("/claude/", "Claude")} significantly outperforms Copilot.',
            ),
        ],
    },
    {
        "post_id": 388,
        "slug": "copilot-engineers",
        "replacements": [
            (
                "For those teams, standalone tools like Claude,ChatGPT, orNotion AIare more appropriate and do not require switching ecosystems.",
                f'For those teams, standalone tools like Claude, {link("/chatgpt/", "ChatGPT")}, or {link("/notion-ai/", "Notion AI")} are more appropriate and do not require switching ecosystems.',
            ),
            (
                "It can help you draft simple code snippets in a Word document or Teams message, but it is not a substitute for GitHub Copilot,Cursor, orClaudefor actual engineering work.",
                f'It can help you draft simple code snippets in a Word document or Teams message, but it is not a substitute for GitHub Copilot, {link("/cursor/", "Cursor")}, or {link("/claude/", "Claude")} for actual engineering work.',
            ),
            (
                "For complex RFC drafting, architecture decision records, or reasoning over large codebases,Claudeis significantly stronger.",
                f'For complex RFC drafting, architecture decision records, or reasoning over large codebases, {link("/claude/", "Claude")} is significantly stronger.',
            ),
        ],
    },
    {
        "post_id": 387,
        "slug": "copilot-real-estate",
        "replacements": [
            (
                "For live market lookups, use your MLS directly or usePerplexity AIfor web-based research.",
                f'For live market lookups, use your MLS directly or use {link("/perplexity/", "Perplexity AI")} for web-based research.',
            ),
        ],
    },
    {
        "post_id": 386,
        "slug": "copilot-physicians",
        "replacements": [
            (
                "It can retrieve general information but lacks the citation rigor needed for clinical evidence review. UsePerplexity AIfor literature research tasks.",
                f'It can retrieve general information but lacks the citation rigor needed for clinical evidence review. Use {link("/perplexity/", "Perplexity AI")} for literature research tasks.',
            ),
            (
                "It is not the right tool for reading and synthesizing a 60-page medical record in a single session. Use Claude orChatGPTfor that task.",
                f'It is not the right tool for reading and synthesizing a 60-page medical record in a single session. Use Claude or {link("/chatgpt/", "ChatGPT")} for that task.',
            ),
            (
                "Copilot cannot matchClaude's 200K context window for full patient record analysis.",
                f'Copilot cannot match {link("/claude/", "Claude")}\'s 200K context window for full patient record analysis.',
            ),
        ],
    },
    {
        "post_id": 385,
        "slug": "copilot-legal",
        "replacements": [
            (
                "Do not use it for legal research. For research, usePerplexity AIfor current events and regulatory lookups, or dedicated legal research platforms.",
                f'Do not use it for legal research. For research, use {link("/perplexity/", "Perplexity AI")} for current events and regulatory lookups, or dedicated legal research platforms.',
            ),
        ],
    },
    {
        "post_id": 380,
        "slug": "perplexity-insurance",
        "replacements": [
            (
                "For policy analysis, use Claude. For drafting proposals and correspondence, use ChatGPT orCopilot. Perplexity fills the current-information research layer that the other tools lack.",
                f'For policy analysis, use Claude. For drafting proposals and correspondence, use ChatGPT or {link("/copilot/", "Copilot")}. Perplexity fills the current-information research layer that the other tools lack.',
            ),
        ],
    },
    {
        "post_id": 373,
        "slug": "claude-finance",
        "replacements": [
            (
                "If you need AI assistance directly inside Excel, Word, or Outlook,Microsoft Copilotoffers deeper native integration with the M365 tools many advisors already use for client reports and correspondence.",
                f'If you need AI assistance directly inside Excel, Word, or Outlook, {link("/copilot/", "Microsoft Copilot")} offers deeper native integration with the M365 tools many advisors already use for client reports and correspondence.',
            ),
        ],
    },
    {
        "post_id": 371,
        "slug": "claude-real-estate",
        "replacements": [
            (
                "Claude has fewer native integrations with CRM and email platforms than ChatGPT orMicrosoft Copilot. Most workflows involve copy-paste. If you need an AI tool that lives inside your email client or CRM,Copilotor a ChatGPT-based integration may be more practical.",
                f'Claude has fewer native integrations with CRM and email platforms than ChatGPT or {link("/copilot/", "Microsoft Copilot")}. Most workflows involve copy-paste. If you need an AI tool that lives inside your email client or CRM, {link("/copilot/", "Copilot")} or a ChatGPT-based integration may be more practical.',
            ),
        ],
    },
    {
        "post_id": 366,
        "slug": "chatgpt-insurance",
        "replacements": [
            (
                "For regulatory research, usePerplexity AIto find current state-specific guidance from primary sources.",
                f'For regulatory research, use {link("/perplexity/", "Perplexity AI")} to find current state-specific guidance from primary sources.',
            ),
            (
                "For thorough policy review of complex commercial coverage,Claude's larger context window is more appropriate.",
                f'For thorough policy review of complex commercial coverage, {link("/claude/", "Claude")}\'s larger context window is more appropriate.',
            ),
        ],
    },
    {
        "post_id": 365,
        "slug": "chatgpt-finance",
        "replacements": [
            (
                "For current market information, usePerplexity AIor your research platform alongside ChatGPT.",
                f'For current market information, use {link("/perplexity/", "Perplexity AI")} or your research platform alongside ChatGPT.',
            ),
            (
                "For long-document analysis,Claude's 200K context window is more appropriate.",
                f'For long-document analysis, {link("/claude/", "Claude")}\'s 200K context window is more appropriate.',
            ),
        ],
    },
    {
        "post_id": 364,
        "slug": "chatgpt-engineers",
        "replacements": [
            (
                "For tasks where you want AI inline in your editing flow, Cursor or GitHubCopiloteliminates that friction.",
                f'For tasks where you want AI inline in your editing flow, Cursor or GitHub {link("/copilot/", "Copilot")} eliminates that friction.',
            ),
        ],
    },
    {
        "post_id": 362,
        "slug": "chatgpt-physicians",
        "replacements": [
            (
                "For real-time encounter transcription, useOtter.aior a dedicated ambient documentation tool. The strongest documentation workflow combines both:Otter.aicaptures the spoken encounter, ChatGPT formats the transcript into a structured clinical document.",
                f'For real-time encounter transcription, use {link("/otter/", "Otter.ai")} or a dedicated ambient documentation tool. The strongest documentation workflow combines both: {link("/otter/", "Otter.ai")} captures the spoken encounter, ChatGPT formats the transcript into a structured clinical document.',
            ),
        ],
    },
    {
        "post_id": 361,
        "slug": "chatgpt-legal",
        "replacements": [
            (
                "For high-volume workflows across an active file, this copy-paste overhead becomes significant.Microsoft Copilot's integration with Word and Outlook avoids this friction for M365 firms.",
                f'For high-volume workflows across an active file, this copy-paste overhead becomes significant. {link("/copilot/", "Microsoft Copilot")}\'s integration with Word and Outlook avoids this friction for M365 firms.',
            ),
            (
                "For full-length contract review of 100+ page agreements,Claude's larger context window handles the task more reliably.",
                f'For full-length contract review of 100+ page agreements, {link("/claude/", "Claude")}\'s larger context window handles the task more reliably.',
            ),
        ],
    },
]


def count_occurrences(value, needle, counter):
    if isinstance(value, str):
        counter[0] += value.count(needle)
    elif isinstance(value, list):
        for v in value:
            count_occurrences(v, needle, counter)
    elif isinstance(value, dict):
        for v in value.values():
            count_occurrences(v, needle, counter)


def replace_in_value(value, old, new):
    if isinstance(value, str):
        return value.replace(old, new)
    elif isinstance(value, list):
        return [replace_in_value(v, old, new) for v in value]
    elif isinstance(value, dict):
        return {k: replace_in_value(v, old, new) for k, v in value.items()}
    return value


def main():
    total_fixed = 0
    total_skipped = 0
    for page in FIXES:
        post_id = page["post_id"]
        slug = page["slug"]
        print(f"\n=== {slug} (post {post_id}) ===")

        resp = requests.get(
            f"{WP_URL}/wp/v2/cross_reference/{post_id}",
            params={"context": "edit", "_fields": "id,content"},
            auth=AUTH,
        )
        resp.raise_for_status()
        raw = resp.json()["content"]["raw"]

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"  ABORT — existing content isn't valid JSON ({e}). Not touching this post.")
            continue

        applied_any = False
        for old, new in page["replacements"]:
            counter = [0]
            count_occurrences(data, old, counter)
            if counter[0] == 0:
                print(f"  SKIP — old text not found (may already be fixed): {old[:70]}...")
                total_skipped += 1
                continue
            if counter[0] > 1:
                print(f"  SKIP — old text found {counter[0]} times (ambiguous, needs manual review): {old[:70]}...")
                total_skipped += 1
                continue
            data = replace_in_value(data, old, new)
            applied_any = True
            total_fixed += 1
            print(f"  Fixed: {old[:70]}...")

        if not applied_any:
            print("  No changes applied for this post.")
            continue

        new_raw = json.dumps(data, ensure_ascii=False)
        put_resp = requests.post(
            f"{WP_URL}/wp/v2/cross_reference/{post_id}",
            headers={
                "X-HTTP-Method-Override": "PUT",
                "Content-Type": "application/json; charset=utf-8",
            },
            auth=AUTH,
            data=json.dumps({"content": new_raw}, ensure_ascii=False).encode("utf-8"),
        )
        put_resp.raise_for_status()
        print(f"  Saved post {post_id}.")

    print(f"\n\nDone. Fixed: {total_fixed}, Skipped: {total_skipped}.")
    print("Give WP.com/CDN caching a minute, then spot-check a few of the pages above.")


if __name__ == "__main__":
    main()
