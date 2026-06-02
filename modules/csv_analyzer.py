import streamlit as st
import pandas as pd
from groq import Groq

def csv_analyzer_ui():
    st.subheader("📊 CSV Analyzer")
    st.caption("Upload CSV files and analyze data with AI insights.")

    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())

        question = st.text_input("Ask about this dataset...")
        if question:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a data analyst."},
                    {"role": "user", "content": f"Dataset:\n{df.head(20).to_string()}\n\nQuestion: {question}"}
                ]
            )
            st.write(response.choices[0].message.content)
