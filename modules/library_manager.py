from modules.rag_manager import (
    extract_pdf_text,
    extract_docx_text,
    extract_txt_text,
    extract_pptx_text,
    extract_image_text,
    chunk_text,
    generate_embedding
)

from db import supabase

def get_library_files(
    user_email
):

    result = supabase.table(
        "library_files"
    ).select("*").eq(
        "user_email",
        user_email
    ).order(
        "created_at",
        desc=True
    ).execute()

    return result.data


def save_file_metadata(
    user_email,
    file_name,
    file_type,
    file_path,
    file_size,
    project_id=None
):

    result = supabase.table(
        "library_files"
    ).insert(
        {
            "user_email": user_email,
            "project_id": project_id,
            "file_name": file_name,
            "file_type": file_type,
            "file_path": file_path,
            "file_size": file_size
        }
    ).execute()

    return result.data[0]["id"]


def delete_file(
    file_id,
    file_path
):

    try:

        print(f"Deleting storage file: {file_path}")

        result = supabase.storage.from_(
            "library"
        ).remove(
            [file_path]
        )

        print("Storage result:", result)

        supabase.table(
            "library_files"
        ).delete().eq(
            "id",
            file_id
        ).execute()

        return True

    except Exception as e:

        print("DELETE ERROR:", e)

        return False
    
def process_file_for_rag(
    file_id,
    user_email,
    project_id,
    file_name,
    file_bytes
):
    print("========== PDF DEBUG ==========")
    print("file_id:", file_id)
    print("user_email:", user_email)
    print("project_id:", project_id)

    supabase.table(
        "document_chunks"
    ).delete().eq(
        "file_id",
        file_id
    ).execute()

    extension = file_name.lower().split(".")[-1]

    if extension == "pdf":

        text = extract_pdf_text(file_bytes)

    elif extension == "docx":

        text = extract_docx_text(file_bytes)

    elif extension == "txt":

        text = extract_txt_text(file_bytes)

    elif extension == "pptx":

        text = extract_pptx_text(file_bytes)

    elif extension in ["png", "jpg", "jpeg"]:

        text = extract_image_text(file_bytes)

    else:

        text = ""

    print("PDF TEXT LENGTH:", len(text))

    chunks = chunk_text(text)

    print("NUMBER OF CHUNKS:", len(chunks))

    for index, chunk in enumerate(chunks):
        embedding = generate_embedding(chunk)

        supabase.table(
            "document_chunks"
        ).insert(
            {
                "file_id": file_id,
                "user_email": user_email,
                "project_id": project_id,
                "chunk_index": index,
                "chunk_text": chunk,
                "embedding": embedding
            }
        ).execute()

    print("PDF PROCESS COMPLETE")