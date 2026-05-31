import streamlit as st


def sql_generator_ui():

    st.subheader("🧠 SQL Generator")

    question = st.text_area(
        "Describe SQL Requirement"
    )

    if st.button("Generate SQL"):

        query = f"""
SELECT *
FROM table_name
WHERE condition;

Requirement:
{question}
"""

        st.code(query, language="sql")