#!/usr/bin/env python3
"""Corrected diagnostic: decode content.raw as JSON FIRST (like linking_apply.py
does), then search the DECODED text for existing_text/proposed_text. Comparing
against the still-encoded raw string (as the previous two diagnostics did) is
unreliable whenever the text contains any non-ASCII character, since default
JSON encoding escapes those as \\uXXXX sequences in the raw string. Read-only,
no writes."""

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

sys.path.insert(0, str(REPO_ROOT / "automation"))
from system3_monthly import _count_in_value  # noqa: E402 — same tested logic linking_apply.py uses

log = json.loads((REPO_ROOT / "automation/linking_change_log.json").read_text())
by_source = {e["source_url"]: e for e in log}

CHECKS = [
    (378, "https://aitoolsforpros.com/perplexity/physicians/"),
    (376, "https://aitoolsforpros.com/claude/creatives/"),
    (389, "https://aitoolsforpros.com/copilot/finance/"),
]

for post_id, url in CHECKS:
    resp = requests.get(
        f"{WP_URL}/wp/v2/cross_reference/{post_id}",
        params={"context": "edit", "_fields": "id,slug,link,content"},
        auth=AUTH,
    )
    resp.raise_for_status()
    post = resp.json()
    data = json.loads(post["content"]["raw"])  # decode FIRST, then search
    entry = by_source[url]

    existing_count = [0]
    _count_in_value(data, entry["existing_text"], existing_count)
    proposed_count = [0]
    _count_in_value(data, entry["proposed_text"], proposed_count)

    print(f"=== post {post_id} ({url}) ===")
    print(f"  existing_text (old, unlinked) found: {existing_count[0]}x")
    print(f"  proposed_text (new, with link) found: {proposed_count[0]}x")
    print()
