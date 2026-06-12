import streamlit as st
from db import supabase


def reset_password_page():
    st.title("🔑 Reset Password")

    new_password = st.text_input(
        "New Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("Update Password"):

        if not new_password:
            st.error("Please enter a new password.")
            return

        if new_password != confirm_password:
            st.error("Passwords do not match.")
            return

        try:
            supabase.auth.update_user(
                {
                    "password": new_password
                }
            )

            st.success(
                "Password updated successfully. Please log in with your new password."
            )

        except Exception as e:
            st.error(str(e))