#!/usr/bin/env python3
"""Second follow-up: the previous diagnostic used an ambiguous anchor phrase
that matched an earlier, unrelated occurrence on the page for 2 of 3 posts.
This searches using the exact full existing_text/proposed_text strings from
the change log (unambiguous), and reports every match position if there's
more than one. Read-only, no writes."""

import json
import sys
from pathlib import Path

# NOTE: this file was moved into automation/incidents/2026-08-05-link-redundancy/
# after it was run (see README.md in this folder). Path resolution below walks
# up to the actual repo root from this archived location.
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))
import requests
from wp_creds import AUTH, WP_URL

log = json.loads((REPO_ROOT / "automation/linking_change_log.json").read_text())
by_source = {e["source_url"]: e for e in log}

CHECKS = [
    (378, "https://aitoolsforpros.com/perplexity/physicians/"),
    (376, "https://aitoolsforpros.com/claude/creatives/"),
]

for post_id, url in CHECKS:
    resp = requests.get(
        f"{WP_URL}/wp/v2/cross_reference/{post_id}",
        params={"context": "edit", "_fields": "id,slug,link,content"},
        auth=AUTH,
    )
    resp.raise_for_status()
    post = resp.json()
    raw = post["content"]["raw"]
    entry = by_source[url]
    existing = entry["existing_text"]
    proposed = entry["proposed_text"]

    print(f"=== post {post_id} ({url}) ===")

    def count_and_show(label, needle):
        count = raw.count(needle)
        print(f"  {label}: {count} occurrence(s)")
        idx = 0
        for _ in range(count):
            idx = raw.find(needle, idx)
            start = max(0, idx - 80)
            end = min(len(raw), idx + len(needle) + 120)
            print("    ...", raw[start:end], "...")
            idx += 1

    count_and_show("existing_text (old, unlinked)", existing)
    count_and_show("proposed_text (new, with link)", proposed)
    print()
