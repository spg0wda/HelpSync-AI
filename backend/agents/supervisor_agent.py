from agents.classifier_agent import classify_issue
from agents.retrieval_agent import retrieve_solution
from agents.ticketing_agent import create_ticket
from agents.escalation_agent import escalate_issue


def process_service_request(user_query: str) -> dict:
    """
    Supervisor Agent:
    Controls the complete service desk workflow.

    Flow:
    1. Sends user query to Classifier Agent
    2. Routes query to Retrieval / Ticketing / Escalation Agent
    3. Collects all agent outputs
    4. Builds final user response
    """

    workflow_trace = []

    # Step 1: Classifier Agent
    classification = classify_issue(user_query)

    workflow_trace.append({
        "step": 1,
        "agent": "Classifier Agent",
        "action": "Classified user issue",
        "output": classification
    })

    retrieval_result = None
    ticket = None
    escalation = None

    route_to = classification["route_to"]

    # Step 2: Route to Retrieval Agent
    if route_to == "Retrieval Agent":
        retrieval_result = retrieve_solution(
            user_query=user_query,
            issue_type=classification["issue_type"]
        )

        workflow_trace.append({
            "step": 2,
            "agent": "Retrieval Agent",
            "action": "Searched knowledge base for solution",
            "output": retrieval_result
        })

        # If no solution is found, create ticket
        if retrieval_result["found"] is False:
            ticket = create_ticket(
                user_query=user_query,
                issue_type=classification["issue_type"],
                priority=classification["priority"]
            )

            workflow_trace.append({
                "step": 3,
                "agent": "Ticketing Agent",
                "action": "Created ticket because no strong KB solution was found",
                "output": ticket
            })

    # Step 3: Route directly to Ticketing Agent
    elif route_to == "Ticketing Agent":
        ticket = create_ticket(
            user_query=user_query,
            issue_type=classification["issue_type"],
            priority=classification["priority"]
        )

        workflow_trace.append({
            "step": 2,
            "agent": "Ticketing Agent",
            "action": "Created ticket for manual support",
            "output": ticket
        })

    # Step 4: Route to Escalation Agent
    elif route_to == "Escalation Agent":
        ticket = create_ticket(
            user_query=user_query,
            issue_type=classification["issue_type"],
            priority=classification["priority"]
        )

        workflow_trace.append({
            "step": 2,
            "agent": "Ticketing Agent",
            "action": "Created ticket before escalation",
            "output": ticket
        })

        escalation = escalate_issue(
            user_query=user_query,
            issue_type=classification["issue_type"],
            priority=classification["priority"],
            ticket_id=ticket["ticket_id"]
        )

        workflow_trace.append({
            "step": 3,
            "agent": "Escalation Agent",
            "action": "Escalated critical issue to higher support team",
            "output": escalation
        })

    final_response = build_final_response(
        classification=classification,
        retrieval_result=retrieval_result,
        ticket=ticket,
        escalation=escalation
    )

    return {
        "user_query": user_query,
        "supervisor": {
            "agent": "Supervisor Agent",
            "decision": route_to,
            "status": "Completed workflow successfully"
        },
        "classification": classification,
        "retrieval_result": retrieval_result,
        "ticket": ticket,
        "escalation": escalation,
        "workflow_trace": workflow_trace,
        "final_response": final_response
    }


def build_final_response(
    classification: dict,
    retrieval_result: dict | None,
    ticket: dict | None,
    escalation: dict | None
) -> str:
    """
    Builds final response after collecting all agent outputs.
    """

    if escalation:
        return (
            f"Your issue has been classified as {classification['issue_type']} "
            f"with {classification['priority']} priority. "
            f"A ticket has been created and escalated successfully. "
            f"Ticket ID: {ticket['ticket_id']}. "
            f"Escalation ID: {escalation['escalation_id']}. "
            f"Escalated To: {escalation['escalated_to']}."
        )

    if ticket:
        return (
            f"Your issue has been classified as {classification['issue_type']} "
            f"with {classification['priority']} priority. "
            f"A support ticket has been created. "
            f"Ticket ID: {ticket['ticket_id']}. "
            f"Assigned Team: {ticket['assigned_team']}."
        )

    if retrieval_result and retrieval_result["found"]:
        return (
            f"Your issue has been classified as {classification['issue_type']}. "
            f"Suggested solution: {retrieval_result['solution']}"
        )

    return (
        f"Your issue has been classified as {classification['issue_type']} "
        f"with {classification['priority']} priority."
    )