#!/usr/bin/env python3
"""Revert the 7 changes reaudit_37.py flagged as rule-3 violations (new
contextual link landed in the same closing section as an existing table
and/or footer "Comparing your options?" link to the same target — the
tightly-clustered pattern Rich flagged on chatgpt/architects -> midjourney).

Writes existing_text back over proposed_text — the exact reverse of
linking_apply.py's apply direction, reusing the same decode-JSON / replace
on the decoded structure / re-encode / PUT / re-fetch-verify pattern (the
_replace_in_value / _count_in_value functions are imported from
system3_monthly.py, not duplicated). Appends a "reverted" entry to
linking_change_log.json for each — the original "applied" entry is left
in place (append-only log, matching how the rest of this pipeline logs).

Usage:
    python3 revert_7.py --dry-run   # re-checks only, no writes
    python3 revert_7.py             # live: writes + logs
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# NOTE: this file was moved into automation/incidents/2026-08-05-link-redundancy/
# after it was run (see README.md in this folder). REPO now resolves up to the
# actual repo root from this archived location. The 7 reverts listed below have
# already been applied and verified — do not re-run this against them again;
# see linking_change_log.json for the "reverted" entries.
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "automation"))

import requests  # noqa: E402
from wp_creds import AUTH, WP_URL  # noqa: E402
from system3_monthly import _replace_in_value, _count_in_value, run_selftests  # noqa: E402

CHANGE_LOG_PATH = REPO / "automation/linking_change_log.json"

REVERT_RECORD_IDS = [
    "rec_378_386",  # perplexity/physicians -> copilot
    "rec_392_376",  # midjourney/creatives -> claude
    "rec_368_400",  # chatgpt/creatives -> grammarly
    "rec_384_391",  # gemini/architects -> midjourney
    "rec_375_391",  # claude/architects -> midjourney
    "rec_367_391",  # chatgpt/architects -> midjourney
    "rec_379_389",  # perplexity/finance -> copilot
]


def api_get(post_id, fields):
    resp = requests.get(
        f"{WP_URL}/wp/v2/cross_reference/{post_id}",
        params={"context": "edit", "_fields": fields},
        auth=AUTH,
    )
    resp.raise_for_status()
    return resp.json()


def api_put_content(post_id, new_raw):
    resp = requests.post(
        f"{WP_URL}/wp/v2/cross_reference/{post_id}",
        headers={"X-HTTP-Method-Override": "PUT", "Content-Type": "application/json; charset=utf-8"},
        auth=AUTH,
        data=json.dumps({"content": new_raw}, ensure_ascii=False).encode("utf-8"),
    )
    resp.raise_for_status()
    return resp.json()


def append_change_log(entries):
    existing = []
    if CHANGE_LOG_PATH.exists():
        try:
            existing = json.loads(CHANGE_LOG_PATH.read_text())
        except json.JSONDecodeError:
            existing = []
    CHANGE_LOG_PATH.write_text(json.dumps(existing + entries, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    run_selftests()

    log = json.loads(CHANGE_LOG_PATH.read_text())
    by_id = {e["record_id"]: e for e in log if e.get("status") == "applied"}

    new_log_entries = []
    results = []

    for record_id in REVERT_RECORD_IDS:
        entry = by_id.get(record_id)
        if not entry:
            print(f"SKIP [{record_id}] — no applied entry found in change log")
            continue

        source_id = int(record_id.split("_")[1])
        existing_text = entry["existing_text"]  # original, pre-edit sentence — what we're reverting TO
        proposed_text = entry["proposed_text"]  # currently-live sentence with the added link — what we're reverting FROM

        source = api_get(source_id, "id,slug,content")
        data = json.loads(source["content"]["raw"])

        counter = [0]
        _count_in_value(data, proposed_text, counter)
        if counter[0] != 1:
            print(f"HOLD [{record_id}] — proposed_text matched {counter[0]}x at revert time (expected exactly 1; "
                  f"page may have changed since the audit). Not reverting — check manually.")
            results.append((record_id, "held", counter[0]))
            continue

        print(f"{'[DRY RUN] would revert' if args.dry_run else 'REVERTING'} [{record_id}]: "
              f"{entry['source_url']} -> {entry['sibling_tool']}")

        if args.dry_run:
            results.append((record_id, "dry_run_ok", 1))
            continue

        counter = [0]
        new_data = _replace_in_value(data, proposed_text, existing_text, counter)
        new_raw = json.dumps(new_data, ensure_ascii=False)
        api_put_content(source_id, new_raw)

        verify = api_get(source_id, "content")
        if verify["content"]["raw"] == new_raw:
            print(f"    WRITTEN + VERIFIED — confirmed by re-fetch.")
            status, reason = "reverted", "replaced 1x (proposed_text -> existing_text), verified by re-fetch"
        else:
            print(f"    WRITTEN BUT UNVERIFIED — re-fetched content.raw does not match what was sent.")
            status, reason = "reverted_unverified", "post-write re-fetch did not match sent content"

        results.append((record_id, status, 1))
        new_log_entries.append({
            "record_id": entry["record_id"],
            "source_url": entry["source_url"],
            "target_url": entry["target_url"],
            "primary_tool": entry["primary_tool"],
            "sibling_tool": entry["sibling_tool"],
            "profession": entry["profession"],
            "anchor_text": entry.get("anchor_text"),
            "existing_text": proposed_text,  # what it was (pre-revert)
            "proposed_text": existing_text,  # what it's reverted to
            "rationale": "Reverted per Rich's 2026-08-05 zone-aware redundancy rules, rule 3: this contextual "
                         "link landed in the page's closing section, which already carried a comparison-table "
                         "and/or footer cross-navigation link to the same sibling — tightly clustered.",
            "policy_version": "1.3.0",
            "status": status,
            "reason": reason,
            "applied_at": datetime.now(timezone.utc).isoformat(),
        })

    if new_log_entries:
        append_change_log(new_log_entries)
        print(f"\n{len(new_log_entries)} revert(s) appended to {CHANGE_LOG_PATH.name}.")

    print(f"\n{'=' * 60}\nSUMMARY\n{'=' * 60}")
    for record_id, status, count in results:
        print(f"  [{status}] {record_id} (match count: {count})")


if __name__ == "__main__":
    main()
