import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { loadHistory } from "../store/interactionsSlice";

export default function InteractionHistory() {
  const dispatch = useDispatch();
  const { history } = useSelector((state) => state.interactions);

  useEffect(() => {
    dispatch(loadHistory());
  }, [dispatch]);

  return (
    <div className="panel">
      <div className="history-header">
        <h2>Interaction History</h2>
        <button className="refresh-btn" onClick={() => dispatch(loadHistory())}>
          Refresh
        </button>
      </div>

      {history.length === 0 && <p className="hint">No interactions logged yet.</p>}

      <div className="history-list">
        {history.map((item) => (
          <div key={item.id} className={`history-card sentiment-${item.sentiment}`}>
            <div className="history-card-header">
              <strong>{item.hcp_name}</strong>
              <span className="badge">{item.sentiment}</span>
            </div>
            <p className="history-topic">{item.topic}</p>
            {item.outcomes && <p className="history-detail"><em>Outcomes:</em> {item.outcomes}</p>}
            {item.followup && <p className="history-detail"><em>Follow-up:</em> {item.followup}</p>}
            <span className="history-date">
              {item.created_at ? new Date(item.created_at).toLocaleString() : ""}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
