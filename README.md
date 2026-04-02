# AI Tools for Pros

An independent review site that helps working professionals find the right AI tools for their workflows. No paid placements, no affiliate bias. Just honest, profession-specific reviews.

**Live site:** [aitoolsforpros.com](https://aitoolsforpros.com)

## What This Is

AI Tools for Pros reviews 10 major AI tools across 8 professional fields, producing three types of content:

1. **Tool Hub Pages** (10) — In-depth reviews of each AI tool from a professional's perspective
2. **Profession Hub Pages** (8) — Landing pages for each profession showing which AI tools are relevant
3. **Cross-Reference Pages** (41) — Deep dives into specific tool + profession combinations (e.g., "ChatGPT for Legal Professionals")

## Tech Stack

- **Pure static HTML/CSS/JS** — no frameworks, no build step, no dependencies
- **Single shared stylesheet** (`style.css`) — ~1,800 lines covering all page types
- **Vanilla JS** (`site.js`) — mobile nav, cookie consent, scroll behavior
- **Hand-coded SVG avatars** — `author.svg`, `ryan-cooper.svg`
- **Structured data** — JSON-LD schema on every page (FAQ, Review, Article types)
- **SEO-first architecture** — semantic HTML, Open Graph tags, sitemap.xml, robots.txt

## Project Structure

```
├── index.html                  # Homepage
├── style.css                   # Shared stylesheet (all pages)
├── site.js                     # Shared JavaScript
├── logo.svg                    # Site logo
├── favicon.svg                 # Browser favicon
├── author.svg                  # Rich Migliorisi avatar (used in author bylines)
├── ryan-cooper.svg             # Ryan Cooper avatar (used on about page)
│
├── chatgpt.html                # ┐
├── claude.html                 # │
├── perplexity.html             # │
├── gemini.html                 # │  Tool Hub Pages (10)
├── copilot.html                # │  In-depth review of each AI tool
├── midjourney.html             # │
├── cursor.html                 # │
├── notion-ai.html              # │
├── grammarly.html              # │
├── otter.html                  # ┘
│
├── legal.html                  # ┐
├── physicians.html             # │
├── real-estate.html            # │  Profession Hub Pages (8)
├── engineers.html              # │  Which AI tools matter for each field
├── finance.html                # │
├── insurance.html              # │
├── architects.html             # │
├── creatives.html              # ┘
│
├── chatgpt/                    # ┐
│   ├── legal.html              # │  Cross-Reference Pages (41)
│   ├── physicians.html         # │  Tool × Profession deep dives
│   └── ...                     # │  Organized by tool name
├── claude/                     # │
├── copilot/                    # │
├── cursor/                     # │
├── gemini/                     # │
├── grammarly/                  # │
├── midjourney/                 # │
├── notion-ai/                  # │
├── otter/                      # │
├── perplexity/                 # ┘
│
├── about-us.html               # Team page (founder + fact-checker)
├── our-process.html            # Editorial process explanation
├── newsletter.html             # Newsletter signup
├── cookie-policy.html          # Cookie policy
├── privacy-policy.html         # Privacy policy
│
├── sitemap.xml                 # XML sitemap for search engines
├── robots.txt                  # Crawler directives
│
├── docs/                        # Content generation system
│   ├── AIFORPROS.md             # Master content prompt (page generation rules)
│   ├── AIFORPROS-REFERENCE.md   # HTML boilerplate reference (nav, footer, etc.)
│   └── AIFORPROS-QA.md          # QA validation checklist
│
└── dev/                         # Development/testing files
    └── browser-test.html        # Browser compatibility test page
```

## Page Architecture

### Tool Hub Pages

Each tool hub page follows a strict 15-section template:

1. Page header (breadcrumb, tool badge, H1, subtitle, verdict badge)
2. Consistency blocks (Bottom Line, Key Takeaway, Best For, Avoid If, Mini Workflow)
3. Quick Facts bar (5 columns)
4. What It Is (and Is Not)
5. Who It's Right For
6. Features That Matter (7 features)
7. Pricing table
8. Profession cards (links to cross-reference pages)
9. Comparison table (all 10 tools, current tool highlighted)
10. Our Verdict
11. FAQ (6 questions, answers start with Yes/No/It depends)
12. Sources Checked (5 sources with numbered badges)
13. What Most Reviews Miss (3 insights)
14. Related Guides grid
15. Footer with back-to-top button

### Cross-Reference Pages

Each cross-reference page covers a specific tool for a specific profession (e.g., `chatgpt/legal.html`). These include profession-specific use cases, workflow examples, and practical guidance.

### Navigation

All pages share a consistent nav structure with dropdowns for tools and professions. The nav is defined inline in each HTML file (no templating system). Cross-reference pages use `../` relative paths for root assets.

## Content Generation Workflow

Pages are generated using a structured prompt system:

1. **docs/AIFORPROS.md** — Master prompt with all content rules, section templates, and tone guidelines
2. **docs/AIFORPROS-REFERENCE.md** — HTML boilerplate for nav, footer, and author cards
3. Content is generated via ChatGPT using page-specific variables
4. **docs/AIFORPROS-QA.md** — QA validation checklist run in Claude Code to catch errors
5. Validated HTML is written directly to the repo

## Content Rules

- **Em dash rule**: Em dashes allowed in headings and metadata only, never in body text
- **[VERIFY DETAILS] flag**: Applied to any claim needing vendor confirmation (pricing, compliance, features)
- **Verdict badges**: Blue (`.verdict-badge-recommended`) for broadly useful tools, purple (`.verdict-badge-specialized`) for ecosystem-specific tools
- **No dead links**: Profession cards only link to cross-reference pages that exist

## Team

- **Rich Migliorisi** — Founder. SEO professional, 8+ years experience.
- **Ryan Cooper** — Fact-Checker & Editor. Product manager, 8 years EdTech experience.

## License

All content is original. All rights reserved.
