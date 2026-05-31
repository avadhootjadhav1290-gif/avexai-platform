import streamlit as st


def admin_dashboard_ui():

    st.subheader("📈 Admin Dashboard")

    st.metric("Total Users", 120)
    st.metric("Total Chats", 5420)
    st.metric("Premium Users", 15)

    st.write("### Recent Activity")

    st.write("- User1 used CSV Analyzer")
    st.write("- User2 uploaded PDF")
    st.write("- User3 generated SQL")