import json
import os
from datetime import datetime
from typing import Any

from agents.memory_agent import load_conversation_history


REPORTS_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "reports.json"
)


def load_reports() -> list:
    """
    Loads generated service desk reports.
    """

    if not os.path.exists(REPORTS_FILE):
        return []

    with open(REPORTS_FILE, "r") as file:
        return json.load(file)


def save_reports(reports: list) -> None:
    """
    Saves generated reports into local JSON file.
    """

    with open(REPORTS_FILE, "w") as file:
        json.dump(reports, file, indent=4)


def find_conversation(conversation_id: str | None = None) -> dict[str, Any] | None:
    """
    Finds a conversation by ID.
    If no ID is given, returns the latest conversation.
    """

    history = load_conversation_history()

    if not history:
        return None

    if conversation_id is None:
        return history[-1]

    for conversation in history:
        if conversation.get("conversation_id") == conversation_id:
            return conversation

    return None


def generate_service_report(conversation_id: str | None = None) -> dict:
    """
    Report Agent:
    Generates a final service desk report from conversation memory.
    """

    conversation = find_conversation(conversation_id)

    if conversation is None:
        return {
            "generated": False,
            "message": "No conversation found to generate report.",
            "agent": "Report Agent"
        }

    reports = load_reports()

    report_id = f"RPT-{4001 + len(reports)}"

    classification = conversation.get("classification") or {}
    retrieval_result = conversation.get("retrieval_result") or {}
    ticket = conversation.get("ticket")
    escalation = conversation.get("escalation")

    issue_type = classification.get("issue_type", "Unknown")
    priority = classification.get("priority", "Unknown")
    route_to = conversation.get("route_to", "Unknown")

    report = {
        "report_id": report_id,
        "conversation_id": conversation.get("conversation_id"),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "agent": "Report Agent",
        "generated": True,

        "case_summary": {
            "user_query": conversation.get("user_query"),
            "issue_type": issue_type,
            "priority": priority,
            "route_to": route_to,
            "final_response": conversation.get("final_response")
        },

        "resolution_summary": build_resolution_summary(
            retrieval_result=retrieval_result,
            ticket=ticket,
            escalation=escalation
        ),

        "architecture_flow": build_architecture_flow(
            retrieval_result=retrieval_result,
            ticket=ticket,
            escalation=escalation
        ),

        "risk_analysis": build_risk_analysis(issue_type, priority, escalation),

        "security_considerations": build_security_notes(issue_type, priority),

        "scalability_considerations": build_scalability_notes(issue_type, route_to),

        "final_recommendation": build_final_recommendation(
            issue_type=issue_type,
            priority=priority,
            ticket=ticket,
            escalation=escalation
        )
    }

    reports.append(report)
    save_reports(reports)

    return report


def build_resolution_summary(
    retrieval_result: dict,
    ticket: dict | None,
    escalation: dict | None
) -> str:
    """
    Creates a resolution summary.
    """

    if escalation:
        return (
            f"The issue was escalated to {escalation.get('escalated_to')} "
            f"with escalation ID {escalation.get('escalation_id')}."
        )

    if ticket:
        return (
            f"A support ticket was created with ticket ID {ticket.get('ticket_id')} "
            f"and assigned to {ticket.get('assigned_team')}."
        )

    if retrieval_result and retrieval_result.get("found"):
        return (
            f"A knowledge base solution was found: "
            f"{retrieval_result.get('solution')}"
        )

    return "No final resolution action was available."


def build_architecture_flow(
    retrieval_result: dict,
    ticket: dict | None,
    escalation: dict | None
) -> list:
    """
    Returns the agent flow used in the case.
    """

    flow = ["User Interface", "FastAPI Backend", "LangGraph Supervisor", "Classifier Agent"]

    if retrieval_result:
        flow.append("Retrieval Agent")

    if ticket:
        flow.append("Ticketing Agent")

    if escalation:
        flow.append("Escalation Agent")

    flow.append("Memory Agent")
    flow.append("Report Agent")

    return flow


def build_risk_analysis(
    issue_type: str,
    priority: str,
    escalation: dict | None
) -> str:
    """
    Generates simple risk analysis.
    """

    if priority == "Critical":
        return (
            f"This is a critical {issue_type} issue. "
            f"It may affect business continuity, productivity, or service availability."
        )

    if escalation:
        return (
            f"The issue required escalation, so it may need senior support attention."
        )

    return (
        f"The issue has {priority} priority. "
        f"Risk is manageable if handled within normal service desk SLA."
    )


def build_security_notes(issue_type: str, priority: str) -> str:
    """
    Generates security considerations.
    """

    if issue_type == "Access":
        return (
            "Access-related issues should be handled carefully. "
            "Identity verification, password reset policy, and audit logging are recommended."
        )

    if priority == "Critical":
        return (
            "Critical incidents should be reviewed for possible security impact, "
            "especially if they involve outage, breach, or unauthorized access."
        )

    return (
        "No major security concern detected, but support activity should still be logged."
    )


def build_scalability_notes(issue_type: str, route_to: str) -> str:
    """
    Generates scalability considerations.
    """

    return (
        f"For repeated {issue_type} issues, the knowledge base should be expanded. "
        f"Routing through {route_to} can be optimized by adding more rules, "
        f"LLM classification, or vector-based retrieval in the future."
    )


def build_final_recommendation(
    issue_type: str,
    priority: str,
    ticket: dict | None,
    escalation: dict | None
) -> str:
    """
    Generates final recommendation.
    """

    if escalation:
        return (
            "Monitor this issue until closure, notify the responsible team, "
            "and review root cause after resolution."
        )

    if ticket:
        return (
            "Track the ticket status and ensure the assigned team resolves it within SLA."
        )

    return (
        f"Keep improving the knowledge base for {issue_type} issues "
        f"to reduce manual support effort."
    )


def get_all_reports() -> list:
    """
    Returns all generated reports.
    """

    return load_reports()[::-1]