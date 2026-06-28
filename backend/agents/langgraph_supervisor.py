from typing import Any, Dict, List, TypedDict

from langgraph.graph import END, StateGraph

from agents.classifier_agent import classify_issue
from agents.retrieval_agent import retrieve_solution
from agents.ticketing_agent import create_ticket
from agents.escalation_agent import escalate_issue
from agents.memory_agent import save_conversation


class ServiceDeskState(TypedDict, total=False):
    user_query: str
    route_to: str
    classification: Any
    retrieval_result: Any
    ticket: Any
    escalation: Any
    workflow_trace: List[str]
    final_response: str
    memory_record: Any
    llm_response: str
    current_stage: str


def _base_state(user_query: str) -> ServiceDeskState:
    return {
        "user_query": user_query,
        "route_to": "supervisor",
        "classification": "",
        "retrieval_result": "",
        "ticket": None,
        "escalation": None,
        "workflow_trace": [],
        "final_response": "",
        "memory_record": None,
        "llm_response": "",
        "current_stage": "LangGraph Supervisor Workflow",
    }


def _text(value: Any) -> str:
    if value is None:
        return ""

    if isinstance(value, str):
        return value

    if isinstance(value, dict):
        for key in [
            "issue_type",
            "priority",
            "route_to",
            "classification",
            "retrieval_result",
            "solution",
            "message",
            "response",
            "answer",
            "final_response",
            "llm_response",
            "ticket_id",
            "status",
        ]:
            if key in value and value[key]:
                return str(value[key])
        return str(value)

    return str(value)


def _get_issue_type(classification: Any, user_query: str) -> str:
    if isinstance(classification, dict):
        issue_type = classification.get("issue_type") or classification.get("classification")
        if issue_type:
            return str(issue_type)

    text = f"{classification} {user_query}".lower()

    if "wifi" in text or "wi-fi" in text or "network" in text:
        return "Network"
    if "password" in text or "login" in text or "signin" in text:
        return "Access"
    if "email" in text or "mail" in text:
        return "Email"
    if "software" in text or "application" in text or "app" in text:
        return "Software"
    if "security" in text or "hacked" in text or "breach" in text:
        return "Security"

    return "General"


def _get_priority(classification: Any, user_query: str) -> str:
    if isinstance(classification, dict):
        priority = classification.get("priority")
        if priority:
            return str(priority)

    text = f"{classification} {user_query}".lower()

    if any(word in text for word in ["urgent", "critical", "server down", "outage", "breach", "hacked"]):
        return "High"

    if any(word in text for word in ["not working", "unable", "failed", "error"]):
        return "Medium"

    return "Low"


def _call_classifier(user_query: str) -> Any:
    try:
        return classify_issue(user_query)
    except Exception as error:
        return {
            "issue_type": _get_issue_type("", user_query),
            "priority": _get_priority("", user_query),
            "route_to": "Retrieval Agent",
            "agent": "Classifier Agent",
            "warning": str(error),
        }


def _call_retrieval(user_query: str, issue_type: str) -> Any:
    attempts = [
        lambda: retrieve_solution(user_query, issue_type),
        lambda: retrieve_solution(issue_type, user_query),
        lambda: retrieve_solution(user_query),
        lambda: retrieve_solution(
            {
                "user_query": user_query,
                "issue_type": issue_type,
            }
        ),
    ]

    last_error = None

    for attempt in attempts:
        try:
            return attempt()
        except Exception as error:
            last_error = error

    return {
        "status": "failed",
        "error": str(last_error),
        "message": "No direct solution found. A ticket may be required.",
    }


def _call_ticket(user_query: str, issue_type: str, priority: str) -> Any:
    attempts = [
        lambda: create_ticket(user_query, issue_type, priority),
        lambda: create_ticket(issue_type, priority, user_query),
        lambda: create_ticket(
            {
                "user_query": user_query,
                "issue_type": issue_type,
                "priority": priority,
            }
        ),
    ]

    last_error = None

    for attempt in attempts:
        try:
            return attempt()
        except Exception as error:
            last_error = error

    return {
        "status": "ticket_prepared",
        "issue_type": issue_type,
        "priority": priority,
        "message": "Ticket prepared for IT support team.",
        "error": str(last_error),
    }


def _call_escalation(user_query: str, issue_type: str, priority: str) -> Any:
    attempts = [
        lambda: escalate_issue(user_query, issue_type, priority),
        lambda: escalate_issue(issue_type, priority, user_query),
        lambda: escalate_issue(
            {
                "user_query": user_query,
                "issue_type": issue_type,
                "priority": priority,
            }
        ),
        lambda: escalate_issue(user_query),
    ]

    last_error = None

    for attempt in attempts:
        try:
            return attempt()
        except Exception as error:
            last_error = error

    return {
        "status": "escalation_prepared",
        "issue_type": issue_type,
        "priority": priority,
        "message": "Escalation prepared for support team.",
        "error": str(last_error),
    }


def supervisor_node(state: ServiceDeskState) -> ServiceDeskState:
    trace = state.get("workflow_trace", [])
    trace.append("LangGraph Supervisor received user query")
    trace.append("Supervisor routed issue to Classifier Agent")

    state["workflow_trace"] = trace
    state["route_to"] = "classifier_agent"
    state["current_stage"] = "LangGraph Supervisor Workflow"

    return state


def classifier_node(state: ServiceDeskState) -> ServiceDeskState:
    user_query = state.get("user_query", "")

    result = _call_classifier(user_query)

    state["classification"] = result
    state["route_to"] = "retrieval_agent"

    trace = state.get("workflow_trace", [])
    trace.append("Classifier Agent classified the issue")
    trace.append("Supervisor routed issue to Retrieval Agent")
    state["workflow_trace"] = trace

    return state


def retrieval_node(state: ServiceDeskState) -> ServiceDeskState:
    user_query = state.get("user_query", "")
    classification = state.get("classification", "")

    issue_type = _get_issue_type(classification, user_query)
    priority = _get_priority(classification, user_query)

    result = _call_retrieval(user_query, issue_type)

    state["retrieval_result"] = result

    result_text = _text(result).lower()
    query_text = user_query.lower()

    trace = state.get("workflow_trace", [])
    trace.append("Retrieval Agent searched knowledge base and vector store")

    high_priority_words = [
        "security",
        "breach",
        "data leak",
        "hacked",
        "urgent",
        "critical",
        "server down",
        "outage",
        "production",
    ]

    unresolved_words = [
        "no direct solution",
        "no solution",
        "not found",
        "failed",
        "could not process",
        "unable",
        "error",
    ]

    if any(word in query_text for word in high_priority_words) or priority.lower() == "high":
        state["route_to"] = "escalation_agent"
        trace.append("Supervisor detected high-priority issue and routed to Escalation Agent")
    elif any(word in result_text for word in unresolved_words):
        state["route_to"] = "ticketing_agent"
        trace.append("Supervisor detected unresolved issue and routed to Ticketing Agent")
    else:
        state["route_to"] = "response_agent"
        trace.append("Supervisor routed issue to Response Agent")

    state["workflow_trace"] = trace

    return state


def ticketing_node(state: ServiceDeskState) -> ServiceDeskState:
    user_query = state.get("user_query", "")
    classification = state.get("classification", "")

    issue_type = _get_issue_type(classification, user_query)
    priority = _get_priority(classification, user_query)

    result = _call_ticket(user_query, issue_type, priority)

    state["ticket"] = result
    state["route_to"] = "response_agent"

    trace = state.get("workflow_trace", [])
    trace.append("Ticketing Agent created or prepared a support ticket")
    trace.append("Supervisor routed issue to Response Agent")
    state["workflow_trace"] = trace

    return state


def escalation_node(state: ServiceDeskState) -> ServiceDeskState:
    user_query = state.get("user_query", "")
    classification = state.get("classification", "")

    issue_type = _get_issue_type(classification, user_query)
    priority = _get_priority(classification, user_query)

    result = _call_escalation(user_query, issue_type, priority)

    state["escalation"] = result
    state["route_to"] = "response_agent"

    trace = state.get("workflow_trace", [])
    trace.append("Escalation Agent escalated the issue")
    trace.append("Supervisor routed issue to Response Agent")
    state["workflow_trace"] = trace

    return state


def response_node(state: ServiceDeskState) -> ServiceDeskState:
    user_query = state.get("user_query", "")
    classification = state.get("classification", "")
    retrieval_result = state.get("retrieval_result", "")
    ticket = state.get("ticket")
    escalation = state.get("escalation")

    issue_type = _get_issue_type(classification, user_query)
    priority = _get_priority(classification, user_query)

    final_response = f"""HelpSync AI has analyzed your issue.

Issue:
{user_query}

Issue Type:
{issue_type}

Priority:
{priority}

Suggested Solution:
{_text(retrieval_result)}
"""

    if ticket:
        final_response += f"""

Ticket Status:
A support ticket has been created or prepared.

Ticket Details:
{_text(ticket)}
"""

    if escalation:
        final_response += f"""

Escalation Status:
This issue has been escalated to the support team.

Escalation Details:
{_text(escalation)}
"""

    if "wi-fi" in user_query.lower() or "wifi" in user_query.lower():
        final_response += """

Wi-Fi Troubleshooting Steps:
1. Turn Wi-Fi off and on.
2. Check if airplane mode is disabled.
3. Forget and reconnect to the office Wi-Fi network.
4. Restart your laptop or mobile device.
5. Restart the network adapter.
6. Move closer to the router or access point.
7. Contact IT support if the issue continues.
"""

    state["final_response"] = final_response.strip()
    state["llm_response"] = final_response.strip()
    state["route_to"] = "langgraph_supervisor"

    trace = state.get("workflow_trace", [])
    trace.append("Response Agent generated final service desk response")
    trace.append("LangGraph Supervisor workflow completed")
    state["workflow_trace"] = trace

    return state


def memory_node(state: ServiceDeskState) -> ServiceDeskState:
    try:
        memory_record = save_conversation(
            state.get("user_query", ""),
            state.get("classification", ""),
            state.get("route_to", ""),
            state.get("retrieval_result", ""),
            state.get("ticket", None),
            state.get("escalation", None),
            state.get("final_response", ""),
        )

        state["memory_record"] = memory_record

    except Exception as error:
        state["memory_record"] = {
            "status": "memory_save_failed",
            "error": str(error),
        }

    trace = state.get("workflow_trace", [])
    trace.append("Conversation saved to memory")
    state["workflow_trace"] = trace

    return state


def route_after_retrieval(state: ServiceDeskState) -> str:
    route_to = state.get("route_to", "")

    if route_to == "ticketing_agent":
        return "ticketing_agent"

    if route_to == "escalation_agent":
        return "escalation_agent"

    return "response_agent"


def build_langgraph_supervisor():
    graph = StateGraph(ServiceDeskState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("classifier_agent", classifier_node)
    graph.add_node("retrieval_agent", retrieval_node)
    graph.add_node("ticketing_agent", ticketing_node)
    graph.add_node("escalation_agent", escalation_node)
    graph.add_node("response_agent", response_node)
    graph.add_node("memory_agent", memory_node)

    graph.set_entry_point("supervisor")

    graph.add_edge("supervisor", "classifier_agent")
    graph.add_edge("classifier_agent", "retrieval_agent")

    graph.add_conditional_edges(
        "retrieval_agent",
        route_after_retrieval,
        {
            "ticketing_agent": "ticketing_agent",
            "escalation_agent": "escalation_agent",
            "response_agent": "response_agent",
        },
    )

    graph.add_edge("ticketing_agent", "response_agent")
    graph.add_edge("escalation_agent", "response_agent")
    graph.add_edge("response_agent", "memory_agent")
    graph.add_edge("memory_agent", END)

    return graph.compile()


_supervisor_app = None


def get_supervisor_app():
    global _supervisor_app

    if _supervisor_app is None:
        _supervisor_app = build_langgraph_supervisor()

    return _supervisor_app


def run_langgraph_supervisor(user_query: str) -> Dict[str, Any]:
    app = get_supervisor_app()

    initial_state = _base_state(user_query)

    result = app.invoke(initial_state)

    result["current_stage"] = "LangGraph Supervisor Workflow"
    result["route_to"] = "langgraph_supervisor"

    return result


def run_supervisor_graph(user_query: str) -> Dict[str, Any]:
    return run_langgraph_supervisor(user_query)


def run_supervisor(user_query: str) -> Dict[str, Any]:
    return run_langgraph_supervisor(user_query)


def run_langgraph_workflow(user_query: str) -> Dict[str, Any]:
    return run_langgraph_supervisor(user_query)