# HelpSync AI

**HelpSync AI** is an Enterprise Multi-Agent Service Desk Chatbot built using **FastAPI**, **LangGraph Supervisor Architecture**, and **Streamlit**.

The system accepts employee service desk issues, classifies the issue type, retrieves possible solutions from a knowledge base, creates support tickets, escalates critical issues, stores conversation history, and displays dashboard analytics.

---

## Project Title

**HelpSync AI: An Enterprise Multi-Agent Service Desk Chatbot Using LangGraph Supervisor Architecture**

---

## Problem Statement

Enterprise service desks receive many support requests related to IT, HR, access, software, hardware, and network issues. Traditional helpdesk systems often require manual classification, routing, ticket creation, and escalation.

This project solves the problem by using a multi-agent architecture where different agents handle specific responsibilities and a LangGraph supervisor coordinates the complete workflow.

---

## Objectives

* Build an intelligent service desk chatbot.
* Classify employee issues automatically.
* Retrieve solutions from an internal knowledge base.
* Create support tickets for unresolved or hardware-related issues.
* Escalate urgent and critical issues.
* Store conversation history using a memory layer.
* Provide dashboard analytics for conversations, tickets, and escalations.
* Demonstrate LangGraph-based multi-agent orchestration.

---

## System Architecture

```text
User Interface
     |
     v
FastAPI Backend
     |
     v
LangGraph Supervisor
     |
     |----> Classifier Agent
     |----> Retrieval Agent
     |----> Ticketing Agent
     |----> Escalation Agent
     |----> Memory Agent
     |----> Dashboard Agent
     |
     v
Data and Memory Layer
     |
     |----> Knowledge Base
     |----> Tickets JSON
     |----> Escalations JSON
     |----> Conversation History JSON
```

---

## Agents Used

### 1. Classifier Agent

Classifies the user issue into categories such as:

* Network
* Hardware
* Software
* Access
* HR
* General

It also assigns priority and decides the next route.

### 2. Retrieval Agent

Searches the internal knowledge base and returns a possible solution for known issues.

### 3. Ticketing Agent

Creates a support ticket when the issue requires manual support or no strong solution is found.

### 4. Escalation Agent

Escalates critical issues such as server outage, security breach, or urgent system failures.

### 5. Memory Agent

Stores conversation history including user query, classification, route decision, ticket, escalation, and final response.

### 6. Dashboard Agent

Generates analytics such as total conversations, ticket count, escalation count, issue type count, and priority count.

### 7. LangGraph Supervisor

Coordinates all agents using a graph-based workflow.

---

## Features

* Multi-agent service desk workflow
* LangGraph supervisor architecture
* FastAPI backend
* Streamlit frontend
* Rule-based issue classification
* Knowledge base retrieval
* Automatic ticket creation
* Critical issue escalation
* Conversation memory
* Dashboard analytics
* API testing with Swagger UI

---

## Tech Stack

| Component      | Technology |
| -------------- | ---------- |
| Backend        | FastAPI    |
| Agent Workflow | LangGraph  |
| Frontend       | Streamlit  |
| Language       | Python     |
| API Server     | Uvicorn    |
| Data Storage   | JSON files |
| Validation     | Pydantic   |

---

## Project Structure

```text
HelpSyncAI/
│
├── backend/
│   ├── agents/
│   │   ├── classifier_agent.py
│   │   ├── retrieval_agent.py
│   │   ├── ticketing_agent.py
│   │   ├── escalation_agent.py
│   │   ├── supervisor_agent.py
│   │   ├── langgraph_supervisor.py
│   │   ├── memory_agent.py
│   │   └── dashboard_agent.py
│   │
│   ├── api/
│   │   └── routes.py
│   │
│   ├── data/
│   │   ├── knowledge_base.py
│   │   ├── tickets.json
│   │   ├── escalations.json
│   │   └── conversation_history.json
│   │
│   ├── models/
│   ├── utils/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   └── app.py
│
├── README.md
└── .gitignore
```

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/spg0wda/HelpSync-AI.git
cd HelpSyncAI
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

For Windows Command Prompt:

```bash
venv\Scripts\activate
```

For PowerShell:

```bash
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

---

## Run the Backend

```bash
cd backend
python -m uvicorn main:app --reload
```

Backend will run at:

```text
http://127.0.0.1:8000
```

Swagger API docs:

```text
http://127.0.0.1:8000/docs
```

---

## Run the Frontend

Open a second terminal:

```bash
venv\Scripts\activate
python -m streamlit run frontend/app.py
```

Frontend will run at:

```text
http://localhost:8501
```

---

## API Endpoints

| Method | Endpoint                 | Description                      |
| ------ | ------------------------ | -------------------------------- |
| GET    | `/`                      | Backend health check             |
| POST   | `/chat`                  | Process service desk issue       |
| GET    | `/history`               | View recent conversation history |
| GET    | `/dashboard/stats`       | View dashboard analytics         |
| GET    | `/dashboard/tickets`     | View created tickets             |
| GET    | `/dashboard/escalations` | View escalated issues            |

---

## Example Queries

```text
My laptop is not connecting to WiFi
I forgot my password and cannot login
My laptop screen is broken
Urgent server is down for everyone
Payroll salary is not received
The application keeps crashing
I need VPN access for remote work
```

---

## Example Workflow

### Input

```text
Urgent server is down for everyone
```

### Output Flow

```text
Classifier Agent
    ↓
Ticketing Agent
    ↓
Escalation Agent
    ↓
Memory Agent
    ↓
Final Response
```

### Final Response

```text
Your issue has been classified as Network with Critical priority.
A ticket has been created and escalated successfully.
```

---

## Current Project Status

* FastAPI backend completed
* Classifier Agent completed
* Retrieval Agent completed
* Ticketing Agent completed
* Escalation Agent completed
* LangGraph Supervisor completed
* Conversation Memory completed
* Dashboard APIs completed
* Streamlit frontend completed

---

## Future Enhancements

* Add user authentication
* Add role-based dashboard
* Add database support using PostgreSQL or MySQL
* Add LLM-based classification
* Add vector database retrieval using ChromaDB
* Add email notification for escalations
* Add admin panel for ticket updates
* Add Docker deployment
* Add cloud deployment
* Add voice-based support interface

---

## Author

**Shiv Prakash**

---

## License

This project is created for academic and learning purposes.
