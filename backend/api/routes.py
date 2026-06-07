from fastapi import APIRouter
from pydantic import BaseModel

from agents.langgraph_supervisor import run_langgraph_workflow
from agents.memory_agent import get_recent_conversations
from agents.dashboard_agent import (
    get_dashboard_stats,
    get_all_tickets,
    get_all_escalations
)
from agents.report_agent import generate_service_report, get_all_reports
from agents.feedback_agent import (
    create_feedback,
    get_all_feedback,
    get_feedback_summary
)
from data.chroma_store import seed_knowledge_base, reset_knowledge_base

router = APIRouter()


class ChatRequest(BaseModel):
    user_query: str


class ReportRequest(BaseModel):
    conversation_id: str | None = None

class FeedbackRequest(BaseModel):
    conversation_id: str | None = None
    helpful: bool
    rating: int
    comment: str = ""
    improvement_suggestion: str = ""

@router.post("/chat")
def chat(request: ChatRequest):
    """
    Main chat endpoint.
    Sends user query into the LangGraph multi-agent workflow.
    """

    result = run_langgraph_workflow(request.user_query)

    return {
        "current_stage": "Phase 12 - Final Report Generator",
        **result
    }


@router.get("/history")
def history():
    """
    Returns recent conversation history stored by Memory Agent.
    """

    conversations = get_recent_conversations(limit=10)

    return {
        "current_stage": "Phase 12 - Final Report Generator",
        "total_returned": len(conversations),
        "conversations": conversations
    }


@router.get("/dashboard/stats")
def dashboard_stats():
    """
    Returns dashboard analytics.
    """

    stats = get_dashboard_stats()

    return {
        "current_stage": "Phase 12 - Final Report Generator",
        "dashboard": stats
    }


@router.get("/dashboard/tickets")
def dashboard_tickets():
    """
    Returns all created support tickets.
    """

    tickets = get_all_tickets()

    return {
        "current_stage": "Phase 12 - Final Report Generator",
        "total_tickets": len(tickets),
        "tickets": tickets
    }


@router.get("/dashboard/escalations")
def dashboard_escalations():
    """
    Returns all escalation records.
    """

    escalations = get_all_escalations()

    return {
        "current_stage": "Phase 12 - Final Report Generator",
        "total_escalations": len(escalations),
        "escalations": escalations
    }


@router.post("/reports/generate")
def generate_report(request: ReportRequest):
    """
    Generates a final service desk report.
    If conversation_id is null, it generates a report for the latest conversation.
    """

    report = generate_service_report(request.conversation_id)

    return {
        "current_stage": "Phase 12 - Final Report Generator",
        "report": report
    }


@router.get("/reports")
def reports():
    """
    Returns all generated reports.
    """

    all_reports = get_all_reports()

    return {
        "current_stage": "Phase 12 - Final Report Generator",
        "total_reports": len(all_reports),
        "reports": all_reports
    }
@router.post("/feedback")
def submit_feedback(request: FeedbackRequest):
    """
    Stores human feedback for a conversation.
    """

    feedback = create_feedback(
        conversation_id=request.conversation_id,
        helpful=request.helpful,
        rating=request.rating,
        comment=request.comment,
        improvement_suggestion=request.improvement_suggestion
    )

    return {
        "current_stage": "Phase 13 - Human Feedback and Learning Loop",
        "message": "Feedback submitted successfully.",
        "feedback": feedback
    }


@router.get("/feedback")
def feedback_records():
    """
    Returns all feedback records and summary.
    """

    feedback = get_all_feedback()
    summary = get_feedback_summary()

    return {
        "current_stage": "Phase 13 - Human Feedback and Learning Loop",
        "summary": summary,
        "total_feedback": len(feedback),
        "feedback": feedback
    }
@router.post("/vector/seed")
def seed_vector_database():
    result = seed_knowledge_base()

    return {
        "current_stage": "Phase 15 - ChromaDB Vector Retrieval",
        "result": result
    }


@router.post("/vector/reset")
def reset_vector_database():
    result = reset_knowledge_base()

    return {
        "current_stage": "Phase 15 - ChromaDB Vector Retrieval",
        "result": result
    }