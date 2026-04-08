"""
Sync wiki pages between local Obsidian vault and Upstash Redis.

Usage:
    python scripts/sync_wiki.py --push     # Upload local wiki → Redis
    python scripts/sync_wiki.py --pull     # Download Redis wiki → local
    python scripts/sync_wiki.py --status   # Show diff between local and remote
    python scripts/sync_wiki.py --seed     # Initial seed: push local wiki + embeddings to Redis

Requires KV_REST_API_URL and KV_REST_API_TOKEN in .env
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from chunker import get_embeddings_batch

PROJECT_ROOT = Path(__file__).parent.parent
VAULT = PROJECT_ROOT / "prof-bhagwan-hybrid-demo"
WIKI_DIR = VAULT / "wiki"
DATA_DIR = PROJECT_ROOT / "data"
WEBAPP_DATA = PROJECT_ROOT / "webapp" / "data"

REDIS_KEY = "wiki_pages"


def get_redis_config():
    url = os.environ.get("KV_REST_API_URL", "")
    token = os.environ.get("KV_REST_API_TOKEN", "")
    if not url or not token:
        print("ERROR: KV_REST_API_URL and KV_REST_API_TOKEN must be set in .env")
        sys.exit(1)
    return url.rstrip("/"), token


def redis_get(url, token, key):
    import requests
    resp = requests.get(f"{url}/get/{key}", headers={"Authorization": f"Bearer {token}"}, timeout=10)
    resp.raise_for_status()
    result = resp.json().get("result")
    if result:
        return json.loads(result) if isinstance(result, str) else result
    return []


def redis_set(url, token, key, value):
    import requests
    resp = requests.post(
        f"{url}/set/{key}",
        headers={"Authorization": f"Bearer {token}"},
        json=json.dumps(value),
        timeout=10,
    )
    resp.raise_for_status()


def load_local_wiki():
    """Load all wiki pages from local Obsidian vault."""
    pages = []
    if not WIKI_DIR.exists():
        return pages
    for md_file in sorted(WIKI_DIR.rglob("*.md")):
        content = md_file.read_text(encoding="utf-8").strip()
        if len(content) < 50:
            continue
        title = md_file.stem.replace("-", " ").replace("_", " ").title()
        for line in content.splitlines():
            if line.startswith("# "):
                title = line.lstrip("# ").strip()
                break
        pages.append({
            "title": title,
            "path": str(md_file.relative_to(VAULT)),
            "content": content,
            "type": "wiki",
        })
    return pages


def save_page_locally(page):
    """Write a wiki page to the local Obsidian vault."""
    path = page.get("path", "")
    if not path:
        slug = page["title"].lower().replace(" ", "-")
        path = f"wiki/{slug}.md"

    full_path = VAULT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(page["content"], encoding="utf-8")
    return full_path


def cmd_status():
    url, token = get_redis_config()
    local_pages = load_local_wiki()
    remote_pages = redis_get(url, token, REDIS_KEY)

    local_titles = {p["title"].lower() for p in local_pages}
    remote_titles = {p["title"].lower() for p in remote_pages}

    only_local = local_titles - remote_titles
    only_remote = remote_titles - local_titles
    shared = local_titles & remote_titles

    print(f"\nLocal:  {len(local_pages)} pages")
    print(f"Remote: {len(remote_pages)} pages")
    print(f"Shared: {len(shared)} pages")

    if only_local:
        print(f"\nOnly local ({len(only_local)}):")
        for t in sorted(only_local):
            print(f"  + {t}")

    if only_remote:
        print(f"\nOnly remote ({len(only_remote)}) — created by web conversations:")
        for t in sorted(only_remote):
            print(f"  * {t}")

    if not only_local and not only_remote:
        print("\nLocal and remote are in sync.")


def cmd_push():
    url, token = get_redis_config()
    local_pages = load_local_wiki()
    remote_pages = redis_get(url, token, REDIS_KEY)

    # Merge: local pages override remote, but keep remote-only pages
    remote_by_title = {p["title"].lower(): p for p in remote_pages}
    local_by_title = {p["title"].lower(): p for p in local_pages}

    merged = []
    for p in local_pages:
        merged.append(p)
    for title_lower, p in remote_by_title.items():
        if title_lower not in local_by_title:
            merged.append(p)

    redis_set(url, token, REDIS_KEY, merged)
    print(f"Pushed {len(local_pages)} local pages to Redis (total: {len(merged)})")


def cmd_pull():
    url, token = get_redis_config()
    remote_pages = redis_get(url, token, REDIS_KEY)
    local_pages = load_local_wiki()
    local_titles = {p["title"].lower() for p in local_pages}

    new_count = 0
    for page in remote_pages:
        if page["title"].lower() not in local_titles:
            path = save_page_locally(page)
            print(f"  Downloaded: {page['title']} → {path}")
            new_count += 1

    if new_count:
        print(f"\nPulled {new_count} new page(s) from Redis to local vault.")
        print("Review them in Obsidian, then update wiki/index.md.")
    else:
        print("No new remote pages to pull.")


def cmd_seed():
    """Initial seed: push local wiki pages WITH embeddings to Redis."""
    url, token = get_redis_config()
    gemini_key = os.environ.get("GEMINI_API_KEY", "")

    # Load from exported webapp data (which has embeddings)
    wiki_json_path = WEBAPP_DATA / "wiki_pages.json"
    if wiki_json_path.exists():
        pages = json.loads(wiki_json_path.read_text(encoding="utf-8"))
        print(f"Seeding from exported data: {len(pages)} pages")
    else:
        pages = load_local_wiki()
        print(f"Seeding from local wiki: {len(pages)} pages")
        if gemini_key and pages:
            print("Generating embeddings…")
            texts = [p["content"] for p in pages]
            embs = get_embeddings_batch(texts, gemini_key, batch_pause=0.05)
            for page, emb in zip(pages, embs):
                page["embedding"] = emb

    redis_set(url, token, REDIS_KEY, pages)
    print(f"Seeded {len(pages)} pages to Redis.")


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")

    parser = argparse.ArgumentParser(description="Sync wiki with Upstash Redis")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--push", action="store_true", help="Push local wiki to Redis")
    group.add_argument("--pull", action="store_true", help="Pull Redis wiki to local")
    group.add_argument("--status", action="store_true", help="Show diff")
    group.add_argument("--seed", action="store_true", help="Initial seed with embeddings")
    args = parser.parse_args()

    if args.status:
        cmd_status()
    elif args.push:
        cmd_push()
    elif args.pull:
        cmd_pull()
    elif args.seed:
        cmd_seed()
