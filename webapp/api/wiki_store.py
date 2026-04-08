"""
Wiki persistence layer — Upstash Redis (dynamic) with static JSON fallback.

If KV_REST_API_URL and KV_REST_API_TOKEN are set → uses Upstash Redis.
Otherwise → reads from bundled wiki_pages.json (read-only, no dynamic updates).

This is what makes the wiki compound from web conversations.
"""

import os
import json
import time
import requests as http_requests
from pathlib import Path


class WikiStore:
    """Abstract interface for wiki storage."""

    def get_all_pages(self):
        """Return list of wiki page dicts."""
        raise NotImplementedError

    def save_page(self, page):
        """Save/update a wiki page dict {title, content, path, type, embedding}."""
        raise NotImplementedError

    def is_dynamic(self):
        """Return True if this store supports writes (Redis)."""
        return False


class StaticWikiStore(WikiStore):
    """Read-only store backed by a bundled JSON file."""

    def __init__(self, json_path):
        self._path = Path(json_path)
        self._pages = []
        if self._path.exists():
            self._pages = json.loads(self._path.read_text(encoding="utf-8"))

    def get_all_pages(self):
        return list(self._pages)

    def save_page(self, page):
        # No-op for static store
        pass

    def is_dynamic(self):
        return False


class RedisWikiStore(WikiStore):
    """
    Dynamic store backed by Upstash Redis REST API.
    Wiki pages stored as a JSON string under key 'wiki_pages'.
    """

    WIKI_KEY = "wiki_pages"

    def __init__(self, rest_url, rest_token):
        self._url = rest_url.rstrip("/")
        self._token = rest_token
        self._headers = {"Authorization": f"Bearer {rest_token}"}
        self._cache = None
        self._cache_time = 0
        self._cache_ttl = 30  # seconds — re-read from Redis every 30s

    def _redis_get(self, key):
        """GET a value from Upstash Redis."""
        resp = http_requests.get(
            f"{self._url}/get/{key}",
            headers=self._headers,
            timeout=5,
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("result")

    def _redis_set(self, key, value):
        """SET a value in Upstash Redis."""
        resp = http_requests.post(
            f"{self._url}/set/{key}",
            headers=self._headers,
            json=value,
            timeout=10,
        )
        resp.raise_for_status()

    def get_all_pages(self):
        now = time.time()
        if self._cache is not None and (now - self._cache_time) < self._cache_ttl:
            return list(self._cache)

        try:
            raw = self._redis_get(self.WIKI_KEY)
            if raw:
                self._cache = json.loads(raw) if isinstance(raw, str) else raw
            else:
                self._cache = []
            self._cache_time = now
        except Exception as exc:
            print(f"[WikiStore] Redis read failed: {exc}")
            if self._cache is not None:
                return list(self._cache)
            self._cache = []

        return list(self._cache)

    def save_page(self, page):
        """Add or update a page, then write back to Redis."""
        pages = self.get_all_pages()

        # Update existing or append
        updated = False
        for i, p in enumerate(pages):
            if p.get("title", "").lower() == page.get("title", "").lower():
                pages[i] = page
                updated = True
                break
        if not updated:
            pages.append(page)

        try:
            self._redis_set(self.WIKI_KEY, json.dumps(pages))
            self._cache = pages
            self._cache_time = time.time()
        except Exception as exc:
            print(f"[WikiStore] Redis write failed: {exc}")

    def is_dynamic(self):
        return True

    def seed(self, pages):
        """Bulk load pages into Redis (used during initial setup)."""
        try:
            self._redis_set(self.WIKI_KEY, json.dumps(pages))
            self._cache = pages
            self._cache_time = time.time()
            print(f"[WikiStore] Seeded {len(pages)} pages to Redis")
        except Exception as exc:
            print(f"[WikiStore] Seed failed: {exc}")

    def get_all_raw(self):
        """Get raw pages from Redis (for sync script)."""
        raw = self._redis_get(self.WIKI_KEY)
        if raw:
            return json.loads(raw) if isinstance(raw, str) else raw
        return []


def create_wiki_store(data_dir=None):
    """
    Factory: return RedisWikiStore if env vars are set, else StaticWikiStore.
    """
    kv_url = os.environ.get("KV_REST_API_URL", "")
    kv_token = os.environ.get("KV_REST_API_TOKEN", "")

    if kv_url and kv_token:
        print("[WikiStore] Using Upstash Redis (dynamic wiki)")
        return RedisWikiStore(kv_url, kv_token)

    if data_dir is None:
        data_dir = Path(__file__).parent.parent / "data"
    json_path = Path(data_dir) / "wiki_pages.json"
    print(f"[WikiStore] Using static JSON: {json_path}")
    return StaticWikiStore(json_path)
