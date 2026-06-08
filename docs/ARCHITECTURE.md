# 🤖 HelpSync AI Architecture Documentation

## 🏷️ Title

**HelpSync AI: Enterprise Multi-Agent Service Desk Chatbot using LangGraph Supervisor Architecture**

---

## 1. 📌 Introduction

HelpSync AI is an enterprise service desk chatbot designed using a multi-agent architecture. The system uses LangGraph as the supervisor workflow engine to coordinate different AI agents.

The main goal of the system is to automate service desk operations such as issue classification, knowledge retrieval, ticket creation, escalation, feedback collection, reporting, and learning from feedback.

---

## 2. ❗ Problem Statement

Traditional service desk systems require manual ticket classification, manual troubleshooting, and repeated support interactions. This leads to delays, inconsistent responses, and increased workload for support teams.

HelpSync AI solves this by using an intelligent multi-agent system that can automatically understand user issues, retrieve solutions, create tickets, escalate complex problems, and improve from feedback.

---

## 3. 💡 Proposed System

The proposed system is an AI-powered service desk chatbot where the user interacts through a Streamlit frontend. The backend is built using FastAPI. LangGraph manages the agent workflow. ChromaDB is used for vector search. PostgreSQL stores user and conversation records. LangSmith monitors the AI workflow.

---

## 4. 🏗️ Architecture Layers

```text
User Interface Layer
    Streamlit Web App

API Layer
    FastAPI Backend

Supervisor Layer
    LangGraph Supervisor Agent

Agent Layer
    Classifier Agent
    Retrieval Agent
    Ticketing Agent
    Escalation Agent
    Memory Agent
    Report Agent
    Feedback Agent
    Learning Agent
    LLM Response Agent

Data Layer
    PostgreSQL
    ChromaDB
    JSON Storage

Monitoring Layer
    LangSmith

Deployment Layer
    Docker
```

---

## 5. 🤖 Agent Responsibilities

### 5.1 Classifier Agent

The classifier agent identifies the type of issue submitted by the user. It helps the supervisor decide which agent should handle the request next.

Example categories:

* Network issue
* Login issue
* Hardware issue
* Software issue
* Email issue
* VPN issue

---

### 5.2 Retrieval Agent

The retrieval agent searches the knowledge base for a possible solution. It uses ChromaDB vector search and approved learning notes.

If a solution is found, the system responds to the user. If no solution is found, the workflow moves to ticket creation.

---

### 5.3 Ticketing Agent

The ticketing agent creates a support ticket when the issue cannot be solved directly.

The ticket includes:

* Ticket ID
* Issue type
* User query
* Priority
* Status
* Created time

---

### 5.4 Escalation Agent

The escalation agent handles critical or unresolved issues. It marks the issue for higher-level human support.

Escalation is useful for:

* Critical failures
* Repeated issues
* Unresolved tickets
* High-priority service requests

---

### 5.5 Memory Agent

The memory agent stores conversations so that the system can maintain history.

Conversation data is stored in:

* JSON files
* PostgreSQL database

---

### 5.6 Report Agent

The report agent generates service desk reports based on conversations, tickets, escalations, and feedback.

---

### 5.7 Feedback Agent

The feedback agent collects user feedback after service interactions.

It stores:

* Rating
* Helpful or not helpful response
* User comment
* Improvement suggestion

---

### 5.8 Learning Agent

The learning agent analyzes low-rated feedback and improvement suggestions.

It generates learning notes that can be reviewed and applied. Approved learning notes are used by the retrieval agent to improve future responses.

---

### 5.9 LLM Response Agent

The LLM response agent uses Groq API to polish final responses and make them more helpful and user-friendly.

---

## 6. 🔁 Workflow

```text
User submits issue
        |
FastAPI receives request
        |
LangGraph Supervisor starts workflow
        |
Classifier Agent classifies issue
        |
Retrieval Agent searches solution
        |
If solution found:
        Return final response
Else:
        Ticketing Agent creates ticket
        |
        Escalation Agent escalates if needed
        |
Memory Agent saves conversation
        |
LLM Response Agent polishes response
        |
User receives response
        |
User submits feedback
        |
Learning Agent generates improvement notes
```

---

## 7. 🔄 Data Flow

```text
User Query
   |
Streamlit Frontend
   |
FastAPI Backend
   |
LangGraph Supervisor
   |
Agents
   |
PostgreSQL + JSON + ChromaDB
   |
Response
   |
Frontend
```

---

## 8. 🗄️ Database Design

### Users Table

Stores registered users.

Fields:

* id
* username
* email
* full_name
* hashed_password
* role
* is_active
* created_at

### Conversations Table

Stores conversation records.

Fields:

* id
* conversation_id
* user_query
* classification
* route_to
* retrieval_result
* ticket
* escalation
* final_response
* raw_record
* created_at

---

## 9. 🔐 Security Design

The system uses JWT authentication.

Security features:

* Password hashing
* JWT access token
* Protected secure chat endpoint
* Protected learning loop endpoints
* User session management in Streamlit

---

## 10. 🧠 Feedback Learning Design

Feedback is used to improve the system.

Process:

1. User submits feedback.
2. Feedback Agent stores feedback.
3. Learning Agent checks low ratings and suggestions.
4. Learning notes are generated.
5. User/admin applies useful learning notes.
6. Retrieval Agent uses approved notes in future responses.

---

## 11. 🐳 Deployment Design

Docker Compose runs:

* PostgreSQL container
* FastAPI backend container
* Streamlit frontend container

Command:

```bash
docker compose up --build
```

---

## 12. ✅ Advantages

* Reduces manual service desk workload
* Provides faster responses
* Creates tickets automatically
* Supports escalation
* Learns from feedback
* Provides dashboard and reports
* Uses secure authentication
* Supports Docker deployment
* Easy to extend with more agents

---

## 13. ⚠️ Limitations

* Current learning loop is approval-based, not fully automatic knowledge rewriting
* Email and Slack integration are not added yet
* Admin role management can be improved
* Cloud deployment is still pending
* Large-scale production deployment requires stronger security and monitoring

---

## 14. 🔮 Future Scope

* Admin dashboard
* Role-based access control
* Email notifications
* Slack or Teams integration
* PDF report download
* Cloud deployment
* Better analytics
* Real-time chat streaming
* Organization-wise multi-tenant support

---
