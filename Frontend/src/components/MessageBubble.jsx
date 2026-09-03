function TypingDots() {
  return (
    <span className="inline-flex items-center gap-1 py-1">
      {[0, 1, 2].map((i) => (
        <span
          key={i}
          className="h-1.5 w-1.5 rounded-full bg-textLo animate-blink"
          style={{ animationDelay: `${i * 0.15}s` }}
        />
      ))}
    </span>
  );
}

export default function MessageBubble({ role, content, mode, isLoading, isError, timestamp }) {
  const isUser = role === "user";
  const accentDot = mode === "agent" ? "bg-amber" : "bg-teal";

  if (isUser) {
    return (
      <div className="flex justify-end animate-rise">
        <div className="max-w-[75%] rounded-lg rounded-tr-sm bg-paper px-4 py-2.5 text-[15px] leading-relaxed text-ink">
          {content}
        </div>
      </div>
    );
  }

  return (
    <div className="flex justify-start animate-rise">
      <div
        className={`max-w-[75%] rounded-lg rounded-tl-sm px-4 py-2.5 text-[15px] leading-relaxed ${
          isError
            ? "bg-rose/10 text-rose border border-rose/30"
            : "bg-panel2 text-textHi border border-border"
        }`}
      >
        <div className="mb-1 flex items-center gap-1.5">
          <span className={`h-1.5 w-1.5 rounded-full ${isError ? "bg-rose" : accentDot}`} />
          <span className="text-[11px] font-medium text-textLo">
            {isError ? "Folio couldn't answer" : "Folio"}
          </span>
          {timestamp && <span className="text-[11px] text-textLo/70">· {timestamp}</span>}
        </div>
        {isLoading ? <TypingDots /> : <div className="whitespace-pre-wrap">{content}</div>}
      </div>
    </div>
  );
}
