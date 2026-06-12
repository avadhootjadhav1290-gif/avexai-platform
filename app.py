import streamlit as st
from modules.projects import projects_ui
from modules.library import library_ui
from modules.chatbot import chatbot_ui
from modules.admin_dashboard import admin_dashboard_ui
from modules.profile import profile_ui
from modules.project_manager import (
    create_project,
    get_projects,
    rename_project,
    delete_project,
    move_chat_to_project,
    get_project_chats
)
from modules.chat_manager import (
    create_chat,
    get_chat_messages,
    rename_chat,
    delete_chat,
    pin_chat,
    unpin_chat,
    archive_chat,
    unarchive_chat,
    get_pinned_chats,
    get_normal_chats,
    get_archived_chats,
    duplicate_chat,
    get_sorted_chats
)

from modules.login_system import (
    login_page,
    logout
)

from modules.admin_check import is_admin
#from modules.reset_password import reset_password_page


st.set_page_config(
    page_title="AvexAI",
    page_icon="🤖",
    layout="wide"
)

# ---------------- LOGIN ----------------
if "user" not in st.session_state and "guest" not in st.session_state:
    login_page()
    st.stop()

# ---------------- USER ----------------

user_email = None

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "page" not in st.session_state:
    st.session_state.page = "chat"

if "user" in st.session_state:
    user_email = st.session_state.user.email

admin_access = False

if user_email:
    admin_access = is_admin(user_email)

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("🧠 AvexAI")
    st.caption("Your AI Assistant")

    # NEW CHAT

    if st.button("➕ New Chat"):

        if user_email:

            chat_id = create_chat(
                user_email,
                st.session_state.get("project_id")
            )

            st.session_state.conversation_id = chat_id
            st.session_state.messages = []
            st.session_state.page = "chat"

            # Clear previous chat attachments
            st.session_state.attached_dataframes = {}
            st.session_state.processed_uploads = set()
            #st.session_state.last_uploaded_chat_file = None

            st.rerun()

    # CHAT ACTIONS

    if st.session_state.get("conversation_id"):

        st.markdown("---")

        new_name = st.text_input(
            "Rename Current Chat"
        )

        if st.button("💾 Save Name"):

            if new_name.strip():

                rename_chat(
                    st.session_state.conversation_id,
                    new_name
                )

                st.rerun()

        projects = get_projects(
            user_email
        )

        if len(projects) > 0:

            project_names = {
                project["name"]: project["id"]
                for project in projects
            }

            selected_project = st.selectbox(
                "Move Chat To Project",
                list(project_names.keys())
            )

            if st.button(
                "📁 Move Chat"
            ):

                move_chat_to_project(
                    st.session_state.conversation_id,
                    project_names[selected_project]
                )

                st.success(
                    "Chat moved successfully"
                )

                st.rerun()
        
        if st.button("📌 Pin Current Chat"):

            pin_chat(
                st.session_state.conversation_id
            )

            st.rerun()

        if st.button("📂 Archive Current Chat"):

            archive_chat(
                st.session_state.conversation_id
            )

            st.session_state.conversation_id = None
            st.session_state.messages = []

            st.rerun()

        if st.button("🗑 Delete Current Chat"):

            delete_chat(
                st.session_state.conversation_id
            )

            st.session_state.conversation_id = None
            st.session_state.messages = []

            st.rerun()
            

# CHAT LIST

    if user_email:

        st.markdown("---")

        search_query = st.text_input(
            "🔍 Search Chats"
        )

        sort_option = st.selectbox(
            "Sort Chats",
            [
                "Recent",
                "Oldest"
            ]
        )

        pinned_chats = get_pinned_chats(
            user_email
        )

        normal_chats = get_sorted_chats(
            user_email,
            sort_option
        )

        archived_chats = get_archived_chats(
            user_email
        )

        # SEARCH

        if search_query:

            pinned_chats = [
                chat for chat in pinned_chats
                if search_query.lower()
                in chat["title"].lower()
            ]

            normal_chats = [
                chat for chat in normal_chats
                if search_query.lower()
                in chat["title"].lower()
            ]

            archived_chats = [
                chat for chat in archived_chats
                if search_query.lower()
                in chat["title"].lower()
            ]

        # ---------------- PINNED ----------------

        if len(pinned_chats) > 0:

            st.markdown("### 📌 Pinned")

            for chat in pinned_chats:

                col1, col2 = st.columns([4, 1])

                with col1:

                    if st.button(
                        f"💬 {chat['title']}",
                        key=f"pin_{chat['id']}"
                    ):

                        st.session_state.conversation_id = chat["id"]

                        messages = get_chat_messages(
                            chat["id"]
                        )

                        st.session_state.messages = [
                            {
                                "role": msg["role"],
                                "content": msg["content"]
                            }
                            for msg in messages
                        ]

                        st.session_state.page = "chat"

                        st.rerun()

                with col2:

                    if st.button(
                        "📍",
                        key=f"unpin_{chat['id']}"
                    ):

                        unpin_chat(
                            chat["id"]
                        )

                        st.rerun()

        # ---------------- NORMAL ----------------

        st.markdown("### 💬 Chats")

        for chat in normal_chats:

            col1, col2 = st.columns([4, 1])

            with col1:

                if st.button(
                    f"💬 {chat['title']}",
                    key=f"chat_{chat['id']}"
                ):

                    st.session_state.conversation_id = chat["id"]

                    messages = get_chat_messages(
                        chat["id"]
                    )

                    st.session_state.messages = [
                        {
                            "role": msg["role"],
                            "content": msg["content"]
                        }
                        for msg in messages
                    ]

                    st.session_state.page = "chat"

                    st.rerun()

            with col2:

                if st.button(
                    "📄",
                    key=f"copy_{chat['id']}"
                ):

                    duplicate_chat(
                        chat["id"],
                        user_email
                    )

                    st.rerun()

        # ---------------- ARCHIVED ----------------

        if len(archived_chats) > 0:

            st.markdown("### 📂 Archive")

            for chat in archived_chats:

                col1, col2 = st.columns([4, 1])

                with col1:

                    if st.button(
                        f"💬 {chat['title']}",
                        key=f"archive_{chat['id']}"
                    ):

                        st.session_state.conversation_id = chat["id"]

                        messages = get_chat_messages(
                            chat["id"]
                        )

                        st.session_state.messages = [
                            {
                                "role": msg["role"],
                                "content": msg["content"]
                            }
                            for msg in messages
                        ]

                        st.session_state.page = "chat"

                        st.rerun()

                with col2:

                    if st.button(
                        "♻️",
                        key=f"restore_{chat['id']}"
                    ):

                        unarchive_chat(
                            chat["id"]
                        )

                        st.rerun()     

        # PROFILE

        if st.button("📁 Projects"):

            st.session_state.page = "projects"

            st.rerun()

        if st.button("📚 Library"):

            st.session_state.page = "library"

            st.rerun()
        
        if st.button("👤 Profile"):

            st.session_state.page = "profile"

            st.rerun()

        # ADMIN

        if admin_access:

            if st.button("📈 Admin Dashboard"):

                st.session_state.page = "admin"

                st.rerun()

        # LOGOUT

        st.markdown("---")

        if user_email:
            st.write(f"👤 {user_email}")

        if st.button("🚪 Logout"):

            logout()

# ---------------- MAIN ----------------

if st.session_state.page == "admin":

    admin_dashboard_ui()

elif st.session_state.page == "profile":

    profile_ui()

elif st.session_state.page == "projects":

    projects_ui()
    
elif st.session_state.page == "library":

    library_ui()

else:

    chatbot_ui()