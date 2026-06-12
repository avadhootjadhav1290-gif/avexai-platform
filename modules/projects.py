import streamlit as st

from modules.project_manager import (
    create_project,
    get_projects,
    get_project_chats
)

from modules.chat_manager import (
    get_chat_messages
)


def projects_ui():

    st.title("📁 Projects")

    user_email = st.session_state.user.email

    # CREATE PROJECT

    new_project = st.text_input(
        "Project Name"
    )

    if st.button(
        "Create Project"
    ):

        if new_project:

            create_project(
                user_email,
                new_project
            )

            st.rerun()

    st.divider()

    projects = get_projects(
        user_email
    )

    # PROJECT LIST

    for project in projects:

        project_chats = get_project_chats(
            project["id"]
        )

        with st.expander(
            f"📁 {project['name']} ({len(project_chats)} chats)"
        ):

            if len(project_chats) == 0:

                st.info(
                    "No chats in this project"
                )

            for chat in project_chats:

                if st.button(
                    f"💬 {chat['title']}",
                    key=f"project_chat_{chat['id']}"
                ):

                    messages = get_chat_messages(
                        chat["id"]
                    )

                    st.session_state.conversation_id = chat["id"]

                    st.session_state.messages = []

                    for msg in messages:

                        st.session_state.messages.append(
                            {
                                "role": msg["role"],
                                "content": msg["content"]
                            }
                        )

                    st.session_state.page = "chat"

                    st.rerun()