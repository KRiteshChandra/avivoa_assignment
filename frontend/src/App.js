import React from "react";
import LogInteractionForm from "./components/LogInteractionForm";
import ChatInterface from "./components/ChatInterface";
import InteractionHistory from "./components/InteractionHistory";
import "./index.css";

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>AI-First CRM — HCP Interaction Log</h1>
      </header>

      <main className="app-grid">
        <LogInteractionForm />
        <ChatInterface />
      </main>

      <section className="app-history-section">
        <InteractionHistory />
      </section>
    </div>
  );
}

export default App;
