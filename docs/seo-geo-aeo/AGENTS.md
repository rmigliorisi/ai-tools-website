# Project Instructions for AI Coding Agents

You are working on a website that must meet high standards for SEO, AI Search Visibility, accessibility, and agent-friendly usability.

## Primary goals

1. Preserve crawlability and indexability.
2. Use clean semantic HTML.
3. Ensure important content is visible in initial or rendered HTML.
4. Keep HTML/text responses lean, especially below the 2 MB Googlebot processing threshold for HTML/text responses.
5. Use real links and buttons.
6. Maintain accessible names, roles, labels, and states.
7. Use only relevant Google-supported structured data.
8. Improve internal linking without over-optimization.
9. Avoid introducing duplicate, thin, low-value, or generic AI-looking content.
10. Produce a change log for every batch of edits.

## Required behavior

Before making changes:
- Read all files in `/docs/seo/` or `/seo-requirements/`.
- Identify the affected page templates or components.
- Explain the issue, severity, and proposed fix.
- Do not implement until the user approves.

When implementing:
- Make minimal, targeted changes.
- Preserve existing URL paths unless a migration is explicitly approved.
- Preserve canonical rules unless explicitly approved.
- Do not add robots.txt blocks or noindex directives without approval.
- Do not add schema that does not match visible page content.
- Do not hide important content behind click-only or scroll-only interactions.
- Prefer semantic HTML over div/span-based custom controls.
- Keep CTAs, forms, navigation, and cards accessible.

After implementing:
- Provide a summary of files changed.
- Provide before/after behavior.
- Provide validation steps.
- Provide rollback notes.

## Hard no

Do not:
- add fake FAQ/schema markup not visible on-page
- use schema as a dumping ground for keywords
- use JavaScript-only internal links
- make cards clickable with only `div onclick`
- rely on hover-only navigation
- lazy-load primary content in a way crawlers/agents may not see
- noindex important pages without approval
- canonicalize strategic pages to unrelated URLs
- block CSS/JS required for rendering
- create massive inline JSON or hydration state that bloats HTML
