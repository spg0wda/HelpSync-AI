from typing import TypedDict, Any

from langgraph.graph import StateGraph, START, END

from agents.classifier_agent import classify_issue
from agents.retrieval_agent import retrieve_solution
from agents.ticketing_agent import create_ticket
from agents.escalation_agent import escalate_issue


class ServiceDeskState(TypedDict, total=False):
    """
    Shared state passed between LangGraph agent nodes.
    """

    user_query: str
    route_to: str

    classification: dict[str, Any]
    retrieval_result: dict[str, Any] | None
    ticket: dict[str, Any] | None
    escalation: dict[str, Any] | None

    workflow_trace: list[dict[str, Any]]
    final_response: str


def add_trace(
    state: ServiceDeskState,
    step: int,
    agent: str,
    action: str,
    output: dict[str, Any] | None
) -> list[dict[str, Any]]:
    """
    Adds one step to the workflow trace.
    """

    existing_trace = state.get("workflow_trace", [])

    return existing_trace + [
        {
            "step": step,
            "agent": agent,
            "action": action,
            "output": output
        }
    ]


def classifier_node(state: ServiceDeskState) -> ServiceDeskState:
    """
    LangGraph node 1:
    Runs Classifier Agent.
    """

    user_query = state["user_query"]

    classification = classify_issue(user_query)

    return {
        "classification": classification,
        "route_to": classification["route_to"],
        "workflow_trace": add_trace(
            state=state,
            step=1,
            agent="Classifier Agent",
            action="Classified user issue and selected route",
            output=classification
        )
    }


def retrieval_node(state: ServiceDeskState) -> ServiceDeskState:
    """
    LangGraph node 2:
    Runs Retrieval Agent.
    """

    retrieval_result = retrieve_solution(
        user_query=state["user_query"],
        issue_type=state["classification"]["issue_type"]
    )

    return {
        "retrieval_result": retrieval_result,
        "workflow_trace": add_trace(
            state=state,
            step=2,
            agent="Retrieval Agent",
            action="Searched knowledge base for possible solution",
            output=retrieval_result
        )
    }


def ticketing_node(state: ServiceDeskState) -> ServiceDeskState:
    """
    LangGraph node 3:
    Runs Ticketing Agent.
    """

    ticket = create_ticket(
        user_query=state["user_query"],
        issue_type=state["classification"]["issue_type"],
        priority=state["classification"]["priority"]
    )

    step_number = len(state.get("workflow_trace", [])) + 1

    return {
        "ticket": ticket,
        "workflow_trace": add_trace(
            state=state,
            step=step_number,
            agent="Ticketing Agent",
            action="Created support ticket",
            output=ticket
        )
    }


def escalation_node(state: ServiceDeskState) -> ServiceDeskState:
    """
    LangGraph node 4:
    Runs Escalation Agent.
    """

    ticket = state.get("ticket")

    escalation = escalate_issue(
        user_query=state["user_query"],
        issue_type=state["classification"]["issue_type"],
        priority=state["classification"]["priority"],
        ticket_id=ticket["ticket_id"] if ticket else None
    )

    step_number = len(state.get("workflow_trace", [])) + 1

    return {
        "escalation": escalation,
        "workflow_trace": add_trace(
            state=state,
            step=step_number,
            agent="Escalation Agent",
            action="Escalated critical issue to higher support team",
            output=escalation
        )
    }


def final_response_node(state: ServiceDeskState) -> ServiceDeskState:
    """
    LangGraph final node:
    Builds final response after collecting all agent outputs.
    """

    classification = state.get("classification")
    retrieval_result = state.get("retrieval_result")
    ticket = state.get("ticket")
    escalation = state.get("escalation")

    final_response = build_final_response(
        classification=classification,
        retrieval_result=retrieval_result,
        ticket=ticket,
        escalation=escalation
    )

    step_number = len(state.get("workflow_trace", [])) + 1

    return {
        "final_response": final_response,
        "workflow_trace": add_trace(
            state=state,
            step=step_number,
            agent="Supervisor Agent",
            action="Prepared final response for user",
            output={"final_response": final_response}
        )
    }


def route_after_classification(state: ServiceDeskState) -> str:
    """
    Conditional edge:
    Decides where to go after classification.
    """

    route_to = state["route_to"]

    if route_to == "Retrieval Agent":
        return "retrieval"

    # Both Ticketing Agent and Escalation Agent first create a ticket.
    return "ticketing"


def route_after_retrieval(state: ServiceDeskState) -> str:
    """
    Conditional edge:
    If retrieval found a solution, finish.
    If not, create a ticket.
    """

    retrieval_result = state.get("retrieval_result")

    if retrieval_result and retrieval_result.get("found") is True:
        return "final_response"

    return "ticketing"


def route_after_ticketing(state: ServiceDeskState) -> str:
    """
    Conditional edge:
    If original classifier route was escalation, escalate after ticket creation.
    Otherwise, finish.
    """

    if state.get("route_to") == "Escalation Agent":
        return "escalation"

    return "final_response"


def build_final_response(
    classification: dict[str, Any],
    retrieval_result: dict[str, Any] | None,
    ticket: dict[str, Any] | None,
    escalation: dict[str, Any] | None
) -> str:
    """
    Builds final user-facing response.
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

    if retrieval_result and retrieval_result.get("found"):
        return (
            f"Your issue has been classified as {classification['issue_type']}. "
            f"Suggested solution: {retrieval_result['solution']}"
        )

    return (
        f"Your issue has been classified as {classification['issue_type']} "
        f"with {classification['priority']} priority."
    )


def build_service_desk_graph():
    """
    Builds and compiles the LangGraph workflow.
    """

    workflow = StateGraph(ServiceDeskState)

    workflow.add_node("classifier", classifier_node)
    workflow.add_node("retrieval", retrieval_node)
    workflow.add_node("ticketing", ticketing_node)
    workflow.add_node("escalation", escalation_node)
    workflow.add_node("final_response", final_response_node)

    workflow.add_edge(START, "classifier")

    workflow.add_conditional_edges(
        "classifier",
        route_after_classification,
        {
            "retrieval": "retrieval",
            "ticketing": "ticketing"
        }
    )

    workflow.add_conditional_edges(
        "retrieval",
        route_after_retrieval,
        {
            "final_response": "final_response",
            "ticketing": "ticketing"
        }
    )

    workflow.add_conditional_edges(
        "ticketing",
        route_after_ticketing,
        {
            "escalation": "escalation",
            "final_response": "final_response"
        }
    )

    workflow.add_edge("escalation", "final_response")
    workflow.add_edge("final_response", END)

    return workflow.compile()


service_desk_graph = build_service_desk_graph()


def run_langgraph_workflow(user_query: str) -> dict:
    """
    Runs the compiled LangGraph workflow.
    """

    initial_state: ServiceDeskState = {
        "user_query": user_query,
        "workflow_trace": []
    }

    result = service_desk_graph.invoke(initial_state)

    return {
        "user_query": result["user_query"],
        "supervisor": {
            "agent": "LangGraph Supervisor",
            "decision": result.get("route_to"),
            "status": "Completed graph workflow successfully"
        },
        "classification": result.get("classification"),
        "retrieval_result": result.get("retrieval_result"),
        "ticket": result.get("ticket"),
        "escalation": result.get("escalation"),
        "workflow_trace": result.get("workflow_trace"),
        "final_response": result.get("final_response")
    }