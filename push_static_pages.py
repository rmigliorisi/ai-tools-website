#!/usr/bin/env python3
"""
Extract main content from 5 static HTML files and push to WordPress pages.
Strips: nav, footer, h1 (template renders it), section padding wrappers.
Fixes: relative links → absolute /slug/ paths.
"""

import urllib.request, json, ssl, base64, re
from bs4 import BeautifulSoup

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

CREDS = base64.b64encode(b'rmigliorisi:pj60 SqmD OSRD pSe1 9DsV BEeh').decode()
HEADERS = {'Authorization': f'Basic {CREDS}', 'Content-Type': 'application/json'}
BASE = 'https://aitoolsforpros.com/wp-json/wp/v2'

BASE_DIR = '/Users/rmigs/Projects/aitoolsforpros website'

# WordPress page IDs
PAGE_IDS = {
    'our-process':    684,
    'newsletter':     685,
    'privacy-policy': 686,
    'cookie-policy':  687,
    'about-us':       1,
}

# Static HTML file for each page
FILES = {
    'our-process':    'our-process.html',
    'newsletter':     'newsletter.html',
    'privacy-policy': 'privacy-policy.html',
    'cookie-policy':  'cookie-policy.html',
    'about-us':       'about-us.html',
}

# Tool/profession slugs — links like "chatgpt.html" → "/chatgpt/"
SLUG_MAP = {
    'chatgpt.html': '/chatgpt/',
    'claude.html': '/claude/',
    'perplexity.html': '/perplexity/',
    'gemini.html': '/gemini/',
    'copilot.html': '/copilot/',
    'midjourney.html': '/midjourney/',
    'cursor.html': '/cursor/',
    'notion-ai.html': '/notion-ai/',
    'grammarly.html': '/grammarly/',
    'otter.html': '/otter/',
    'legal.html': '/legal/',
    'physicians.html': '/physicians/',
    'engineers.html': '/engineers/',
    'real-estate.html': '/real-estate/',
    'finance.html': '/finance/',
    'insurance.html': '/insurance/',
    'architects.html': '/architects/',
    'creatives.html': '/creatives/',
    'about-us.html': '/about-us/',
    'our-process.html': '/our-process/',
    'newsletter.html': '/newsletter/',
    'privacy-policy.html': '/privacy-policy/',
    'cookie-policy.html': '/cookie-policy/',
    'index.html': '/',
}


def fix_links(soup):
    """Replace relative HTML links with absolute WordPress paths."""
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href in SLUG_MAP:
            a['href'] = SLUG_MAP[href]
        elif href.endswith('.html') and '/' not in href:
            # Unknown .html link — strip extension
            a['href'] = '/' + href.replace('.html', '') + '/'


def extract_content(slug):
    """Parse static HTML and return the inner content HTML string."""
    filepath = f'{BASE_DIR}/{FILES[slug]}'
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Remove nav, footer, script, noscript, cookie consent
    for tag in soup.find_all(['nav', 'footer', 'script', 'noscript']):
        tag.decompose()
    # Remove cookie consent div if present
    for div in soup.find_all('div', id=lambda x: x and 'cookie' in x.lower()):
        div.decompose()

    # Fix links before extracting
    fix_links(soup)

    # Find all section elements (content lives here after nav removal)
    sections = soup.find_all('section')
    if not sections:
        # Fallback: everything inside body
        body = soup.find('body')
        return str(body) if body else ''

    parts = []
    for section in sections:
        # Include the full section tag so its inline padding/styles are preserved.
        # H1 is kept — page.php does not render a separate title for pages.
        html_str = str(section).strip()
        if html_str:
            parts.append(html_str)

    return '\n\n'.join(parts)


def api_put(page_id, content_html):
    payload = {'content': content_html}
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


def main():
    for slug, page_id in PAGE_IDS.items():
        content = extract_content(slug)
        print(f"  {slug}: extracted {len(content)} chars")
        api_put(page_id, content)
        print(f"  PUSHED: {slug} → page ID {page_id}")

    print("\nDone.")


if __name__ == '__main__':
    main()
