# SEO / GEO / AEO Website Requirements Bundle

**Last updated:** 2026-05-04

This bundle is a reusable source-of-truth for building and auditing websites for traditional SEO, technical SEO, AI Search Visibility / GEO / AEO, agent-friendly website UX, accessibility-tree clarity, structured data, internal linking, performance, rendering, and launch QA.

Use these files in any website repo or project folder. They are designed to be read by humans and by AI coding agents such as Claude Code, Codex, Antigravity, Cursor, or similar tools.

## Recommended folder placement

Place the bundle in one of these locations:

```text
/docs/seo/
```

or:

```text
/seo-requirements/
```

Also copy `AGENTS.md` to the root of the repo if your coding agent reads root-level project instructions.

## Files included

1. `AGENTS.md`
2. `01_SEO_REQUIREMENTS.md`
3. `02_AI_SEARCH_GEO_AEO_REQUIREMENTS.md`
4. `03_AGENT_FRIENDLY_WEBSITE_REQUIREMENTS.md`
5. `04_SCHEMA_REQUIREMENTS.md`
6. `05_CONTENT_QUALITY_REQUIREMENTS.md`
7. `06_TECHNICAL_SEO_AUDIT_CHECKLIST.md`
8. `07_ACCESSIBILITY_AND_SEMANTIC_HTML.md`
9. `08_INTERNAL_LINKING_REQUIREMENTS.md`
10. `09_PERFORMANCE_RENDERING_HTML_SIZE.md`
11. `10_ROBOTS_SITEMAPS_CRAWLER_ACCESS.md`
12. `11_LAUNCH_QA_CHECKLIST.md`
13. `12_CLAUDE_ANTIGRAVITY_AUDIT_PROMPTS.md`
14. `13_SOURCES_AND_CURRENT_FACTS.md`

## Core operating principle

Do not optimize for one crawler, one AI engine, or one tool score. Build websites that are crawlable, indexable, fast, accessible, semantically clear, internally well-linked, easy to extract answers from, structured around real user intent, and clear enough for humans, search engines, and AI agents.

## How to use this with Claude / Antigravity / Codex

Give the agent this instruction:

> Audit the site against the attached SEO, GEO/AEO, agent-friendly, accessibility, schema, internal linking, and launch QA requirements. Do not make changes yet. Return a prioritized issue list with affected templates/files, severity, recommended fix, implementation risk, and expected SEO/AI-search impact.

Then review the recommendations before allowing implementation.

## Implementation rule

Agents can assist with diagnosis and code changes, but they should not independently make high-impact SEO decisions such as changing URLs, adding noindex, altering canonicals, blocking crawlers, deleting content, changing schema types, rewriting large sections, or changing navigation/internal link architecture.
