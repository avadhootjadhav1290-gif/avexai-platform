import streamlit as st
from modules.chatbot import chatbot_ui
from modules.csv_analyzer import csv_analyzer_ui
from modules.pdf_chat import pdf_chat_ui
from modules.sql_generator import sql_generator_ui
from modules.resume_assistant import resume_assistant_ui
from modules.admin_dashboard import admin_dashboard_ui

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Avex AI Workspace",
    page_icon="🤖",
    layout="wide"
)

# ---------------- LOGIN ----------------

password = st.sidebar.text_input(
    "Enter Access Password",
    type="password"
)

if password != "Avex123":
    st.warning("Incorrect Password")
    st.stop()

# ---------------- SIDEBAR ----------------

st.sidebar.title("🚀 Avex AI Workspace")
st.sidebar.caption("Professional AI Platform")

feature = st.sidebar.radio(
    "Choose Tool",
    [
        "💬 AI Chat",
        "📊 CSV Analyzer",
        "📄 PDF Assistant",
        "🧠 SQL Generator",
        "📝 Resume Assistant",
        "📈 Admin Dashboard"
    ]
)

st.sidebar.markdown("---")
st.sidebar.success("System Online")

# ---------------- MAIN TITLE ----------------

st.title("🤖 Avex AI Workspace")
st.caption("Professional AI Platform")

# ---------------- ROUTING ----------------

if feature == "💬 AI Chat":
    chatbot_ui()

elif feature == "📊 CSV Analyzer":
    csv_analyzer_ui()

elif feature == "📄 PDF Assistant":
    pdf_chat_ui()

elif feature == "🧠 SQL Generator":
    sql_generator_ui()

elif feature == "📝 Resume Assistant":
    resume_assistant_ui()

elif feature == "📈 Admin Dashboard":
    admin_dashboard_ui()