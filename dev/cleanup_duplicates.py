#!/usr/bin/env python3
"""
Delete duplicate tool_review and profession_hub posts, keeping the canonical slug only.
Canonical slugs: chatgpt, claude, perplexity, gemini, copilot, midjourney, cursor, notion-ai, grammarly, otter
                 legal, physicians, real-estate, engineers, finance, insurance, architects, creatives
"""
import sys, requests

sys.path.insert(0, __import__('pathlib').Path(__file__).parent.parent.__str__())
from migrate_v2 import WP_URL, AUTH

KEEP_SLUGS = {
    'tool_review': {
        'chatgpt', 'claude', 'perplexity', 'gemini', 'copilot',
        'midjourney', 'cursor', 'notion-ai', 'grammarly', 'otter',
    },
    'profession_hub': {
        'legal', 'physicians', 'real-estate', 'engineers',
        'finance', 'insurance', 'architects', 'creatives',
    },
}


def cleanup(post_type):
    kept = KEEP_SLUGS[post_type]
    page, deleted = 1, 0
    while True:
        r = requests.get(
            f"{WP_URL}/wp/v2/{post_type}",
            params={'per_page': 100, 'page': page, 'context': 'edit'},
            auth=AUTH,
        )
        if r.status_code != 200:
            break
        posts = r.json()
        if not posts:
            break
        for post in posts:
            slug = post['slug']
            pid = post['id']
            if slug not in kept:
                resp = requests.delete(
                    f"{WP_URL}/wp/v2/{post_type}/{pid}",
                    params={'force': True},
                    auth=AUTH,
                )
                status = 'DELETED' if resp.status_code == 200 else f'FAIL({resp.status_code})'
                print(f"  {status}  {post_type}/{slug}  (id {pid})")
                deleted += 1
            else:
                print(f"  KEEP    {post_type}/{slug}  (id {pid})")
        page += 1
    return deleted


print("── Tool Reviews ──")
n1 = cleanup('tool_review')
print(f"\n── Profession Hubs ──")
n2 = cleanup('profession_hub')
print(f"\nTotal deleted: {n1 + n2}")
