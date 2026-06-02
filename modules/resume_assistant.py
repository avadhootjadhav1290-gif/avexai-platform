import streamlit as st
from groq import Groq

def resume_assistant_ui():
    st.subheader("📝 Resume Assistant")
    st.caption("Upload or paste your resume for AI suggestions.")

    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    resume = st.text_area("Paste your resume content:")

    if st.button("Analyze Resume"):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a career coach."},
                {"role": "user", "content": f"Resume:\n{resume}\n\nPlease suggest improvements."}
            ]
        )
        st.write(response.choices[0].message.content)
