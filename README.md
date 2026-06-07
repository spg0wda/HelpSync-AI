# HelpSync AI

HelpSync AI is an Enterprise Multi-Agent Service Desk Chatbot built using FastAPI and LangGraph Supervisor Architecture.

## Features

- Classifier Agent
- Retrieval Agent
- Ticketing Agent
- Escalation Agent
- LangGraph Supervisor Workflow
- Knowledge Base Retrieval
- Ticket and Escalation Tracking

## Tech Stack

- Python
- FastAPI
- LangGraph
- Uvicorn
- Pydantic

## Project Structure

```text
HelpSyncAI/
├── backend/
│   ├── agents/
│   ├── api/
│   ├── data/
│   ├── models/
│   ├── utils/
│   ├── main.py
│   └── requirements.txt
├── frontend/
└── README.md

## Example Queries

You can test the chatbot using these sample service desk issues:

- My laptop is not connecting to WiFi
- I forgot my password and cannot login
- My laptop screen is broken
- Urgent server is down for everyone
- Payroll salary is not received
- The application keeps crashing
- I need VPN access for remote work