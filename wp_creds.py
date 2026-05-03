"""
WordPress REST API credentials — loaded from .env in the repo root.

Required .env keys (see .env.example):
    WORDPRESS_USERNAME
    WORDPRESS_APP_PASSWORD
    WORDPRESS_SITE_URL  (optional, defaults to https://aitoolsforpros.com)

Also accepts legacy WP_USERNAME / WP_APP_PASSWORD / WP_BASE_URL names.

Usage:
    from wp_creds import HEADERS, BASE          # urllib-based scripts
    from wp_creds import AUTH, WP_URL           # requests-based scripts (migrate_*.py)
"""

import os
import base64
from pathlib import Path

# Load .env from the same directory as this file (repo root)
_env_file = Path(__file__).resolve().parent / '.env'
if _env_file.exists():
    with open(_env_file) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith('#') and '=' in _line:
                _k, _v = _line.split('=', 1)
                os.environ.setdefault(_k.strip(), _v.strip())


def _require(primary, fallback=None):
    val = os.environ.get(primary) or (os.environ.get(fallback) if fallback else None)
    if not val:
        raise RuntimeError(
            f'{primary} is not set.\n'
            'Add it to .env in the repo root (see .env.example).'
        )
    return val


_username = _require('WORDPRESS_USERNAME', fallback='WP_USERNAME')
_password = _require('WORDPRESS_APP_PASSWORD', fallback='WP_APP_PASSWORD')
_site_url = (
    os.environ.get('WORDPRESS_SITE_URL')
    or os.environ.get('WP_BASE_URL', 'https://aitoolsforpros.com')
)

_creds = base64.b64encode(f'{_username}:{_password}'.encode()).decode()

HEADERS = {'Authorization': f'Basic {_creds}', 'Content-Type': 'application/json'}
BASE   = _site_url.rstrip('/') + '/wp-json/wp/v2'  # urllib scripts
AUTH   = (_username, _password)                      # requests scripts (auth= param)
WP_URL = _site_url.rstrip('/') + '/wp-json'         # migrate scripts
