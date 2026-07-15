# JSON Schema definitions for each tool, following OpenAI/Groq function-calling format.
# The LLM reads these descriptions to decide which tool to call and what arguments to extract.

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "log_interaction",
            "description": (
                "Log a NEW HCP (Healthcare Professional) interaction. Use this when the "
                "field rep describes a meeting, call, or visit that hasn't been logged yet. "
                "Extract structured details from their natural-language description."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "hcp_name": {"type": "string", "description": "Name of the HCP/doctor"},
                    "topic": {"type": "string", "description": "Main topic(s) discussed"},
                    "sentiment": {
                        "type": "string",
                        "enum": ["positive", "neutral", "negative"],
                        "description": "Observed or inferred sentiment of the HCP"
                    },
                    "outcomes": {"type": "string", "description": "Key outcomes or agreements, if mentioned"},
                    "followup": {"type": "string", "description": "Follow-up actions mentioned, if any"}
                },
                "required": ["hcp_name", "topic"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit_interaction",
            "description": (
                "Edit or update a PREVIOUSLY logged interaction. Use this when the user says "
                "things like 'edit', 'update', 'change', or 'correct' about an existing entry. "
                "If no interaction_id is given, edits the most recently logged interaction."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "interaction_id": {"type": "integer", "description": "ID of interaction to edit. Omit to edit the most recent one."},
                    "hcp_name": {"type": "string"},
                    "topic": {"type": "string"},
                    "sentiment": {"type": "string", "enum": ["positive", "neutral", "negative"]},
                    "outcomes": {"type": "string"},
                    "followup": {"type": "string"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_history",
            "description": "Retrieve past logged interactions, optionally filtered by HCP name. Use when the user asks to see, list, or review past interactions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "hcp_name": {"type": "string", "description": "Filter by HCP name (optional)"},
                    "limit": {"type": "integer", "description": "Max records to return, default 5"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "summarize",
            "description": "Generate a concise summary of a logged interaction. Use when the user asks for a summary or recap.",
            "parameters": {
                "type": "object",
                "properties": {
                    "interaction_id": {"type": "integer", "description": "ID to summarize. Omit to summarize the most recent one."}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "suggest_followup",
            "description": "Suggest next-step follow-up actions (e.g. schedule meeting, send materials) for a logged interaction.",
            "parameters": {
                "type": "object",
                "properties": {
                    "interaction_id": {"type": "integer", "description": "ID to base suggestions on. Omit to use the most recent one."}
                },
                "required": []
            }
        }
    }
]
