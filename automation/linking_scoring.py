#!/usr/bin/env python3
"""
Internal Linking Automation — scoring step (spec §17).

Second implementation increment against docs/AIFORPROS-INTERNAL-LINKING-
AUTOMATION-SPEC.md (policy_version 1.2.0+). This is Operating Mode 2
(Suggestion, spec §1): it reads gap_detected records emitted by
linking_audit.py, uses the Claude API to evaluate each one against
governance §8's genuine-contextual-mention test, and writes proposal
records. IT MAKES NO WRITES TO WORDPRESS. A record produced here still
requires human review (spec §7) before anything is ever applied by a
future, not-yet-built supervised-apply step (spec §8's fail-closed write
protocol).

Evidence grounding (governance §1, `SITE_PUBLISHED_CONTENT`): this script
does not fetch new external vendor documentation — that duplicates System
1's job and is out of scope. Instead, the model is required to ground any
proposed claim in the SIBLING page's own already-published, already-
reviewed content (its consistency_blocks / feature sections), quoting the
exact supporting text. If it can't find genuine support there, the
correct outcome is needs_evidence or no_opportunity_proposed, not a
fabricated claim.

Order of preference (spec §12), enforced in the prompt:
  1. Link existing text — an already-genuine mention of the sibling tool
     exists in the source page's prose but isn't a link yet.
  2. Expand an existing sentence to make the comparison explicit.
  3. Propose a new sentence, only if neither of the above applies.

Hard gates applied AFTER the model responds (not left to the model's own
judgment, per spec §6's routing rules):
  - useful_without_link must be true, or the record is forced to
    needs_editorial_review regardless of what else the model said.
  - A claim with no quoted supporting_text from the sibling's own content
    is forced to needs_evidence.
  - no_opportunity_proposed is never auto-finalized to
    no_opportunity_confirmed here — that transition requires a human
    actor (spec §6b) and is out of scope for this script entirely.

Environment: WORDPRESS_USERNAME, WORDPRESS_APP_PASSWORD (via wp_creds.py),
ANTHROPIC_API_KEY.

Usage:
    python3 automation/linking_scoring.py                  # cap=15 (spec §14 default)
    python3 automation/linking_scoring.py --cap 5           # smaller batch
    python3 automation/linking_scoring.py --record rec_373_365   # score one specific pair
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import requests  # noqa: E402
from wp_creds import AUTH, WP_URL  # noqa: E402

import anthropic  # noqa: E402

from linking_audit import (  # noqa: E402
    classify_existing_links,
    find_section_containing,
    FOOTER_SENTENCE_MARKER,
)

POLICY_VERSION = "1.3.0"
MODEL = "claude-sonnet-5"
MAX_TOKENS = 8192

AUDIT_INPUT_PATH = Path(__file__).resolve().parent / "linking_audit_output.json"
PROPOSALS_OUTPUT_PATH = Path(__file__).resolve().parent / "linking_proposals_output.json"

# Site-wide contextual-link style marker (matches STYLE_MARKER "2563eb" used
# throughout the audit/detection scripts to distinguish genuine contextual
# prose links from structural table/footer links). The model is instructed
# to include this in every <a> tag it proposes, but instruction-following on
# an exact literal string is not reliable enough to trust alone — this is
# enforced programmatically as a defense-in-depth step, not left solely to
# the model's compliance. Only injects the style when an <a href="..."> tag
# has no style attribute at all; a tag that already carries one (correct or
# not) is left untouched rather than risk double-attributing it.
LINK_STYLE_ATTR = 'style="color:#2563eb;text-decoration:none;font-weight:500;"'
BARE_A_TAG_RE = re.compile(r'<a\s+href="([^"]+)"\s*>')


def enforce_link_style(text):
    if not text:
        return text
    return BARE_A_TAG_RE.sub(lambda m: f'<a href="{m.group(1)}" {LINK_STYLE_ATTR}>', text)


# ---------------------------------------------------------------------------
# Page text rendering — reuses the exact pattern proven correct in
# system3_monthly.py (flatten every text field with its JSON location
# label, rather than passing raw escaped JSON to the model — the earlier
# bug this fixed was a mismatch between what the model was shown and what
# apply-time string matching searches against).
# ---------------------------------------------------------------------------

def flatten_text_fields(value, path=""):
    if isinstance(value, str):
        if value.strip():
            yield path, value
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from flatten_text_fields(v, f"{path}[{i}]")
    elif isinstance(value, dict):
        for k, v in value.items():
            yield from flatten_text_fields(v, f"{path}.{k}" if path else k)


def render_page_text(data, allowed_top_level_keys=None):
    lines = []
    for path, value in flatten_text_fields(data):
        top_key = path.split(".")[0].split("[")[0]
        if allowed_top_level_keys and top_key not in allowed_top_level_keys:
            continue
        lines.append(f"[{path}]: {value}")
    return "\n".join(lines)


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


SCORING_SYSTEM_PROMPT = """You are evaluating exactly ONE candidate internal link on a review website (aitoolsforpros.com), \
governed by a strict editorial policy. You will be given:
1. The SOURCE page's full text (every field, labeled with its location in the page's JSON structure).
2. The SIBLING page's full text (same format) — this is the page the candidate link would point to.
3. The specific tool names and profession involved.

Your job: decide whether a genuine, natural, useful contextual link from the source page to the sibling page \
belongs somewhere in the source page's existing prose — specifically within its `content_sections[N].section_body` \
fields only. You may NOT propose edits to consistency_blocks, quick_facts, comparison_notes, faq, sources, or any \
other field — only content_sections[N].section_body.

THE TEST (apply this exactly, it is not optional):
A genuine contextual mention must:
- Address a specific reader need, limitation, workflow, or tradeoff.
- Explain WHY the sibling tool is relevant at that specific point.
- Fit naturally into the surrounding paragraph, not as a bolted-on aside.
- Be grounded in something the SIBLING page's own text ALREADY says about itself (quote the exact supporting \
sentence or phrase from the sibling's text — do not invent a capability, limitation, or comparison that isn't \
already stated on the sibling's own page).
- Remain useful even if the hyperlink were removed. If a sentence would only exist to contain an anchor, it \
FAILS this test.

ORDER OF PREFERENCE (try each before moving to the next):
1. LINK EXISTING TEXT — the sibling tool is already mentioned by name somewhere in the source page's \
content_sections prose, but that mention isn't currently a link. If so, this is edit_type "link_existing_text" \
and existing_text should be that exact already-present sentence (unchanged).
2. EXPAND AN EXISTING SENTENCE — a related sentence exists that could be extended with a specific, evidenced \
comparison point. edit_type "modify_sentence".
3. PROPOSE A NEW SENTENCE — only if neither of the above is possible, and only if a genuine comparison point \
exists per the test above. edit_type "insert_sentence".

PLACEMENT — you will be told below which links to the sibling tool ALREADY exist on this page and in which zone \
(a comparison-table row, the closing "Comparing your options?" cross-navigation sentence, or an earlier genuine \
contextual mention). A table link plus one useful contextual link is a normal, healthy pattern — do NOT treat an \
existing table or footer-sentence link as a reason to withhold a genuinely useful contextual mention elsewhere. \
But if you are choosing WHERE to place a new contextual mention and more than one content_sections entry would \
work, prefer an earlier feature/workflow section over the page's LAST content_sections entry (the "Where [Tool] \
Falls Short" / limitations section) — that closing section already carries the footer cross-navigation sentence, \
so a second link to the same target placed there reads as clustered even when each link is individually fine. \
This is a placement preference, not a hard rule: if the only genuinely useful, evidenced comparison point belongs \
in that closing section, say so honestly rather than forcing a weaker sentence into an earlier section.

If you cannot satisfy the test above with real, evidenced content, the correct answer is "no_opportunity_proposed" \
or "needs_evidence" — NOT a manufactured sentence. Do not treat this as a failure; it is a normal, expected, valid \
outcome for many pairs. Do not add links merely to fill a quota.

Respond with ONLY a single JSON object — no markdown fences, no text before or after. This exact shape:
{
  "verdict": "opportunity_proposed" | "needs_evidence" | "needs_editorial_review" | "no_opportunity_proposed",
  "edit_type": "link_existing_text" | "change_anchor" | "modify_sentence" | "insert_sentence" | null,
  "content_zone": "limitation_card" | "feature_section" | null,
  "section_title_hint": "the section_title of the content_sections entry you are proposing to touch, or null",
  "existing_text": "the exact current sentence/span being linked or modified, verbatim from the source page's text above, or null",
  "proposed_text": "the full replacement sentence/span including the <a href=\\"...\\"> tag, or null",
  "anchor_text": "the visible link text being proposed, or null",
  "rationale": "one or two sentences: the specific reader need this addresses and why the sibling is relevant here",
  "useful_without_link": true or false — apply the test literally: if you removed the <a> tag and kept the sentence, would it still be a true, useful, standalone statement?,
  "evidence_supporting_text": "the EXACT sentence or phrase quoted verbatim from the SIBLING page's text above that supports this claim, or null if none exists",
  "evidence_source_field": "the [bracketed field path] from the sibling page's text where evidence_supporting_text came from, or null",
  "confidence": {
    "relevance_confidence": "high" | "medium" | "low",
    "evidence_confidence": "high" | "medium" | "low",
    "placement_confidence": "high" | "medium" | "low",
    "editorial_naturalness_confidence": "high" | "medium" | "low"
  },
  "notes": "anything a human reviewer should know"
}

Remember: aitoolsforpros.com's content style avoids em dashes in body text, and every claim about a tool's \
capabilities must trace back to something the sibling page's own text already says — you are not authorized to \
introduce new facts about either tool.
"""


def describe_existing_links(source_data, sibling_slug):
    """Human-readable summary of classify_existing_links()'s output, for the
    model prompt — e.g. 'table: 1, footer_sentence: 1, contextual: 0'."""
    counts, closing_titles = classify_existing_links(source_data, sibling_slug)
    parts = [f"{zone}: {n}" for zone, n in counts.items()]
    line = ", ".join(parts)
    if closing_titles:
        line += f" (closing section: {', '.join(sorted(closing_titles))})"
    return line, counts, closing_titles


def score_pair(client, source_data, source_slug, sibling_data, sibling_slug, primary_tool, sibling_tool, profession):
    source_text = render_page_text(source_data, allowed_top_level_keys={"content_sections"})
    sibling_text = render_page_text(sibling_data)  # full sibling text — evidence can come from any field
    existing_links_summary, _counts, _closing_titles = describe_existing_links(source_data, sibling_slug)

    user_prompt = f"""SOURCE page (primary tool: {primary_tool}, profession: {profession}), editable prose only:
{source_text}

---

Existing links from the SOURCE page to the SIBLING tool ({sibling_tool}), by zone: {existing_links_summary}

---

SIBLING page (tool: {sibling_tool}, same profession — candidate link target), full text:
{sibling_text}

---

Evaluate the candidate link from the SOURCE page to the SIBLING page ({sibling_tool}'s page for {profession})."""

    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SCORING_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )
    text_blocks = [block.text for block in response.content if getattr(block, "type", None) == "text"]
    if not text_blocks:
        return None, f"No text block in response (block types: {[getattr(b, 'type', None) for b in response.content]})"
    raw_text = text_blocks[0].strip()
    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError as e:
        return None, f"JSON parse failure: {e}. Raw response (first 500 chars): {raw_text[:500]}"

    parsed["proposed_text"] = enforce_link_style(parsed.get("proposed_text"))
    return parsed, None


def apply_hard_gates(model_output):
    """Post-process the model's self-reported verdict against the hard gates
    spec §6 requires — these override the model's own claim, they are not
    suggestions to it."""
    verdict = model_output.get("verdict")

    if verdict == "opportunity_proposed":
        if not model_output.get("useful_without_link"):
            model_output["verdict"] = "needs_editorial_review"
            model_output["notes"] = (model_output.get("notes", "") +
                " [HARD GATE OVERRIDE: model proposed an opportunity but marked "
                "useful_without_link=false — routed to needs_editorial_review, not trusted as opportunity_proposed.]")
        elif not model_output.get("evidence_supporting_text"):
            model_output["verdict"] = "needs_evidence"
            model_output["notes"] = (model_output.get("notes", "") +
                " [HARD GATE OVERRIDE: no evidence_supporting_text quoted from the sibling page — "
                "routed to needs_evidence regardless of model's stated verdict.]")

    return model_output


def apply_placement_gates(model_output, source_data, sibling_slug):
    """Rich's 2026-08-05 zone-aware redundancy rules, applied programmatically
    and independently of the model's own self-report — matching the same
    fail-closed philosophy as apply_hard_gates() and linking_apply.py's live
    re-checks (never trust self-report where it can be verified directly).

    Implements the three rules that are checkable mechanically. The other
    four (allow table+contextual coexistence; judge usefulness, not absence
    or presence of other links; don't treat count alone as proof either way)
    are deliberately NOT encoded as blockers here — they're judgment calls
    left to the model's own reasoning per the system prompt's PLACEMENT
    section, exactly because Rich's correction was that blanket count-based
    blocking is the wrong instrument for those:

      Rule 1 (defense-in-depth) — a genuine contextual link to this sibling
        already exists somewhere on the page. linking_audit.py's gap
        detection already excludes these pairs upstream, so this should be
        unreachable in practice; checked again here anyway in case source
        content changed between the audit run and this scoring run.
      Rule 2 — never link the same target twice in one paragraph: if the
        model's own existing_text span already contains a link to the same
        sibling, adding another would double-link that span.
      Rule 3 — flag tight clustering in the same closing section: the page's
        last content_sections entry (verified structurally, not from the
        model's self-reported section_title_hint) already carries the
        footer "Comparing your options?" cross-navigation sentence to this
        same sibling, or a comparison-table row to it, AND the model wants
        to place its new contextual mention in that very same section.
    """
    if model_output.get("verdict") != "opportunity_proposed":
        return model_output

    existing_text = model_output.get("existing_text") or ""
    counts, closing_titles = classify_existing_links(source_data, sibling_slug)

    if counts["contextual"] > 0:
        model_output["verdict"] = "needs_editorial_review"
        model_output["notes"] = (model_output.get("notes", "") +
            " [PLACEMENT GATE — rule 1: a genuine contextual link to this sibling already exists "
            "elsewhere on the page. Not trusting the model's verdict; this pair should not have reached "
            "scoring as a gap at all, so source content may have changed since the last audit run.]")
        return model_output

    if f"/{sibling_slug}/" in existing_text:
        model_output["verdict"] = "needs_editorial_review"
        model_output["notes"] = (model_output.get("notes", "") +
            " [PLACEMENT GATE — rule 2: existing_text already contains a link to this same sibling — "
            "adding another would link the same target twice within one paragraph.]")
        return model_output

    actual_section = find_section_containing(source_data, existing_text)
    if actual_section and actual_section in closing_titles and (counts["table"] or counts["footer_sentence"]):
        model_output["verdict"] = "needs_editorial_review"
        model_output["notes"] = (model_output.get("notes", "") +
            f" [PLACEMENT GATE — rule 3: proposed placement is in '{actual_section}', the page's closing "
            f"section, which already carries a table link ({counts['table']}) and/or the footer "
            f"cross-navigation sentence ({counts['footer_sentence']}) to this same sibling — this would be "
            "tightly clustered. Held for a human look at placement, not auto-rejected outright.]")
        return model_output

    return model_output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cap", type=int, default=15, help="max pairs to score this run (spec §14 default: 10-20)")
    parser.add_argument("--record", type=str, default=None, help="score only this specific record_id")
    args = parser.parse_args()

    if not AUDIT_INPUT_PATH.exists():
        print(f"ERROR: {AUDIT_INPUT_PATH} not found. Run linking_audit.py first.")
        return

    # The fresh audit output is always the source of truth for which (source, sibling)
    # pairs are CURRENTLY live gaps (linking_audit.py re-derives this from the actual
    # live pages every run). Scoring results accumulate ACROSS runs on top of that,
    # rather than each run wiping out everything scored by a previous run — a record
    # already scored to a terminal state (opportunity_proposed / needs_evidence /
    # needs_editorial_review / no_opportunity_proposed) is carried forward untouched
    # as long as its pair is still present in the fresh audit; if a record_id no longer
    # appears in the fresh audit at all, the underlying gap is gone (most likely because
    # linking_apply.py already applied it, so it's no longer a gap) and it is correctly
    # dropped here rather than lingering forever.
    with open(AUDIT_INPUT_PATH) as f:
        fresh_audit = json.load(f)
    fresh_by_id = {r["record_id"]: r for r in fresh_audit}

    previously_scored = {}
    if PROPOSALS_OUTPUT_PATH.exists():
        with open(PROPOSALS_OUTPUT_PATH) as f:
            for r in json.load(f):
                if r.get("state") != "gap_detected":
                    previously_scored[r["record_id"]] = r

    carried_over = {
        rid: rec for rid, rec in previously_scored.items() if rid in fresh_by_id
    }
    dropped_stale = [rid for rid in previously_scored if rid not in fresh_by_id]
    if dropped_stale:
        print(f"{len(dropped_stale)} previously-scored record(s) no longer appear in the fresh audit "
              f"(gap likely already closed) — dropping: {', '.join(dropped_stale)}\n")

    candidates = [
        r for rid, r in fresh_by_id.items()
        if r["state"] == "gap_detected" and rid not in carried_over
    ]
    if args.record:
        candidates = [r for r in candidates if r["record_id"] == args.record]
    candidates = candidates[: args.cap]

    print(f"Scoring {len(candidates)} gap_detected record(s) (cap={args.cap})...\n")

    client = anthropic.Anthropic()
    page_cache = {}
    results = []

    for i, record in enumerate(candidates, 1):
        print(f"[{i}/{len(candidates)}] {record['record_id']}: "
              f"{record['primary_tool']} -> {record['sibling_tool']} ({record['profession']})")

        try:
            if record["source_post_id"] not in page_cache:
                page_cache[record["source_post_id"]] = fetch_page(record["source_post_id"])
            if record["canonical_target_id"] not in page_cache:
                page_cache[record["canonical_target_id"]] = fetch_page(record["canonical_target_id"])

            source_post, source_data = page_cache[record["source_post_id"]]
            sibling_post, sibling_data = page_cache[record["canonical_target_id"]]

            model_output, error = score_pair(
                client, source_data, source_post["slug"], sibling_data, sibling_post["slug"],
                record["primary_tool"], record["sibling_tool"], record["profession"],
            )

            if error:
                print(f"    HELD — {error}")
                record["state"] = "needs_editorial_review"
                record["notes"] = f"Scoring step failed: {error}"
                results.append(record)
                continue

            model_output = apply_hard_gates(model_output)
            model_output = apply_placement_gates(model_output, source_data, sibling_post["slug"])

            record.update({
                "state": model_output["verdict"],
                "edit_type": model_output.get("edit_type"),
                "content_zone": model_output.get("content_zone"),
                "section_title_hint": model_output.get("section_title_hint"),
                "existing_text": model_output.get("existing_text"),
                "proposed_text": model_output.get("proposed_text"),
                "anchor_text": model_output.get("anchor_text"),
                "rationale": model_output.get("rationale"),
                "useful_without_link": model_output.get("useful_without_link"),
                "evidence": {
                    "supporting_text": model_output.get("evidence_supporting_text"),
                    "source_field": model_output.get("evidence_source_field"),
                    "source_type": "SITE_PUBLISHED_CONTENT",
                    "source_url": sibling_post["link"],
                } if model_output.get("evidence_supporting_text") else None,
                "confidence": model_output.get("confidence"),
                "notes": model_output.get("notes"),
                "policy_version": POLICY_VERSION,
                "scored_at": datetime.now(timezone.utc).isoformat(),
                "reviewed_by": None,
            })
            print(f"    -> {record['state']}")
            results.append(record)

        except Exception as e:
            print(f"    ERROR (item-level, continuing) — {e}")
            record["state"] = "needs_editorial_review"
            record["notes"] = f"Scoring step raised an exception: {e}"
            results.append(record)

    # Rebuild the full output from three sources: records scored just now, records
    # carried over unchanged from a previous run (still a live pair, already had a
    # terminal verdict), and everything else currently in the fresh audit (unscored
    # gap_detected records still waiting for a future run's cap, plus
    # blocked_eligibility_unknown records, which are never scored). This makes the
    # proposals file a full reconstruction from the live audit each run, not an
    # ever-growing diff — anything the fresh audit no longer reports simply isn't
    # carried forward (see the dropped_stale note above).
    scored_ids = {r["record_id"] for r in results}
    remaining_fresh = [
        r for rid, r in fresh_by_id.items()
        if rid not in scored_ids and rid not in carried_over
    ]
    merged = list(carried_over.values()) + results + remaining_fresh

    with open(PROPOSALS_OUTPUT_PATH, "w") as f:
        json.dump(merged, f, indent=2)

    from collections import Counter
    counts = Counter(r["state"] for r in results)
    print(f"\nDone. Scored {len(results)} pair(s) this run:")
    for state, count in counts.items():
        print(f"  {state}: {count}")
    print(f"\n{len(carried_over)} previously-scored record(s) carried forward unchanged.")
    print(f"Full output written to {PROPOSALS_OUTPUT_PATH} ({len(merged)} total records).")
    print("No writes to WordPress happen in this script — linking_apply.py applies opportunity_proposed "
          "records under its own hard-gated, fail-closed write protocol.")


if __name__ == "__main__":
    main()
