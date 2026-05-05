# 04 Schema / Structured Data Requirements

## Goal

Use structured data to help search engines understand content and qualify for supported rich results where appropriate.

Do not add schema just because it validates. Schema must match visible page content and a real page purpose.

## 1. Source of truth

Use Google-supported structured data features first.

Schema.org contains many types, but Google Search supports only specific feature families for Search appearance. A schema type can be valid but still provide little or no Google Search benefit.

## 2. Required implementation standards

### Use JSON-LD where possible
Google supports JSON-LD, Microdata, and RDFa, but JSON-LD is generally easiest to maintain.

### Visible-content match
Structured data must describe content visible to users on the page.

### Specificity
Use the most specific relevant type supported by Google and appropriate to the page.

### Completeness
Include required properties and recommended properties where accurate.

### Crawlability
Structured data pages and images referenced in structured data must be crawlable/indexable if they are needed for Search display.

## 3. Core schema by site type

### Most sites
- `Organization`
- `WebSite` where appropriate
- `BreadcrumbList`
- `Article` / `BlogPosting` for editorial pages
- `FAQPage` only where visible FAQ content exists and the site/page is eligible
- `VideoObject` where original video is important
- `ImageObject` / image metadata where relevant

### Review/content sites
- `Article` or `BlogPosting`
- `Review` / review snippet only when genuine visible review content exists
- `Product` only when the page is actually about a product/software entity and meets guidelines
- `SoftwareApplication` when reviewing software/apps and the visible content supports it
- `FAQPage` selectively

### Community/forum sites
- `DiscussionForumPosting`
- `ProfilePage`
- `QAPage` where the page is truly Q&A
- `BreadcrumbList`

### Local businesses
- `LocalBusiness` or subtype
- `Organization`
- `BreadcrumbList`
- `FAQPage` selectively
- `Review` only if reviews follow Google policies

### Ecommerce
- `Product`
- `ProductGroup` / product variants where appropriate
- `Offer`
- `AggregateRating` only if genuine and visible
- `MerchantReturnPolicy`
- `BreadcrumbList`

### Jobs/careers
- `JobPosting`
- `Organization`
- `BreadcrumbList`

## 4. What not to do

Do not:
- mark up hidden content
- add fake reviews
- add FAQ schema to questions not visible on-page
- use Product schema on non-product editorial pages unless it clearly fits
- mark a listicle as multiple unrelated products just to get rich results
- use unsupported schema as an SEO shortcut
- add ambiguous Review/AggregateRating markup where it is unclear what is being reviewed
- duplicate conflicting schema items without clear nesting or relationships

## 5. AI Search and schema

Schema may help clarify entities and relationships, but do not claim that schema is a confirmed ranking factor for AI Overviews, ChatGPT, or other AI answer engines.

Best current use:
- reduce ambiguity
- support entity clarity
- qualify for Google Search rich result features
- improve machine understanding where schema matches visible content

## 6. Validation workflow

Before launch:
1. Validate with Google Rich Results Test.
2. Validate with Schema Markup Validator.
3. Check rendered HTML to confirm schema is present.
4. Confirm schema content matches visible page content.
5. Confirm images/URLs referenced in schema are crawlable.
6. Check Search Console enhancements after indexing.

## 7. Page-level rule

Every page should have the minimum schema needed to accurately represent it, not the maximum schema possible.
