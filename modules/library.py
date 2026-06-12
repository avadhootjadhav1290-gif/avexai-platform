import streamlit as st

from modules.project_manager import (
    get_projects
)

import uuid
from modules.library_manager import (
    get_library_files,
    save_file_metadata,
    delete_file,
    process_file_for_rag
)

from db import supabase


def library_ui():

    st.title("📚 Library")

    if "upload_in_progress" not in st.session_state:
        st.session_state.upload_in_progress = False
    # LOAD PROJECTS

    projects = get_projects(
        st.session_state.user.email
    )
    
    project_lookup = {}

    for project in projects:

        project_lookup[
            project["id"]
        ] = project["name"]

    project_names = ["No Project"]

    project_map = {}

    for project in projects:

        project_names.append(
            project["name"]
        )

        project_map[
            project["name"]
        ] = project["id"]

    selected_project = st.selectbox(
        "Select Project",
        project_names
    )

    # FILE UPLOADER

    if "file_uploader_key" not in st.session_state:
        st.session_state["file_uploader_key"] = "default"

    uploaded_file = st.file_uploader(
        "Upload File",
        type=[
            "pdf",   
            "docx",
            "txt",
            "csv",
            "xlsx",
            "png",
            "jpg",
            "jpeg"
            ],
        key=st.session_state["file_uploader_key"]
    )

    if uploaded_file and not st.session_state.upload_in_progress:

        st.session_state.upload_in_progress = True

        project_id = None

        if selected_project != "No Project":

            project_id = project_map[
                selected_project
            ]

        file_path = (
            f"{st.session_state.user.email}/"
            f"{uuid.uuid4()}_{uploaded_file.name}"
        )

        try:
            
            existing = (
                supabase.table("library_files")
                .select("id")
                .eq(
                    "user_email",
                    st.session_state.user.email
                )
                .eq(
                    "file_name",
                    uploaded_file.name
                )
                .execute()
            )

            if existing.data:

                st.warning(
                    "This file already exists."
                )

                st.session_state.upload_in_progress = False

                return

            supabase.storage.from_(
                "library"
            ).upload(
                file_path,
                uploaded_file.getvalue(),
                {
                    "content-type": uploaded_file.type
                }
            )

        except Exception as e:

            if "Duplicate" in str(e):

                st.warning(
                    "File already exists. Please rename it or delete the old file."
                )

                st.session_state.upload_in_progress = False

                return

        file_id = save_file_metadata(
            st.session_state.user.email,
            uploaded_file.name,
            uploaded_file.type,
            file_path,
            uploaded_file.size,
            project_id
        )

        if uploaded_file.type == "application/pdf":

            with st.spinner(
                "Processing PDF..."
            ):

                process_pdf_for_rag(
                    file_id,
                    st.session_state.user.email,
                    project_id,
                    uploaded_file.getvalue()
                )

        st.success(
            "File uploaded successfully"
        )

        st.session_state.upload_in_progress = False

        st.session_state["file_uploader_key"] = str(
            uuid.uuid4()
        )

        st.rerun()

    # LOAD FILES

    files = get_library_files(
        st.session_state.user.email
    )

    if len(files) == 0:

        st.info(
            "No files uploaded yet"
        )

        return

    # SHOW FILES

    for file in files:

        project_name = "Unassigned"

        if file["project_id"]:

            project_name = project_lookup.get(
                file["project_id"],
                "Unknown Project"
            )

        st.write(
            f"📁 Project: {project_name}"
        )

        st.write(
            f"📄 {file['file_name']}"
        )

        st.write(
            f"Type: {file['file_type']}"
        )

        st.write(
            f"Size: {round(file['file_size']/1024,2)} KB"
        )

        file_url = supabase.storage.from_(
            "library"
        ).get_public_url(
            file["file_path"]
        )

        col1, col2 = st.columns(2)

        with col1:

            st.link_button(
                "Open File",
                file_url,
                key=f"open_{file['id']}"
            )

        with col2:

            if st.button(
                "Delete",
                key=f"delete_{file['id']}"
            ):

                success = delete_file(
                    file["id"],
                    file["file_path"]
                )

                if success:

                    st.success(
                        "File deleted"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Failed to delete file from Storage"
                    )

        st.divider()