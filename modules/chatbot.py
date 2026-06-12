import streamlit as st
import traceback
from groq import Groq
from db import supabase
from modules.chat_manager import (
    save_message,
    update_chat_title
)
from modules.excel_manager import (
    load_file,
    dataframe_summary
)
from modules.rag_manager import (
    get_document_context,
    get_chat_file_context
)
from modules.conversation_file_manager import (
    attach_file_to_chat,
    get_chat_files,
    get_chat_file_metadata
)
from modules.library_manager import (
    save_file_metadata,
    process_file_for_rag
)
import uuid

def get_chat_project_id(
    conversation_id
):

    result = (
        supabase.table(
            "conversations"
        )
        .select("project_id")
        .eq(
            "id",
            conversation_id
        )
        .single()
        .execute()
    )

    return result.data["project_id"]

def chatbot_ui():

    st.subheader("💬 Avex AI Chatbot")

    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    if "attached_dataframes" not in st.session_state:
        st.session_state.attached_dataframes = {}
        
    if "loaded_chat_context" not in st.session_state:
        st.session_state.loaded_chat_context = None
        
    if "chat_files" not in st.session_state:
        st.session_state.chat_files = []
        
    if "processed_uploads" not in st.session_state:
        st.session_state.processed_uploads = set()

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    if (
        st.session_state.get("conversation_id")
        and st.session_state.loaded_chat_context
        != st.session_state.conversation_id
    ):

        # Clear previous spreadsheet cache
        st.session_state.attached_dataframes = {}

        # Mark this conversation as loaded
        st.session_state.loaded_chat_context = (
            st.session_state.conversation_id
        )

    uploader_key = (
        f"chat_file_{st.session_state.get('conversation_id', 'default')}"
    )

    chat_file = st.file_uploader(
        "📎 Attach File",
        type=[
            "pdf",
            "docx",
            "txt",
            "csv",
            "xlsx",
            "pptx",
            "png",
            "jpg",
            "jpeg"
        ],
        key=uploader_key
    )
    
    upload_signature = None

    if chat_file:
        upload_signature = (
            st.session_state.conversation_id,
            chat_file.name,
            chat_file.size
        )

    if (
        chat_file
        and st.session_state.get("conversation_id")
        and upload_signature not in st.session_state.processed_uploads
    ):

        file_path = (
            f"{st.session_state.user.email}/"
            f"{uuid.uuid4()}_{chat_file.name}"
        )

        try:

            supabase.storage.from_(
                "library"
            ).upload(
                file_path,
                chat_file.getvalue(),
                {
                    "content-type": chat_file.type
                }
            )
            
            project_id = get_chat_project_id(
                st.session_state.conversation_id
            )

            file_id = save_file_metadata(
                st.session_state.user.email,
                chat_file.name,
                chat_file.type,
                file_path,
                chat_file.size,
                project_id
            )

            attach_file_to_chat(
                st.session_state.conversation_id,
                file_id
            )
            if (
                chat_file.name.endswith(".csv")
                or chat_file.name.endswith(".xlsx")
                or chat_file.name.endswith(".xls")
            ):

                chat_file.seek(0)

                df = load_file(chat_file)

                if df is not None:

                    summary = dataframe_summary(df)

                    st.session_state.attached_dataframes[str(file_id)] = summary

            if chat_file.name.lower().endswith(
                (
                    ".pdf",
                    ".docx",
                    ".txt",
                    ".pptx",
                    ".png",
                    ".jpg",
                    ".jpeg"
                )
            ):

                process_file_for_rag(
                    file_id=file_id,
                    user_email=st.session_state.user.email,
                    project_id=None,
                    file_name=chat_file.name,
                    file_bytes=chat_file.getvalue()
                )

                st.toast("File uploaded successfully ✅")
                
                st.session_state.processed_uploads.add(
                    upload_signature
                )

            #st.success("File attached to chat" )
            
            # st.session_state.last_uploaded_chat_file = chat_file.name

            #st.rerun()

        except Exception as e:

            st.error(str(e))

            st.code(
                traceback.format_exc()
            )
        
    user_input = st.chat_input(
        "Ask anything..."
    )

    if user_input:

        # Auto-title new conversations
        if (
            st.session_state.get("conversation_id")
            and len(st.session_state.messages) == 0
        ):

            title = user_input[:40]

            update_chat_title(
                st.session_state.conversation_id,
                title
            )

        # Show user message
        with st.chat_message("user"):
            st.write(user_input)

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        # Save user message
        if st.session_state.get("conversation_id"):

            save_message(
                st.session_state.conversation_id,
                "user",
                user_input
            )

        # Generate AI response
        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                context = ""

                if st.session_state.get("conversation_id"):

                    chat_files = get_chat_files(
                        st.session_state.conversation_id
                    )
                    
                    st.write("DEBUG conversation_id:", st.session_state.conversation_id)
                    st.write("DEBUG attached file IDs:", chat_files)

                    context = get_chat_file_context(
                        user_input,
                        chat_files
                    )

                # Excel / CSV Context
                spreadsheet_context = ""

                for data in (
                    st.session_state
                    .attached_dataframes
                    .values()
                ):

                    spreadsheet_context += data
                    spreadsheet_context += "\n\n"

                system_prompt = f"""
                You are AvexAI.

                Answer naturally and professionally.

                Use uploaded documents if relevant.

                Do not mention internal implementation details such as:
                - PDF Context
                - Spreadsheet Context
                - Context Length

                If Document Context is empty, explicitly state that no document context is available.

                If Document Context is available:
                - Use it to answer questions about uploaded documents.

                Document Context:
                {context}

                SPREADSHEET DATA:
                {spreadsheet_context}
                """
                
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt
                        }
                    ]
                    +
                    [
                        {
                            "role": msg["role"],
                            "content": msg["content"]
                        }
                        for msg in st.session_state.messages
                    ]
                )

                answer = response.choices[0].message.content

                st.write(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        # Save assistant message
        if st.session_state.get("conversation_id"):

            save_message(
                st.session_state.conversation_id,
                "assistant",
                answer
            )
