export default function Header({ mode, filepath, onMenuClick }) {
  const accent = mode === "agent" ? "text-amber" : "text-teal";
  const label = mode === "agent" ? "Agent mode" : "Document mode";

  return (
    <header className="flex items-center justify-between border-b border-border bg-ink px-4 py-3 sm:px-6">
      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={onMenuClick}
          aria-label="Open menu"
          className="rounded-sm border border-border p-1.5 text-textHi lg:hidden"
        >
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M2 4h12M2 8h12M2 12h12" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
          </svg>
        </button>
        <div>
          <p className={`text-sm font-medium ${accent}`}>{label}</p>
          {mode === "rag" && (
            <p className="max-w-[220px] truncate text-[11px] text-textLo sm:max-w-xs">
              {filepath || "No document path set"}
            </p>
          )}
        </div>
      </div>
    </header>
  );
}
