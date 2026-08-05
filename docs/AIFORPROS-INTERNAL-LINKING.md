# Internal Linking Guide — AI Tools for Pros

Editorial policy and governance for how internal links get added to `tool_review`, `profession_hub`, and `cross_reference` pages, both by hand and by any future automation. Written after the August 2026 internal-link audit found 65 broken links, 5 same-paragraph repetitions, and generic anchor text across all 41 `cross_reference` pages, and confirmed 76 places where a sibling tool is reachable only via a table or footer list, with no genuine mention in the body text.

This document is the **editorial constitution**: what a good link is, what a bad link is, who can change what without review. Machine behavior — modes, scoring, schemas, thresholds, rollback — belongs in the companion file, `AIFORPROS-INTERNAL-LINKING-AUTOMATION-SPEC.md`. That spec must satisfy every rule here; if it can't, this document wins and the spec changes, not the other way around.

## 0. Document control

- **`policy_version`**: 1.3.0
- **Effective date**: 2026-08-05
- **Owner / approver**: Rich Migliorisi (site owner)
- **Change log**:
  - 1.3.0 (2026-08-05) — Authorized auto-apply for contextual link additions on `cross_reference` pages, narrowly: ONLY when proposed by the specific built pipeline (`linking_scoring.py`'s hard-gated verdict, then `linking_apply.py`'s fail-closed write protocol — live re-check of both sides of the pair immediately before writing, decode-JSON replace, post-write re-fetch verification, capped batch size, append-only change log). §16 set this exact bar in advance — "after the fail-closed write protocol, versioned backups, acceptance tests, and rollback procedures defined in the automation spec are in place and demonstrated" — and it has now been built and demonstrated (see §11, §14, §15, §16 for the specific wording changes). This does NOT make "adding a new contextual link" broadly auto-safe (§15) — a link proposed by hand, by a different script, or by this pipeline with a record that failed a live re-check remains review-required. `tool_review` and `profession_hub` remain audit-only (§11); nothing here changes that.
  - 1.2.0 (2026-08-03) — Added a sixth evidence classification, `SITE_PUBLISHED_CONTENT` (§1), discovered while building the contextual-link scoring step: reusing a sibling page's own already-published, already-researched content (e.g. its `consistency_blocks` or feature descriptions) as the evidentiary basis for a new cross-page claim didn't fit any of the original five categories. This is distinct from `SITE_GOVERNANCE_RULE` (a policy decision) and from citing external vendor documentation directly.
  - 1.1.0 (2026-08-03) — Resolved the contextual-link contradiction (§2 vs. former §11); added stable rule IDs, precedence rule, and normative-language definitions; separated source/target/audit-only/excluded page scope; defined `cross_reference` relationship vocabulary; narrowed the "safe automatic correction" classes to operational conditions; formally defined "verified information" and added an evidence-record requirement; corrected an evidence-tag error (crawler user agents were mislabeled `OFFICIAL_GOOGLE_GUIDANCE`); moved volatile product-fact examples to a dated, non-normative appendix.
  - 1.0.0 (2026-08-03) — Initial version.
- **Normative language** (RFC 2119-style): **MUST** / **MUST NOT** = non-negotiable; **SHOULD** / **SHOULD NOT** = strong default, deviation needs a stated reason on record; **MAY** = permitted, not required.
- **Precedence rule**: when rules or change classifications overlap or conflict, precedence is **prohibited change > review-required change > auto-safe change**. An auto-safe exception applies only when *every* condition defined for that exact change class (§12) is satisfied; any uncertainty routes the item to review. Every logged proposal or decision MUST record the stable rule ID(s) it relies on and the `policy_version` in effect at the time.

## 1. Evidence classification

Every guidance point below is labeled with where it actually comes from, so the automation's decision log can distinguish "Google told us this" from "the tool vendor told us this" from "an SEO blog observed this" from "we decided this ourselves." Don't treat these the same:

- **`OFFICIAL_GOOGLE_GUIDANCE`** — stated directly in Google's own developer documentation.
- **`OFFICIAL_VENDOR_DOCUMENTATION`** — stated directly in a non-Google vendor's own documentation (e.g., OpenAI, Anthropic, or Perplexity documenting their own crawler's behavior).
- **`LEAK_DIRECTIONAL`** — an attribute or field name exposed in the May 2024 Content Warehouse API leak. Confirms Google's systems *track* something; does not confirm weight or current behavior. Directional context, not a ranking-factor citation.
- **`INDUSTRY_OBSERVATION`** — a pattern reported by SEO practitioners/tools, not by Google or the relevant vendor. Useful, not authoritative.
- **`SITE_GOVERNANCE_RULE`** — a rule this project has chosen to adopt, independent of any external source, usually to keep automation safe.
- **`SITE_PUBLISHED_CONTENT`** — a claim grounded in content already live on this site, itself previously researched and reviewed (e.g. via System 1's vendor-verification pipeline) — such as a sibling page's own `consistency_blocks` or feature description being cited as the reason a contextual link to it is genuine. Distinct from `SITE_GOVERNANCE_RULE` (a policy decision, not a factual claim) and from citing a vendor's documentation directly (`OFFICIAL_VENDOR_DOCUMENTATION`). A claim in this category is only as reliable as the site content it points to — it does not independently re-verify that content against the vendor.

## 2. The core principle — `SITE_GOVERNANCE_RULE` [GOV-LINK-001]

A link earns its place by being genuinely useful to a reader at the exact point they encounter it. Not by filling a quota, not by matching a table row, not by "we should probably link to that page somewhere."

- **`OFFICIAL_GOOGLE_GUIDANCE`** — *"There's no magical ideal number of links a given page should contain. However, if you think it's too much, then it probably is."* ([Google Search Central](https://developers.google.com/search/docs/crawling-indexing/links-crawlable))
- **`OFFICIAL_GOOGLE_GUIDANCE`** — *"Try reading only the anchor text (out of context) and check if it's specific enough to make sense by itself."* If it isn't, the anchor text is too generic.

## 3. Placement hierarchy — where a link should live, in order of value [GOV-LINK-002]

1. **In-body, contextual (highest value).** Supported by `OFFICIAL_GOOGLE_GUIDANCE` that *"the words before and after links matter, so pay attention to the sentence as a whole."* A link that appears at the exact moment a reader is evaluating a specific tradeoff.
2. **Structured comparison elements (tables).** Useful and expected — readers scanning a comparison table expect to click through.
3. **Closing "see also" / footer lists.** Fine as a catch-all and for links with no natural home elsewhere (tool overview, profession hub).

**[GOV-LINK-003] A table or footer link does not, by itself, count as contextual coverage.** It MAY remain the only link to a sibling page for a given source–target pair **when no genuine, relevant, and verifiable contextual opportunity exists** for that specific pair (see §11 for the decision process and §14's "safe candidates" for what may be changed without review). That conclusion MUST be recorded per source-page/target-page pair; it MUST NOT be assumed or left undocumented.

The preferred remedy, **when a genuine opportunity exists**, is a contextual mention (§8) — not "always add one regardless." The August 2026 audit found the opposite of the ideal distribution on 32 of 41 pages: a sibling tool linked only in the table/footer, with no in-body mention. Closing that gap is the goal; manufacturing a mention where none is warranted is not (§8, §11, §14).

## 4. Anchor text rules

- **`OFFICIAL_GOOGLE_GUIDANCE`** — Descriptive over generic. "Claude for Architects" beats "Claude" beats "click here." This is the bug fixed site-wide in the August 2026 anchor-text pass (all 41 `cross_reference` footer lines had a bare first link next to two descriptive siblings).
- **`OFFICIAL_GOOGLE_GUIDANCE`** — Concise, not stuffed. Don't cram every related keyword into the anchor. If it feels forced, it's too much.
- **`OFFICIAL_GOOGLE_GUIDANCE`** — Don't chain links together; Google explicitly calls out stacking several links back-to-back as bad. This site avoids that by design; automation MUST preserve it.
- **`SITE_GOVERNANCE_RULE` [GOV-LINK-004]** — Anchor diversity SHOULD be evaluated for naturalness at the page and site level. Fixed exact-match/partial-match percentages MUST NOT be enforced — that's an industry heuristic, not Google guidance, and an automation chasing a ratio produces unnatural-sounding anchors, the exact failure mode this document exists to prevent. Instead, the automation MAY report repeated anchor patterns (most-used anchor per target, page count, percentage of links to that target, semantic variants) for human review — it MUST NOT auto-correct toward a predetermined mix.

## 5. What the 2024 Google API leak adds — `LEAK_DIRECTIONAL`

The May 2024 Content Warehouse API leak exposed internal attribute and field names. This is not confirmed ranking-weight documentation — it shows what Google's systems evidently track, not how much it matters or whether current behavior matches.

- Fields associated with weighting links by placement — main content versus sidebar/footer/boilerplate navigation. Supports §3: the mega-nav and footer directory on every page here are boilerplate and shouldn't be relied on as "the" link to a page.
- A `siteAuthority` field and internal PageRank-style computation for distributing authority between a site's own pages via internal links.
- Spam-velocity fields (`phraseAnchorSpamDays`, `phraseAnchorSpamDemoted`, `LINK_SPAM_PHRASE_SPIKE`) associated with sudden spikes of repeated, matching anchor phrases.

**[GOV-LINK-005] Operational conclusion:** any batch of automated link additions SHOULD roll out in controlled batches so changes can be reviewed, measured, reverted, and prevented from creating repeated anchor or placement patterns. This is justified by quality control and reversibility, not by asserting a specific ranking interpretation as fact.

(Sources: [Search Logistics leak summary](https://www.searchlogistics.com/learn/seo/link-building/leaked-lessons/), [Vizion Interactive leak review](https://www.vizion.com/blog/everything-you-need-to-know-about-the-google-leak-misstatements-and-api-revelations/), [ipullrank leak analysis](https://ipullrank.com/google-algo-leak), accessed 2026-08-03)

## 6. AI crawlers and content-use controls relevant to this site

- **`OFFICIAL_VENDOR_DOCUMENTATION`** — Crawler user agents relevant to this site: **GPTBot** (OpenAI's own documentation), **ClaudeBot** (Anthropic's own documentation), **PerplexityBot** (Perplexity's own documentation). These are actual HTTP user agents that fetch pages, each documented by its own operator — not by Google.
- **`OFFICIAL_GOOGLE_GUIDANCE`** — **Google-Extended is not a crawler.** It's a `robots.txt` product token; Google's own documentation states its existing crawlers do the fetching, while `Google-Extended` separately controls whether that already-crawled content may be used for Gemini training and grounding. ([Google for Developers](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers), accessed 2026-08-03)
- **`SITE_GOVERNANCE_RULE` [GOV-LINK-006]** — Access status (allow/disallow, per token) MUST be re-verified against the live `robots.txt` file during each technical audit. A previously documented configuration MUST NOT be assumed still active — this is a live-site condition, not a fact about this evergreen document.

## 7. AEO / GEO considerations (AI answer engines) [GOV-LINK-006A]

- **`INDUSTRY_OBSERVATION`** — What gets an AI engine to *cite* a page, versus just index it, appears distinct from classic ranking: clear, well-sourced, well-structured content that directly answers a specific question tends to perform across both search and AI-answer surfaces. ([ALM Corp AEO playbook](https://almcorp.com/blog/answer-engine-optimization-2026/), [WRITER GEO/AEO/SEO guide](https://writer.com/blog/geo-aeo-optimization/), accessed 2026-08-03)
- **`SITE_GOVERNANCE_RULE`** — Contextual links are more useful for AI retrieval/answer-generation systems because the surrounding passage supplies semantic context for the relationship between two pages. Treat this as a content-architecture principle, not a confirmed weighting factor for any specific proprietary system — we have no visibility into those internals.

## 8. What counts as a genuine contextual mention [GOV-LINK-007]

A genuine contextual mention MUST:

- Address a specific reader need, limitation, workflow, or tradeoff.
- Explain *why* the linked page or tool is relevant at that point.
- Fit naturally into the surrounding paragraph (not a bolted-on aside).
- Be supported by **verified information** (defined below) — not an invented or unconfirmed claim.
- **Remain useful even if the hyperlink were removed.** If a sentence exists only to contain an anchor, it fails this test and MUST NOT be used.

Does **not** qualify: a standalone recommendation ("You can also consider Claude for architects."), a generic "see also" sentence, or any sentence written only to contain a link. The "useful without the hyperlink" test is the single most important check on an AI-generated linking suggestion — apply it before anything else.

### Verified information — definition [GOV-LINK-008]

A claim is "verified" for the purposes of this document only when there is an **evidence record** containing, at minimum:

- The specific claim being supported.
- A primary source URL (vendor documentation, official pricing page, etc.) or an approved internal source.
- The source's publisher/class (e.g. `OFFICIAL_VENDOR_DOCUMENTATION`, `SITE_GOVERNANCE_RULE`).
- A retrieval or verification date.
- The supporting passage or structured field, quoted or referenced directly.
- A freshness status (current / needs re-check / stale).
- The reviewer's name, when manually verified.

**Existing page content is not automatically "verified" just because it's already published.** Already-published text may itself be stale, circular (citing another page on this site that cites it back), or unsupported. A proposal that reuses an existing claim MUST trace it back to the evidence record above, not merely to "it's already on the page." The full evidence-record schema and storage mechanism is defined in the automation spec.

## 9. Duplicate-link policy [GOV-LINK-009]

- Default to **one** contextual link to a given target within the main body of a page.
- A second in-body link to the same target MAY appear only when: the page is long, the second occurrence serves a materially different reader intent than the first (a distinct comparison point, not a restatement), and the two links are separated by substantial content.
- **A target MUST NOT be linked twice within one paragraph.** This is the exact pattern fixed in the August 2026 "same breath" repetition cleanup (5 instances across 5 pages).
- Tables, Related Guides cards, main navigation, and footer links are tracked **separately** from in-body duplication. A table link plus one in-body contextual link to the same target is normal and expected, not a duplicate under this policy.
- Before proposing a new in-body link, the system MUST check for existing links to the same target anywhere on the page — not only within the same paragraph.

## 10. Link-eligibility checklist [GOV-LINK-010]

Before proposing or inserting any internal link, the target MUST pass all of the following. (Precise machine semantics — normalization, canonical equality, status-code handling — are defined in the automation spec; an item whose eligibility cannot be determined MUST be treated as ineligible, not assumed eligible.)

1. The target URL is on `aitoolsforpros.com`.
2. It resolves successfully (not a 404/5xx).
3. It is not a redirect, unless an authoritative URL map explicitly approves the destination.
4. It is canonical and indexable.
5. It is not an unnecessary self-link to the source page. Intentional same-page fragment navigation (e.g. `#pricing` jump links) is outside the scope of this contextual internal-linking policy.
6. It is published (not draft, private, or scheduled).
7. It is relevant to the surrounding text (§8).
8. It is not already linked elsewhere on the same page in a way that would violate §9.
9. Its anchor text is descriptive of the destination (§4).
10. The proposed link does not require stating an unsupported factual claim to justify it (§8).

## 11. Scope — allowed source types, target types, audit-only types, excluded types [GOV-LINK-011]

- **Allowed source types (Phase 1 — may be inspected AND edited, under auto-apply per §14/§16 when proposed by the built pipeline, otherwise review-required):** `cross_reference`. This is the page type the current gap-filling project targets, and where this document is currently strongest.
- **Audit-only source types (may be inspected and reported on, MUST NOT be edited yet):** `tool_review`, `profession_hub`. Graduating either into an editable source type requires an explicit revision to this document, not a quiet expansion of scope.
- **Allowed target types (valid link destinations, always):** `tool_review`, `profession_hub`, `cross_reference` — provided each individually passes §10.
- **Excluded target types:** internal/non-public post types (`aifp_update`, `aifp_subscriber`, `aifp_contact`, `aifp_update_log`); static utility pages (`/contact/`, `/newsletter/`, `/privacy-policy/`, `/cookie-policy/`, `/about-us/`, `/our-process/`); any external domain (this document governs internal links only); media/attachment URLs; any URL not matching one of the three canonical post-type permalink patterns.

## 12. `cross_reference` relationship vocabulary [GOV-LINK-012]

A `cross_reference` page represents exactly one (tool × profession) pair, not a direct "tool vs. tool" comparison page. To avoid the ambiguity of phrases like "both tools being compared," this document defines:

- **`primary_tool`** — the tool this specific `cross_reference` page is about, per its `linked_tool` post-meta (e.g., for `claude-finance`, the primary tool is Claude).
- **`profession`** — the profession this page is about, per its `linked_profession` post-meta (e.g., Finance).
- **`sibling_tool`** — any other tool (not the primary tool) that has its own `cross_reference` page for the *same* profession.
- **`sibling_cross_reference`** — the specific `cross_reference` page representing (`sibling_tool`, `profession`) — e.g., `chatgpt-finance` is the sibling cross-reference of `claude-finance` for the ChatGPT sibling.

The comparison table and "Comparing your options" footer on a `cross_reference` page link to that page's `sibling_cross_reference` pages. Every gap-filling decision in §14 operates on one (`source cross_reference page`, `sibling_tool`) pair at a time — not on "the page" as a whole (see §14).

## 13. Page-type-specific link rules

### `tool_review`
Expected link relationships: relevant profession implementations (this tool's `cross_reference` pages); direct tool-to-tool comparison pages where they exist; workflow/guide pages relevant to actual usage; verified alternatives where a genuine limitation is discussed; the tool's own overview/parent page where structurally necessary (e.g. breadcrumbs). Automation MUST NOT add every profession page to every tool review — link only where the specific profession is actually relevant to the point being made. (Audit-only per §11 until this document is revised.)

### `profession_hub`
Expected link relationships: tool pages genuinely relevant to that profession; supporting workflow/guide content; cross-tool comparisons tied to a specific professional task; the parent profession directory where applicable. Prioritize task relevance over exhaustive tool coverage. (Audit-only per §11 until this document is revised.)

### `cross_reference`
Expected link relationships (using §12's vocabulary): the page's own `primary_tool` context; relevant `sibling_cross_reference` pages; the `profession_hub` for this page's profession; the `tool_review` for `primary_tool`; contextual alternatives among `sibling_tool`s, when verified (§8) and naturally relevant to a specific limitation or use case. This is the only Phase 1 editable source type (§11) and where the current gap-filling project is focused.

## 14. Practical rules for closing the `cross_reference` contextual-link gaps [GOV-LINK-013]

The **atomic unit of decision is one (`source cross_reference page`, `sibling_tool`) pair** — not "the page" as a whole. A single source page legitimately produces different outcomes for different siblings (e.g., an opportunity for Claude, no opportunity for Gemini, a needs-review case for ChatGPT). The exact record schema (identity, workflow state, expiration) is defined in the automation spec; this section defines the policy those records must satisfy.

For each (source page, sibling) pair currently reachable only via table/footer (§3):

1. **If a genuine, relevant, verifiable (§8) contextual opportunity exists** — a contextual in-body mention SHOULD be proposed and logged. As of policy_version 1.3.0, a proposal produced by the built pipeline (`linking_scoring.py`) that clears its hard gates (`useful_without_link` true, quoted `evidence_supporting_text` present) MAY be applied by `linking_apply.py` without a human approving that specific instance — but only through that pipeline's fail-closed write protocol (§16). A contextual link proposed any other way (by hand, by a different tool, or a pipeline record that failed a live re-check at apply time) remains review-required and MUST NOT be published without human approval (§15).
2. **If it's unclear whether a genuine opportunity exists** — the pair MUST be routed to human review (or, in the built pipeline, to `needs_evidence` / `needs_editorial_review`, which are held states, not published), not decided by the system as a positive.
3. **If no natural opportunity exists** — the table/footer link MUST remain as the only link for that pair. When this conclusion is reached by a human, it is recorded as `no_contextual_opportunity` for that specific pair. When reached by the built pipeline's model as `no_opportunity_proposed`, it is NOT auto-finalized to `no_contextual_opportunity` — that transition still requires a human actor (automation spec §6b); the record simply stays unlinked and open to re-evaluation next audit run. **A model confidence score alone MUST NOT finalize a negative outcome as permanent** — only that it found nothing to apply this run. A confirmed `no_contextual_opportunity` conclusion SHOULD expire and be re-evaluated if the source page, target page, this policy, or the supporting evidence record changes.

Additional rules:

- Do not invent a reason (§8's "useful without the hyperlink" test governs this).
- Vary anchor text across pages for the same target (§4) — don't let every page mentioning Claude use the literal string "Claude"; match what's actually being discussed at that point.
- Batch any automated rollout (§5) — spread writes out; do not push all outstanding gap-fills in one commit. The built pipeline enforces this mechanically (automation spec §14's caps), not just as a stated intention.
- Human review before publish remains the default for every change class except the one narrow auto-apply path defined in this section and §15/§16.

## 15. Change classification — what may be touched automatically [GOV-LINK-014]

Precedence (§0): **prohibited > review-required > auto-safe.** An auto-safe class applies only when *every* stated condition for that exact class is met; any uncertainty routes to review, never to auto-apply.

- **Safe candidates for automatic correction** — each defined operationally, not just by name:
  - *Broken/canonical URL correction*: auto-safe only when an authoritative URL map identifies **exactly one** replacement representing the same content entity (e.g. a slug rename with a 1:1 mapping). A merely similar or topically-related page is a **target replacement**, which is review-required, not auto-safe.
  - *Duplicate hyperlink removal*: auto-safe only when the same normalized target occurs twice within the same paragraph and the edit removes exactly one `<a>` wrapper without changing any visible text. If choosing *which* occurrence to unlink requires judgment (e.g. they're not textually adjacent, or the two mentions serve different purposes), it is review-required.
  - *Malformed markup repair*: auto-safe only for allowlisted, deterministic transformations that preserve visible text, block structure, all attributes, and every unrelated link on the page.
  - *Redirect correction*: auto-safe only with a stable, verified redirect or authoritative canonical mapping — never a single transient HTTP response.
- **Review-required changes:** adding a new contextual link; changing anchor wording; adding or modifying a comparison sentence; removing a link because it appears unnecessary; replacing one link target with a different page; making any claim about product capabilities, pricing, limits, privacy, or suitability. **Exception, added in 1.3.0:** adding a new contextual link to a `cross_reference` page is auto-safe, without a human approving that specific instance, ONLY when produced end-to-end by the built pipeline (`linking_scoring.py`'s hard-gated verdict + `linking_apply.py`'s live re-checks and fail-closed write) — every other path to adding a contextual link remains review-required exactly as before.
- **Prohibited without explicit governance approval:** inventing new facts to justify a link; rewriting multiple paragraphs to manufacture link opportunities; adding links solely to hit a coverage target (e.g. treating "close all N gaps" as a number to hit, divorced from §8's test); publishing AI-written comparisons without verification; **altering affiliate links, schema, calls to action, citations, or page templates as part of an internal-linking pass, under any circumstance, including within an otherwise auto-safe change.**

## 16. Path to automation [GOV-LINK-015]

Human approval is the default for contextual additions and any meaning-changing edit. An auto-apply mode may be enabled for a specific change class only after the fail-closed write protocol, versioned backups, acceptance tests, and rollback procedures defined in the automation spec are in place and demonstrated — not assumed. Technical corrections meeting an auto-safe class's full conditions (§15) may be auto-applied earlier than that. AI-generated comparison claims remain review-required unless this document is explicitly revised to say otherwise.

**As of policy_version 1.3.0 (2026-08-05), this bar has been met for exactly one class: contextual link additions to `cross_reference` pages, proposed end-to-end by the built pipeline.** What was demonstrated before this was authorized: `linking_scoring.py`'s hard gates (a model's own `opportunity_proposed` verdict is overridden to `needs_editorial_review` or `needs_evidence` if it lacks `useful_without_link` or a quoted evidence sentence — the model cannot talk its way past these); `linking_apply.py`'s live re-checks immediately before writing (target page still eligible, `existing_text` still present exactly once on the source page — never trusting a proposal's age); the decode-JSON/replace/re-fetch-verify write pattern already proven safe on System 3's unattended monthly runs; a hard cap (5 applied per run, 1 per source page per run) with FIFO backlog for overflow; and an append-only change log recording enough detail (record_id, exact old/new text, evidence, timestamp) to manually revert any single change. Every other change class in §15 — including contextual links proposed any other way — still requires human approval before publish. Expanding auto-apply to another change class or another source page type requires the same bar: built, demonstrated, then an explicit revision to this document, not a quiet expansion of scope.

## 17. Appendix: illustrative examples (non-normative, dated)

Examples below illustrate a *type* of claim, not a currently-verified fact. Any specific product detail (context window size, pricing, plan names) changes over time and MUST be re-verified against current vendor documentation before being used in an actual proposal — do not copy a number from this appendix into content.

- Example of the *kind* of tradeoff a genuine contextual mention describes: "[Tool]'s larger context window handles full-document review in one pass, where a smaller-context tool requires chunking." (Illustrative only — as of this document's last revision, this site's own content is inconsistent about the exact context-window figures across pages, which is itself a separate, open content-accuracy issue outside this document's scope, not a template to copy.)

## 18. Companion document

Machine behavior — operating modes, workflow states, opportunity scoring, confidence thresholds, the audit-output schema, before/after diffs, fingerprinting, per-page/per-run change caps, the fail-closed write protocol, validation/acceptance tests, rollback, scheduling, the change log, security handling of untrusted page content, and quality metrics — lives in `AIFORPROS-INTERNAL-LINKING-AUTOMATION-SPEC.md`. That spec must satisfy every rule in this document. This document should change rarely, with each change recorded in §0; the spec will change more often as the system is designed and built.
