from db import supabase


def attach_file_to_chat(
    conversation_id,
    file_id
):

    supabase.table(
        "conversation_files"
    ).insert(
        {
            "conversation_id": conversation_id,
            "file_id": file_id
        }
    ).execute()


def get_chat_files(
    conversation_id
):

    result = (
        supabase.table(
            "conversation_files"
        )
        .select(
            "file_id"
        )
        .eq(
            "conversation_id",
            conversation_id
        )
        .execute()
    )

    return [
        item["file_id"]
        for item in result.data
    ]
    
def get_chat_file_metadata(
    conversation_id
):

    result = (
        supabase.table(
            "conversation_files"
        )
        .select(
            "file_id, library_files(*)"
        )
        .eq(
            "conversation_id",
            conversation_id
        )
        .execute()
    )

    return result.data

