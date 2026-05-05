# 08 Internal Linking Requirements

## Goal

Use internal links to improve discovery, authority flow, topical clarity, user navigation, and conversion paths.

## 1. Link eligibility

Only link to URLs that are:
- 200 status
- canonical
- indexable unless intentionally supporting non-indexable utility pages
- relevant to the source context
- useful to users
- not blocked by robots.txt
- not redirected

## 2. Source-to-destination logic

Each internal link should have a reason:
- topical relevance
- parent/child relationship
- next-step user journey
- conversion support
- authority flow to priority page
- clarification of an entity/topic
- cluster reinforcement

## 3. Anchor text

Good anchors:
- descriptive
- natural
- context-specific
- varied
- useful out of context

Avoid:
- click here
- read more
- generic repeated anchors
- exact-match overuse
- misleading anchors
- anchors that do not match destination intent

## 4. Page hierarchy

Important pages should receive links from:
- homepage or hub pages where appropriate
- relevant category/tool/profession pages
- related editorial pages
- breadcrumbs
- comparison pages
- high-authority content

## 5. Orphan prevention

Every indexable page should be:
- in the sitemap
- internally linked
- reachable within a reasonable crawl depth
- connected to its topic cluster

## 6. Link depth

Priority pages should generally be within:
- 1-3 clicks for major commercial pages
- 2-4 clicks for important supporting pages
- deeper only when intentionally low-priority

## 7. Vector embedding workflow

For larger sites, use semantic similarity to find missing links.

Suggested process:
1. Export indexable pages.
2. Create embeddings for page representations.
3. Find semantically related pages.
4. Exclude already-linked pairs.
5. Filter out non-indexable/canonicalized/redirected pages.
6. Score opportunities by relevance, priority, scarcity, and anchor quality.
7. Review manually before implementation.

## 8. Internal linking QA

Audit for:
- pages with 0 internal links
- pages with only 1 internal link
- important pages at high crawl depth
- links to redirected URLs
- links to 404s
- links to canonicalized duplicates
- nofollow internal links
- over-optimized anchors
- missing breadcrumbs
- weak hub pages

## 9. Automation guardrails

AI agents may suggest links, but should not auto-publish without approval.

Each suggestion should include:
- source URL
- destination URL
- anchor text
- insertion paragraph
- reason
- confidence
- status
