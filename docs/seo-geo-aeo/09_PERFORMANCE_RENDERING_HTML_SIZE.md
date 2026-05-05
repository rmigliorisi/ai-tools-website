# 09 Performance, Rendering, and HTML Size Requirements

## Goal

Keep pages fast, renderable, crawl-efficient, and machine-readable.

## 1. HTML/text response size

Current operating rule:
- Treat 2 MB HTML/text response size as a serious technical threshold for Google Search processing.
- Keep important content, links, metadata, and structured data well before that threshold.
- Prefer much smaller HTML where possible.

## 2. What counts toward HTML bloat

Large HTML can come from:
- visible text
- inline CSS
- inline JavaScript
- hydration state
- embedded JSON
- large schema blobs
- repeated nav/footer markup
- hidden tabs/accordions loaded into DOM
- huge tables/lists
- page-builder output
- duplicated modules

## 3. What does not count as HTML body size but still matters

- images
- external JS files
- external CSS files
- fonts
- videos
- iframes
- third-party scripts

These still affect performance and rendering, but the HTML-size issue specifically concerns the HTML/text response and text resources.

## 4. Lazy loading

Good for:
- images
- videos
- iframes
- below-the-fold media
- noncritical widgets

Avoid lazy-loading:
- H1
- intro
- key answer/verdict
- primary body text
- core internal links
- structured data
- pricing/compliance details
- main CTA
- content needed for Search visibility

Lazy-loaded content must load when visible in the viewport, not only after user actions like clicking or scrolling.

## 5. JavaScript rendering

Preferred:
- server-side rendering
- static rendering
- hydration with meaningful initial HTML

Riskier:
- client-side only rendering for important content
- content only available after interaction
- links generated only by JS
- metadata that differs between raw and rendered HTML
- error pages rendered client-side after wrong status codes

## 6. Core Web Vitals

Monitor:
- LCP
- INP
- CLS

Do not optimize only for lab scores. Prioritize real user impact and important templates.

## 7. Performance priorities

1. Reduce oversized HTML.
2. Remove unnecessary inline scripts/state.
3. Compress and resize images.
4. Defer noncritical JS.
5. Reduce third-party scripts.
6. Use caching.
7. Avoid layout shifts.
8. Improve server response time.
9. Split large pages/modules where appropriate.
10. Keep render-critical content available quickly.

## 8. Render QA

For important pages:
- compare raw HTML vs rendered HTML
- inspect source for critical content
- inspect rendered HTML in Search Console URL Inspection
- test with JS disabled
- use mobile user agent
- test slow connection
- confirm metadata/canonicals are stable

## 9. Agent/browser QA

Confirm:
- screenshots show stable UI
- accessibility tree has correct roles/names
- core actions are visible
- no overlays block key content/actions
- buttons/links are semantic
