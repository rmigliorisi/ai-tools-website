# 10 Robots, Sitemaps, and Crawler Access Requirements

## Goal

Control crawler access deliberately without accidentally blocking important content from search or AI discovery.

## 1. Robots.txt

Use robots.txt to manage crawling, not indexing.

Good uses:
- block low-value crawl traps
- block internal search results
- block infinite parameter spaces
- block private utility paths
- reduce crawling of unimportant resources where safe

Bad uses:
- trying to remove pages from Google results
- canonicalization
- hiding pages that are already indexed
- blocking pages with noindex tags before crawlers can see the noindex

## 2. Noindex

Use noindex when:
- the page may be crawled
- but should not appear in search results

Examples:
- thin utility pages
- thank-you pages
- internal landing variants
- private-but-publicly-accessible pages
- duplicate pages that should not rank and are not canonical candidates

## 3. Sitemaps

Sitemaps should include:
- canonical URLs
- indexable URLs
- 200 status URLs
- URLs you want crawled/indexed

Sitemaps should exclude:
- redirects
- 404s
- noindex pages
- blocked pages
- canonicalized duplicates
- parameter junk
- non-strategic thin pages

## 4. Lastmod

Use accurate `lastmod` values only when content meaningfully changes. Do not update lastmod automatically for trivial template or timestamp changes.

## 5. AI crawler policy

Decide crawler access by business policy.

Common AI-related user agents:
- OAI-SearchBot: ChatGPT search/discovery
- GPTBot: OpenAI training-related crawling
- Google-Extended: Google AI model training/product improvement controls
- PerplexityBot: Perplexity crawling
- ClaudeBot / anthropic-ai: Anthropic crawling depending on current published policy

Confirm current bot names in official docs before deploying.

## 6. Example robots.txt policy

```text
User-agent: *
Disallow: /wp-admin/
Disallow: /search/
Disallow: /*?s=
Allow: /wp-admin/admin-ajax.php

Sitemap: https://www.example.com/sitemap.xml

User-agent: OAI-SearchBot
Allow: /

User-agent: GPTBot
Disallow: /
```

This is only an example. Adjust to business/legal policy.

## 7. Validation

After robots/sitemap changes:
- test robots.txt
- fetch as Googlebot
- inspect important URLs in GSC
- check AI crawler access policy
- crawl with robots respected
- crawl with robots ignored for diagnostic comparison
- monitor server logs
