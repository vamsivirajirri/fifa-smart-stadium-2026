import os
import streamlit as st

# -------------------------------------------------------------------
# 1. Page Configuration & Setup
# -------------------------------------------------------------------
st.set_page_config(
    page_title="FIFA-Sphere: Smart Stadiums & Tournament Operations",
    page_icon="🏟️",
    layout="wide",
)

# Custom CSS for polished layout spacing
st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    div[data-testid="stMetricValue"] { font-size: 2.2rem !important; }
    </style>
""",
    unsafe_allow_html=True,
)


# -------------------------------------------------------------------
# 2. GenAI Model Initialization & Handling
# -------------------------------------------------------------------
def get_ai_client():
    """Safely initializes the Google Generative AI module."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        # Target standard base model
        return genai.GenerativeModel("gemini-1.5-flash")
    except Exception:
        return None


model = get_ai_client()

# -------------------------------------------------------------------
# 3. Sidebar - Real-Time Venue Controls
# -------------------------------------------------------------------
with st.sidebar:
    st.header("📊 Real-Time Venue Controls")
    st.write("---")

    selected_venue = st.selectbox(
        "Select Target Venue",
        [
            "Estadio Azteca (Mexico City)",
            "MetLife Stadium (New York/New Jersey)",
            "SoFi Stadium (Los Angeles)",
            "BC Place (Vancouver)",
        ],
    )

    st.write("")

    # Simulated Live Metrics based on Venue Selection
    if "Azteca" in selected_venue:
        crowd_density = "87%"
        wait_time = "9.4 Mins"
        saturation = "Moderate"
        wait_delta = "-2.1 Mins (Optimized)"
    elif "MetLife" in selected_venue:
        crowd_density = "92%"
        wait_time = "14.2 Mins"
        saturation = "High"
        wait_delta = "+1.5 Mins (Congested)"
    else:
        crowd_density = "79%"
        wait_time = "6.8 Mins"
        saturation = "Low"
        wait_delta = "-3.4 Mins (Optimal)"

    st.metric(
        label="Overall Stadium Crowd Density",
        value=crowd_density,
        delta="High Volume Flow",
    )
    st.metric(
        label="Avg. Gate Entry Waiting Time", value=wait_time, delta=wait_delta
    )
    st.metric(
        label="Concession Zone Saturation",
        value=saturation,
        delta="Zone B Bottleneck" if "High" in saturation else "Stable Corridors",
    )

# -------------------------------------------------------------------
# 4. Main Dashboard UI
# -------------------------------------------------------------------
st.title("🏟️ FIFA-Sphere: Smart Stadiums & Tournament Operations")
st.caption(
    "AI-Native Operational Framework • Formulated for FIFA World Cup 2026"
)
st.write("---")

col1, col2 = st.columns([1.1, 1.0], gap="large")

# Left Main Column: Logistics & Incident Command
with col1:
    st.subheader("🛠️ Logistics & Incident Command")

    st.info(
        "🏆 **Next Match Fixture:** Quarter-Finals Match 92 | 18:00 Local Time"
    )

    with st.expander("🚨 Dynamic Infrastructure Alerts", expanded=True):
        st.warning(
            "⚠️ **Zone 4 Gate Congestion:** Directing Turnstile 12 to overflow corridors."
        )
        st.success(
            "✅ **Transit Synchronization:** Regional shuttle bus frequency increased by 20%."
        )
        st.error(
            "🛑 **Section 204 Scanner Fault:** Hardware offline. Manual fallback verification active."
        )

# Right Main Column: GenAI Incident Assistant Workspace
with col2:
    st.subheader("🤖 GenAI Fan & Crew Incident Assistant")

    if model:
        st.success(
            "⚡ GenAI Engine Synchronized Safely via Environment Variable."
        )
    else:
        st.warning(
            "💡 Running in Offline Sandbox Mode. Attach a GEMINI_API_KEY inside environment variables for live LLM inference."
        )

    st.write(
        "**System Active.** Ask me about venue navigation, emergency protocols, or crowd dispatch routing."
    )

    # Initialize persistent state for chat logs
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display past chat interactions
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle incoming user query
    user_input = st.chat_input("Enter operational query or dispatch request...")

    if user_input:
        # Append and display user request immediately
        st.session_state.chat_history.append(
            {"role": "user", "content": user_input}
        )
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate response using live AI model with resilient fallback handling
        with st.chat_message("assistant"):
            response_placeholder = st.empty()

            if model:
                try:
                    response = model.generate_content(user_input)
                    ai_response = response.text
                except Exception:
                    # Graceful programmatic API/SDK exception containment
                    ai_response = (
                        "🤖 **[Operations Control Center Simulation Mode]**\n\n"
                        "Your request has been routed through the core FIFA-Sphere fallback engine:\n"
                        f"* **Context Analyzed:** '{user_input}' processed for venue location *{selected_venue}*.\n"
                        "* **Navigation Protocol:** Access corridors for your target sector are working at steady volume capacities. Follow designated color-coded directional signage.\n"
                        "* **Crowd Mitigation:** Operational controls have adjusted entry point gates dynamically to absorb current peak flow rates.\n"
                        "* **Emergency Status:** Primary and tactical egress paths remain clear. Incident logistics dispatch teams are on active monitoring standby."
                    )
            else:
                # Sandbox response pattern when no API key is set
                ai_response = (
                    "🤖 **[Sandbox Response]**\n\n"
                    "Request logged into the Operations Control Center. Emergency routes remain clear, "
                    "automated guidance is active, and personnel lines have been notified for deployment."
                )

            response_placeholder.markdown(ai_response)

        # Append final system response to state tracking
        st.session_state.chat_history.append(
            {"role": "assistant", "content": ai_response}
        )
