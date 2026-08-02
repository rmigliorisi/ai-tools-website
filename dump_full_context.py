"""
Read-only follow-up to scan_stripped_links.py. That scan's 60-character
context windows cut off mid-word in several places, which isn't safe to
guess from when building exact-match replacements. This dumps a much wider
window (300 chars) around each confirmed real hit (false positives like
"OtterPilot", "GrammarlyGO", and intentional "Claude/ChatGPT" slash
notation are excluded — those aren't the stripped-link bug).

Does not modify anything.

Run:
    python3 dump_full_context.py > full_context.txt
"""

import json

import requests
from wp_creds import AUTH, WP_URL

# post_id, slug, and a short stable anchor (no ambiguous truncation) drawn
# from scan_stripped_links.py's output, used to locate each real hit.
TARGETS = [
    (398, "grammarly-real-estate", ["orClaude. Grammarly"]),
    (395, "notion-ai-engineers", ["thatCursoror GitHubCopilotprovide"]),
    (393, "cursor-engineers", ["Cursor withChatGPTorClaude"]),
    (390, "copilot-insurance", ["usePerplexity AIto find", "Like Claude andChatGPT", "programs,Claudeis"]),
    (389, "copilot-finance", ["usePerplexity AI. Copilot handles", "Like Claude andChatGPT", "analysis,Claudesignificantly"]),
    (388, "copilot-engineers", ["Claude,ChatGPT, orNotion AIare", "Copilot,Cursor, orClaudefor", "codebases,Claudeis"]),
    (387, "copilot-real-estate", ["usePerplexity AIfor web-based"]),
    (386, "copilot-physicians", ["UsePerplexity AIfor literature", "Claude orChatGPTfor that task", "cannot matchClaude's 200K"]),
    (385, "copilot-legal", ["usePerplexity AIfor current events"]),
    (380, "perplexity-insurance", ["ChatGPT orCopilot. Perplexity"]),
    (373, "claude-finance", ["Outlook,Microsoft Copilotoffers"]),
    (371, "claude-real-estate", ["ChatGPT orMicrosoft Copilot. Most workflows", "CRM,Copilotor a ChatGPT-based"]),
    (366, "chatgpt-insurance", ["usePerplexity AIto find current state", "coverage,Claude's larger"]),
    (365, "chatgpt-finance", ["usePerplexity AIor your research", "analysis,Claude's 200K"]),
    (364, "chatgpt-engineers", ["GitHubCopiloteliminates"]),
    (362, "chatgpt-physicians", ["useOtter.aior a dedicated", "both:Otter.aicaptures"]),
    (361, "chatgpt-legal", ["significant.Microsoft Copilot's integration", "agreements,Claude's larger"]),
]


def flatten_strings(value, out):
    if isinstance(value, str):
        if value.strip():
            out.append(value)
    elif isinstance(value, list):
        for v in value:
            flatten_strings(v, out)
    elif isinstance(value, dict):
        for v in value.values():
            flatten_strings(v, out)


def main():
    for post_id, slug, anchors in TARGETS:
        resp = requests.get(
            f"{WP_URL}/wp/v2/cross_reference/{post_id}",
            params={"context": "edit", "_fields": "id,content"},
            auth=AUTH,
        )
        resp.raise_for_status()
        raw = resp.json()["content"]["raw"]

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"\n=== {slug} (post {post_id}) === INVALID JSON ({e})")
            continue

        strings = []
        flatten_strings(data, strings)

        print(f"\n=== {slug} (post {post_id}) ===")
        for anchor in anchors:
            found = False
            for s in strings:
                idx = s.find(anchor)
                if idx != -1:
                    found = True
                    start = max(0, idx - 150)
                    end = min(len(s), idx + len(anchor) + 150)
                    print(f"  anchor {anchor!r}:")
                    print(f"    {s[start:end]!r}")
            if not found:
                print(f"  anchor {anchor!r}: NOT FOUND")


if __name__ == "__main__":
    main()
