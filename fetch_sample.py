#!/usr/bin/env python3
"""Verify links in chatgpt-architects content_sections and comparison_notes."""
import urllib.request, json, ssl, base64, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

CREDS = base64.b64encode(b'rmigliorisi:pj60 SqmD OSRD pSe1 9DsV BEeh').decode()
HEADERS = {'Authorization': f'Basic {CREDS}'}
BASE = 'https://aitoolsforpros.com/wp-json/wp/v2'

req = urllib.request.Request(
    f'{BASE}/cross_reference/367?context=edit&_fields=id,slug,content',
    headers=HEADERS
)
with urllib.request.urlopen(req, context=ctx) as r:
    post = json.loads(r.read())

raw = post['content']['raw']
data = json.loads(raw)

sections = data.get('content_sections', [])
print(f"Sections: {len(sections)}")
for i, s in enumerate(sections):
    body = s.get('section_body', '')
    links = re.findall(r'href="([^"]+)"', body)
    print(f"  [{i}] {s.get('section_title','?')[:40]} — links: {links}")

print("\n=== COMPARISON_NOTES links ===")
comp = data.get('comparison_notes', '')
links = re.findall(r'href="([^"]+)"', comp)
print(links)

print("\n=== All data keys ===")
print(list(data.keys()))
