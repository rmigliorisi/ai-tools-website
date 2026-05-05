# 12 Claude / Antigravity / Codex Audit Prompts

## Prompt 1: full site audit without changes

```text
Audit this website/repo against the SEO, AI Search/GEO/AEO, agent-friendly website, schema, accessibility, internal linking, and performance requirements in the attached .md files.

Do not make changes yet.

Return:
1. Critical issues
2. High-priority issues
3. Medium-priority issues
4. Low-priority issues
5. Affected files/components/templates
6. Recommended fix
7. SEO/GEO/accessibility impact
8. Implementation risk
9. Validation steps
10. Suggested implementation order
```

## Prompt 2: template-level audit

```text
Audit the main page templates/components against the attached SEO requirements.

Focus on:
- semantic HTML
- crawlable links
- indexability/canonical assumptions
- accessibility tree clarity
- structured data placement
- top summary modules
- internal links
- lazy loading
- HTML bloat
- mobile readability

Do not edit. Produce a template-by-template report.
```

## Prompt 3: implement approved fixes only

```text
Implement only the approved Priority 1 fixes from the audit.

Rules:
- Keep changes minimal.
- Do not change URLs.
- Do not add noindex/canonical/robots changes unless explicitly approved.
- Do not add unsupported schema.
- Preserve design unless the fix requires semantic/accessibility correction.
- Provide a before/after summary.
- Provide files changed.
- Provide validation steps.
```

## Prompt 4: schema audit

```text
Audit structured data against Google-supported Search features and the schema requirements file.

For each page type, report:
- current schema
- whether it matches visible content
- whether Google supports it for Search features
- missing required/recommended properties
- invalid or misleading markup
- recommended schema type
- implementation notes

Do not add schema without approval.
```

## Prompt 5: agent-friendly website audit

```text
Audit this site for agent-friendly usability based on semantic HTML, accessibility tree clarity, stable layouts, and actionable controls.

Check:
- navigation
- cards
- CTAs
- forms
- accordions/tabs
- comparison tables
- menus
- overlays/popups
- lazy-loaded content

Return specific code-level recommendations.
```

## Prompt 6: content quality audit

```text
Audit the content against the content quality and AI Search requirements.

Look for:
- generic AI-style filler
- weak information gain
- bloated summary boxes
- unclear answers
- missing expert/source signals
- weak internal links
- unsupported claims
- stale content
- poor mobile readability

Do not rewrite yet. Provide prioritized recommendations.
```

## Prompt 7: internal linking audit

```text
Audit internal links against the internal linking requirements.

Report:
- orphan pages
- pages with weak inlinks
- links to redirects/404s/non-canonical pages
- vague anchor text
- overused anchors
- missing hub-to-spoke links
- missed contextual links
- high-value pages needing more internal support

Do not add links yet. Provide a proposed link map.
```
