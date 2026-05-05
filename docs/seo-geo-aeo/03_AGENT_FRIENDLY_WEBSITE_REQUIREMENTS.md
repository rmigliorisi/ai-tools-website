# 03 Agent-Friendly Website Requirements

## Goal

Make the website usable by AI agents that may navigate, interpret, and act on behalf of users.

Agent-friendly design is not a confirmed Google Search ranking factor. Treat it as an emerging web usability layer that overlaps with accessibility, UX, technical SEO, and AI search readiness.

## 1. Agents may use multiple inputs

Design for agents that may use:
- screenshots
- raw HTML / DOM
- accessibility tree
- semantic HTML
- visible text
- page layout
- links and form controls

## 2. Use semantic HTML

### Required
Use real semantic elements wherever possible:

```html
<header>
<nav>
<main>
<article>
<section>
<aside>
<footer>
<a href="/page/">Link text</a>
<button type="button">Open menu</button>
<form>
<label for="email">Email address</label>
<input id="email" name="email" type="email">
<table>
<thead>
<tbody>
```

### Avoid
- fake buttons made from `div`
- fake links made from `span`
- clickable cards without real anchors
- unlabeled form fields
- icon-only buttons without accessible names
- hover-only menus

## 3. Make actions explicit

Each action should answer:
- what is this?
- what happens if selected?
- what object does it act on?
- what state is it in?

### Good
```html
<button aria-expanded="false" aria-controls="tools-menu">
  AI Tools
</button>
<nav id="tools-menu" aria-label="AI tools">
  <a href="/chatgpt/">ChatGPT review</a>
</nav>
```

### Bad
```html
<div onclick="toggleMenu()">AI Tools</div>
```

## 4. Link cards correctly

If a card links to a page, use a real anchor.

Good:

```html
<article class="card">
  <h3><a href="/chatgpt/legal/">ChatGPT for Lawyers</a></h3>
  <p>Workflow guidance for legal professionals.</p>
</article>
```

Avoid vague repeated anchors like:
- Learn more
- Click here
- Read more

Use descriptive anchors:
- Read the ChatGPT for Lawyers guide
- Compare AI tools for real estate agents

## 5. Make forms machine-readable

Required:
- every input has a visible or accessible label
- labels are associated with inputs
- errors are readable and associated with fields
- submit buttons describe the action
- required fields are marked accessibly

Good:

```html
<label for="newsletter-email">Email address</label>
<input id="newsletter-email" name="email" type="email" autocomplete="email">
<button type="submit">Subscribe to updates</button>
```

## 6. Keep layouts stable

Avoid:
- major content shifts after load
- popups covering key actions
- cookie banners blocking CTAs
- invisible overlays
- moving buttons
- menus that relocate after interaction

## 7. Do not hide critical content behind interaction

Agents and crawlers may not click or scroll like humans.

Keep these visible or reliably rendered:
- H1
- intro/definition
- key answer/verdict
- primary CTA
- primary internal links
- pricing/eligibility details
- important warnings/caveats
- structured data matching visible content

## 8. Lazy loading rules

Good to lazy-load:
- images
- videos
- iframes
- below-the-fold media
- noncritical widgets

Risky to lazy-load:
- primary text
- important links
- pricing tables
- legal/compliance content
- reviews/ratings
- key comparison data
- structured data

## 9. Accessibility tree clarity

Important elements must have:
- correct role
- accessible name
- state where relevant
- focusability where interactive
- keyboard operability

Test in Chrome DevTools Accessibility panel.

## 10. Agent QA checklist

For each important template, verify:
- Can an agent identify the page topic?
- Can an agent find the main CTA?
- Can an agent understand menus?
- Can an agent understand cards and tables?
- Can an agent submit a form safely?
- Can an agent tell which button/link belongs to which item?
- Does the screenshot match the semantic structure?
- Does the accessibility tree make sense?
