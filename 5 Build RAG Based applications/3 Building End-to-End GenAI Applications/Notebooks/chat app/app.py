import os
import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from dotenv import load_dotenv
load_dotenv()
# -----------------------------
# 1) Set OpenAI key (required)
# -----------------------------
# Set this from your shell or OS environment first:
# export OPENAI_API_KEY="sk-..."
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY not found. Set env variable and restart.")
    st.stop()

# -----------------------------
# 2) Initialize Streamlit page
# -----------------------------
st.set_page_config(page_title="LangChain Chatbot", page_icon="💬", layout="wide")
st.title("💬 Conversational App (LangChain + Streamlit)")
st.write("Type something and the bot will answer using an LLM.")

# -----------------------------
# 3) Conversation memory across turns
# -----------------------------
# Keep chat turns in session state, then create messages for LLM.
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list of (role, text)

# -----------------------------
# 4) LLM initialization
# -----------------------------
# Choose gpt-4o-mini (ChatGPT-4.0 mini).
if "chat_model" not in st.session_state:
    st.session_state.chat_model = init_chat_model(
        model="gpt-4o-mini",
        model_provider="openai",
        temperature=0.6,
        openai_api_key=OPENAI_API_KEY,
    )

# -----------------------------
# 6) User input
# -----------------------------
user_input = st.text_input("You:", key="user_input", placeholder="Say hello...", label_visibility="collapsed")

# -----------------------------
# 7) On submit, produce a response
# -----------------------------
if st.button("Send") and user_input:
    st.session_state.chat_history.append(("user", user_input))

    messages = [SystemMessage(content="You are a helpful assistant.")]
    for role, text in st.session_state.chat_history:
        if role == "user":
            messages.append(HumanMessage(content=text))
        else:
            messages.append(AIMessage(content=text))

    full_response = st.session_state.chat_model.generate([messages])
    bot_text = full_response.generations[0][0].text.strip()

    st.session_state.chat_history.append(("assistant", bot_text))

# -----------------------------
# 8) Render chat history
# -----------------------------
if "chat_history" in st.session_state:
    st.markdown("### Chat history")
    for i, (human, bot) in enumerate(st.session_state.chat_history):
        st.markdown(f"**You {i + 1}:** {human}")
        st.markdown(f"**Bot {i + 1}:** {bot}")
        st.write("---")

# -----------------------------
# 9) Optional reset
# -----------------------------
if st.button("Reset Conversation"):
    st.session_state.chat_history = []
    st.experimental_rerun()
