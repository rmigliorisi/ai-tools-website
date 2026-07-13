# AI Tools for Pros

An independent review site that helps working professionals find the right AI tools for their workflows. No paid placements, no affiliate bias. Just honest, profession-specific reviews.

**Live site:** [aitoolsforpros.com](https://aitoolsforpros.com)

## What This Is

AI Tools for Pros reviews 10 major AI tools across 8 professional fields, producing three types of content:

1. **Tool Hub Pages** (10) — In-depth reviews of each AI tool from a professional's perspective
2. **Profession Hub Pages** (8) — Landing pages for each profession showing which AI tools are relevant
3. **Cross-Reference Pages** (41) — Deep dives into specific tool + profession combinations (e.g., "ChatGPT for Legal Professionals")

## Tech Stack

- **WordPress.com Business** — live site hosted on WordPress.com Business plan
- **Custom theme** (`aifp-theme/`) — PHP templates, CSS, and JS
- **Custom post types** — `tool_review`, `profession_hub`, `cross_reference`, `aifp_subscriber`, `aifp_contact`
- **JSON content storage** — page content stored as JSON in `post_content`; fetched via REST API
- **Static HTML files** — original static site source kept as reference/archive (root-level `.html` files)
- **Python scripts** — one-off migration and content push scripts (credentials in `.env`)
- **SEO-first architecture** — custom sitemap, robots.txt, Open Graph tags, JSON-LD schema

## Project Structure

```
├── aifp-theme/                 # Live WordPress custom theme (auto-deployed via GitHub Actions)
│   ├── functions.php           # Theme setup, CPTs, REST API, rewrites, sitemap, AJAX handlers
│   ├── header.php              # Site header
│   ├── footer.php              # Site footer (includes nav, contact link, newsletter subscribe JS)
│   ├── front-page.php          # Homepage template
│   ├── single-tool_review.php  # Tool hub page template
│   ├── single-profession_hub.php # Profession hub page template
│   ├── single-cross_reference.php # Cross-reference page template
│   ├── page-templates/
│   │   └── page-contact.php   # Contact page template (form + AJAX + honeypot)
│   ├── inc/
│   │   ├── cpt.php             # Custom post types and rewrite rules
│   │   ├── helpers.php         # Theme helper functions
│   │   └── json-ld.php         # JSON-LD structured data
│   └── assets/
│       ├── css/                # site.css, components.css
│       ├── js/                 # site.js (dark mode, mobile nav, etc.)
│       └── svg/                # favicon.svg, logo.svg, avatars
│
├── .github/
│   └── workflows/
│       ├── wpcom.yml           # PRIMARY: QA + deploys aifp-theme/ to WordPress.com on push
│       └── deploy-theme.yml    # SECONDARY: QA-only check (also runs on pull requests)
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
├── gemini.html                 # │  Tool Hub Pages (10) — static source reference
├── copilot.html                # │
├── midjourney.html             # │
├── cursor.html                 # │
├── notion-ai.html              # │
├── grammarly.html              # │
├── otter.html                  # ┘
│
├── legal.html                  # ┐
├── physicians.html             # │
├── real-estate.html            # │  Profession Hub Pages (8) — static source reference
├── engineers.html              # │
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
├── sitemap.xml                 # Static XML sitemap (source reference — WP generates live one)
├── robots.txt                  # Source reference — live version served by WordPress
│
└── dev/                        # Development/testing files (not used in production)
    └── browser-test.html       # Browser compatibility test page
```

## Deployment Pipeline

Theme changes are deployed automatically via GitHub Actions + WordPress.com Deployments:

```
Edit aifp-theme/ files → git push to main
        ↓
GitHub Actions: wpcom.yml runs
  1. PHP syntax check (blocks deploy on parse/fatal errors)
  2. [VERIFY DETAILS] flag scan (blocks deploy if flags remain)
  3. Debug code check (blocks deploy if var_dump/print_r/die found)
  4. Required files check (verifies critical theme assets exist)
        ↓ (all checks pass)
WordPress.com: picks up the artifact, deploys to /wp-content/themes/aifp-theme/
        ↓
Jetpack: automatic backup runs after each deploy
```

**deploy-theme.yml** runs the same QA checks on pull requests (without deploying), so problems are caught before code reaches `main`.

**To trigger a manual deploy:** Go to the GitHub Actions tab → "Deploy Theme to WordPress.com" → "Run workflow".

## WordPress Pages

| URL | Template |
|-----|----------|
| `/` | `front-page.php` (homepage) |
| `/[tool]/` | `single-tool_review.php` (10 tool hub pages) |
| `/[profession]/` | `single-profession_hub.php` (8 profession pages) |
| `/[tool]/[profession]/` | `single-cross_reference.php` (41 cross-reference pages) |
| `/contact/` | `page-templates/page-contact.php` |
| `/newsletter/` | Standard WP page |
| `/about-us/` | Standard WP page |
| `/our-process/` | Standard WP page |
| `/privacy-policy/` | Standard WP page |
| `/cookie-policy/` | Standard WP page |

## WP Admin — Custom Post Types

| Post Type | Admin Label | Purpose |
|-----------|-------------|---------|
| `tool_review` | Tool Reviews | One per AI tool (10 total) |
| `profession_hub` | Profession Hubs | One per profession (8 total) |
| `cross_reference` | Cross-References | One per tool+profession combo (41 total) |
| `aifp_subscriber` | Subscribers | Newsletter signups (captured via AJAX) |
| `aifp_contact` | Contact Submissions | Contact form submissions (stored + emailed) |

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

### Contact Page

Live at `/contact/`. Built with:
- AJAX form submission (no page reload)
- Honeypot spam protection
- Server-side validation + sanitization
- Submissions stored as `aifp_contact` custom posts in WP Admin
- Email notification sent to admin on each submission

### Navigation

All pages share a consistent nav structure with dropdowns for tools and professions. The nav is defined in `header.php` on the WordPress theme.

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
4. **docs/AIFORPROS-QA.md** — QA validation checklist run to catch errors before publishing
5. Validated HTML is written directly to the repo

## Content Rules

- **Em dash rule**: Em dashes allowed in headings and metadata only, never in body text
- **[VERIFY DETAILS] flag**: Applied to any claim needing vendor confirmation (pricing, compliance, features). Must have real text before the flag, never as the entire field value.
- **Verdict badges**: Blue (`.verdict-badge-recommended`) for broadly useful tools, purple (`.verdict-badge-specialized`) for ecosystem-specific tools
- **No dead links**: Profession cards only link to cross-reference pages that exist

## Team

- **Rich Migliorisi** — Founder. SEO professional, 8+ years experience.
- **Ryan Cooper** — Fact-Checker & Editor. Product manager, 8 years EdTech experience.

## License

All content is original. All rights reserved.
