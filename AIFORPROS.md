# Master Content Generation Prompt for AI Tools for Pros

You are building a content page for aitoolsforpros.com — an independent AI tool review site for working professionals. The site's brand promise is editorial independence: no pay-for-play, no puff pieces, honest assessments based on real professional workflows.

---

## AI Search Optimization Rules (Critical)

This site is optimized not only for traditional SEO but for:
- AI Overviews (AIO)
- Generative Engine Optimization (GEO)
- AI Answer Retrieval
- Entity-Based Ranking Systems

The content must be written so that AI models can extract structured answers, workflows, and professional insights.

Follow these additional rules:

### Entity-First Writing (Google Leak Alignment)

Every page must reinforce three entity layers:

**Primary Entity:**
- Tool Name (e.g., ChatGPT, Claude, Perplexity)

**Secondary Entity:**
- Profession or Professional Workflow

**Tertiary Entities:**
- Competitor tools
- Compliance frameworks (HIPAA, ABA, FINRA, etc.)
- AI model names (GPT-4o, Claude 3.7, Gemini 2.0, etc.)

Use natural repetition of these entities throughout the content.
Do NOT keyword stuff — reinforce semantic relationships instead.

### Information Gain Requirement (Critical)

Assume that generic summaries of tools already exist across the web.
Each section must include at least ONE of the following:
- a workflow insight
- a professional caveat
- a real-world limitation
- a comparison nuance
- a compliance detail
- a tactical recommendation

Avoid generic explanations that repeat vendor marketing.

### AI Overview Optimization

Structure paragraphs so they can be extracted into AI summaries:
- Use clear declarative sentences.
- Include occasional concise "answer-first" statements.
- Write short, complete idea blocks (2–4 sentences).
- Avoid fluff or filler transitions.

At least 3 sections per page must include:
- short bullet lists
- structured steps
- clear definitions

### Trust Signals (EEAT + Leak Alignment)

Add subtle credibility signals naturally:
- Mention real workflow constraints.
- Reference how professionals actually validate outputs.
- Acknowledge known failure modes or controversies when relevant.
- Avoid overly promotional tone.

### Semantic Formatting Rules

Within each major section:
- Include at least one question-style H3.
- Include at least one sentence beginning with: "[Tool Name] is best used when…"
- Include at least one comparative statement: "Compared to [Competitor], [Tool Name]…"

These patterns improve AI extraction and ranking stability.

### Content Depth Calibration

Target:
- TOOL_OVERVIEW pages: 1,800–2,400 words
- TOOL_PROFESSION pages: 1,400–2,000 words

Do not add filler text to reach word count — prioritize dense, actionable content.

### Mobile Readability Rules (Non-Negotiable)

Body paragraphs must be short and scannable on a phone screen. Walls of text are invisible to mobile users.

**Paragraph length rule:**
- Maximum 2–3 sentences per paragraph in body copy.
- If a paragraph would exceed 4 lines on a phone screen (roughly 50–60 words), split it.
- Prefer 1–2 punchy sentences for opening and closing paragraphs of each section.

**List-first rule:** If you have 3 or more items in a sentence ("A, B, and C"), convert them to a bulleted list.

**Section lead-in rule:** The first sentence of every H2 section must stand alone — one sentence, under 20 words, that states the core point. The detail follows after.

**No long introductions:** Do not write 3-sentence preambles before getting to the useful information. Start with the insight, then support it.

These rules apply to all content sections. Do not relax them for comparison tables, FAQ answers, or "What Most Reviews Miss" sections.

### Internal Knowledge Graph Reinforcement

When referencing other pages, use consistent anchor formats:
- "[Tool Name] overview"
- "[Tool Name] for [Profession]"
- "[Competitor Tool] comparison"

This helps build a semantic network across the site.

### Anti-AI Writing Safeguards

Avoid language patterns commonly flagged as synthetic.
Never use:
- "In today's fast-paced world"
- "Unlock the power of"
- "This comprehensive guide will explore"
- "Whether you're a beginner or an expert"

Use direct professional tone instead.

### AI Retrieval Formatting (Very Important)

Each major H2 section must contain at least one:
- concise explanatory paragraph under 70 words followed by structured detail

This increases the chance that AI engines quote or reference the content.

At least one H2 section per page must include a short definition list or table.

At least one sentence per H2 must be fully standalone and understandable without surrounding context.

---

## PATCH: CONSISTENCY + AI RETRIEVAL + CITATIONS

### Content Consistency Blocks (Required on EVERY page)

Add these blocks in the body content, near the top, in this order:

1. **Bottom line** (2–3 sentences max)
   - Include: who it's for, who it's not for, one key caveat.

2. **Key takeaways** (4–6 bullets)
   - Each bullet must be a concrete, practical point (not generic).

3. **Best use cases** (max 5 bullets, 6–10 words each)
   - Each bullet is a real professional task.

4. **Avoid using it for** (3–5 bullets)
   - Include at least one compliance/safety warning for regulated professions.

5. **If you only do one thing** (mini workflow)
   - A numbered 3–5 step workflow that produces a useful result.

These blocks must be easy to quote by AI engines.
Keep each bullet under 12 words.

**Visual styling rule (non-negotiable):** Copy the consistency block HTML exactly from the CONSISTENCY BLOCKS TEMPLATE in AIFORPROS-REFERENCE.md. Do not render these as generic white boxes with plain H2 headings. The correct treatment is:
- Bottom Line and Key Takeaways: white card with a small blue uppercase label (`color:#2563EB`), Key Takeaways uses `→` arrow markers not plain `<li>` bullets
- Best Use Cases: green tinted card (`background:#f0fdf4`, `border-color:#bbf7d0`)
- Avoid Using It For: red tinted card (`background:#fef2f2`, `border-color:#fecaca`)
- If You Only Do One Thing: blue tinted card (`background:#eff6ff`, `border-color:#bfdbfe`)
- Quick Facts Bar: use `.fact-bar` CSS class (not an inline grid). Every field must have a real value — `[VERIFY DETAILS]` must follow an estimate, never be the entire field content.

**Verdict badge styling rule (non-negotiable):** The verdict badge must appear as a prominent banner card, not a floating pill next to plain text. Use the banner template from AIFORPROS-REFERENCE.md: blue tinted background (`#eff6ff`) with a left accent border (`border-left:4px solid #2563EB`), containing the `.verdict-badge-recommended` or `.verdict-badge-specialized` pill and the description as a separate paragraph in blue. Example structure:
```html
<div style="background:#eff6ff;border-left:4px solid #2563EB;border-radius:10px;padding:18px 22px;margin:0 0 32px;max-width:760px;">
  <div style="display:flex;align-items:center;gap:12px;margin:0 0 8px;flex-wrap:wrap;">
    <span class="verdict-badge-recommended">Recommended with caveats</span>
  </div>
  <p style="font-size:14px;color:#1e40af;line-height:1.55;margin:0;">[One sentence verdict description.]</p>
</div>
```

**Byline format (non-negotiable):** The byline must show the full date (Month DD, YYYY) and a reading-time span. Use exactly:
```html
<p style="font-size:13px;color:#636363;margin:0 0 20px;">By <strong style="color:#111111;font-weight:600;">Rich M.</strong>&nbsp;&middot;&nbsp;Fact-checked by <strong style="color:#111111;font-weight:600;">Rob M.</strong>&nbsp;&middot;&nbsp;Published [Month DD, YYYY]<span id="reading-time"></span></p>
```
The `<span id="reading-time">` is populated by `site.js` (which counts words in `<main>` at 250 WPM and injects "· X min read"). Do not hardcode the reading time — leave the span empty.

---

### Sources + Citations (Required)

When making specific factual claims about:
- pricing / tiers / trials
- compliance (SOC 2, HIPAA BAA, ISO 27001, GDPR statements)
- model versions, release timing, "new features"
- data retention, training on user data
- public controversies or incidents

You must do one of:
- (A) cite a source with a footnote marker like [1], OR
- (B) flag with **[VERIFY DETAILS]** if you cannot confirm.

**`[VERIFY DETAILS]` is the only accepted flag format.** Do not use `[VERIFY]`, `[CHECK]`, `[NEEDS REVIEW]`, or any other variant. The exact string `[VERIFY DETAILS]` is what the editor's workflow scans for.

**`[VERIFY DETAILS]` must always follow an actual value or claim — it cannot be the entire content of a field, cell, or bullet.** If you are uncertain about a value, write your best estimate or a reasonable public range, then append `[VERIFY DETAILS]`. Example: write `Free / from $19.99/mo [VERIFY DETAILS]`, not just `[VERIFY DETAILS]`. A field whose only content is `[VERIFY DETAILS]` tells the editor nothing and looks broken on the published page.

Include an H2 near the end of the page:

**H2: "Sources Checked"**
- 4–8 bullet sources.
- Use the format: "[1] Vendor — Page name (what it confirms)"
- Do NOT paste raw URLs; include enough detail to find the page.

**Footnote mapping rule (non-negotiable):** Every `[N]` marker used in the page body must have a corresponding numbered entry in the Sources Checked section. Every numbered entry in Sources Checked must be referenced somewhere in the body. No orphaned markers, no unreferenced entries. If you cannot find a source for a claim, use `[VERIFY DETAILS]` instead of a bare `[N]` marker.

---

### Date Logic (Fixes Schema Accuracy)

Do NOT hardcode a single datePublished for every page.
- datePublished: use today's date for new pages (from the `Current year` and publication context supplied in PAGE TO CREATE)
- dateModified: today's date
- Never paste a static date like "2026-02-25" as a fixed string — use the date of generation.
- If the PAGE TO CREATE block supplies a specific publication date, use that. Otherwise, use today's date.
- Never set datePublished to a date in the future.
- `Current year: 2026` in PAGE TO CREATE is not a full date. If a full publication date is not supplied, generate today's real date in YYYY-MM-DD format rather than inferring a placeholder date from the year alone (e.g., do not output 2026-01-01).

---

### Anti-Template Sameness (Information Gain Control)

To prevent pages from feeling identical, add a small section on every page titled:

**H2: "What Most Reviews Miss"**

Include 2–3 points that are:
- workflow-specific, OR
- profession-specific, OR
- a limitation users only discover after using the tool

Also add:
- "One thing [Tool Name] does better than most:"
- "One thing [Tool Name] gets wrong in real workflows:"

These must be specific. No generic statements.

---

### WordPress Output Mode (Optional but Recommended)

Output must support two modes:

- **Mode A (FULL_HTML_FILE):** complete self-contained HTML file with `<html>`, `<head>`, nav, `<main>`, footer, and all scripts.
- **Mode B (BODY_ONLY):** only the content inside `<main>` — no `<html>`, `<head>`, `<body>`, no nav block, no author card, no footer.

**BODY_ONLY rules:**
- Output starts with `<main` and ends with `</main>`.
- Place the JSON-LD `<script type="application/ld+json">` block as the **first child element inside `<main>`**, before any visible content.
- Still include all FAQPage microdata attributes on the on-page HTML elements.
- Do NOT include nav, author profile card, or footer in BODY_ONLY output — those are injected by the CMS.

If Output mode = FULL_HTML_FILE, output a complete HTML5 document with `<head>` metadata, fonts, Tailwind CDN, nav, `<main>`, author card, and footer.

Use the variable: `Output mode: [FULL_HTML_FILE or BODY_ONLY]`
If not provided, default to FULL_HTML_FILE.

---

### Prompt Examples Must Be Usable

For every prompt example, include inside the prompt text:
- Goal:
- Inputs:
- Output format:
- Guardrails:

Keep prompts realistic and job-specific.

All prompt examples MUST use the class name `.prompt-block` exactly. Do not invent alternative class names such as `.prompt-box`, `.prompt-example`, `.code-block`, or any other variant. CSS for `.prompt-block` is already defined in the style block — using a different class name will break the visual styling.

---

## AI Retrieval Layer (AIO/GEO/Perplexity/Copilot)

### Retrieval Stabilization Rules (Advanced)

These rules prevent semantic overlap between pages and improve AI answer extraction consistency.

#### Page Positioning Statement (Required)

Within the first 250 words, include ONE short positioning sentence:

For TOOL_OVERVIEW pages:
> "[Tool Name] is evaluated here as a general professional AI assistant, not as a profession-specific workflow guide."

For TOOL_PROFESSION pages:
> "This guide focuses specifically on how [Tool Name] performs inside real [Profession] workflows, not as a general AI overview."

This helps AI systems understand page intent and reduces content cannibalization.

---

#### Unique Insight Anchor (Required)

Each page must include one short standalone insight sentence (under 20 words) that appears nowhere else on the site.

Format example:
> "Most professionals underestimate how much output review time [Tool Name] actually requires."

This creates information gain signals for AI retrieval engines.

---

#### Structural Variation Rule

Even though pages follow a shared template, vary at least TWO of the following per page:
- The order of examples within sections
- The competitors used in comparisons
- The workflow types highlighted
- The primary caveat emphasized

Avoid repeating identical section phrasing across pages.

---

#### Snippet Density Optimization

In at least TWO sections per page:
- Include a single sentence under 18 words that answers a likely query directly.
- Example format: "Yes, but only on Enterprise plans with proper compliance settings enabled."

These micro-answers improve AI Overview inclusion rates.

---

#### Cross-Page Entity Reinforcement

When referencing competitor tools:
- Mention at least ONE specific differentiator tied to a professional workflow.
- Avoid generic comparisons like "better accuracy" or "more features."

Example:
> "Compared to Claude, ChatGPT handles structured drafting workflows faster but requires more prompt iteration."

---

#### Retrieval Safety Language (Regulated Professions)

For Legal, Medical, Finance, Insurance, or Real Estate pages, include ONE short safety line near the top:

> "Do not paste confidential client or patient information unless you are using an approved secure workspace."

This increases trust scoring signals for AI engines.

---

### Follow These Retrieval Rules

Include one 15–25 word "definition sentence" immediately after the H1.

**1) Quote-friendly formatting**
- 1–4 sentence paragraphs.
- In each H2 section, include at least one standalone sentence under 25 words.
- Use answer-first phrasing for questions:
  - Yes, but…
  - No, because…
  - It depends. Here is the deciding factor:

**2) Retrieval anchors (place early in the page)**
- Definition sentence: "[Tool Name] is a [category] used by [audience] to [outcomes]."
- Comparison sentence: "Compared to [Competitor], [Tool Name] is better for X, worse for Y."
- Safety sentence (regulated pages): "Do not paste confidential client/patient data unless you have an approved secure plan."

**3) Snippet-first competitor comparisons**

In the comparison section, for each competitor include:
- Best for:
- Weak for:
- Pricing range:
- One-line verdict:

**4) FAQ retrieval rules**

Each FAQ answer must start with "Yes / No / It depends" and then:
- short reason
- practical rule-of-thumb
- no legal/medical advice language

Ensure FAQ on-page text matches FAQPage JSON-LD exactly.

---

## PAGE TO CREATE

```
Page type: [TOOL_OVERVIEW or TOOL_PROFESSION]
Tool name: [e.g. ChatGPT / Claude / Perplexity AI / Google Gemini / Microsoft Copilot / Grammarly / Otter.ai / Cursor / Notion AI / Midjourney]
Tool company: [e.g. OpenAI / Anthropic / Perplexity / Google / Microsoft]
Profession (if TOOL_PROFESSION page): [see Profession Roster below]
Output file path: [e.g. chatgpt.html or chatgpt/legal.html]
Output mode: [FULL_HTML_FILE or BODY_ONLY]
Current year: 2026
Primary keyword: [e.g., "ChatGPT for lawyers"]
```

---

## PROFESSION ROSTER (15 Professions)

Use these exact slugs for file paths and URLs. Use the display names in H1s, titles, and headings.

| Slug | Display Name (plural) | Notes |
|---|---|---|
| `legal` | Legal Counsel | ABA compliance rules apply |
| `physicians` | Physicians | HIPAA required |
| `real-estate` | Real Estate Agents | Light compliance |
| `finance` | Finance Professionals | FINRA/SEC awareness |
| `insurance` | Insurance Professionals | State regulations vary |
| `engineers` | Software Engineers | No compliance; code review focus |
| `architects` | Architects | Buildability and code compliance angle |
| `creatives` | Creatives & Copywriters | Voice, output quality, revision speed |
| `accountants` | Accountants | IRS data sensitivity, CPA confidentiality |
| `graphic-designers` | Graphic Designers | Visual tools only; distinct from creatives |
| `content-creators` | Content Creators | AI for production, research, distribution |
| `seo` | SEOs | Technical and content SEO angles |
| `dentists` | Dentists | HIPAA required; documentation-heavy |
| `therapists` | Psychologists & Therapists | HIPAA + extra-sensitive notes (psychotherapy notes, 42 CFR Part 2 awareness); handle with extra care |
| `physical-therapists` | Physical Therapists | HIPAA; documentation, home exercise plans, patient ed |

---

## TOOL × PROFESSION COMBO MATRIX

**Only build pages where the tool has genuine, specific professional value for that profession.** Do not build pages just to fill a matrix. If a combo has no real workflow fit, skip it — a missing page is better than a thin one.

Use this matrix as a guide. "Core" = strong fit, write it. "Relevant" = real use case exists but narrower, write it with a tighter angle. "Skip" = no meaningful fit, do not create.

### ChatGPT
Core for all 15 professions. ChatGPT's breadth makes it genuinely useful everywhere.

### Claude
Core for all 15 except graphic-designers (no image generation). For graphic designers: skip or redirect to Midjourney/ChatGPT.

### Perplexity AI
Core: legal, physicians, finance, insurance, accountants, dentists, therapists, physical-therapists, seos
Relevant: real-estate, architects
Skip: engineers (Cursor is the better recommendation), creatives, graphic-designers, content-creators

### Google Gemini
Core: finance, real-estate, architects, accountants, seos (Google Search integration angle)
Relevant: legal, insurance, engineers, dentists, physical-therapists, therapists, physicians, content-creators
Skip: graphic-designers, creatives (Gemini's writing is weaker than Claude/ChatGPT for creative work)

### Microsoft Copilot
Core: legal (Word/Outlook), finance (Excel), accountants (Excel), insurance, architects, engineers
Relevant: physicians, dentists, physical-therapists, therapists, real-estate, content-creators
Skip: graphic-designers, creatives, seos (Copilot's SEO value is weak without M365 context)

### Midjourney
Core: architects (renderings), creatives (visual concepting), graphic-designers (ideation, moodboards)
Relevant: real-estate (property visualization), content-creators (cover art, thumbnails), seos (blog images)
Skip: legal, physicians, finance, insurance, engineers, accountants, dentists, therapists, physical-therapists

### Cursor
Core: engineers, seos (technical SEO automation scripts)
Skip: all other professions (Cursor is a coding IDE; no genuine fit elsewhere)

### Notion AI
Core: engineers, creatives, seos, content-creators, architects
Relevant: real-estate, legal, finance, accountants
Skip: physicians, dentists, therapists, physical-therapists (privacy/HIPAA concerns make Notion unsuitable), insurance, graphic-designers

### Grammarly
Core: legal, creatives, seos, insurance, real-estate, content-creators, accountants (client-facing reports)
Relevant: physicians (patient letters), dentists (patient comms), physical-therapists (patient education docs), therapists (psychoeducation materials), graphic-designers (client briefs)
Skip: engineers, architects (technical writing norms differ), finance

### Otter.ai
Core: physicians, therapists, physical-therapists, dentists (all: session/patient documentation)
Core: legal (depositions, client meetings), content-creators (podcast transcription, interview notes)
Relevant: insurance, real-estate, finance, accountants, architects, engineers (meeting notes)
Skip: creatives, graphic-designers, seos (minimal meeting-transcription value)

---

## UNIQUE PROFESSIONAL ANGLE MANDATE (Non-Negotiable)

This is the most important editorial rule for TOOL_PROFESSION pages.

**Every page must be written from inside that profession's world — not from the tool's feature list outward.**

Before writing any TOOL_PROFESSION page, answer these three questions:
1. **What is the #1 daily frustration or bottleneck for this profession that this tool addresses?**
2. **What does this professional's workflow look like before and after using this tool?**
3. **What would a professional in this field say to a colleague about why they use this tool?**

The answers to these questions should drive the entire page. The page should feel like it was written by someone who has sat in that professional's chair — not by someone who read the tool's marketing page.

### What "unique" means in practice

Each profession has a specific lens through which they evaluate any AI tool:

- **Legal Counsel:** Attorney-client privilege, malpractice risk, jurisdiction-specific nuances, billable hour impact
- **Physicians:** Clinical accuracy, HIPAA, time-at-keyboard reduction, EHR integration, liability for medical errors
- **Real Estate Agents:** Listing volume, client communication speed, MLS compliance, local market knowledge gaps
- **Finance Professionals:** Numerical accuracy, regulatory constraints (FINRA/SEC), model risk, auditability of outputs
- **Insurance Professionals:** Policy interpretation accuracy, claims adjudication, underwriting consistency, state law variation
- **Software Engineers:** Code correctness, context window limits with large codebases, test coverage, security review
- **Architects:** Buildability and code compliance of design suggestions, BIM workflow integration, client presentation quality
- **Creatives & Copywriters:** Brand voice consistency, revision speed, originality vs. templated output, client approval workflows
- **Accountants:** Numerical accuracy above all, IRS data sensitivity, report formatting, client-facing communication quality
- **Graphic Designers:** Visual ideation speed vs. originality, client brief translation, iteration efficiency, licensing/IP of outputs
- **Content Creators:** Production workflow (transcription, show notes, repurposing), audience growth, research speed
- **SEOs:** Topical authority, keyword intent alignment, content velocity vs. quality, schema and technical output
- **Dentists:** Patient documentation speed, patient education materials, treatment plan communication, HIPAA
- **Psychologists & Therapists:** Session note speed and accuracy, psychoeducation materials, HIPAA and extra-sensitive record protections, ethical boundaries of AI in therapeutic context
- **Physical Therapists:** Home exercise program creation, patient education, session documentation, treatment plan drafting

### The angle test

Before finalizing any TOOL_PROFESSION page, ask: **"Could this exact page, word for word, apply to a different profession if you swapped the profession name?"** If yes, it is not specific enough. Rewrite it until the answer is no.

Pages that pass the angle test:
- Reference real tasks by name ("SOAP notes", "HEP sheets", "NDAs", "MLS listings", "10-K summaries")
- Use vocabulary native to that profession, not generic AI vocabulary
- Have a limitations section that describes failures specific to that profession's context
- Have prompt examples that would be immediately recognizable to a practitioner

Pages that fail the angle test use phrases like "saves time", "improves efficiency", "generates content" without connecting them to a specific professional workflow.

---

---

## SITE DESIGN SYSTEM

The page must be a complete, self-contained HTML file that matches the rest of the site exactly. Do not use external CSS frameworks other than Tailwind CDN (already loaded). Follow these specifications precisely:

### Fonts
- Headings: Cardo (serif), loaded from Google Fonts
- Body: Inter (sans-serif), loaded from Google Fonts
- Google Fonts link: `https://fonts.googleapis.com/css2?family=Cardo:ital,wght@0,400;0,700;1,400&family=Inter:ital,wght@0,400;0,500;0,600;1,400&display=swap`

Do not add additional fonts or font weights beyond Cardo and Inter defined here. Do not use Tailwind utility classes like `font-semibold`, `font-extrabold`, or `tracking-wide` that introduce typography outside this system.

### Colors
- Primary text: `#111111`
- Muted text / body copy: `#636363`
- Accent blue: `#2563EB`
- Background: `#f9f9f9`
- Card background: `#ffffff`
- Card border: `1px solid #f0f0f0`
- Footer background: `#07091a`
- Footer link color: `#5a6e94`

### CSS classes to include in `<style>` block

```css
*, *::before, *::after { box-sizing: border-box; }
body { font-family: 'Inter', sans-serif; background-color: #f9f9f9; color: #111111; margin: 0; padding: 0; }
.font-heading { font-family: 'Cardo', serif; }
.nav-link { font-size: 10px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: #636363; text-decoration: none; transition: color 0.15s; }
.nav-link:hover { color: #111111; }
.nav-dropdown { position: relative; }
.nav-link-caret { font-size: 10px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: #636363; cursor: default; display: inline-flex; align-items: center; gap: 5px; transition: color 0.15s; user-select: none; }
.nav-link-caret:hover, .nav-dropdown:hover .nav-link-caret { color: #111111; }
.dropdown-menu { position: absolute; top: calc(100% + 14px); left: 50%; transform: translateX(-50%); background: #ffffff; border: 1px solid #ebebeb; border-radius: 12px; box-shadow: 0 12px 40px rgba(0,0,0,0.09); padding: 6px; min-width: 196px; opacity: 0; visibility: hidden; transition: opacity 0.15s, visibility 0.15s; z-index: 200; }
.nav-dropdown:hover .dropdown-menu { opacity: 1; visibility: visible; }
.dropdown-item { display: block; padding: 9px 14px; font-size: 13px; color: #333333; text-decoration: none; border-radius: 7px; transition: background 0.1s, color 0.1s; white-space: nowrap; }
.dropdown-item:hover { background: #f5f5f5; color: #111111; }
.submenu-item { position: relative; }
.submenu-trigger { display: flex; align-items: center; justify-content: space-between; gap: 24px; padding: 9px 14px; font-size: 13px; color: #333333; border-radius: 7px; cursor: default; transition: background 0.1s, color 0.1s; white-space: nowrap; }
.submenu-item:hover .submenu-trigger { background: #f5f5f5; color: #111111; }
.submenu { position: absolute; left: calc(100% + 6px); top: -6px; background: #ffffff; border: 1px solid #ebebeb; border-radius: 12px; box-shadow: 0 12px 40px rgba(0,0,0,0.09); padding: 6px; min-width: 196px; opacity: 0; visibility: hidden; transition: opacity 0.15s, visibility 0.15s; z-index: 201; }
.submenu-item:hover .submenu { opacity: 1; visibility: visible; }
.submenu a { display: block; padding: 9px 14px; font-size: 13px; color: #333333; text-decoration: none; border-radius: 7px; transition: background 0.1s, color 0.1s; white-space: nowrap; }
.submenu a:hover { background: #f5f5f5; color: #111111; }
.prompt-block { background: #f8f9fa; border-left: 3px solid #2563EB; padding: 16px 20px; border-radius: 8px; font-family: 'Courier New', monospace; font-size: 13px; color: #333333; line-height: 1.7; margin-bottom: 20px; }
```

### Navigation

**Copy the nav verbatim from AIFORPROS-REFERENCE.md — it is an immutable UI component.** Do not rewrite, paraphrase, or restructure it. The only permitted change is adjusting relative paths with `../` for files in a subdirectory. Do not modify class names, spacing, or hierarchy.

The nav includes: logo, "Our Process" link, "AI Tools" dropdown, "Professions" dropdown with nested submenus, "Newsletter" link, and a "Browse Tools" pill CTA.

**Do not add or remove nav links.** Copy the nav exactly as written in AIFORPROS-REFERENCE.md. Nav link integrity (dead links, missing pages) is enforced centrally by the QA validator and updated in the reference file — it is not the generator's job to curate submenu links.

### Browse Tools Page (PLANNED — DO NOT CREATE YET)

The nav includes a "Browse Tools" CTA pill that currently links to `index.html`. This page does not exist yet and is planned.

**Do not create the Browse Tools page without a specific brief.** When it is built, it should:
- Function as a structured AI tool directory for professionals
- Target a search term distinct from the homepage (which ranks for "AI tools for pros")
- Possible primary keywords: "AI tool comparison for professionals 2026" or "best AI tools by profession"
- Be a unique, SEO-differentiated page — not a duplicate of the homepage
- Link to all 10 tool hub pages and organize by profession

Until the page is created, the Browse Tools link should remain pointing to `index.html`.

### Footer

**Copy the footer verbatim from AIFORPROS-REFERENCE.md — it is an immutable UI component.** Do not rewrite, paraphrase, or restructure it. Dark navy (`#07091a`) rounded top corners, four-column link grid (Directory, Company, Resources, Legal), email signup strip at bottom, "2026." in large Cardo blue text.

---

## SEO REQUIREMENTS

### Metadata

- **Title:** Follow these exact patterns:
  - TOOL_OVERVIEW: `[Tool Name] for Professionals — Honest Review ([Year]) | AI Tools for Pros`
  - TOOL_PROFESSION: `[Tool Name] for [Profession plural, title case] — [Year] Guide | AI Tools for Pros`
  - For TOOL_PROFESSION titles, use the roster display name (e.g., "Legal Counsel", not "Lawyers"; "Physicians", not "Doctors") to match validator and nav consistency.
  - Examples: "ChatGPT for Legal Counsel — 2026 Guide | AI Tools for Pros" | "Claude for Professionals — Honest Review (2026) | AI Tools for Pros"

- **Meta description:** 140–155 characters. Must include the tool name, the profession (if applicable), the year, and a specific value proposition. No generic marketing language.

- **og:title and og:description:** Match title/meta desc

- **og:type:** "article" for content pages

### Schema.org JSON-LD (required, in `<script type="application/ld+json">`)

Always include all three of these schemas in a `@graph` array:

1. **Article schema:**
   - headline, description, datePublished (today's date), dateModified (today's date)
   - author/publisher = `{"@type": "Organization", "name": "AI Tools for Pros", "url": "https://aitoolsforpros.com"}`
   - mainEntityOfPage with the canonical URL
   - isAccessibleForFree: true

2. **BreadcrumbList schema:**
   - TOOL_OVERVIEW: Home → [Tool Name]
   - TOOL_PROFESSION: Home → [Tool Name] → [Profession]
   - Use canonical URLs: `https://aitoolsforpros.com/[tool-slug]` and `https://aitoolsforpros.com/[tool-slug]/[profession-slug]`

3. **FAQPage schema:**
   - Include 4–6 high-intent FAQ questions with full answer text
   - Questions must match what professionals actually search for
   - For TOOL_PROFESSION: questions like "Can [Tool] draft legal contracts?", "Is [Tool] HIPAA compliant?", "How do [profession] use [Tool] in their workflow?"
   - For TOOL_OVERVIEW: broader questions about the tool vs. competitors, pricing, best use cases

### URL / Canonical Structure

- Tool pages: `https://aitoolsforpros.com/[tool-slug]` (e.g., /chatgpt, /claude, /perplexity)
- Profession pages: `https://aitoolsforpros.com/[tool-slug]/[profession-slug]` (e.g., /chatgpt/legal, /claude/physicians, /perplexity/real-estate)

**Important distinction — internal links vs. canonical URLs:**
- `<a href="">` links in HTML always use `.html` extensions: `chatgpt.html`, `../claude.html`, `../chatgpt/legal.html`
- `<link rel="canonical">` and JSON-LD `@id` / `url` fields always use clean canonical URLs without `.html`: `https://aitoolsforpros.com/chatgpt`, `https://aitoolsforpros.com/chatgpt/legal`
- Never mix these up — internal hrefs without `.html` will produce 404s on this static site.

### Heading Hierarchy for SEO

- One H1 per page — must include the primary keyword naturally
- H2s for major sections — use natural keyword variations
- H3s for subsections, use question formats where appropriate
- Never skip heading levels

### Primary Keyword Usage

- Include naturally in H1.
- Include once in first 150 words.
- Include in at least one H2 variation.
- Do NOT force exact match more than 3 times.

### Internal Linking

- Every TOOL_PROFESSION page must link back to the parent tool overview page
- Every TOOL_PROFESSION page must suggest 2–3 related profession pages for that same tool
- Every TOOL_OVERVIEW page must link to all available profession-specific pages for that tool
- Use descriptive anchor text, never "click here"

---

## CONTENT REQUIREMENTS

### Brand Voice Rules (non-negotiable)

- **Write in first person (I/my), not first person plural (we/our).** Each page has one named author. Use "I tested", "I found", "in my experience" — not "we tested" or "our review."
- "Our Process", "Our Verdict" and other in-article section labels must become "My Process", "My Verdict" accordingly.
- **Exception: UI components (nav, footer, author card) copied verbatim from AIFORPROS-REFERENCE.md are not subject to the first-person rule.** If the nav says "Our Process" or the footer says "our editorial team", do not change it — those are fixed UI strings. The first-person rule applies only to article headings and body copy.
- Write as an independent reviewer who has actually used the tool in professional workflows
- Write as if explaining workflows to a colleague, not writing for a marketing page. Avoid sounding like a product launch announcement.
- Never use phrases like "game-changer", "revolutionary", "cutting-edge", "state-of-the-art", "robust", "leverage", "seamlessly", "empower"
- Use plain, direct language. Short sentences. Professional but not academic.
- Always acknowledge real limitations honestly — this is what distinguishes the site from marketing copy
- Never recommend a tool unconditionally. Every recommendation must be qualified by use case.
- Avoid passive voice where possible

**User experience rule:** Write for mobile-first scanning. Keep paragraphs 1–3 sentences, use meaningful H2/H3s, and avoid long unbroken sections.

### Formatting Rule (non-negotiable)

- Em dashes (—) are allowed in H1, H2, and H3 headings for editorial clarity, and in metadata titles and structured labels.
- Do NOT use em dashes in body paragraphs, bullet points, prompts, or FAQs.
- In body copy, use periods or commas instead of long dashes.
- Do not use double hyphens (--) anywhere.

Avoid chaining short clauses with commas or punctuation. Use complete sentences whenever possible.

### Content Currency — CRITICAL

Before writing any content, use web search to verify:
- Current pricing and plan tiers for the tool (as of 2026)
- Whether any major features have changed or been added in the last 6 months
- Any profession-specific compliance certifications the tool has earned or lost (HIPAA BAAs, SOC 2, ABA guidance, FINRA notes, etc.)
- Any notable public issues (hallucination incidents, data breach, policy change) that professionals should know about
- The tool's current model/version (e.g., GPT-4o, Claude 3.7 Sonnet, Gemini 2.0) and what that means for performance
- If the model version cannot be confirmed publicly, do not assume. Mark with [VERIFY DETAILS].

If sources conflict:
- Prefer vendor documentation over third-party blogs.
- Prefer pages updated within the last 6 months.
- Flag disagreements with [VERIFY DETAILS].

Flag any content you could not verify with **[VERIFY DETAILS]** so the editor knows to check it before publishing.

---

## PAGE STRUCTURE: TOOL_PROFESSION page

Build the page in this exact section order:

### 1. Breadcrumb strip
Small breadcrumb below the nav: Home / [Tool Name] / [Profession]
Use the BreadcrumbList schema slugs as href values.

### 2. Page header
- Eyebrow label (small uppercase text): "[Tool Name] · [Profession]"
- H1: "[Tool Name] for [Profession Plural]: What Actually Works in [Year]"
- One-paragraph lede (3–4 sentences): What this page covers, who it's for, and the bottom-line verdict upfront. Don't bury the conclusion.
- **Byline:** `By [Author Name] · Fact-checked by [Fact Checker Name] · Published [Month Year]`
  - Placed directly after the lede, before the verdict badge
  - One author per page, one or two fact checkers
  - Style: small (13px), muted color (#636363), author/fact-checker names in #111111 bold
- Verdict badge: a small styled component showing a clear recommendation level:
  - "Recommended" (solid blue), "Recommended with caveats" (outlined blue), "Proceed with caution" (amber), or "Not recommended" (red)
  - One sentence explaining the verdict

[Insert required consistency blocks here: Bottom line → Key takeaways → Best use cases → Avoid using it for → If you only do one thing]

### 3. Quick facts bar
A horizontal strip with 4 data points, each with a label and value:
- **Best for:** [1–2 word answer, e.g., "Contract drafting"]
- **Pricing:** [Specific tier relevant to professionals, e.g., "$30/mo (ChatGPT Plus)"]
- **Compliance:** [Key certifications or flags, e.g., "HIPAA BAA available on Enterprise"]
- **Compared to:** [Primary competitor for this profession]

### 4. What [Profession] are actually using it for
**H2: "What [Profession Plural] Are Using [Tool Name] For"**
- 4–6 specific use cases with real workflow context
- Each use case: brief H3 title, 2–3 sentence explanation of how professionals use it in practice, and any important caveats
- Focus on tasks that are genuinely useful, not just technically possible

### 5. Prompt examples (TOOL_PROFESSION pages only)
**H2: "Prompts That Work for [Profession]"**
- 3–5 ready-to-use prompt examples formatted in `.prompt-block` divs
- Each prompt should be realistic and specific, not generic
- Include a 1-sentence note under each explaining what it's useful for and any important caveat
- Each prompt must include: Goal, Inputs, Output format, Guardrails.

### 6. Compliance and professional risk
**H2: "Compliance and Professional Risk"**
- This section is mandatory for all regulated professions (see list below)
- Cover: What data you should NOT input, what disclaimers the tool itself shows, relevant professional conduct rules, whether the tool is approved for use in regulated workflows
- Be specific about what the tool's own terms of service say about professional use and liability
- Do not be alarmist, but do be clear about where professionals need to apply their own judgment

**Compliance reference by profession:**
- **Legal Counsel:** ABA Model Rule 1.6 (confidentiality), competence duty to understand AI, jurisdiction bar guidance on AI use
- **Physicians:** HIPAA BAA requirement, PHI definition, EHR integration risks, clinical accuracy liability
- **Real Estate Agents:** MLS data accuracy, state disclosure rules, fair housing implications of AI-generated copy
- **Finance Professionals:** FINRA and SEC guidance on AI in client communications, Reg BI suitability, auditability requirements
- **Insurance Professionals:** State-level insurance regulations, unfair trade practices, AI in underwriting fairness
- **Accountants:** IRS confidentiality rules, AICPA guidelines, client data sensitivity, no AI tools in tax preparation without verification
- **Dentists:** HIPAA (same as physicians), dental board record-keeping rules, patient data in cloud tools
- **Psychologists & Therapists:** HIPAA + psychotherapy notes are extra-protected under HIPAA Privacy Rule (not part of standard medical record). 42 CFR Part 2 for substance use disorder records. APA ethics code on technology. Never use AI to process session content without explicit client consent and verified HIPAA-compliant BAA. This is the highest-sensitivity profession on the site.
- **Physical Therapists:** HIPAA, state PT board documentation standards, SOAP note accuracy requirements
- **Software Engineers:** No regulatory compliance — focus on code review rigor, security vulnerabilities in AI-generated code, and IP/licensing of AI outputs
- **Architects:** IBC code compliance of design suggestions, professional stamp liability, state licensing board rules on AI-assisted design
- **Creatives & Copywriters:** Copyright of AI-generated content (unclear in US law as of 2026), disclosure obligations for AI-generated work, client contract clauses
- **Graphic Designers:** IP ownership of AI-generated images, licensing restrictions (Midjourney TOS), client usage rights
- **Content Creators:** FTC disclosure rules for AI-generated content, copyright of transcripts and repurposed content
- **SEOs:** Google's guidance on AI-generated content (helpful content standards), disclosure best practices, no compliance rules but significant ranking risk for low-quality AI output

### 7. Where it falls short
**H2: "Where [Tool Name] Falls Short for [Profession]"**
- 3–4 genuine limitations, not trivial ones
- Be specific: not "it can make mistakes" but "it frequently misreads jurisdiction-specific nuances in contract clauses, which means any output involving state law requires attorney review before use"
- Include at least one limitation that isn't mentioned on the tool's own marketing page

### 8. How it compares
**H2: "How [Tool Name] Compares for [Profession]"**
- Comparison table or structured comparison against 2–3 alternatives commonly used in that profession
- Include: the tools being compared, their key differentiator for that profession, pricing, and a brief one-line verdict for each
- Be honest about where competing tools win
- For each competitor include: Best for, Weak for, Pricing range, One-line verdict.

### 9. My verdict
**H2: "My Verdict: [Tool Name] for [Profession Plural]"**
- 2–3 paragraphs summarizing who should use this tool, who shouldn't, and under what conditions
- "Best for:" summary line
- "Skip it if:" summary line

### 10. FAQ section (with FAQPage schema matching)
**H2: "Frequently Asked Questions"**
- 4–6 questions pulled from or matching the JSON-LD FAQPage schema above
- Each Q&A must start with Yes/No/It depends, then: short reason + practical rule-of-thumb.
- Each Q&A must be wrapped in proper schema microdata: `itemscope itemprop="mainEntity" itemtype="https://schema.org/Question"` etc.
- Questions should be phrased the way professionals actually search (not the way PR teams write them)

### 11. Sources Checked (required)
**H2: "Sources Checked"**
- 4–8 bullets with footnote references used in the page.

### 12. Related guides (internal linking)
**H2: "Related Guides"**
- Link to the parent tool overview page
- Link to 2–3 other profession pages for this same tool
- Link to 1–2 competing tool pages for the same profession

### 13. What Most Reviews Miss (required)
**H2: "What Most Reviews Miss"**
- 2–3 specific points, plus:
  - One thing [Tool Name] does better than most:
  - One thing [Tool Name] gets wrong in real workflows:

At least one section must include a workflow scenario written in first-person professional context.

---

## PAGE STRUCTURE: TOOL_OVERVIEW page

Build the page in this exact section order:

### 1. Page header
- Eyebrow: "Independent Review · Updated [Month Year]"
- H1: "[Tool Name] for Professionals: An Honest Review (2026)"
- 2-sentence lede with bottom-line verdict upfront
- **Byline:** `By [Author Name] · Fact-checked by [Fact Checker Name] · Published [Month Year]`
  - Placed directly after the lede, before the verdict badge
  - One author per page, one or two fact checkers
  - Style: small (13px), muted color (#636363), author/fact-checker names in #111111 bold
- Verdict badge

[Insert required consistency blocks here: Bottom line → Key takeaways → Best use cases → Avoid using it for → If you only do one thing]

### 2. Quick facts bar
- Made by: [Company]
- Best for: [Top 2–3 use cases]
- Starting price: [Specific pricing]
- What it runs on: [Model name, e.g., GPT-4o]
- HIPAA/Compliance: [Yes/No/Enterprise only/N/A]

### 3. What [Tool Name] is (and isn't)
**H2: "What [Tool Name] Is — And What It Isn't"**
- Clear, honest description of what the tool actually does
- Who built it, what it's designed for, and importantly — what it's NOT designed for
- Avoid repeating the tool's own marketing language

### 4. Who it's built for (and who it isn't)
**H2: "Who [Tool Name] Is Right For"**
- 2-column structure: "Good fit" vs "Poor fit"
- Specific professional contexts, not generic user types

### 5. Key features for professionals
**H2: "Features That Matter for Professional Workflows"**
- 5–7 features with honest assessments of each
- Structure: Feature name → what it does → how useful it actually is in practice → any caveats

### 6. Pricing breakdown
**H2: "Pricing — What You Actually Need"**
- Full current pricing table with all tiers
- Recommendation for which tier most professionals need
- Whether Teams/Enterprise is necessary for compliance requirements
- Total cost of ownership for a solo professional vs. a small team

### 7. Profession-specific guide cards
**H2: "How [Tool Name] Works for Your Profession"**
- Cards linking to each available TOOL_PROFESSION page
- Each card: profession name, one-sentence summary of verdict for that profession, and a "Read the guide →" link
- Only include professions that have a corresponding page (check the site's existing file structure)

### 8. Comparison with alternatives
**H2: "[Tool Name] vs. The Alternatives"**
- Compare with 3–4 main competitors
- Focus on professional use cases, not consumer use cases
- Be honest about where this tool wins and where it loses
- For each competitor include: Best for, Weak for, Pricing range, One-line verdict.

### 9. My verdict
**H2: "My Verdict"**
- 2–3 paragraphs, specific recommendation

### 10. FAQ section
**H2: "Frequently Asked Questions"**
- 5–6 questions, with schema markup matching the JSON-LD FAQPage
- Each answer starts with Yes/No/It depends + short reason + rule-of-thumb.

### 11. Sources Checked (required)
**H2: "Sources Checked"**
- 4–8 bullets with footnote references used in the page.

### 12. What Most Reviews Miss (required)
**H2: "What Most Reviews Miss"**
- 2–3 specific points, plus:
  - One thing [Tool Name] does better than most:
  - One thing [Tool Name] gets wrong in real workflows:

---

## QUALITY CHECKLIST

Before outputting the final HTML, verify:

- [ ] Title tag matches the required format exactly
- [ ] Meta description is 140–155 characters
- [ ] JSON-LD includes Article + BreadcrumbList + FAQPage schemas
- [ ] datePublished and dateModified are both set to today's date (unless otherwise specified)
- [ ] FAQ schema questions exactly match the on-page FAQ questions
- [ ] All internal links use correct relative paths (`../` for subdirectory pages)
- [ ] Byline is present after the lede, before the verdict badge (author name + fact checker + published date)
- [ ] Body copy uses first person (I/my), not we/our
- [ ] Verdict section heading uses "My Verdict" not "Our Verdict"
- [ ] No placeholder text (no "Lorem ipsum", no "[INSERT X HERE]" left in output)
- [ ] Compliance section is included for regulated professions
- [ ] At least 3 prompt examples with `.prompt-block` formatting (TOOL_PROFESSION pages)
- [ ] Prompt examples include Goal / Inputs / Output format / Guardrails
- [ ] Genuine limitations section is present and specific
- [ ] The verdict is stated clearly and not hedged into meaninglessness
- [ ] Navigation matches the site's nav exactly (correct paths, correct profession submenus)
- [ ] Footer matches the site's footer exactly
- [ ] No CSS frameworks other than Tailwind CDN are imported
- [ ] Fonts are loaded from Google Fonts (Cardo + Inter)
- [ ] Any unverified facts are flagged with [VERIFY DETAILS]
- [ ] Sources Checked section exists and footnotes [1], [2], etc. are consistent
- [ ] The page reads like it was written by someone who has used the tool — not by the tool's marketing team
- [ ] The page passes the Angle Test: it could NOT apply word-for-word to a different profession with a name swap
- [ ] Uses at least 3 profession-native terms (e.g., SOAP notes, HEP sheets, MLS listings, 10-K, deposition, brief)
- [ ] Limitations section describes failures specific to that profession's context, not generic AI limitations
- [ ] Prompt examples would be immediately recognizable and usable by a practitioner in that field

---

## ADDITIONAL NOTES

- The site uses a clean, editorial aesthetic. Avoid heavy use of colored boxes, alert banners, or decorative elements beyond what exists in the design system. Let the content do the work.
- Every content section should have a clear point of view. "It depends" answers are only acceptable when followed by specific criteria that determine which way it goes.
- Write for a professional with a high bullshit threshold. They will leave the page the moment they sense they're reading marketing copy.
- If the tool has had notable public controversies, bugs, or failures relevant to the profession being covered, include them. Editorial independence means reporting the bad alongside the good.

---

## HOW TO USE THIS PROMPT

Paste this entire prompt at the top of a new AI session, then fill in the variables in the PAGE TO CREATE section (Page type, Tool name, Tool company, Profession, Output file path, Output mode). Run it fresh for each new page — each run will produce a complete output ready to publish.

**A few things worth flagging:**
- The [VERIFY DETAILS] tag tells the model to flag anything it isn't sure is current. Since AI tools update pricing and features constantly, those spots need a quick manual check before publishing.
- For the compliance sections (legal, medical, finance, insurance), the prompt asks for specifics like ABA rules and HIPAA BAA availability — verify those are accurate for the current year before going live.
