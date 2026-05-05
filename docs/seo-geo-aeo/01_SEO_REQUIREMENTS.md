# 01 SEO Requirements

## Goal

Build every website so search engines can crawl, render, understand, index, and rank the right pages with minimal ambiguity.

## 1. Crawlability

### Required
- Important pages must be reachable through crawlable internal links.
- Use real `<a href="...">` links for navigation, cards, breadcrumbs, related pages, and CTAs.
- Avoid JavaScript-only navigation for important links.
- Important URLs should not rely only on search forms, filters, or internal site search.
- Sitemaps should include only canonical, indexable URLs.

### Avoid
- Links triggered only by `onclick`, `data-url`, or JS events.
- Links without `href`.
- Important pages only discoverable after login, search, filters, or user interaction.
- Blocked render-critical CSS/JS.

## 2. Indexability

### Required
Every page must have a clear indexability decision:
- indexable
- noindex
- canonicalized
- redirected
- blocked
- removed

Important organic landing pages should generally be:
- status 200
- indexable
- self-canonical
- included in sitemap
- internally linked

### Noindex rules
Use `noindex` when a page should be crawled but not included in Search results.

Do not combine `robots.txt` disallow with `noindex` if your goal is to remove a page from search, because crawlers must be able to crawl the page to see the noindex directive.

## 3. Canonicalization

### Required
- Every indexable page should normally have a self-referencing canonical.
- Duplicate or near-duplicate URL variants should canonicalize to the preferred URL.
- Internal links should point to canonical URLs.
- Sitemap URLs should match canonical URLs.
- Do not canonicalize a page to another URL unless the content is duplicate or substantially similar.

### Avoid
- Multiple canonical tags.
- Canonicals to broken, redirected, noindex, blocked, or unrelated URLs.
- Conflicting canonical signals across HTML, HTTP headers, sitemaps, and redirects.
- Using robots.txt for canonicalization.

## 4. Redirects

### Required
- Use 301/308 for permanent moves.
- Use 302/307 only for temporary moves.
- Keep redirect chains short.
- Update internal links to final destination URLs.

### Avoid
- Redirect chains.
- Redirect loops.
- Redirecting many old URLs to irrelevant pages.
- Using 404/403 for rate limiting.

## 5. URL structure

### Required
- URLs should be readable, stable, lowercase, and descriptive.
- Use hyphens rather than underscores.
- Avoid unnecessary parameters for indexable pages.
- Keep URLs durable over time.

### Avoid
- Date-based URLs unless needed.
- Long, keyword-stuffed slugs.
- Session IDs or tracking parameters in canonical URLs.
- Generating indexable duplicates from sort/filter/tracking parameters.

## 6. Titles and meta descriptions

### Required
- Every indexable page needs one descriptive `<title>`.
- Titles should match search intent and page purpose.
- Meta descriptions should be unique where practical and should summarize the page accurately.
- Avoid boilerplate-only title/description patterns at scale.

### Rules of thumb
- Title: usually 45-65 characters, but relevance matters more than exact length.
- Meta description: usually 120-160 characters, but Google may choose its own snippet.
- Use page-specific differentiators.

## 7. Headings

### Required
- One clear H1 per page is preferred.
- H1 should describe the primary purpose of the page.
- H2/H3 structure should map to user intent and page sections.
- Do not use headings purely for styling.

## 8. Images

### Required
- Use descriptive alt text for meaningful images.
- Decorative images should have empty alt text (`alt=""`).
- Use compressed, appropriately sized images.
- Do not embed important text only inside images.
- Use responsive image practices where appropriate.

## 9. Page quality

### Required
Each indexable page should have:
- unique purpose
- clear user value
- useful main content
- strong internal links
- no thin/duplicate boilerplate patterns
- visible expert/reviewer/brand trust signals where appropriate

## 10. Measurement

Every SEO build should support:
- Google Search Console
- analytics
- sitemap submission
- crawl exports
- rank tracking for priority pages
- conversion/event tracking for business goals
