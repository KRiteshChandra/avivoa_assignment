import React, { useState, useRef, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { submitChat } from "../store/interactionsSlice";

function formatToolResponse(payload) {
  if (!payload) return "";
  if (payload.error) return `Error: ${payload.error}`;
  if (payload.response && typeof payload.response === "string") return payload.response;

  const { tool, result } = payload;
  if (!tool) return JSON.stringify(payload);

  switch (tool) {
    case "log_interaction":
      return `Logged interaction #${result.id} for ${result.hcp_name} (sentiment: ${result.sentiment}).`;
    case "edit_interaction":
      return `Updated interaction #${result.id} for ${result.hcp_name}.`;
    case "get_history":
      if (result.length === 0) return "No interactions found.";
      return result.map((r) => {
        let details = `#${r.id} — ${r.hcp_name} (${r.sentiment})\nTopic: ${r.topic}`;
        if (r.outcomes) details += `\nOutcomes: ${r.outcomes}`;
        if (r.followup) details += `\nFollow-up: ${r.followup}`;
        return details;
      }).join("\n\n");
    case "summarize":
      return `Summary: ${result.summary}`;
    case "suggest_followup":
      return `Suggestions:\n${result.suggestions}`;
    default:
      return JSON.stringify(result);
  }
}

export default function ChatInterface() {
  const dispatch = useDispatch();
  const { chatLog, loading } = useSelector((state) => state.interactions);
  const [input, setInput] = useState("");
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatLog]);

  const handleSend = async () => {
    if (!input.trim()) return;
    const text = input;
    setInput("");
    await dispatch(submitChat(text));
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="panel">
      <h2>AI Assistant</h2>
      <p className="hint">Log interactions in plain English, or ask to edit, summarize, or view history.</p>

      <div className="chat-window">
        {chatLog.length === 0 && (
          <div className="chat-placeholder">
            e.g. "Met Dr. Sharma, discussed insulin, he seemed interested"
          </div>
        )}
        {chatLog.map((msg, i) => (
          <div key={i} className={`chat-bubble ${msg.role}`}>
            {msg.role === "user" ? msg.content : formatToolResponse(msg.content)}
          </div>
        ))}
        {loading && <div className="chat-bubble assistant">Thinking...</div>}
        <div ref={scrollRef} />
      </div>

      <div className="chat-input-row">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Describe interaction or ask a question..."
          rows={2}
        />
        <button onClick={handleSend} disabled={loading}>Send</button>
      </div>
    </div>
  );
}
