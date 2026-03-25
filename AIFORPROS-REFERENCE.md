# AI Tools for Pros — HTML Reference File

Use this file alongside AIFORPROS.md. AIFORPROS.md is the master content prompt. This file gives you the exact HTML boilerplate, nav, footer, and author card to copy verbatim into every page you generate.

---

## CRITICAL — PRE-SUBMIT CHECKLIST

Before you output the final HTML, verify every item below. These are the most common failure points. A page that misses any of these will be rejected and need a full correction pass.

1. **`style.css` link in `<head>`** — After the closing `</style>` tag, this exact line must be present:
   ```html
   <link rel="stylesheet" href="../style.css">
   ```
   (For root-level hub pages use `style.css` with no `../`.)

2. **`site.js` script in `<head>`** — Immediately before `</head>`, this exact line must be present:
   ```html
   <script src="../site.js" defer></script>
   ```
   (For root-level hub pages use `site.js` with no `../`.)

3. **Nav IDs** — The nav middle div must have `id="nav-desktop"`. Copy the nav verbatim from this file — do not rebuild it.

4. **Consistency blocks — exact card format** — There are 5 separate `<div>` card blocks: Bottom Line, Key Takeaways, Best Use Cases, Avoid If, and Mini Workflow. Each uses a styled card `<div>` with an UPPERCASE label `<p>` tag — NOT an H2 heading. Do NOT wrap them in a single `<section>`. Copy each card verbatim from the CONSISTENCY BLOCKS TEMPLATE section below.

   ❌ Wrong (reject this — common ChatGPT mistake):
   ```html
   <section style="...">
     <h2>Bottom Line</h2>
     <p>...</p>
     <h2>Key Takeaways</h2>
     <ul>...</ul>
   </section>
   ```
   ✓ Correct: 5 separate `<div>` cards, each with an uppercase `<p>` label in blue (not an H2), exactly as in the CONSISTENCY BLOCKS TEMPLATE below.

5. **Verdict badge — blue left-border card, not a pill or icon badge** — The verdict banner goes directly after the byline, before the consistency blocks. It must be a `<div>` with `background:#eff6ff` and `border-left:4px solid #2563EB`. Do NOT output a plain pill span, a checkmark icon, or a white card with a dot.

   ❌ Wrong (reject this — common ChatGPT mistake):
   ```html
   <span style="background:#dbeafe;color:#1d4ed8;padding:4px 14px;border-radius:999px;font-size:12px;">✓ Recommended</span>
   ```
   ✓ Correct: copy the verdict badge `<div>` verbatim from the top of the CONSISTENCY BLOCKS TEMPLATE section below. It uses `.verdict-badge-recommended` (blue) or `.verdict-badge-specialized` (purple) as the `<span>` class inside the card.

6. **Quick Facts Bar — use `.fact-bar` and `.fact-item` classes** — Do not substitute an inline `display:grid` or a `<table>`. Copy the class-based markup from the CONSISTENCY BLOCKS TEMPLATE. Also: every field value must have real text before any `[VERIFY DETAILS]` flag — never `[VERIFY DETAILS]` as the entire field content.

7. **Byline — full date + reading-time span** — The byline must use the full date (`February 25, 2026`, not `February 2026`) and must include `<span id="reading-time"></span>` immediately after the date. Do not omit the span — site.js injects the read-time into it at page load.

8. **Nav Legal Counsel submenu** — Must include `<a href="../gemini/legal.html">Google Gemini</a>` and `<a href="../notion-ai/legal.html">Notion AI</a>`. Copy the full nav from this file verbatim; do not reconstruct it from memory.

---

---

## HOW TO USE THESE TWO FILES

1. Paste AIFORPROS.md first into your ChatGPT session (this is the master prompt)
2. Then paste this file (AIFORPROS-REFERENCE.md) to give it the HTML structure
3. Then give the PAGE TO CREATE variables:
   ```
   Page type: TOOL_PROFESSION
   Tool name: ChatGPT
   Tool company: OpenAI
   Profession: Legal Counsel
   Output file path: chatgpt/legal.html
   Output mode: FULL_HTML_FILE
   Current year: 2026
   Primary keyword: ChatGPT for lawyers
   ```
4. Generate one page per session for best quality. Long pages need full context.

---

## IMPORTANT PATH RULES

All TOOL_PROFESSION pages live in subdirectories (e.g., `chatgpt/legal.html`).
This means all links must use `../` prefix:
- Logo: `../logo.svg`
- Hub page links: `../chatgpt.html`, `../claude.html`, etc.
- Cross-reference links: `../chatgpt/legal.html`, `../claude/physicians.html`, etc.
- Back to home: `../index.html`
- About, process, newsletter: `../about-us.html`, `../our-process.html`, `../newsletter.html`
- Legal pages: `../privacy-policy.html`, `../cookie-policy.html`
- Shared assets: `../style.css`, `../site.js` (for TOOL_PROFESSION pages in subdirectories)
- For TOOL_OVERVIEW hub pages (root-level): use `style.css` and `site.js` (no `../`)

---

## HEAD BLOCK (copy into every TOOL_PROFESSION page)

Replace the [BRACKETED] values for each page.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Tool Name] for [Profession Plural] — 2026 Guide | AI Tools for Pros</title>
  <meta name="description" content="[140-155 char description. Include tool name, profession, year, specific value prop. No generic marketing language.]">
  <meta property="og:title" content="[Tool Name] for [Profession Plural] — 2026 Guide | AI Tools for Pros">
  <meta property="og:description" content="[Same as meta description]">
  <meta property="og:image" content="https://aitoolsforpros.com/og-image.jpg">
  <meta property="og:type" content="article">
  <link rel="canonical" href="https://aitoolsforpros.com/[tool-slug]/[profession-slug]">
  <link rel="icon" type="image/svg+xml" href="../favicon.svg">
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cardo:ital,wght@0,400;0,700;1,400&family=Inter:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {
      theme: { extend: { fontFamily: { body: ['Inter','sans-serif'], heading: ['Cardo','serif'] } } }
    }
  </script>
  <style>
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
    .submenu-trigger { display: flex; align-items: center; justify-content: space-between; gap: 24px; padding: 9px 14px; font-size: 13px; color: #333333; text-decoration: none; border-radius: 7px; cursor: pointer; transition: background 0.1s, color 0.1s; white-space: nowrap; }
    .submenu-item:hover .submenu-trigger { background: #f5f5f5; color: #111111; }
    .submenu { position: absolute; left: calc(100% + 6px); top: -6px; background: #ffffff; border: 1px solid #ebebeb; border-radius: 12px; box-shadow: 0 12px 40px rgba(0,0,0,0.09); padding: 6px; min-width: 196px; opacity: 0; visibility: hidden; transition: opacity 0.15s, visibility 0.15s; z-index: 201; }
    .submenu-item:hover .submenu { opacity: 1; visibility: visible; }
    .submenu a { display: block; padding: 9px 14px; font-size: 13px; color: #333333; text-decoration: none; border-radius: 7px; transition: background 0.1s, color 0.1s; white-space: nowrap; }
    .submenu a:hover { background: #f5f5f5; color: #111111; }
    .prompt-block { background: #f8f9fa; border-left: 3px solid #2563EB; padding: 16px 20px; border-radius: 8px; font-family: 'Courier New', monospace; font-size: 13px; color: #333333; line-height: 1.7; margin-bottom: 20px; }
  </style>
  <!-- Shared stylesheet: responsive layout + dark mode -->
  <link rel="stylesheet" href="../style.css">

  <!-- JSON-LD: replace all [BRACKETED] values -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Article",
        "headline": "[Tool Name] for [Profession Plural] — 2026 Guide",
        "description": "[Same as meta description]",
        "author": {"@type": "Person", "name": "Rich M."},
        "publisher": {"@type": "Organization", "name": "AI Tools for Pros", "url": "https://aitoolsforpros.com"},
        "datePublished": "[YYYY-MM-DD]",
        "dateModified": "[YYYY-MM-DD]",
        "mainEntityOfPage": {"@type": "WebPage", "@id": "https://aitoolsforpros.com/[tool-slug]/[profession-slug]"},
        "isAccessibleForFree": true
      },
      {
        "@type": "BreadcrumbList",
        "itemListElement": [
          {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://aitoolsforpros.com/"},
          {"@type": "ListItem", "position": 2, "name": "[Tool Name]", "item": "https://aitoolsforpros.com/[tool-slug]"},
          {"@type": "ListItem", "position": 3, "name": "[Profession Display Name]", "item": "https://aitoolsforpros.com/[tool-slug]/[profession-slug]"}
        ]
      },
      {
        "@type": "FAQPage",
        "mainEntity": [
          {
            "@type": "Question",
            "name": "[FAQ Question 1 — match on-page text exactly]",
            "acceptedAnswer": {"@type": "Answer", "text": "[Answer 1 — starts Yes/No/It depends]"}
          },
          {
            "@type": "Question",
            "name": "[FAQ Question 2]",
            "acceptedAnswer": {"@type": "Answer", "text": "[Answer 2]"}
          },
          {
            "@type": "Question",
            "name": "[FAQ Question 3]",
            "acceptedAnswer": {"@type": "Answer", "text": "[Answer 3]"}
          },
          {
            "@type": "Question",
            "name": "[FAQ Question 4]",
            "acceptedAnswer": {"@type": "Answer", "text": "[Answer 4]"}
          }
        ]
      }
    ]
  }
  </script>
  <!-- Shared site script: dark mode toggle + mobile hamburger nav -->
  <script src="../site.js" defer></script>
</head>
```

---

## NAV HTML (for TOOL_PROFESSION pages — all paths use `../`)

**IMPORTANT:** The Professions submenu below only lists professions and tools where pages currently exist. Do NOT add nav entries for pages that have not been built yet. As new pages are created, the nav will be updated centrally. Use this nav as-is for now.

```html
<nav style="padding:18px min(6.5rem,8vw);position:sticky;top:0;z-index:50;background:#ffffff;border-bottom:1px solid #f0f0f0;" class="flex items-center justify-between">
  <a href="../index.html" class="flex items-center gap-2.5 no-underline" style="display:flex;align-items:center;gap:10px;text-decoration:none;">
    <img src="../logo.svg" width="32" height="32" alt="AI Tools for Pros" style="border-radius:8px;display:block;">
    <span style="font-size:13px;font-weight:500;color:#111111;">AI Tools for Pros</span>
  </a>
  <div id="nav-desktop" style="display:flex;align-items:center;gap:36px;">
    <a href="../our-process.html" class="nav-link">Our Process</a>

    <!-- AI Tools Dropdown -->
    <div class="nav-dropdown">
      <span class="nav-link-caret">AI Tools <svg width="8" height="5" viewBox="0 0 8 5" fill="none"><path d="M1 1l3 3 3-3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
      <div class="dropdown-menu">
        <a href="../chatgpt.html" class="dropdown-item">ChatGPT</a>
        <a href="../claude.html" class="dropdown-item">Claude</a>
        <a href="../perplexity.html" class="dropdown-item">Perplexity AI</a>
        <a href="../gemini.html" class="dropdown-item">Google Gemini</a>
        <a href="../copilot.html" class="dropdown-item">Microsoft Copilot</a>
        <a href="../midjourney.html" class="dropdown-item">Midjourney</a>
        <a href="../cursor.html" class="dropdown-item">Cursor</a>
        <a href="../notion-ai.html" class="dropdown-item">Notion AI</a>
        <a href="../grammarly.html" class="dropdown-item">Grammarly</a>
        <a href="../otter.html" class="dropdown-item">Otter.ai</a>
      </div>
    </div>

    <!-- Professions Dropdown — only includes professions with published pages -->
    <div class="nav-dropdown">
      <span class="nav-link-caret">Professions <svg width="8" height="5" viewBox="0 0 8 5" fill="none"><path d="M1 1l3 3 3-3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
      <div class="dropdown-menu">

        <div class="submenu-item">
          <a href="../legal.html" class="submenu-trigger">Legal Counsel <svg width="5" height="8" viewBox="0 0 5 8" fill="none"><path d="M1 1l3 3-3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
          <div class="submenu">
            <a href="../chatgpt/legal.html">ChatGPT</a>
            <a href="../claude/legal.html">Claude</a>
            <a href="../perplexity/legal.html">Perplexity AI</a>
            <a href="../gemini/legal.html">Google Gemini</a>
            <a href="../copilot/legal.html">Microsoft Copilot</a>
            <a href="../grammarly/legal.html">Grammarly</a>
            <a href="../notion-ai/legal.html">Notion AI</a>
          </div>
        </div>

        <div class="submenu-item">
          <a href="../physicians.html" class="submenu-trigger">Physicians <svg width="5" height="8" viewBox="0 0 5 8" fill="none"><path d="M1 1l3 3-3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
          <div class="submenu">
            <a href="../chatgpt/physicians.html">ChatGPT</a>
            <a href="../claude/physicians.html">Claude</a>
            <a href="../perplexity/physicians.html">Perplexity AI</a>
            <a href="../copilot/physicians.html">Microsoft Copilot</a>
            <a href="../otter/physicians.html">Otter.ai</a>
          </div>
        </div>

        <div class="submenu-item">
          <a href="../real-estate.html" class="submenu-trigger">Real Estate <svg width="5" height="8" viewBox="0 0 5 8" fill="none"><path d="M1 1l3 3-3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
          <div class="submenu">
            <a href="../chatgpt/real-estate.html">ChatGPT</a>
            <a href="../claude/real-estate.html">Claude</a>
            <a href="../gemini/real-estate.html">Google Gemini</a>
            <a href="../copilot/real-estate.html">Microsoft Copilot</a>
            <a href="../grammarly/real-estate.html">Grammarly</a>
          </div>
        </div>

        <div class="submenu-item">
          <a href="../finance.html" class="submenu-trigger">Finance <svg width="5" height="8" viewBox="0 0 5 8" fill="none"><path d="M1 1l3 3-3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
          <div class="submenu">
            <a href="../chatgpt/finance.html">ChatGPT</a>
            <a href="../claude/finance.html">Claude</a>
            <a href="../perplexity/finance.html">Perplexity AI</a>
            <a href="../copilot/finance.html">Microsoft Copilot</a>
            <a href="../gemini/finance.html">Google Gemini</a>
          </div>
        </div>

        <div class="submenu-item">
          <a href="../insurance.html" class="submenu-trigger">Insurance <svg width="5" height="8" viewBox="0 0 5 8" fill="none"><path d="M1 1l3 3-3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
          <div class="submenu">
            <a href="../chatgpt/insurance.html">ChatGPT</a>
            <a href="../claude/insurance.html">Claude</a>
            <a href="../perplexity/insurance.html">Perplexity AI</a>
            <a href="../copilot/insurance.html">Microsoft Copilot</a>
            <a href="../grammarly/insurance.html">Grammarly</a>
          </div>
        </div>

        <div class="submenu-item">
          <a href="../engineers.html" class="submenu-trigger">Engineers <svg width="5" height="8" viewBox="0 0 5 8" fill="none"><path d="M1 1l3 3-3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
          <div class="submenu">
            <a href="../chatgpt/engineers.html">ChatGPT</a>
            <a href="../claude/engineers.html">Claude</a>
            <a href="../cursor/engineers.html">Cursor</a>
            <a href="../copilot/engineers.html">Microsoft Copilot</a>
            <a href="../notion-ai/engineers.html">Notion AI</a>
          </div>
        </div>

        <div class="submenu-item">
          <a href="../architects.html" class="submenu-trigger">Architects <svg width="5" height="8" viewBox="0 0 5 8" fill="none"><path d="M1 1l3 3-3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
          <div class="submenu">
            <a href="../chatgpt/architects.html">ChatGPT</a>
            <a href="../claude/architects.html">Claude</a>
            <a href="../gemini/architects.html">Google Gemini</a>
            <a href="../midjourney/architects.html">Midjourney</a>
          </div>
        </div>

        <div class="submenu-item">
          <a href="../creatives.html" class="submenu-trigger">Creatives <svg width="5" height="8" viewBox="0 0 5 8" fill="none"><path d="M1 1l3 3-3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
          <div class="submenu">
            <a href="../chatgpt/creatives.html">ChatGPT</a>
            <a href="../claude/creatives.html">Claude</a>
            <a href="../midjourney/creatives.html">Midjourney</a>
            <a href="../grammarly/creatives.html">Grammarly</a>
            <a href="../notion-ai/creatives.html">Notion AI</a>
          </div>
        </div>

      </div>
    </div>

    <a href="../newsletter.html" class="nav-link">Newsletter</a>
  </div>
</nav>
```

---

## BYLINE HTML

Place this directly after the lede paragraph, before the verdict badge. Use the same markup on every page.

Replace `[Month DD, YYYY]` with the actual publication date (e.g., `February 25, 2026`). Leave `<span id="reading-time"></span>` empty — `site.js` injects "· X min read" automatically at page load.

```html
<p style="font-size:13px;color:#636363;margin:0 0 20px;">By <strong style="color:#111111;font-weight:600;">Rich M.</strong>&nbsp;&middot;&nbsp;Fact-checked by <strong style="color:#111111;font-weight:600;">Rob M.</strong>&nbsp;&middot;&nbsp;Published [Month DD, YYYY]<span id="reading-time"></span></p>
```

---

## AUTHOR PROFILE CARD HTML

Place this immediately before the `<footer>` tag. Use this exact markup — do not substitute a different avatar or bio.

```html
<!-- AUTHOR PROFILE CARD -->
<section style="padding:48px 24px;background:#f9fafb;border-top:1px solid #e5e7eb;">
  <div style="max-width:860px;margin:0 auto;">
    <div style="background:#ffffff;border:1px solid #f0f0f0;border-radius:16px;padding:28px 32px;display:flex;align-items:flex-start;gap:20px;">
      <div style="flex-shrink:0;">
        <svg width="72" height="72" viewBox="0 0 72 72" fill="none" xmlns="http://www.w3.org/2000/svg" style="border-radius:50%;display:block;">
          <rect width="72" height="72" rx="36" fill="#f0f4ff"/>
          <circle cx="36" cy="28" r="12" fill="#bfcfff"/>
          <ellipse cx="36" cy="56" rx="20" ry="14" fill="#bfcfff"/>
          <circle cx="36" cy="28" r="10" fill="#d6e0ff">
            <animate attributeName="r" values="10;10.5;10" dur="4s" repeatCount="indefinite"/>
          </circle>
        </svg>
      </div>
      <div>
        <p style="font-size:14px;font-weight:600;color:#111111;margin:0 0 4px;">Rich M.</p>
        <p style="font-size:12px;color:#9ca3af;margin:0 0 10px;">Editor, AI Tools for Pros</p>
        <p style="font-size:13px;color:#636363;line-height:1.7;margin:0 0 10px;">I test AI tools inside real professional workflows and write honest, first-person assessments. My goal is straightforward guidance on AI tools, without agenda or affiliate incentives.</p>
        <a href="../about-us.html" style="font-size:12px;color:#2563EB;text-decoration:none;font-weight:500;" onmouseover="this.style.color='#1d4ed8'" onmouseout="this.style.color='#2563EB'">Read more about our editorial process</a>
      </div>
    </div>
  </div>
</section>
```

---

## FOOTER HTML (for TOOL_PROFESSION pages — all paths use `../`)

```html
<footer style="background:#07091a;border-radius:28px 28px 0 0;padding:56px min(6.5rem,8vw);">
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:40px;margin-bottom:52px;">
    <div>
      <p style="color:#4a5568;font-size:9px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;margin:0 0 16px;">Directory</p>
      <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:10px;">
        <li><a href="../legal.html" style="color:#5a6e94;font-size:13px;text-decoration:none;transition:color 0.15s;" onmouseover="this.style.color='#ffffff'" onmouseout="this.style.color='#5a6e94'">Legal Counsel</a></li>
        <li><a href="../architects.html" style="color:#5a6e94;font-size:13px;text-decoration:none;transition:color 0.15s;" onmouseover="this.style.color='#ffffff'" onmouseout="this.style.color='#5a6e94'">Architects</a></li>
        <li><a href="../physicians.html" style="color:#5a6e94;font-size:13px;text-decoration:none;transition:color 0.15s;" onmouseover="this.style.color='#ffffff'" onmouseout="this.style.color='#5a6e94'">Physicians</a></li>
        <li><a href="../engineers.html" style="color:#5a6e94;font-size:13px;text-decoration:none;transition:color 0.15s;" onmouseover="this.style.color='#ffffff'" onmouseout="this.style.color='#5a6e94'">Engineers</a></li>
        <li><a href="../finance.html" style="color:#5a6e94;font-size:13px;text-decoration:none;transition:color 0.15s;" onmouseover="this.style.color='#ffffff'" onmouseout="this.style.color='#5a6e94'">Finance</a></li>
        <li><a href="../creatives.html" style="color:#5a6e94;font-size:13px;text-decoration:none;transition:color 0.15s;" onmouseover="this.style.color='#ffffff'" onmouseout="this.style.color='#5a6e94'">Creatives</a></li>
      </ul>
    </div>
    <div>
      <p style="color:#4a5568;font-size:9px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;margin:0 0 16px;">Company</p>
      <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:10px;">
        <li><a href="../about-us.html" style="color:#5a6e94;font-size:13px;text-decoration:none;transition:color 0.15s;" onmouseover="this.style.color='#ffffff'" onmouseout="this.style.color='#5a6e94'">About</a></li>
        <li><a href="../our-process.html" style="color:#5a6e94;font-size:13px;text-decoration:none;transition:color 0.15s;" onmouseover="this.style.color='#ffffff'" onmouseout="this.style.color='#5a6e94'">Our Process</a></li>
      </ul>
    </div>
    <div>
      <p style="color:#4a5568;font-size:9px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;margin:0 0 16px;">Resources</p>
      <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:10px;">
        <li><a href="../newsletter.html" style="color:#5a6e94;font-size:13px;text-decoration:none;transition:color 0.15s;" onmouseover="this.style.color='#ffffff'" onmouseout="this.style.color='#5a6e94'">Newsletter</a></li>
      </ul>
    </div>
    <div>
      <p style="color:#4a5568;font-size:9px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;margin:0 0 16px;">Legal</p>
      <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:10px;">
        <li><a href="../privacy-policy.html" style="color:#5a6e94;font-size:13px;text-decoration:none;transition:color 0.15s;" onmouseover="this.style.color='#ffffff'" onmouseout="this.style.color='#5a6e94'">Privacy Policy</a></li>
        <li><a href="../cookie-policy.html" style="color:#5a6e94;font-size:13px;text-decoration:none;transition:color 0.15s;" onmouseover="this.style.color='#ffffff'" onmouseout="this.style.color='#5a6e94'">Cookie Policy</a></li>
      </ul>
    </div>
  </div>
  <div style="border-top:1px solid #111e38;margin-bottom:48px;"></div>
  <div style="display:flex;align-items:center;justify-content:space-between;">
    <div>
      <p style="color:#1e2a45;font-size:11px;font-weight:500;margin:0 0 4px;letter-spacing:0.05em;opacity:0.6;">AI Tools for Pros</p>
      <p class="font-heading" style="color:#2563EB;font-size:48px;font-weight:700;margin:0 0 10px;line-height:1;">2026.</p>
      <p style="color:#4a5568;font-size:13px;margin:0;">Join 15,000+ professionals receiving our monthly tool audit.</p>
    </div>
    <div style="display:flex;align-items:center;gap:10px;">
      <div style="position:relative;display:flex;align-items:center;">
        <input type="email" placeholder="professional@email.com" style="background:#0d1228;color:#4a5568;font-size:13px;padding:13px 48px 13px 18px;border-radius:999px;border:1px solid #1a2444;outline:none;width:248px;font-family:'Inter',sans-serif;">
        <div style="position:absolute;right:8px;width:28px;height:28px;background:#1a2444;border-radius:50%;display:flex;align-items:center;justify-content:center;">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M2 6h8M6 2l4 4-4 4" stroke="#4a5568" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </div>
      </div>
      <button style="background:#ffffff;color:#111111;font-size:13px;font-weight:500;padding:13px 24px;border-radius:999px;border:none;cursor:pointer;font-family:'Inter',sans-serif;" onmouseover="this.style.background='#f0f0f0'" onmouseout="this.style.background='#ffffff'">Subscribe</button>
    </div>
  </div>
</footer>
```

---

## CONSISTENCY BLOCKS TEMPLATE (copy into every TOOL_PROFESSION page)

Replace all `[BRACKETED]` values. Use the exact color styling — these blocks must look identical across all cross-reference pages.

```html
<!-- Verdict badge banner — use .verdict-badge-recommended (blue) for broadly useful tools,
     .verdict-badge-specialized (purple) for ecosystem-specific tools.
     The banner card makes the verdict prominently visible — do not reduce it to a plain pill. -->
<div style="background:#eff6ff;border-left:4px solid #2563EB;border-radius:10px;padding:18px 22px;margin:0 0 32px;max-width:760px;">
  <div style="display:flex;align-items:center;gap:12px;margin:0 0 8px;flex-wrap:wrap;">
    <span class="verdict-badge-recommended">[Verdict text, e.g. Recommended with caveats]</span>
  </div>
  <p style="font-size:14px;color:#1e40af;line-height:1.55;margin:0;">[One sentence expanding on the verdict — no em dashes.]</p>
</div>

<!-- Block 1: Bottom Line — white card with blue label -->
<div style="background:#ffffff;border:1px solid #f0f0f0;border-radius:12px;padding:24px 28px;margin-bottom:20px;max-width:760px;">
  <p style="font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#2563EB;margin:0 0 10px;">Bottom Line</p>
  <p style="font-size:14px;color:#333333;line-height:1.7;margin:0;">[2–3 sentences. Honest, specific, first-person.]</p>
</div>

<!-- Block 2: Key Takeaways — white card with blue arrow markers -->
<div style="background:#ffffff;border:1px solid #f0f0f0;border-radius:12px;padding:24px 28px;margin-bottom:20px;max-width:760px;">
  <p style="font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#2563EB;margin:0 0 14px;">Key Takeaways</p>
  <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:10px;">
    <li style="display:flex;gap:10px;font-size:14px;color:#333333;line-height:1.6;"><span style="color:#2563EB;flex-shrink:0;font-weight:700;">&#8594;</span> [Takeaway 1 — under 12 words]</li>
    <li style="display:flex;gap:10px;font-size:14px;color:#333333;line-height:1.6;"><span style="color:#2563EB;flex-shrink:0;font-weight:700;">&#8594;</span> [Takeaway 2]</li>
    <li style="display:flex;gap:10px;font-size:14px;color:#333333;line-height:1.6;"><span style="color:#2563EB;flex-shrink:0;font-weight:700;">&#8594;</span> [Takeaway 3]</li>
    <li style="display:flex;gap:10px;font-size:14px;color:#333333;line-height:1.6;"><span style="color:#2563EB;flex-shrink:0;font-weight:700;">&#8594;</span> [Takeaway 4]</li>
  </ul>
</div>

<!-- Blocks 3 + 4: Best Use Cases (green) + Avoid (red) — side by side -->
<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;max-width:760px;margin-bottom:20px;">
  <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;padding:20px 24px;">
    <p style="font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#15803d;margin:0 0 12px;">Best Use Cases</p>
    <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:8px;">
      <li style="font-size:13px;color:#166534;">[Use case 1 — 6–10 words]</li>
      <li style="font-size:13px;color:#166534;">[Use case 2]</li>
      <li style="font-size:13px;color:#166534;">[Use case 3]</li>
      <li style="font-size:13px;color:#166534;">[Use case 4]</li>
    </ul>
  </div>
  <div style="background:#fef2f2;border:1px solid #fecaca;border-radius:12px;padding:20px 24px;">
    <p style="font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#dc2626;margin:0 0 12px;">Avoid Using It For</p>
    <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:8px;">
      <li style="font-size:13px;color:#991b1b;">[Avoid 1 — include at least one compliance/safety risk]</li>
      <li style="font-size:13px;color:#991b1b;">[Avoid 2]</li>
      <li style="font-size:13px;color:#991b1b;">[Avoid 3]</li>
    </ul>
  </div>
</div>

<!-- Block 5: Mini Workflow — blue card -->
<div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:12px;padding:24px 28px;max-width:760px;margin-bottom:28px;">
  <p style="font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#1d4ed8;margin:0 0 12px;">If You Only Do One Thing</p>
  <p style="font-size:13px;color:#1e40af;margin:0 0 12px;">[One-sentence lead-in to the workflow]</p>
  <ol style="padding:0 0 0 18px;margin:0;display:flex;flex-direction:column;gap:6px;">
    <li style="font-size:13px;color:#1e40af;">[Step 1]</li>
    <li style="font-size:13px;color:#1e40af;">[Step 2]</li>
    <li style="font-size:13px;color:#1e40af;">[Step 3]</li>
    <li style="font-size:13px;color:#1e40af;">[Step 4]</li>
  </ol>
</div>

<!-- Quick Facts Bar — use .fact-bar class (responsive grid built in) -->
<div class="fact-bar" style="max-width:860px;margin:0 0 28px;">
  <div class="fact-item">
    <p style="font-size:9px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#9ca3af;margin:0 0 6px;">Best for</p>
    <p style="font-size:14px;font-weight:600;color:#111111;margin:0;">[2–4 words]</p>
  </div>
  <div class="fact-item">
    <p style="font-size:9px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#9ca3af;margin:0 0 6px;">Pricing</p>
    <p style="font-size:14px;font-weight:600;color:#111111;margin:0;">[Best estimate with tier, e.g. Free / from $20/mo] [VERIFY DETAILS]</p>
  </div>
  <div class="fact-item">
    <p style="font-size:9px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#9ca3af;margin:0 0 6px;">Compliance</p>
    <p style="font-size:14px;font-weight:600;color:#111111;margin:0;">[Compliance status] [VERIFY DETAILS]</p>
  </div>
  <div class="fact-item">
    <p style="font-size:9px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#9ca3af;margin:0 0 6px;">Compared to</p>
    <p style="font-size:14px;font-weight:600;color:#111111;margin:0;">[Primary competitor tool]</p>
  </div>
</div>
```

**IMPORTANT — [VERIFY DETAILS] in Quick Facts Bar:** The `[VERIFY DETAILS]` flag must follow an actual value or estimate — never appear alone as the entire field content. If you don't know the exact price, write a reasonable range based on publicly known tiers and append `[VERIFY DETAILS]`. Example: `Free / from $19.99/mo [VERIFY DETAILS]`, never just `[VERIFY DETAILS]`.

---

## PAGE SKELETON (how to assemble the pieces)

Every TOOL_PROFESSION page follows this exact order:

```
[HEAD BLOCK]
<body>
  [NAV]
  [BREADCRUMB]
  [HERO: eyebrow, H1, lede, BYLINE, verdict badge]
  [CONSISTENCY BLOCKS: Bottom Line, Key Takeaways, Best Use Cases, Avoid If, Mini Workflow]
  [QUICK FACTS BAR]
  [WHAT PROFESSION USES IT FOR — H2 with use cases]
  [PROMPTS THAT WORK FOR PROFESSION — H2 with .prompt-block divs]
  [COMPLIANCE AND PROFESSIONAL RISK — H2]
  [WHERE IT FALLS SHORT — H2]
  [HOW IT COMPARES — H2 with comparison table]
  [MY VERDICT — H2]
  [FAQ — H2 with schema microdata]
  [SOURCES CHECKED — H2]
  [RELATED GUIDES — H2]
  [WHAT MOST REVIEWS MISS — H2]
  [AUTHOR PROFILE CARD]
  [FOOTER]
</body>
```

---

## CONTENT STYLE RULES (quick reference)

- **No em dashes in body copy.** Use commas, periods, semicolons, or colons instead. Em dashes are only allowed in H1/H2/H3 headings and `<title>` tags.
- **First person only.** Use "I tested", "I found", "in my experience". Never "we" or "our" in body copy. Verdict heading: "My Verdict", not "Our Verdict".
- **[VERIFY DETAILS]** on any claim that needs vendor confirmation before publishing (pricing, HIPAA status, feature availability).
- **FAQ answers** must start with Yes / No / It depends.
- **Sources Checked** format: `[N] Vendor — Page description (what it confirms)`
- **Slug for this page's link in Related Guides:** use `../[tool-slug]/[profession-slug].html`

---

## QUICK REFERENCE: SLUG TABLE

| Profession | Slug | File path example |
|---|---|---|
| Legal Counsel | `legal` | `chatgpt/legal.html` |
| Physicians | `physicians` | `chatgpt/physicians.html` |
| Real Estate Agents | `real-estate` | `chatgpt/real-estate.html` |
| Finance Professionals | `finance` | `chatgpt/finance.html` |
| Insurance Professionals | `insurance` | `chatgpt/insurance.html` |
| Software Engineers | `engineers` | `chatgpt/engineers.html` |
| Architects | `architects` | `chatgpt/architects.html` |
| Creatives & Copywriters | `creatives` | `chatgpt/creatives.html` |
| Accountants | `accountants` | `chatgpt/accountants.html` |
| Graphic Designers | `graphic-designers` | `chatgpt/graphic-designers.html` |
| Content Creators | `content-creators` | `chatgpt/content-creators.html` |
| SEOs | `seo` | `chatgpt/seo.html` |
| Dentists | `dentists` | `chatgpt/dentists.html` |
| Psychologists & Therapists | `therapists` | `chatgpt/therapists.html` |
| Physical Therapists | `physical-therapists` | `chatgpt/physical-therapists.html` |

| Tool | Slug | Hub page |
|---|---|---|
| ChatGPT | `chatgpt` | `chatgpt.html` |
| Claude | `claude` | `claude.html` |
| Perplexity AI | `perplexity` | `perplexity.html` |
| Google Gemini | `gemini` | `gemini.html` |
| Microsoft Copilot | `copilot` | `copilot.html` |
| Midjourney | `midjourney` | `midjourney.html` |
| Cursor | `cursor` | `cursor.html` |
| Notion AI | `notion-ai` | `notion-ai.html` |
| Grammarly | `grammarly` | `grammarly.html` |
| Otter.ai | `otter` | `otter.html` |
