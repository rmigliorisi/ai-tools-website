#!/usr/bin/env python3
"""
Monthly Cross-Reference & Profession Hub Editorial Review — System 3 automation.

Graduated from suggest-only (human approves every change in a live conversation)
to capped autonomous apply, per Rich's decision on 2026-07-25 after the first
manual cycle (Claude's 200K -> 1M-token context window, 7 pages) went cleanly
end to end and the tooling around it (self-tests, JSON-decode-based text
replacement, post-write verification) proved itself. See
docs/AIFORPROS-AUTOMATED-CONTENT.md, System 3 section, for the full spec this
script implements, including WHY the cap/backlog design below exists (Google's
"scaled content abuse" policy risk — see that doc's "Purpose" section).

WHAT THIS DOES, END TO END, EACH RUN:
  1. Research: one Claude API call per tool (web_search restricted to that
     vendor's own domains — same TOOLS/domains list as System 1) asking what
     professionally-relevant capability changed in roughly the last month.
  2. For each tool with a real finding, gather every cross_reference page for
     that tool (slug prefix match, e.g. "claude-legal") and every profession_hub
     page that mentions the tool by name.
  3. For each (tool, page) pair, one more Claude API call: given the finding
     AND the page's full decoded JSON as text, ask for every literal
     old_text -> new_text edit that connects the finding to something the page
     already claims — a full-text sweep done BY THE MODEL because it can read
     the whole page and reason about relevance, not a keyword grep. old_text
     must be an exact substring of the page text; this script re-verifies that
     locally before trusting it (see IDENTIFY_SYSTEM_PROMPT and apply_candidate).
  4. Guardrail QA: source required, must resolve to the vendor's own domain,
     confidence must be "vendor_official_current" (the same strict bar System 1
     uses for pricing/compliance — verdict-level page content deserves at least
     that, arguably more, now that nothing here gets a human second look before
     publish) — anything softer is held, not applied.
  5. Cap + backlog: at most CAP pages (default 10) get written in a single run.
     Older queued pages (from a prior run that exceeded the cap) are applied
     before new ones — first-in-first-out — so a busy month doesn't strand a
     page indefinitely. Overflow gets written to automation/system3_backlog.json
     and picked up automatically next run; nothing is dropped, it just queues.
  6. Apply via the WP REST API using the exact pattern proven safe on the July
     2026 manual cycle: decode content.raw as JSON, walk it recursively doing
     string replacement (never raw-text substring matching — that's what
     caused a real bug: a quote-containing sentence silently failed to match
     because raw JSON text escapes " as \\" and the search pattern didn't),
     re-encode, PUT, then re-fetch and diff to confirm the write actually took.
  7. Log + notify: every applied/held/queued edit gets logged via the same
     digest endpoint System 1 uses (POST /wp-json/aifp/v1/update-digest) so
     Rich sees a summary by email every run, even though nothing is gated on
     his approval anymore. Automation, not invisibility.

ARCHITECTURE NOTE — why this runs on GitHub Actions, not as a Cowork scheduled
task (the Cowork task "system3-cross-reference-editorial-review" that produced
suggest-only reports is being retired in favor of this): Cowork's sandbox
cannot make authenticated writes to WordPress — outbound HTTPS to third-party
hosts is blocked at the proxy, confirmed by testing during System 1's build.
The old Cowork task worked fine when the only output was a text report (no
write needed), but autonomous apply needs real network access, which only a
GitHub Actions runner has. See .github/workflows/system3-monthly.yml.

Environment (GitHub Actions secrets in production; local .env for testing):
    WORDPRESS_USERNAME, WORDPRESS_APP_PASSWORD, WORDPRESS_SITE_URL (optional)
    ANTHROPIC_API_KEY
(Same secrets System 1 already uses — nothing new to add.)

Usage:
    python3 automation/system3_monthly.py             # live run: writes + digest
    python3 automation/system3_monthly.py --dry-run   # research + QA gate only, no writes, no email
    python3 automation/system3_monthly.py --cap 5     # override the per-run page cap (default 10)
"""

import argparse
import json
import re
import ssl
import sys
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from weekly_tool_update import TOOLS  # noqa: E402 — single source of truth for tool -> vendor domains

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from wp_creds import HEADERS, BASE, WP_URL  # noqa: E402

import anthropic  # noqa: E402

try:
    import certifi
    CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    CTX = ssl.create_default_context()

MODEL = "claude-sonnet-5"
BACKLOG_PATH = Path(__file__).resolve().parent / "system3_backlog.json"
DEFAULT_CAP = 10

RESEARCH_SYSTEM_PROMPT = """You are researching what has genuinely, substantively changed about one AI \
tool's capabilities in roughly the last month, for a review site aimed at working professionals \
(lawyers, physicians, engineers, real estate agents, accountants, insurance agents, creatives). You \
only have search access to the vendor's own official domains — never third-party summaries, \
aggregators, or your own memory.

You are looking for capability changes that would change how a professional should think about using \
this tool for real work — a materially larger context window, a new or substantially improved \
document/image analysis capability, a new agentic/tool-use capability, a compliance/security status \
change, a meaningfully different pricing tier structure. A minor version bump or UI tweak with no \
workflow-relevant capability change is NOT a finding — return an empty list rather than manufacturing \
significance.

Respond with ONLY a JSON array — no explanation before it, no markdown code fences, no text after it. \
Your entire final message must start with `[` and end with `]`. Empty array `[]` if nothing genuinely \
changed. Each item:
{
  "capability": "short name, e.g. 'context window' or 'document analysis'",
  "description": "one or two sentences stating the OLD state and the NEW state concretely, e.g. \
'Context window increased from 200K tokens to 1M tokens on Pro/Team/Enterprise plans.' A vague \
'improved X' is not acceptable here — name the actual before/after.",
  "source_url": "the exact vendor page URL you confirmed this on",
  "confidence": "vendor_official_current" or "third_party" or "uncertain"
}

Only "vendor_official_current" findings will ever be auto-applied anywhere; the other tiers exist so \
you can still report something worth a human's attention without overstating your certainty.
"""

IDENTIFY_SYSTEM_PROMPT = """You are doing a full-text sweep of one page on an AI-tool review site to find \
every place a specific, already-confirmed capability change should update the page's existing text.

You will be given: (1) a capability finding — a specific, sourced, confirmed change to one AI tool's \
capabilities, and (2) the ENTIRE current text content of one page that reviews or discusses that tool — \
every text field, each labeled with its location (e.g. "[faq[2].answer]: ..."). Your job is to find \
every literal place in the page text where the OLD state (from before this finding) is stated or \
implied as still true, and propose an exact replacement for each one.

This must be a genuine full-text sweep, not a skim of the obvious sections (Bottom Line, comparison \
table). Check FAQ answers, insight/"what most reviews miss" sections, feature descriptions, quick \
facts, everywhere — a real production bug on this exact site was caused by missing occurrences that \
were sitting in FAQ answers, not the prominent sections. Read the whole page text you're given.

A page only qualifies at all if the finding plausibly and specifically affects something THIS page \
already claims — not just "the tool got better" in the abstract. If this page doesn't mention anything \
the finding would change, return an empty edits list. Don't force a connection that isn't really there.

Respond with ONLY a JSON object — no explanation before it, no markdown code fences, no text after it. \
Your entire final message must start with `{` and end with `}`. This shape:
{
  "edits": [
    {
      "old_text": "the EXACT literal substring from the page content given to you, verbatim, that \
should change — copy it character-for-character, do not paraphrase or summarize it",
      "new_text": "the exact replacement text, preserving the surrounding sentence's grammar and tone",
      "rationale": "one sentence: why this specific spot needs to change given the finding"
    }
  ]
}
old_text must be copy-pasted exactly from the page content provided — if you cannot quote it exactly, \
do not include that edit. Return an empty edits array if nothing on this page needs to change.
"""


# ---------------------------------------------------------------------------
# REST helpers — same pattern as weekly_tool_update.py / the July 2026 patch script
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# The tested, safe text-replacement core (carried over verbatim in spirit from
# automation/system3_2026-07_claude_context_window.py, where this exact logic
# was hardened after a real bug: matching against raw JSON text fails silently
# whenever the target sentence contains a literal quotation mark, since the
# raw text escapes it as \" and a plain-quote search pattern never matches
# that. Operating on the DECODED Python object sidesteps this entirely.
# ---------------------------------------------------------------------------

def _replace_in_value(value, old, new, counter):
    if isinstance(value, str):
        count = value.count(old)
        if count:
            counter[0] += count
            return value.replace(old, new)
        return value
    if isinstance(value, list):
        return [_replace_in_value(v, old, new, counter) for v in value]
    if isinstance(value, dict):
        return {k: _replace_in_value(v, old, new, counter) for k, v in value.items()}
    return value


def _count_in_value(value, old, counter):
    """Non-mutating twin of _replace_in_value — counts occurrences of `old` across the
    same nested structure without changing anything. Used to verify a candidate edit's
    old_text is genuinely present in the DECODED page data (the same representation the
    real replace will later search) before queuing it — see render_page_text() below
    for why checking against raw JSON text instead was the actual bug."""
    if isinstance(value, str):
        counter[0] += value.count(old)
    elif isinstance(value, list):
        for v in value:
            _count_in_value(v, old, counter)
    elif isinstance(value, dict):
        for v in value.values():
            _count_in_value(v, old, counter)


def flatten_text_fields(value, path=""):
    """Yield (path, string) for every non-empty string leaf in a decoded JSON structure,
    using the actual decoded value — no JSON string-escaping — so what the model reads
    exactly matches what _replace_in_value / _count_in_value will later search against.

    This exists because raw JSON text escapes a literal quote character as \\" — if the
    model were shown that raw text and asked to copy old_text verbatim, any quote-
    containing sentence would come back with backslashes baked in, which then never
    matches the plain-quote string sitting in the decoded Python object. That mismatch
    was the exact bug the July 2026 manual cycle hit and this script's docstring claims
    to have fixed — it was fixed in _replace_in_value's traversal, but the model was
    still being shown raw escaped text upstream of that. Flattening to plain text here
    closes that gap end to end."""
    if isinstance(value, str):
        if value.strip():
            yield path, value
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from flatten_text_fields(v, f"{path}[{i}]")
    elif isinstance(value, dict):
        for k, v in value.items():
            yield from flatten_text_fields(v, f"{path}.{k}" if path else k)


def render_page_text(data):
    """Plain-text rendering of every text field on a page, each tagged with its location
    in the JSON structure, for feeding to identify_candidates instead of raw JSON text."""
    return "\n".join(f"[{path}]: {value}" for path, value in flatten_text_fields(data))


def run_selftests():
    """Fail-closed sanity check on the replacement logic, run automatically before
    any network call. If any assertion fails, abort — do not let untested logic
    touch a live site that now has no human review step before publish."""
    tests_run = 0

    def check(label, actual, expected):
        nonlocal tests_run
        tests_run += 1
        if actual != expected:
            raise AssertionError(f"Self-test FAILED [{label}]: expected {expected!r}, got {actual!r}")

    c = [0]
    check("plain replace", _replace_in_value("The 200K window", "200K", "1M", c), "The 1M window")
    check("plain replace count", c[0], 1)

    c = [0]
    sentence = 'Most reviews lead with "Claude has a 200K context window" as if it is a spec.'
    result = _replace_in_value(sentence, '"Claude has a 200K context window"', '"Claude has a 1M-token context window"', c)
    check("quoted-substring replace", result, 'Most reviews lead with "Claude has a 1M-token context window" as if it is a spec.')
    check("quoted-substring count", c[0], 1)

    c = [0]
    nested = {"a": ["x 200K y", {"b": "z 200K w"}], "c": "no match here"}
    result = _replace_in_value(nested, "200K", "1M", c)
    check("nested structure replace", result, {"a": ["x 1M y", {"b": "z 1M w"}], "c": "no match here"})
    check("nested structure count", c[0], 2)

    c = [0]
    check("no-match unchanged", _replace_in_value("nothing relevant here", "200K", "1M", c), "nothing relevant here")
    check("no-match count", c[0], 0)

    sample = {"key": "value with → arrow and \"quotes\" and it's an apostrophe"}
    round_tripped = json.loads(json.dumps(sample, ensure_ascii=False))
    check("json round-trip", round_tripped, sample)

    # Regression test for the escaped-quote mismatch: identify_candidates must be shown
    # DECODED text (plain quotes) so old_text it copies verbatim matches what
    # _count_in_value / _replace_in_value will actually search for later. If this ever
    # regresses to feeding the model raw JSON text again, this test catches it.
    sample_page = {
        "faq": [{
            "question": "Does it support long docs?",
            "answer": 'Most reviews lead with "Claude has a 200K context window" as if it is a spec.',
        }],
    }
    rendered = render_page_text(sample_page)
    check("rendered page text uses plain quotes, not escaped",
          '"Claude has a 200K context window"' in rendered, True)
    c = [0]
    _count_in_value(sample_page, '"Claude has a 200K context window"', c)
    check("count_in_value finds the plain-quote old_text in decoded data", c[0], 1)
    # And confirm the escaped form (what raw JSON text would have shown instead) does
    # NOT match the decoded data — proving these two representations really do differ.
    c2 = [0]
    _count_in_value(sample_page, '\\"Claude has a 200K context window\\"', c2)
    check("escaped-quote form does not match decoded data (proves the bug this fixes)", c2[0], 0)

    print(f"Self-tests passed ({tests_run} checks).")


# ---------------------------------------------------------------------------
# Research + candidate identification
# ---------------------------------------------------------------------------

def research_tool_capabilities(client, tool_key, info):
    """One bounded call: what changed for this tool, professionally-relevant,
    in roughly the last month. Returns (findings_list, raw_text). On any API
    failure, findings_list is None and raw_text starts with RESEARCH_FAILED:"""
    try:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=RESEARCH_SYSTEM_PROMPT,
            tools=[{
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": 5,
                "allowed_domains": info["domains"],
            }],
            messages=[{
                "role": "user",
                "content": f"What has genuinely changed about {info['name']}'s capabilities in roughly "
                            f"the last month that would matter to a working professional deciding "
                            f"whether/how to use it?",
            }],
        )
    except anthropic.APIError as e:
        return None, f"RESEARCH_FAILED: {type(e).__name__}: {e}"
    except Exception as e:
        return None, f"RESEARCH_FAILED: unexpected {type(e).__name__}: {e}"

    text_blocks = [b.text for b in resp.content if getattr(b, "type", None) == "text"]
    full_text = "\n".join(text_blocks)
    match = re.search(r"\[.*\]", full_text, re.DOTALL)
    if not match:
        return None, full_text
    try:
        return json.loads(match.group(0)), full_text
    except json.JSONDecodeError:
        return None, full_text


def identify_candidates(client, finding, page_text):
    """One call: given a confirmed finding + a page's full text, find every
    exact old_text -> new_text edit that connects them. Returns (edits_list, raw_text)."""
    try:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=IDENTIFY_SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": (
                    f"CONFIRMED FINDING:\n{json.dumps(finding, indent=2)}\n\n"
                    f"PAGE CONTENT (every text field, labeled with its location):\n{page_text}"
                ),
            }],
        )
    except anthropic.APIError as e:
        return None, f"RESEARCH_FAILED: {type(e).__name__}: {e}"
    except Exception as e:
        return None, f"RESEARCH_FAILED: unexpected {type(e).__name__}: {e}"

    text_blocks = [b.text for b in resp.content if getattr(b, "type", None) == "text"]
    full_text = "\n".join(text_blocks)
    match = re.search(r"\{.*\}", full_text, re.DOTALL)
    if not match:
        return None, full_text
    try:
        parsed = json.loads(match.group(0))
        return parsed.get("edits", []), full_text
    except json.JSONDecodeError:
        return None, full_text


def source_is_vendor_domain(source_url, allowed_domains):
    try:
        netloc = urllib.parse.urlparse(source_url).netloc.lower()
    except Exception:
        return False
    netloc = netloc[4:] if netloc.startswith("www.") else netloc
    return any(netloc == d or netloc.endswith(f".{d}") for d in allowed_domains)


# ---------------------------------------------------------------------------
# Backlog (cap rollover)
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


# ---------------------------------------------------------------------------
# Apply
# ---------------------------------------------------------------------------

def apply_page_edits(post_type, slug, post_id, edits, dry_run, changes_log):
    """edits: list of {old_text, new_text, source_url, rationale}. Verifies
    each old_text is still present verbatim before touching anything (a page
    may have changed since the edit was queued in the backlog), applies via
    the decoded-JSON replace, and verifies the write by re-fetching."""
    post = api_get(f"/{post_type}/{post_id}?context=edit")
    raw = post["content"]["raw"]
    print(f"\n=== {slug} ({post_type}, post id {post_id}) ===")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        # A page can drift between identify-time and apply-time (another edit, a manual
        # fix, or — as happened once already on this site — a corrupting resave through
        # the WP Admin editor). Hold and move on rather than crashing the whole run and
        # silently skipping every remaining queued page after this one.
        print(f"  SKIP — existing content JSON failed to parse ({e}) — needs manual review, not touching this page")
        changes_log.append({
            "tool": slug, "field": f"{page_url_for(post_type, slug)} (all)",
            "old_value": "", "new_value": "", "source": "", "status": "held",
            "reason": "existing content JSON failed to parse at apply time — needs manual review",
        })
        return

    applied = 0
    for edit in edits:
        counter = [0]
        data = _replace_in_value(data, edit["old_text"], edit["new_text"], counter)
        count = counter[0]
        status = "applied" if count else "held"
        reason = f"replaced {count}x" if count else "old_text not found on page (may have changed since queued)"
        print(f"  {status.upper()} ({count}x): {edit['old_text'][:70]}")
        changes_log.append({
            "tool": slug, "field": f"{page_url_for(post_type, slug)}",
            "old_value": edit["old_text"][:200], "new_value": edit["new_text"][:200],
            "source": edit.get("source_url", ""), "status": status if not dry_run else "dry_run", "reason": reason,
        })
        applied += count

    if applied == 0:
        print("  Nothing to apply on this page (all edits stale or already applied).")
        return

    new_raw = json.dumps(data, ensure_ascii=False)
    if dry_run:
        print(f"  [DRY RUN] {applied} replacement(s) staged, no write performed.")
        return

    api_put(f"/{post_type}/{post_id}", {"content": new_raw})
    verify = api_get(f"/{post_type}/{post_id}?context=edit")
    if verify["content"]["raw"] == new_raw:
        print(f"  WRITTEN + VERIFIED — {applied} replacement(s) confirmed by re-fetch.")
    else:
        print("  WRITTEN BUT UNVERIFIED — re-fetched content.raw does not match what was sent. Check manually.")


def page_url_for(post_type, slug):
    if post_type == "cross_reference":
        # slug convention is "{tool}-{profession}" — best-effort URL guess for the digest;
        # not load-bearing, purely a human-readable pointer in the log/email.
        return f"aitoolsforpros.com/{slug.replace('-', '/', 1)}/"
    return f"aitoolsforpros.com/{slug}/"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Research + QA gate only — no writes, no digest email")
    parser.add_argument("--cap", type=int, default=DEFAULT_CAP, help=f"Max pages written per run (default {DEFAULT_CAP})")
    args = parser.parse_args()

    run_selftests()  # fail closed: abort before any network call if the core logic is broken

    client = anthropic.Anthropic()
    changes_log = []

    cross_refs = api_get("/cross_reference?per_page=100&context=edit&_fields=id,slug,content")
    profession_hubs = api_get("/profession_hub?per_page=100&context=edit&_fields=id,slug,content")
    print(f"Fetched {len(cross_refs)} cross_reference pages, {len(profession_hubs)} profession_hub pages.")

    new_candidates = []  # each: {post_type, slug, post_id, edits: [...]}

    for tool_key, info in TOOLS.items():
        print(f"\n--- Researching {info['name']} ---")
        findings, raw_text = research_tool_capabilities(client, tool_key, info)
        if raw_text.startswith("RESEARCH_FAILED:"):
            print(f"  RESEARCH CALL FAILED: {raw_text}")
            continue
        if findings is None:
            print(f"  No usable findings JSON. Raw (truncated): {raw_text[:200]}")
            continue
        if not findings:
            print("  No workflow-relevant capability changes found this month.")
            continue

        for finding in findings:
            print(f"  FINDING: {finding.get('capability')} — {finding.get('description', '')[:100]}")
            if finding.get("confidence") != "vendor_official_current":
                print(f"    -> held (confidence '{finding.get('confidence')}' below auto-apply bar), skipping page sweep")
                changes_log.append({
                    "tool": info["name"], "field": f"(finding: {finding.get('capability')})",
                    "old_value": "", "new_value": finding.get("description", ""),
                    "source": finding.get("source_url", ""), "status": "held",
                    "reason": f"confidence '{finding.get('confidence')}' below the vendor_official_current bar required for auto-apply",
                })
                continue
            if not source_is_vendor_domain(finding.get("source_url", ""), info["domains"]):
                print("    -> held (source URL doesn't resolve to an allowed vendor domain)")
                changes_log.append({
                    "tool": info["name"], "field": f"(finding: {finding.get('capability')})",
                    "old_value": "", "new_value": finding.get("description", ""),
                    "source": finding.get("source_url", ""), "status": "held",
                    "reason": "source URL doesn't resolve to this tool's allowed vendor domain(s)",
                })
                continue

            relevant_cross_refs = [p for p in cross_refs if p["slug"].startswith(f"{tool_key}-")]
            relevant_hubs = [p for p in profession_hubs if info["name"].lower() in p["content"]["raw"].lower()]

            for post_type, pages in (("cross_reference", relevant_cross_refs), ("profession_hub", relevant_hubs)):
                for page in pages:
                    try:
                        page_data = json.loads(page["content"]["raw"])
                    except json.JSONDecodeError as e:
                        print(f"    {page['slug']}: SKIP — existing content JSON failed to parse ({e})")
                        changes_log.append({
                            "tool": info["name"], "field": f"{page_url_for(post_type, page['slug'])} (all)",
                            "old_value": "", "new_value": "", "source": "", "status": "held",
                            "reason": "existing content JSON failed to parse — needs manual review",
                        })
                        continue

                    # Model is shown DECODED, flattened plain text (not raw JSON) so any
                    # old_text it copies verbatim uses plain quotes, matching what
                    # _count_in_value / _replace_in_value will search for against the
                    # decoded page data below and at apply time. See render_page_text().
                    edits, raw_text = identify_candidates(client, finding, render_page_text(page_data))
                    if raw_text.startswith("RESEARCH_FAILED:"):
                        print(f"    {page['slug']}: IDENTIFY CALL FAILED: {raw_text}")
                        changes_log.append({
                            "tool": info["name"], "field": f"{page_url_for(post_type, page['slug'])} (identify call)",
                            "old_value": "", "new_value": "", "source": "", "status": "held", "reason": raw_text,
                        })
                        continue
                    if edits is None:
                        print(f"    {page['slug']}: no usable edits JSON from identify call. Raw (truncated): {raw_text[:200]}")
                        changes_log.append({
                            "tool": info["name"], "field": f"{page_url_for(post_type, page['slug'])} (identify call)",
                            "old_value": "", "new_value": "", "source": "", "status": "held",
                            "reason": "identify call returned unparseable output — held for review",
                        })
                        continue
                    if not edits:
                        continue

                    # Defensive re-verification: never trust the model's old_text claim without
                    # checking it against the DECODED page data ourselves — the same
                    # representation the real replace will search at apply time — before
                    # queuing a write.
                    verified_edits = []
                    for e in edits:
                        old = e.get("old_text")
                        if not old:
                            continue
                        counter = [0]
                        _count_in_value(page_data, old, counter)
                        if counter[0]:
                            verified_edits.append({**e, "source_url": finding.get("source_url", "")})
                        else:
                            print(f"    {page['slug']}: DROPPED an edit — old_text not verbatim in page (hallucination guard)")

                    if verified_edits:
                        print(f"    {page['slug']}: {len(verified_edits)} candidate edit(s) found")
                        new_candidates.append({
                            "post_type": post_type, "slug": page["slug"], "post_id": page["id"],
                            "edits": verified_edits, "found_date": date.today().isoformat(),
                        })

    backlog = load_backlog()
    queue = backlog + new_candidates
    to_apply, remaining = queue[:args.cap], queue[args.cap:]

    print(f"\n{'=' * 60}")
    print(f"QUEUE: {len(backlog)} carried over from backlog + {len(new_candidates)} new this run "
          f"= {len(queue)} total. Cap this run: {args.cap}. Applying {len(to_apply)}, queuing {len(remaining)}.")
    print(f"{'=' * 60}")

    for candidate in to_apply:
        apply_page_edits(candidate["post_type"], candidate["slug"], candidate["post_id"],
                          candidate["edits"], args.dry_run, changes_log)

    if not args.dry_run:
        save_backlog(remaining)
        if remaining:
            print(f"\n{len(remaining)} page(s) queued to {BACKLOG_PATH.name} for next run.")
    elif remaining:
        print(f"\n[DRY RUN] {len(remaining)} page(s) would be queued to backlog (not written this run, since dry-run doesn't touch the backlog file either).")

    print(f"\n{'=' * 60}\nSUMMARY — {len(changes_log)} change log entries\n{'=' * 60}")
    for c in changes_log:
        print(f"  [{c['status']}] {c['tool']} — {c['field']}: \"{c['old_value'][:60]}\" -> \"{c['new_value'][:60]}\" ({c['reason']})")

    if args.dry_run:
        print("\n[dry run] No writes made, no digest email sent, backlog file untouched.")
        return

    if changes_log:
        digest_result = post_digest(changes_log)
        print(f"\nDigest sent: {digest_result}")
    else:
        print("\nNo changes this run — no digest sent.")


if __name__ == "__main__":
    main()
