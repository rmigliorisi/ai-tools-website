# 02 AI Search / GEO / AEO Requirements

## Goal

Make pages easy for AI search systems and answer engines to understand, extract, summarize, and cite without compromising human readability or traditional SEO.

## Important distinction

AI Search / GEO / AEO is not a replacement for SEO. It is a layer on top of crawlability, indexability, page quality, technical health, topical authority, brand/entity clarity, trust signals, and external mentions.

## 1. Answer-led structure

Important pages should include concise, extractable sections near the top.

### Recommended pattern
- Short intro
- Direct answer / verdict
- Key takeaways
- Who it is for
- Who it is not for
- Comparison or decision table where useful
- Detailed body content
- FAQ only if useful and visible

### Good answer block
A good answer block can stand alone if copied into an AI-generated response.

```text
ChatGPT is best for professionals who need a flexible general-purpose AI assistant for writing, research, analysis, brainstorming, and workflow support. It is less ideal for teams that need highly specialized, regulated, or fully automated workflows without human review.
```

### Avoid
- burying the answer after 800 words
- vague intros
- long brand storytelling before answering
- generic AI-written statements
- unsupported claims
- answer boxes stuffed with too many bullets

## 2. Entity clarity

Every important page should make clear:
- who the page is about
- what product/service/tool/entity is being discussed
- what category it belongs to
- who it helps
- what problem it solves
- what the current year/version/context is
- whether the page is a review, guide, comparison, opinion, documentation, or landing page

## 3. Information gain

AI-search visibility is more likely when pages contain information that is hard to infer from competitors.

Prioritize:
- original data
- screenshots or first-hand testing
- named methodology
- examples from real workflows
- unique pros/cons
- decision criteria
- pricing/compliance caveats
- expert quotes or reviewer notes
- current limitations
- comparisons based on actual use cases

Avoid:
- generic definitions
- recycled competitor summaries
- listicles with no evidence
- best claims without criteria
- content that could be produced from the SERP alone

## 4. Extractable summaries

Each major section should have:
- a clear heading
- a short answer or summary
- supporting detail
- examples where useful

Use concise declarative language for key facts.

## 5. Brand and source consistency

For AI search, entity consistency matters across the open web.

Maintain consistent:
- brand name
- author names
- organization details
- product names
- social profiles
- about page
- contact details
- editorial policy
- author/reviewer pages
- sameAs links in Organization schema where appropriate

## 6. Technical accessibility for AI retrieval

Important content should:
- appear in initial HTML or reliably rendered HTML
- not require login unless intentionally private
- not require click/scroll-only loading
- not be blocked by robots.txt if you want discovery
- not be hidden inside images
- not be dependent on fragile client-side rendering

## 7. AI crawler access

If the site wants visibility in ChatGPT search, allow `OAI-SearchBot` unless there is a policy reason not to.

Training access is separate. `GPTBot` and `OAI-SearchBot` should be considered independently.

Example robots.txt policy:

```text
User-agent: OAI-SearchBot
Allow: /

User-agent: GPTBot
Disallow: /
```

This allows search discoverability while opting out of training-related crawling. Adjust based on business/legal policy.

## 8. GEO measurement

Track:
- AI Overview visibility manually or via tools
- ChatGPT/Perplexity/Gemini citation presence
- branded search lift
- direct/referral lift
- assisted conversion changes
- query/page visibility changes
- entity co-occurrence in third-party mentions
- referral strings where available

Be honest that AI-search attribution is still immature.

## 9. What is confirmed vs speculative

### Higher-confidence practices
- crawlable, accessible content
- clear answers
- strong entity signals
- original data
- third-party mentions
- clean technical foundations
- consistent brand information

### Still uncertain
- exact citation-weighting formulas
- exact role of schema in each AI answer system
- llms.txt adoption across major systems
- how different LLMs weight Bing/Google/Common Crawl/partner data
- precise conversion attribution from AI-generated answers
