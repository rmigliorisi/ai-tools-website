# 06 Technical SEO Audit Checklist

## Goal

Provide a repeatable technical audit workflow for any website.

## 1. Crawl setup

Recommended tools:
- Screaming Frog
- Sitebulb
- Semrush Site Audit
- Ahrefs Site Audit
- Google Search Console
- PageSpeed Insights / CrUX
- Rich Results Test
- Schema Markup Validator
- Chrome DevTools Accessibility panel

## 2. Crawl modes

Run at least two crawls where possible:
1. Standard HTML crawl
2. JavaScript-rendered crawl

Compare differences:
- content visible in raw HTML vs rendered HTML
- links found only after rendering
- canonicals/meta robots differences
- structured data differences
- important content missing pre-render

## 3. Core checks

### Response codes
- 200 indexable pages
- 3xx redirects
- 4xx errors
- 5xx errors
- soft 404s

### Indexability
- noindex pages
- blocked pages
- canonicalized pages
- sitemap inclusion
- orphan URLs

### Canonicals
- missing canonical
- self-canonical
- canonical to other URL
- broken canonical
- redirected canonical
- noindex canonical target
- multiple canonicals

### Robots
- robots.txt blocks
- meta robots
- X-Robots-Tag
- conflicts between robots and noindex
- AI crawler access

### Sitemaps
- only canonical indexable 200 URLs
- lastmod accuracy
- sitemap index health
- URLs in sitemap not crawlable
- crawlable URLs missing from sitemap
- non-indexable URLs in sitemap

### Internal links
- orphan pages
- pages with only one internal link
- high crawl depth
- nofollow internal links
- non-descriptive anchors
- links to redirects/4xx/canonicalized pages
- important pages underlinked

### Page templates
- title patterns
- meta description patterns
- H1 patterns
- duplicate templates
- thin content templates
- bloated HTML templates
- JS-heavy templates

### Structured data
- valid/invalid items
- wrong schema type
- visible-content mismatch
- unsupported schema
- missing Breadcrumb/Organization/Article where appropriate

### Performance
- HTML/text response size
- total page weight
- JS/CSS size
- render-blocking resources
- LCP/INP/CLS
- TTFB
- image weight
- unused JS/CSS

### Accessibility / agent-readiness
- semantic buttons/links
- form labels
- accessible names
- keyboard navigation
- menu states
- hidden overlays
- layout stability

## 4. Prioritization

Score each issue by:
- Business impact
- Ranking/indexing risk
- Template scale
- Developer effort
- Confidence
- Risk of breaking things
- Reversibility

## 5. Output format

Each audit issue should include:

```text
Issue:
Why it matters:
Affected URLs/templates:
Severity:
Recommended fix:
Owner:
Effort:
Expected impact:
Validation steps:
Rollback notes:
```

## 6. Do not overreact to tool counts

Tool issue counts are clues, not decisions.

Always ask:
- Does this affect indexable pages?
- Does this affect important templates?
- Does this affect revenue/conversions?
- Is the issue actually visible to Google?
- Is the fix template-level or URL-level?
- Could the fix create risk?
