import streamlit as st
from groq import Groq
from db import supabase


def chatbot_ui():

    st.subheader("💬 Avex AI Chatbot")

    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input(
        "Ask anything..."
    )

    if user_input:

        with st.chat_message("user"):
            st.write(user_input)

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "user",
                            "content": user_input
                        }
                    ]
                )

                answer = response.choices[0].message.content

                st.write(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        # Save only logged-in users
        if "user" in st.session_state:

            try:

                supabase.table("chats").insert(
                    {
                        "user_email": st.session_state.user.email,
                        "user_message": user_input,
                        "ai_response": answer
                    }
                ).execute()

            except Exception as e:

                st.error(f"Database Error: {e}")