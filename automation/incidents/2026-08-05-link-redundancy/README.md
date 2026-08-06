# Incident: internal-link redundancy from the 2026-08-05 auto-apply batch

**Status: resolved.** These scripts are historical records of a one-time
diagnosis-and-cleanup pass, not part of the recurring internal-linking
pipeline. They already ran to completion (see `linking_change_log.json` at
the repo root for the actual applied/reverted entries). Nothing here needs
to run again on a schedule, and nothing in `automation/linking_audit.py`,
`linking_scoring.py`, or `linking_apply.py` imports from this folder.

## What happened

On 2026-08-05, Rich ran a large manual batch of the internal-linking
auto-apply pipeline (score_cap=150, apply_cap=45), producing 37 applied
contextual-link changes. Reviewing the results, he flagged that some of
these landed a new contextual link onto a page that already had a
comparison-table link AND the "Comparing your options?" footer
cross-navigation sentence pointing at the same sibling tool — visually
clustering multiple links to one target in the page's closing section.
That's the exact problem the whole internal-linking project originally set
out to fix, now reappearing from the opposite direction (too many links to
one target, instead of too few).

Rich's fix wasn't "block on total link count" — he explicitly rejected
that as too blunt (a table link plus one genuinely useful contextual link
is normal). Instead he specified 7 zone-aware rules (classify every link by
purpose — table / footer sentence / genuine contextual mention — before
judging redundancy). Those rules are now implemented directly in
`automation/linking_audit.py` (`classify_existing_links`,
`find_section_containing`) and enforced in `automation/linking_scoring.py`
(`apply_placement_gates`) as of policy_version 1.3.0 — that's the permanent
fix, and it's what the Wednesday scheduled pipeline runs today.

## What's in this folder, in the order it was used

1. **`check_content_raw.py` → `check_content_raw2.py` → `check_content_raw3.py`
   → `check_content_raw4.py`** — four iterations of verifying that 4
   apparently-missing live changes had actually been written. The first
   three each had a real bug (comparing against the still-JSON-encoded raw
   string instead of the decoded content, or matching an ambiguous short
   anchor phrase) — kept here as a worked example of that bug class, since
   it's the same mistake `system3_monthly.py`'s `render_page_text` /
   `flatten_text_fields` were built to avoid, and it's easy to reintroduce.
   `check_content_raw4.py` is the corrected version; it confirmed the
   4 "missing" changes were actually just WordPress.com/Jetpack public-page
   cache lag, not a write failure.
2. **`reaudit_37.py`** — re-ran the new zone-aware classification rules
   against all 37 originally-applied changes. Result: 30 kept, 7 flagged as
   rule-3 violations (new link clustered in the same closing section as an
   existing table/footer link to the same target). Output preserved in
   `reaudit_37_output.json`.
3. **`revert_7.py`** — reverted exactly those 7 flagged changes (writing
   `existing_text` back over `proposed_text`, same decode/replace/re-fetch-
   verify pattern the rest of the pipeline uses). All 7 reverts succeeded
   and were verified by re-fetch; see the `"reverted"` entries in
   `automation/linking_change_log.json` for the record.

## If you're a future dev (or AI) reading this

You don't need to run any of these again. If you're trying to understand
the CURRENT redundancy-prevention logic, read `classify_existing_links()`
and `apply_placement_gates()` in the two files named above — this folder is
just the paper trail for how that logic was designed and validated against
real, already-published pages.
