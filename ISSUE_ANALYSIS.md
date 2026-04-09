# Issue Analysis — Logging Failure + Prompt Conflicts

**Date**: 10 April 2026  
**Status**: CRITICAL — Production broken

---

## Issue 1: Logging Fails in Production (Vercel)

### Error
```
[Log] Failed to write log: [Errno 2] No such file or directory: 
'/var/prof-bhagwan-hybrid-demo/wiki/log.md'
```

### Root Cause
1. **Filesystem doesn't exist on Vercel**: Vercel's cloud runtime has ephemeral filesystem storage
2. **Path construction wrong for serverless**: `DATA_DIR.parent / "prof-bhagwan-hybrid-demo"` resolves incorrectly
3. **No fallback to Redis**: Code tries filesystem-only, no graceful degradation to Redis/Upstash

### Current Code (webapp/api/index.py line 735)
```python
log_path = DATA_DIR.parent / "prof-bhagwan-hybrid-demo" / "wiki" / "log.md"
```

### Why It Fails
- Local: `DATA_DIR = .../prof-bhagwan-hybrid-demo/data` → path works ✓
- Vercel: `DATA_DIR = /var/task/data` (app runs from /var/task/) → parent becomes `/var`, then adds `prof-bhagwan-hybrid-demo`, results in bad path ✗

### Solution
Replace filesystem logging with **Redis-first fallback to stdout**:
```python
def log_to_wiki_log(operation, description, metadata=None):
    """Log to Redis first, fallback to stdout for serverless."""
    # Try Redis if available
    kv_url = os.environ.get("KV_REST_API_URL", "")
    kv_token = os.environ.get("KV_API_TOKEN", "")
    
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "operation": operation,
        "description": description,
        "metadata": metadata or {}
    }
    
    if kv_url and kv_token:
        # Store in Redis
        try:
            # ... redis store logic
        except:
            print(f"[Log] {json.dumps(log_entry)}")  # Fallback to stdout
    else:
        # Serverless environment, just log to stdout
        print(f"[Log] {json.dumps(log_entry)}")
```

---

## Issue 2: Prompt Conflicts & Redundancy

### Three System Prompts Found

#### A. WIKI_LLM_SYSTEM_PROMPT (line 507)
- **Purpose**: Wiki search specialist
- **Output**: JSON only, no markdown
- **Key Rule**: "Do NOT use theatrical formatting like *laughs*"
- **Confidence**: Low/Medium/High

#### B. REPLY_LLM_SYSTEM_PROMPT (line 530)
- **Purpose**: Prof. Bhagwan synthesis (wiki + RAG)
- **Output**: JSON only
- **Key Rule**: "Speak directly — NO theatrical formatting like *laughs*"
- **Sources**: Tracks wiki vs RAG origins
- **Wiki Update**: Recommends when synthesis warranted

#### C. SYSTEM_PROMPT_TEMPLATE (line 823) — **OBSOLETE?**
- **Purpose**: Old v1 endpoint system prompt
- **Output**: Free-form text (NOT JSON)
- **Key Rule**: Vague — "embed naturally in language, not in asterisks"
- **Wiki Update**: Includes wiki_update format rules
- **ISSUE**: Doesn't have explicit "*laughs*" prohibition like others

### Conflicts
| Aspect | WIKI_LLM | REPLY_LLM | SYSTEM_TEMPLATE |
|--------|----------|-----------|-----------------|
| **Output Format** | JSON only | JSON only | Free text |
| **Theatrical Formatting** | ❌ Explicitly forbidden | ❌ Explicitly forbidden | ⚠️ Vague |
| **Wiki Updates** | Not mentioned | Yes, with rules | Yes, with detailed format |
| **Voice** | Not applicable | Prof. Bhagwan | Prof. Bhagwan |

### Redundancy
- WIKI_LLM and REPLY_LLM both say "NO *laughs*" but with slightly different emphasis
- SYSTEM_PROMPT_TEMPLATE repeats similar voice guidance as REPLY_LLM
- Wiki update rules appear twice (slightly different formatting)

### "laughs warmly" Issue
**In production screenshot**: Response contains plain English "laughs warmly" which:
1. Violates the explicit "*laughs*" prohibition in WIKI_LLM and REPLY_LLM
2. Suggests SYSTEM_PROMPT_TEMPLATE is being used (lacks explicit prohibition)
3. Indicates v1 endpoint being called (not v2 with REPLY_LLM)

### Recommendation
1. **Phase out SYSTEM_PROMPT_TEMPLATE** — move to v2 endpoint fully
2. **Consolidate theatrical formatting rules** — one clear statement
3. **Enforce JSON output** — ensure all responses parse correctly

---

## Issue 3: The "laughs warmly" Problem

### What's Happening
The response contains theatrical language ("laughs warmly") which indicates either:
1. **API v1 is still active** (using SYSTEM_PROMPT_TEMPLATE)
2. **Prompt isn't being enforced** (Claude ignoring instructions)
3. **Response parsing is broken** (theatrical text leaking into output)

### Why This Violates the Prompt
```
REPLY_LLM_SYSTEM_PROMPT explicitly states:
"Speak directly — NO theatrical formatting like *laughs*, *leans forward*, or stage directions"

Examples:
❌ "*laughs* That's a great question"
✅ "That's genuinely fascinating"
```

### Status
- ❌ Production shows "laughs warmly" in responses
- ❌ Contradicts v2 prompt instructions
- ❌ Logs show [Log] Fail entries

---

## Action Items (Priority)

1. **CRITICAL**: Fix logging to use Redis + stdout fallback
2. **HIGH**: Remove "laughs warmly" from responses by ensuring v2 endpoint is used
3. **MEDIUM**: Consolidate prompts to eliminate redundancy
4. **MEDIUM**: Verify no SYSTEM_PROMPT_TEMPLATE calls

---

## Files to Modify

- `webapp/api/index.py`: Lines 735–759 (log_to_wiki_log function)
- `webapp/api/index.py`: Lines 507–600 (WIKI_LLM + REPLY_LLM consolidation)
- `webapp/api/index.py`: Lines 823+ (SYSTEM_PROMPT_TEMPLATE — mark for deprecation)
- `tests/test_comprehensive.py`: Add test for logging Redis fallback

