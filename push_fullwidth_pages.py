#!/usr/bin/env python3
"""
Re-push about-us and newsletter with full section wrappers preserved.
The full-width template (page-fullwidth.php) renders content without any
max-width constraint, so section padding/grids work exactly like the static site.
"""

import urllib.request, json, ssl
from bs4 import BeautifulSoup
from wp_creds import HEADERS, BASE

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
BASE_DIR = '/Users/rmigs/Projects/aitoolsforpros website'

SLUG_MAP = {
    'chatgpt.html': '/chatgpt/', 'claude.html': '/claude/', 'perplexity.html': '/perplexity/',
    'gemini.html': '/gemini/', 'copilot.html': '/copilot/', 'midjourney.html': '/midjourney/',
    'cursor.html': '/cursor/', 'notion-ai.html': '/notion-ai/', 'grammarly.html': '/grammarly/',
    'otter.html': '/otter/', 'legal.html': '/legal/', 'physicians.html': '/physicians/',
    'engineers.html': '/engineers/', 'real-estate.html': '/real-estate/', 'finance.html': '/finance/',
    'insurance.html': '/insurance/', 'architects.html': '/architects/', 'creatives.html': '/creatives/',
    'about-us.html': '/about-us/', 'our-process.html': '/our-process/', 'newsletter.html': '/newsletter/',
    'privacy-policy.html': '/privacy-policy/', 'cookie-policy.html': '/cookie-policy/', 'index.html': '/',
}


THEME_SVG = 'https://aitoolsforpros.com/wp-content/themes/aifp-theme/assets/svg'
SVG_FILES = ['author.svg', 'ryan-cooper.svg', 'logo.svg', 'favicon.svg']


def fix_links(soup):
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href in SLUG_MAP:
            a['href'] = SLUG_MAP[href]
        elif href.endswith('.html') and '/' not in href:
            a['href'] = '/' + href.replace('.html', '') + '/'
    for img in soup.find_all('img', src=True):
        src = img['src']
        filename = src.split('/')[-1]
        if filename in SVG_FILES:
            img['src'] = f'{THEME_SVG}/{filename}'


def extract_fullwidth(filename):
    """Extract full section HTML (with wrappers) — content manages its own layout."""
    with open(f'{BASE_DIR}/{filename}', 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Remove nav, footer, scripts, cookie consent
    for tag in soup.find_all(['nav', 'footer', 'script', 'noscript']):
        tag.decompose()
    for div in soup.find_all('div', id=lambda x: x and 'cookie' in x.lower()):
        div.decompose()

    fix_links(soup)

    sections = soup.find_all('section')
    if not sections:
        return ''

    parts = []
    for section in sections:
        # Remove H1 — WordPress title is set separately; section still provides its own heading hierarchy
        for h1 in section.find_all('h1'):
            h1.decompose()
        # Remove the "Review Methodology" pill badges if present
        for badge in section.find_all('div', style=lambda s: s and 'letter-spacing:0.2em' in s if s else False):
            badge.decompose()
        parts.append(str(section))

    return '\n'.join(parts)


def api_update(page_id, content_html, template=None):
    payload = {'content': content_html}
    if template:
        payload['template'] = template
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f'{BASE}/pages/{page_id}',
        data=data,
        headers=HEADERS,
        method='POST'
    )
    req.add_header('X-HTTP-Method-Override', 'PUT')
    with urllib.request.urlopen(req, context=ctx) as r:
        return json.loads(r.read())


pages = [
    ('about-us.html',   1,   'about-us'),
    ('newsletter.html', 685, 'newsletter'),
]

for filename, page_id, slug in pages:
    content = extract_fullwidth(filename)
    print(f"  {slug}: {len(content)} chars extracted")
    result = api_update(page_id, content)
    print(f"  PUSHED: {slug} → page {page_id}")

print("\nContent pushed. Now upload the theme zip, then run this script again with --set-template to activate page-fullwidth.php.")

import sys
if '--set-template' in sys.argv:
    print("\nSetting template on both pages...")
    for filename, page_id, slug in pages:
        result = api_update(page_id, '', template='page-fullwidth.php')
        print(f"  Template set: {slug} → {result.get('template','?')}")
