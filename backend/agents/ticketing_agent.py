import json
import os
from datetime import datetime


TICKETS_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "tickets.json"
)


def load_tickets() -> list:
    """
    Loads tickets from the local JSON file.
    """
    if not os.path.exists(TICKETS_FILE):
        return []

    with open(TICKETS_FILE, "r") as file:
        return json.load(file)


def save_tickets(tickets: list) -> None:
    """
    Saves tickets into the local JSON file.
    """
    with open(TICKETS_FILE, "w") as file:
        json.dump(tickets, file, indent=4)


def create_ticket(user_query: str, issue_type: str, priority: str) -> dict:
    """
    Ticketing Agent:
    Creates a support ticket for issues that need manual resolution.
    """

    tickets = load_tickets()

    ticket_id = f"TKT-{1001 + len(tickets)}"

    new_ticket = {
        "ticket_id": ticket_id,
        "user_query": user_query,
        "issue_type": issue_type,
        "priority": priority,
        "status": "Open",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "assigned_team": assign_team(issue_type),
        "agent": "Ticketing Agent"
    }

    tickets.append(new_ticket)
    save_tickets(tickets)

    return new_ticket


def assign_team(issue_type: str) -> str:
    """
    Assigns ticket to the correct support team.
    """

    team_mapping = {
        "Network": "IT Network Support",
        "Hardware": "IT Hardware Support",
        "Software": "Software Support Team",
        "Access": "Identity and Access Management Team",
        "HR": "HR Operations Team",
        "General": "Service Desk Team"
    }

    return team_mapping.get(issue_type, "Service Desk Team")