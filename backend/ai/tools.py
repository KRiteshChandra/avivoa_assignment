from db import SessionLocal
from models import Interaction
from ai.llm import call_llm_plain


def _get_interaction(db, interaction_id=None):
    """Helper: fetch by ID, or fall back to most recent."""
    if interaction_id:
        return db.query(Interaction).filter(Interaction.id == interaction_id).first()
    return db.query(Interaction).order_by(Interaction.created_at.desc()).first()


# Tool 1: Log Interaction
def log_interaction(args: dict) -> dict:
    db = SessionLocal()
    try:
        record = Interaction(
            hcp_name=args.get("hcp_name"),
            topic=args.get("topic"),
            sentiment=args.get("sentiment"),
            outcomes=args.get("outcomes"),
            followup=args.get("followup"),
            raw_input=args.get("_raw_input"),
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return {"tool": "log_interaction", "result": record.to_dict()}
    finally:
        db.close()


# Tool 2: Edit Interaction
def edit_interaction(args: dict) -> dict:
    db = SessionLocal()
    try:
        record = _get_interaction(db, args.get("interaction_id"))
        if not record:
            return {"tool": "edit_interaction", "result": {"error": "No interaction found to edit."}}

        for field in ["hcp_name", "topic", "sentiment", "outcomes", "followup"]:
            if args.get(field) is not None:
                setattr(record, field, args[field])

        db.commit()
        db.refresh(record)
        return {"tool": "edit_interaction", "result": record.to_dict()}
    finally:
        db.close()


# Tool 3: Get History
def get_history(args: dict) -> dict:
    db = SessionLocal()
    try:
        query = db.query(Interaction)
        if args.get("hcp_name"):
            query = query.filter(Interaction.hcp_name.ilike(f"%{args['hcp_name']}%"))
        limit = args.get("limit", 5)
        records = query.order_by(Interaction.created_at.desc()).limit(limit).all()
        return {"tool": "get_history", "result": [r.to_dict() for r in records]}
    finally:
        db.close()


# Tool 4: Summarize
def summarize(args: dict) -> dict:
    db = SessionLocal()
    try:
        record = _get_interaction(db, args.get("interaction_id"))
        if not record:
            return {"tool": "summarize", "result": {"error": "No interaction found to summarize."}}

        prompt = f"""Summarize this HCP interaction in 1-2 sentences:
HCP: {record.hcp_name}
Topic: {record.topic}
Sentiment: {record.sentiment}
Outcomes: {record.outcomes}
"""
        summary = call_llm_plain(prompt)
        return {"tool": "summarize", "result": {"interaction_id": record.id, "summary": summary}}
    finally:
        db.close()


# Tool 5: Suggest Follow-up
def suggest_followup(args: dict) -> dict:
    db = SessionLocal()
    try:
        record = _get_interaction(db, args.get("interaction_id"))
        if not record:
            return {"tool": "suggest_followup", "result": {"error": "No interaction found."}}

        prompt = f"""Based on this HCP interaction, suggest 2-3 concise follow-up actions for the field rep.
HCP: {record.hcp_name}
Topic: {record.topic}
Sentiment: {record.sentiment}
Outcomes: {record.outcomes}

Return as a short bulleted list."""
        suggestions = call_llm_plain(prompt)
        return {"tool": "suggest_followup", "result": {"interaction_id": record.id, "suggestions": suggestions}}
    finally:
        db.close()


# Registry so graph.py can dispatch by name
TOOL_FUNCTIONS = {
    "log_interaction": log_interaction,
    "edit_interaction": edit_interaction,
    "get_history": get_history,
    "summarize": summarize,
    "suggest_followup": suggest_followup,
}
