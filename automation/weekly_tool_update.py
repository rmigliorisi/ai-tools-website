#!/usr/bin/env python3
"""
Weekly Tool Page Update — System 1 automation.

For each of the 10 tool_review pages: research current pricing/features/HIPAA
status via the Claude API's web_search tool (restricted to that vendor's own
official domains), diff the findings against the live page's decoded JSON
content, apply only what passes the guardrail QA gate (see
docs/AIFORPROS-AUTOMATED-CONTENT.md "Guardrail / QA gate"), write changes back
via the WP REST API, and log + email a digest of everything applied, held, or
flagged.

This runs unattended via .github/workflows/weekly-tool-update.yml on GitHub
Actions — NOT as a Cowork scheduled task. Cowork's sandbox cannot make
authenticated writes to WordPress (outbound HTTPS to third-party hosts is
blocked at the proxy), so the actual write step has to live somewhere with
real network access. GitHub Actions runners have that; Cowork does the
one-off/interactive work instead.

Environment (GitHub Actions secrets in production; local .env for testing):
    WORDPRESS_USERNAME, WORDPRESS_APP_PASSWORD, WORDPRESS_SITE_URL (optional)
    ANTHROPIC_API_KEY

Usage:
    python3 automation/weekly_tool_update.py            # live run: writes + digest
    python3 automation/weekly_tool_update.py --dry-run  # research + QA gate only, no writes, no email
"""

import argparse
import json
import re
import ssl
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from wp_creds import HEADERS, BASE, WP_URL  # noqa: E402

import anthropic  # noqa: E402

CTX = ssl.create_default_context()
MODEL = "claude-sonnet-5"

# tool_slug (matches the WP post slug / tool_slug field) -> display name + the
# ONLY domains web_search is allowed to pull from for that tool. This is what
# makes the "vendor's own official page" confidence tier meaningful — Claude
# physically cannot cite a result outside these domains.
TOOLS = {
    "chatgpt":    {"name": "ChatGPT",           "domains": ["openai.com", "help.openai.com", "chatgpt.com"]},
    "claude":     {"name": "Claude",            "domains": ["anthropic.com", "claude.com", "support.claude.com"]},
    "cursor":     {"name": "Cursor",            "domains": ["cursor.com"]},
    "gemini":     {"name": "Gemini",            "domains": ["gemini.google.com", "one.google.com", "support.google.com", "ai.google.dev"]},
    "grammarly":  {"name": "Grammarly",         "domains": ["grammarly.com"]},
    "copilot":    {"name": "Microsoft Copilot", "domains": ["microsoft.com", "copilot.microsoft.com", "support.microsoft.com"]},
    "midjourney": {"name": "Midjourney",        "domains": ["midjourney.com", "docs.midjourney.com"]},
    "notion-ai":  {"name": "Notion AI",         "domains": ["notion.com", "notion.so"]},
    "otter":      {"name": "Otter.ai",          "domains": ["otter.ai"]},
    "perplexity": {"name": "Perplexity",        "domains": ["perplexity.ai"]},
}

RESEARCH_SYSTEM_PROMPT = """You are a careful research assistant checking one AI tool's current, official \
pricing, plan names, feature set, and HIPAA/compliance status. You must ONLY use information from the \
tool's own official website (the domains you've been given access to) — never third-party summaries, \
aggregators, or your own memory. If you cannot confirm a fact on the vendor's own current page, say so \
rather than guessing.

Return your findings as a single JSON object, and nothing else after it, with this shape:
{
  "made_by": {"value": "...", "source_url": "...", "confidence": "..."} or null,
  "pricing_fact": {"value": "...", "source_url": "...", "confidence": "..."} or null,
  "hipaa_fact": {"value": "...", "source_url": "...", "confidence": "..."} or null,
  "pricing_tiers": [{"tier_name": "...", "tier_price": "...", "tier_features": "...", "source_url": "...", "confidence": "..."}] or null,
  "feature_updates": [{"feature_name": "...", "feature_description": "...", "source_url": "...", "confidence": "..."}] or null,
  "notes": "anything uncertain or worth a human's attention, as plain text"
}

"confidence" must be exactly one of:
- "vendor_official_current" — directly confirmed on the vendor's own current page during this search
- "third_party" — a credible secondary source reported it, not confirmed on the vendor's own page
- "uncertain" — you are not confident this is current or correct

Only include a key if you found something that looks NEW or CHANGED versus what a review page written a \
few months ago would already say. If nothing looks changed for a key, use null. Never invent a value.
"""


def api_get(path):
    req = urllib.request.Request(f"{BASE}{path}", headers=HEADERS)
    with urllib.request.urlopen(req, context=CTX) as r:
        return json.loads(r.read())


def api_put(path, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(f"{BASE}{path}", data=data, headers=HEADERS, method="POST")
    req.add_header("X-HTTP-Method-Override", "PUT")
    with urllib.request.urlopen(req, context=CTX) as r:
        return json.loads(r.read())


def post_digest(changes):
    data = json.dumps({"changes": changes}).encode()
    req = urllib.request.Request(f"{WP_URL}/aifp/v1/update-digest", data=data, headers=HEADERS, method="POST")
    with urllib.request.urlopen(req, context=CTX) as r:
        return json.loads(r.read())


def research_tool(client, info):
    """One bounded research call per tool. web_search is a server tool — Claude
    can issue multiple searches within this single API call (up to max_uses),
    so we don't need to manage a multi-turn loop ourselves.

    Returns (findings, text). On any API-level failure (out of credits, rate
    limited, auth problem, network issue), findings is None and text starts
    with "RESEARCH_FAILED:" so callers can tell "the call itself failed" apart
    from "the call succeeded but didn't return usable JSON" — those need
    different handling and different messages to whoever reads the log.
    """
    try:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=RESEARCH_SYSTEM_PROMPT,
            tools=[{
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": 5,
                "allowed_domains": info["domains"],
            }],
            messages=[{
                "role": "user",
                "content": (
                    f"Check {info['name']}'s current official pricing, plan names, key features, and "
                    f"HIPAA/compliance status. Report only what you can directly confirm on {info['name']}'s "
                    f"own official site right now."
                ),
            }],
        )
    except anthropic.APIError as e:
        # Covers billing/credit errors, rate limits, auth failures, etc. — anything
        # the Anthropic SDK raises as a structured API error.
        return None, f"RESEARCH_FAILED: {type(e).__name__}: {e}"
    except Exception as e:
        # Anything else (network blip, unexpected SDK behavior) — fail the same
        # clean way rather than letting an uncaught exception crash the whole run.
        return None, f"RESEARCH_FAILED: unexpected {type(e).__name__}: {e}"

    text_blocks = [b.text for b in resp.content if getattr(b, "type", None) == "text"]
    full_text = "\n".join(text_blocks)
    match = re.search(r"\{.*\}", full_text, re.DOTALL)
    if not match:
        return None, full_text
    try:
        return json.loads(match.group(0)), full_text
    except json.JSONDecodeError:
        return None, full_text


def _extract_price(s):
    m = re.search(r"\$?\s*([\d,]+(?:\.\d+)?)", s or "")
    return float(m.group(1).replace(",", "")) if m else None


def numeric_sanity_ok(old_value, new_value):
    """Reject scraping-error-looking price swings: reads as $0, or a >5x jump."""
    old_p, new_p = _extract_price(old_value), _extract_price(new_value)
    if new_p is not None and new_p == 0:
        return False
    if old_p and new_p and old_p > 0 and new_p > 0:
        ratio = new_p / old_p if new_p > old_p else old_p / new_p
        if ratio > 5:
            return False
    return True


def evaluate_field(old_value, finding, strict):
    """
    Apply the guardrail QA gate (docs/AIFORPROS-AUTOMATED-CONTENT.md) to one
    candidate field change. Returns (decision, reason):
      "skip"    — no real change, nothing to log
      "applied" — passes every check, safe to write
      "flagged" — applied, but noted in the digest (soft warning)
      "held"    — not applied, logged for human review
    """
    if finding is None:
        return "skip", "no finding"

    value = finding.get("value")
    source_url = finding.get("source_url") or ""
    confidence = finding.get("confidence", "uncertain")

    if value == old_value:
        return "skip", "unchanged"
    if not source_url:
        return "held", "no traceable source URL"
    if not numeric_sanity_ok(old_value, value):
        return "held", "numeric sanity check failed (looks like a scraping error, not a real change)"
    if strict and confidence != "vendor_official_current":
        return "held", f"confidence '{confidence}' below the required bar for pricing/compliance fields"
    if confidence == "uncertain":
        return "held", "confidence too low to auto-apply"
    if confidence == "third_party":
        return "flagged", "confirmed via a credible third-party source, not the vendor's own page"
    return "applied", "confirmed on the vendor's current official page"


def process_tool(slug, info, post, findings, dry_run, changes_log):
    raw = post.get("content", {}).get("raw", "")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  ERROR: existing content JSON failed to parse ({e}) — held for manual review")
        changes_log.append({
            "tool": info["name"], "field": "(all)", "old_value": "", "new_value": "",
            "source": "", "status": "held", "reason": "existing content JSON failed to parse",
        })
        return False

    dirty = False
    qf = data.setdefault("quick_facts", {})

    for key, strict in (("pricing_fact", True), ("hipaa_fact", True), ("made_by", False)):
        finding = findings.get(key)
        decision, reason = evaluate_field(qf.get(key, ""), finding, strict)
        if decision == "skip":
            continue
        print(f"  quick_facts.{key}: {decision} — {reason}")
        old_value = qf.get(key, "")
        if decision in ("applied", "flagged"):
            qf[key] = finding["value"]
            dirty = True
        changes_log.append({
            "tool": info["name"], "field": f"quick_facts.{key}",
            "old_value": old_value, "new_value": finding.get("value", ""),
            "source": finding.get("source_url", ""), "status": decision, "reason": reason,
        })

    for tier_finding in (findings.get("pricing_tiers") or []):
        tname = tier_finding.get("tier_name", "")
        existing = next((t for t in data.get("pricing_tiers", []) if t.get("tier_name") == tname), None)
        if not existing:
            changes_log.append({
                "tool": info["name"], "field": f"pricing_tiers.{tname}",
                "old_value": "(no matching tier)", "new_value": tier_finding.get("tier_price", ""),
                "source": tier_finding.get("source_url", ""), "status": "held",
                "reason": "tier name doesn't match an existing tier — adding/removing tiers is editorial",
            })
            continue
        decision, reason = evaluate_field(existing.get("tier_price", ""), {
            "value": tier_finding.get("tier_price"),
            "source_url": tier_finding.get("source_url"),
            "confidence": tier_finding.get("confidence"),
        }, strict=True)
        if decision == "skip":
            continue
        print(f"  pricing_tiers.{tname}: {decision} — {reason}")
        old_value = existing.get("tier_price", "")
        if decision in ("applied", "flagged"):
            existing["tier_price"] = tier_finding["tier_price"]
            if tier_finding.get("tier_features"):
                existing["tier_features"] = tier_finding["tier_features"]
            dirty = True
        changes_log.append({
            "tool": info["name"], "field": f"pricing_tiers.{tname}.tier_price",
            "old_value": old_value, "new_value": tier_finding.get("tier_price", ""),
            "source": tier_finding.get("source_url", ""), "status": decision, "reason": reason,
        })

    existing_features = data.get("features", [])
    if len(existing_features) != 7:
        print(f"  WARNING: features array has {len(existing_features)} items (expected 7) — skipping feature updates")
    else:
        for feat_finding in (findings.get("feature_updates") or []):
            fname = feat_finding.get("feature_name", "")
            existing = next((f for f in existing_features if f.get("feature_name") == fname), None)
            if not existing:
                changes_log.append({
                    "tool": info["name"], "field": f"features.{fname}",
                    "old_value": "(no matching feature)", "new_value": feat_finding.get("feature_description", ""),
                    "source": feat_finding.get("source_url", ""), "status": "held",
                    "reason": "feature name doesn't match any of the existing 7 — adding/removing is editorial",
                })
                continue
            decision, reason = evaluate_field(existing.get("feature_description", ""), {
                "value": feat_finding.get("feature_description"),
                "source_url": feat_finding.get("source_url"),
                "confidence": feat_finding.get("confidence"),
            }, strict=False)
            if decision == "skip":
                continue
            print(f"  features.{fname}: {decision} — {reason}")
            old_value = existing.get("feature_description", "")
            if decision in ("applied", "flagged"):
                existing["feature_description"] = feat_finding["feature_description"]
                dirty = True
            changes_log.append({
                "tool": info["name"], "field": f"features.{fname}.feature_description",
                "old_value": old_value, "new_value": feat_finding.get("feature_description", ""),
                "source": feat_finding.get("source_url", ""), "status": decision, "reason": reason,
            })

    if dirty and not dry_run:
        result = api_put(f"/tool_review/{post['id']}", {"content": json.dumps(data)})
        if "id" in result:
            print(f"  WROTE update to post {post['id']}")
        else:
            print(f"  FAILED to write: {result}")
    elif dirty:
        print("  [dry run] would have written changes")

    return dirty


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                         help="Research + QA gate only — no writes, no digest email")
    args = parser.parse_args()

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
    changes_log = []

    posts = api_get("/tool_review?per_page=100&context=edit&_fields=id,slug,content")
    posts_by_slug = {p["slug"]: p for p in posts}

    for slug, info in TOOLS.items():
        post = posts_by_slug.get(slug)
        print(f"\n=== {info['name']} ({slug}) ===")
        if not post:
            print("  SKIP: no matching tool_review post found")
            continue

        findings, raw_text = research_tool(client, info)

        if raw_text.startswith("RESEARCH_FAILED:"):
            # The API call itself failed (billing/credits, rate limit, auth, network) —
            # distinct from a call that succeeded but returned unparseable text. Log it
            # plainly, record it in the digest as held-for-review, and move on to the
            # next tool rather than letting this crash the whole run.
            print(f"  RESEARCH CALL FAILED: {raw_text}")
            changes_log.append({
                "tool": info["name"], "field": "(research call)",
                "old_value": "", "new_value": "",
                "source": "", "status": "held",
                "reason": raw_text,
            })
            continue

        if findings is None:
            print(f"  No usable findings returned. Raw model text (truncated): {raw_text[:200]}")
            continue

        process_tool(slug, info, post, findings, args.dry_run, changes_log)

    print(f"\n{'=' * 60}\nSUMMARY — {len(changes_log)} change entries\n{'=' * 60}")
    for c in changes_log:
        print(f"  [{c['status']}] {c['tool']} — {c['field']}: \"{c['old_value']}\" -> \"{c['new_value']}\" ({c['reason']})")

    if args.dry_run:
        print("\n[dry run] No writes made, no digest email sent.")
        return

    if changes_log:
        digest_result = post_digest(changes_log)
        print(f"\nDigest sent: {digest_result}")
    else:
        print("\nNo changes this run — no digest sent.")


if __name__ == "__main__":
    main()
