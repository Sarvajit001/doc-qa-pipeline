import { useRef, useState } from "react";

export default function Composer({ mode, disabled, onSend }) {
  const [value, setValue] = useState("");
  const ref = useRef(null);

  const accent = mode === "agent" ? "focus-within:border-amber" : "focus-within:border-teal";
  const buttonAccent = mode === "agent" ? "bg-amber text-ink" : "bg-teal text-ink";

  function handleSubmit(e) {
    e.preventDefault();
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setValue("");
    requestAnimationFrame(() => ref.current?.focus());
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="border-t border-border bg-ink px-4 py-3 sm:px-6">
      <div
        className={`flex items-end gap-2 rounded-md border border-border bg-panel2 px-3 py-2 transition-colors ${accent}`}
      >
        <textarea
          ref={ref}
          rows={1}
          value={value}
          disabled={disabled}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={
            mode === "agent"
              ? "Ask something the agent can look up or act on…"
              : "Ask something about the document…"
          }
          className="max-h-40 flex-1 resize-none bg-transparent text-[15px] text-textHi placeholder:text-textLo/70 focus:outline-none disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={disabled || !value.trim()}
          className={`shrink-0 rounded-sm px-3.5 py-1.5 text-sm font-medium transition-opacity ${buttonAccent} disabled:opacity-30`}
        >
          Send
        </button>
      </div>
      <p className="mt-1.5 text-[11px] text-textLo">Enter to send · Shift + Enter for a new line</p>
    </form>
  );
}
