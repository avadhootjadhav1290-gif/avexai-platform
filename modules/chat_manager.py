from db import supabase


def create_chat(user_email):

    result = supabase.table(
        "conversations"
    ).insert(
        {
            "user_email": user_email
        }
    ).execute()

    return result.data[0]["id"]


def get_user_chats(user_email):

    result = supabase.table(
        "conversations"
    ).select("*").eq(
        "user_email",
        user_email
    ).execute()

    return result.data