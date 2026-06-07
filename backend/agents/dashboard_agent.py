from agents.memory_agent import load_conversation_history
from agents.ticketing_agent import load_tickets
from agents.escalation_agent import load_escalations


def get_dashboard_stats() -> dict:
    """
    Dashboard Agent:
    Generates analytics and summary data for the service desk system.
    """

    conversations = load_conversation_history()
    tickets = load_tickets()
    escalations = load_escalations()

    issue_type_counts = {}
    priority_counts = {}
    route_counts = {}

    for conversation in conversations:
        classification = conversation.get("classification") or {}

        issue_type = classification.get("issue_type", "Unknown")
        priority = classification.get("priority", "Unknown")
        route_to = conversation.get("route_to", "Unknown")

        issue_type_counts[issue_type] = issue_type_counts.get(issue_type, 0) + 1
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
        route_counts[route_to] = route_counts.get(route_to, 0) + 1

    open_tickets = [
        ticket for ticket in tickets
        if ticket.get("status") == "Open"
    ]

    return {
        "total_conversations": len(conversations),
        "total_tickets": len(tickets),
        "open_tickets": len(open_tickets),
        "total_escalations": len(escalations),
        "issue_type_counts": issue_type_counts,
        "priority_counts": priority_counts,
        "route_counts": route_counts,
        "recent_conversations": conversations[-5:][::-1],
        "recent_tickets": tickets[-5:][::-1],
        "recent_escalations": escalations[-5:][::-1],
        "agent": "Dashboard Agent"
    }


def get_all_tickets() -> list:
    """
    Returns all created tickets.
    """

    return load_tickets()[::-1]


def get_all_escalations() -> list:
    """
    Returns all escalation records.
    """

    return load_escalations()[::-1]