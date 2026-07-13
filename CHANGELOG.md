# Changelog

All notable changes to the AI Tools for Pros website are documented here.

---

## [2026-07-06] — Auto-Deploy Pipeline, Contact Page Live, Docs Overhaul

### Added
- **GitHub Actions deploy pipeline** — `wpcom.yml` workflow: runs QA checks then uploads `aifp-theme/` as an artifact to WordPress.com Deployments on every push to `main` that touches theme files
- **GitHub Actions QA workflow** — `deploy-theme.yml`: PHP syntax check + flag scan on push and pull requests (no deploy, acts as a gate for PRs)
- **QA checks in pipeline**: PHP syntax check, `[VERIFY DETAILS]` flag scan, debug code scan (`var_dump`/`print_r`/`die()`), required files existence check
- **Contact page live** — `/contact/` page created in WordPress using `page-templates/page-contact.php` template (Page ID: 976)

### Changed
- **README.md** — Complete overhaul: reflects WordPress.com Business hosting, auto-deploy pipeline, all custom post types, WordPress page inventory, deployment instructions
- **CLAUDE.md** — Updated to reflect current state: WordPress.com hosting, deploy pipeline, contact page, removed outdated manual upload references

---

## [2026-05-21] — Contact Page Template

### Added
- **Contact page template** (`aifp-theme/page-templates/page-contact.php`) — Full contact form with AJAX submission, honeypot spam protection, client-side and server-side validation
- **Contact AJAX handler** in `functions.php` — validates, sanitizes, stores submission as `aifp_contact` CPT, sends email notification to admin with Reply-To set to submitter
- **`aifp_contact` custom post type** in `inc/cpt.php` — contact form submissions viewable in WP Admin → Contact Submissions
- **Footer contact link** added to `footer.php`

---

## [2026-05-12] — Newsletter Subscriber Capture + Google Tag Manager

### Added
- **Newsletter subscriber AJAX** — subscribe buttons on newsletter page captured via `wp_footer` JS; stores email as `aifp_subscriber` CPT
- **GTM dataLayer push** on newsletter subscribe success (`event: newsletter_subscribe`)
- **Google Tag Manager container** (`GTM-KCVDNRMV`) added to `<head>` and `<body>` via `functions.php`

### Fixed
- **Newsletter button selector** — fixed incorrect selector; button is a sibling of the input, not a child

---

## [2026-05-11] — Profession Hub Lede Fix

### Fixed
- **Profession hub lede HTML rendering** — fixed raw HTML appearing as text instead of rendered markup

---

## [2026-05-06] — SEO / GEO / AEO Requirements Docs

### Added
- **`docs/seo-geo-aeo/`** — 13 detailed SEO, GEO (geographic), and AEO (answer engine optimization) requirement documents covering technical SEO, schema, internal linking, content quality, accessibility, robots/sitemaps, and AI search readiness
- **SEO improvements** — improved homepage metadata and JSON-LD schema
- **robots.txt** — updated to point to `wp-sitemap.xml`; suppressed empty author archive from sitemap

---

## [2026-04-02] — Author Avatars, Ryan Cooper, Skin Tone Refinements

### Added
- **Ryan Cooper profile** — Created hand-coded SVG avatar (`ryan-cooper.svg`): bald head, dark beard with mustache, lavender button-down shirt
- **Ryan Cooper on about-us.html** — Added his section below the founder with bio, LinkedIn link, and SVG avatar
- **Ryan Cooper fact-checker credit** — Added his LinkedIn icon next to his name as fact-checker across all 59 content pages (hub pages, profession pages, cross-reference pages)
- **JSON-LD update** — Added Ryan Cooper as a Person entity on the About page

### Changed
- **Rich Migliorisi avatar refinements** — Multiple rounds of iteration on `author.svg`:
  - Replaced old avatar (glasses, dark suit) with casual look (V-neck sweater, no glasses)
  - Redesigned hair as single unified path with natural sideburns
  - Adjusted smile to show teeth moderately
  - Added light stubble
  - Tuned skin tone to fair complexion (`#f5d0b2` face, `#edc5a3` ears)
- **Hub page author bylines** — Replaced old inline SVG avatars with `<img src="author.svg">` across all 10 hub pages
- **About-us.html inline SVG** — Kept in sync with author.svg through all changes
- **Ryan Cooper skin tone** — Adjusted to fair complexion matching the illustration style

---

## [2026-04-02] — CSS Fixes, Author Byline Alignment, Spacing

### Fixed
- **Author byline alignment on profession hub pages** — Fixed misalignment on wide screens (>1060px) where the author card shifted left relative to section content. Added `@media (min-width: 1060px)` rule for `.author-card` with matching `calc((100% - 900px) / 2)` margins
- **Excessive whitespace above author byline** — Reduced FAQ section bottom padding from `min(8rem,10vw)` to `min(3rem,4vw)` on 7 profession pages. Reduced author card top margin from 40px to 16px

### Changed
- **Author byline CSS** — New rules in `style.css` for `main:not([style]):not(.prose-page) > .author-card` to handle centering on profession hub pages vs. cross-reference pages
- **Key Takeaway consistency block** — Changed accent color from blue to purple on specialized-verdict tools (Perplexity, Midjourney, Notion AI)

---

## [2026-03-27] — Site-Wide CSS Normalization and QA

### Changed
- **Cross-reference page CSS overhaul** — Normalized styles across all 41 cross-reference pages
- **Hub page CSS cleanup** — Minor style fixes across all 10 tool hub pages
- **Profession hub page fixes** — Standardized nav link styling and section spacing across all 8 profession pages
- **style.css expansion** — Added ~220 lines of new CSS rules for consistent cross-page styling, responsive layout fixes, and component normalization

---

## [2026-03-25] — Initial Commit

### Added
- **Complete website launch** — 84 files, ~48,000 lines of code
- **10 Tool Hub Pages** — ChatGPT, Claude, Perplexity, Google Gemini, Microsoft Copilot, Midjourney, Cursor, Notion AI, Grammarly, and Otter.ai
- **8 Profession Hub Pages** — Legal, Physicians, Real Estate, Engineers, Finance, Insurance, Architects, and Creatives
- **41 Cross-Reference Pages** — Tool-specific guides for each profession
- **Homepage** (`index.html`) — Main landing page
- **About Us**, **Our Process**, **Newsletter**, policy pages
- **Global stylesheet** (`style.css`) — ~1,700 lines
- **JavaScript** (`site.js`) — Mobile navigation, cookie consent, scroll-to-top, dropdowns
- **SVG assets** — Logo, favicon, author avatar
- **SEO infrastructure** — JSON-LD, sitemap.xml, robots.txt, Open Graph tags
- **Content generation system** — `AIFORPROS.md`, `AIFORPROS-REFERENCE.md`, `AIFORPROS-QA.md`

---

## Removed Pages

- **`cursor/architects.html`** — Deleted (below-average content quality). Nav links removed from all pages.
