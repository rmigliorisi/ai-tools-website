# Automated Content — Weekly Tool Updates & Monthly AI Updates Page

This defines two automated content systems for aitoolsforpros.com, run on a schedule with no
daily human involvement, but with different risk postures matched to what each one touches.

| System | Touches | Cadence | Goes live |
|---|---|---|---|
| Weekly Tool Page Updates | Existing, already-published `tool_review` pages | Weekly | Automatically, no approval step |
| Monthly AI Updates Page | New page at `/[month]-[year]-updates/` | Monthly | Only when Rich clicks Publish |
| Monthly Editorial Review | Existing `cross_reference` (41) / `profession_hub` (8) pages | Monthly | Suggest-only — Rich approves each change before anything is applied |

The difference in risk posture is deliberate. Weekly updates are factual maintenance on pages a
human already wrote and vetted — small, verifiable deltas (a price changed, a feature shipped).
The monthly page is new editorial content making judgment calls about what counts as
noteworthy — that stays a human decision.

Both systems share one non-negotiable principle: **fail closed.** If a fact can't be confirmed
with a real, current source, the system does not guess. It leaves the existing text alone (or
adds a `[VERIFY DETAILS]` flag, per the existing flag system in CLAUDE.md) rather than publish
an uncertain claim unattended.

---

## System 1: Weekly Tool Page Updates (auto-publish)

### Purpose

Keep the 10 `tool_review` pages factually current — pricing, plan names, features, HIPAA/compliance
status — without Rich having to manually re-check 10 vendor sites every week. This is the same
job the `[VERIFY DETAILS]` flag already does manually; this system does it on a schedule.

Freshness is also a direct AEO/GEO signal, not just accuracy upkeep. Recent data shows the large
majority of AI citations for commercial/evaluation queries come from pages updated within the past
12 months, and pages left unrefreshed for a full quarter are markedly more likely to lose AI
citations than recently updated ones. Weekly updates keep these pages inside that freshness window,
which is a second, independent reason (beyond factual accuracy) this system runs on a schedule
instead of ad hoc.

### Schedule

Weekly, recommended **Monday morning**, so any changes are visible for the rest of the week.

Runs as a **GitHub Actions workflow** (`.github/workflows/weekly-tool-update.yml`), not a Cowork
scheduled task. Cowork's sandbox cannot make authenticated writes to any external host — outbound
HTTPS to third-party services is blocked at the proxy, confirmed by testing both `git push` and a
plain authenticated `GET` against the WP REST API from inside a Cowork session. A GitHub Actions
runner has normal outbound network access, so that's where the actual research-and-write logic
(`automation/weekly_tool_update.py`) lives and runs. Cowork remains the place for one-off/interactive
work (the monthly page, ad hoc fixes) but isn't the execution environment for a recurring
unattended job that needs to reach the live site.

### How the research step works

Each of the 10 tools gets one Claude API call using the **web search tool**
(`web_search_20250305`), with `allowed_domains` locked to that vendor's own official site(s) —
Claude physically cannot cite a result from outside that list. This is what makes the "vendor's
own official page" confidence tier in the QA gate meaningful rather than just self-reported.
Findings come back as structured JSON (value, source URL, confidence tier) and are diffed against
the live page's decoded content before anything is written. Cost is bounded and small: at most 5
searches per tool × 10 tools × 52 weeks/year, at $10 per 1,000 searches plus token costs — a
few dollars a year, not a metered per-user cost like the chatbot idea that was passed on earlier.

### Process

1. **Research** — for each of the 10 tools (ChatGPT, Claude, Cursor, Gemini, Grammarly, Copilot,
   Midjourney, Notion AI, Otter.ai, Perplexity), search the vendor's official pricing page,
   changelog/release notes, and blog for anything published or changed since the last run.
   Never rely on model memory for pricing or feature claims — every candidate change must trace
   back to a fetched source URL from this run.
2. **Fetch current state** — `GET` the post via the WP REST API (`/wp-json/wp/v2/tool_review/{id}`)
   and `json_decode` its `content` field. This site does **not** use ACF postmeta as the data
   source — every `tool_review`/`profession_hub`/`cross_reference` page stores its entire
   structured data as a JSON object inside `post_content`, read back by `aifp_get_data()` in
   `inc/helpers.php`. (`acf-fields.php` is a dormant editing-UI blueprint, not the real data
   path — confirmed against both `helpers.php` and `migrate_v2.py`'s `create_post()` /
   `safe_json_content()`, which is what actually populated these pages.) So "current state" means
   the full decoded JSON object, not a set of ACF fields.
3. **Diff** — compare researched facts to the current values inside that decoded object. Only
   keys with an actual, sourced change become candidate edits. No wholesale rewrites.
4. **Guardrail QA** (below) — every candidate edit passes through the QA gate before it's applied.
5. **Apply** — modify only the specific keys that changed in the decoded object (e.g.
   `quick_facts.pricing_fact`, one entry inside `features`), re-serialize the *entire* object with
   `json_encode`, and `POST` (with `X-HTTP-Method-Override: PUT`) that full string back as the
   post's `content` field — the same `create_post()` pattern `migrate_v2.py` already uses to write
   these pages, just reading-modifying-writing instead of writing fresh. There is no way to PATCH
   a single key at the REST layer since the whole object lives in one `content` string; the
   discipline is in only *changing* specific keys locally before the write, not in what the REST
   call touches. Bump `publish_date` only if the page's substantive content changed — not on
   every run.
6. **Log + notify** — every change (applied or held) gets logged and summarized in a weekly
   digest, even though nothing is gated on approval. See "Visibility" below.

### Fields this system is allowed to touch

Mapped to the JSON keys actually read by `single-tool_review.php` / `template-parts/quick-facts.php`
via `aifp_get_data()` (these happen to share names with the `acf-fields.php` blueprint, since that
file documents the same schema — just isn't the live data path):

**Eligible (factual, objective):**
- `quick_facts.made_by`, `quick_facts.pricing_fact`, `quick_facts.custom_fact_label` /
  `custom_fact_value`, `quick_facts.hipaa_fact`
- `pricing_tiers` (repeater: `tier_name`, `tier_price`, `tier_features`)
- `features` (repeater, fixed at 7 items — update `feature_description` when a listed feature
  changes materially; do not add/remove items, that's an editorial call)
- `sources` (repeater, fixed at 5 items — rotate in a new source only when it directly backs a
  change made this run; never exceed the existing min/max)

**Off-limits — editorial voice, never auto-edited:**
- `consistency_blocks.*` (Bottom Line, Key Takeaway, Best For, Avoid If, Mini Workflow)
- `verdict_text` ("Our Verdict")
- `what_it_is`, `who_its_right_for`
- `subtitle`

If a researched change would logically affect the verdict or a consistency block (e.g., a price
increase big enough to change whether the tool is still "Best For" a given budget), the system
does **not** rewrite that field. It applies the factual field update and adds a note to the
weekly digest flagging that the verdict may need a human look. This is the one place automation
defers to editorial judgment even in an otherwise fully automated run.

### SEO / internal linking requirements

- Any new fact that references a feature or plan already covered on a related cross-reference
  page must not introduce a contradiction — cross-check the same fact isn't stated differently
  on a linked `cross_reference` page for that tool. If it is, hold the change and flag it (a
  cross-tool inconsistency is worse than a stale single page).
- No new outbound links are added to page body content by this system. Sources go in the
  `sources` repeater only (per the existing `[N] Vendor — description` format, no raw URLs),
  matching the "no dead links" and "Sources Checked" rules already in CLAUDE.md / AIFORPROS-QA.md.
- Internal links already on the page are validated to still resolve (no 404s) before the run
  completes.

### Guardrail / QA gate (must pass before anything applies)

Every candidate change is scored, not just spot-checked. Structure this like the existing
`AIFORPROS-QA.md` validator — a PASS/FAIL report per run, not a silent process.

**Hard fails — change is dropped, not applied, logged for review:**
- No traceable source URL for the claim.
- Source is not the vendor's own site (aggregator/blog speculation isn't sufficient for
  pricing or compliance claims).
- Numeric sanity check fails — e.g., a price reads as `$0`, a >5x swing from the current value,
  or a plan name that doesn't resemble any real SaaS pricing convention. These read as scraping
  errors, not real changes.
- Change would touch an off-limits field (see above).
- Change would break the expected array shape (7 items in `features`, 5 in `sources`) that
  `single-tool_review.php` and `quick-facts.php` assume when they loop over the decoded JSON.

**Extra bar for pricing, plan names, and compliance/HIPAA status specifically:**
Because these apply with no human check, they require the *strictest* confirmation tier —
the source must be the vendor's current, live pricing/security/compliance page fetched during
this run (not a cached or third-party summary). If confidence is anything less than "directly
confirmed on vendor's own current page," the system does not apply the change — it leaves the
existing value in place and appends `[VERIFY DETAILS]` per the existing flag convention instead
of guessing.

**Soft warnings — change applies, but gets flagged in the digest:**
- Source is recent but not from the vendor directly (e.g., a credible tech press writeup of a
  vendor announcement).
- Change is stylistically inconsistent with the rest of the field (unusual phrasing, length).

### Visibility (still automated, not invisible)

No manual approval gate, but Rich should never be surprised by what changed. After each run:
- Every applied change, every held/flagged change, and the reason, gets logged (a new
  `aifp_update_log` CPT is the simplest option — visible in WP Admin like Contact Submissions).
- A short digest email goes to rmigliorisi@gmail.com summarizing the run: what changed, what was
  held and why, any cross-page inconsistency flags. Built as a custom authenticated REST route,
  `POST /wp-json/aifp/v1/update-digest` (see `aifp_handle_update_digest()` in `functions.php`),
  since `aifp_update_log` has `show_in_rest => false` and isn't reachable through the standard
  content REST route the same way `tool_review` is. One call at the end of each weekly run logs
  every change as its own `aifp_update_log` entry (visible in WP Admin) and sends the digest
  email via `wp_mail()`, reusing the same pattern as the contact form notification.

---

## System 2: Monthly AI Updates Page (draft, manual publish)

### Purpose

A monthly roundup of notable AI/AI-tool news — launches, funding, major feature releases,
credible rumors — broader in scope than just the 10 reviewed tools. This is new editorial
content, not maintenance, so it always lands as a draft.

### URL and content structure

- URL: `aitoolsforpros.com/[month]-[year]-updates/` (e.g. `/july-2026-updates/`)
- New CPT: `aifp_update`, registered the same way as the existing CPTs in
  `aifp-theme/inc/cpt.php`, with `'rewrite' => false` and the post's `post_name` set directly to
  the full slug (e.g. `july-2026-updates`) at creation time — same as `tool_review` and
  `profession_hub` already do. Extend the existing `post_type_link` filter in `cpt.php`
  (currently `if ($post->post_type === 'tool_review' || $post->post_type === 'profession_hub')`)
  to include `aifp_update` in that same conditional, so it outputs `home_url('/' . $post->post_name . '/')`
  with no `/updates/` prefix. Also needs its own inbound `add_rewrite_rule()` in `functions.php`
  next to the existing tool/profession rules — those use a hardcoded alternation of known slugs,
  which doesn't work for a slug that's different every month, so this one needs a pattern match
  instead, e.g. `^([a-z]+-[0-9]{4}-updates)/?$` routed to `index.php?post_type=aifp_update&name=$matches[1]`.
  Also add `aifp_update` to the `redirect_canonical` filter's `is_singular()` allow-list right
  below it, same reason `tool_review`/`profession_hub`/`cross_reference` are there.
- Content storage follows the same pattern as every other content type on this site — a JSON
  object written to `post_content` (via `content: json.dumps(data_dict)` in the REST payload,
  matching `migrate_v2.py`'s `create_post()`), read back by `aifp_get_data()`. No ACF field group
  needed for this to function; something like `{"month_label": "July 2026", "intro": "...",
  "news_items": [{"headline":..., "summary":..., "source_name":..., "source_url":...}, ...],
  "related_tool_slugs": ["claude", "cursor", ...], "related_profession_slugs": [...],
  "what_to_watch": "..."}` is enough. `related_tool_slugs`/`related_profession_slugs` drive the
  structural internal-linking section in `single-aifp_update.php` — see "Content Optimization
  Guardrails" below. (A matching `acf-fields.php` entry could be added later purely as a
  wp-admin editing convenience, same caveat as the other three CPTs — optional, not required.)
- Needs a `single-aifp_update.php` template (or reuse `page-fullwidth.php` if the layout is close
  enough). Because each monthly page is now a root-level slug (`/july-2026-updates/`) rather than
  nested under a shared `/updates/` path, there's no automatic WP archive at that URL — if an
  index of past months is wanted later, it'll need a dedicated hub page (similar to a profession
  hub) that links out to each monthly post. Not required for the first version.

### Schedule

Generate **2-3 days before the end of each month** (not the 1st, not mid-month). Reasoning: on
the 1st there's nothing to recap yet; mid-month only captures half the month's news either way.
Generating near month's end captures a near-complete picture of that month while leaving a buffer
for Rich to review and publish before the month turns over, and the page's dated month actually
matches what happened in it.

### Process

1. **Research** — search for notable AI/AI-tool developments across the month: major model
   releases, funding rounds, feature launches from the 10 tools already covered plus the wider
   market, and credible (sourced) rumors. Every item needs a real source link, no exceptions —
   this is publicly-facing "news," so unsourced claims are the single biggest reputational risk
   here.
2. **Draft** — compose the page: intro, news items grouped sensibly (not just a flat list),
   optional forward-looking section. Written in the same first-person editorial voice used
   elsewhere on the site per `AIFORPROS.md`. Also populate `related_tool_slugs` (and
   `related_profession_slugs` if relevant) with every one of the 10 reviewed tools mentioned this
   month — see "Content Optimization Guardrails" below for why this is structural, not optional.
3. **Guardrail QA** — same fail-closed sourcing standard as System 1: every factual claim needs
   a real, current source. No `[VERIFY DETAILS]` placeholders left in publicly-facing draft copy
   without an accompanying real value — same rule already enforced in `AIFORPROS-QA.md` Step 5.
   Additional checks specific to this page: no unverifiable rumor stated as fact (frame as
   "reportedly," attributed to a named source), internal links to any of the 10 tool pages that
   are mentioned actually resolve.
4. **Create as WordPress draft** — `POST` to `/wp-json/wp/v2/aifp_update` with `status: "draft"`,
   `slug` set to the month-year-updates string, and `content` set to the JSON-encoded data object
   (same `create_post()` pattern used elsewhere on this site). Never `publish` — this is the one
   hard difference from System 1.
5. **Notify** — Rich gets a heads-up that the draft is ready for review, with a link to it in
   WP Admin.
6. **Publish** — manual, whenever Rich reviews and clicks Publish.

---

## System 3: Monthly Cross-Reference & Profession Hub Editorial Review (suggest-only)

### Purpose

System 1 keeps the 10 tool_review pages factually current, but it deliberately never touches
verdict-level judgment calls — "is Claude now a better fit for architects than it used to be" is
not a fact you can confirm on a vendor's pricing page, it's a synthesis across several capability
changes plus a call about whether that synthesis is strong enough to justify updating a page a
human already wrote and stands behind. That's exactly the kind of claim the guardrails in System 1
and the SEO docs (fail-closed sourcing, no unverifiable claims stated as fact) exist to keep out of
anything that auto-publishes.

So this system does the research and the noticing, but never the writing. It surfaces candidate
verdict-level updates to the 41 `cross_reference` pages (tool × profession) and, more rarely, the 8
`profession_hub` pages, as a reviewable report — evidence, reasoning, and a specific suggested edit
to a specific section — and Rich decides what actually changes. Nothing here auto-publishes, ever.
This is the same posture as System 2 (draft/suggestion, human in the loop) rather than System 1
(auto-publish), because the content itself is a different kind of claim.

This also protects against a real, current risk: Google's spam policy update in 2026 specifically
targets "scaled content abuse" — large volumes of pages edited or generated with little real value
to users. A system that touched dozens of editorial verdicts every month on autopilot, even with
good intentions, would look exactly like what that policy targets. Keeping a human decision at the
point of publish, and keeping the volume of suggested changes deliberately small and well-evidenced,
is what keeps this system firmly on the right side of that line.

### Schedule

Monthly, timed alongside System 2's research pass (2-3 days before month end) since the two share
research ground — System 2 is already looking at what changed across the AI tools market that
month; this system asks the follow-up question of whether anything found is significant enough to
change a specific page's positioning.

### Process

1. **Research** — for each of the 10 tools, look at what's changed since the page was last
   substantively edited (`publish_date` on the page vs. this month): new capabilities, model
   upgrades, workflow-relevant features. Cross-reference against what each of the 8 professions'
   pages says that tool is good or weak at.
2. **Identify candidates** — a page becomes a candidate only when there's a specific, named
   capability change that plausibly affects a specific claim already on that page (e.g., a
   materially larger context window or improved image/document analysis bearing on a page that
   says the tool struggles with long specs or drawings). "The model got a version bump" alone is
   not sufficient reason — the change has to connect to something the page actually claims.
3. **Draft the suggestion, not the rewrite** — for each candidate, produce: the exact current
   sentence/section being questioned, the specific evidence (with source), and one concrete
   proposed replacement (not a vague "consider updating this"). Small, targeted edits to the
   specific claim — not a full rewrite of the page's verdict.
4. **Guardrail QA** — same fail-closed sourcing standard as the other systems: every piece of
   evidence needs a real, current, ideally vendor-official source. No suggestion ships without one.
   Additionally: cap suggestions at a small number per cycle (a handful, not dozens) — if research
   turns up more candidates than that, only the ones with the strongest evidence get surfaced, the
   rest wait for next cycle. Volume discipline here is itself a guardrail, not just an editorial
   nicety (see "Purpose" above on scaled content abuse).
5. **Deliver the report** — to Rich, for review. Nothing is written to WordPress at this stage.
6. **Apply approved changes** — for whichever suggestions Rich approves, apply them the same way
   the July monthly page was patched: fetch the current page's JSON via the WP REST API
   (`context=edit` to get `content.raw`, same pattern as `automation/weekly_tool_update.py`), change
   only the approved field(s), re-encode, `PUT` back. Because this always requires a human decision
   first, it doesn't need to live in a GitHub Actions schedule the way System 1 does — a short
   script generated at approval time, run once locally, is enough.

---

## Content Optimization Guardrails (SEO / GEO / AEO)

Applies to every run of both systems. Grounded in the site's existing strategy docs
(`docs/seo-geo-aeo/08_INTERNAL_LINKING_REQUIREMENTS.md` and
`docs/seo-geo-aeo/02_AI_SEARCH_GEO_AEO_REQUIREMENTS.md`) rather than inventing separate rules for
automated content. Found and fixed after the first live proof-of-concept (the July 2026 draft)
shipped with zero internal links.

### Internal linking is structural, not a writing reminder

Content generation reliably forgets to add links; a template can't. `single-aifp_update.php`
renders a "Related Reviews" section directly from `related_tool_slugs` /
`related_profession_slugs` in the data object, so every monthly page that mentions a reviewed
tool automatically links to that tool's review page, no matter what the generated prose does.
Every run must populate these arrays with every reviewed tool (and profession, where relevant)
mentioned that month. Same principle applies to System 1: any weekly fact update that touches a
tool with existing `cross_reference` pages should be checked for consistency with those pages
(already required above) rather than left to prose to reference correctly.

Per `08_INTERNAL_LINKING_REQUIREMENTS.md` section 9 ("AI agents may suggest links, but should not
auto-publish without approval"), this system stays inside a narrow, safe exception: linking a
tool's own name to its own already-published review page is mechanical and requires no subjective
judgment, so it's fine to auto-apply on both systems. Anything less obvious, a suggested link to a
page that isn't a direct, unambiguous match, gets logged as a suggestion in the weekly digest
rather than silently added.

Anchor text follows section 3 of that doc: descriptive and natural ("Our Claude review," "AI
tools for Legal Counsel"), never "click here" or bare repeated tool names.

**Link each destination once per page.** If a tool is mentioned in multiple items on the same
page, only the first meaningful mention gets linked; later mentions of the same destination stay
plain text. The exception is an image or thumbnail pointing to the same destination later in the
page, that's a distinct, additional link, not a duplicate. This applies per-page, not per-item:
don't re-link Claude in the third item just because it's a different news item on the same page.

### Answer-led structure (AEO)

Per `02_AI_SEARCH_GEO_AEO_REQUIREMENTS.md` section 1, the intro paragraph on the monthly page
must be able to stand alone if lifted verbatim into an AI-generated answer: a direct, concrete
statement of what happened this month, not scene-setting or vague preamble. Same standard for any
weekly page-level summary text. Avoid burying the substantive point after throat-clearing.

### Entity clarity

Every news item's first mention of a tool or company must use the full, unambiguous name (e.g.
"Anthropic," "Cursor"), not a pronoun or vague reference, per section 2 of the same doc.

### Information gain

Per section 3, a rewritten press release is not enough. Each item should carry a sentence of
relevance to this site's specific audience (working professionals), not just restate the news.

### QA gate addition

Add to both systems' existing QA checks: reject/hold any draft where `related_tool_slugs` is
empty despite a reviewed tool being named in the body text, and reject any anchor text that is
generic ("click here," "read more," bare "link").

---

## Shared implementation notes

- Both systems reuse the existing `.env` / `wp_creds.py` Application Password auth (read via
  `WORDPRESS_USERNAME` / `WORDPRESS_APP_PASSWORD` env vars — from GitHub Actions secrets in CI,
  from `.env` locally) — no new credential *format* needed, just a second place (GitHub repo
  secrets) it also has to live for System 1.
- System 1 runs as a scheduled **GitHub Actions workflow** calling the Claude API directly
  (see "How the research step works" above) — not a Cowork scheduled task, because Cowork's
  sandbox can't make the authenticated write. System 2 (monthly) still runs interactively through
  Cowork today, since a draft-only page with a human publish step doesn't need to run unattended.
  This keeps the "not costly" requirement from the earlier chatbot discussion intact either way —
  no per-message API meter, just a bounded weekly job (a few dollars a year, see above).
- Neither system touches theme code (`aifp-theme/`), so neither goes through the GitHub Actions
  QA/deploy pipeline — that pipeline validates PHP files, not WordPress content. The QA gates
  described above are the content-level equivalent, purpose-built for this.
- Before either system runs unattended for the first time, do one supervised dry run: generate
  the output as normal but don't apply/publish, just show Rich the proposed diff (System 1) or
  draft (System 2) so the QA gate's judgment can be sanity-checked once before trusting it.

## Still to build

- [x] `aifp_update_log` CPT for the weekly change log — `inc/cpt.php`
- [x] `aifp_update` CPT + inbound rewrite rule + `single-aifp_update.php` template for the monthly page
- [x] Weekly digest email function — `POST /wp-json/aifp/v1/update-digest` in `functions.php`
- [x] Article/BreadcrumbList JSON-LD support for `aifp_update` — `inc/json-ld.php`
- [x] `aifp_update` added to the custom sitemap generator
- [x] System 1 research + diff + QA-gate + write logic — `automation/weekly_tool_update.py`
- [x] System 1 scheduled execution — `.github/workflows/weekly-tool-update.yml` (GitHub Actions,
      `workflow_dispatch` only for now; `schedule:` trigger is commented out on purpose)
- [ ] Add `ANTHROPIC_API_KEY`, `WORDPRESS_USERNAME`, `WORDPRESS_APP_PASSWORD` as GitHub repo secrets
- [ ] One supervised dry run of System 1 (via `workflow_dispatch` with dry run checked), then
      uncomment the `schedule:` trigger once the output looks right
- [ ] System 2's monthly run is still manual-via-Cowork end to end (research → draft → notify);
      no scheduled execution built for it yet since draft-only + human-publish doesn't need one
- [x] System 3 spec'd (Monthly Cross-Reference & Profession Hub Editorial Review, suggest-only)
- [ ] System 3 has no automation yet — first pass run manually via Cowork as a live test
      (Claude for Architects, prompted by Rich noticing the tool has likely improved for that
      profession) before deciding whether it's worth scheduling at all
- [ ] Requires a `git commit` + `push` to deploy — see repo for pending changes
