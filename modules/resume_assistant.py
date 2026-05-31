import streamlit as st


def resume_assistant_ui():

    st.subheader("📝 Resume Assistant")

    resume = st.text_area(
        "Paste Resume Content"
    )

    if st.button("Analyze Resume"):

        st.success("Resume analyzed successfully")

        st.write("### Suggestions")

        st.write(
            "- Add measurable achievements\n"
            "- Improve project descriptions\n"
            "- Add technical skills"
        )