# 🎬 HelpSync AI Demo Script

## Demo Title

**HelpSync AI: Enterprise Multi-Agent Service Desk Chatbot using LangGraph Supervisor Architecture**

---

## 1. Introduction

Hello everyone, my project is **HelpSync AI**, an enterprise multi-agent service desk chatbot.

It helps users raise IT/service desk issues, automatically classifies the problem, searches for solutions, creates tickets, escalates unresolved issues, collects feedback, and improves using an autonomous learning loop.

The project uses **FastAPI, LangGraph, ChromaDB, Groq API, LangSmith, PostgreSQL, JWT Authentication, Streamlit, and Docker**.

---

## 2. Start the Project

First, I will run the full project using Docker.

```bash
docker compose up --build
```

This starts:

* PostgreSQL database
* FastAPI backend
* Streamlit frontend

Frontend runs on:

```text
http://localhost:8501
```

Backend Swagger runs on:

```text
http://localhost:8000/docs
```

---

## 3. User Authentication Demo

Now I will open the Streamlit UI.

First, I register a new user.

Then I login using username and password.

The system uses **JWT authentication**, so secure APIs can only be accessed after login.

---

## 4. Secure Chat Demo

Now I will submit an IT issue:

```text
I cannot connect to office wireless network
```

The request goes to the secure chat endpoint.

The **LangGraph Supervisor Agent** starts the workflow.

It routes the request through different agents:

* Classifier Agent
* Retrieval Agent
* Ticketing Agent
* Escalation Agent
* Memory Agent
* LLM Response Agent

---

## 5. Multi-Agent Workflow Explanation

The Classifier Agent identifies the issue type.

The Retrieval Agent searches the knowledge base using ChromaDB vector search.

If a solution is found, the chatbot responds directly.

If no solution is found, the Ticketing Agent creates a support ticket.

If the issue is critical, the Escalation Agent escalates it.

The Memory Agent stores the conversation.

The LLM Response Agent improves the final response using Groq.

---

## 6. Dashboard Demo

Next, I will open the Dashboard tab.

Here we can see:

* Total conversations
* Total tickets
* Total escalations
* Total feedback records
* PostgreSQL status

This shows that the system is not just a chatbot, but a complete service desk platform.

---

## 7. Ticket and Escalation Demo

Now I will open the Tickets tab.

Here we can see automatically created tickets and escalations.

Each ticket contains:

* Ticket ID
* Issue type
* Priority
* Status
* Created time

---

## 8. Feedback Dashboard Demo

Next, I will open the Feedback tab.

I will submit feedback for the chatbot response.

The feedback dashboard shows:

* Total feedback
* Average rating
* Helpful count
* Not helpful count
* Rating distribution
* Improvement suggestions
* Learning actions

---

## 9. Autonomous Learning Loop Demo

Now I will open the Learning Loop tab.

When low-rated feedback is submitted, the Learning Agent generates learning notes.

These notes can be reviewed and applied.

Once applied, approved learning notes help the Retrieval Agent improve future responses.

This makes the system closer to a self-learning multi-agent service desk assistant.

---

## 10. LangSmith Monitoring Demo

The project also uses LangSmith monitoring.

LangSmith helps trace the LangGraph workflow and shows how each agent executed.

This is useful for debugging, monitoring, and explaining the AI workflow.

---

## 11. PostgreSQL and Docker Demo

The project stores users and conversations in PostgreSQL.

Docker Compose runs the full system with one command.

This makes the project easier to run, test, and deploy.

---

## 12. Conclusion

HelpSync AI demonstrates a complete enterprise-ready multi-agent service desk chatbot.

It includes:

* Multi-agent architecture
* LangGraph supervisor workflow
* Vector search
* LLM response generation
* Authentication
* PostgreSQL database
* Feedback analytics
* Autonomous learning loop
* Monitoring
* Docker deployment

Thank you.
