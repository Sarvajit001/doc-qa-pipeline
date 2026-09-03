export function shortId(id) {
  if (!id) return "";
  return id.length > 10 ? `${id.slice(0, 8)}…` : id;
}

export function newSessionId() {
  if (crypto?.randomUUID) return crypto.randomUUID();
  return `sess-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

// The history endpoint's exact shape depends on pipeline.get_history().
// Normalize a few likely shapes into a flat [{role, content}] list so the
// UI doesn't break if that shape changes.
export function normalizeHistory(payload) {
  const raw = payload?.history ?? payload;
  if (!Array.isArray(raw)) return [];

  const messages = [];
  for (const entry of raw) {
    if (entry && typeof entry === "object" && "question" in entry && "answer" in entry) {
      messages.push({ role: "user", content: entry.question });
      messages.push({ role: "assistant", content: entry.answer });
    } else if (entry && typeof entry === "object" && "role" in entry && "content" in entry) {
      messages.push({ role: entry.role, content: entry.content });
    } else if (typeof entry === "string") {
      messages.push({ role: "assistant", content: entry });
    }
  }
  return messages;
}

export function timeNow() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}
