// Thin client for the Flask backend in app.py.
// Endpoints: POST /ask, POST /agent, GET /history/:id, DELETE /clear/:id
// Auth: every route is behind @require_api_key, sent as the X-API-Key header.

const DEFAULTS = {
  baseUrl: import.meta.env.VITE_API_URL || "http://localhost:5000",
  apiKey: import.meta.env.VITE_API_KEY || "",
};

export function getConfig() {
  return {
    baseUrl: localStorage.getItem("folio.baseUrl") || DEFAULTS.baseUrl,
    apiKey: localStorage.getItem("folio.apiKey") || DEFAULTS.apiKey,
  };
}

export function saveConfig({ baseUrl, apiKey }) {
  if (baseUrl !== undefined) localStorage.setItem("folio.baseUrl", baseUrl);
  if (apiKey !== undefined) localStorage.setItem("folio.apiKey", apiKey);
}

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

async function request(path, options = {}) {
  const { baseUrl, apiKey } = getConfig();
  if (!baseUrl) throw new ApiError("No API base URL is set. Add one in Settings.", 0);

  let res;
  try {
    res = await fetch(`${baseUrl}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": apiKey,
        ...(options.headers || {}),
      },
    });
  } catch (err) {
    throw new ApiError(
      `Couldn't reach ${baseUrl}. Is the Flask server running?`,
      0
    );
  }

  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    throw new ApiError(data.error || `Request failed (${res.status})`, res.status);
  }
  return data;
}

export const api = {
  ask: (question, filepath, sessionId) =>
    request("/ask", {
      method: "POST",
      body: JSON.stringify({ question, filepath, session_id: sessionId }),
    }),

  agentAsk: (question, filepath, sessionId) =>
    request("/agent", {
      method: "POST",
      body: JSON.stringify({ question, filepath, session_id: sessionId }),
    }),

  getHistory: (sessionId) => request(`/history/${sessionId}`, { method: "GET" }),

  clearHistory: (sessionId) => request(`/clear/${sessionId}`, { method: "DELETE" }),
};

export { ApiError };
