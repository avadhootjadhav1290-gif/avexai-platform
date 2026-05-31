import streamlit as st
import pandas as pd


def csv_analyzer_ui():

    st.subheader("📊 CSV Data Analyzer")

    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"]
    )

    if uploaded_file:

        df = pd.read_csv(uploaded_file)

        st.write("### Dataset Preview")
        st.dataframe(df.head())

        st.write("### Shape")
        st.write(df.shape)

        st.write("### Columns")
        st.write(df.columns.tolist())

        st.write("### Statistics")
        st.dataframe(df.describe())