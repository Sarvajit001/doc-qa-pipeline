import { useState } from "react";
import Sidebar from "./components/Sidebar.jsx";
import Header from "./components/Header.jsx";
import ChatPane from "./components/ChatPane.jsx";
import Composer from "./components/Composer.jsx";
import { api, getConfig, saveConfig } from "./api.js";
import { newSessionId, normalizeHistory, timeNow } from "./utils.js";

export default function App() {
  const [mode, setMode] = useState("rag");
  const [filepath, setFilepath] = useState("");
  const [sessionId, setSessionId] = useState(newSessionId());
  const [messages, setMessages] = useState([]);
  const [busy, setBusy] = useState(false);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [config, setConfig] = useState(getConfig());

  function pushMessage(msg) {
    setMessages((prev) => [...prev, { id: crypto.randomUUID(), ...msg }]);
  }

  function updateMessage(id, patch) {
    setMessages((prev) => prev.map((m) => (m.id === id ? { ...m, ...patch } : m)));
  }

  async function handleSend(question) {
    if (mode === "rag" && !filepath.trim()) {
      pushMessage({
        role: "assistant",
        content: "Add a document path in the sidebar before asking a question.",
        mode,
        isError: true,
        timestamp: timeNow(),
      });
      return;
    }

    pushMessage({ role: "user", content: question, mode });
    const loadingId = crypto.randomUUID();
    setMessages((prev) => [
      ...prev,
      { id: loadingId, role: "assistant", content: "", mode, isLoading: true },
    ]);
    setBusy(true);

    try {
      const data =
        mode === "rag"
          ? await api.ask(question, filepath.trim(), sessionId)
          : await api.agentAsk(question, filepath.trim() || undefined, sessionId);

      updateMessage(loadingId, {
        content: data.answer,
        isLoading: false,
        timestamp: timeNow(),
      });
    } catch (err) {
      updateMessage(loadingId, {
        content: err.message,
        isLoading: false,
        isError: true,
        timestamp: timeNow(),
      });
    } finally {
      setBusy(false);
    }
  }

  function handleNewSession() {
    setSessionId(newSessionId());
    setMessages([]);
  }

  async function handleClearHistory() {
    setBusy(true);
    try {
      await api.clearHistory(sessionId);
      setMessages([]);
    } catch (err) {
      pushMessage({ role: "assistant", content: err.message, mode, isError: true, timestamp: timeNow() });
    } finally {
      setBusy(false);
    }
  }

  async function handleLoadHistory() {
    setBusy(true);
    try {
      const data = await api.getHistory(sessionId);
      const restored = normalizeHistory(data).map((m) => ({
        id: crypto.randomUUID(),
        mode,
        timestamp: timeNow(),
        ...m,
      }));
      setMessages(restored);
    } catch (err) {
      pushMessage({ role: "assistant", content: err.message, mode, isError: true, timestamp: timeNow() });
    } finally {
      setBusy(false);
    }
  }

  function handleSaveConfig(next) {
    saveConfig(next);
    setConfig(next);
  }

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-ink text-textHi">
      {/* Desktop sidebar */}
      <aside className="hidden w-72 shrink-0 border-r border-border bg-panel lg:flex">
        <Sidebar
          mode={mode}
          onModeChange={setMode}
          filepath={filepath}
          onFilepathChange={setFilepath}
          sessionId={sessionId}
          onNewSession={handleNewSession}
          onClearHistory={handleClearHistory}
          onLoadHistory={handleLoadHistory}
          busy={busy}
          config={config}
          onSaveConfig={handleSaveConfig}
        />
      </aside>

      {/* Mobile drawer */}
      {drawerOpen && (
        <div className="fixed inset-0 z-40 flex lg:hidden">
          <div
            className="absolute inset-0 bg-black/50"
            onClick={() => setDrawerOpen(false)}
            aria-hidden="true"
          />
          <div className="relative z-10 h-full w-72 bg-panel">
            <Sidebar
              mode={mode}
              onModeChange={(m) => {
                setMode(m);
                setDrawerOpen(false);
              }}
              filepath={filepath}
              onFilepathChange={setFilepath}
              sessionId={sessionId}
              onNewSession={handleNewSession}
              onClearHistory={handleClearHistory}
              onLoadHistory={handleLoadHistory}
              busy={busy}
              config={config}
              onSaveConfig={handleSaveConfig}
            />
          </div>
        </div>
      )}

      <div className="flex min-w-0 flex-1 flex-col">
        <Header mode={mode} filepath={filepath} onMenuClick={() => setDrawerOpen(true)} />
        <main className="min-h-0 flex-1 overflow-y-auto">
          <ChatPane messages={messages} mode={mode} />
        </main>
        <Composer mode={mode} disabled={busy} onSend={handleSend} />
      </div>
    </div>
  );
}
