#!/usr/bin/env python3
"""
Standardize all "Where Falls Short" content sections to canonical
.limitations-grid + .limit-card + .limit-title + .limit-desc format.
"""

import urllib.request, urllib.parse, json, ssl, sys
from bs4 import BeautifulSoup
from wp_creds import HEADERS, BASE

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def api_get(path):
    req = urllib.request.Request(f'{BASE}{path}', headers=HEADERS)
    with urllib.request.urlopen(req, context=ctx) as r:
        return json.loads(r.read())


def api_put(path, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(f'{BASE}{path}', data=data, headers=HEADERS, method='POST')
    req.add_header('X-HTTP-Method-Override', 'PUT')
    with urllib.request.urlopen(req, context=ctx) as r:
        return json.loads(r.read())


def extract_items(body):
    """Extract (title, desc) pairs from any falls_short HTML format."""
    soup = BeautifulSoup(body, 'html.parser')
    items = []

    # Format A: .limitations-grid > .limitation-card > .limitation-body > h4 + p
    if soup.select('.limitation-body'):
        for card in soup.select('.limitation-card'):
            lb = card.select_one('.limitation-body')
            if not lb:
                continue
            h = lb.find(['h4', 'h3'])
            ps = lb.find_all('p')
            title = h.get_text(strip=True) if h else ''
            desc = ps[0].get_text(strip=True) if ps else ''
            if title:
                items.append((title, desc))
        return items

    # Format B: .limitations-grid > .limitation-card > div.limitation-title + p
    if soup.select('.limitation-card'):
        for card in soup.select('.limitation-card'):
            title_el = card.select_one('.limitation-title')
            p_els = [p for p in card.find_all('p')]
            title = title_el.get_text(strip=True) if title_el else ''
            desc = p_els[0].get_text(strip=True) if p_els else ''
            if title:
                items.append((title, desc))
        return items

    # Format C: .limitations-grid > .limit-card (already canonical — still normalize)
    if soup.select('.limit-card'):
        for card in soup.select('.limit-card'):
            title_el = card.select_one('.limit-title')
            desc_el = card.select_one('.limit-desc')
            title = title_el.get_text(strip=True) if title_el else ''
            desc = desc_el.get_text(strip=True) if desc_el else ''
            if title:
                items.append((title, desc))
        return items

    # Format D: ICON-FLEX — outer div > inner div > span[✗] + div > p + p
    icon_spans = soup.find_all('span', style=lambda s: s and 'flex-shrink' in s if s else False)
    if icon_spans:
        for span in icon_spans:
            parent_div = span.parent
            inner = parent_div.find('div')
            if not inner:
                continue
            ps = inner.find_all('p')
            if len(ps) >= 2:
                title = ps[0].get_text(strip=True)
                desc = ps[1].get_text(strip=True)
                if title:
                    items.append((title, desc))
        if items:
            return items

    # Format E: STACKED-DIVS — sibling div[border:fca5a5 or fecaca] each with p[font-weight:700] + p
    # Also handles INLINE-RED outer container div > inner card divs
    outer_flex = soup.find('div', style=lambda s: s and 'flex-direction:column' in s if s else False)
    if outer_flex:
        for card in outer_flex.find_all('div', recursive=False):
            ps = card.find_all('p')
            if len(ps) >= 2:
                title = ps[0].get_text(strip=True)
                desc = ps[1].get_text(strip=True)
                if title:
                    items.append((title, desc))
        if items:
            return items

    # Format E2: STACKED-DIVS without outer flex wrapper (cards are direct children of body)
    stacked = soup.find_all('div', style=lambda s: s and ('fca5a5' in s or 'fecaca' in s) if s else False)
    if stacked:
        for card in stacked:
            ps = card.find_all('p')
            if len(ps) >= 2:
                title = ps[0].get_text(strip=True)
                desc = ps[1].get_text(strip=True)
                if title:
                    items.append((title, desc))
        if items:
            return items

    # Format F: UL-LIST — ul > li > strong:title + text
    ul = soup.find('ul')
    if ul:
        for li in ul.find_all('li'):
            strong = li.find('strong')
            if strong:
                title = strong.get_text(strip=True).rstrip(':')
                strong.extract()
                desc = li.get_text(strip=True).lstrip()
                items.append((title, desc))
        if items:
            return items

    # Format G: H3+P pattern (perplexity-legal)
    for h3 in soup.find_all('h3'):
        title = h3.get_text(strip=True)
        next_p = h3.find_next_sibling('p')
        desc = next_p.get_text(strip=True) if next_p else ''
        if title:
            items.append((title, desc))
    if items:
        return items

    return []


def build_canonical(items):
    """Build canonical HTML from (title, desc) pairs."""
    cards = []
    for title, desc in items:
        cards.append(
            f'<div class="limit-card">\n'
            f'<div class="limit-title">{title}</div>\n'
            f'<div class="limit-desc">{desc}</div>\n'
            f'</div>'
        )
    return '<div class="limitations-grid">\n' + '\n'.join(cards) + '\n</div>'


def main(dry_run=True):
    posts = api_get('/cross_reference?per_page=100&context=edit&_fields=id,slug,content')
    print(f"Loaded {len(posts)} cross-reference posts")

    updated = 0
    skipped = 0
    failed = []

    for p in posts:
        raw = p['content']['raw']
        try:
            data = json.loads(raw)
        except Exception as e:
            print(f"  JSON error {p['slug']}: {e}")
            continue

        sections = data.get('content_sections', [])
        changed = False

        for i, s in enumerate(sections):
            if 'Falls Short' not in s.get('section_title', ''):
                continue

            body = s.get('section_body', '')
            items = extract_items(body)

            if not items:
                failed.append(p['slug'])
                print(f"  PARSE FAILED: {p['slug']}")
                continue

            new_body = build_canonical(items)

            # Skip if already canonical (exact match)
            if body.strip() == new_body.strip():
                skipped += 1
                continue

            if dry_run:
                print(f"\n  DRY RUN {p['slug']}: {len(items)} items")
                for t, d in items:
                    print(f"    - {t[:70]!r}")
            else:
                sections[i]['section_body'] = new_body
                changed = True

        if changed and not dry_run:
            data['content_sections'] = sections
            payload = {'content': json.dumps(data)}
            try:
                api_put(f'/cross_reference/{p["id"]}', payload)
                print(f"  UPDATED: {p['slug']}")
                updated += 1
            except Exception as e:
                print(f"  ERROR updating {p['slug']}: {e}")
                failed.append(p['slug'])

    print(f"\n{'DRY RUN' if dry_run else 'DONE'}: updated={updated}, skipped={skipped}, failed={len(failed)}")
    if failed:
        print(f"Failed: {failed}")


if __name__ == '__main__':
    dry_run = '--apply' not in sys.argv
    if dry_run:
        print("=== DRY RUN (pass --apply to write changes) ===\n")
    else:
        print("=== APPLYING CHANGES ===\n")
    main(dry_run=dry_run)
