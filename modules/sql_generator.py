import streamlit as st
from groq import Groq

def sql_generator_ui():
    st.subheader("🧠 SQL Generator")
    st.caption("Generate SQL queries from natural language.")

    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    requirement = st.text_area("Describe your SQL requirement:")

    if st.button("Generate SQL"):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an SQL assistant."},
                {"role": "user", "content": requirement}
            ]
        )
        query = response.choices[0].message.content
        st.code(query, language="sql")
