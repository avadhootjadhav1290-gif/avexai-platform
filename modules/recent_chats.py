import streamlit as st
from db import supabase


def recent_chats_ui():

    st.subheader("🕓 Recent Chats")

    if "user" not in st.session_state:

        st.warning(
            "Login required to view chat history."
        )

        return

    user_email = st.session_state.user.email

    chats = (
        supabase.table("chats")
        .select("*")
        .eq("user_email", user_email)
        .order("created_at", desc=True)
        .limit(20)
        .execute()
    )

    if len(chats.data) == 0:

        st.info("No chats found.")

        return

    for chat in chats.data:

        st.markdown(
            f"### 🙋 You\n{chat['user_message']}"
        )

        st.markdown(
            f"### 🤖 AI\n{chat['ai_response']}"
        )

        st.caption(
            chat["created_at"]
        )

        st.divider()