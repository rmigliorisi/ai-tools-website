#!/usr/bin/env python3
"""
Patches the existing July 2026 AI Updates draft (post 979) to add internal
links: inline anchor links to tool names within summaries, plus
related_tool_slugs so the new "Related Reviews" section in
single-aifp_update.php renders automatically.

This is a one-off fix for the first live proof-of-concept. Going forward,
docs/AIFORPROS-AUTOMATED-CONTENT.md's "Content Optimization Guardrails"
section makes this structural for every future run.

Run locally:
    python3 patch_july_2026_update_links.py
"""

import json
import requests
from wp_creds import AUTH, WP_URL

POST_ID = 979

DATA = {
    "month_label": "July 2026",
    "intro": (
        "This month brought a wave of agentic upgrades across the tools I review "
        "regularly, a new flagship model from Anthropic, and a lineup change from "
        "OpenAI. Here is what actually matters if you use these tools for "
        "professional work, plus a couple of items still developing that are "
        "worth watching."
    ),
    "news_items": [
        {
            "headline": "Anthropic Launches Claude Sonnet 5",
            "summary": (
                'Anthropic released <a href="https://aitoolsforpros.com/claude/">Claude</a> '
                "Sonnet 5, its most agentic Sonnet model yet, with meaningful gains over "
                "Sonnet 4.6 in reasoning, tool use, coding, and knowledge work. "
                "Introductory pricing runs through August 31, 2026."
            ),
            "source_name": "Anthropic Newsroom",
            "source_url": "https://www.anthropic.com/news",
        },
        {
            "headline": "Claude Cowork Expands to Web and Mobile",
            "summary": (
                "Claude's Cowork mode now works across web and mobile, carrying "
                "sessions and files between devices under one shared home for Chat "
                "and Cowork. Anthropic also added Microsoft 365 write tools, letting "
                "Claude draft and send email, manage calendar events, and update "
                "OneDrive and SharePoint files directly."
            ),
            "source_name": "Anthropic Newsroom",
            "source_url": "https://www.anthropic.com/news",
        },
        {
            "headline": "OpenAI Rolls Out GPT-5.6 as a Three-Tier Lineup",
            "summary": (
                "OpenAI split its latest model into three tiers built for different "
                "jobs: Sol for high-end reasoning and coding, Terra for GPT-5.5-level "
                "quality at roughly half the cost, and Luna for fast, high-volume "
                'tasks. OpenAI also launched <a href="https://aitoolsforpros.com/chatgpt/">'
                "ChatGPT</a> Work, which breaks a stated goal into steps and executes "
                "across apps and files with minimal supervision."
            ),
            "source_name": "llm-stats.com AI model update tracker",
            "source_url": "https://llm-stats.com/llm-updates",
        },
        {
            "headline": "Cursor Ships Side Chats and a Public iOS Beta",
            "summary": (
                '<a href="https://aitoolsforpros.com/cursor/">Cursor</a>\'s July 11 '
                "release added side chats, agent transcript search, and simpler "
                "project and repo pickers. Cursor for iOS also entered public beta "
                "on all paid plans, bringing always-on agents, remote control, and "
                "mobile code review."
            ),
            "source_name": "Cursor Changelog",
            "source_url": "https://cursor.com/changelog",
        },
        {
            "headline": "Notion 3.6 Brings External Agents Into the Workspace",
            "summary": (
                'Notion\'s July 1 release lets Claude and Cursor act as the first two '
                'External Agents inside <a href="https://aitoolsforpros.com/notion-ai/">'
                "Notion</a>, automating processes end to end alongside a team's own "
                "work. The update also adds speaker-identified AI meeting notes and "
                "interactive HTML blocks."
            ),
            "source_name": "Notion Release Notes",
            "source_url": "https://www.notion.com/releases/2026-07-01",
        },
        {
            "headline": "Perplexity's Comet Agent Defaults to Claude Models",
            "summary": (
                '<a href="https://aitoolsforpros.com/perplexity/">Perplexity</a>\'s Comet '
                "Agent now runs on Claude Sonnet 4.6 by default for Pro subscribers and "
                "Opus 4.6 for Max subscribers, alongside an expanded Deep Research mode "
                "inside Perplexity's Computer assistant."
            ),
            "source_name": "Releasebot - Perplexity AI",
            "source_url": "https://releasebot.io/updates/perplexity-ai",
        },
        {
            "headline": "Grammarly Renames Its Premium Tier to Pro",
            "summary": (
                '<a href="https://aitoolsforpros.com/grammarly/">Grammarly</a> retired '
                'the "Premium" label in favor of "Pro" at the same $12/month price '
                "point. The change is naming only; the underlying features have not "
                "moved."
            ),
            "source_name": "Toolchase AI Tools News",
            "source_url": "https://toolchase.com/blog/ai-tools-news-2026/",
        },
        {
            "headline": "Meta Restructures Around AI, Cutting About 8,000 Roles",
            "summary": (
                "Meta began layoffs affecting roughly 8,000 employees, about 10% of "
                "its workforce, while reassigning another 7,000 to AI-focused teams "
                "as part of a broader restructuring toward AI product development."
            ),
            "source_name": "Crescendo AI News Roundup",
            "source_url": "https://www.crescendo.ai/news/latest-ai-news-and-updates",
        },
    ],
    "related_tool_slugs": [
        "claude", "cursor", "notion-ai", "perplexity", "grammarly", "chatgpt",
    ],
    "related_profession_slugs": [],
    "what_to_watch": (
        "A few threads worth tracking into next month: reports point to the White "
        "House finalizing voluntary frontier AI standards with OpenAI, Google, and "
        "Anthropic, covering release benchmarks and testing timelines. xAI's Grok "
        "4.5 is reportedly in private beta at SpaceX and Tesla, with vendor claims "
        "of near-Opus performance that have not been independently verified yet. "
        "And Grammarly's tier rename is a small signal worth watching for whether "
        "pricing itself moves next, not just the label."
    ),
}


def main():
    endpoint = f"{WP_URL}/wp/v2/aifp_update/{POST_ID}"
    payload = {"content": json.dumps(DATA, ensure_ascii=False)}

    req = requests.Request("POST", endpoint, json=payload, auth=AUTH)
    prepared = req.prepare()
    prepared.headers["X-HTTP-Method-Override"] = "PUT"

    with requests.Session() as s:
        resp = s.send(prepared, timeout=30)

    if resp.status_code in (200, 201):
        print(f"Updated post {POST_ID} with internal links.")
    else:
        print(f"FAILED: HTTP {resp.status_code}")
        try:
            print(resp.json())
        except Exception:
            print(resp.text[:500])


if __name__ == "__main__":
    main()
