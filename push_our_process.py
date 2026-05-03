#!/usr/bin/env python3
"""Re-push our-process page with fixed extraction (section tags preserved, H1 kept)."""

import urllib.request, json, ssl, re
from bs4 import BeautifulSoup
from wp_creds import HEADERS, BASE

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
BASE_DIR = '/Users/rmigs/Projects/aitoolsforpros website'
PAGE_ID = 684

SLUG_MAP = {
    'chatgpt.html': '/chatgpt/', 'claude.html': '/claude/', 'perplexity.html': '/perplexity/',
    'gemini.html': '/gemini/', 'copilot.html': '/copilot/', 'midjourney.html': '/midjourney/',
    'cursor.html': '/cursor/', 'notion-ai.html': '/notion-ai/', 'grammarly.html': '/grammarly/',
    'otter.html': '/otter/', 'legal.html': '/legal/', 'physicians.html': '/physicians/',
    'engineers.html': '/engineers/', 'real-estate.html': '/real-estate/', 'finance.html': '/finance/',
    'insurance.html': '/insurance/', 'architects.html': '/architects/', 'creatives.html': '/creatives/',
    'about-us.html': '/about-us/', 'our-process.html': '/our-process/',
    'newsletter.html': '/newsletter/', 'privacy-policy.html': '/privacy-policy/',
    'cookie-policy.html': '/cookie-policy/', 'index.html': '/',
}

with open(f'{BASE_DIR}/our-process.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

for tag in soup.find_all(['nav', 'footer', 'script', 'noscript']):
    tag.decompose()
for div in soup.find_all('div', id=lambda x: x and 'cookie' in x.lower()):
    div.decompose()

for a in soup.find_all('a', href=True):
    href = a['href']
    if href in SLUG_MAP:
        a['href'] = SLUG_MAP[href]
    elif href.endswith('.html') and '/' not in href:
        a['href'] = '/' + href.replace('.html', '') + '/'

# Include full section tags so inline padding styles are preserved
sections = soup.find_all('section')
parts = [str(s).strip() for s in sections if str(s).strip()]
content = '\n\n'.join(parts)

print(f"Extracted {len(content)} chars from our-process.html")

payload = {'content': content}
data = json.dumps(payload).encode()
req = urllib.request.Request(f'{BASE}/pages/{PAGE_ID}', data=data, headers=HEADERS, method='POST')
req.add_header('X-HTTP-Method-Override', 'PUT')
with urllib.request.urlopen(req, context=ctx) as r:
    result = json.loads(r.read())

print(f"Pushed: page ID {result.get('id')} — status {result.get('status')}")
