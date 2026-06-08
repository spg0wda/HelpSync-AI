# 🤖 HelpSync AI

**Enterprise Multi-Agent Service Desk Chatbot using LangGraph Supervisor Architecture**

HelpSync AI is an AI-powered enterprise service desk assistant that uses a multi-agent architecture to classify user issues, retrieve solutions, create tickets, escalate unresolved problems, collect feedback, generate reports, monitor workflows, and learn from user feedback.

The system is built using **FastAPI, LangGraph, ChromaDB, Groq API, LangSmith, PostgreSQL, JWT Authentication, Streamlit, and Docker**.

---

## 📌 Project Overview

HelpSync AI acts like an intelligent IT/service desk assistant for organizations. A user can log in, submit an issue, and the system automatically routes the request through different agents.

The supervisor agent decides whether the request should be handled by retrieval, ticketing, escalation, memory, reporting, or feedback-based learning.

---

## 🚀 Key Features

* Secure user registration and login
* JWT-based authentication
* LangGraph supervisor workflow
* Multi-agent routing system
* Issue classification agent
* Vector retrieval using ChromaDB
* Groq-powered LLM response generation
* Ticket creation system
* Escalation handling
* Conversation memory
* PostgreSQL database storage
* Feedback collection
* Feedback analytics dashboard
* Autonomous learning loop
* LangSmith monitoring
* Streamlit professional UI
* Docker deployment support

---

## 🛠️ Tech Stack

| Layer            | Technology |
| ---------------- | ---------- |
| Backend          | FastAPI    |
| Frontend         | Streamlit  |
| Agent Framework  | LangGraph  |
| LLM Provider     | Groq       |
| Vector Database  | ChromaDB   |
| Database         | PostgreSQL |
| Authentication   | JWT        |
| Monitoring       | LangSmith  |
| Containerization | Docker     |
| Language         | Python     |

---

## 🏗️ System Architecture

```text
User
 |
 |  Streamlit UI
 |
FastAPI Backend
 |
LangGraph Supervisor Agent
 |
 |-- Classifier Agent
 |-- Retrieval Agent
 |     |-- ChromaDB Vector Search
 |     |-- Approved Learning Notes
 |
 |-- Ticketing Agent
 |-- Escalation Agent
 |-- Memory Agent
 |-- Report Agent
 |-- Feedback Agent
 |-- Autonomous Learning Agent
 |-- LLM Response Agent
 |
PostgreSQL + JSON Storage + LangSmith Monitoring
```

---

## 🔁 Multi-Agent Workflow

1. User logs in using JWT authentication.
2. User submits an issue from the Streamlit UI.
3. FastAPI receives the request.
4. LangGraph Supervisor starts the workflow.
5. Classifier Agent identifies the issue category.
6. Retrieval Agent searches ChromaDB and approved learning notes.
7. If a solution is found, the system returns a response.
8. If no solution is found, Ticketing Agent creates a ticket.
9. If the issue is critical, Escalation Agent escalates it.
10. Memory Agent stores the conversation.
11. PostgreSQL stores conversation and user data.
12. Feedback Agent collects user feedback.
13. Learning Agent generates improvement notes from feedback.
14. LangSmith monitors workflow traces.

---

## 📁 Project Structure

```text
HelpSyncAI/
├── backend/
│   ├── agents/
│   │   ├── auth_agent.py
│   │   ├── classifier_agent.py
│   │   ├── dashboard_agent.py
│   │   ├── escalation_agent.py
│   │   ├── feedback_agent.py
│   │   ├── langgraph_supervisor.py
│   │   ├── learning_agent.py
│   │   ├── llm_response_agent.py
│   │   ├── memory_agent.py
│   │   ├── report_agent.py
│   │   ├── retrieval_agent.py
│   │   ├── supervisor_agent.py
│   │   └── ticketing_agent.py
│   │
│   ├── api/
│   │   └── routes.py
│   │
│   ├── data/
│   │   ├── chroma_store.py
│   │   ├── knowledge_base.py
│   │   ├── conversation_history.json
│   │   ├── tickets.json
│   │   ├── escalations.json
│   │   ├── feedback.json
│   │   ├── learning_notes.json
│   │   ├── approved_learning_notes.json
│   │   ├── reports.json
│   │   └── postgres_store.py
│   │
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── .env
└── README.md
```

---

## 🔌 Backend API Endpoints

### 🔐 Authentication

| Method | Endpoint         | Description                    |
| ------ | ---------------- | ------------------------------ |
| POST   | `/auth/register` | Register a new user            |
| POST   | `/auth/login`    | Login and receive JWT token    |
| POST   | `/auth/token`    | OAuth2 compatible login        |
| GET    | `/auth/me`       | Get current authenticated user |

### 💬 Chat

| Method | Endpoint       | Description                        |
| ------ | -------------- | ---------------------------------- |
| POST   | `/chat`        | Public chat endpoint               |
| POST   | `/secure/chat` | Secure JWT-protected chat endpoint |

### 📊 Dashboard

| Method | Endpoint                 | Description              |
| ------ | ------------------------ | ------------------------ |
| GET    | `/dashboard/stats`       | Get dashboard statistics |
| GET    | `/dashboard/tickets`     | Get all tickets          |
| GET    | `/dashboard/escalations` | Get all escalations      |

### 🕘 History

| Method | Endpoint   | Description              |
| ------ | ---------- | ------------------------ |
| GET    | `/history` | Get recent conversations |

### 📄 Reports

| Method | Endpoint            | Description             |
| ------ | ------------------- | ----------------------- |
| POST   | `/reports/generate` | Generate service report |
| GET    | `/reports`          | Get all reports         |

### ⭐ Feedback

| Method | Endpoint             | Description            |
| ------ | -------------------- | ---------------------- |
| POST   | `/feedback`          | Submit user feedback   |
| GET    | `/feedback`          | Get feedback records   |
| GET    | `/feedback/insights` | Get feedback analytics |

### 🧠 Learning Loop

| Method | Endpoint             | Description                           |
| ------ | -------------------- | ------------------------------------- |
| GET    | `/learning/summary`  | Get learning loop summary             |
| POST   | `/learning/generate` | Generate learning notes from feedback |
| POST   | `/learning/run`      | Run autonomous learning loop          |
| GET    | `/learning/notes`    | Get all learning notes                |
| GET    | `/learning/pending`  | Get pending learning notes            |
| GET    | `/learning/applied`  | Get applied learning notes            |
| POST   | `/learning/apply`    | Apply a learning note                 |

### 🧬 Vector Database

| Method | Endpoint        | Description                   |
| ------ | --------------- | ----------------------------- |
| POST   | `/vector/seed`  | Seed ChromaDB vector database |
| POST   | `/vector/reset` | Reset vector database         |

### 🐘 PostgreSQL

| Method | Endpoint                  | Description                  |
| ------ | ------------------------- | ---------------------------- |
| POST   | `/postgres/init`          | Initialize PostgreSQL tables |
| GET    | `/postgres/status`        | Check PostgreSQL status      |
| GET    | `/postgres/conversations` | Get PostgreSQL conversations |

---

## ⚙️ Local Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd HelpSyncAI
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### 4. Install Backend Dependencies

```bash
pip install -r backend/requirements.txt
```

### 5. Install Frontend Dependencies

```bash
pip install -r frontend/requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the root folder.

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant

LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=HelpSync-AI

DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/helpsync_ai

JWT_SECRET_KEY=your_generated_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Do not push `.env` to GitHub.

---

## ▶️ Run Backend Locally

```bash
cd backend
..\venv\Scripts\activate
python -m uvicorn main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

Swagger API docs:

```text
http://127.0.0.1:8000/docs
```

---

## 🖥️ Run Frontend Locally

Open a new terminal:

```bash
cd HelpSyncAI
venv\Scripts\activate
python -m streamlit run frontend\app.py
```

Frontend runs at:

```text
http://localhost:8501
```

---

## 🐳 Docker Setup

Make sure Docker Desktop is installed and running.

Run:

```bash
docker compose up --build
```

Frontend:

```text
http://localhost:8501
```

Backend:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

Stop Docker containers:

```bash
docker compose down
```

Stop and remove volumes:

```bash
docker compose down -v
```

---

## ✅ How to Test

1. Open Streamlit frontend.
2. Register a new user.
3. Login with username and password.
4. Go to Chat tab.
5. Submit an issue such as:

```text
I cannot connect to office wireless network
```

6. Check the final response.
7. Open Dashboard tab.
8. Check tickets and escalations.
9. Submit feedback.
10. Open Learning Loop tab.
11. Generate learning notes.
12. Apply a learning note.
13. Ask a similar question again.
14. Check PostgreSQL status and conversation records.

---

## 🧪 Example Test Queries

```text
I cannot connect to office wireless network
```

```text
My VPN is not working
```

```text
I forgot my password and cannot login
```

```text
My laptop is very slow
```

```text
Email is not syncing in Outlook
```

---

## 🖼️ Screenshots to Add

Add screenshots in GitHub later for:

* Login page
* Secure chat
* Dashboard
* Tickets
* Feedback dashboard
* Learning loop
* LangSmith trace
* Docker containers

---

## 🌟 Project Highlights

This project demonstrates:

* Multi-agent AI architecture
* LangGraph workflow orchestration
* Real-time service desk automation
* Vector search-based retrieval
* Secure authentication
* Database integration
* Human feedback learning
* Autonomous learning loop
* Monitoring with LangSmith
* Docker-based deployment

---

## 🔮 Future Enhancements

* Role-based admin dashboard
* Email notification support
* Slack or Microsoft Teams integration
* PDF report export
* Advanced analytics charts
* Cloud deployment
* Real-time websocket chat
* Organization-wise user management
* Admin approval workflow for learning notes

---

## 👨‍💻 Author

**Shiv Prakash**

Project: **HelpSync AI**

---
