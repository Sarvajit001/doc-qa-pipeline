import { useState } from "react";
import ModeToggle from "./ModeToggle.jsx";
import { shortId } from "../utils.js";

export default function Sidebar({
  mode,
  onModeChange,
  filepath,
  onFilepathChange,
  sessionId,
  onNewSession,
  onClearHistory,
  onLoadHistory,
  busy,
  config,
  onSaveConfig,
}) {
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [baseUrl, setBaseUrl] = useState(config.baseUrl);
  const [apiKey, setApiKey] = useState(config.apiKey);

  function handleSaveSettings(e) {
    e.preventDefault();
    onSaveConfig({ baseUrl, apiKey });
    setSettingsOpen(false);
  }

  return (
    <div className="flex h-full flex-col">
      <div className="px-5 pb-5 pt-6">
        <h1 className="font-display text-2xl text-textHi">Folio</h1>
        <p className="mt-1 text-xs text-textLo">Ask a document, or send in an agent.</p>
      </div>

      <div className="flex-1 space-y-6 overflow-y-auto px-5 pb-5">
        <section>
          <h2 className="mb-2 text-xs font-medium text-textLo">Mode</h2>
          <ModeToggle mode={mode} onChange={onModeChange} />
        </section>

        {mode === "rag" && (
          <section>
            <h2 className="mb-2 text-xs font-medium text-textLo">Document path</h2>
            <input
              type="text"
              value={filepath}
              onChange={(e) => onFilepathChange(e.target.value)}
              placeholder="/data/reports/q3.pdf"
              className="w-full rounded-sm border border-border bg-panel2 px-3 py-2 text-sm text-textHi placeholder:text-textLo/60 focus:border-teal"
            />
            <p className="mt-1.5 text-[11px] text-textLo">
              A path the server can read. Supports .pdf, .docx, .xlsx, .txt.
            </p>
          </section>
        )}

        <section>
          <h2 className="mb-2 text-xs font-medium text-textLo">Session</h2>
          <div className="rounded-sm border border-border bg-panel2 px-3 py-2">
            <p className="text-xs text-textLo">
              ID <span className="text-textHi">{shortId(sessionId)}</span>
            </p>
          </div>
          <div className="mt-2 grid grid-cols-2 gap-2">
            <button
              type="button"
              onClick={onNewSession}
              className="rounded-sm border border-border py-1.5 text-xs text-textHi hover:bg-panel2"
            >
              New session
            </button>
            <button
              type="button"
              onClick={onLoadHistory}
              disabled={busy}
              className="rounded-sm border border-border py-1.5 text-xs text-textHi hover:bg-panel2 disabled:opacity-40"
            >
              Load history
            </button>
          </div>
          <button
            type="button"
            onClick={onClearHistory}
            disabled={busy}
            className="mt-2 w-full rounded-sm border border-rose/30 py-1.5 text-xs text-rose hover:bg-rose/10 disabled:opacity-40"
          >
            Clear history
          </button>
        </section>
      </div>

      <div className="border-t border-border px-5 py-4">
        <button
          type="button"
          onClick={() => setSettingsOpen((v) => !v)}
          className="flex w-full items-center justify-between text-xs text-textLo hover:text-textHi"
        >
          <span>Connection settings</span>
          <span>{settingsOpen ? "–" : "+"}</span>
        </button>

        {settingsOpen && (
          <form onSubmit={handleSaveSettings} className="mt-3 space-y-2">
            <div>
              <label className="mb-1 block text-[11px] text-textLo">API base URL</label>
              <input
                type="text"
                value={baseUrl}
                onChange={(e) => setBaseUrl(e.target.value)}
                placeholder="http://localhost:5000"
                className="w-full rounded-sm border border-border bg-panel2 px-2.5 py-1.5 text-xs text-textHi focus:border-teal"
              />
            </div>
            <div>
              <label className="mb-1 block text-[11px] text-textLo">API key</label>
              <input
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="X-API-Key"
                className="w-full rounded-sm border border-border bg-panel2 px-2.5 py-1.5 text-xs text-textHi focus:border-teal"
              />
            </div>
            <button
              type="submit"
              className="w-full rounded-sm bg-teal py-1.5 text-xs font-medium text-ink"
            >
              Save
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
