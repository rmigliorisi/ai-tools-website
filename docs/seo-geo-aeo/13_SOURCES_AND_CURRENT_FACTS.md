# 13 Sources and Current Facts

**Last updated:** 2026-05-04

This file records the current operating facts behind the SEO / GEO / AEO requirements. Re-check these periodically because Google, OpenAI, and AI search systems change quickly.

## Google Search official sources

### Search Essentials
Source: https://developers.google.com/search/docs/essentials

Current working fact:
- Meeting technical requirements does not guarantee crawling, indexing, or serving.
- Search performance depends on technical accessibility, quality, and many systems.

### Crawlable links
Source: https://developers.google.com/search/docs/crawling-indexing/links-crawlable

Current working fact:
- Google can generally crawl links that are `<a>` elements with `href`.
- JS-only link patterns are less reliable for discovery.

### Canonicalization
Source: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls

Current working facts:
- Redirects and `rel=canonical` are strong canonicalization signals.
- Sitemap inclusion is a weaker signal.
- Internal links should point to canonical URLs.
- Do not use robots.txt for canonicalization.

### Robots.txt
Source: https://developers.google.com/search/docs/crawling-indexing/robots/intro

Current working facts:
- robots.txt controls crawling, not guaranteed indexing.
- A URL blocked by robots.txt can still appear in Search if discovered elsewhere.
- Use noindex or password protection when the goal is to keep a page out of Search.

### Noindex
Source: https://developers.google.com/search/docs/crawling-indexing/block-indexing

Current working facts:
- noindex must be crawlable to be seen.
- Do not block a noindexed URL in robots.txt if you need Google to see the noindex directive.

### Robots meta tags
Source: https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag

Current working fact:
- `nosnippet` applies to Google Search snippets and also prevents content from being used as direct input for AI Overviews and AI Mode.

### JavaScript SEO
Source: https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics

Current working facts:
- Google can process JavaScript, but limitations exist.
- Other search engines may ignore JavaScript.
- Test with JavaScript disabled or text-only tools to discover hidden content risks.

### Dynamic rendering
Source: https://developers.google.com/search/docs/crawling-indexing/javascript/dynamic-rendering

Current working facts:
- Dynamic rendering is a workaround, not a recommended long-term solution.
- Prefer server-side rendering, static rendering, or hydration.

### Lazy loading
Source: https://developers.google.com/search/docs/crawling-indexing/javascript/lazy-loading

Current working facts:
- Lazy loading is acceptable when relevant content loads as it enters the viewport.
- Google Search does not interact with the page by clicking or scrolling to trigger content.
- Infinite scroll needs paginated, persistent URLs.

### Structured data gallery
Source: https://developers.google.com/search/docs/appearance/structured-data/search-gallery

Current working fact:
- Only certain structured data feature families are supported by Google Search for rich result eligibility.

### Structured data policies
Source: https://developers.google.com/search/docs/appearance/structured-data/sd-policies

Current working facts:
- Structured data must match visible page content.
- Google does not guarantee rich results even when markup validates.
- JSON-LD, Microdata, and RDFa are supported, with JSON-LD generally recommended.

### Intro to structured data
Source: https://developers.google.com/search/docs/guides/intro-structured-data

Current working fact:
- Structured data provides explicit clues about page meaning and can enable rich results when guidelines are met.

### Title links
Source: https://developers.google.com/search/docs/appearance/title-link

Current working facts:
- Google uses multiple sources for title links, including title elements, visual titles, headings, og:title, anchor text, and more.
- Titles should be descriptive and concise.

### Snippets / meta descriptions
Source: https://developers.google.com/search/docs/appearance/snippet

Current working facts:
- Google primarily creates snippets from page content, but may use meta descriptions when useful.
- Meta descriptions do not guarantee displayed snippets.

### Crawl budget
Source: https://developers.google.com/search/docs/advanced/crawling/large-site-managing-crawl-budget

Current working facts:
- Crawl efficiency matters more for large sites.
- Avoid long redirect chains, soft 404s, and inefficient pages.
- Keep sitemaps updated.

### Googlebot 2 MB crawler processing
Source: https://developers.google.com/search/blog/2026/03/crawler-blog-post

Current working facts:
- Google's newer crawler explanation says Search processing uses a 2 MB limit for HTML/text-based responses.
- The limit includes HTTP response headers plus body.
- PDFs are treated differently with a higher limit.
- Important content, links, and structured data should appear before the cutoff.

## Google / web.dev agent-friendly sources

### Build agent-friendly websites
Source: https://web.dev/articles/ai-agent-site-ux

Current working facts:
- Agents may interpret sites through screenshots, raw HTML, and the accessibility tree.
- Semantic HTML, stable layouts, clear actions, real buttons/links, and accessibility tree clarity matter for agent usability.
- This is a web.dev/Chrome/Web Platform resource, not a confirmed Google Search ranking-factor announcement.

### Accessibility tree
Source: https://web.dev/articles/the-accessibility-tree

Current working fact:
- The accessibility tree is a browser-generated representation used by assistive technologies and exposes roles/names/states.

## OpenAI official sources

### OpenAI crawlers
Source: https://platform.openai.com/docs/bots

Current working facts:
- `OAI-SearchBot` is used to surface websites in ChatGPT search.
- `GPTBot` is separate and relates to training/model improvement crawling.
- Crawler controls are independent in robots.txt.
- Allowing search crawling and disallowing training crawling can be configured separately.

## Important working distinctions

### SEO vs GEO/AEO
- Traditional SEO remains foundational.
- GEO/AEO extends SEO into AI answer extraction, citation visibility, entity clarity, and agent usability.

### Schema
- Valid schema.org markup is not the same as Google-supported rich result eligibility.
- Unsupported or irrelevant schema does not create SEO value just because it validates.

### Agent-friendly UX
- Important for future user journeys and browser agents.
- Not currently a confirmed organic ranking factor by itself.
- Strongly overlaps with accessibility, semantic HTML, and conversion UX.

### 2 MB HTML/text threshold
- Treat as a serious technical QA threshold.
- Do not panic over total page weight alone; distinguish HTML/text response size from total assets.
- Prioritize templates where important content/links/schema may fall after the cutoff.
