# Automated Content — Weekly Tool Updates & Monthly AI Updates Page

This defines two automated content systems for aitoolsforpros.com, run on a schedule with no
daily human involvement, but with different risk postures matched to what each one touches.

| System | Touches | Cadence | Goes live |
|---|---|---|---|
| Weekly Tool Page Updates | Existing, already-published `tool_review` pages | Weekly | Automatically, no approval step |
| Monthly AI Updates Page | New page at `/[month]-[year]-updates/` | Monthly | Only when Rich clicks Publish |
| Monthly Editorial Review | Existing `cross_reference` (41) / `profession_hub` (8) pages | Monthly | Automatically, capped at 10 pages/run + backlog rollover — no approval step (graduated from suggest-only 2026-07-25, see System 3 below) |

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

**Known gap (found July 2026, unresolved):** the freshness argument above assumes a genuine content
edit shows up as a fresher `lastmod` somewhere a crawler can see. In testing, Rank Math's
`cross_reference-sitemap.xml` did not update its `lastmod` for `/claude/architects/` after a
REST-API write. Root cause not yet diagnosed (likely a Rank Math or WP.com-level sitemap cache that
isn't invalidating on `save_post`). Worth fixing before leaning too hard on "weekly updates improve
freshness signals" as a selling point — currently that's only fully true for the underlying page
content, not for the sitemap's `lastmod` metadata.

**Serious bug found and fixed (July 25, 2026): never resave `tool_review` / `cross_reference` /
`profession_hub` posts through the plain WP Admin editor.** These post types store their entire page
as a single JSON blob in `post_content`; the theme's PHP decodes that JSON and renders each section.
WordPress's standard post editor silently runs `wptexturize` (straight quotes → curly quotes) and
`wpautop` (wraps detected paragraph breaks in `<p>` tags) on whatever gets saved through its UI. That
auto-formatting is invisible and harmless for normal prose, but it's destructive to a raw JSON blob —
every `"` becomes `&#8220;`/`&#8221;`, and blank lines inside JSON string values get wrapped in stray
`<p>`/`</p>` tags, producing invalid JSON. When that happens, `aifp_get_data()` fails to decode the
content and the PHP template silently falls back to only rendering what *doesn't* depend on the JSON
blob (title, breadcrumb, taxonomy-driven related-guides grid, the static author-card include) —
every JSON-driven section (quick facts, features, pricing, FAQ, sources, insights) just disappears
from the page with no error.

This is exactly what happened to `/claude/architects/` on 2026-07-22: a manual WP Admin resave done
purely to test the sitemap `lastmod` gap above (see revision 984) corrupted the content JSON, and it
went unnoticed for three days because nothing about the save looked like a failure — it showed
"Updated" like any other successful save. It was caught only because Rich happened to view the live
page and noticed most of the content was missing. Recovered by finding the last revision with valid
JSON (revision 983, immediately after the July 16 "1M token" patch) via the WordPress revisions REST
endpoint and writing that content back — see `check_architects_revisions.py` and
`restore_architects_content.py` in the repo root.

**The rule going forward: any edit to these three post types must go through the REST API (a script,
same pattern as the patch scripts and System 1/3), never through the WP Admin editor UI.** If a
manual admin-side check is ever needed again (e.g. re-testing the sitemap issue), verify the live
front-end page still renders all 15 sections immediately afterward — don't assume "Updated" means the
content survived intact.

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

## System 3: Monthly Cross-Reference & Profession Hub Editorial Review (capped autonomous apply)

### Purpose

System 1 keeps the 10 tool_review pages factually current, but it deliberately never touches
verdict-level judgment calls — "is Claude now a better fit for architects than it used to be" is
not a fact you can confirm on a vendor's pricing page, it's a synthesis across several capability
changes plus a call about whether that synthesis is strong enough to justify updating a page a
human already wrote and stands behind.

This system does that research and noticing, and — as of 2026-07-25 — applies the resulting edits
itself, without a human approval step per run. It graduated from suggest-only after the first
manual cycle (Claude's 200K -> 1M-token context window, 7 pages, July 2026) went cleanly end to end,
a real bug found during that cycle (see "Critical" note below) got fixed and covered by an automated
self-test suite, and post-write verification (re-fetch + diff, never just trust a 200 response) got
added. Rich made the call to move to autonomous apply once those held up — see chat history
2026-07-25 for the exact exchange.

**Why the cap and backlog design below exists, and why it isn't optional:** Google's spam policy
update in 2026 specifically targets "scaled content abuse" — large volumes of pages edited or
generated with little real value to users. A system that touched dozens of editorial verdicts every
month on autopilot would look exactly like what that policy targets, autonomous or not. With the
human-approval step gone, the cap (10 pages/run, overflow queued to `automation/system3_backlog.json`
for next run rather than all applied at once) is now the primary thing keeping this system's volume
profile looking like careful maintenance rather than scaled churn. Do not remove or raise the cap
without deliberately re-considering this risk, not just as a performance tweak.

The other guardrails inherited from the suggest-only era (fail-closed sourcing, full-text sweep,
exact-source-domain matching) got *stricter*, not looser, in the move to autonomous apply — a
verdict-level content change with no human second look before publish deserves at least the same
bar System 1 uses for pricing/compliance (vendor-official-current confidence, no exceptions), if not
a higher one. See "Guardrail QA" below.

### Schedule

Monthly, on **day 25** (was previously timed alongside System 2's research pass 2-3 days before
month end; day 25 was chosen when this moved to a dedicated GitHub Actions schedule — see
"Architecture" below). Runs via `.github/workflows/system3-monthly.yml`, calling
`automation/system3_monthly.py`.

### Architecture — why this runs on GitHub Actions, not a Cowork scheduled task

This system used to run as a Cowork scheduled task (`system3-cross-reference-editorial-review`,
retired 2026-07-25) that produced a suggest-only report every month — that worked because the only
output was text, no write needed. Autonomous apply needs a real WordPress write, and Cowork's
sandbox cannot make authenticated writes to any external host (outbound HTTPS to third-party
services is blocked at the proxy — confirmed during System 1's build, see that system's
"Schedule" section above). So, same as System 1, the actual research-and-write logic lives in a
GitHub Actions workflow with real network access, reusing the same `ANTHROPIC_API_KEY` /
`WORDPRESS_USERNAME` / `WORDPRESS_APP_PASSWORD` repo secrets System 1 already set up.

### Process

1. **Research** — for each of the 10 tools, one Claude API call (`web_search`, restricted to that
   vendor's own domains, same `TOOLS` dict System 1 uses) asking what's changed in roughly the last
   month that's relevant to a working professional's use of the tool: new capabilities, model
   upgrades, workflow-relevant features.
2. **Identify candidates** — a page becomes a candidate only when there's a specific, named
   capability change that plausibly affects a specific claim already on that page (e.g., a
   materially larger context window or improved image/document analysis bearing on a page that
   says the tool struggles with long specs or drawings). "The model got a version bump" alone is
   not sufficient reason — the change has to connect to something the page actually claims. This
   connection is judged by a second, page-specific Claude API call (one per tool × relevant page)
   given the finding plus the page's full decoded content, not a keyword grep — see
   `identify_candidates()` in `automation/system3_monthly.py`.
3. **Propose the exact edit, not the rewrite** — for each candidate, the model returns the exact
   current substring being questioned (`old_text`) and the exact proposed replacement (`new_text`),
   plus a one-sentence rationale. Small, targeted edits to the specific claim — not a full rewrite
   of the page's verdict. `old_text` is re-verified as a literal, present substring of the page's
   actual content locally, in Python, before it's trusted — a defensive check against the model
   ever hallucinating a quote that isn't really there.
4. **Full-text sweep, not a skim** — the identification call is explicitly instructed to search the
   *entire* page content for every literal occurrence of the fact being updated (every field, not
   just Bottom Line/comparison table/the "obvious" spots), and propose an edit for each one found.
   This step exists because the first live run (Claude for Architects, July 2026) missed 2 of 6
   "200K" mentions on the first pass — they were sitting in FAQ answers that weren't part of the
   initial visual skim. Cheap insurance against publishing an internally-inconsistent page (old
   number in one FAQ, new number in the Bottom Line).
5. **Guardrail QA** — every edit needs a source, and now (post-graduation from suggest-only) the
   bar is the *strict* one: `confidence` must be exactly `"vendor_official_current"` — third-party
   or uncertain findings are held/logged, never auto-applied, no soft-warning tier the way System 1
   allows for some fields. Source URL must resolve to that tool's allowed vendor domain(s) (checked
   in Python, not just trusted from the model's own claim). `old_text` must verify as a literal
   substring of the actual page content (see step 3). Any edit failing any of these is dropped and
   logged as held, never applied.
6. **Cap + backlog rollover** — at most 10 pages get written per run (`--cap`, default 10; a
   deliberate ceiling, see "Purpose" above). Pages already queued in `automation/system3_backlog.json`
   from a prior run that exceeded the cap are applied first (oldest first), then this run's new
   candidates fill any remaining room. Whatever's left over after the cap gets written back to the
   backlog file for next run — nothing found is ever silently dropped for being over the cap, it
   just waits its turn. If a month turns up zero real candidates, the backlog (if any) still gets
   worked down at the same cap.
7. **Apply** — for everything within this run's cap: fetch the current page's JSON via the WP REST
   API (`context=edit` to get `content.raw`), decode it, walk the decoded structure doing the
   text replacement (never raw-JSON-text matching — see "Critical" note below for why), re-encode,
   `PUT` back, then **re-fetch and diff against what was sent** to confirm the write actually took
   rather than trusting the HTTP response alone.
8. **Log + notify** — every applied, held, and queued edit gets logged via the same digest endpoint
   System 1 uses (`POST /wp-json/aifp/v1/update-digest`), so Rich gets an email summary every run
   even though nothing is gated on his approval. Automated, not invisible — same principle as
   System 1's "Visibility" section above.

### Critical: never apply approved edits through the WP Admin visual/block editor

Found during the July 2026 System 3 cycle (Claude for Engineers, Physicians, Finance, Insurance,
Legal, Real Estate, Creatives) and confirmed by direct evidence, not inference: **opening a
`tool_review` / `profession_hub` / `cross_reference` post in WP Admin and clicking Update — even
with zero visible changes — corrupts its `post_content`.** The block/classic editor parses the
raw JSON-with-embedded-HTML this site stores in `post_content` as if it were normal rich-text
content, runs it through its own HTML cleanup on save, and writes back a mangled result: inline
`style` attributes get garbled (`style="margin:0 0 16px;color:#636363;line-height:1.7;"` becomes
`style="0margin: 0;"`), and quotes inside `class`/`href` attributes get double-escaped
(`class="font-heading"` becomes `class="\&quot;font-heading\&quot;"`). `aifp_get_data()` /
`single-cross_reference.php` then can't parse the corrupted `section_body` HTML correctly, and
whole `content_sections` entries silently stop rendering — the live page loses its Bottom Line,
Quick Facts, Features, comparison table, FAQ, Sources, and Insights blocks entirely, while
chrome (header/nav/footer, Related Guides) still renders fine because that's generated separately,
not from this JSON.

This is also the likely explanation for why a page can look "still wrong" on the live site well
after its underlying data was already corrected: if a fix was applied cleanly via the REST API at
some point, but someone later opens that same post in WP Admin and clicks Update for an unrelated
reason (or just to "refresh" it), the clean REST-written content gets silently re-corrupted. What
looks like a caching problem may actually be exactly this.

**Rule going forward, no exceptions:** all edits to these three post types — the approved
System 3 suggestions, System 1's weekly writes, anything — must go through the WP REST API
(`content.raw` via `context=edit`, full re-`json.dumps`, `POST` with
`X-HTTP-Method-Override: PUT`), never through WP Admin's Update button. If a post ever needs a
human eyeball check, use "Preview" or view the live page, but do not click Update, even with no
edits made.

**If a post has already been corrupted this way:** the fastest recovery is restoring from a
known-good `content.raw` snapshot taken before the corrupting save (not necessarily a WordPress
revision — restoring a WP revision through the admin UI is unverified as safe here and may run
through the same corrupting save path). `automation/system3_2026-07_claude_context_window.py`
(the one-off script from the July 2026 manual cycle, kept around specifically as a recovery tool —
it is not the ongoing System 3 implementation, that's `automation/system3_monthly.py` now) has two
flags built for exactly this:
- `--dump SLUG` / `--dump-all` — writes a post's current `content.raw` to
  `automation/_debug_<slug>.json`, no writes to WordPress. Use this to snapshot state before
  touching anything, and to diagnose whether a page's "still wrong" content is a stale-cache
  problem or actual data corruption.
- `--restore SLUG` — reads `automation/_restore_<slug>.json` (a known-good `content.raw` you've
  saved) and `PUT`s it back verbatim via the REST API, then re-fetches and confirms the write
  matches exactly. This is how the Claude for Engineers corruption from this cycle was fixed.

**A second, related bug found and fixed in the same July 2026 cycle, unrelated to WP Admin:** the
original patch script matched `old_text`/`new_text` pairs against the raw JSON text of
`content.raw` directly. Raw JSON text escapes an embedded `"` as `\"`; the search patterns used
plain, unescaped quotes. Any target sentence containing a literal quotation mark could therefore
never match, producing a false "text not found — may have already changed" even on a real apply
run — this happened on the Claude for Legal page's "What Most Reviews Miss" insight, which quotes
the phrase `"Claude has a 200K context window"` verbatim. **The fix, now standard in
`automation/system3_monthly.py`:** `json.loads()` the raw content first, then do every match/replace
against the *decoded* Python strings (where a `"` is just a character, not a JSON escape sequence),
then `json.dumps()` once at the end before writing. Never match against raw, still-JSON-encoded
text. This fix is covered by an automated self-test suite (`run_selftests()`) that runs
automatically before any network call in `system3_monthly.py` and aborts the whole run if any check
fails — fail closed on the logic itself, not just on sourcing.

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
- System 1 and System 3 both run as scheduled **GitHub Actions workflows** calling the Claude API
  directly (see "How the research step works" above) — not Cowork scheduled tasks, because
  Cowork's sandbox can't make the authenticated write. System 2 (monthly) still runs interactively
  through Cowork today, since a draft-only page with a human publish step doesn't need to run
  unattended. This keeps the "not costly" requirement from the earlier chatbot discussion intact
  either way — bounded jobs, not a per-message API meter (System 1: a few dollars a year, see
  above; System 3: at most 10 tool-research calls + a handful of per-page identification calls a
  month, same order of magnitude).
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
      `schedule:` trigger turned on 2026-07-25 — runs every Monday ~9am ET)
- [x] Add `ANTHROPIC_API_KEY`, `WORDPRESS_USERNAME`, `WORDPRESS_APP_PASSWORD` as GitHub repo secrets
- [x] Supervised live run of System 1 across all 10 tool pages, reviewed via full page-by-page
      audit and the Weekly Update Log (33 entries — real changes applied, new/unrecognized
      tiers and features correctly held). Two bugs found in that review and fixed: quick_facts
      values written as long paragraphs instead of short labels (guardrail: `max_value_len`),
      and the digest email always reporting `sent: true` regardless of `wp_mail()`'s actual
      result. Weekly schedule turned on after these fixes landed.
- [ ] System 2's monthly run is still manual-via-Cowork end to end (research → draft → notify);
      no scheduled execution built for it yet since draft-only + human-publish doesn't need one
- [x] System 3 spec'd (Monthly Cross-Reference & Profession Hub Editorial Review, suggest-only)
- [x] System 3 first live run completed successfully (Claude for Architects, 200K → 1M token
      context window, 6 mentions found and corrected across the page) — proved the
      research → suggest → approve → patch loop works end to end
- [x] System 3 process gap found and fixed in the spec: "full-text sweep" step added after the
      first run missed 2 of 6 mentions on a visual skim (see "Process" step 4 above)
- [x] System 3 originally ran on a monthly Cowork scheduled task
      (`system3-cross-reference-editorial-review`, day 25 of each month) that produced a
      suggest-only report — never wrote to WordPress. **Retired 2026-07-25** in favor of the GitHub
      Actions workflow below, once the process had proven itself on a live manual cycle.
- [x] System 3 graduated from suggest-only to capped autonomous apply (2026-07-25). Built
      `automation/system3_monthly.py` (research -> per-page candidate identification -> strict
      guardrail QA -> 10-page/run cap with backlog rollover in `automation/system3_backlog.json` ->
      apply via REST with the decoded-JSON replace + self-tests + post-write verification proven on
      the manual July cycle -> digest email) and `.github/workflows/system3-monthly.yml` (cron, day
      25, same secrets as System 1). Not yet run live in this new form — first live run should be
      watched closely (see "Before either system runs unattended for the first time" above, same
      principle applies to this graduation).
- [ ] Known gap: Rank Math's sitemap `lastmod` isn't updating on REST-API saves — tempers the
      "weekly updates improve freshness signals" rationale for System 1 (see note under "How the
      research step works" above). Not yet root-caused; low priority since it doesn't hide real
      content changes from crawlers, just weakens one freshness input
- [x] Known gap found and fixed (July 2026): WP Admin's visual/block editor corrupts
      `post_content` on `tool_review`/`profession_hub`/`cross_reference` posts on save (mangles
      inline CSS and double-escapes HTML attribute quotes), causing whole content sections to
      silently stop rendering. Root cause understood, not yet patched at the WP level (would need
      a `save_post` filter that bypasses editor sanitization for these post types, or moving these
      fields out of `post_content` entirely). Workaround in place and documented above: never edit
      these post types via WP Admin's Update button, REST API writes only. See "Critical: never
      apply approved edits through the WP Admin visual/block editor" above.
- [x] Serious bug found and fixed: a manual WP Admin resave corrupted `/claude/architects/`'s content
      JSON on 2026-07-22 (WordPress's editor auto-formatting mangled the raw JSON blob), silently
      dropping every JSON-driven section from the live page for three days. Recovered from WordPress
      revision history (`check_architects_revisions.py` / `restore_architects_content.py`). New rule
      documented above: never resave these post types through the WP Admin editor UI
- [ ] Requires a `git commit` + `push` to deploy — see repo for pending changes
