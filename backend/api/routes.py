from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
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
    get_feedback_summary,
    get_learning_insights
)
from agents.auth_agent import (
    register_user,
    login_user,
    get_current_active_user
)
from data.chroma_store import seed_knowledge_base, reset_knowledge_base
from data.postgres_store import (
    init_postgres_tables,
    get_postgres_status,
    get_recent_postgres_conversations
)


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


class RegisterRequest(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/auth/register")
def auth_register(request: RegisterRequest):
    result = register_user(
        username=request.username,
        email=request.email,
        full_name=request.full_name,
        password=request.password
    )

    if not result.get("registered"):
        raise HTTPException(
            status_code=400,
            detail=result.get("message")
        )

    return {
        "current_stage": "Phase 20 - Human Feedback Dashboard",
        **result
    }


@router.post("/auth/login")
def auth_login(request: LoginRequest):
    result = login_user(
        username=request.username,
        password=request.password
    )

    if not result.get("logged_in"):
        raise HTTPException(
            status_code=401,
            detail=result.get("message")
        )

    return {
        "current_stage": "Phase 20 - Human Feedback Dashboard",
        **result
    }


@router.post("/auth/token")
def auth_token(form_data: OAuth2PasswordRequestForm = Depends()):
    result = login_user(
        username=form_data.username,
        password=form_data.password
    )

    if not result.get("logged_in"):
        raise HTTPException(
            status_code=401,
            detail=result.get("message")
        )

    return {
        "access_token": result.get("access_token"),
        "token_type": "bearer"
    }


@router.get("/auth/me")
def auth_me(current_user: dict = Depends(get_current_active_user)):
    return {
        "current_stage": "Phase 20 - Human Feedback Dashboard",
        "user": current_user
    }


@router.post("/chat")
def chat(request: ChatRequest):
    result = run_langgraph_workflow(request.user_query)

    return {
        "current_stage": "Phase 20 - Human Feedback Dashboard",
        **result
    }


@router.post("/secure/chat")
def secure_chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_active_user)
):
    result = run_langgraph_workflow(request.user_query)

    return {
        "current_stage": "Phase 20 - Human Feedback Dashboard",
        "authenticated_user": current_user,
        **result
    }


@router.get("/history")
def history():
    conversations = get_recent_conversations(limit=10)

    return {
        "current_stage": "Phase 20 - Human Feedback Dashboard",
        "total_returned": len(conversations),
        "conversations": conversations
    }


@router.get("/dashboard/stats")
def dashboard_stats():
    stats = get_dashboard_stats()

    return {
        "current_stage": "Phase 20 - Human Feedback Dashboard",
        "dashboard": stats
    }


@router.get("/dashboard/tickets")
def dashboard_tickets():
    tickets = get_all_tickets()

    return {
        "current_stage": "Phase 20 - Human Feedback Dashboard",
        "total_tickets": len(tickets),
        "tickets": tickets
    }


@router.get("/dashboard/escalations")
def dashboard_escalations():
    escalations = get_all_escalations()

    return {
        "current_stage": "Phase 20 - Human Feedback Dashboard",
        "total_escalations": len(escalations),
        "escalations": escalations
    }


@router.post("/reports/generate")
def generate_report(request: ReportRequest):
    report = generate_service_report(request.conversation_id)

    return {
        "current_stage": "Phase 20 - Human Feedback Dashboard",
        "report": report
    }


@router.get("/reports")
def reports():
    all_reports = get_all_reports()

    return {
        "current_stage": "Phase 20 - Human Feedback Dashboard",
        "total_reports": len(all_reports),
        "reports": all_reports
    }


@router.post("/feedback")
def submit_feedback(request: FeedbackRequest):
    feedback = create_feedback(
        conversation_id=request.conversation_id,
        helpful=request.helpful,
        rating=request.rating,
        comment=request.comment,
        improvement_suggestion=request.improvement_suggestion
    )

    return {
        "current_stage": "Phase 20 - Human Feedback Dashboard",
        "message": "Feedback submitted successfully.",
        "feedback": feedback
    }


@router.get("/feedback")
def feedback_records():
    feedback = get_all_feedback()
    summary = get_feedback_summary()

    return {
        "current_stage": "Phase 20 - Human Feedback Dashboard",
        "summary": summary,
        "total_feedback": len(feedback),
        "feedback": feedback
    }


@router.get("/feedback/insights")
def feedback_insights():
    insights = get_learning_insights()

    return {
        "current_stage": "Phase 20 - Human Feedback Dashboard",
        "insights": insights
    }


@router.post("/vector/seed")
def seed_vector_database():
    result = seed_knowledge_base()

    return {
        "current_stage": "Phase 20 - Human Feedback Dashboard",
        "result": result
    }


@router.post("/vector/reset")
def reset_vector_database():
    result = reset_knowledge_base()

    return {
        "current_stage": "Phase 20 - Human Feedback Dashboard",
        "result": result
    }


@router.post("/postgres/init")
def postgres_init():
    result = init_postgres_tables()

    return {
        "current_stage": "Phase 20 - Human Feedback Dashboard",
        "result": result
    }


@router.get("/postgres/status")
def postgres_status():
    result = get_postgres_status()

    return {
        "current_stage": "Phase 20 - Human Feedback Dashboard",
        "result": result
    }


@router.get("/postgres/conversations")
def postgres_conversations():
    conversations = get_recent_postgres_conversations(limit=10)

    return {
        "current_stage": "Phase 20 - Human Feedback Dashboard",
        "total_returned": len(conversations),
        "conversations": conversations
    }