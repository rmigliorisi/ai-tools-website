# CLAUDE.md

This file provides guidance to AI coding assistants working with this repository.

## Project Overview

AI Tools for Pros is a WordPress site reviewing 10 AI tools across 8 professions. The live site runs on **WordPress.com Business** with a custom PHP theme (`aifp-theme/`). 66 content pages total (10 tool hubs + 8 profession hubs + 41 cross-references + contact + static pages).

**Live site:** aitoolsforpros.com

## Architecture

Three content page types, all served by the custom `aifp-theme/`:

- **Tool Hub Pages** (10) — `single-tool_review.php` — 15-section template reviewing one AI tool
- **Profession Hub Pages** (8) — `single-profession_hub.php` — landing pages per profession
- **Cross-Reference Pages** (41) — `single-cross_reference.php` — tool × profession deep dives

Plus standard WordPress pages:
- `/contact/` — uses `page-templates/page-contact.php`
- `/newsletter/`, `/about-us/`, `/our-process/`, `/privacy-policy/`, `/cookie-policy/` — standard WP pages

### CSS Architecture
- CSS custom properties for theming (light mode default)
- Dark mode via `body.dark-mode` class
- Wide-screen centering: `@media (min-width: 1060px)` uses `calc((100% - 900px) / 2)` for section padding
- Author card alignment: `main:not([style]):not(.prose-page) > .author-card` selector distinguishes profession hub pages from cross-reference pages

### JavaScript
- Dark mode persistence: localStorage (production) + window.name fallback (file:// protocol)
- Reading time calculation injected into `<span id="reading-time">`
- Mobile nav toggle, cookie consent banner

### Path Conventions
- Root pages: `logo.svg`, `style.css`, `site.js`, `author.svg`
- Subdirectory pages: `../logo.svg`, `../style.css`, `../site.js`, `../author.svg`
- (These conventions apply to the static HTML source files, not the WordPress theme)

## Deployment Pipeline

**Never manually upload theme files.** Changes deploy automatically:

1. Edit files in `aifp-theme/`
2. `git push` to `main`
3. GitHub Actions (`wpcom.yml`) runs QA checks — **blocks deploy if anything fails**
4. WordPress.com picks up the artifact and deploys to `/wp-content/themes/aifp-theme/`

**Manual deploy:** GitHub Actions tab → "Deploy Theme to WordPress.com" → "Run workflow"

The QA checks that run before every deploy:
- PHP syntax check on all `.php` files
- `[VERIFY DETAILS]` flag scan
- Debug code scan (`var_dump`, `print_r`, `die()`)
- Required files existence check

## WordPress Custom Post Types

| Post Type | Purpose |
|-----------|---------|
| `tool_review` | Tool hub pages (10) |
| `profession_hub` | Profession hub pages (8) |
| `cross_reference` | Cross-reference pages (41) |
| `aifp_subscriber` | Newsletter email signups |
| `aifp_contact` | Contact form submissions |

Contact submissions appear in **WP Admin → Contact Submissions** and also trigger an email to the admin address.

## Content Generation Workflow

Pages are generated externally and validated here:

1. Paste `docs/AIFORPROS.md` + `docs/AIFORPROS-REFERENCE.md` + PAGE VARIABLES into ChatGPT (one page per session)
2. ChatGPT outputs full HTML
3. Validate against repo state + content rules → PASS/FAIL report + corrected HTML
4. Write passing HTML to repo

### Key Reference Files (in `docs/`)
- **docs/AIFORPROS.md** — Master content prompt (all section templates, tone, word counts)
- **docs/AIFORPROS-REFERENCE.md** — Verbatim HTML boilerplate for nav, footer, author cards
- **docs/AIFORPROS-QA.md** — Validation checklist for generated pages

## Content Rules (Non-Negotiable)

### Em Dash Rule
- **ALLOWED:** H1/H2/H3 headings, `<title>`, og:title, og:description, JSON-LD "headline", HTML comments, Sources Checked `[N] Vendor — description`
- **PROHIBITED:** All body paragraphs, bullets, FAQs, link text, pricing tables, consistency blocks

### [VERIFY DETAILS] Flag
Use `[VERIFY DETAILS]` (not `[VERIFY]`) on any claim needing vendor confirmation: pricing, HIPAA/compliance status, feature availability, plan names, URLs. Must have real text before the flag, never as the entire field value.

### Verdict Badges
- `.verdict-badge-recommended` — blue (#2563EB) — broadly useful tools
- `.verdict-badge-specialized` — purple (#7c3aed) — ecosystem-specific tools (Perplexity, Midjourney, Notion AI)
- Consistency block labels, read-guide-link hover, back-to-top hover must match the badge color

### H1 Format (Hub Pages)
Pattern: `[Tool Name] for Professionals: An Honest Review (2026)`

### Profession Cards
Only link to cross-reference pages that actually exist. No dead links.

## Hub Page Template (15 Sections, In Order)

1. Page Header: breadcrumb, tool-badge, H1, subtitle, meta-row (verdict badge + date + read time)
2. Consistency Blocks (5): Bottom Line, Key Takeaway, Best For, Avoid If, Mini Workflow
3. Quick Facts Bar (5 columns): Made By, Best For, Pricing, [tool-specific], HIPAA
4. What It Is (and Is Not)
5. Who It's Right For
6. Features That Matter (7 features)
7. Pricing table
8. Profession Cards
9. Comparison table (highlight-row for the tool being reviewed)
10. Our Verdict
11. FAQ (6 Q&A, answers start with Yes/No/It depends)
12. Sources Checked (5 sources, numbered badges)
13. What Most Reviews Miss (3 insights + insight-banner)
14. Related Guides grid
15. Footer + back-to-top button

## SVG Avatars

Hand-coded SVG illustrations, not image files:

- **author.svg** — Rich Migliorisi (founder). Short dark hair, V-neck blue sweater, light stubble. Skin: `#f5d0b2` face, `#edc5a3` ears.
- **ryan-cooper.svg** — Ryan Cooper (fact-checker). Bald, dark beard with mustache, lavender button-down. Skin: `#f0c4a0` face, `#e8b894` ears.
- **about-us.html** contains an inline copy of Rich's SVG that must stay in sync with `author.svg`.

## Removed Pages

- `cursor/architects.html` — Deleted. Nav links removed from all pages.

## Special Notes

- **newsletter.html** — "Recent Issues" section is hidden (`display:none`). Restore when real content exists.
- **No templating system** — Each static HTML file is self-contained. The WordPress theme uses PHP includes via `header.php` and `footer.php`.
- **WordPress.com hosting** — No SSH access. No cPanel. Theme files are deployed via GitHub Actions only.
- **Jetpack backups** — WordPress.com/Jetpack handles automatic site backups. No manual backup step needed.

## Team

- **Rich Migliorisi** — Founder, SEO professional (8+ years)
- **Ryan Cooper** — Fact-Checker & Editor, product manager (8 years EdTech)
