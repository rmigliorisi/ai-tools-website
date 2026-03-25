# AI Tools for Pros — Page Validator (Claude Code)

You are validating a newly generated HTML page for aitoolsforpros.com before it is written into the repo.

You have local file access. Use it.

INPUTS I WILL PASTE INTO CHAT (in this order):
1) PAGE VARIABLES
2) GENERATED HTML

YOUR JOB:
A) Validate the page against AIFORPROS.md + AIFORPROS-REFERENCE.md rules.
B) Validate against the CURRENT repo state (existing page paths, nav constraints).
C) Return a clear PASS/FAIL report + exact fixes.
D) If FAIL, output a corrected HTML (full replacement) that preserves content but fixes compliance issues.

---

## Step 0 — Read the repo context (required)

1) Locate and read these reference files in the repo (or ask for their path if missing):
   - `/Users/rmigs/Projects/AIFORPROS.md`
   - `/Users/rmigs/Projects/AIFORPROS-REFERENCE.md`

2) Build an "Existing Page Paths List" automatically:
   - Recursively scan for .html pages in `/Users/rmigs/Projects/` (exclude node_modules, .git, dist artifacts if any).
   - Store the set of relative paths like:
     - `chatgpt.html`
     - `chatgpt/legal.html`
     - `gemini/finance.html`
   - You will use this list to validate nav links + related guides links.

If scanning fails for any reason, report exactly what failed and ask for the paths list to be pasted manually.

---

## Step 1 — Parse PAGE VARIABLES (required)

From PAGE VARIABLES extract:
- Page type (TOOL_OVERVIEW or TOOL_PROFESSION)
- Tool name + tool slug
- Profession display + profession slug (if applicable)
- Output file path
- Output mode (FULL_HTML_FILE or BODY_ONLY)
- Primary keyword
- Current year
- Publication date: use the `Publication date` field if supplied. Otherwise use today's real date in YYYY-MM-DD format.

---

## Step 2 — Hard structural requirements (FAIL if any break)

### 2.1 Output mode envelope
- If FULL_HTML_FILE:
  - Must include `<!DOCTYPE html>`, `<html>`, `<head>`, `<body>`.
  - Must include Tailwind CDN + Google Fonts (Cardo + Inter) exactly as specified in AIFORPROS-REFERENCE.md.
- If BODY_ONLY:
  - Output must start with `<main` and end with `</main>`.
  - The JSON-LD `<script type="application/ld+json">` must be the FIRST child inside `<main>`.

### 2.2 Immutable UI components (NAV + FOOTER + AUTHOR CARD + HEAD BLOCK)
- NAV, FOOTER, AUTHOR PROFILE CARD, and HEAD BLOCK structure are immutable — do not rewrite them.
- PASS pages that include these blocks verbatim (modulo allowed path adjustments).
- NAV must match AIFORPROS-REFERENCE.md verbatim for that page type.
- FOOTER must match AIFORPROS-REFERENCE.md verbatim for that page type.
- AUTHOR PROFILE CARD must match AIFORPROS-REFERENCE.md verbatim.
- HEAD BLOCK (Tailwind CDN, Google Fonts, meta tags structure) must match AIFORPROS-REFERENCE.md verbatim.
- Allowed change: ONLY relative path adjustments with `../` when the page is in a subdirectory.
- Exception: `<link rel="canonical">` may be present or inserted in `<head>` (it is now part of the TOOL_PROFESSION HEAD BLOCK reference). The canonical href must be a clean URL with no `.html`. No other head additions are allowed.
- If any other deviation exists, FAIL and replace with the exact reference versions.

### 2.3 Nav link integrity
- Every link in the nav professions submenus must correspond to a file that exists in the repo.
- If any nav link is dead, FAIL and report:
  - Which link is dead
  - Whether the fix is (a) create the missing page or (b) remove the link from the central nav reference
- Do NOT invent nav links to pages that do not exist.

---

## Step 3 — SEO + schema validation (FAIL on hard breaks)

### 3.1 Title + meta description
- Title must match required pattern exactly:
  - TOOL_OVERVIEW: `[Tool Name] for Professionals — Honest Review (2026) | AI Tools for Pros`
  - TOOL_PROFESSION: `[Tool Name] for [Profession Plural] — 2026 Guide | AI Tools for Pros`
- For TOOL_PROFESSION, use the canonical profession display name from the roster (e.g., "Legal Counsel", not "Lawyers"; "Physicians", not "Doctors"). Do NOT fail a page solely because it uses the roster name rather than a common-language plural.
- Meta description length: 140–155 characters.
- og:title and og:description must match title/meta description.
- og:type must be `"article"`.

### 3.2 Canonical + internal href rules
- `<link rel="canonical">` must use clean URL WITHOUT `.html`:
  - `https://aitoolsforpros.com/[tool-slug]` or `/[tool-slug]/[profession-slug]`
- Internal `<a href="">` links MUST use `.html` extensions and correct `../` prefixes.
- Never mix these up — internal hrefs without `.html` produce 404s on this static site.

### 3.3 JSON-LD graph requirements
JSON-LD must contain a `@graph` array with all three:
1. **Article** — headline, description, datePublished, dateModified, author, publisher, mainEntityOfPage, isAccessibleForFree: true
2. **BreadcrumbList** — correct depth for page type (TOOL_PROFESSION: Home → Tool → Profession; TOOL_OVERVIEW: Home → Tool)
3. **FAQPage** — 4–6 entries, questions must match on-page FAQ text exactly

Date check (hard fail):
- datePublished and dateModified must be a real, specific date in YYYY-MM-DD format.
- FAIL immediately if either value contains any of: `[`, `]`, `TODAY`, `e.g.`, or the literal string `2026-02-25` — UNLESS PAGE VARIABLES explicitly set `Publication date: 2026-02-25`, in which case that date is intentional and must PASS.
- Must NOT be `2026-01-01` or any other year-derived placeholder.
- Must NOT be a future date.

Bracketed placeholder check (hard fail):
- FAIL if the JSON-LD block contains ANY unreplaced bracketed placeholder, including: `[tool-slug]`, `[profession-slug]`, `[Tool Name]`, `[Profession Plural]`, `[Profession Display Name]`, `[FAQ Question`, `[Answer`, `[Same as`, `[140`, or any `[...]` pattern.
- These are catastrophic: they break schema parsers and appear in search previews.

Author/Publisher check:
- Treat AIFORPROS-REFERENCE.md as canonical for Article author/publisher boilerplate.
- Do NOT fail a page for using `{"@type": "Person", "name": "Rich M."}` vs `{"@type": "Organization", ...}` as the Article author — both appear in the reference and either is acceptable.
- Still enforce: `@graph` contains all three schemas (Article, BreadcrumbList, FAQPage), canonical `@id` is a clean URL without `.html`, and dates are real today's dates.

Footnote mapping check:
- Every `[N]` marker in the body must have a matching numbered entry in Sources Checked.
- Every numbered entry in Sources Checked must be referenced by at least one `[N]` in the body.
- No orphaned markers. No unreferenced sources.

---

## Step 4 — Content rules (FAIL on these)

### 4.1 First-person rule
Body copy must use I/my. No "we/our/us" except inside immutable UI components copied verbatim from AIFORPROS-REFERENCE.md (nav, footer, author card).

Scanning scope: check only visible article content inside `<main>`. Exclude `<script>` blocks (including JSON-LD), nav, footer, and author card. A naive full-document scan will produce false positives from those components.

### 4.2 Dash rules
- No double hyphens (`--`) anywhere in visible article content inside `<main>` (exclude `<script>` blocks and immutable UI components).
- No em dashes in body paragraphs, bullets, prompts, or FAQs.
- Em dashes allowed ONLY in H1/H2/H3 headings and `<title>`.

### 4.3 Required consistency blocks
Near the top, in this exact order:
1. Bottom line (2–3 sentences)
2. Key takeaways (4–6 bullets, each under 12 words)
3. Best use cases (max 5 bullets, 6–10 words each)
4. Avoid using it for (3–5 bullets; at least one compliance/safety warning for regulated professions)
5. If you only do one thing (3–5 numbered steps)

### 4.4 Required retrieval anchors
- Immediately after H1: a 15–25 word definition sentence.
- Within first 250 words: page positioning statement:
  - TOOL_OVERVIEW: "evaluated here as a general professional AI assistant…"
  - TOOL_PROFESSION: "focuses specifically on how [Tool] performs inside real [Profession] workflows…"
- For regulated professions (Legal, Medical, Finance, Insurance, Real Estate, Physicians, Accountants, Dentists, Psychologists & Therapists, Physical Therapists): a safety sentence near the top is required. Accept either of these two variants — both are correct:
  - (A) "Do not paste confidential client or patient information unless you are using an approved secure workspace."
  - (B) "Do not paste confidential client/patient data unless you have an approved secure plan."
  - FAIL if neither variant is present on a regulated-profession page.

### 4.5 Section order
Validate H2 order exactly for the page type per AIFORPROS.md:

Between the page header and the first H2, the page may include the consistency blocks and Quick Facts Bar — these are layout components, not H2s, and should be ignored when validating H2 order.

TOOL_PROFESSION order:
1. (Page header — not an H2)
2. What [Profession] Are Using [Tool] For
3. Prompts That Work for [Profession]
4. Compliance and Professional Risk
5. Where [Tool] Falls Short for [Profession]
6. How [Tool] Compares for [Profession]
7. My Verdict: [Tool] for [Profession]
8. Frequently Asked Questions
9. Sources Checked
10. Related Guides
11. What Most Reviews Miss

Quick Facts Bar placement: the Quick Facts Bar is a layout component, not an H2. It must appear after the consistency blocks and before the first H2 ("What [Profession] Are Using [Tool] For"). Do NOT require it to be wrapped in an H2 heading.

TOOL_OVERVIEW order:
1. (Page header — not an H2)
2. What [Tool] Is — And What It Isn't
3. Who [Tool] Is Right For
4. Features That Matter for Professional Workflows
5. Pricing — What You Actually Need
6. How [Tool] Works for Your Profession
7. [Tool] vs. The Alternatives
8. My Verdict
9. Frequently Asked Questions
10. Sources Checked
11. What Most Reviews Miss

### 4.6 Prompt blocks (TOOL_PROFESSION only)
- 3–5 prompts required.
- Each prompt must be in a `<div class="prompt-block">` — exact class name, no variants.
- Each prompt must include: Goal, Inputs, Output format, Guardrails.
- Each prompt must have a 1-sentence explanatory note outside the prompt block.

### 4.7 "What Most Reviews Miss" section
Must include:
- 2–3 specific points (workflow-specific or profession-specific, not generic)
- "One thing [Tool Name] does better than most:" line
- "One thing [Tool Name] gets wrong in real workflows:" line
- At least one first-person workflow scenario

### 4.8 Byline
Must appear directly after the lede paragraph, before the verdict badge.

**Required format:** The byline must show the full date (Month DD, YYYY) and include `<span id="reading-time"></span>` for the JS-injected reading time. Required structure:

```html
<p style="font-size:13px;color:#636363;margin:0 0 20px;">By <strong style="color:#111111;font-weight:600;">Rich M.</strong>&nbsp;&middot;&nbsp;Fact-checked by <strong style="color:#111111;font-weight:600;">Rob M.</strong>&nbsp;&middot;&nbsp;Published [Month DD, YYYY]<span id="reading-time"></span></p>
```

FAIL if:
- The date is month+year only (e.g., "February 2026") — must be "February 25, 2026" or equivalent full date.
- The `<span id="reading-time">` is missing.

PASS if the byline matches the above structure with a real full date.

**Legacy exception:** Pages generated before this rule was added may use "Published February 2026" without the span. WARN rather than FAIL for these legacy pages, and note the update needed.

---

## Step 5 — Verification flags and citations

For factual claims about pricing, compliance certifications (SOC 2, HIPAA BAA, ISO, GDPR), model versions, data retention, or public controversies:
- Either cite with a footnote like `[1]` tied to a Sources Checked entry, OR
- Flag with `[VERIFY DETAILS]`

**`[VERIFY DETAILS]` is the only accepted uncertainty marker.** Any other form (`[VERIFY]`, `[CHECK]`, `[NEEDS REVIEW]`, etc.) is a FAIL — replace with `[VERIFY DETAILS]`.

**`[VERIFY DETAILS]` as sole field content — WARN:** If `[VERIFY DETAILS]` is the entire visible content of a table cell, Quick Facts field value, or bullet (no preceding text or value), that is a soft WARN. The flag must follow an actual claim or value. Flag the specific location and note: "Needs a value or estimate before the flag — e.g., `Free / from $19.99/mo [VERIFY DETAILS]` not just `[VERIFY DETAILS]`."

Sources Checked format and numbering rules:
- Format: `[N] Vendor — Page name (what it confirms)`. No raw URLs.
- **If the page body uses `[1]`, `[2]`, etc. footnote markers:**
  - Every `[N]` in the body must have a matching numbered entry in Sources Checked.
  - Every numbered entry in Sources Checked must be referenced by at least one `[N]` in the body.
  - No orphaned markers. No unreferenced entries.
- **If the page body uses NO `[N]` markers:**
  - Sources Checked must NOT contain numbered `[N]` entries. Use unnumbered bullets (plain dashes) instead, or rely on `[VERIFY DETAILS]` flags.
  - A Sources Checked section with numbered entries but no corresponding body markers is a FAIL.

---

## Step 6 — Soft checks (WARN, do not FAIL)

- Word count:
  - TOOL_OVERVIEW: 1,800–2,400 words
  - TOOL_PROFESSION: 1,400–2,000 words
  - If out of range, WARN. Do not FAIL unless it looks padded or thin.
- At least 3 sections contain bullets, steps, or a definition list/table.
- At least one H2 contains a short definition list or table.
- In at least 2 sections: at least one sentence under 18 words answering a likely query directly.
- No placeholder text left in output (no "Lorem ipsum", no "[INSERT X HERE]", no `[BRACKETED]` values).

### 6.1 Mobile readability check (WARN)

Scan body `<p>` tags for paragraph length violations:
- WARN if any body paragraph exceeds 60 words (roughly 4+ lines on a phone).
- WARN if any H2 section's opening paragraph exceeds 25 words (opening sentence must be short and declarative).
- WARN if 3 or more items appear in a single sentence list ("A, B, and C, and D...") that should be a `<ul>` list.
- Do NOT fail on these — they are content quality signals. List the offending paragraphs (first 10 words + word count) and recommend splitting.

---

## Step 7 — Report format (required)

Return in this exact structure:

```
STATUS: PASS or FAIL

SUMMARY (5–10 bullets):
- ...

FAILURES (if any), grouped by category:

  Immutable UI:
  - ...

  SEO / Schema:
  - ...

  Content Structure:
  - ...

  Style Rules:
  - ...

  Citations / Verify:
  - ...

WARNINGS (soft checks):
- ...

EXACT FIXES:
  [Section or line reference] → [Replacement text]

CORRECTED HTML (if FAIL):
  [Full corrected file — same output mode as PAGE VARIABLES]
```

---

## Behavior rules (non-negotiable)

- Do not invent nav links to pages that do not exist in the repo.
- Do not change immutable UI copy (nav, footer, author card) other than path adjustments.
- If the ONLY failure is a dead nav link, output FAIL + report only. Do NOT output a corrected HTML with the nav link removed — nav is centrally managed via AIFORPROS-REFERENCE.md. The fix is either (a) create the missing page or (b) remove the link from the central nav reference, not a local patch.
- Do not add raw URLs in Sources Checked.
- Do not change `[VERIFY DETAILS]` to any other form.
- If unsure about a factual claim and cannot verify quickly, flag it `[VERIFY DETAILS]` rather than guessing.
- The corrected HTML must preserve all article content — only fix compliance issues, never rewrite the substance.
