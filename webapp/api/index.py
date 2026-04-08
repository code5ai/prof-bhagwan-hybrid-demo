"""
Flask backend for Prof. Bhagwan Chowdhry's knowledge chatbot.

Hybrid search (92.4% semantic + 7.6% BM25) over wiki pages and RAG chunks.
Streamed via Claude Sonnet 4.6 with SSE.
Wiki updates extracted from responses and persisted to Upstash Redis.
"""

import os
import json
import time
import threading
from pathlib import Path

import numpy as np
import requests as http_requests
from flask import Flask, request, Response, jsonify, send_from_directory
from anthropic import Anthropic
from rank_bm25 import BM25Okapi

# ---------------------------------------------------------------------------
# Wiki persistence layer (inline — Vercel can't resolve sibling imports)
# ---------------------------------------------------------------------------


def _safe_parse_pages(raw):
    """Unwrap potentially double/triple-encoded JSON from Redis.
    Returns a list of dicts, or [] on failure."""
    if raw is None:
        return []
    parsed = raw
    # Keep unwrapping JSON strings until we get a list
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
    # Ensure every element is a dict with a "content" key
    return [p for p in parsed if isinstance(p, dict) and "content" in p]


class WikiStore:
    def get_all_pages(self):
        raise NotImplementedError

    def save_page(self, page):
        raise NotImplementedError

    def is_dynamic(self):
        return False


class StaticWikiStore(WikiStore):
    def __init__(self, json_path):
        self._pages = []
        p = Path(json_path)
        if p.exists():
            try:
                self._pages = _safe_parse_pages(p.read_text(encoding="utf-8"))
            except Exception as exc:
                print(f"[WikiStore] Failed to load {p}: {exc}")

    def get_all_pages(self):
        return list(self._pages)

    def save_page(self, page):
        pass

    def is_dynamic(self):
        return False


class RedisWikiStore(WikiStore):
    WIKI_KEY = "wiki_pages"

    def __init__(self, rest_url, rest_token):
        self._url = rest_url.rstrip("/")
        self._headers = {"Authorization": f"Bearer {rest_token}"}
        self._cache = None
        self._cache_time = 0
        self._cache_ttl = 30

    def _redis_get(self, key):
        resp = http_requests.get(
            f"{self._url}/get/{key}", headers=self._headers, timeout=5)
        resp.raise_for_status()
        return resp.json().get("result")

    def _redis_set(self, key, value):
        """Store a Python object in Redis. Serializes to JSON internally."""
        resp = http_requests.post(
            f"{self._url}/set/{key}", headers=self._headers,
            json=value, timeout=10)
        resp.raise_for_status()

    def get_all_pages(self):
        now = time.time()
        if self._cache is not None and (now - self._cache_time) < self._cache_ttl:
            return list(self._cache)
        try:
            raw = self._redis_get(self.WIKI_KEY)
            self._cache = _safe_parse_pages(raw)
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
        updated = False
        for i, p in enumerate(pages):
            if p.get("title", "").lower() == page.get("title", "").lower():
                pages[i] = page
                updated = True
                break
        if not updated:
            pages.append(page)
        try:
            # Pass the Python list directly — _redis_set handles serialization
            self._redis_set(self.WIKI_KEY, pages)
            self._cache = pages
            self._cache_time = time.time()
        except Exception as exc:
            print(f"[WikiStore] Redis write failed: {exc}")

    def is_dynamic(self):
        return True


def create_wiki_store(data_dir=None):
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


# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = Flask(__name__)

DATA_DIR = Path(__file__).parent.parent / "data"

# Claude model — configurable via env var
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")

# Search weights
W_BM25 = 0.076
W_SEMANTIC = 0.924

# Wiki update markers
WIKI_OPEN = "<wiki_update>"
WIKI_CLOSE = "</wiki_update>"

# ---------------------------------------------------------------------------
# Load knowledge base
# ---------------------------------------------------------------------------


def _load_json(path):
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"[Data] Failed to load {path}: {exc}")
    return []


# RAG chunks — static, bundled at deploy time (text only, no embeddings)
_raw_chunks = _load_json(DATA_DIR / "chunks.json")
# Validate: only keep dicts with a "content" key
CHUNKS = [c for c in _raw_chunks if isinstance(c, dict) and "content" in c]
print(f"[Data] Loaded {len(CHUNKS)} RAG chunks")

# Chunk embeddings — stored as numpy binary to avoid 352MB JSON bloat
_CHUNK_EMB_PATH = DATA_DIR / "chunks_embeddings.npy"
CHUNK_EMBEDDINGS = None
try:
    if _CHUNK_EMB_PATH.exists():
        CHUNK_EMBEDDINGS = np.load(str(_CHUNK_EMB_PATH))
        print(f"[Data] Loaded chunk embeddings: {CHUNK_EMBEDDINGS.shape}")
except Exception as exc:
    print(f"[Data] Failed to load embeddings: {exc}. Falling back to BM25-only.")

# Wiki pages — dynamic via store (Redis or static fallback)
WIKI_STORE = create_wiki_store(DATA_DIR)

# ---------------------------------------------------------------------------
# Search index — rebuilt when wiki updates
# ---------------------------------------------------------------------------

_index_lock = threading.Lock()


class SearchIndex:
    """Mutable search index that can be rebuilt when wiki pages change."""

    def __init__(self):
        self.all_docs = []
        self.bm25 = None
        self.embeddings = None
        self.has_embeddings = False
        self.rebuild()

    def rebuild(self):
        """Rebuild the index from current wiki pages + static RAG chunks."""
        wiki_pages = WIKI_STORE.get_all_pages()
        self.all_docs = wiki_pages + CHUNKS

        if not self.all_docs:
            self.bm25 = None
            self.embeddings = None
            self.has_embeddings = False
            return

        tokenized = [doc["content"].lower().split() for doc in self.all_docs]
        self.bm25 = BM25Okapi(tokenized)

        # Build embedding matrix
        wiki_embs = [p["embedding"] for p in wiki_pages
                     if isinstance(p.get("embedding"), list) and len(p["embedding"]) > 0]

        if CHUNK_EMBEDDINGS is not None and len(CHUNK_EMBEDDINGS) == len(CHUNKS):
            if len(wiki_embs) == len(wiki_pages) and wiki_embs:
                wiki_arr = np.array(wiki_embs, dtype=np.float32)
                self.embeddings = np.vstack([wiki_arr, CHUNK_EMBEDDINGS])
            else:
                # Wiki pages missing/incomplete embeddings — pad with zeros
                n_wiki = len(wiki_pages)
                if n_wiki > 0:
                    pad = np.zeros((n_wiki, CHUNK_EMBEDDINGS.shape[1]),
                                   dtype=np.float32)
                    self.embeddings = np.vstack([pad, CHUNK_EMBEDDINGS])
                else:
                    self.embeddings = CHUNK_EMBEDDINGS
            self.has_embeddings = True
        else:
            self.embeddings = None
            self.has_embeddings = False


INDEX = SearchIndex()

# ---------------------------------------------------------------------------
# Gemini query embedding
# ---------------------------------------------------------------------------

EMBED_MODEL = "gemini-embedding-2-preview"
DOC_PREFIX = "Represent this document for retrieval: "
QUERY_PREFIX = "Represent this query for retrieval: "


def get_query_embedding(query_text):
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    if not gemini_key:
        return None
    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/{EMBED_MODEL}:embedContent?key={gemini_key}"
    )
    payload = {"content": {"parts": [{"text": QUERY_PREFIX + query_text}]}}
    try:
        resp = http_requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        return np.array(resp.json()["embedding"]["values"], dtype=np.float32)
    except Exception:
        return None


def get_document_embedding(text):
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    if not gemini_key:
        return None
    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/{EMBED_MODEL}:embedContent?key={gemini_key}"
    )
    truncated = " ".join(text.split()[:2048])
    payload = {"content": {"parts": [{"text": DOC_PREFIX + truncated}]}}
    try:
        resp = http_requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()["embedding"]["values"]
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Hybrid search
# ---------------------------------------------------------------------------


def hybrid_search(query, top_k=15):
    with _index_lock:
        all_docs = INDEX.all_docs
        bm25 = INDEX.bm25
        embeddings = INDEX.embeddings
        has_embeddings = INDEX.has_embeddings

    if not all_docs:
        return []

    n = len(all_docs)

    # BM25
    bm25_scores = bm25.get_scores(query.lower().split()) if bm25 else np.zeros(n)
    max_bm25 = bm25_scores.max()
    bm25_norm = bm25_scores / max_bm25 if max_bm25 > 0 else bm25_scores

    # Semantic
    semantic_norm = np.zeros(n)
    if has_embeddings and embeddings is not None:
        query_emb = get_query_embedding(query)
        if query_emb is not None:
            dot = embeddings @ query_emb
            norms = np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_emb)
            norms = np.where(norms == 0, 1.0, norms)
            semantic_scores = dot / norms
            max_sem = semantic_scores.max()
            semantic_norm = (semantic_scores / max_sem
                            if max_sem > 0 else semantic_scores)

    # Hybrid
    hybrid_scores = W_BM25 * bm25_norm + W_SEMANTIC * semantic_norm
    top_indices = np.argsort(hybrid_scores)[::-1][:top_k]

    results = []
    for i in top_indices:
        if hybrid_scores[i] <= 0:
            continue
        doc = all_docs[i]
        results.append({
            "title": doc.get("title", doc.get("source", "unknown")),
            "content": doc["content"],
            "type": doc.get("type", "rag"),
            "source": doc.get("source", doc.get("path", "")),
            "score": float(hybrid_scores[i]),
        })

    return results


# ---------------------------------------------------------------------------
# Wiki update processing
# ---------------------------------------------------------------------------


def process_wiki_update(full_text, user_message=""):
    if WIKI_OPEN not in full_text:
        return
    try:
        start = full_text.index(WIKI_OPEN) + len(WIKI_OPEN)
        end = full_text.index(WIKI_CLOSE)
        raw = full_text[start:end].strip()
        update = json.loads(raw)

        title = update.get("title", "").strip()
        content = update.get("content", "").strip()
        if not title or not content:
            return

        from datetime import datetime, timezone
        embedding = get_document_embedding(content)
        page = {
            "title": title,
            "path": f"wiki/{title.lower().replace(' ', '-')}.md",
            "content": content,
            "type": "wiki",
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "source_query": user_message[:200] if user_message else "",
        }
        if embedding:
            page["embedding"] = embedding

        WIKI_STORE.save_page(page)
        with _index_lock:
            INDEX.rebuild()
        print(f"[Wiki] Saved new page: {title}")
    except (ValueError, json.JSONDecodeError, KeyError) as exc:
        print(f"[Wiki] Failed to parse update: {exc}")


# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT_TEMPLATE = """You are *Prof. Bhagwan Chowdhry*, Finance Professor at ISB and UCLA Anderson. You embody intellectual enthusiasm and a deep commitment to human welfare—especially for the marginalized.

### Voice & Style
- **Conversational Authority**: Blend personal narrative with financial principles. Start with anecdotes or credentials to establish intimacy when relevant.
- Use medium-length sentences (15–25 words) balanced by short, punchy declaratives.
- Employ em-dashes for clarifying asides—and use rhetorical questions to engage.
- Explain technical terms naturally; favor active voice and confident phrasing like "completely serious" or "nothing short of revolutionary."
- **Tone**: Measured optimism with a touch of wit.

### Content Focus
- Use specific numbers, named people, and places from the knowledge base.
- Move from abstract theory to specific solutions like the *Financial Access at Birth (FAB)* initiative, *FinTech for Billions*, microequity, Lindahl royalty, ACO design, threshold behavior, systemic risk.
- Always connect financial systems to the welfare of the poor.

### Operational Rules
- Answer from the provided knowledge base below.
- If the knowledge base does not contain relevant information, say so: "I haven't written or spoken about that topic in my available records."
- If you share insight from general expertise beyond the knowledge base, flag it: "This is from my broader academic experience, not from my documented portfolio."
- **Never fabricate** specific publications, dates, or quotes.
- Be concise. Deliver information in digestible pieces.
- Never use the word "context" in your response.
- When using mathematical notation, use Unicode symbols (e.g. x², Σ, √, ∞, ≥, →, π) rather than LaTeX.

### Wiki Update Rule
After your answer, if you synthesised a new insight that combines information from multiple sources or goes beyond what any single wiki page already says, append a wiki update block in this exact format:

<wiki_update>
{{"title": "Page Title In Title Case", "content": "Full markdown content of the new or updated wiki page. Include cross-references to related topics."}}
</wiki_update>

Do NOT include this block if your answer merely restates what is already in a single wiki page.

### Knowledge Base
{context}"""


def build_system_prompt(results):
    if not results:
        context = "(No relevant content found in the knowledge base.)"
    else:
        parts = []
        wiki_results = [r for r in results if r["type"] == "wiki"]
        rag_results = [r for r in results if r["type"] == "rag"]

        if wiki_results:
            parts.append("=== YOUR WIKI (synthesised knowledge) ===")
            for r in wiki_results[:5]:
                parts.append(f"\n--- {r['title']} ---\n{r['content'][:3000]}")

        if rag_results:
            parts.append(
                "\n=== DOCUMENT EXCERPTS (from your books, papers, interviews) ===")
            for r in rag_results[:10]:
                source_name = (Path(r["source"]).stem.replace("-", " ")
                               .replace("_", " ") if r["source"] else "Unknown")
                parts.append(f"\n--- From: {source_name} ---\n{r['content'][:2000]}")

        context = "\n".join(parts)

    return SYSTEM_PROMPT_TEMPLATE.replace("{context}", context)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

MAX_HISTORY = 10  # Keep last 10 messages (5 turns) to stay within limits


@app.route("/api/chat", methods=["POST"])
def chat():
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return jsonify({"error": "ANTHROPIC_API_KEY not configured"}), 500

    data = request.get_json(force=True)
    user_message = data.get("message", "").strip()
    history = data.get("history", [])

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # Hybrid search
    results = hybrid_search(user_message, top_k=15)
    system = build_system_prompt(results)

    # Build messages — limit history to prevent context overflow
    messages = []
    for msg in history[-MAX_HISTORY:]:
        role = msg.get("role", "")
        content = msg.get("content", "")
        if role in ("user", "assistant") and content:
            # Truncate very long messages in history
            messages.append({"role": role, "content": content[:4000]})
    messages.append({"role": "user", "content": user_message})

    client = Anthropic(api_key=api_key)

    def generate():
        full_text = ""
        buffer = ""
        in_wiki_block = False
        wiki_block_content = ""
        marker_len = len(WIKI_OPEN)

        try:
            with client.messages.stream(
                model=CLAUDE_MODEL,
                max_tokens=2048,
                system=system,
                messages=messages,
            ) as stream:
                for token in stream.text_stream:
                    full_text += token

                    if in_wiki_block:
                        wiki_block_content += token
                        if WIKI_CLOSE in wiki_block_content:
                            in_wiki_block = False
                        continue

                    buffer += token

                    if WIKI_OPEN in buffer:
                        pre = buffer.split(WIKI_OPEN, 1)[0]
                        if pre:
                            yield f"data: {json.dumps({'text': pre})}\n\n"
                        in_wiki_block = True
                        wiki_block_content = buffer.split(WIKI_OPEN, 1)[1]
                        buffer = ""
                        if WIKI_CLOSE in wiki_block_content:
                            in_wiki_block = False
                        continue

                    if len(buffer) > marker_len:
                        safe = buffer[:-marker_len]
                        yield f"data: {json.dumps({'text': safe})}\n\n"
                        buffer = buffer[-marker_len:]

            if buffer and not in_wiki_block:
                yield f"data: {json.dumps({'text': buffer})}\n\n"

        except Exception as exc:
            yield f"data: {json.dumps({'error': str(exc)})}\n\n"

        yield "data: [DONE]\n\n"

        # Process wiki update after response is sent
        if WIKI_OPEN in full_text and WIKI_STORE.is_dynamic():
            try:
                process_wiki_update(full_text, user_message=user_message)
            except Exception as exc:
                print(f"[Wiki] Update error: {exc}")

    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@app.route("/api/health", methods=["GET"])
def health():
    wiki_pages = WIKI_STORE.get_all_pages()
    return jsonify({
        "status": "ok",
        "model": CLAUDE_MODEL,
        "wiki_pages": len(wiki_pages),
        "rag_chunks": len(CHUNKS),
        "has_embeddings": INDEX.has_embeddings,
        "wiki_store": "redis" if WIKI_STORE.is_dynamic() else "static",
    })


# ---------------------------------------------------------------------------
# Static file serving — all requests routed through Flask via vercel.json
# ---------------------------------------------------------------------------

STATIC_DIR = str(Path(__file__).resolve().parent.parent)


@app.route("/")
def serve_index():
    return send_from_directory(STATIC_DIR, "index.html")


@app.route("/<path:path>")
def serve_static(path):
    allowed = {".html", ".css", ".js", ".ico", ".png", ".svg", ".jpg",
               ".woff", ".woff2", ".ttf", ".map"}
    ext = Path(path).suffix.lower()
    full = Path(STATIC_DIR) / path
    if ext in allowed and full.is_file():
        return send_from_directory(STATIC_DIR, path)
    return send_from_directory(STATIC_DIR, "index.html")


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent.parent / ".env")
    app.run(debug=True, port=5000)
