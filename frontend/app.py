import requests
import streamlit as st
from html import escape


BACKEND_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="HelpSync AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


for key, default_value in {
    "last_conversation_id": "",
    "last_final_response": "",
    "last_issue_type": "",
    "last_priority": "",
    "last_route": ""
}.items():
    if key not in st.session_state:
        st.session_state[key] = default_value


st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        color: #e5e7eb;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(59, 130, 246, 0.10), transparent 30%),
            radial-gradient(circle at top right, rgba(124, 58, 237, 0.10), transparent 30%),
            linear-gradient(180deg, #020617 0%, #0f172a 100%);
        color: #e5e7eb !important;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1.2rem;
        padding-bottom: 2.2rem;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020617 0%, #0f172a 100%) !important;
        border-right: 1px solid #1e293b !important;
    }

    section[data-testid="stSidebar"] * {
        color: #e5e7eb !important;
    }

    section[data-testid="stSidebar"] code {
        color: #f8fafc !important;
        background: #111827 !important;
    }

    .sidebar-logo {
        font-size: 30px;
        font-weight: 950;
        color: #ffffff !important;
        letter-spacing: -0.8px;
        margin-bottom: 4px;
    }

    .sidebar-caption {
        color: #94a3b8 !important;
        font-size: 13px;
        line-height: 1.6;
        margin-bottom: 18px;
    }

    .sidebar-section {
        color: #60a5fa !important;
        font-size: 12px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-top: 20px;
        margin-bottom: 12px;
    }

    .saas-hero {
        background:
            radial-gradient(circle at top left, rgba(255,255,255,0.18), transparent 28%),
            linear-gradient(135deg, #1d4ed8 0%, #4338ca 45%, #7c3aed 100%);
        color: #ffffff !important;
        padding: 34px;
        border-radius: 28px;
        margin-bottom: 24px;
        border: 1px solid rgba(255,255,255,0.16);
        box-shadow: 0 24px 70px rgba(0, 0, 0, 0.35);
    }

    .hero-kicker {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255,255,255,0.14);
        border: 1px solid rgba(255,255,255,0.18);
        padding: 7px 13px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 900;
        letter-spacing: 0.06em;
        margin-bottom: 16px;
        color: #ffffff !important;
    }

    .hero-title {
        font-size: 52px;
        line-height: 1.02;
        font-weight: 950;
        margin: 0 0 12px 0;
        letter-spacing: -1.8px;
        color: #ffffff !important;
    }

    .hero-subtitle {
        font-size: 17px;
        max-width: 920px;
        line-height: 1.7;
        color: rgba(255,255,255,0.96) !important;
    }

    .hero-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin-top: 24px;
    }

    .hero-mini-card {
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 18px;
        padding: 16px;
        backdrop-filter: blur(12px);
    }

    .hero-mini-label {
        font-size: 12px;
        font-weight: 800;
        color: rgba(255,255,255,0.82) !important;
        margin-bottom: 4px;
    }

    .hero-mini-value {
        font-size: 20px;
        font-weight: 950;
        color: #ffffff !important;
    }

    .section-title {
        font-size: 26px;
        font-weight: 950;
        color: #f8fafc !important;
        letter-spacing: -0.5px;
        margin: 8px 0 12px 0;
    }

    .status-box {
        border-radius: 18px;
        padding: 16px 18px;
        margin-bottom: 16px;
        border: 1px solid;
        font-weight: 650;
        line-height: 1.6;
    }

    .status-blue {
        background: rgba(37, 99, 235, 0.14);
        color: #bfdbfe !important;
        border-color: rgba(96, 165, 250, 0.35);
    }

    .status-green {
        background: rgba(16, 185, 129, 0.14);
        color: #a7f3d0 !important;
        border-color: rgba(52, 211, 153, 0.35);
    }

    .status-orange {
        background: rgba(249, 115, 22, 0.14);
        color: #fdba74 !important;
        border-color: rgba(251, 146, 60, 0.35);
    }

    .status-red {
        background: rgba(239, 68, 68, 0.14);
        color: #fca5a5 !important;
        border-color: rgba(248, 113, 113, 0.35);
    }

    .pill {
        display: inline-block;
        padding: 8px 13px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 900;
        margin-right: 8px;
        margin-bottom: 8px;
        letter-spacing: 0.02em;
    }

    .pill-blue {
        background: rgba(37, 99, 235, 0.18);
        color: #93c5fd !important;
        border: 1px solid rgba(96, 165, 250, 0.24);
    }

    .pill-green {
        background: rgba(16, 185, 129, 0.18);
        color: #86efac !important;
        border: 1px solid rgba(74, 222, 128, 0.24);
    }

    .pill-orange {
        background: rgba(249, 115, 22, 0.18);
        color: #fdba74 !important;
        border: 1px solid rgba(251, 146, 60, 0.24);
    }

    .pill-red {
        background: rgba(239, 68, 68, 0.18);
        color: #fca5a5 !important;
        border: 1px solid rgba(248, 113, 113, 0.24);
    }

    .pill-purple {
        background: rgba(139, 92, 246, 0.18);
        color: #c4b5fd !important;
        border: 1px solid rgba(167, 139, 250, 0.24);
    }

    .final-response {
        background: linear-gradient(135deg, rgba(37,99,235,0.16) 0%, rgba(124,58,237,0.16) 100%);
        border: 1px solid rgba(96, 165, 250, 0.28);
        border-radius: 20px;
        padding: 22px;
        color: #e0f2fe !important;
        font-size: 16px;
        line-height: 1.75;
        font-weight: 650;
        margin-bottom: 18px;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.18);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        margin-bottom: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        background: #111827 !important;
        border: 1px solid #1f2937 !important;
        border-radius: 999px;
        padding: 10px 18px;
        box-shadow: none;
    }

    .stTabs [data-baseweb="tab"] p {
        color: #cbd5e1 !important;
        font-weight: 850 !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%) !important;
        border-color: transparent !important;
    }

    .stTabs [aria-selected="true"] p {
        color: #ffffff !important;
    }

    div[data-testid="stMetric"] {
        background: #111827 !important;
        border: 1px solid #1f2937 !important;
        padding: 17px;
        border-radius: 20px;
        box-shadow: 0 12px 28px rgba(0,0,0,0.22);
    }

    div[data-testid="stMetricLabel"] p {
        color: #94a3b8 !important;
        font-weight: 850 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-weight: 950;
        font-size: 28px;
    }

    textarea,
    input,
    .stTextInput input,
    .stTextArea textarea {
        background: #0f172a !important;
        color: #f8fafc !important;
        caret-color: #f8fafc !important;
        border-radius: 14px !important;
        border: 1px solid #334155 !important;
    }

    textarea::placeholder,
    input::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
    }

    label,
    .stTextInput label,
    .stTextArea label,
    .stSlider label,
    .stRadio label,
    .stSelectbox label {
        color: #e5e7eb !important;
        font-weight: 850 !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
        color: #ffffff !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 850 !important;
        padding: 0.68rem 1rem !important;
        box-shadow: 0 12px 24px rgba(37,99,235,0.22);
    }

    .stButton > button:hover {
        filter: brightness(1.05);
    }

    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] li,
    div[data-testid="stMarkdownContainer"] span,
    .stMarkdown,
    .stText,
    p,
    li {
        color: #e5e7eb;
    }

    details {
        background: #111827 !important;
        border: 1px solid #1f2937 !important;
        border-radius: 16px !important;
    }

    details summary {
        color: #f8fafc !important;
    }

    details summary p {
        color: #f8fafc !important;
        font-weight: 850 !important;
    }

    .stAlert {
        background: #111827 !important;
        color: #e5e7eb !important;
        border-radius: 14px !important;
    }

    .stAlert p {
        color: #e5e7eb !important;
    }

    [data-testid="stExpander"] {
        background: #111827 !important;
        border: 1px solid #1f2937 !important;
        border-radius: 16px !important;
    }

    [data-testid="stJson"] {
        background: #0b1220 !important;
        border-radius: 14px !important;
    }

    [data-baseweb="radio"] label,
    [role="radiogroup"] label {
        color: #e5e7eb !important;
    }

    [data-baseweb="slider"] * {
        color: #e5e7eb !important;
    }

    @media (max-width: 900px) {
        .hero-grid {
            grid-template-columns: repeat(2, 1fr);
        }

        .hero-title {
            font-size: 36px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


def html_escape(value):
    return escape(str(value))


def render_hero():
    st.markdown(
        """
        <div class="saas-hero">
            <div class="hero-kicker">⚡ LANGGRAPH SUPERVISOR ARCHITECTURE</div>
            <div class="hero-title">HelpSync AI</div>
            <div class="hero-subtitle">
                Enterprise-grade multi-agent service desk automation for classifying issues,
                retrieving solutions, creating tickets, escalating critical incidents,
                storing memory, generating reports, and collecting feedback.
            </div>
            <div class="hero-grid">
                <div class="hero-mini-card">
                    <div class="hero-mini-label">Workflow</div>
                    <div class="hero-mini-value">Multi-Agent</div>
                </div>
                <div class="hero-mini-card">
                    <div class="hero-mini-label">Backend</div>
                    <div class="hero-mini-value">FastAPI</div>
                </div>
                <div class="hero-mini-card">
                    <div class="hero-mini-label">Frontend</div>
                    <div class="hero-mini-value">Streamlit</div>
                </div>
                <div class="hero-mini-card">
                    <div class="hero-mini-label">Memory</div>
                    <div class="hero-mini-value">JSON Store</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_message(message, status="blue"):
    css_map = {
        "blue": "status-blue",
        "green": "status-green",
        "orange": "status-orange",
        "red": "status-red"
    }
    css_class = css_map.get(status, "status-blue")

    st.markdown(
        f"""
        <div class="status-box {css_class}">
            {html_escape(message)}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_pill(text, css_class="pill-blue"):
    st.markdown(
        f'<span class="pill {css_class}">{html_escape(text)}</span>',
        unsafe_allow_html=True
    )


def priority_class(priority):
    priority = (priority or "").lower()
    if priority == "critical":
        return "pill-red"
    if priority == "high":
        return "pill-orange"
    if priority == "medium":
        return "pill-blue"
    return "pill-green"


def render_final_response(response):
    st.markdown(
        f"""
        <div class="final-response">
            {html_escape(response)}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_json_card(title, data):
    st.markdown(f"#### {title}")
    st.json(data)


def safe_request(method, endpoint, **kwargs):
    url = f"{BACKEND_URL}{endpoint}"
    if method.lower() == "get":
        response = requests.get(url, timeout=30, **kwargs)
    else:
        response = requests.post(url, timeout=30, **kwargs)
    response.raise_for_status()
    return response.json()


def call_chat_api(user_query):
    return safe_request("post", "/chat", json={"user_query": user_query})


def get_dashboard_stats():
    return safe_request("get", "/dashboard/stats")


def get_history():
    return safe_request("get", "/history")


def get_tickets():
    return safe_request("get", "/dashboard/tickets")


def get_escalations():
    return safe_request("get", "/dashboard/escalations")


def generate_report(conversation_id=None):
    return safe_request("post", "/reports/generate", json={"conversation_id": conversation_id})


def get_reports():
    return safe_request("get", "/reports")


def submit_feedback(conversation_id, helpful, rating, comment, improvement_suggestion):
    return safe_request(
        "post",
        "/feedback",
        json={
            "conversation_id": conversation_id,
            "helpful": helpful,
            "rating": rating,
            "comment": comment,
            "improvement_suggestion": improvement_suggestion
        }
    )


def get_feedback_records():
    return safe_request("get", "/feedback")


with st.sidebar:
    st.markdown('<div class="sidebar-logo">🤖 HelpSync AI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sidebar-caption">Enterprise service desk automation powered by coordinated AI agents.</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="sidebar-section">System Stack</div>', unsafe_allow_html=True)
    render_pill("FastAPI", "pill-blue")
    render_pill("LangGraph", "pill-purple")
    render_pill("Streamlit", "pill-green")
    render_pill("JSON Memory", "pill-orange")

    st.divider()

    st.markdown('<div class="sidebar-section">Agent Layer</div>', unsafe_allow_html=True)
    st.caption("Classifier Agent")
    st.caption("Retrieval Agent")
    st.caption("Ticketing Agent")
    st.caption("Escalation Agent")
    st.caption("Memory Agent")
    st.caption("Report Agent")
    st.caption("Feedback Agent")

    st.divider()

    st.markdown('<div class="sidebar-section">Sample Queries</div>', unsafe_allow_html=True)

    samples = [
        "My laptop is not connecting to WiFi",
        "I forgot my password and cannot login",
        "My laptop screen is broken",
        "Urgent server is down for everyone",
        "Payroll salary is not received"
    ]

    for sample in samples:
        st.code(sample)

    st.divider()

    st.markdown('<div class="sidebar-section">Last Conversation</div>', unsafe_allow_html=True)

    if st.session_state.last_conversation_id:
        st.success(st.session_state.last_conversation_id)
    else:
        st.info("No conversation yet")


render_hero()


tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "💬 Chat",
    "📊 Dashboard",
    "🎫 Tickets",
    "🧠 History",
    "📄 Reports",
    "⭐ Feedback"
])


with tab1:
    st.markdown('<div class="section-title">Service Desk Assistant</div>', unsafe_allow_html=True)

    render_message(
        "Submit an employee issue. The supervisor will classify, route, resolve, ticket, escalate, and store the interaction.",
        "blue"
    )

    user_query = st.text_area(
        "Issue description",
        placeholder="Example: Urgent server is down for everyone",
        height=140
    )

    col_run, col_clear = st.columns([4, 1])

    with col_run:
        run_clicked = st.button("🚀 Run Multi-Agent Workflow", type="primary", use_container_width=True)

    with col_clear:
        clear_clicked = st.button("Clear", use_container_width=True)

    if clear_clicked:
        st.session_state.last_conversation_id = ""
        st.session_state.last_final_response = ""
        st.session_state.last_issue_type = ""
        st.session_state.last_priority = ""
        st.session_state.last_route = ""
        st.rerun()

    if run_clicked:
        if not user_query.strip():
            st.warning("Please enter an issue first.")
        else:
            try:
                with st.spinner("LangGraph supervisor is coordinating agents..."):
                    result = call_chat_api(user_query)

                classification = result.get("classification", {}) or {}
                supervisor = result.get("supervisor", {}) or {}
                memory_record = result.get("memory_record", {}) or {}

                conversation_id = memory_record.get("conversation_id", "")
                final_response = result.get("final_response", "No response generated.")

                st.session_state.last_conversation_id = conversation_id
                st.session_state.last_final_response = final_response
                st.session_state.last_issue_type = classification.get("issue_type", "")
                st.session_state.last_priority = classification.get("priority", "")
                st.session_state.last_route = supervisor.get("decision", "")

                render_message("Workflow completed successfully.", "green")

                st.markdown("### Final Response")
                render_final_response(final_response)

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Issue Type", classification.get("issue_type", "N/A"))
                col2.metric("Priority", classification.get("priority", "N/A"))
                col3.metric("Routed To", supervisor.get("decision", "N/A"))
                col4.metric("Conversation ID", conversation_id or "N/A")

                render_pill(f"Issue: {classification.get('issue_type', 'N/A')}", "pill-blue")
                render_pill(
                    f"Priority: {classification.get('priority', 'N/A')}",
                    priority_class(classification.get("priority", ""))
                )
                render_pill(f"Route: {supervisor.get('decision', 'N/A')}", "pill-purple")

                st.divider()

                col_left, col_right = st.columns(2)

                with col_left:
                    render_json_card("🧭 Classification", classification)
                    retrieval = result.get("retrieval_result")
                    if retrieval:
                        st.markdown("#### 📚 Knowledge Base Result")
                        if retrieval.get("found"):
                            render_message(retrieval.get("solution", "Solution found."), "green")
                        else:
                            render_message(retrieval.get("message", "No solution found."), "orange")
                        st.json(retrieval)

                with col_right:
                    render_json_card("🧠 Supervisor Decision", supervisor)

                    ticket = result.get("ticket")
                    if ticket:
                        st.markdown("#### 🎫 Ticket")
                        render_message(
                            f"Ticket {ticket.get('ticket_id')} assigned to {ticket.get('assigned_team')}.",
                            "blue"
                        )
                        st.json(ticket)

                    escalation = result.get("escalation")
                    if escalation:
                        st.markdown("#### 🚨 Escalation")
                        render_message(
                            f"Escalated to {escalation.get('escalated_to')} with ID {escalation.get('escalation_id')}.",
                            "orange"
                        )
                        st.json(escalation)

                if memory_record:
                    st.divider()
                    render_json_card("💾 Memory Record", memory_record)

                st.divider()
                st.markdown("### Agent Workflow Trace")

                workflow_trace = result.get("workflow_trace", [])
                if not workflow_trace:
                    st.info("No workflow trace available.")
                else:
                    for step in workflow_trace:
                        with st.expander(f"Step {step.get('step')} — {step.get('agent')}"):
                            st.write("**Action:**", step.get("action"))
                            st.json(step.get("output"))

            except requests.exceptions.ConnectionError:
                render_message("Backend is not running. Start the FastAPI backend first.", "red")
            except Exception as error:
                render_message(f"Something went wrong: {error}", "red")


with tab2:
    st.markdown('<div class="section-title">Executive Dashboard</div>', unsafe_allow_html=True)

    render_message(
        "Live analytics from conversations, tickets, escalations, routes, and priorities.",
        "blue"
    )

    if st.button("🔄 Refresh Analytics", type="primary", use_container_width=True):
        try:
            dashboard_response = get_dashboard_stats()
            dashboard = dashboard_response.get("dashboard", {}) or {}

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Conversations", dashboard.get("total_conversations", 0))
            col2.metric("Tickets", dashboard.get("total_tickets", 0))
            col3.metric("Open Tickets", dashboard.get("open_tickets", 0))
            col4.metric("Escalations", dashboard.get("total_escalations", 0))

            st.divider()

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.markdown("### Issue Distribution")
                st.json(dashboard.get("issue_type_counts", {}))

            with col_b:
                st.markdown("### Priority Distribution")
                st.json(dashboard.get("priority_counts", {}))

            with col_c:
                st.markdown("### Routing Distribution")
                st.json(dashboard.get("route_counts", {}))

            st.markdown("### Recent Conversations")
            conversations = dashboard.get("recent_conversations", [])

            if not conversations:
                st.info("No recent conversations.")
            else:
                for item in conversations:
                    with st.expander(f"{item.get('conversation_id')} — {item.get('route_to')}"):
                        st.write("**Query:**", item.get("user_query"))
                        st.write("**Final Response:**", item.get("final_response"))
                        st.json(item)

        except requests.exceptions.ConnectionError:
            render_message("Backend is not running. Start the FastAPI backend first.", "red")
        except Exception as error:
            render_message(f"Something went wrong: {error}", "red")


with tab3:
    st.markdown('<div class="section-title">Ticket Operations</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        render_message("Support tickets created by the Ticketing Agent.", "blue")

        if st.button("Load Tickets", use_container_width=True):
            try:
                ticket_response = get_tickets()
                tickets = ticket_response.get("tickets", [])

                st.metric("Total Tickets", ticket_response.get("total_tickets", 0))

                if not tickets:
                    st.info("No tickets created yet.")
                else:
                    for ticket in tickets:
                        with st.expander(f"{ticket.get('ticket_id')} — {ticket.get('issue_type')}"):
                            st.write("**Priority:**", ticket.get("priority"))
                            st.write("**Status:**", ticket.get("status"))
                            st.write("**Assigned Team:**", ticket.get("assigned_team"))
                            st.write("**Created At:**", ticket.get("created_at"))
                            st.json(ticket)

            except requests.exceptions.ConnectionError:
                render_message("Backend is not running. Start the FastAPI backend first.", "red")
            except Exception as error:
                render_message(f"Something went wrong: {error}", "red")

    with col2:
        render_message("Critical issues escalated to senior teams.", "orange")

        if st.button("Load Escalations", use_container_width=True):
            try:
                escalation_response = get_escalations()
                escalations = escalation_response.get("escalations", [])

                st.metric("Total Escalations", escalation_response.get("total_escalations", 0))

                if not escalations:
                    st.info("No escalations created yet.")
                else:
                    for escalation in escalations:
                        with st.expander(f"{escalation.get('escalation_id')} — {escalation.get('issue_type')}"):
                            st.write("**Priority:**", escalation.get("priority"))
                            st.write("**Escalated To:**", escalation.get("escalated_to"))
                            st.write("**Reason:**", escalation.get("reason"))
                            st.write("**Created At:**", escalation.get("created_at"))
                            st.json(escalation)

            except requests.exceptions.ConnectionError:
                render_message("Backend is not running. Start the FastAPI backend first.", "red")
            except Exception as error:
                render_message(f"Something went wrong: {error}", "red")


with tab4:
    st.markdown('<div class="section-title">Conversation Memory</div>', unsafe_allow_html=True)

    render_message(
        "Recent service desk interactions stored by the Memory Agent.",
        "blue"
    )

    if st.button("Load Conversation Memory", type="primary", use_container_width=True):
        try:
            history_response = get_history()
            conversations = history_response.get("conversations", [])

            st.metric("Total Returned", history_response.get("total_returned", 0))

            if not conversations:
                st.info("No conversation history available.")
            else:
                for conversation in conversations:
                    conversation_id = conversation.get("conversation_id")
                    classification = conversation.get("classification", {}) or {}
                    issue = classification.get("issue_type", "Unknown")
                    priority = classification.get("priority", "Unknown")

                    with st.expander(f"{conversation_id} — {issue} — {priority}"):
                        st.write("**User Query:**", conversation.get("user_query"))
                        st.write("**Route:**", conversation.get("route_to"))
                        st.write("**Final Response:**", conversation.get("final_response"))
                        st.json(conversation)

        except requests.exceptions.ConnectionError:
            render_message("Backend is not running. Start the FastAPI backend first.", "red")
        except Exception as error:
            render_message(f"Something went wrong: {error}", "red")


with tab5:
    st.markdown('<div class="section-title">Case Reports</div>', unsafe_allow_html=True)

    render_message(
        "Generate service desk case reports with risk, security, scalability, and recommendations.",
        "blue"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Generate Report")

        report_conversation_id = st.text_input(
            "Conversation ID",
            value=st.session_state.last_conversation_id,
            placeholder="Leave empty to generate for latest conversation",
            key="report_conversation_id"
        )

        if st.button("Generate Report", type="primary", use_container_width=True):
            try:
                chosen_id = report_conversation_id.strip() if report_conversation_id.strip() else None
                report_response = generate_report(chosen_id)
                report = report_response.get("report", {})

                if report.get("generated") is False:
                    st.warning(report.get("message", "Report could not be generated."))
                else:
                    st.success("Report generated successfully.")
                    st.markdown("#### Case Summary")
                    st.json(report.get("case_summary", {}))
                    st.markdown("#### Resolution Summary")
                    st.info(report.get("resolution_summary", "No resolution summary."))
                    st.markdown("#### Architecture Flow")
                    st.json(report.get("architecture_flow", []))
                    st.markdown("#### Risk Analysis")
                    st.warning(report.get("risk_analysis", "No risk analysis."))
                    st.markdown("#### Security Considerations")
                    st.info(report.get("security_considerations", "No security notes."))
                    st.markdown("#### Scalability Considerations")
                    st.info(report.get("scalability_considerations", "No scalability notes."))
                    st.markdown("#### Final Recommendation")
                    st.success(report.get("final_recommendation", "No recommendation."))

                    with st.expander("Full Report JSON"):
                        st.json(report)

            except requests.exceptions.ConnectionError:
                render_message("Backend is not running. Start the FastAPI backend first.", "red")
            except Exception as error:
                render_message(f"Something went wrong: {error}", "red")

    with col2:
        st.markdown("### Report Repository")

        if st.button("Load Reports", use_container_width=True):
            try:
                reports_response = get_reports()
                reports = reports_response.get("reports", [])

                st.metric("Total Reports", reports_response.get("total_reports", 0))

                if not reports:
                    st.info("No reports generated yet.")
                else:
                    for report in reports:
                        with st.expander(f"{report.get('report_id')} — {report.get('conversation_id')}"):
                            st.write("**Generated At:**", report.get("generated_at"))
                            st.write("**Agent:**", report.get("agent"))
                            st.json(report)

            except requests.exceptions.ConnectionError:
                render_message("Backend is not running. Start the FastAPI backend first.", "red")
            except Exception as error:
                render_message(f"Something went wrong: {error}", "red")


with tab6:
    st.markdown('<div class="section-title">Feedback and Learning</div>', unsafe_allow_html=True)

    render_message(
        "Collect human feedback and generate learning notes for future workflow improvement.",
        "blue"
    )

    conversation_id = st.text_input(
        "Conversation ID",
        value=st.session_state.last_conversation_id,
        placeholder="Example: CONV-3008",
        key="feedback_conversation_id"
    )

    col_left, col_right = st.columns(2)

    with col_left:
        helpful_option = st.radio(
            "Was the response helpful?",
            ["Helpful", "Not Helpful"],
            horizontal=True
        )
        helpful = helpful_option == "Helpful"

    with col_right:
        rating = st.slider(
            "Rating",
            min_value=1,
            max_value=5,
            value=5
        )

    comment = st.text_area(
        "Comment",
        placeholder="Example: The ticket routing was correct."
    )

    improvement_suggestion = st.text_area(
        "Improvement Suggestion",
        placeholder="Example: Add more troubleshooting steps before ticket creation."
    )

    if st.button("Submit Feedback", type="primary", use_container_width=True):
        try:
            feedback_response = submit_feedback(
                conversation_id=conversation_id.strip() if conversation_id.strip() else None,
                helpful=helpful,
                rating=rating,
                comment=comment,
                improvement_suggestion=improvement_suggestion
            )

            st.success("Feedback submitted successfully.")
            st.json(feedback_response.get("feedback", {}))

        except requests.exceptions.ConnectionError:
            render_message("Backend is not running. Start the FastAPI backend first.", "red")
        except Exception as error:
            render_message(f"Something went wrong: {error}", "red")

    st.divider()
    st.markdown("### Feedback Analytics")

    if st.button("Load Feedback Records", use_container_width=True):
        try:
            feedback_records = get_feedback_records()
            summary = feedback_records.get("summary", {})
            records = feedback_records.get("feedback", [])

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Feedback", summary.get("total_feedback", 0))
            col2.metric("Helpful", summary.get("helpful_count", 0))
            col3.metric("Not Helpful", summary.get("not_helpful_count", 0))
            col4.metric("Average Rating", summary.get("average_rating", 0))

            if not records:
                st.info("No feedback records yet.")
            else:
                for record in records:
                    with st.expander(f"{record.get('feedback_id')} — Rating {record.get('rating')}/5"):
                        st.write("**Conversation ID:**", record.get("conversation_id"))
                        st.write("**Helpful:**", record.get("helpful"))
                        st.write("**Learning Note:**", record.get("learning_note"))
                        st.json(record)

        except requests.exceptions.ConnectionError:
            render_message("Backend is not running. Start the FastAPI backend first.", "red")
        except Exception as error:
            render_message(f"Something went wrong: {error}", "red")