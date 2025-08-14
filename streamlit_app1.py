# streamlit_app1.py
import streamlit as st
from src.agent_wrapper import get_agent

# ================== Page Config ==================
st.set_page_config(page_title="FactChecker Bot", layout="wide")

# ================== Title ==================
st.title("🕵️ FactChecker Bot")

# ================== Session State ==================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ================== Initialize Agent ==================
agent = get_agent()

# ================== Chat Display (history first) ==================
for message in st.session_state.chat_history:
    st.markdown(f"**You:** {message['user']}")
    st.markdown(f"**Bot:** {message['bot']}")
    st.markdown("---")

# ================== User Input ==================
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Enter your claim:", "")
    submitted = st.form_submit_button("Send")

    if submitted and user_input.strip():
        with st.spinner("Fact-checking..."):
            # Get bot response
            bot_response = agent.check_claim(user_input)

        # Save to history
        st.session_state.chat_history.append({"user": user_input, "bot": bot_response})
        st.rerun()
