import streamlit as st

from modules.chatbot import chatbot_ui
from modules.csv_analyzer import csv_analyzer_ui
from modules.pdf_chat import pdf_chat_ui
from modules.sql_generator import sql_generator_ui
from modules.resume_assistant import resume_assistant_ui
from modules.admin_dashboard import admin_dashboard_ui
from modules.recent_chats import recent_chats_ui

from modules.login_system import login_page
from modules.admin_check import is_admin


st.set_page_config(
    page_title="AvexAI",
    page_icon="🤖",
    layout="wide"
)

# ---------------- LOGIN CHECK ----------------

if "user" not in st.session_state and "guest" not in st.session_state:

    login_page()

    st.stop()

# ---------------- USER INFO ----------------

user_email = None

if "user" in st.session_state:
    user_email = st.session_state.user.email

admin_access = False

if user_email:
    admin_access = is_admin(user_email)

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("🧠 AvexAI")

    st.caption(
        "Your All-in-One AI Assistant"
    )

    menu = [
        "💬 AI Chatbot",
        "📄 PDF Assistant",
        "📊 CSV Analyzer",
        "🧠 SQL Generator",
        "📝 Resume Assistant",
        "🕓 Recent Chats"
    ]

    if admin_access:
        menu.append(
            "📈 Admin Dashboard"
        )

    selected = st.radio(
        "Navigation",
        menu
    )

# ---------------- MAIN ----------------

if selected == "💬 AI Chatbot":
    chatbot_ui()

elif selected == "📄 PDF Assistant":
    pdf_chat_ui()

elif selected == "📊 CSV Analyzer":
    csv_analyzer_ui()

elif selected == "🧠 SQL Generator":
    sql_generator_ui()

elif selected == "📝 Resume Assistant":
    resume_assistant_ui()

elif selected == "🕓 Recent Chats":
    recent_chats_ui()

elif selected == "📈 Admin Dashboard":

    if admin_access:
        admin_dashboard_ui()

    else:
        st.error(
            "Unauthorized Access"
        )