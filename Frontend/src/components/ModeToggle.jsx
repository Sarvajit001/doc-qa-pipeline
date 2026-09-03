const MODES = [
  {
    id: "rag",
    label: "Document mode",
    hint: "Answers only from the file you point it to.",
    accent: "teal",
  },
  {
    id: "agent",
    label: "Agent mode",
    hint: "Searches tools and can act to find an answer.",
    accent: "amber",
  },
];

export default function ModeToggle({ mode, onChange }) {
  return (
    <div className="space-y-2">
      {MODES.map((m) => {
        const active = mode === m.id;
        const accentClasses =
          m.accent === "teal"
            ? active
              ? "border-teal bg-teal/10"
              : "border-border"
            : active
            ? "border-amber bg-amber/10"
            : "border-border";
        const dotClasses = m.accent === "teal" ? "bg-teal" : "bg-amber";

        return (
          <button
            key={m.id}
            type="button"
            onClick={() => onChange(m.id)}
            aria-pressed={active}
            className={`w-full text-left rounded-md border ${accentClasses} px-3 py-2.5 transition-colors hover:border-textLo/50`}
          >
            <div className="flex items-center gap-2">
              <span
                className={`h-1.5 w-1.5 rounded-full ${active ? dotClasses : "bg-textLo/40"}`}
              />
              <span className="text-sm font-medium text-textHi">{m.label}</span>
            </div>
            <p className="mt-1 text-xs leading-snug text-textLo">{m.hint}</p>
          </button>
        );
      })}
    </div>
  );
}
