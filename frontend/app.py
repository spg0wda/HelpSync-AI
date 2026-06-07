import requests
import streamlit as st


BACKEND_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="HelpSync AI",
    page_icon="🤖",
    layout="wide"
)


st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #2563eb;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        color: #475569;
        margin-bottom: 25px;
    }

    .metric-card {
        background-color: #f8fafc;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        text-align: center;
    }

    .success-box {
        background-color: #ecfdf5;
        color: #065f46;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #a7f3d0;
    }

    .info-box {
        background-color: #eff6ff;
        color: #1e3a8a;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #bfdbfe;
    }

    .warning-box {
        background-color: #fff7ed;
        color: #9a3412;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #fed7aa;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown('<p class="main-title">🤖 HelpSync AI</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Enterprise Multi-Agent Service Desk Chatbot using LangGraph Supervisor Architecture</p>',
    unsafe_allow_html=True
)


def call_chat_api(user_query: str):
    response = requests.post(
        f"{BACKEND_URL}/chat",
        json={"user_query": user_query},
        timeout=30
    )
    response.raise_for_status()
    return response.json()


def get_dashboard_stats():
    response = requests.get(f"{BACKEND_URL}/dashboard/stats", timeout=30)
    response.raise_for_status()
    return response.json()


def get_history():
    response = requests.get(f"{BACKEND_URL}/history", timeout=30)
    response.raise_for_status()
    return response.json()


def get_tickets():
    response = requests.get(f"{BACKEND_URL}/dashboard/tickets", timeout=30)
    response.raise_for_status()
    return response.json()


def get_escalations():
    response = requests.get(f"{BACKEND_URL}/dashboard/escalations", timeout=30)
    response.raise_for_status()
    return response.json()


with st.sidebar:
    st.header("📌 Project Info")
    st.write("**Project:** HelpSync AI")
    st.write("**Backend:** FastAPI")
    st.write("**Workflow:** LangGraph")
    st.write("**Frontend:** Streamlit")
    st.write("**Storage:** Local JSON")
    st.divider()

    st.header("🧪 Sample Queries")
    st.code("My laptop is not connecting to WiFi")
    st.code("I forgot my password and cannot login")
    st.code("My laptop screen is broken")
    st.code("Urgent server is down for everyone")


tab1, tab2, tab3, tab4 = st.tabs([
    "💬 Chat",
    "📊 Dashboard",
    "🎫 Tickets",
    "🧠 History"
])


with tab1:
    st.subheader("💬 Service Desk Chat")

    st.markdown(
        """
        <div class="info-box">
        Enter an employee support issue. The LangGraph supervisor will route it to the correct agent.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    user_query = st.text_area(
        "Enter your service desk issue",
        placeholder="Example: My laptop is not connecting to WiFi",
        height=120
    )

    if st.button("Analyze Issue", type="primary", use_container_width=True):
        if not user_query.strip():
            st.warning("Please enter an issue first.")
        else:
            try:
                with st.spinner("Supervisor and agents are processing your request..."):
                    result = call_chat_api(user_query)

                st.markdown(
                    """
                    <div class="success-box">
                    Workflow completed successfully.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.write("")

                st.markdown("## ✅ Final Response")
                st.info(result.get("final_response", "No response generated."))

                classification = result.get("classification", {})
                supervisor = result.get("supervisor", {})

                col1, col2, col3 = st.columns(3)

                col1.metric("Issue Type", classification.get("issue_type", "N/A"))
                col2.metric("Priority", classification.get("priority", "N/A"))
                col3.metric("Routed To", supervisor.get("decision", "N/A"))

                st.divider()

                left_col, right_col = st.columns(2)

                with left_col:
                    st.markdown("### 🧭 Classification")
                    st.json(classification)

                with right_col:
                    st.markdown("### 🧠 Supervisor Decision")
                    st.json(supervisor)

                if result.get("retrieval_result"):
                    st.markdown("### 📚 Retrieval Result")
                    st.json(result.get("retrieval_result"))

                if result.get("ticket"):
                    st.markdown("### 🎫 Ticket Details")
                    st.json(result.get("ticket"))

                if result.get("escalation"):
                    st.markdown("### 🚨 Escalation Details")
                    st.json(result.get("escalation"))

                if result.get("memory_record"):
                    st.markdown("### 💾 Memory Record")
                    st.json(result.get("memory_record"))

                st.markdown("### 🔁 Workflow Trace")

                workflow_trace = result.get("workflow_trace", [])

                for step in workflow_trace:
                    with st.expander(f"Step {step.get('step')} - {step.get('agent')}"):
                        st.write("**Action:**", step.get("action"))
                        st.json(step.get("output"))

            except requests.exceptions.ConnectionError:
                st.error("Backend is not running. Start the FastAPI backend first.")
            except Exception as error:
                st.error(f"Something went wrong: {error}")


with tab2:
    st.subheader("📊 Dashboard Analytics")

    st.markdown(
        """
        <div class="info-box">
        View service desk analytics generated from conversation memory, tickets, and escalation records.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if st.button("Refresh Dashboard", type="primary", use_container_width=True):
        try:
            dashboard_response = get_dashboard_stats()
            dashboard = dashboard_response.get("dashboard", {})

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Total Conversations", dashboard.get("total_conversations", 0))
            col2.metric("Total Tickets", dashboard.get("total_tickets", 0))
            col3.metric("Open Tickets", dashboard.get("open_tickets", 0))
            col4.metric("Escalations", dashboard.get("total_escalations", 0))

            st.divider()

            col_a, col_b, col_c = st.columns(3)

            with col_a:
                st.markdown("### Issue Types")
                st.json(dashboard.get("issue_type_counts", {}))

            with col_b:
                st.markdown("### Priorities")
                st.json(dashboard.get("priority_counts", {}))

            with col_c:
                st.markdown("### Routing")
                st.json(dashboard.get("route_counts", {}))

            st.markdown("### Recent Conversations")
            st.json(dashboard.get("recent_conversations", []))

        except requests.exceptions.ConnectionError:
            st.error("Backend is not running. Start the FastAPI backend first.")
        except Exception as error:
            st.error(f"Something went wrong: {error}")


with tab3:
    st.subheader("🎫 Tickets and Escalations")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Support Tickets")
        if st.button("Load Tickets", use_container_width=True):
            try:
                ticket_response = get_tickets()
                st.metric("Total Tickets", ticket_response.get("total_tickets", 0))
                st.json(ticket_response.get("tickets", []))
            except requests.exceptions.ConnectionError:
                st.error("Backend is not running. Start the FastAPI backend first.")
            except Exception as error:
                st.error(f"Something went wrong: {error}")

    with col2:
        st.markdown("### Escalation Records")
        if st.button("Load Escalations", use_container_width=True):
            try:
                escalation_response = get_escalations()
                st.metric("Total Escalations", escalation_response.get("total_escalations", 0))
                st.json(escalation_response.get("escalations", []))
            except requests.exceptions.ConnectionError:
                st.error("Backend is not running. Start the FastAPI backend first.")
            except Exception as error:
                st.error(f"Something went wrong: {error}")


with tab4:
    st.subheader("🧠 Conversation History")

    st.markdown(
        """
        <div class="info-box">
        This section displays recent conversations stored by the Memory Agent.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if st.button("Load Recent History", type="primary", use_container_width=True):
        try:
            history_response = get_history()
            st.metric("Total Returned", history_response.get("total_returned", 0))
            st.json(history_response.get("conversations", []))
        except requests.exceptions.ConnectionError:
            st.error("Backend is not running. Start the FastAPI backend first.")
        except Exception as error:
            st.error(f"Something went wrong: {error}")