import requests
import streamlit as st


BACKEND_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="HelpSync AI",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 HelpSync AI")
st.caption("Enterprise Multi-Agent Service Desk Chatbot using LangGraph Supervisor Architecture")


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


tab1, tab2, tab3, tab4 = st.tabs([
    "💬 Chat",
    "📊 Dashboard",
    "🎫 Tickets",
    "🧠 History"
])


with tab1:
    st.subheader("Service Desk Chat")

    user_query = st.text_area(
        "Enter your service desk issue",
        placeholder="Example: My laptop is not connecting to WiFi"
    )

    if st.button("Analyze Issue", type="primary"):
        if not user_query.strip():
            st.warning("Please enter an issue first.")
        else:
            try:
                with st.spinner("Agents are working..."):
                    result = call_chat_api(user_query)

                st.success("Workflow completed successfully.")

                st.markdown("### Final Response")
                st.info(result.get("final_response", "No response generated."))

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### Classification")
                    st.json(result.get("classification"))

                with col2:
                    st.markdown("### Supervisor Decision")
                    st.json(result.get("supervisor"))

                if result.get("retrieval_result"):
                    st.markdown("### Retrieval Result")
                    st.json(result.get("retrieval_result"))

                if result.get("ticket"):
                    st.markdown("### Ticket Details")
                    st.json(result.get("ticket"))

                if result.get("escalation"):
                    st.markdown("### Escalation Details")
                    st.json(result.get("escalation"))

                if result.get("memory_record"):
                    st.markdown("### Memory Record")
                    st.json(result.get("memory_record"))

                st.markdown("### Workflow Trace")
                workflow_trace = result.get("workflow_trace", [])

                for step in workflow_trace:
                    with st.expander(f"Step {step.get('step')} - {step.get('agent')}"):
                        st.write("Action:", step.get("action"))
                        st.json(step.get("output"))

            except requests.exceptions.ConnectionError:
                st.error("Backend is not running. Start FastAPI backend first.")
            except Exception as error:
                st.error(f"Something went wrong: {error}")


with tab2:
    st.subheader("Dashboard Analytics")

    if st.button("Refresh Dashboard"):
        try:
            dashboard_response = get_dashboard_stats()
            dashboard = dashboard_response.get("dashboard", {})

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Total Conversations", dashboard.get("total_conversations", 0))
            col2.metric("Total Tickets", dashboard.get("total_tickets", 0))
            col3.metric("Open Tickets", dashboard.get("open_tickets", 0))
            col4.metric("Total Escalations", dashboard.get("total_escalations", 0))

            st.markdown("### Issue Type Counts")
            st.json(dashboard.get("issue_type_counts", {}))

            st.markdown("### Priority Counts")
            st.json(dashboard.get("priority_counts", {}))

            st.markdown("### Route Counts")
            st.json(dashboard.get("route_counts", {}))

            st.markdown("### Recent Conversations")
            st.json(dashboard.get("recent_conversations", []))

        except requests.exceptions.ConnectionError:
            st.error("Backend is not running. Start FastAPI backend first.")
        except Exception as error:
            st.error(f"Something went wrong: {error}")


with tab3:
    st.subheader("Tickets and Escalations")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Load Tickets"):
            try:
                ticket_response = get_tickets()
                st.write(f"Total Tickets: {ticket_response.get('total_tickets', 0)}")
                st.json(ticket_response.get("tickets", []))
            except requests.exceptions.ConnectionError:
                st.error("Backend is not running. Start FastAPI backend first.")
            except Exception as error:
                st.error(f"Something went wrong: {error}")

    with col2:
        if st.button("Load Escalations"):
            try:
                escalation_response = get_escalations()
                st.write(f"Total Escalations: {escalation_response.get('total_escalations', 0)}")
                st.json(escalation_response.get("escalations", []))
            except requests.exceptions.ConnectionError:
                st.error("Backend is not running. Start FastAPI backend first.")
            except Exception as error:
                st.error(f"Something went wrong: {error}")


with tab4:
    st.subheader("Conversation History")

    if st.button("Load Recent History"):
        try:
            history_response = get_history()
            st.write(f"Total Returned: {history_response.get('total_returned', 0)}")
            st.json(history_response.get("conversations", []))
        except requests.exceptions.ConnectionError:
            st.error("Backend is not running. Start FastAPI backend first.")
        except Exception as error:
            st.error(f"Something went wrong: {error}")