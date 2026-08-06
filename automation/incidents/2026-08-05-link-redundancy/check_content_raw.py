#!/usr/bin/env python3
"""One-off, read-only check: does the LIVE, AUTHORITATIVE content.raw for these
three cross_reference posts actually contain the link linking_apply.py's change
log says it wrote? This checks the REST API directly (bypassing any public-page
cache entirely), which is the only way to know for certain whether the write
really took or whether the live-page mismatch seen via a plain public fetch is
just cache lag. Makes no writes."""

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

CHECKS = [
    (378, "https://aitoolsforpros.com/copilot/physicians/"),  # perplexity/physicians -> copilot
    (376, "https://aitoolsforpros.com/grammarly/creatives/"),  # claude/creatives -> grammarly
    (389, "https://aitoolsforpros.com/gemini/finance/"),       # copilot/finance -> gemini
]

log = json.loads((REPO_ROOT / "automation/linking_change_log.json").read_text())
by_post = {}
for e in log:
    by_post[e["source_url"]] = e

for post_id, _ in CHECKS:
    resp = requests.get(
        f"{WP_URL}/wp/v2/cross_reference/{post_id}",
        params={"context": "edit", "_fields": "id,slug,link,content"},
        auth=AUTH,
    )
    resp.raise_for_status()
    post = resp.json()
    raw = post["content"]["raw"]
    entry = by_post.get(post["link"])
    print(f"=== post {post_id} ({post['link']}) ===")
    if entry:
        proposed = entry["proposed_text"]
        print("Expected proposed_text found in live content.raw:", proposed in raw)
        if proposed not in raw:
            print("  Expected existing_text still present instead:", entry["existing_text"] in raw)
    else:
        print("  No matching change log entry found for this URL.")
    print()
