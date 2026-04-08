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
            self._pages = json.loads(p.read_text(encoding="utf-8"))
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
            self._redis_set(self.WIKI_KEY, json.dumps(pages))
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
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return []


# RAG chunks — static, bundled at deploy time (text only, no embeddings)
CHUNKS = _load_json(DATA_DIR / "chunks.json")

# Chunk embeddings — stored as numpy binary to avoid 352MB JSON bloat
_CHUNK_EMB_PATH = DATA_DIR / "chunks_embeddings.npy"
CHUNK_EMBEDDINGS = None
if _CHUNK_EMB_PATH.exists():
    CHUNK_EMBEDDINGS = np.load(str(_CHUNK_EMB_PATH))
    print(f"[Data] Loaded chunk embeddings: {CHUNK_EMBEDDINGS.shape}")

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

        # Build embedding matrix: wiki page embeddings (from JSON) +
        # chunk embeddings (from numpy binary file)
        wiki_embs = [p["embedding"] for p in wiki_pages if "embedding" in p]

        if CHUNK_EMBEDDINGS is not None and len(CHUNK_EMBEDDINGS) == len(CHUNKS):
            if wiki_embs:
                wiki_arr = np.array(wiki_embs, dtype=np.float32)
                self.embeddings = np.vstack([wiki_arr, CHUNK_EMBEDDINGS])
            else:
                # Wiki pages have no embeddings (e.g. fresh Redis with no embeddings)
                # Use chunks only, pad wiki positions with zeros
                pad = np.zeros((len(wiki_pages), CHUNK_EMBEDDINGS.shape[1]), dtype=np.float32)
                self.embeddings = np.vstack([pad, CHUNK_EMBEDDINGS]) if wiki_pages else CHUNK_EMBEDDINGS
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
    """Get embedding from gemini-embedding-2-preview for a search query."""
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    if not gemini_key:
        return None

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/{EMBED_MODEL}:embedContent?key={gemini_key}"
    )
    payload = {
        "content": {"parts": [{"text": QUERY_PREFIX + query_text}]},
    }
    try:
        resp = http_requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        return np.array(resp.json()["embedding"]["values"], dtype=np.float32)
    except Exception:
        return None


def get_document_embedding(text):
    """Get embedding for a new wiki page (document-type)."""
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    if not gemini_key:
        return None

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/{EMBED_MODEL}:embedContent?key={gemini_key}"
    )
    truncated = " ".join(text.split()[:2048])
    payload = {
        "content": {"parts": [{"text": DOC_PREFIX + truncated}]},
    }
    try:
        resp = http_requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()["embedding"]["values"]
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Hybrid search: 92.4% semantic + 7.6% BM25
# ---------------------------------------------------------------------------

def hybrid_search(query, top_k=15):
    """Return top-k documents ranked by hybrid score."""
    with _index_lock:
        all_docs = INDEX.all_docs
        bm25 = INDEX.bm25
        embeddings = INDEX.embeddings
        has_embeddings = INDEX.has_embeddings

    if not all_docs:
        return []

    n = len(all_docs)

    # --- BM25 ---
    bm25_scores = bm25.get_scores(query.lower().split()) if bm25 else np.zeros(n)
    max_bm25 = bm25_scores.max()
    bm25_norm = bm25_scores / max_bm25 if max_bm25 > 0 else bm25_scores

    # --- Semantic ---
    semantic_norm = np.zeros(n)
    if has_embeddings and embeddings is not None:
        query_emb = get_query_embedding(query)
        if query_emb is not None:
            dot = embeddings @ query_emb
            norms = np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_emb)
            norms = np.where(norms == 0, 1.0, norms)
            semantic_scores = dot / norms
            max_sem = semantic_scores.max()
            semantic_norm = semantic_scores / max_sem if max_sem > 0 else semantic_scores

    # --- Hybrid ---
    hybrid_scores = W_BM25 * bm25_norm + W_SEMANTIC * semantic_norm
    top_indices = np.argsort(hybrid_scores)[::-1][:top_k]

    results = []
    for i in top_indices:
        if hybrid_scores[i] <= 0:
            continue
        results.append({
            "title": all_docs[i].get("title", all_docs[i].get("source", "unknown")),
            "content": all_docs[i]["content"],
            "type": all_docs[i].get("type", "rag"),
            "source": all_docs[i].get("source", all_docs[i].get("path", "")),
            "score": float(hybrid_scores[i]),
        })

    return results


# ---------------------------------------------------------------------------
# Wiki update processing
# ---------------------------------------------------------------------------

def process_wiki_update(full_text):
    """
    Parse <wiki_update> block from Claude's response.
    Save new wiki page to store with embedding. Rebuild search index.
    """
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

        # Generate embedding for the new page
        embedding = get_document_embedding(content)

        page = {
            "title": title,
            "path": f"wiki/{title.lower().replace(' ', '-')}.md",
            "content": content,
            "type": "wiki",
        }
        if embedding:
            page["embedding"] = embedding

        WIKI_STORE.save_page(page)

        # Rebuild search index
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
- **Tone**: Measured optimism with a touch of wit. Acknowledge limitations while asserting expertise.

### Content Focus
- Use specific numbers, named people, and places from the knowledge base.
- Move from abstract theory to specific solutions like the *Financial Access at Birth (FAB)* initiative, *FinTech for Billions*, microequity, Lindahl royalty, ACO design, threshold behavior, systemic risk.
- Always connect financial systems to the welfare of the poor. End with future-focused projections that inspire action.

### Operational Rules
- Answer from the provided knowledge base (wiki pages and document excerpts) below. This is your personal knowledge base containing your publications, interviews, research, and theoretical contributions.
- If the knowledge base does not contain relevant information, say so explicitly: "I haven't written or spoken about that topic in my available records."
- If you choose to share insight from your general expertise beyond the knowledge base, explicitly flag it: "This is from my broader academic experience, not from my documented portfolio."
- **Never fabricate** specific publications, dates, or quotes.
- Be concise. If an answer is long, deliver information in digestible pieces rather than a wall of text.
- Never use the word "context" in your response.

### Wiki Update Rule
After your answer, if you synthesised a new insight that combines information from multiple sources or goes beyond what any single wiki page already says, append a wiki update block in this exact format:

<wiki_update>
{{"title": "Page Title In Title Case", "content": "Full markdown content of the new or updated wiki page. Include cross-references to related topics."}}
</wiki_update>

Do NOT include this block if your answer merely restates what is already in a single wiki page. Only include it when you have genuinely synthesised or connected ideas in a novel way.

### Knowledge Base
The following wiki pages and document excerpts are from your personal knowledge base:

{context}"""


def build_system_prompt(results):
    """Build the system prompt with retrieved context."""
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
            parts.append("\n=== DOCUMENT EXCERPTS (from your books, papers, interviews) ===")
            for r in rag_results[:10]:
                source_name = Path(r["source"]).stem.replace("-", " ").replace("_", " ") if r["source"] else "Unknown"
                parts.append(f"\n--- From: {source_name} ---\n{r['content'][:2000]}")

        context = "\n".join(parts)

    return SYSTEM_PROMPT_TEMPLATE.replace("{context}", context)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Main chat endpoint — streams Claude's response via SSE.
    Uses a sliding buffer to intercept <wiki_update> blocks before they
    reach the client, then saves the update to the wiki store.
    """
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

    # Build prompt
    system = build_system_prompt(results)

    # Build messages (keep last 10 turns)
    messages = []
    for msg in history[-20:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
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
                model="claude-sonnet-4-6-20250514",
                max_tokens=2048,
                system=system,
                messages=messages,
            ) as stream:
                for token in stream.text_stream:
                    full_text += token

                    if in_wiki_block:
                        # Accumulate wiki content, don't send to client
                        wiki_block_content += token
                        if WIKI_CLOSE in wiki_block_content:
                            in_wiki_block = False
                        continue

                    buffer += token

                    # Check if we've entered a wiki block
                    if WIKI_OPEN in buffer:
                        # Send everything before the marker
                        pre = buffer.split(WIKI_OPEN, 1)[0]
                        if pre:
                            yield f"data: {json.dumps({'text': pre})}\n\n"
                        in_wiki_block = True
                        wiki_block_content = buffer.split(WIKI_OPEN, 1)[1]
                        buffer = ""
                        if WIKI_CLOSE in wiki_block_content:
                            in_wiki_block = False
                        continue

                    # Flush safe portion of buffer (keep last marker_len chars)
                    if len(buffer) > marker_len:
                        safe = buffer[:-marker_len]
                        yield f"data: {json.dumps({'text': safe})}\n\n"
                        buffer = buffer[-marker_len:]

            # Flush remaining buffer
            if buffer and not in_wiki_block:
                yield f"data: {json.dumps({'text': buffer})}\n\n"

        except Exception as exc:
            yield f"data: {json.dumps({'error': str(exc)})}\n\n"

        yield "data: [DONE]\n\n"

        # Process wiki update in background (after response is sent)
        if WIKI_OPEN in full_text and WIKI_STORE.is_dynamic():
            try:
                process_wiki_update(full_text)
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
    """Health check — shows wiki + RAG stats and store type."""
    wiki_pages = WIKI_STORE.get_all_pages()
    return jsonify({
        "status": "ok",
        "wiki_pages": len(wiki_pages),
        "rag_chunks": len(CHUNKS),
        "has_embeddings": INDEX.has_embeddings,
        "wiki_store": "redis" if WIKI_STORE.is_dynamic() else "static",
    })


# ---------------------------------------------------------------------------
# Static file serving — all requests routed through Flask on Vercel
# ---------------------------------------------------------------------------

# On Vercel: /var/task/api/index.py → parent.parent = /var/task/
# Locally:   webapp/api/index.py    → parent.parent = webapp/
STATIC_DIR = str(Path(__file__).resolve().parent.parent)


@app.route("/")
def serve_index():
    return send_from_directory(STATIC_DIR, "index.html")


@app.route("/<path:path>")
def serve_static(path):
    full = Path(STATIC_DIR) / path
    if full.is_file():
        return send_from_directory(STATIC_DIR, path)
    # SPA fallback
    return send_from_directory(STATIC_DIR, "index.html")


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent.parent / ".env")
    app.run(debug=True, port=5000)
