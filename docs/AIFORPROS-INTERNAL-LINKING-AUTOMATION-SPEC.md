# Internal Linking Automation Spec — AI Tools for Pros

Machine behavior for any tool that proposes, scores, or applies internal-link changes. This file must satisfy every rule in `AIFORPROS-INTERNAL-LINKING.md` (`policy_version` 1.3.0 or later) — where a design decision here would conflict with that document, the governance document wins and this file must change.

**Status: implemented and running on a weekly schedule, as of 2026-08-05.** Sections 1–9 held up through design review and are now built, not just specified: `automation/linking_audit.py` (audit-only inventory + gap detection), `automation/linking_scoring.py` (the LLM prompt/scoring logic §17 originally deferred — hard gates applied per §6), and `automation/linking_apply.py` (a working implementation of §8's write protocol, with some deliberate, disclosed deviations from the idealized version below — see the note under §8). All three are chained in `.github/workflows/linking-automation.yml` on a weekly cron. The system skipped "supervised-apply" (§1) entirely and went straight from suggestion-only to a narrow auto-apply, per Rich's 2026-08-05 decision to bring internal linking up to the same operating standard System 1 and System 3 already run at — see governance §16's 1.3.0 change-log entry for the exact conditions that decision required to be true first.

Sections below are left largely as originally designed, with inline notes added only where the actual implementation deviates from the idealized version or where a section is now stale. Treat this document as the target design; the docstrings in `automation/linking_*.py` are the source of truth for what the code actually does today.

## 1. Operating modes

- **Audit-only** — read-only, no writes. `automation/linking_audit.py`, still runs first every cycle.
- **Suggestion** — generates proposals (§3 schema; in practice, `linking_scoring.py`'s output shape is close to but not identical to §4's schema — see the note there). No longer the terminal mode for contextual additions as of 2026-08-05.
- **Supervised-apply** — a human approves a specific proposal *revision* (§3, §7) before it's written. **Never built.** The system moved directly from suggestion to auto-apply for this one change class; this mode remains available in principle for any future change class where a human-in-the-loop step is wanted again.
- **Auto-apply** — as of 2026-08-05, enabled for exactly one class: contextual link additions to `cross_reference` pages produced end-to-end by `linking_scoring.py` + `linking_apply.py`, per governance §16's 1.3.0 entry. Still reserved otherwise for governance §15's "safe candidates," each condition fully satisfied — this did not generally enable auto-apply for other change classes.

## 2. Scope inventory

- Editable source type (Phase 1): `cross_reference` only (governance §11).
- Audit-only source types: `tool_review`, `profession_hub`.
- Valid target types: `tool_review`, `profession_hub`, `cross_reference`, each passing §5's eligibility checks.
- Excluded target types: per governance §11.
- Inventory rebuilt each run from the XML sitemaps + REST API `context=edit` reads; never cached indefinitely.
- Relationship model uses governance §12 vocabulary exactly: `primary_tool`, `profession`, `sibling_tool`, `sibling_cross_reference`.

## 3. Evidence-record schema and storage

Evidence is stored **independently and referenced by ID**, not copied into every proposal — the same fact (e.g. a tool's context-window size) may support multiple proposals across multiple pages, and a single update to the evidence record should invalidate all of them at once rather than requiring N separate corrections.

```json
{
  "evidence_id": "ev_2026-08-03_claude-context-window",
  "claim": "Claude's Pro/Team/Enterprise plans support a 1,000,000-token context window",
  "source_url": "https://docs.claude.com/...",
  "source_type": "OFFICIAL_VENDOR_DOCUMENTATION",
  "publisher": "Anthropic",
  "_comment_source_type_note": "source_type is one of the six governance §1 evidence classifications. For the scoring step in §17, the expected common case is SITE_PUBLISHED_CONTENT — citing a sibling page's own already-published, already-reviewed content (e.g. its consistency_blocks.bottom_line) rather than fetching new external vendor documentation, which is out of scope for this system and duplicates System 1's job.",
  "retrieved_at": "2026-08-03T16:00:00Z",
  "supporting_text": "exact quoted passage or structured field from the source",
  "freshness_status": "current",
  "expires_at": "2026-09-03T00:00:00Z",
  "verified_by": "Rich Migliorisi",
  "source_content_hash": "sha256:..."
}
```

- `freshness_status` is one of `current` / `needs_recheck` / `stale`. An evidence record automatically moves to `needs_recheck` when `expires_at` passes.
- Any proposal referencing an `evidence_id` whose `freshness_status` is not `current` at application time MUST be blocked from `applied` and routed back to `needs_evidence` (§6), even if it was previously `approved` — see §6's transition table.
- Evidence expiring between approval and application is an explicit acceptance-test case (§9's list).

## 4. Proposal (audit) record schema

One record per governance §14's atomic unit — a (source `cross_reference` page, `sibling_tool`) pair. This is the authoritative object the reviewer interface (§7), the write protocol (§8), and the change log (§11) all operate on.

```json
{
  "record_id": "rec_...",
  "source_post_id": 373,
  "source_url": "https://aitoolsforpros.com/claude/finance/",
  "canonical_target_id": 365,
  "target_url": "https://aitoolsforpros.com/chatgpt/finance/",
  "primary_tool": "Claude",
  "sibling_tool": "ChatGPT",
  "profession": "Finance",
  "policy_version": "1.1.0",
  "state": "opportunity_proposed",
  "edit_type": "link_existing_text",
  "content_zone": "limitation_card",
  "placement_locator": { "...": "see §5" },
  "existing_text": "...",
  "proposed_text": "...",
  "anchor_text": "...",
  "rationale": "why this is a genuine comparison point, not a filler sentence",
  "useful_without_link": true,
  "evidence_ids": ["ev_..."],
  "rules_applied": ["GOV-LINK-007", "GOV-LINK-010"],
  "confidence": { "...": "see §6" },
  "source_revision": 1234,
  "source_content_hash": "sha256:...",
  "created_at": "2026-08-03T16:00:00Z",
  "reviewed_by": null,
  "reviewed_at": null,
  "fingerprint": { "...": "see §6a" }
}
```

`useful_without_link` MUST be explicitly recorded (true/false) as the direct output of governance §8's test — not inferred later by a reviewer from the rest of the record.

## 5. Placement locator

The exact-match-count check (§8 step 5) remains authoritative for whether a write is safe to apply. This locator gives reviewers (and the fingerprinting logic in §6a) enough surrounding context to judge placement and detect staleness, without relying on `exact_text` alone:

```json
{
  "zone": "limitation_cards",
  "section_key": "context_limitations",
  "paragraph_index": 2,
  "exact_text": "the exact sentence or span being modified",
  "preceding_text": "the sentence immediately before it",
  "following_text": "the sentence immediately after it",
  "source_revision": 1234
}
```

`zone` values come from the content-zone taxonomy (§10 below).

## 6. Confidence dimensions and routing

A single blended confidence score can hide which specific thing is uncertain. Confidence is tracked as separate dimensions, each independently gating the record's state:

- `relevance_confidence` — is this genuinely about the sibling tool's actual strength/weakness relative to the primary tool, on this specific page?
- `evidence_confidence` — does a valid, non-expired evidence record (§3) actually support the claim?
- `placement_confidence` — does the proposed sentence fit naturally at this exact location?
- `editorial_naturalness_confidence` — does it read as genuine prose, not a bolted-on aside (governance §8)?
- `target_eligibility_confidence` — has §5/§10's eligibility check fully resolved (not `blocked_eligibility_unknown`)?

**Routing rules** (all must pass for `opportunity_proposed`; any single failure below routes accordingly — these are hard gates, not averaged):

- Evidence missing or expired → `needs_evidence`, regardless of the other four dimensions.
- Target eligibility unresolved → `blocked_eligibility_unknown` (§10) — the record does not proceed to review at all until this clears.
- Relevance or naturalness ambiguous → `needs_editorial_review`.
- All required dimensions pass → `opportunity_proposed`.

No numeric threshold (e.g. "average confidence above 0.85") may substitute for these gates.

### 6a. Fingerprinting and invalidation

Three distinct fingerprints, not one:

- **Record identity** — `source_post_id` + `canonical_target_id` + `policy_version`. Stable for the life of the (page, sibling) pair under a given policy version.
- **Proposal fingerprint** — hash of (`source_revision` + `target_revision` + `evidence_ids` + the proposed diff). Changes whenever any input to a specific proposal changes, even if the record identity doesn't.
- **Resolution fingerprint** — hash of the final applied diff, or of the confirmed `no_opportunity_confirmed` decision + the evidence/reasoning behind it.

This separation exists specifically to prevent: re-proposing an already-rejected sentence on every subsequent run; treating a materially changed proposal as identical to a stale one; and permanently suppressing a real opportunity just because an earlier pass concluded `no_opportunity_confirmed` before the source or target content changed. A changed proposal fingerprint on a record that's `approved` or `no_opportunity_confirmed` moves that record to `stale` (§6b).

### 6b. State-transition table

Explicit valid transitions. Any transition not listed is invalid and MUST be rejected by the system, not silently allowed. `gap_detected` is the entry state produced by the audit-only inventory layer (`automation/linking_audit.py`) — it means "no contextual coverage exists and the target is eligible," with no judgment yet about whether a genuine opportunity exists. It is not itself a proposal and carries none of §4's scoring fields (`edit_type`, `rationale`, `evidence_ids`, `confidence`, etc.) until the not-yet-built scoring step (§17) evaluates it:

```
gap_detected            → opportunity_proposed | needs_evidence | needs_editorial_review | no_opportunity_proposed | stale
opportunity_proposed   → approved | rejected | needs_evidence | stale
needs_evidence          → opportunity_proposed | rejected | stale
needs_editorial_review  → opportunity_proposed | no_opportunity_proposed | rejected | stale
no_opportunity_proposed → no_opportunity_confirmed | needs_editorial_review | opportunity_proposed | stale
approved                → applied | stale | failed
failed                  → approved | stale | rolled_back
applied                 → rolled_back
no_opportunity_confirmed → stale
stale                   → (re-evaluated; re-enters the flow at opportunity_proposed / needs_evidence / needs_editorial_review / no_opportunity_proposed as appropriate)
rejected                → (terminal, unless the underlying page changes, which produces a new proposal fingerprint and effectively a new evaluation)
rolled_back             → (terminal for that specific applied change; a new record may be created afresh)
```

Transitions requiring a human actor — `no_opportunity_proposed → no_opportunity_confirmed`, `opportunity_proposed → approved`, any `→ rejected` — MUST fail if no `reviewed_by` is recorded on the transition. This is the mechanism that enforces governance §14.3's rule that a model score alone cannot finalize `no_contextual_opportunity`.

## 7. Reviewer workflow

**As of 2026-08-05, `opportunity_proposed` records that clear `linking_scoring.py`'s hard gates go straight to `linking_apply.py` — no human sees them before publish.** This section's workflow still applies in full to `needs_editorial_review` and `no_opportunity_proposed` records (nothing auto-finalizes those to a negative or positive conclusion, per governance §14), and to any record from a different change class or page type. No reviewer UI has been built; these records are currently only inspectable by reading `automation/linking_proposals_output.json` directly.

A human reviewing a record (`opportunity_proposed`, `needs_editorial_review`, or `no_opportunity_proposed`) must see, at minimum:

- Source URL and target URL, with the `primary_tool` / `sibling_tool` / `profession` relationship (§2).
- Content zone and the placement locator's surrounding text (§5).
- The existing paragraph and the proposed paragraph, with an exact highlighted diff.
- Anchor text and destination.
- The full evidence record(s) (§3), not just a summary.
- Rules applied (governance rule IDs) and this record's confidence dimensions (§6).
- Eligibility check results (§10) and risk classification (edit type, per §4).
- The current source revision, to catch a staleness conflict before acting.

**Available actions:** approve, reject, defer (leave in current state), edit, confirm-no-opportunity. **An edit MUST create a new proposal revision** (new proposal fingerprint, §6a) rather than silently overwriting the AI-generated text — the review record must show what the AI proposed and what the human actually approved as two distinct, retained values.

## 8. Fail-closed write protocol

Restated below as originally designed, with **[IMPLEMENTED]** / **[DEVIATION]** / **[NOT BUILT]** tags showing what `automation/linking_apply.py` actually does as of 2026-08-05. This is disclosed deliberately rather than silently claiming full compliance — the deviations were accepted as reasonable for this narrow, capped, low-blast-radius change class, not oversights:

1. Re-fetch the current source page content. **[IMPLEMENTED]**
2. Re-fetch the current target page; confirm it still passes §10. **[IMPLEMENTED]** — reuses `linking_audit.check_eligibility()` directly rather than a second copy of the same logic.
3. Confirm the source page's revision/content hash matches the approved proposal's `source_revision`; mismatch → `stale`, abort. **[DEVIATION]** — no `source_revision` hash is stored on the proposal record at all. Instead, step 5's exact-count check on the specific `existing_text` span serves the same practical purpose (detect drift since scoring) for this narrow case, since the only thing that matters is whether that one span is still there — but it would NOT catch every kind of page drift a full content-hash comparison would (e.g. a change elsewhere on the page that leaves the target span untouched passes silently, which is fine here since it doesn't affect this edit's correctness).
4. Re-run the full eligibility check (§10) on the target. **[IMPLEMENTED]** — same call as step 2.
5. Confirm the exact intended text node occurs exactly once in the decoded content. **[IMPLEMENTED]** — `_count_in_value`, imported from `system3_monthly.py` rather than re-implemented.
6. Create an immutable pre-write snapshot of the exact content being changed. **[DEVIATION]** — no full pre-write page snapshot is stored. `linking_change_log.json` records the exact `existing_text`/`proposed_text` span (enough to manually revert this specific change by replacing one for the other) but not a snapshot of the entire page as it existed before the write.
7. Apply exactly one allowlisted transformation matching the approved diff. **[IMPLEMENTED]** — one `_replace_in_value` call per record.
8. Validate the full resulting document (valid JSON, §12 protected-region invariants untouched, no unrelated link altered). **[DEVIATION]** — valid JSON is guaranteed by construction (only string leaf values are mutated); there is no independent post-write check confirming protected regions or unrelated links were untouched. This relies on `linking_scoring.py`'s system prompt restricting edits to `content_sections[N].section_body` and on `existing_text` being an exact, narrow substring match — not on an explicit invariant check at write time.
9. Re-fetch the saved page, verify the change matches intent, record a rollback identifier tied to the pre-write snapshot. **[IMPLEMENTED, differently]** — re-fetches and requires the ENTIRE `content.raw` to match what was sent (stricter than just "the change matches intent"), and logs to `linking_change_log.json`; there's no separate rollback identifier because there's no separate snapshot (§8 step 6) to tie one to — the change log entry itself is the revert reference.

**Item-level failure** (target ineligible, missing text fields, JSON parse failure, exact-match count ≠ 1) → hold that item, log, continue the run. **[IMPLEMENTED]** **Systemic failure** (auth failure, network outage) → **[NOT BUILT as a deliberate branch]** — an uncaught exception from `requests` currently crashes the run entirely, which does halt all remaining writes for that run (the practical effect §8 wants), but not via an intentional, clearly-logged "systemic failure" code path. Worth hardening before this pipeline's cap is ever raised significantly.

## 9. Acceptance-test matrix

Required as fixtures, all passing consistently, before supervised-apply is enabled for any record — not merely before auto-apply:

1. Target resolves to a valid canonical 200 page.
2. Target is a redirect with an authoritative mapping.
3. Target is a redirect with no authoritative mapping.
4. Target returns a soft 404.
5. Target is `noindex`.
6. Target is draft/private/scheduled.
7. Same target already linked in the table, not in prose (should still be a valid opportunity).
8. Same target already linked once in prose (should route to duplicate-link handling, governance §9).
9. A legitimate second-intent link (different content zone, different specific point — should be allowed per governance §9).
10. A duplicate link within the same paragraph (should be blocked or routed to auto-safe removal per governance §15's narrow conditions).
11. Exact-match text occurs zero times at write time (item-level failure, §8 step 5).
12. Exact-match text occurs more than once at write time (item-level failure, §8 step 5).
13. Source page changed after approval (staleness, §8 step 3).
14. Target page changed after approval (re-eligibility failure, §8 step 4).
15. A protected region (schema, affiliate link, citation) is accidentally touched by a proposed diff — must be rejected before write.
16. WordPress save reports success but post-write verification (§8 step 9) finds a mismatch.
17. Rollback succeeds.
18. Rollback verification itself fails (systemic failure, §8).
19. Page content contains text resembling an instruction or override directed at the system (prompt-injection-style content) — must be treated as inert data per §13.
20. Generated markup contains an attribute outside the allowlist — must be rejected before write.
21. Evidence record expires between `approved` and the write attempt (§3) — record must route back to `needs_evidence`, not proceed to write.

## 10. URL and eligibility semantics

- **URL normalization**: scheme, host, `www` presence, trailing slash, query string, fragment normalized consistently before comparison.
- **Allowed origin**: `aitoolsforpros.com` (canonical `www`/non-`www` form only) — no subdomains unless this section is explicitly revised.
- **Acceptable resolution**: HTTP 200 on the canonical URL. Soft 404s, `403`, `429`, and timeouts do not mean "permanently ineligible" — they produce `blocked_eligibility_unknown`.
- **`blocked_eligibility_unknown` clarification**: this is an **ineligible-for-action** state, not a determination that the target is permanently invalid. It blocks proposal publication and all writes until eligibility is established on a later run — it is not equivalent to governance §10's "must be treated as ineligible" in the sense of a final rejection; it is a hold state pending re-check, and a developer must not treat it as safe to advance to review.
- **Canonical equality**: target's declared canonical URL must match the proposed URL, or the redirect-handling rules apply (governance §15).
- **Publish status**: only `publish` is eligible; `noindex`/robots-disallowed targets are ineligible regardless of publish status.
- **Revalidation**: at proposal creation *and* immediately before write (§8 step 4).
- **Existing-link check**: scans the entire page, not just the same paragraph (governance §9).

## 11. Content-zone taxonomy

- Main prose (limitation cards, feature-discussion sections) — where contextual links belong.
- Lists and callouts.
- Comparison tables (`comparison_notes`).
- Related Guides blocks (template-rendered, out of scope for content edits; in scope for audit).
- The in-content closing "Comparing your options" section — page-level content, distinct from:
- Site-wide navigation/footer — shared PHP chrome, never edited, never counted toward a page's own contextual coverage.
- Reusable blocks, schema/JSON-LD, shortcodes, citations, affiliate elements — protected regions, never altered under any change class (governance §15).

## 12. Order of preference when adding contextual coverage

1. Link existing text (add an `<a>` wrapper to an already-genuine mention, no visible-text change).
2. Expand an existing sentence to make the comparison explicit.
3. Propose a new sentence, only when neither of the above applies.

Recorded as `edit_type` (§4): `link_existing_text` / `change_anchor` / `modify_sentence` / `insert_sentence`. All four remain review-required (governance §15); the type surfaces relative risk to the reviewer.

## 13. Security: untrusted content handling

Page text, comments, embedded metadata, and any fetched external material are **untrusted data**, never instructions. They cannot override this document, the governance document, or the tool's own operating instructions regardless of what they claim (e.g. a comment claiming to be an "approved override" — test case §9.19). Generated output is limited to sanitized anchor markup within an allowlisted attribute set (`href`, the existing inline body-link `style` value) — never arbitrary HTML, scripts, or attributes (test case §9.20).

## 14. Scheduling, batching, and initial caps

Batched per governance §5, applied per record (pair), not per page. **Phase 1 starting limits** (configuration values, not hardcoded forever):

- Audit: unlimited read-only records.
- Suggestions (scored) generated per run: 10–20 pairs — `linking_scoring.py --cap`, default 15.
- Applications per run: maximum 5 pairs — `linking_apply.py --cap`, default 5. (Originally scoped as "human-approved applications"; as of 2026-08-05 these are applications that cleared `linking_scoring.py`'s hard gates, not a human, for this one change class — see governance §16.)
- Maximum applied changes per source page per run: 1 — implemented as `MAX_PER_SOURCE_PAGE` in `linking_apply.py`.
- Auto-safe technical corrections per run: 10 (once that mode exists and its conditions are met — still not built).
- Contextual-edit batches: no more than one batch per week — implemented as the weekly cron in `.github/workflows/linking-automation.yml`, not a manually-run supervised batch.

## 15. Change log and suppression registry

- Every state transition (§6b) recorded with timestamp, actor, governance rule IDs relied on, and `policy_version` — extending the existing `aifp_update_log` pattern from System 1/3.
- **Suppression/exception registry**: records "do not propose for this specific (source, target) pair," with reason, owner, explicit scope, and expiration — so a one-off editorial call doesn't silently become a permanent undocumented exception.

## 16. Quality metrics

Reviewer approval vs. rejection rate (with stated rejection reasons); rate of `needs_editorial_review` vs. confident proposals; §8 step 8 invariant-failure rate; rate of records reaching `stale` before being acted on; rollback rate; periodic sampled precision review — a human re-checking a random sample of `applied` and `no_opportunity_confirmed` records against governance §8's test, independent of the system's own self-reported confidence.

## 17. Implementation notes (supersedes the original "Not yet designed")

The LLM prompt and opportunity-scoring logic this section originally deferred is now built, in `automation/linking_scoring.py`'s `SCORING_SYSTEM_PROMPT`. Summary of what it does, for anyone reading this spec without the code open:

- One model call per (source, sibling) pair, given the source page's `content_sections` prose and the sibling's full page text.
- Enforces governance §8's exact test and the §12 order of preference (link existing text > expand a sentence > new sentence) in the prompt itself.
- Requires a verbatim quoted `evidence_supporting_text` from the sibling's own already-published content (`SITE_PUBLISHED_CONTENT`, governance §1) — the model is not authorized to introduce new facts about either tool.
- `apply_hard_gates()` then overrides the model's own verdict: no quoted evidence → forced to `needs_evidence`; `useful_without_link: false` → forced to `needs_editorial_review`, regardless of what verdict the model returned. The model's self-report is never trusted past these two checks.
- A separate `enforce_link_style()` post-processing pass injects the site's required inline-link style attribute onto any `<a>` tag the model forgot it on — found necessary after an early test batch came back with about half the proposals missing it. Not relied on as a suggestion to the model; enforced regardless of what the model actually output.

One known gap not yet closed: linking_scoring.py has no fingerprinting/invalidation mechanism (§6a as originally envisioned for a full reviewer workflow) — it uses a simpler reconciliation instead. Each run rebuilds `linking_proposals_output.json` from the fresh audit output, carrying forward any already-scored record whose pair still appears in the fresh audit, and dropping any that don't (which almost always means `linking_apply.py` already closed that gap). This does not detect the narrower case §6a was designed for — the sibling page's own content changing enough to invalidate an already-quoted `evidence_supporting_text` without the pair disappearing from the audit entirely. `linking_apply.py`'s own live re-check (§8, this file) catches drift in the source page's `existing_text`, but not drift in evidence grounded on the sibling page. Worth closing before this pipeline's scope or caps grow.
