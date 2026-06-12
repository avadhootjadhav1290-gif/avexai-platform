import streamlit as st
from db import supabase


def admin_dashboard_ui():

    st.title("📈 Admin Dashboard")

    st.caption("Owner Access Only")

    try:

        users = supabase.table(
            "users"
        ).select("*").execute()

        conversations = supabase.table(
            "conversations"
        ).select("*").execute()

        messages = supabase.table(
            "messages"
        ).select("*").execute()

        total_users = len(users.data)
        total_conversations = len(conversations.data)
        total_messages = len(messages.data)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "👥 Users",
                total_users
            )

        with col2:
            st.metric(
                "💬 Conversations",
                total_conversations
            )

        with col3:
            st.metric(
                "📝 Messages",
                total_messages
            )

        st.divider()

        # Most Active User

        user_counts = {}

        for convo in conversations.data:

            email = convo["user_email"]

            user_counts[email] = (
                user_counts.get(email, 0) + 1
            )

        most_active = "No Data"

        if user_counts:

            most_active = max(
                user_counts,
                key=user_counts.get
            )

        st.metric(
            "🔥 Most Active User",
            most_active
        )

        st.divider()

        st.subheader(
            "👥 Registered Users"
        )

        st.dataframe(
            users.data,
            use_container_width=True
        )

        st.divider()

        st.subheader(
            "💬 Conversations"
        )

        st.dataframe(
            conversations.data,
            use_container_width=True
        )

        st.divider()

        st.subheader(
            "📝 Messages"
        )

        st.dataframe(
            messages.data,
            use_container_width=True
        )

    except Exception as e:

        st.error(
            f"Database Error: {e}"
        )