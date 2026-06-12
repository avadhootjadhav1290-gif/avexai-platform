# modules/login_system.py

import streamlit as st
from db import supabase


def signup(email, password):

    try:

        result = supabase.auth.sign_up(
            {
                "email": email,
                "password": password
            }
        )

        if result.user:

            supabase.table(
                "users"
            ).insert(
                {
                    "id": result.user.id,
                    "email": email,
                    "role": "user"
                }
            ).execute()

        st.success(
            "Account created successfully!"
        )

    except Exception as e:

        st.error(str(e))


def login(email, password):

    try:

        result = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password
            }
        )

        st.session_state.user = result.user

        st.success("Login successful")

        st.rerun()

    except Exception as e:

        st.error(str(e))


def reset_password(email):

    if not email.strip():

        st.error("Please enter your email address.")

        return

    try:

        supabase.auth.reset_password_email(email)

        st.success(
            "Password reset email has been sent. Please check your inbox."
        )

    except Exception as e:

        st.error(str(e))


def logout():

    supabase.auth.sign_out()

    st.session_state.clear()

    st.rerun()


def login_page():

    st.title("🔐 Welcome to AvexAI")

    option = st.radio(
        "Choose",
        [
            "Login",
            "Signup",
            "Continue as Guest"
        ]
    )

    if option == "Continue as Guest":

        st.session_state["guest"] = True

        st.rerun()

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if option == "Signup":

        if st.button("Create Account"):

            signup(email, password)

    if option == "Login":

        if st.button("Login"):

            login(email, password)

        if st.button("Forgot Password?"):

            reset_password(email)