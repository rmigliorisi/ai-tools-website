#!/usr/bin/env python3
"""
Internal Linking Automation — auto-apply step (spec §8's fail-closed write
protocol, Operating Mode "auto-apply").

Third implementation increment against docs/AIFORPROS-INTERNAL-LINKING-
AUTOMATION-SPEC.md (policy_version 1.2.0+). Graduated straight to autonomous
apply per Rich's decision on 2026-08-05 to bring internal linking up to the
same standard System 1 (weekly tool update) and System 3 (monthly editorial
review) already run at: a hard-gated model verdict stands in for a human
reviewer, and a fail-closed write protocol (re-verify before writing, re-fetch
to confirm after writing, log everything, cap the blast radius) stands in for
a human's judgment about when something is safe to trust. Nothing here is
gated on Rich's approval before publish — the digest email at the end is
informational, matching System 1/3's "automation, not invisibility" pattern,
not a gate.

WHAT THIS DOES, END TO END, EACH RUN:
  1. Reads automation/linking_proposals_output.json (produced by
     linking_scoring.py) and takes only records already in state
     "opportunity_proposed" — meaning they already cleared linking_scoring.py's
     hard gates (useful_without_link, quoted evidence_supporting_text). This
     script does not re-litigate the model's editorial judgment; it only
     re-verifies that the world hasn't changed since that judgment was made.
  2. For each candidate, re-checks TWO things live, at apply time, because
     audit -> scoring -> apply can span separate scheduled runs and either
     side of the pair could have moved in between:
       a. The target page is still eligible (governance §10 / spec §10's
          exact check — reused verbatim from linking_audit.check_eligibility,
          not re-implemented) — still published, still resolves to its own
          canonical URL.
       b. The source page's existing_text is still present VERBATIM, exactly
          once, in the source page's current decoded content. Zero matches
          means the page already changed out from under this proposal; more
          than one means the proposed edit is no longer unambiguous. Either
          way: hold, don't guess.
  3. Applies via the exact tested pattern System 3 already proved safe on a
     live site with no human review before publish: decode content.raw as
     JSON, replace on the DECODED structure (never raw escaped JSON text),
     re-encode, PUT, then re-fetch and diff to confirm the write actually
     took. The replace/count functions themselves are IMPORTED from
     system3_monthly.py, not duplicated — this reuses code that already has
     a self-test suite covering the exact quote-escaping bug that bit the
     July 2026 manual cycle, rather than re-deriving that logic in a second,
     untested copy that could reintroduce the same bug.
  4. Caps + backlog, per spec §14: at most CAP records applied per run
     (default 5), at most 1 applied change per source page per run. Overflow
     (skipped only because the cap was hit, not because a re-check failed)
     queues to automation/linking_backlog.json and is applied first next run,
     oldest first — the same first-in-first-out pattern System 3 uses.
     Records that FAIL a live re-check are held and logged, but not
     re-queued: they are not stale-due-to-capacity, they are stale-due-to-
     drift, and the next linking_audit.py run will regenerate a fresh,
     re-verified proposal for that pair if the underlying gap still exists.
  5. Every applied change is appended to automation/linking_change_log.json
     (append-only, never overwritten) — the safety net: enough detail
     (record_id, exact old/new text, urls, evidence, confidence, timestamp)
     that any single change can be found and manually reverted (by writing
     existing_text back over proposed_text) without having to reconstruct
     what happened from WordPress revision history.
  6. Sends the same digest endpoint System 1/3 already use
     (POST /wp-json/aifp/v1/update-digest) so Rich sees a summary every run,
     even though nothing is gated on his approval.

Scope: only `cross_reference` posts (governance §11 — Phase 1 is the only
editable source type; tool_review and profession_hub remain audit-only/out
of scope for writes).

Environment: WORDPRESS_USERNAME, WORDPRESS_APP_PASSWORD (via wp_creds.py).
No ANTHROPIC_API_KEY needed here — this script makes no model calls; all the
judgment already happened in linking_scoring.py.

Usage:
    python3 automation/linking_apply.py              # live run: applies + digest
    python3 automation/linking_apply.py --dry-run    # re-checks only, no writes, no digest, no backlog/log changes
    python3 automation/linking_apply.py --cap 3      # override the per-run cap (default 5)
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from system3_monthly import _replace_in_value, _count_in_value, run_selftests, post_digest  # noqa: E402 — reuse tested core, don't duplicate it
from linking_audit import check_eligibility  # noqa: E402 — reuse the exact spec §10 eligibility check, don't duplicate it

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import requests  # noqa: E402
from wp_creds import AUTH, WP_URL  # noqa: E402

PROPOSALS_PATH = Path(__file__).resolve().parent / "linking_proposals_output.json"
BACKLOG_PATH = Path(__file__).resolve().parent / "linking_backlog.json"
CHANGE_LOG_PATH = Path(__file__).resolve().parent / "linking_change_log.json"

DEFAULT_CAP = 5          # spec §14: max approved applications per run
MAX_PER_SOURCE_PAGE = 1  # spec §14: max 1 applied change per source page per run


# ---------------------------------------------------------------------------
# REST helpers — requests-based, matching linking_audit.py / linking_scoring.py
# ---------------------------------------------------------------------------

def api_get(post_type, post_id, fields):
    resp = requests.get(
        f"{WP_URL}/wp/v2/{post_type}/{post_id}",
        params={"context": "edit", "_fields": fields},
        auth=AUTH,
    )
    resp.raise_for_status()
    return resp.json()


def api_put_content(post_type, post_id, new_raw):
    resp = requests.post(
        f"{WP_URL}/wp/v2/{post_type}/{post_id}",
        headers={"X-HTTP-Method-Override": "PUT", "Content-Type": "application/json; charset=utf-8"},
        auth=AUTH,
        data=json.dumps({"content": new_raw}, ensure_ascii=False).encode("utf-8"),
    )
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# Backlog + change log (same shape/spirit as system3_backlog.json)
# ---------------------------------------------------------------------------

def load_backlog():
    if not BACKLOG_PATH.exists():
        return []
    try:
        return json.loads(BACKLOG_PATH.read_text())
    except json.JSONDecodeError:
        print(f"  WARNING: {BACKLOG_PATH} failed to parse — treating backlog as empty this run.")
        return []


def save_backlog(entries):
    BACKLOG_PATH.write_text(json.dumps(entries, indent=2, ensure_ascii=False))


def append_change_log(entries):
    existing = []
    if CHANGE_LOG_PATH.exists():
        try:
            existing = json.loads(CHANGE_LOG_PATH.read_text())
        except json.JSONDecodeError:
            existing = []
    CHANGE_LOG_PATH.write_text(json.dumps(existing + entries, indent=2, ensure_ascii=False))


def log_entry(record, status, reason):
    return {
        "record_id": record["record_id"],
        "source_url": record["source_url"],
        "target_url": record["target_url"],
        "primary_tool": record["primary_tool"],
        "sibling_tool": record["sibling_tool"],
        "profession": record["profession"],
        "anchor_text": record.get("anchor_text"),
        "existing_text": record.get("existing_text"),
        "proposed_text": record.get("proposed_text"),
        "rationale": record.get("rationale"),
        "evidence": record.get("evidence"),
        "confidence": record.get("confidence"),
        "policy_version": record.get("policy_version"),
        "status": status,
        "reason": reason,
        "applied_at": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Apply one record
# ---------------------------------------------------------------------------

def apply_record(record, dry_run, change_log):
    record_id = record["record_id"]
    post_type = "cross_reference"
    source_id = record["source_post_id"]
    target_id = record["canonical_target_id"]

    # Live re-check #1: is the target still eligible right now, not just at audit time?
    target = api_get(post_type, target_id, "status,link")
    eligible, elig_status, elig_detail = check_eligibility({"status": target["status"], "link": target["link"]})
    if not eligible:
        print(f"  HOLD [{record_id}] — target no longer eligible: {elig_detail}")
        change_log.append(log_entry(record, "held", f"target re-check failed ({elig_status}): {elig_detail}"))
        return "held"

    old_text = record.get("existing_text")
    new_text = record.get("proposed_text")
    if not old_text or not new_text:
        print(f"  HOLD [{record_id}] — missing existing_text or proposed_text")
        change_log.append(log_entry(record, "held", "missing existing_text or proposed_text"))
        return "held"

    source = api_get(post_type, source_id, "id,slug,content")
    try:
        data = json.loads(source["content"]["raw"])
    except json.JSONDecodeError as e:
        print(f"  HOLD [{record_id}] — source page JSON failed to parse ({e})")
        change_log.append(log_entry(record, "held", f"source JSON parse failure: {e}"))
        return "held"

    # Live re-check #2: is existing_text still present, exactly once, right now?
    counter = [0]
    _count_in_value(data, old_text, counter)
    if counter[0] != 1:
        print(f"  HOLD [{record_id}] — existing_text matched {counter[0]}x at apply time (expected exactly 1; "
              f"page may have drifted since scoring)")
        change_log.append(log_entry(record, "held", f"existing_text match count = {counter[0]} at apply time, expected 1"))
        return "held"

    print(f"  {'[DRY RUN] would apply' if dry_run else 'APPLYING'} [{record_id}]: "
          f"{record['primary_tool']} -> {record['sibling_tool']} ({record['profession']})")

    if dry_run:
        change_log.append(log_entry(record, "dry_run", "re-checks passed, not written (dry run)"))
        return "applied"

    counter = [0]
    new_data = _replace_in_value(data, old_text, new_text, counter)
    new_raw = json.dumps(new_data, ensure_ascii=False)
    api_put_content(post_type, source_id, new_raw)

    verify = api_get(post_type, source_id, "content")
    if verify["content"]["raw"] == new_raw:
        print(f"    WRITTEN + VERIFIED — confirmed by re-fetch.")
        change_log.append(log_entry(record, "applied", "replaced 1x, verified by re-fetch"))
    else:
        print(f"    WRITTEN BUT UNVERIFIED — re-fetched content.raw does not match what was sent. Check manually.")
        change_log.append(log_entry(record, "applied_unverified", "post-write re-fetch did not match sent content"))
    return "applied"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Re-checks only — no writes, no digest, no backlog/log changes")
    parser.add_argument("--cap", type=int, default=DEFAULT_CAP, help=f"Max records applied per run (default {DEFAULT_CAP})")
    args = parser.parse_args()

    run_selftests()  # fail closed: reuses System 3's proven tests for the exact replace/count functions this script depends on

    if not PROPOSALS_PATH.exists():
        print(f"ERROR: {PROPOSALS_PATH} not found. Run linking_audit.py then linking_scoring.py first.")
        return

    proposals = json.loads(PROPOSALS_PATH.read_text())
    opportunities = [r for r in proposals if r.get("state") == "opportunity_proposed"]

    backlog = load_backlog()
    backlog_ids = {r["record_id"] for r in backlog}
    new_ones = [r for r in opportunities if r["record_id"] not in backlog_ids]
    queue = backlog + new_ones

    print(f"Queue: {len(backlog)} carried over from backlog + {len(new_ones)} new opportunity_proposed record(s) "
          f"= {len(queue)} total. Cap this run: {args.cap} (max {MAX_PER_SOURCE_PAGE} per source page).\n")

    change_log = []
    applied_count = 0
    per_page_count = {}
    remaining = []

    for record in queue:
        page_id = record["source_post_id"]
        if applied_count >= args.cap or per_page_count.get(page_id, 0) >= MAX_PER_SOURCE_PAGE:
            remaining.append(record)
            continue

        result = apply_record(record, args.dry_run, change_log)
        if result == "applied":
            applied_count += 1
            per_page_count[page_id] = per_page_count.get(page_id, 0) + 1
        # "held" records are logged but not re-queued — see docstring §4.

    print(f"\n{'=' * 60}\nSUMMARY — {len(change_log)} change log entries this run\n{'=' * 60}")
    for c in change_log:
        print(f"  [{c['status']}] {c['record_id']}: {c['primary_tool']} -> {c['sibling_tool']} ({c['profession']}) — {c['reason']}")

    if args.dry_run:
        print(f"\n[DRY RUN] {applied_count} would be applied, {len(remaining)} would queue/skip. "
              f"No writes, no backlog change, no change log entry saved, no digest sent.")
        return

    save_backlog(remaining)
    if remaining:
        print(f"\n{len(remaining)} record(s) queued to {BACKLOG_PATH.name} for next run.")

    applied_entries = [c for c in change_log if c["status"] in ("applied", "applied_unverified")]
    if applied_entries:
        append_change_log(applied_entries)
        print(f"{len(applied_entries)} applied change(s) appended to {CHANGE_LOG_PATH.name}.")

    if change_log:
        digest_payload = [{
            "tool": c["primary_tool"],
            "field": f"{c['source_url']} -> {c['sibling_tool']} ({c['target_url']})",
            "old_value": (c["existing_text"] or "")[:200],
            "new_value": (c["proposed_text"] or "")[:200],
            "source": c["target_url"],
            "status": c["status"],
            "reason": c["reason"],
        } for c in change_log]
        digest_result = post_digest(digest_payload)
        print(f"\nDigest sent: {digest_result}")
    else:
        print("\nNo changes this run — no digest sent.")


if __name__ == "__main__":
    main()
