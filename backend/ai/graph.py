import json
from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from ai.llm import call_llm_with_tools
from ai.tool_schemas import TOOLS
from ai.tools import TOOL_FUNCTIONS

SYSTEM_PROMPT = """You are an AI assistant for a pharma CRM system, helping field reps log and manage
HCP (Healthcare Professional) interactions. Based on the user's message, decide which tool to call.
If they're describing a new interaction, log it. If they mention editing/updating, use edit_interaction.
If they ask about past interactions, use get_history. If they ask for a summary, use summarize.
If they ask for next steps, use suggest_followup.

IMPORTANT: Never invent or guess an interaction_id. Only include interaction_id in a tool call if the
user explicitly states a number. If they refer to "that", "the last one", or don't mention an ID at all,
omit interaction_id entirely from the tool call so the system defaults to the most recent interaction."""


class AgentState(TypedDict):
    messages: List[Dict[str, Any]]
    output: Dict[str, Any]


def agent_node(state: AgentState):
    messages = state["messages"]
    try:
        ai_message = call_llm_with_tools(messages, TOOLS)
    except Exception:
        # Model occasionally produces malformed tool-call syntax. Retry once.
        try:
            ai_message = call_llm_with_tools(messages, TOOLS)
        except Exception as e2:
            return {
                "messages": messages,
                "output": {"error": f"I couldn't process that request. Please rephrase and try again. ({str(e2)})"}
            }

    if ai_message.tool_calls:
        messages.append({
            "role": "assistant",
            "content": ai_message.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments}
                } for tc in ai_message.tool_calls
            ]
        })
        return {"messages": messages, "output": {}}
    else:
        return {"messages": messages, "output": {"response": ai_message.content}}


def tools_node(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    tool_calls = last_message.get("tool_calls", [])

    final_output = {}
    for tc in tool_calls:
        tool_name = tc["function"]["name"]
        try:
            args = json.loads(tc["function"]["arguments"])
        except json.JSONDecodeError:
            args = {}
        if args is None:
            args = {}

        tool_fn = TOOL_FUNCTIONS.get(tool_name)
        if tool_fn:
            result = tool_fn(args)
        else:
            result = {"tool": tool_name, "result": {"error": "Unknown tool"}}

        final_output = result

        messages.append({
            "role": "tool",
            "tool_call_id": tc["id"],
            "name": tool_name,
            "content": json.dumps(result["result"])
        })

    return {"messages": messages, "output": final_output}


def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.get("role") == "assistant" and last_message.get("tool_calls"):
        return "tools"
    return END


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tools_node)
    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    graph.add_edge("tools", END)
    return graph.compile()
