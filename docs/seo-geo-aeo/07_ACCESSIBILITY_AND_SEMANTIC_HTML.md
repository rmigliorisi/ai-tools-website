# 07 Accessibility and Semantic HTML Requirements

## Goal

Make the site understandable and usable by humans, assistive technology, search engines, and AI agents.

## 1. Accessibility tree clarity

The accessibility tree is a browser-generated machine-readable representation of the page. It exposes roles, names, descriptions, values, and states for interactive elements.

A clear accessibility tree helps:
- screen readers
- keyboard users
- browser agents
- AI agents
- QA tools
- semantic understanding

## 2. Required element standards

### Links
Use real anchors:

```html
<a href="/chatgpt/">ChatGPT Review</a>
```

Do not use:

```html
<div onclick="location.href='/chatgpt/'">ChatGPT Review</div>
```

### Buttons
Use buttons for actions:

```html
<button type="button">Open menu</button>
```

Do not use divs/spans as buttons unless absolutely necessary and fully accessible.

### Forms
Every input needs a label:

```html
<label for="email">Email address</label>
<input id="email" name="email" type="email">
```

### Icon buttons
Icon-only controls require accessible labels:

```html
<button aria-label="Open navigation menu">
  <svg aria-hidden="true">...</svg>
</button>
```

### Menus
Menus should expose state:

```html
<button aria-expanded="false" aria-controls="main-menu">
  Menu
</button>
<nav id="main-menu" aria-label="Main navigation">
  ...
</nav>
```

## 3. Keyboard access

All interactive elements must be:
- focusable
- usable with keyboard
- visible when focused
- operable without hover
- reachable in logical order

## 4. Tables

Use real table markup for data tables:
- `<table>`
- `<caption>` where useful
- `<thead>`
- `<th scope="col">`
- `<th scope="row">`

Do not use tables for layout.

## 5. Accordions and tabs

Questions/headers should be buttons. State should be clear with `aria-expanded`. Associated content should be connected using `aria-controls`.

## 6. Images

Meaningful images need descriptive alt. Decorative images should use empty alt.

## 7. Common fixes

### Bad
```html
<div class="card" onclick="go('/tool')">
  <h3>Tool Name</h3>
</div>
```

### Better
```html
<article class="card">
  <h3><a href="/tool">Tool Name</a></h3>
</article>
```

## 8. Testing workflow

For each major template:
1. Use keyboard only.
2. Inspect with Chrome DevTools Accessibility panel.
3. Confirm key elements have role/name/state.
4. Run Lighthouse accessibility.
5. Run axe DevTools if available.
6. Test mobile menu.
7. Test newsletter/contact forms.
8. Confirm no critical action requires hover only.

## 9. Pass/fail criteria

A page passes when:
- main nav is understandable
- CTAs are real links/buttons
- forms are labeled
- menus expose state
- cards have descriptive links
- tables are semantic
- keyboard navigation works
- focus is visible
- agent-relevant actions are obvious
