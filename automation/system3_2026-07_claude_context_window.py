#!/usr/bin/env python3
"""
System 3 approved-edit patcher — Claude 200K -> 1M context window (July 2026 cycle)

Applies the specific, Rich-approved text replacements identified during the
July 2026 System 3 monthly editorial review: Claude Sonnet 5 now supports a
1M-token context window on Pro, Team, and Enterprise plans (previously 200K
on Pro/Team), per Anthropic's own current documentation. Seven cross_reference
pages (Claude x Engineers/Physicians/Finance/Insurance/Legal/Real Estate/
Creatives) still stated the old 200K figure across various fields (bottom
lines, key takeaways, comparison tables, FAQs, one section heading). Claude
for Architects was already corrected in the prior cycle and is intentionally
not touched here.

This is a one-off, run-once-at-approval script (see docs/AIFORPROS-AUTOMATED-
CONTENT.md, System 3, step 7) — not a scheduled job. It does NOT re-research
or re-decide anything; every replacement below was already reviewed and
approved by Rich in chat on 2026-07-25.

Safety:
  - Defaults to dry-run: fetches, diffs, reports, writes nothing.
  - For each replacement, counts literal occurrences in the live content.raw
    before touching it. If the count is 0 (text has since changed / already
    fixed by someone else), that edit is skipped and flagged rather than
    guessed at.
  - Re-validates the whole content string as JSON both before and after
    edits, before ever PUTing.
  - Only ever touches the exact substrings listed below — no wholesale
    rewrites, nothing outside what's explicitly listed here.

Usage:
    python3 automation/system3_2026-07_claude_context_window.py           # dry run
    python3 automation/system3_2026-07_claude_context_window.py --apply   # writes for real
"""

import argparse
import json
import ssl
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from wp_creds import HEADERS, BASE  # noqa: E402

try:
    # macOS python.org installs often ship without a working root CA bundle
    # wired into the `ssl` module ("CERTIFICATE_VERIFY_FAILED: unable to get
    # local issuer certificate"). certifi provides a bundle directly so we
    # don't depend on the OS keychain being configured for Python.
    import certifi
    CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    CTX = ssl.create_default_context()

SOURCE_NOTE = (
    "Anthropic, 'Introducing Claude Sonnet 5' (anthropic.com/news/claude-sonnet-5, "
    "Jun 30, 2026) + Claude Help Center, 'How large is the context window on paid "
    "Claude plans?' (support.claude.com, updated Jul 25, 2026): Claude Opus 5 and "
    "Sonnet 5 support a 1M-token context window on all paid plans (Pro, Team, "
    "Enterprise) when chatting with Claude."
)

# slug -> [(old_text, new_text), ...]  Every pair below was shown to Rich verbatim
# in the July 2026 System 3 report and approved in chat before this script existed.
EDITS = {
    "claude-engineers": [
        ("The 200K context window is not a marketing feature, it changes what you can review and reason about in a single session.",
         "The 1M-token context window is not a marketing feature, it changes what you can review and reason about in a single session."),
        ("The 200K context window lets you paste an entire service layer, PR diff, or spec document for reasoning in one session.",
         "The 1M-token context window lets you paste an entire service layer, PR diff, or spec document for reasoning in one session."),
        ("This is where the 200K context window creates a workflow that simply does not exist with smaller-context tools",
         "This is where the 1M-token context window creates a workflow that simply does not exist with smaller-context tools"),
        ("The 200K context window is large, but a real enterprise monorepo may be orders of magnitude larger.",
         "The 1M-token context window is large, but a real enterprise monorepo may still be orders of magnitude larger."),
        ("Claude's 200,000-token context window is large enough to hold substantial sections of a codebase",
         "Claude's 1M-token context window (on Pro, Team, and Enterprise plans) is large enough to hold substantial sections of a codebase"),
    ],
    "claude-physicians": [
        ("Its 200K context window enables full-record analysis that shorter-context tools cannot match.",
         "Its 1M-token context window enables full-record analysis that shorter-context tools cannot match."),
        ("The 200K context window lets you paste a complete de-identified record and get a structured clinical summary in minutes.",
         "The 1M-token context window lets you paste a complete de-identified record and get a structured clinical summary in minutes."),
        ("Full Clinical Record Analysis: Where the 200K Window Changes Things",
         "Full Clinical Record Analysis: Where the 1M-Token Window Changes Things"),
        ("200,000 tokens",
         "1M tokens (Pro, Team, Enterprise)"),
        ("Claude's 200,000-token context window lets you paste a full discharge summary, specialist consultation notes, operative report, and medication list into a single session",
         "Claude's 1M-token context window lets you paste a full discharge summary, specialist consultation notes, operative report, and medication list into a single session"),
    ],
    "claude-finance": [
        ("Its 200K context window is why financial advisors use it when document length is the constraint.",
         "Its 1M-token context window is why financial advisors use it when document length is the constraint."),
        ("Claude's 200K context window creates a meaningful difference versus competitors.",
         "Claude's 1M-token context window creates a meaningful difference versus competitors."),
        ("200K context window allows full prospectus, financial plan, or regulatory filing review in a single session",
         "1M-token context window allows full prospectus, financial plan, or regulatory filing review in a single session"),
        ("Claude's 200,000 token context window can handle very long documents including full prospectuses, comprehensive financial plans, and detailed regulatory filings in a single session",
         "Claude's 1M-token context window (on Pro, Team, and Enterprise plans) can handle very long documents including full prospectuses, comprehensive financial plans, and detailed regulatory filings in a single session"),
    ],
    "claude-insurance": [
        ("Claude's 200K context window creates a meaningful difference.",
         "Claude's 1M-token context window creates a meaningful difference."),
        ("200K context window handles full commercial policies including base form plus all endorsements",
         "1M-token context window handles full commercial policies including base form plus all endorsements"),
        ("Claude's 200,000 token context window can handle very long commercial policies including base forms, endorsements, and schedules",
         "Claude's 1M-token context window can handle very long commercial policies including base forms, endorsements, and schedules"),
        ("Claude's 200K window allows the entire policy, base form plus endorsements, to be reviewed in a single session with full context.",
         "Claude's 1M-token window allows the entire policy, base form plus endorsements, to be reviewed in a single session with full context."),
    ],
    "claude-legal": [
        ("Best-in-class (200K context)",
         "Best-in-class (1M context)"),
        ("Claude's context window (200,000 tokens on Pro and Team plans) can ingest a 150-page agreement in a single session",
         "Claude's context window (1M tokens on Pro, Team, and Enterprise plans) can ingest a 150-page agreement in a single session"),
        ('Most reviews lead with "Claude has a 200K context window" as if it is a storage specification.',
         'Most reviews lead with "Claude has a 1M-token context window" as if it is a storage specification.'),
        ("The free and standard Pro plans have a smaller context window than the Team and Enterprise tiers.",
         "The free plan has a smaller context window than the Pro, Team, and Enterprise tiers, which all now support Claude's 1M-token window."),
    ],
    "claude-real-estate": [
        ("Its 200K context window is not a talking point, it changes what you can do in a single session.",
         "Its 1M-token context window is not a talking point, it changes what you can do in a single session."),
        ("The 200K context window lets you paste a full HOA package or purchase agreement and get a working summary in minutes.",
         "The 1M-token context window lets you paste a full HOA package or purchase agreement and get a working summary in minutes."),
        ("Claude's key advantage for real estate agents is its 200,000-token context window, which allows it to process entire purchase agreements",
         "Claude's key advantage for real estate agents is its 1M-token context window, which allows it to process entire purchase agreements"),
        ("The 200K context window is different because it unlocks a workflow that does not exist with smaller-context tools.",
         "The 1M-token context window is different because it unlocks a workflow that does not exist with smaller-context tools."),
    ],
    "claude-creatives": [
        ("Claude handles these well because the 200K context window means it can hold a full brand guide",
         "Claude handles these well because the 1M-token context window means it can hold a full brand guide"),
    ],
}


def api_get(path, query=""):
    req = urllib.request.Request(f"{BASE}{path}{query}", headers=HEADERS)
    with urllib.request.urlopen(req, context=CTX) as r:
        return json.loads(r.read())


def api_put(path, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(f"{BASE}{path}", data=data, headers=HEADERS, method="POST")
    req.add_header("X-HTTP-Method-Override", "PUT")
    with urllib.request.urlopen(req, context=CTX) as r:
        return json.loads(r.read())


def get_post_id(slug):
    results = api_get("/cross_reference", f"?slug={slug}")
    if not results:
        raise RuntimeError(f"No cross_reference post found for slug '{slug}'")
    return results[0]["id"]


def patch_post(slug, edits, dry_run=True):
    post_id = get_post_id(slug)
    post = api_get(f"/cross_reference/{post_id}", "?context=edit")
    raw = post["content"]["raw"]

    json.loads(raw)  # sanity check: must be valid JSON before we touch it

    new_raw = raw
    applied = 0
    print(f"\n=== {slug} (post id {post_id}) ===")
    for old, new in edits:
        count = new_raw.count(old)
        if count == 0:
            print(f"  SKIP (text not found — may have already changed): {old[:70]}...")
            continue
        if count > 1:
            print(f"  NOTE: found {count} occurrences, replacing all: {old[:70]}...")
        new_raw = new_raw.replace(old, new)
        applied += count
        print(f"  OK ({count}x): {old[:60]}\n        -> {new[:60]}")

    json.loads(new_raw)  # sanity check: must still be valid JSON after edits

    if applied == 0:
        print("  Nothing to apply on this page.")
        return

    if dry_run:
        print(f"  [DRY RUN] {applied} replacement(s) staged, no write performed.")
        return

    api_put(f"/cross_reference/{post_id}", {"content": new_raw})
    print(f"  WRITTEN — {applied} replacement(s) applied to post {post_id}.")


def inspect_post(slug, needle):
    """Diagnostic only: print raw context around every occurrence of `needle`
    so we can see exactly what's stored (markup, quote style, whitespace)
    before trusting any replacement logic. Makes no writes."""
    post_id = get_post_id(slug)
    post = api_get(f"/cross_reference/{post_id}", "?context=edit")
    raw = post["content"]["raw"]
    print(f"\n=== RAW INSPECT: {slug} (post id {post_id}), {len(raw)} chars ===")
    start = 0
    hit = 0
    while True:
        idx = raw.find(needle, start)
        if idx == -1:
            break
        hit += 1
        lo, hi = max(0, idx - 60), min(len(raw), idx + 60)
        print(f"  [{hit}] ...{raw[lo:hi]!r}...")
        start = idx + len(needle)
    if hit == 0:
        print(f"  No occurrences of {needle!r} found at all.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Actually write changes. Default is dry-run.")
    parser.add_argument("--inspect", metavar="SLUG", help="Diagnostic: print raw context around --needle for one slug, no writes.")
    parser.add_argument("--needle", default="200", help="Text to search for with --inspect (default: '200').")
    parser.add_argument("--dump", metavar="SLUG", help="Diagnostic: write full raw content.raw for one slug to a local .json file, no writes to WordPress.")
    parser.add_argument("--dump-all", dest="dump_all", action="store_true", help="Diagnostic: write full raw content.raw for all 7 slugs to local .json files, no writes to WordPress.")
    args = parser.parse_args()

    if args.inspect:
        inspect_post(args.inspect, args.needle)
        sys.exit(0)

    if args.dump:
        post_id = get_post_id(args.dump)
        post = api_get(f"/cross_reference/{post_id}", "?context=edit")
        out_path = Path(__file__).resolve().parent / f"_debug_{args.dump}.json"
        out_path.write_text(post["content"]["raw"])
        print(f"Wrote raw content.raw for {args.dump} (post {post_id}) to {out_path}")
        sys.exit(0)

    if getattr(args, "dump_all", False):
        for slug in EDITS:
            post_id = get_post_id(slug)
            post = api_get(f"/cross_reference/{post_id}", "?context=edit")
            out_path = Path(__file__).resolve().parent / f"_debug_{slug}.json"
            out_path.write_text(post["content"]["raw"])
            print(f"Wrote raw content.raw for {slug} (post {post_id}) to {out_path}")
        sys.exit(0)

    print(f"Source for every edit below:\n  {SOURCE_NOTE}\n")
    if not args.apply:
        print("Running in DRY RUN mode — no writes will be made. Pass --apply to write for real.\n")

    for slug, edits in EDITS.items():
        try:
            patch_post(slug, edits, dry_run=not args.apply)
        except Exception as e:
            print(f"\n=== {slug} FAILED: {e} ===")
