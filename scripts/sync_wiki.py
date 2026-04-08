"""
Sync wiki pages between local Obsidian vault and Upstash Redis.

Usage:
    python scripts/sync_wiki.py --push         # Upload local wiki → Redis
    python scripts/sync_wiki.py --pull         # Download new + updated pages from Redis
    python scripts/sync_wiki.py --status       # Show diff between local and remote
    python scripts/sync_wiki.py --seed         # Initial seed: push local wiki + embeddings
    python scripts/sync_wiki.py --lint         # Run wiki health checks
    python scripts/sync_wiki.py --sync-and-pr  # Pull from Redis + lint + create GitHub PR

Requires KV_REST_API_URL and KV_REST_API_TOKEN in .env
"""

import os
import re
import sys
import json
import hashlib
import argparse
import subprocess
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


# ---------------------------------------------------------------------------
# Redis helpers
# ---------------------------------------------------------------------------

def get_redis_config():
    url = os.environ.get("KV_REST_API_URL", "")
    token = os.environ.get("KV_REST_API_TOKEN", "")
    if not url or not token:
        print("ERROR: KV_REST_API_URL and KV_REST_API_TOKEN must be set in .env")
        sys.exit(1)
    return url.rstrip("/"), token


def redis_get(url, token, key):
    import requests
    resp = requests.get(
        f"{url}/get/{key}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    resp.raise_for_status()
    result = resp.json().get("result")
    if result is None:
        return []
    # Handle potentially double-encoded JSON
    parsed = result
    for _ in range(5):
        if isinstance(parsed, list):
            break
        if isinstance(parsed, str):
            try:
                parsed = json.loads(parsed)
            except (json.JSONDecodeError, TypeError):
                return []
        else:
            break
    if not isinstance(parsed, list):
        return []
    return [p for p in parsed if isinstance(p, dict) and "content" in p]


def redis_set(url, token, key, value):
    import requests
    resp = requests.post(
        f"{url}/set/{key}",
        headers={"Authorization": f"Bearer {token}"},
        json=value,
        timeout=10,
    )
    resp.raise_for_status()


# ---------------------------------------------------------------------------
# Local wiki helpers
# ---------------------------------------------------------------------------

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


def _content_hash(content):
    """Hash content for comparison (ignoring trailing whitespace)."""
    return hashlib.md5(content.strip().encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_status():
    url, token = get_redis_config()
    local_pages = load_local_wiki()
    remote_pages = redis_get(url, token, REDIS_KEY)

    local_titles = {p["title"].lower() for p in local_pages}
    remote_titles = {p["title"].lower() for p in remote_pages}

    only_local = local_titles - remote_titles
    only_remote = remote_titles - local_titles
    shared = local_titles & remote_titles

    # Check for content differences in shared pages
    local_by_title = {p["title"].lower(): p for p in local_pages}
    remote_by_title = {p["title"].lower(): p for p in remote_pages}
    content_diff = []
    for t in shared:
        lh = _content_hash(local_by_title[t]["content"])
        rh = _content_hash(remote_by_title[t]["content"])
        if lh != rh:
            content_diff.append(t)

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

    if content_diff:
        print(f"\nContent differs ({len(content_diff)}):")
        for t in sorted(content_diff):
            meta = remote_by_title[t]
            updated = meta.get("updated_at", "unknown")
            query = meta.get("source_query", "")
            extra = f" (updated: {updated})" if updated != "unknown" else ""
            if query:
                extra += f" query: \"{query[:60]}...\""
            print(f"  ~ {t}{extra}")

    if not only_local and not only_remote and not content_diff:
        print("\nLocal and remote are in sync.")


def cmd_push():
    url, token = get_redis_config()
    local_pages = load_local_wiki()
    remote_pages = redis_get(url, token, REDIS_KEY)

    # Merge: local pages override remote, but keep remote-only pages
    remote_by_title = {p["title"].lower(): p for p in remote_pages}
    local_by_title = {p["title"].lower(): p for p in local_pages}

    merged = list(local_pages)
    for title_lower, p in remote_by_title.items():
        if title_lower not in local_by_title:
            merged.append(p)

    redis_set(url, token, REDIS_KEY, merged)
    print(f"Pushed {len(local_pages)} local pages to Redis (total: {len(merged)})")


def cmd_pull():
    """Pull new AND updated pages from Redis to local vault."""
    url, token = get_redis_config()
    remote_pages = redis_get(url, token, REDIS_KEY)
    local_pages = load_local_wiki()
    local_by_title = {p["title"].lower(): p for p in local_pages}

    new_count = 0
    updated_count = 0
    changes = []

    for page in remote_pages:
        title_lower = page["title"].lower()
        if title_lower not in local_by_title:
            # New page
            path = save_page_locally(page)
            print(f"  New: {page['title']} → {path}")
            new_count += 1
            changes.append({"title": page["title"], "action": "new",
                            "path": str(path)})
        else:
            # Check content difference
            local_hash = _content_hash(local_by_title[title_lower]["content"])
            remote_hash = _content_hash(page["content"])
            if local_hash != remote_hash:
                path = save_page_locally(page)
                print(f"  Updated: {page['title']} → {path}")
                updated_count += 1
                changes.append({"title": page["title"], "action": "updated",
                                "path": str(path)})

    total = new_count + updated_count
    if total:
        print(f"\nPulled {new_count} new + {updated_count} updated page(s).")
        print("Review them in Obsidian, then update wiki/index.md if needed.")
    else:
        print("No changes to pull.")

    return changes


def cmd_seed():
    """Initial seed: push local wiki pages WITH embeddings to Redis."""
    url, token = get_redis_config()
    gemini_key = os.environ.get("GEMINI_API_KEY", "")

    wiki_json_path = WEBAPP_DATA / "wiki_pages.json"
    if wiki_json_path.exists():
        pages = json.loads(wiki_json_path.read_text(encoding="utf-8"))
        print(f"Seeding from exported data: {len(pages)} pages")
    else:
        pages = load_local_wiki()
        print(f"Seeding from local wiki: {len(pages)} pages")
        if gemini_key and pages:
            print("Generating embeddings...")
            texts = [p["content"] for p in pages]
            embs = get_embeddings_batch(texts, gemini_key, batch_pause=0.05)
            for page, emb in zip(pages, embs):
                page["embedding"] = emb

    redis_set(url, token, REDIS_KEY, pages)
    print(f"Seeded {len(pages)} pages to Redis.")


# ---------------------------------------------------------------------------
# Lint checks
# ---------------------------------------------------------------------------

def cmd_lint():
    """Run wiki health checks per CLAUDE.md periodic lint rules."""
    pages = load_local_wiki()
    if not pages:
        print("No wiki pages found.")
        return []

    # Build link graph
    all_stems = set()
    for md_file in WIKI_DIR.rglob("*.md"):
        all_stems.add(md_file.stem.lower())

    # Parse [[wiki-links]] from all pages
    link_pattern = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
    inbound_count = {}  # stem → count of pages linking TO it
    broken_links = []   # (source_title, broken_target)
    all_links = {}      # title → set of targets

    for page in pages:
        links = link_pattern.findall(page["content"])
        targets = set()
        for link in links:
            target_stem = link.strip().lower()
            targets.add(target_stem)
            # Check if target exists
            if target_stem not in all_stems:
                broken_links.append((page["title"], link.strip()))
            else:
                inbound_count[target_stem] = inbound_count.get(target_stem, 0) + 1
        all_links[page["title"]] = targets

    # Exclude index.md and log.md from orphan check
    skip_stems = {"index", "log"}

    results = []

    # Check 1: Orphan pages (fewer than 2 inbound links)
    orphans = []
    for page in pages:
        stem = Path(page["path"]).stem.lower()
        if stem in skip_stems:
            continue
        count = inbound_count.get(stem, 0)
        if count < 2:
            orphans.append((page["title"], count))

    if orphans:
        results.append("### Orphan Pages (fewer than 2 inbound links)")
        for title, count in sorted(orphans):
            results.append(f"- **{title}** ({count} inbound links)")

    # Check 2: Broken links
    if broken_links:
        results.append("\n### Broken Links (target page does not exist)")
        for source, target in sorted(set(broken_links)):
            results.append(f"- `[[{target}]]` in **{source}**")

    # Check 3: Stub promotion candidates (stubs with 3+ inbound links)
    stubs = []
    for page in pages:
        if "**Type**: RAG stub" in page["content"] or \
           page["path"].startswith("wiki/stub-"):
            stem = Path(page["path"]).stem.lower()
            count = inbound_count.get(stem, 0)
            if count >= 3:
                stubs.append((page["title"], count))

    if stubs:
        results.append("\n### Stub Promotion Candidates (3+ inbound links)")
        for title, count in sorted(stubs):
            results.append(
                f"- **{title}** ({count} links) — consider full wiki ingest")

    # Print results
    if results:
        print("\n=== Wiki Lint Report ===\n")
        for line in results:
            print(line)
    else:
        print("\nWiki lint: all checks passed.")

    return results


# ---------------------------------------------------------------------------
# Sync and PR
# ---------------------------------------------------------------------------

def cmd_sync_and_pr():
    """Pull from Redis, run lint, create a GitHub PR for review."""
    # Step 1: Pull changes
    print("=== Step 1: Pull changes from Redis ===")
    changes = cmd_pull()

    if not changes:
        print("\nNo changes from Redis. Checking lint anyway...")

    # Step 2: Run lint
    print("\n=== Step 2: Wiki lint checks ===")
    lint_results = cmd_lint()

    # Step 3: Check if there are any git changes to commit
    result = subprocess.run(
        ["git", "status", "--porcelain", "--", "prof-bhagwan-hybrid-demo/wiki/"],
        capture_output=True, text=True, cwd=PROJECT_ROOT,
    )
    if not result.stdout.strip():
        print("\nNo wiki file changes to commit.")
        return

    # Step 4: Create branch
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    branch = f"wiki-sync/{timestamp}"
    print(f"\n=== Step 3: Creating branch {branch} ===")

    subprocess.run(["git", "checkout", "-b", branch], cwd=PROJECT_ROOT, check=True)

    # Step 5: Stage and commit
    subprocess.run(
        ["git", "add", "prof-bhagwan-hybrid-demo/wiki/"],
        cwd=PROJECT_ROOT, check=True,
    )

    # Build commit message
    commit_lines = ["Wiki sync from Redis\n"]
    for ch in changes:
        commit_lines.append(f"- {ch['action'].capitalize()}: {ch['title']}")

    subprocess.run(
        ["git", "commit", "-m", "\n".join(commit_lines)],
        cwd=PROJECT_ROOT, check=True,
    )

    # Step 6: Push and create PR
    print(f"\n=== Step 4: Push and create PR ===")
    subprocess.run(
        ["git", "push", "-u", "origin", branch],
        cwd=PROJECT_ROOT, check=True,
    )

    # Build PR body
    body_lines = ["## Wiki Sync from Redis\n"]
    body_lines.append(
        "Pages updated by the live chatbot, pulled from Upstash Redis.\n")

    if changes:
        body_lines.append("### Changes\n")
        for ch in changes:
            meta = ""
            if ch.get("updated_at"):
                meta += f" (updated: {ch['updated_at']})"
            if ch.get("source_query"):
                meta += f" query: \"{ch['source_query'][:60]}\""
            body_lines.append(f"- **{ch['action'].upper()}**: {ch['title']}{meta}")

    if lint_results:
        body_lines.append("\n---\n")
        body_lines.append("## Lint Report\n")
        body_lines.extend(lint_results)

    pr_body = "\n".join(body_lines)

    subprocess.run(
        ["gh", "pr", "create",
         "--title", f"Wiki sync {timestamp}",
         "--body", pr_body,
         "--base", "main"],
        cwd=PROJECT_ROOT, check=True,
    )

    # Switch back to main
    subprocess.run(["git", "checkout", "main"], cwd=PROJECT_ROOT, check=True)

    print("\nDone! PR created. Review it on GitHub.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")

    parser = argparse.ArgumentParser(description="Sync wiki with Upstash Redis")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--push", action="store_true",
                       help="Push local wiki to Redis")
    group.add_argument("--pull", action="store_true",
                       help="Pull new + updated pages from Redis")
    group.add_argument("--status", action="store_true",
                       help="Show diff between local and remote")
    group.add_argument("--seed", action="store_true",
                       help="Initial seed with embeddings")
    group.add_argument("--lint", action="store_true",
                       help="Run wiki health checks")
    group.add_argument("--sync-and-pr", action="store_true",
                       help="Pull from Redis + lint + create GitHub PR")
    args = parser.parse_args()

    if args.status:
        cmd_status()
    elif args.push:
        cmd_push()
    elif args.pull:
        cmd_pull()
    elif args.seed:
        cmd_seed()
    elif args.lint:
        cmd_lint()
    elif args.sync_and_pr:
        cmd_sync_and_pr()
