import streamlit as st
from pypdf import PdfReader   # only use pypdf

def pdf_chat_ui():
    st.subheader("📄 PDF Assistant")
    st.caption("Upload PDF files and ask questions about their content.")

    uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_pdf:
        reader = PdfReader(uploaded_pdf)
        text = "".join(page.extract_text() for page in reader.pages)
        st.text_area("Extracted Text", text[:3000])
