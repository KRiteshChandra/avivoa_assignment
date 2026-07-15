import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { submitStructuredLog } from "../store/interactionsSlice";

const initialForm = {
  hcp_name: "",
  topic: "",
  sentiment: "neutral",
  outcomes: "",
  followup: "",
};

export default function LogInteractionForm() {
  const dispatch = useDispatch();
  const [form, setForm] = useState(initialForm);
  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.hcp_name || !form.topic) return;
    await dispatch(submitStructuredLog(form));
    setForm(initialForm);
    setSubmitted(true);
    setTimeout(() => setSubmitted(false), 2000);
  };

  return (
    <div className="panel">
      <h2>Log HCP Interaction</h2>
      <form onSubmit={handleSubmit} className="form">
        <label>
          HCP Name
          <input
            name="hcp_name"
            value={form.hcp_name}
            onChange={handleChange}
            placeholder="Dr. Sharma"
            required
          />
        </label>

        <label>
          Topics Discussed
          <textarea
            name="topic"
            value={form.topic}
            onChange={handleChange}
            placeholder="Discussed insulin efficacy, shared brochure..."
            required
          />
        </label>

        <label>
          Observed Sentiment
          <select name="sentiment" value={form.sentiment} onChange={handleChange}>
            <option value="positive">Positive</option>
            <option value="neutral">Neutral</option>
            <option value="negative">Negative</option>
          </select>
        </label>

        <label>
          Outcomes
          <textarea
            name="outcomes"
            value={form.outcomes}
            onChange={handleChange}
            placeholder="Key outcomes or agreements..."
          />
        </label>

        <label>
          Follow-up Actions
          <textarea
            name="followup"
            value={form.followup}
            onChange={handleChange}
            placeholder="Next steps..."
          />
        </label>

        <button type="submit">Log Interaction</button>
        {submitted && <span className="success-msg">Saved ✓</span>}
      </form>
    </div>
  );
}
