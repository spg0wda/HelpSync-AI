import json
import os
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor

from agents.classifier_agent import classify_issue
from agents.retrieval_agent import retrieve_solution
from agents.ticketing_agent import create_ticket
from agents.escalation_agent import escalate_issue
from agents.memory_agent import save_conversation


BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"

load_dotenv()
load_dotenv(ENV_PATH)


def _json_text(data: Any) -> str:
    try:
        return json.dumps(data, indent=2, default=str)
    except Exception:
        return str(data)


def _extract_text(value: Any) -> str:
    if value is None:
        return ""

    if isinstance(value, str):
        return value

    if isinstance(value, dict):
        for key in ["final_response", "llm_response", "response", "message", "answer", "retrieval_result"]:
            if key in value and value[key]:
                return str(value[key])
        return _json_text(value)

    return str(value)


def _base_state(user_query: str) -> Dict[str, Any]:
    return {
        "user_query": user_query,
        "route_to": "",
        "classification": "",
        "retrieval_result": "",
        "ticket": None,
        "escalation": None,
        "workflow_trace": [],
        "final_response": "",
        "memory_record": None,
        "llm_response": "",
    }


def _safe_agent_call(func, user_query: str, extra_state: Dict[str, Any] | None = None) -> Any:
    state = _base_state(user_query)

    if extra_state:
        state.update(extra_state)

    attempts = [
        state,
        {"user_query": user_query},
        {"query": user_query},
        {"issue": user_query},
        user_query,
    ]

    last_error = None

    for item in attempts:
        try:
            return func(item)
        except Exception as error:
            last_error = error

    return {
        "status": "failed",
        "error": str(last_error),
        "message": f"{func.__name__} could not process the request.",
    }


def _get_model():
    return ChatGroq(
        model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0,
        timeout=30,
        max_retries=1,
    )


def classify_service_issue(user_query: str) -> str:
    """Classify the user's service desk issue into the correct IT support category."""
    result = _safe_agent_call(classify_issue, user_query)
    return _json_text(result)


def retrieve_service_solution(user_query: str) -> str:
    """Search the knowledge base and vector database for the best solution to the user's issue."""
    result = _safe_agent_call(retrieve_solution, user_query)
    return _json_text(result)


def create_service_ticket(user_query: str) -> str:
    """Create a support ticket when the issue cannot be solved directly."""
    result = _safe_agent_call(
        create_ticket,
        user_query,
        {
            "classification": "support_ticket",
            "retrieval_result": "No complete solution found. Creating ticket.",
        },
    )
    return _json_text(result)


def escalate_service_request(user_query: str) -> str:
    """Escalate unresolved or high-priority service desk issues to the support team."""
    result = _safe_agent_call(
        escalate_issue,
        user_query,
        {
            "classification": "escalation_required",
            "retrieval_result": "Issue requires escalation.",
        },
    )
    return _json_text(result)


def _fallback_response(user_query: str, error: str = "") -> Dict[str, Any]:
    state = _base_state(user_query)

    classification_result = _safe_agent_call(classify_issue, user_query)
    retrieval_result = _safe_agent_call(retrieve_solution, user_query)

    classification_text = _extract_text(classification_result)
    retrieval_text = _extract_text(retrieval_result)

    final_response = (
        "I understand you are facing a service desk issue.\n\n"
        f"Issue: {user_query}\n\n"
        "Suggested steps:\n"
        "1. Restart the affected device or application.\n"
        "2. Check your internet/network connection.\n"
        "3. Try signing out and signing in again.\n"
        "4. If it is a Wi-Fi issue, turn Wi-Fi off and on, forget and reconnect to the network, and restart the network adapter.\n"
        "5. If the issue continues, a support ticket should be created for the IT team.\n\n"
        "This response was generated using the HelpSync AI fallback flow because the LLM supervisor took too long or failed temporarily."
    )

    state.update(
        {
            "route_to": "langgraph_supervisor_fallback",
            "classification": classification_text,
            "retrieval_result": retrieval_text,
            "workflow_trace": [
                "LangGraph Supervisor attempted execution",
                "Supervisor failed or timed out",
                "Fallback service desk flow generated response",
            ],
            "final_response": final_response,
            "llm_response": final_response,
            "error": error,
        }
    )

    try:
        memory_record = save_conversation(state)
        state["memory_record"] = memory_record
    except Exception as save_error:
        state["memory_record"] = {
            "status": "memory_save_failed",
            "error": str(save_error),
        }

    return state


def build_langgraph_supervisor():
    model = _get_model()

    classifier_agent = create_react_agent(
        model=model,
        tools=[classify_service_issue],
        name="classifier_agent",
        prompt=(
            "You are the Classifier Agent for HelpSync AI. "
            "Classify the user issue into a clear IT support category. "
            "Return only the category and short reason."
        ),
    )

    retrieval_agent = create_react_agent(
        model=model,
        tools=[retrieve_service_solution],
        name="retrieval_agent",
        prompt=(
            "You are the Retrieval Agent for HelpSync AI. "
            "Find the best solution from the knowledge base. "
            "Return short step-by-step troubleshooting guidance."
        ),
    )

    ticket_agent = create_react_agent(
        model=model,
        tools=[create_service_ticket],
        name="ticket_agent",
        prompt=(
            "You are the Ticketing Agent for HelpSync AI. "
            "Create a ticket only if the problem cannot be solved immediately."
        ),
    )

    escalation_agent = create_react_agent(
        model=model,
        tools=[escalate_service_request],
        name="escalation_agent",
        prompt=(
            "You are the Escalation Agent for HelpSync AI. "
            "Escalate urgent, repeated, security-related, or high-impact issues."
        ),
    )

    workflow = create_supervisor(
        agents=[
            classifier_agent,
            retrieval_agent,
            ticket_agent,
            escalation_agent,
        ],
        model=model,
        supervisor_name="helpsync_supervisor",
        output_mode="last_message",
        prompt=(
            "You are the LangGraph Supervisor for HelpSync AI. "
            "Handle enterprise service desk issues using the available agents. "
            "First classify the issue. Then retrieve a solution. "
            "If the solution is enough, give a clear final answer. "
            "If the issue cannot be solved, create a ticket. "
            "If the issue is urgent, repeated, security-related, or high impact, escalate it. "
            "Keep the answer short, professional, and step-by-step."
        ),
    )

    return workflow.compile()


_supervisor_app = None


def get_supervisor_app():
    global _supervisor_app

    if _supervisor_app is None:
        _supervisor_app = build_langgraph_supervisor()

    return _supervisor_app


def run_langgraph_supervisor(user_query: str) -> Dict[str, Any]:
    try:
        if not os.getenv("GROQ_API_KEY"):
            return _fallback_response(user_query, "GROQ_API_KEY is missing.")

        app = get_supervisor_app()

        result = app.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_query,
                    }
                ]
            },
            config={"recursion_limit": 8},
        )

        messages = result.get("messages", [])
        final_response = ""

        if messages:
            last_message = messages[-1]
            final_response = getattr(last_message, "content", str(last_message))

        if not final_response:
            final_response = "The issue was processed by HelpSync AI, but no final response was generated."

        final_state = _base_state(user_query)

        final_state.update(
            {
                "route_to": "langgraph_supervisor",
                "classification": "handled_by_langgraph_supervisor",
                "retrieval_result": "",
                "ticket": None,
                "escalation": None,
                "workflow_trace": [
                    "LangGraph Supervisor received user query",
                    "Supervisor delegated work to specialized agents",
                    "Supervisor generated final response",
                ],
                "final_response": final_response,
                "llm_response": final_response,
            }
        )

        try:
            memory_record = save_conversation(final_state)
            final_state["memory_record"] = memory_record
        except Exception as error:
            final_state["memory_record"] = {
                "status": "memory_save_failed",
                "error": str(error),
            }

        return final_state

    except Exception as error:
        return _fallback_response(user_query, str(error))


def run_supervisor_graph(user_query: str) -> Dict[str, Any]:
    return run_langgraph_supervisor(user_query)


def run_supervisor(user_query: str) -> Dict[str, Any]:
    return run_langgraph_supervisor(user_query)


def run_langgraph_workflow(user_query: str) -> Dict[str, Any]:
    return run_langgraph_supervisor(user_query)