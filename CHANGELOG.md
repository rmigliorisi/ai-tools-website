# Changelog

All notable changes to the AI Tools for Pros website are documented here.

This project was developed iteratively with AI assistance (Claude Code). GitHub was connected partway through development, so early work is captured in the initial commit.

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
- **Cross-reference page CSS overhaul** — Normalized styles across all 41 cross-reference pages:
  - Standardized heading styles, spacing, and font sizes
  - Fixed inconsistent padding and margins
  - Unified author card and byline formatting
  - Normalized comparison table layouts
  - Cleaned up FAQ section formatting
- **Hub page CSS cleanup** — Minor style fixes across all 10 tool hub pages
- **Profession hub page fixes** — Standardized nav link styling and section spacing across all 8 profession pages
- **style.css expansion** — Added ~220 lines of new CSS rules for consistent cross-page styling, responsive layout fixes, and component normalization

---

## [2026-03-25] — Homepage Padding Test

### Changed
- Minor padding adjustment on `index.html` for testing layout spacing

---

## [2026-03-25] — Initial Commit

### Added
- **Complete website launch** — 84 files, ~48,000 lines of code
- **10 Tool Hub Pages** — In-depth reviews of ChatGPT, Claude, Perplexity, Google Gemini, Microsoft Copilot, Midjourney, Cursor, Notion AI, Grammarly, and Otter.ai
- **8 Profession Hub Pages** — Landing pages for Legal, Physicians, Real Estate, Engineers, Finance, Insurance, Architects, and Creatives
- **41 Cross-Reference Pages** — Tool-specific guides for each profession (e.g., `chatgpt/legal.html`, `claude/engineers.html`)
- **Homepage** (`index.html`) — Main landing page with tool grid and profession navigation
- **About Us** (`about-us.html`) — Founder profile with hand-coded SVG avatar
- **Our Process** (`our-process.html`) — Editorial methodology explanation
- **Newsletter** (`newsletter.html`) — Email signup page (Recent Issues section hidden until content exists)
- **Policy pages** — Cookie policy and privacy policy
- **Global stylesheet** (`style.css`) — ~1,700 lines covering all page types, responsive design, dark/light components
- **JavaScript** (`site.js`) — Mobile navigation, cookie consent banner, scroll-to-top, dropdown menus
- **SVG assets** — Logo, favicon, author avatar
- **SEO infrastructure** — JSON-LD structured data on every page, sitemap.xml, robots.txt, Open Graph tags
- **Content generation system** — `AIFORPROS.md` (master prompt), `AIFORPROS-REFERENCE.md` (HTML boilerplate), `AIFORPROS-QA.md` (validation checklist)

---

## Removed Pages

- **`cursor/architects.html`** — Deleted (below-average content quality, no genuine fit per the tool-profession combo matrix). Nav links removed from all pages.
