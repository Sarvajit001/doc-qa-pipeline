import { useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble.jsx";

function EmptyState({ mode }) {
  return (
    <div className="flex h-full flex-col items-center justify-center px-6 text-center">
      <div
        className={`mb-4 h-2 w-2 rounded-full ${mode === "agent" ? "bg-amber" : "bg-teal"}`}
      />
      <h2 className="font-display text-xl text-textHi">
        {mode === "agent" ? "Send in the agent" : "Ask about the document"}
      </h2>
      <p className="mt-2 max-w-sm text-sm text-textLo">
        {mode === "agent"
          ? "It can search tools, run them, and bring back an answer — no document required."
          : "Point Folio at a file in the sidebar, then ask anything about what's inside it."}
      </p>
    </div>
  );
}

export default function ChatPane({ messages, mode }) {
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages.length, messages[messages.length - 1]?.content]);

  if (messages.length === 0) return <EmptyState mode={mode} />;

  return (
    <div className="mx-auto flex w-full max-w-3xl flex-col gap-4 px-4 py-6 sm:px-6">
      {messages.map((m) => (
        <MessageBubble key={m.id} {...m} />
      ))}
      <div ref={endRef} />
    </div>
  );
}
