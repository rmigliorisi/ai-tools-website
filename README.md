# AI Tools for Pros

An independent review site that helps working professionals find the right AI tools for their workflows. No paid placements, no affiliate bias. Just honest, profession-specific reviews.

**Live site:** [aitoolsforpros.com](https://aitoolsforpros.com)

## What This Is

AI Tools for Pros reviews 10 major AI tools across 8 professional fields, producing three types of content:

1. **Tool Hub Pages** (10) — In-depth reviews of each AI tool from a professional's perspective
2. **Profession Hub Pages** (8) — Landing pages for each profession showing which AI tools are relevant
3. **Cross-Reference Pages** (41) — Deep dives into specific tool + profession combinations (e.g., "ChatGPT for Legal Professionals")

## Tech Stack

- **WordPress CMS** — live site runs on WordPress with a custom theme (`aifp-theme/`)
- **Custom post types** — `tool_review`, `profession_hub`, `cross_reference` (registered in theme)
- **JSON content storage** — page content stored as JSON in `post_content`; fetched via REST API
- **Custom theme** (`aifp-theme/`) — PHP templates, assets in `aifp-theme/assets/`
- **Static HTML files** — original static site source kept as reference/archive
- **Python scripts** — one-off migration and content push scripts (credentials in `.env`)
- **SEO-first architecture** — custom sitemap, robots.txt, Open Graph tags, JSON-LD schema

## Project Structure

```
├── aifp-theme/                 # Live WordPress custom theme
│   ├── functions.php           # Theme setup, CPTs, REST API, rewrites, sitemap
│   ├── single-tool_review.php  # Tool hub page template
│   ├── single-profession_hub.php # Profession hub page template
│   ├── single-cross_reference.php # Cross-reference page template
│   ├── assets/css/             # site.css, components.css
│   └── assets/js/              # site.js (dark mode, mobile nav, etc.)
│
├── docs/                        # Content generation system (see below)
│
├── [tool].py / push_*.py       # One-off migration/content scripts (see Scripts section)
│
├── index.html                  # Static homepage (source reference)
├── style.css                   # Static shared stylesheet (source reference)
├── site.js                     # Static shared JavaScript (source reference)
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
│   ├── AIFORPROS-QA.md          # QA validation checklist
│   ├── AIFORPROS-GITHUB-CLEANUP.md  # Repo cleanup rules
│   └── aitoolsforpros-internal-linking-rules.md  # Internal linking audit rules
│
└── dev/                         # Development/testing files (not used in production)
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

## WordPress API Scripts

Python scripts in the root push content to WordPress via the REST API. To run any of them:

1. Copy `.env.example` to `.env`
2. Fill in your WordPress username and a fresh Application Password
3. Run: `python3 script_name.py`

**Credential safety**: Never commit `.env`. The `.gitignore` excludes it. If a credential is ever accidentally committed, revoke it in WordPress Admin > Users > Profile > Application Passwords immediately.

| Script | Purpose |
|--------|---------|
| `add_internal_links.py` | Adds contextual links to cross-reference pages |
| `add_hub_links.py` | Adds child links to tool and profession hub pages |
| `fix_hub_links_bullets.py` | Reformats hub links as bullet lists |
| `push_static_pages.py` | Pushes static pages (newsletter, about, etc.) |
| `migrate_v2.py` | Original site migration script (one-off, complete) |

---

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
