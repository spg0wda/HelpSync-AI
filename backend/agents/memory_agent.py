import json
import os
from datetime import datetime
from typing import Any


HISTORY_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "conversation_history.json"
)


def load_conversation_history() -> list:
    """
    Loads conversation history from local JSON file.
    """

    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r") as file:
        return json.load(file)


def save_conversation_history(history: list) -> None:
    """
    Saves conversation history to local JSON file.
    """

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


def save_conversation(
    user_query: str,
    classification: dict[str, Any] | None,
    route_to: str | None,
    retrieval_result: dict[str, Any] | None,
    ticket: dict[str, Any] | None,
    escalation: dict[str, Any] | None,
    final_response: str
) -> dict:
    """
    Memory Agent:
    Stores the complete service desk interaction.
    """

    history = load_conversation_history()

    conversation_id = f"CONV-{3001 + len(history)}"

    record = {
        "conversation_id": conversation_id,
        "user_query": user_query,
        "classification": classification,
        "route_to": route_to,
        "retrieval_result": retrieval_result,
        "ticket": ticket,
        "escalation": escalation,
        "final_response": final_response,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "agent": "Memory Agent"
    }

    history.append(record)
    save_conversation_history(history)

    return record


def get_recent_conversations(limit: int = 10) -> list:
    """
    Returns recent conversation history.
    """

    history = load_conversation_history()
    return history[-limit:][::-1]