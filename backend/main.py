from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="HelpSync AI",
    description="Enterprise Multi-Agent Service Desk Chatbot using LangGraph Supervisor Architecture",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "HelpSync AI backend is running successfully",
        "project": "Enterprise Multi-Agent Service Desk Chatbot",
        "status": "active"
    }