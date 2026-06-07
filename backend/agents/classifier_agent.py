def classify_issue(user_query: str) -> dict:
    """
    Classifier Agent:
    Classifies the user's service desk issue into category, priority, and routing decision.
    """

    query = user_query.lower()

    issue_type = "General"
    priority = "Medium"
    route_to = "Retrieval Agent"

    # Network / IT issues
    if any(word in query for word in ["wifi", "internet", "network", "vpn", "connection"]):
        issue_type = "Network"
        route_to = "Retrieval Agent"

    # Hardware issues
    elif any(word in query for word in ["laptop", "keyboard", "mouse", "screen", "printer", "battery"]):
        issue_type = "Hardware"
        route_to = "Ticketing Agent"

    # Software issues
    elif any(word in query for word in ["software", "install", "application", "app", "crash", "bug"]):
        issue_type = "Software"
        route_to = "Retrieval Agent"

    # Access issues
    elif any(word in query for word in ["password", "login", "account", "access", "locked", "reset"]):
        issue_type = "Access"
        route_to = "Retrieval Agent"

    # HR issues
    elif any(word in query for word in ["leave", "salary", "payroll", "attendance", "employee", "hr"]):
        issue_type = "HR"
        route_to = "Retrieval Agent"

    # Critical / urgent cases
    if any(word in query for word in ["urgent", "immediately", "critical", "down", "not working for everyone", "security breach"]):
        priority = "Critical"
        route_to = "Escalation Agent"

    elif any(word in query for word in ["not working", "failed", "error", "unable"]):
        priority = "High"

    elif any(word in query for word in ["how to", "request", "need", "help"]):
        priority = "Medium"

    else:
        priority = "Low"

    return {
        "issue_type": issue_type,
        "priority": priority,
        "route_to": route_to,
        "agent": "Classifier Agent"
    }