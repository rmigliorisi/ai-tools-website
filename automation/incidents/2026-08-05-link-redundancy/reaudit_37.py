#!/usr/bin/env python3
"""Re-audit the 37 already-applied contextual-link changes against Rich's
2026-08-05 zone-aware redundancy rules (governance update, policy_version
1.3.0). Read-only — makes no writes. For each applied change, fetches the
CURRENT live content.raw for its source page, decodes it, and checks:

  Rule 2 — did the ORIGINAL existing_text already contain a link to the same
    sibling before this edit? If so, the edit created two links to the same
    target within one paragraph.
  Rule 3 — does the section the new link now lives in (found on the live
    page) also carry a comparison-table link and/or the footer "Comparing
    your options?" cross-navigation sentence to the SAME sibling? If so,
    this is the "tightly clustered in the same closing section" pattern
    Rich flagged on the chatgpt/architects -> midjourney example.

Does NOT auto-decide based on total link count (rule 7) and does NOT treat
absence of a table/footer link as proof the addition was good (rule 6) —
those are exactly the blanket heuristics Rich told us not to use. This
script reports classification only; the revert decision is a separate step.
"""

import json
import sys
from pathlib import Path

# NOTE: this file was moved into automation/incidents/2026-08-05-link-redundancy/
# after it was run (see README.md in this folder). REPO now resolves up to the
# actual repo root from this archived location.
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "automation"))

import requests  # noqa: E402
from wp_creds import AUTH, WP_URL  # noqa: E402
from linking_audit import classify_existing_links, find_section_containing  # noqa: E402

CHANGE_LOG = REPO / "automation/linking_change_log.json"


def fetch_page(post_id):
    resp = requests.get(
        f"{WP_URL}/wp/v2/cross_reference/{post_id}",
        params={"context": "edit", "_fields": "id,slug,link,content"},
        auth=AUTH,
    )
    resp.raise_for_status()
    post = resp.json()
    data = json.loads(post["content"]["raw"])
    return post, data


def main():
    log = json.loads(CHANGE_LOG.read_text())
    applied = [e for e in log if e.get("status") == "applied"]
    print(f"{len(applied)} applied entries to re-audit.\n")

    page_cache = {}
    keep, revert, unclear = [], [], []

    for entry in applied:
        source_post_id = int(entry["record_id"].split("_")[1])
        sibling_slug = entry["sibling_tool"]

        if source_post_id not in page_cache:
            page_cache[source_post_id] = fetch_page(source_post_id)
        post, data = page_cache[source_post_id]

        rule2_violation = f"/{sibling_slug}/" in entry["existing_text"]

        section_now = find_section_containing(data, entry["proposed_text"])
        counts, closing_titles = classify_existing_links(data, sibling_slug)
        rule3_violation = bool(section_now) and section_now in closing_titles and (
            counts["table"] > 0 or counts["footer_sentence"] > 0
        )

        verdict = "KEEP"
        reasons = []
        if rule2_violation:
            verdict = "REVERT"
            reasons.append("rule 2: existing_text already had a link to this same sibling before the edit")
        if rule3_violation:
            verdict = "REVERT"
            reasons.append(
                f"rule 3: new link landed in '{section_now}', which already carries "
                f"table={counts['table']} / footer_sentence={counts['footer_sentence']} link(s) to {sibling_slug}"
            )
        if not section_now:
            unclear.append(entry)
            verdict = "UNCLEAR (couldn't locate proposed_text on live page — check separately)"

        record = {
            "record_id": entry["record_id"],
            "source_url": entry["source_url"],
            "sibling_tool": sibling_slug,
            "section_now": section_now,
            "counts": counts,
            "closing_titles": sorted(closing_titles),
            "verdict": verdict,
            "reasons": reasons,
        }
        if verdict == "REVERT":
            revert.append(record)
        elif verdict.startswith("KEEP"):
            keep.append(record)

        print(f"[{entry['record_id']}] {entry['source_url']} -> {sibling_slug}: {verdict}")
        if reasons:
            for r in reasons:
                print(f"    {r}")

    print(f"\n=== Summary: {len(keep)} keep, {len(revert)} revert, {len(unclear)} unclear ===\n")
    if revert:
        print("REVERT candidates:")
        for r in revert:
            print(f"  {r['record_id']}  {r['source_url']} -> {r['sibling_tool']}")
            for reason in r["reasons"]:
                print(f"      {reason}")

    out_path = Path(__file__).resolve().parent / "reaudit_37_output.json"
    out_path.write_text(json.dumps({"keep": keep, "revert": revert, "unclear": [e["record_id"] for e in unclear]}, indent=2))
    print(f"\nFull classification written to {out_path}")


if __name__ == "__main__":
    main()
