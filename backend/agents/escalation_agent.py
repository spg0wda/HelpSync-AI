import json
import os
from datetime import datetime


ESCALATIONS_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "escalations.json"
)


def load_escalations() -> list:
    """
    Loads previous escalations from the local JSON file.
    """
    if not os.path.exists(ESCALATIONS_FILE):
        return []

    with open(ESCALATIONS_FILE, "r") as file:
        return json.load(file)


def save_escalations(escalations: list) -> None:
    """
    Saves escalation records into the local JSON file.
    """
    with open(ESCALATIONS_FILE, "w") as file:
        json.dump(escalations, file, indent=4)


def escalate_issue(user_query: str, issue_type: str, priority: str, ticket_id: str | None = None) -> dict:
    """
    Escalation Agent:
    Escalates critical or unresolved issues to a higher support team.
    """

    escalations = load_escalations()

    escalation_id = f"ESC-{2001 + len(escalations)}"

    escalation = {
        "escalation_id": escalation_id,
        "ticket_id": ticket_id,
        "user_query": user_query,
        "issue_type": issue_type,
        "priority": priority,
        "status": "Escalated",
        "escalated_to": assign_escalation_team(issue_type),
        "reason": get_escalation_reason(user_query, priority),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "agent": "Escalation Agent"
    }

    escalations.append(escalation)
    save_escalations(escalations)

    return escalation


def assign_escalation_team(issue_type: str) -> str:
    """
    Assigns escalated issue to the correct higher-level team.
    """

    escalation_team_mapping = {
        "Network": "Senior Network Operations Team",
        "Hardware": "Senior Hardware Support Team",
        "Software": "Application Engineering Team",
        "Access": "Identity Security Team",
        "HR": "HR Escalation Team",
        "General": "Service Desk Manager"
    }

    return escalation_team_mapping.get(issue_type, "Service Desk Manager")


def get_escalation_reason(user_query: str, priority: str) -> str:
    """
    Creates a simple explanation for why the issue was escalated.
    """

    query = user_query.lower()

    if "security breach" in query:
        return "Possible security incident detected."

    if "down" in query or "not working for everyone" in query:
        return "Service outage or large-scale impact detected."

    if priority == "Critical":
        return "Issue marked as critical priority."

    return "Issue requires higher-level support."