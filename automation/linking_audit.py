#!/usr/bin/env python3
"""
Internal Linking Automation — audit-only inventory + gap detection.

First implementation increment against docs/AIFORPROS-INTERNAL-LINKING-
AUTOMATION-SPEC.md (policy_version 1.1.0). This is Operating Mode 1
(audit-only, spec §1): READ-ONLY. It makes no writes to WordPress and
contains no LLM scoring logic — spec §17 explicitly defers that until
this inventory/eligibility layer is stable and reviewed.

What this does:
  1. Fetches the Phase 1 editable source type (`cross_reference`, spec §2)
     via the WP REST API.
  2. Builds the relationship model from GOV-LINK-012's vocabulary:
     primary_tool, profession, sibling_tool, sibling_cross_reference —
     derived from each post's linked_tool / linked_profession meta, not
     from slug-parsing.
  3. For every (source, sibling) pair, runs the eligibility checks from
     spec §10 against the sibling's cross_reference page (resolves 200,
     correct canonical per the REST API's own `link` field, publish
     status) — LIVE, via real HTTP requests, not cached assumptions.
  4. Detects existing contextual coverage using the same inline-styled-
     link detection built for analyze_contextual_coverage.py during the
     August 2026 audit (a link carrying the body-mention style, anywhere
     in the page's decoded content — not just the same paragraph).
  5. For every (source, sibling) pair with NO contextual coverage and an
     ELIGIBLE target, emits a proposal record per spec §4's schema, in a
     new entry state: `gap_detected`. This state is not yet in the spec's
     state-transition table (spec §6b) because it didn't exist until this
     script needed it — see the note at the bottom of this file and the
     corresponding spec update this script's first run should prompt.
  6. Ineligible or unresolvable targets are recorded as
     `blocked_eligibility_unknown` per spec §10's exact definition (a
     hold state, not a permanent rejection) rather than silently skipped.

Nothing here decides whether a gap SHOULD be filled — that is governance
§8's genuine-contextual-mention test, applied by a human or (eventually)
the not-yet-built scoring step in spec §17. This script only tells you,
with confidence, WHERE the gaps are and WHICH targets are safe to
consider.

Run:
    python3 automation/linking_audit.py > linking_audit_report.txt
    (also writes automation/linking_audit_output.json — the structured
    proposal-record output, one record per (source, sibling) gap or
    blocked-eligibility case)
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import requests  # noqa: E402
from wp_creds import AUTH, WP_URL  # noqa: E402

POLICY_VERSION = "1.3.0"
STYLE_MARKER = "2563eb"  # inline body-link style used for contextual mentions

# The literal, fixed lead-in text of the cross-navigation sentence at the end
# of every cross_reference page's LAST content_sections entry (the "Where
# [Tool] Falls Short" section) — e.g. "Comparing your options? Also see...".
# Confirmed against a real page dump (automation/_debug_claude-creatives.json,
# 2026-08-05): this sentence is NOT a separate top-level JSON field. It is the
# trailing paragraph inside the SAME content_sections[-1].section_body string
# that also holds the limitations-grid / limit-card HTML — i.e. structurally
# adjacent to, not separate from, the genuine contextual mentions that live in
# that same closing section. This is exactly why a new contextual link placed
# in that section reads as clustered even though it's a different HTML zone
# in principle.
FOOTER_SENTENCE_MARKER = "Comparing your options?"

A_TAG_RE = re.compile(
    r'<a\s+href=\\?"([^"\\]+)\\?"(?:\s+style=\\?"([^"\\]*)\\?")?[^>]*>(.*?)<\/a>',
    re.DOTALL,
)


# ---------------------------------------------------------------------------
# Inventory
# ---------------------------------------------------------------------------

def fetch_all(post_type, fields="id,slug,link,status,content,meta"):
    posts = []
    page = 1
    while True:
        resp = requests.get(
            f"{WP_URL}/wp/v2/{post_type}",
            params={"context": "edit", "_fields": fields, "per_page": 100, "page": page},
            auth=AUTH,
        )
        if resp.status_code == 400:
            break
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        posts.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return posts


def build_tool_and_profession_maps(tool_reviews, profession_hubs):
    """id -> display name, for linked_tool / linked_profession meta lookups."""
    tool_names = {p["id"]: p["slug"] for p in tool_reviews}
    profession_names = {p["id"]: p["slug"] for p in profession_hubs}
    return tool_names, profession_names


# ---------------------------------------------------------------------------
# Contextual coverage detection (spec §4, reusing the August 2026 audit logic)
# ---------------------------------------------------------------------------

def flatten_strings(value, out):
    if isinstance(value, str):
        if "<a " in value or "<a\\ " in value:
            out.append(value)
    elif isinstance(value, list):
        for v in value:
            flatten_strings(v, out)
    elif isinstance(value, dict):
        for v in value.values():
            flatten_strings(v, out)


def tool_slug_from_href(href):
    parts = [p for p in href.strip("/").split("/") if p]
    return parts[0] if parts else None


def get_contextual_tool_slugs(decoded_content):
    """Tool slugs that have at least one INLINE STYLED (body-mention) link
    anywhere in this page's decoded content — the spec §4 definition of
    existing contextual coverage."""
    strings = []
    flatten_strings(decoded_content, strings)
    contextual = set()
    for s in strings:
        for m in A_TAG_RE.finditer(s):
            href, style, _text = m.group(1), m.group(2), m.group(3)
            if style and STYLE_MARKER in style:
                slug = tool_slug_from_href(href)
                if slug:
                    contextual.add(slug)
    return contextual


def classify_existing_links(decoded_content, target_slug):
    """Rich's 2026-08-05 redundancy-classification rules, applied at the
    structural level rather than as a simple link-count blocker: scan every
    existing link to target_slug on this page and bucket it by zone/purpose
    so the scoring/apply steps can tell a table link, a footer cross-nav
    sentence, and a genuine contextual mention apart — because "a table link
    plus one useful contextual link is normal" and total count alone proves
    nothing either way (governance §14, per Rich's explicit correction).

    Returns (counts, closing_section_titles):
      counts — {"table": n, "footer_sentence": n, "contextual": n} occurrences
        of a link to target_slug in each zone.
      closing_section_titles — set of content_sections[*].section_title
        values whose section_body contains the footer_sentence link to this
        target. In practice this is always the single last content_sections
        entry (the "Where [Tool] Falls Short" section) — a NEW contextual
        link proposed for one of these titles is "tightly clustered in the
        same closing section" with any existing table/footer link, per rule 3.
    """
    counts = {"table": 0, "footer_sentence": 0, "contextual": 0}
    closing_section_titles = set()

    table_html = decoded_content.get("comparison_notes") or ""
    for m in A_TAG_RE.finditer(table_html):
        if tool_slug_from_href(m.group(1)) == target_slug:
            counts["table"] += 1

    for sec in decoded_content.get("content_sections") or []:
        body = sec.get("section_body") or ""
        title = sec.get("section_title")
        if FOOTER_SENTENCE_MARKER in body:
            idx = body.index(FOOTER_SENTENCE_MARKER)
            before, after = body[:idx], body[idx:]
        else:
            before, after = body, ""

        for m in A_TAG_RE.finditer(after):
            if tool_slug_from_href(m.group(1)) == target_slug:
                counts["footer_sentence"] += 1
                closing_section_titles.add(title)

        for m in A_TAG_RE.finditer(before):
            href, style = m.group(1), m.group(2)
            if tool_slug_from_href(href) == target_slug and style and STYLE_MARKER in style:
                counts["contextual"] += 1

    return counts, closing_section_titles


def find_section_containing(decoded_content, snippet):
    """Which content_sections[*].section_title contains this exact snippet,
    if any. Used to independently verify a model's self-reported placement
    rather than trust it, matching the fail-closed pattern used everywhere
    else in this pipeline (e.g. linking_apply.py's live re-checks)."""
    if not snippet:
        return None
    for sec in decoded_content.get("content_sections") or []:
        if snippet in (sec.get("section_body") or ""):
            return sec.get("section_title")
    return None


# ---------------------------------------------------------------------------
# Eligibility (spec §10)
# ---------------------------------------------------------------------------

def check_eligibility(candidate):
    """Returns (eligible: bool, status: str, detail: str).
    status is one of: 'eligible', 'blocked_eligibility_unknown', 'ineligible'.
    """
    if candidate["status"] != "publish":
        return False, "ineligible", f"post status is '{candidate['status']}', not publish"

    url = candidate["link"]
    try:
        resp = requests.get(url, allow_redirects=True, timeout=15)
    except requests.RequestException as e:
        return False, "blocked_eligibility_unknown", f"request failed: {e}"

    if resp.status_code == 200:
        # Canonical check: did we land where the REST API says this post lives?
        final_url = resp.url.rstrip("/")
        expected_url = url.rstrip("/")
        if final_url != expected_url:
            return False, "blocked_eligibility_unknown", (
                f"resolved to a different URL than the REST-API canonical link "
                f"(expected {expected_url}, got {final_url}) — needs an authoritative "
                f"redirect mapping per governance §15 before this is auto-eligible"
            )
        return True, "eligible", "200, canonical match, publish status confirmed"

    if resp.status_code in (403, 429):
        return False, "blocked_eligibility_unknown", f"transient status {resp.status_code}, retry on a later run"

    return False, "blocked_eligibility_unknown", f"unexpected status {resp.status_code}"


# ---------------------------------------------------------------------------
# Relationship model + gap detection (GOV-LINK-012, spec §2)
# ---------------------------------------------------------------------------

def main():
    print("Fetching inventory (cross_reference is the only Phase 1 editable source type)...")
    cross_refs = fetch_all("cross_reference")
    tool_reviews = fetch_all("tool_review", fields="id,slug,link,status")
    profession_hubs = fetch_all("profession_hub", fields="id,slug,link,status")
    print(f"  {len(cross_refs)} cross_reference, {len(tool_reviews)} tool_review, "
          f"{len(profession_hubs)} profession_hub posts fetched.\n")

    tool_names, profession_names = build_tool_and_profession_maps(tool_reviews, profession_hubs)

    # Decode content + build per-profession sibling groups.
    decoded = {}
    for post in cross_refs:
        try:
            decoded[post["id"]] = json.loads(post["content"]["raw"])
        except json.JSONDecodeError as e:
            print(f"  SKIP {post['slug']} (post {post['id']}) — invalid JSON: {e}")

    by_profession = {}  # profession_id -> list of cross_ref posts
    for post in cross_refs:
        if post["id"] not in decoded:
            continue
        prof_id = post.get("meta", {}).get("linked_profession")
        if not prof_id:
            continue
        by_profession.setdefault(prof_id, []).append(post)

    records = []
    now = datetime.now(timezone.utc).isoformat()

    for prof_id, group in by_profession.items():
        profession_slug = profession_names.get(prof_id, f"profession-{prof_id}")

        for source in group:
            source_id = source["id"]
            source_tool_id = source.get("meta", {}).get("linked_tool")
            primary_tool_slug = tool_names.get(source_tool_id, "unknown")
            source_content = decoded[source_id]
            existing_contextual = get_contextual_tool_slugs(source_content)

            siblings = [p for p in group if p["id"] != source_id]

            for sibling in siblings:
                sibling_tool_id = sibling.get("meta", {}).get("linked_tool")
                sibling_tool_slug = tool_names.get(sibling_tool_id, "unknown")

                record_id = f"rec_{source_id}_{sibling['id']}"
                base_record = {
                    "record_id": record_id,
                    "source_post_id": source_id,
                    "source_url": source["link"],
                    "canonical_target_id": sibling["id"],
                    "target_url": sibling["link"],
                    "primary_tool": primary_tool_slug,
                    "sibling_tool": sibling_tool_slug,
                    "profession": profession_slug,
                    "policy_version": POLICY_VERSION,
                    "created_at": now,
                    # Fields requiring the not-yet-built scoring step (spec §17)
                    # are intentionally absent here, not stubbed with fake values:
                    # edit_type, existing_text, proposed_text, anchor_text,
                    # rationale, useful_without_link, evidence_ids, rules_applied,
                    # confidence, placement_locator.
                }

                eligible, elig_status, elig_detail = check_eligibility({
                    "status": sibling["status"], "link": sibling["link"],
                })
                base_record["eligibility"] = {"status": elig_status, "detail": elig_detail}

                if not eligible:
                    base_record["state"] = "blocked_eligibility_unknown"
                    records.append(base_record)
                    continue

                if sibling_tool_slug in existing_contextual:
                    # Genuine contextual coverage already exists for this pair —
                    # not a gap. Not emitted as a record at all; this script only
                    # reports gaps and blocked-eligibility cases, per its stated
                    # purpose above.
                    continue

                base_record["state"] = "gap_detected"
                records.append(base_record)

    gap_count = sum(1 for r in records if r["state"] == "gap_detected")
    blocked_count = sum(1 for r in records if r["state"] == "blocked_eligibility_unknown")

    out_path = Path(__file__).resolve().parent / "linking_audit_output.json"
    with open(out_path, "w") as f:
        json.dump(records, f, indent=2)

    print(f"gap_detected records: {gap_count}")
    print(f"blocked_eligibility_unknown records: {blocked_count}")
    print(f"Total records written to {out_path}: {len(records)}\n")

    print("Sample (first 5 gap_detected records):")
    shown = 0
    for r in records:
        if r["state"] == "gap_detected" and shown < 5:
            print(f"  {r['record_id']}: {r['source_url']} -> sibling '{r['sibling_tool']}' "
                  f"({r['target_url']})")
            shown += 1

    if blocked_count:
        print("\nblocked_eligibility_unknown records (need attention before scoring can proceed):")
        for r in records:
            if r["state"] == "blocked_eligibility_unknown":
                print(f"  {r['record_id']}: {r['target_url']} — {r['eligibility']['detail']}")


if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------
# NOTE for docs/AIFORPROS-INTERNAL-LINKING-AUTOMATION-SPEC.md:
# This script's output enters the state machine at a state not yet listed in
# spec §6b's transition table: `gap_detected`. It is the entry point produced
# by this audit-only layer, BEFORE the not-yet-built scoring step (spec §17)
# evaluates it into opportunity_proposed / needs_evidence /
# needs_editorial_review / no_opportunity_proposed. The spec should be updated
# to add: `gap_detected -> opportunity_proposed | needs_evidence |
# needs_editorial_review | no_opportunity_proposed | stale` alongside the
# existing states, once this is reviewed.
# ---------------------------------------------------------------------------
