#!/usr/bin/env python3
"""Follow-up diagnostic: neither existing_text nor proposed_text matched the
live content.raw for 3 posts. This prints the actual raw text surrounding
a short, distinctive anchor phrase from each, so we can see exactly what's
there now instead of just a boolean match/no-match. Read-only, no writes."""

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
    (378, "Claude or ChatGPT"),       # perplexity/physicians -> copilot
    (376, "Grammarly"),                # claude/creatives -> grammarly
    (389, "Microsoft's ecosystem"),    # copilot/finance -> gemini
]

for post_id, anchor in CHECKS:
    resp = requests.get(
        f"{WP_URL}/wp/v2/cross_reference/{post_id}",
        params={"context": "edit", "_fields": "id,slug,link,content"},
        auth=AUTH,
    )
    resp.raise_for_status()
    post = resp.json()
    raw = post["content"]["raw"]
    print(f"=== post {post_id} ({post['link']}) — searching for {anchor!r} ===")
    idx = raw.find(anchor)
    if idx == -1:
        print("  Anchor phrase not found AT ALL in live content.raw.")
    else:
        start = max(0, idx - 150)
        end = min(len(raw), idx + 250)
        print("  Context around match:")
        print(" ", raw[start:end])
    print()
