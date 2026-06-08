import requests
import streamlit as st


API_BASE_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="HelpSync AI",
    page_icon="🤖",
    layout="wide"
)


if "access_token" not in st.session_state:
    st.session_state.access_token = None

if "user" not in st.session_state:
    st.session_state.user = None

if "last_conversation_id" not in st.session_state:
    st.session_state.last_conversation_id = None


st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #020617 0%, #0f172a 45%, #111827 100%);
        color: #e5e7eb;
    }

    section[data-testid="stSidebar"] {
        background-color: #020617;
        border-right: 1px solid #1f2937;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 5px;
    }

    .sub-title {
        font-size: 17px;
        color: #94a3b8;
        margin-bottom: 25px;
    }

    .card {
        background: rgba(15, 23, 42, 0.95);
        border: 1px solid #1e293b;
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 18px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.35);
    }

    .success-card {
        background: rgba(6, 78, 59, 0.35);
        border: 1px solid #10b981;
        border-radius: 15px;
        padding: 16px;
        color: #d1fae5;
    }

    .error-card {
        background: rgba(127, 29, 29, 0.35);
        border: 1px solid #ef4444;
        border-radius: 15px;
        padding: 16px;
        color: #fee2e2;
    }

    .small-muted {
        color: #94a3b8;
        font-size: 14px;
    }

    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.95);
        border: 1px solid #1e293b;
        padding: 18px;
        border-radius: 16px;
    }

    .stTextInput input, .stTextArea textarea {
        background-color: #020617;
        color: #f8fafc;
        border: 1px solid #334155;
    }

    .stSelectbox div {
        color: #f8fafc;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def get_auth_headers():
    if st.session_state.access_token:
        return {
            "Authorization": f"Bearer {st.session_state.access_token}"
        }
    return {}


def api_get(path, auth=False):
    headers = get_auth_headers() if auth else {}

    try:
        response = requests.get(
            f"{API_BASE_URL}{path}",
            headers=headers,
            timeout=30
        )

        try:
            data = response.json()
        except Exception:
            data = {"detail": response.text}

        return response.status_code, data

    except Exception as error:
        return 500, {"detail": str(error)}


def api_post(path, payload=None, auth=False):
    headers = get_auth_headers() if auth else {}

    try:
        response = requests.post(
            f"{API_BASE_URL}{path}",
            json=payload or {},
            headers=headers,
            timeout=60
        )

        try:
            data = response.json()
        except Exception:
            data = {"detail": response.text}

        return response.status_code, data

    except Exception as error:
        return 500, {"detail": str(error)}


def login_user(username, password):
    status, data = api_post(
        "/auth/login",
        {
            "username": username,
            "password": password
        }
    )

    if status == 200 and data.get("access_token"):
        st.session_state.access_token = data.get("access_token")
        st.session_state.user = data.get("user")
        return True, data

    return False, data


def register_user(username, email, full_name, password):
    status, data = api_post(
        "/auth/register",
        {
            "username": username,
            "email": email,
            "full_name": full_name,
            "password": password
        }
    )

    return status == 200, data


def logout_user():
    st.session_state.access_token = None
    st.session_state.user = None
    st.session_state.last_conversation_id = None
    st.rerun()


def render_json_card(title, data):
    with st.expander(title, expanded=False):
        st.json(data)


with st.sidebar:
    st.markdown("## 🤖 HelpSync AI")
    st.markdown('<p class="small-muted">Enterprise Service Desk Assistant</p>', unsafe_allow_html=True)

    st.divider()

    if st.session_state.user:
        st.success(f"Logged in as {st.session_state.user.get('username')}")
        st.caption(f"Role: {st.session_state.user.get('role')}")

        if st.button("Logout", use_container_width=True):
            logout_user()

    else:
        auth_mode = st.radio(
            "Account",
            ["Login", "Register"],
            horizontal=True
        )

        if auth_mode == "Login":
            st.markdown("### Login")

            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login", use_container_width=True):
                success, result = login_user(login_username, login_password)

                if success:
                    st.success("Login successful")
                    st.rerun()
                else:
                    st.error(result.get("detail", result.get("message", "Login failed")))

        else:
            st.markdown("### Register")

            reg_username = st.text_input("Username", key="reg_username")
            reg_email = st.text_input("Email", key="reg_email")
            reg_full_name = st.text_input("Full Name", key="reg_full_name")
            reg_password = st.text_input("Password", type="password", key="reg_password")

            if st.button("Create Account", use_container_width=True):
                success, result = register_user(
                    reg_username,
                    reg_email,
                    reg_full_name,
                    reg_password
                )

                if success:
                    st.success("Account created. Now login.")
                else:
                    st.error(result.get("detail", result.get("message", "Registration failed")))

    st.divider()
    st.caption("FastAPI + LangGraph + ChromaDB + Groq + LangSmith + PostgreSQL + JWT")


st.markdown('<div class="main-title">HelpSync AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Enterprise Multi-Agent Service Desk Chatbot using LangGraph Supervisor Architecture</div>',
    unsafe_allow_html=True
)


if not st.session_state.user:
    st.markdown(
        """
        <div class="card">
            <h3>🔐 Login Required</h3>
            <p class="small-muted">
                Please login or create an account from the sidebar to access HelpSync AI.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Authentication", "JWT")
    with col2:
        st.metric("Database", "PostgreSQL")
    with col3:
        st.metric("Supervisor", "LangGraph")

    st.stop()


tab_chat, tab_dashboard, tab_tickets, tab_history, tab_reports, tab_feedback = st.tabs(
    [
        "💬 Chat",
        "📊 Dashboard",
        "🎫 Tickets",
        "🕘 History",
        "📄 Reports",
        "⭐ Feedback"
    ]
)


with tab_chat:
    st.markdown("### 💬 Secure Service Desk Chat")

    user_query = st.text_area(
        "Describe your issue",
        placeholder="Example: I cannot connect to office wireless network",
        height=120
    )

    if st.button("Send to HelpSync AI", use_container_width=True):
        if not user_query.strip():
            st.warning("Please enter your issue.")
        else:
            with st.spinner("LangGraph Supervisor is routing your request..."):
                status, result = api_post(
                    "/secure/chat",
                    {"user_query": user_query},
                    auth=True
                )

            if status == 200:
                st.markdown(
                    """
                    <div class="success-card">
                        <b>✅ Response generated successfully</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                memory_record = result.get("memory_record", {})

                if memory_record.get("conversation_id"):
                    st.session_state.last_conversation_id = memory_record.get("conversation_id")

                final_response = result.get("final_response")

                if final_response:
                    st.markdown("### ✅ Final Response")
                    st.info(final_response)

                llm_response = result.get("llm_response")

                if llm_response:
                    st.markdown("### 🤖 LLM Response Agent")
                    st.success(llm_response.get("response", "No LLM response found."))
                    render_json_card("LLM Details", llm_response)

                render_json_card("Authenticated User", result.get("authenticated_user", {}))
                render_json_card("Supervisor Decision", result.get("supervisor", {}))
                render_json_card("Classification Agent", result.get("classification", {}))
                render_json_card("Retrieval Agent", result.get("retrieval_result", {}))
                render_json_card("Ticketing Agent", result.get("ticket", {}))
                render_json_card("Escalation Agent", result.get("escalation", {}))
                render_json_card("Workflow Trace", result.get("workflow_trace", []))
                render_json_card("Memory Record", memory_record)

            else:
                st.error(result.get("detail", "Request failed."))


with tab_dashboard:
    st.markdown("### 📊 Dashboard Overview")

    status, data = api_get("/dashboard/stats")

    if status == 200:
        dashboard = data.get("dashboard", data)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Conversations", dashboard.get("total_conversations", 0))
        with col2:
            st.metric("Total Tickets", dashboard.get("total_tickets", 0))
        with col3:
            st.metric("Total Escalations", dashboard.get("total_escalations", 0))
        with col4:
            st.metric("Total Feedback", dashboard.get("total_feedback", 0))

        render_json_card("Full Dashboard Data", dashboard)

    else:
        st.error(data.get("detail", "Could not load dashboard."))

    st.markdown("### 🐘 PostgreSQL Status")

    status, pg_data = api_get("/postgres/status")

    if status == 200:
        st.json(pg_data)
    else:
        st.error(pg_data.get("detail", "Could not load PostgreSQL status."))


with tab_tickets:
    st.markdown("### 🎫 Tickets and Escalations")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Tickets")
        status, tickets_data = api_get("/dashboard/tickets")

        if status == 200:
            tickets = tickets_data.get("tickets", [])

            if tickets:
                for ticket in tickets:
                    render_json_card(
                        f"Ticket - {ticket.get('ticket_id', 'Unknown')}",
                        ticket
                    )
            else:
                st.info("No tickets found.")
        else:
            st.error(tickets_data.get("detail", "Could not load tickets."))

    with col2:
        st.markdown("#### Escalations")
        status, escalations_data = api_get("/dashboard/escalations")

        if status == 200:
            escalations = escalations_data.get("escalations", [])

            if escalations:
                for escalation in escalations:
                    render_json_card(
                        f"Escalation - {escalation.get('escalation_id', 'Unknown')}",
                        escalation
                    )
            else:
                st.info("No escalations found.")
        else:
            st.error(escalations_data.get("detail", "Could not load escalations."))


with tab_history:
    st.markdown("### 🕘 Conversation History")

    status, history_data = api_get("/history")

    if status == 200:
        conversations = history_data.get("conversations", [])

        if conversations:
            for conversation in conversations:
                conversation_id = conversation.get("conversation_id", "Unknown")
                render_json_card(f"Conversation - {conversation_id}", conversation)
        else:
            st.info("No conversation history found.")
    else:
        st.error(history_data.get("detail", "Could not load history."))

    st.markdown("### 🐘 PostgreSQL Conversations")

    status, pg_conv_data = api_get("/postgres/conversations")

    if status == 200:
        pg_conversations = pg_conv_data.get("conversations", [])

        if pg_conversations:
            for conversation in pg_conversations:
                conversation_id = conversation.get("conversation_id", "Unknown")
                render_json_card(f"PostgreSQL - {conversation_id}", conversation)
        else:
            st.info("No PostgreSQL conversations found.")
    else:
        st.error(pg_conv_data.get("detail", "Could not load PostgreSQL conversations."))


with tab_reports:
    st.markdown("### 📄 Reports")

    default_conversation_id = st.session_state.last_conversation_id or ""

    conversation_id = st.text_input(
        "Conversation ID",
        value=default_conversation_id,
        placeholder="Leave empty to generate latest/general report"
    )

    if st.button("Generate Report", use_container_width=True):
        payload = {
            "conversation_id": conversation_id if conversation_id.strip() else None
        }

        status, report_data = api_post("/reports/generate", payload)

        if status == 200:
            st.success("Report generated successfully.")
            st.json(report_data)
        else:
            st.error(report_data.get("detail", "Report generation failed."))

    st.divider()

    status, reports_data = api_get("/reports")

    if status == 200:
        reports = reports_data.get("reports", [])

        if reports:
            for report in reports:
                render_json_card(
                    f"Report - {report.get('report_id', 'Unknown')}",
                    report
                )
        else:
            st.info("No reports found.")
    else:
        st.error(reports_data.get("detail", "Could not load reports."))


with tab_feedback:
    st.markdown("### ⭐ Submit Feedback")

    feedback_conversation_id = st.text_input(
        "Conversation ID",
        value=st.session_state.last_conversation_id or ""
    )

    helpful = st.radio(
        "Was this response helpful?",
        [True, False],
        format_func=lambda x: "Yes" if x else "No",
        horizontal=True
    )

    rating = st.slider("Rating", 1, 5, 5)

    comment = st.text_area("Comment", placeholder="Write your feedback here...")
    improvement = st.text_area("Improvement Suggestion", placeholder="How can HelpSync AI improve?")

    if st.button("Submit Feedback", use_container_width=True):
        payload = {
            "conversation_id": feedback_conversation_id if feedback_conversation_id.strip() else None,
            "helpful": helpful,
            "rating": rating,
            "comment": comment,
            "improvement_suggestion": improvement
        }

        status, feedback_data = api_post("/feedback", payload)

        if status == 200:
            st.success("Feedback submitted successfully.")
            st.json(feedback_data)
        else:
            st.error(feedback_data.get("detail", "Feedback failed."))

    st.divider()

    st.markdown("### Feedback Records")

    status, all_feedback = api_get("/feedback")

    if status == 200:
        st.json(all_feedback)
    else:
        st.error(all_feedback.get("detail", "Could not load feedback."))