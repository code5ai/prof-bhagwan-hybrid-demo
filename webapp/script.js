/**
 * Prof. Bhagwan Chowdhry — Knowledge Chatbot
 * Client-side chat logic with SSE streaming
 */

const chatContainer = document.getElementById("chat-container");
const messageInput = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");
const statusText = document.getElementById("status-text");
const statusDot = document.querySelector(".status-dot");

let conversationHistory = [];
let isStreaming = false;

// Configure marked for safe rendering
marked.setOptions({
  breaks: true,
  gfm: true,
});

// Strip wiki_update blocks from displayed text (safety net — backend buffers these)
function stripWikiBlocks(text) {
  return text.replace(/<wiki_update>[\s\S]*?<\/wiki_update>/g, "").trimEnd();
}

// ---- Auto-resize textarea ----
messageInput.addEventListener("input", () => {
  messageInput.style.height = "auto";
  messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + "px";
});

// Enter to send, Shift+Enter for newline
messageInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    if (!isStreaming) handleSubmit();
  }
});

// ---- Suggestion chips ----
function sendSuggestion(btn) {
  if (isStreaming) return;
  messageInput.value = btn.textContent;
  handleSubmit();
}

// ---- Submit handler ----
function handleSubmit(e) {
  if (e) e.preventDefault();
  const text = messageInput.value.trim();
  if (!text || isStreaming) return;

  // Remove welcome message
  const welcome = chatContainer.querySelector(".welcome-message");
  if (welcome) welcome.remove();

  // Add user message
  appendMessage("user", text);
  conversationHistory.push({ role: "user", content: text });

  // Clear input
  messageInput.value = "";
  messageInput.style.height = "auto";

  // Stream response
  streamResponse(text);
}

// ---- Append a message to chat ----
function appendMessage(role, content) {
  const msg = document.createElement("div");
  msg.className = `message ${role === "user" ? "user" : "bot"}`;

  const avatar = document.createElement("div");
  avatar.className = "message-avatar";
  avatar.textContent = role === "user" ? "You" : "BC";

  const bubble = document.createElement("div");
  bubble.className = "message-bubble";

  if (role === "user") {
    bubble.textContent = content;
  } else {
    bubble.innerHTML = marked.parse(content);
  }

  msg.appendChild(avatar);
  msg.appendChild(bubble);
  chatContainer.appendChild(msg);
  scrollToBottom();

  return bubble;
}

// ---- Show thinking indicator ----
function showThinking() {
  const msg = document.createElement("div");
  msg.className = "message bot";
  msg.id = "thinking-msg";

  const avatar = document.createElement("div");
  avatar.className = "message-avatar";
  avatar.textContent = "BC";

  const bubble = document.createElement("div");
  bubble.className = "message-bubble";
  bubble.innerHTML = `<div class="thinking-dots"><span></span><span></span><span></span></div>`;

  msg.appendChild(avatar);
  msg.appendChild(bubble);
  chatContainer.appendChild(msg);
  scrollToBottom();
}

function removeThinking() {
  const el = document.getElementById("thinking-msg");
  if (el) el.remove();
}

// ---- Stream response from backend ----
async function streamResponse(userMessage) {
  isStreaming = true;
  sendBtn.disabled = true;
  setStatus("Thinking…", true);
  showThinking();

  let fullText = "";
  let bubble = null;

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: userMessage,
        history: conversationHistory.slice(-20),
      }),
    });

    if (!response.ok) {
      const err = await response.json().catch(() => ({}));
      throw new Error(err.error || `Server error (${response.status})`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    removeThinking();
    bubble = appendMessage("bot", "");

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });

      // Process complete SSE lines
      const lines = buffer.split("\n");
      buffer = lines.pop(); // keep incomplete line in buffer

      for (const line of lines) {
        if (!line.startsWith("data: ")) continue;
        const data = line.slice(6).trim();

        if (data === "[DONE]") continue;

        try {
          const parsed = JSON.parse(data);
          if (parsed.error) {
            fullText += `\n\n*Error: ${parsed.error}*`;
          } else if (parsed.text) {
            fullText += parsed.text;
          }
        } catch {
          // skip malformed lines
        }
      }

      // Render accumulated markdown (strip wiki blocks)
      bubble.innerHTML = marked.parse(stripWikiBlocks(fullText));
      scrollToBottom();
    }

    // Save assistant response to history (strip wiki blocks)
    const cleanText = stripWikiBlocks(fullText);
    if (cleanText.trim()) {
      conversationHistory.push({ role: "assistant", content: cleanText });
    }
  } catch (err) {
    removeThinking();
    appendMessage("bot", `*Something went wrong: ${err.message}*`);
  } finally {
    isStreaming = false;
    sendBtn.disabled = false;
    setStatus("Ready", false);
    messageInput.focus();
  }
}

// ---- Helpers ----
function scrollToBottom() {
  requestAnimationFrame(() => {
    chatContainer.scrollTop = chatContainer.scrollHeight;
  });
}

function setStatus(text, thinking) {
  statusText.textContent = text;
  if (thinking) {
    statusDot.classList.add("thinking");
  } else {
    statusDot.classList.remove("thinking");
  }
}

// ---- Initial health check ----
async function checkHealth() {
  try {
    const resp = await fetch("/api/health");
    const data = await resp.json();
    if (data.wiki_pages === 0 && data.rag_chunks === 0) {
      setStatus("No data loaded", false);
    }
  } catch {
    // Backend not available — that's fine during local dev startup
  }
}

checkHealth();
