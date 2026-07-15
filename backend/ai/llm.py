import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"  # confirmed working; supports native tool calling on Groq


def call_llm_with_tools(messages, tools):
    """
    Sends messages + tool schemas to Groq. The model decides whether to call
    a tool (returns tool_calls) or respond directly (returns content).
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    return response.choices[0].message


def call_llm_plain(prompt: str) -> str:
    """Simple text-generation call, no tools. Used by summarize/suggest_followup."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()