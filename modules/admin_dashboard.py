import streamlit as st
from db import supabase


def admin_dashboard_ui():

    st.title("📈 Admin Dashboard")

    st.caption("Owner Access Only")

    try:

        users = supabase.table("users").select("*").execute()

        chats = supabase.table("chats").select("*").execute()

        total_users = len(users.data)

        total_chats = len(chats.data)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "👥 Total Users",
                total_users
            )

        with col2:
            st.metric(
                "💬 Total Chats",
                total_chats
            )

        with col3:
            st.metric(
                "🤖 AI Requests",
                total_chats
            )

        st.divider()

        st.subheader("👥 Registered Users")

        if total_users > 0:

            st.dataframe(
                users.data,
                use_container_width=True
            )

        else:

            st.info(
                "No users found."
            )

        st.divider()

        st.subheader("💬 Recent Chats")

        if total_chats > 0:

            st.dataframe(
                chats.data,
                use_container_width=True
            )

        else:

            st.info(
                "No chats found."
            )

    except Exception as e:

        st.error(
            f"Database Error: {e}"
        )