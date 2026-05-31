import streamlit as st
from pypdf import PdfReader


def pdf_chat_ui():

    st.subheader("📄 PDF Assistant")

    uploaded_pdf = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_pdf:

        reader = PdfReader(uploaded_pdf)

        text = ""

        for page in reader.pages:
            text += page.extract_text()

        st.write(text[:5000])