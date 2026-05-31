import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def chatbot_ui():

    st.subheader("💬 AI Chat Assistant")

    groq_api_key = st.secrets["GROQ_API_KEY"]

    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name="llama-3.1-8b-instant"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are Avex AI, a smart and professional AI assistant."
            ),
            (
                "user",
                "Question: {question}"
            )
        ]
    )

    chain = prompt | llm | StrOutputParser()

    user_input = st.chat_input("Ask anything...")

    if user_input:

        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                response = chain.invoke(
                    {
                        "question": user_input
                    }
                )

                st.write(response)