import streamlit as st
from db import supabase


def profile_ui():

    st.title("👤 Profile")

    if "user" not in st.session_state:
        st.warning("Please login")
        return

    email = st.session_state.user.email

    user_data = (
        supabase.table("users")
        .select("*")
        .eq("email", email)
        .execute()
    )

    if not user_data.data:

        st.error(
            f"No profile found for: {email}"
        )

        return

    user = user_data.data[0]

    conversations = (
        supabase.table("conversations")
        .select("*")
        .eq("user_email", email)
        .execute()
    )

    total_conversations = len(
        conversations.data
    )

    total_messages = 0

    for convo in conversations.data:

        msgs = (
            supabase.table("messages")
            .select("*")
            .eq(
                "conversation_id",
                convo["id"]
            )
            .execute()
        )

        total_messages += len(
            msgs.data
        )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "💬 Conversations",
            total_conversations
        )

    with col2:

        st.metric(
            "📝 Messages",
            total_messages
        )

    st.divider()

    st.write(
        f"**Email:** {user['email']}"
    )

    st.write(
        f"**Role:** {user['role']}"
    )

    st.write(
        f"**Joined:** {user['created_at']}"
    )