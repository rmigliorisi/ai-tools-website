# 11 Launch QA Checklist

## Goal

Prevent SEO, AI-search, accessibility, and technical issues before launch.

## Pre-launch checks

### Crawlability
- [ ] Important pages use real `<a href>` links.
- [ ] Important pages are internally linked.
- [ ] No important pages are blocked by robots.txt.
- [ ] Navigation is crawlable.
- [ ] XML sitemap exists and is clean.

### Indexability
- [ ] Important pages return 200.
- [ ] Important pages are indexable.
- [ ] Important pages have self-canonical tags.
- [ ] Non-indexable pages are intentionally noindexed.
- [ ] No accidental sitewide noindex.

### Metadata
- [ ] Unique title tags.
- [ ] Useful meta descriptions.
- [ ] One clear H1.
- [ ] Open Graph/Twitter metadata where useful.

### Structured data
- [ ] Organization schema on brand-level pages.
- [ ] Breadcrumb schema on hierarchical pages.
- [ ] Article/BlogPosting schema on editorial pages.
- [ ] FAQ schema only where visible/eligible.
- [ ] No fake or misleading schema.
- [ ] Rich Results Test passed where applicable.

### Content
- [ ] Page purpose is clear.
- [ ] Above-the-fold summary answers user intent.
- [ ] Key takeaways are concise.
- [ ] Content has information gain.
- [ ] No generic filler.
- [ ] Internal links support next steps.

### Performance
- [ ] HTML response is below risk thresholds.
- [ ] LCP/INP/CLS checked.
- [ ] Images optimized.
- [ ] No excessive third-party scripts.
- [ ] Critical content is not lazy-loaded incorrectly.

### Accessibility and agent readiness
- [ ] Navigation works with keyboard.
- [ ] Buttons are real buttons.
- [ ] Links are real anchors.
- [ ] Forms have labels.
- [ ] Cards have descriptive links.
- [ ] Tables use semantic markup.
- [ ] Accessibility tree checked for key templates.
- [ ] No hover-only critical interactions.

### AI Search / GEO
- [ ] Entity names are consistent.
- [ ] Direct answers are extractable.
- [ ] Author/reviewer/source information is clear.
- [ ] Important content is visible to crawlers.
- [ ] AI crawler policy is intentional.
- [ ] Brand/about/contact details are consistent.

### Analytics
- [ ] GSC verified.
- [ ] GA4 or analytics installed.
- [ ] Conversion events configured.
- [ ] Sitemap submitted.
- [ ] Rank/visibility tracking setup for priority queries.

## Post-launch checks

Within 24-48 hours:
- [ ] Crawl live site.
- [ ] Inspect key URLs in GSC.
- [ ] Check robots.txt.
- [ ] Validate sitemaps.
- [ ] Validate structured data.
- [ ] Check 404/redirect errors.
- [ ] Check analytics firing.

Within 2-4 weeks:
- [ ] Monitor indexation.
- [ ] Review GSC impressions.
- [ ] Check query/page matching.
- [ ] Fix crawl anomalies.
- [ ] Review AI-search visibility manually.
