from db import supabase


def create_chat(user_email, project_id=None):

    result = supabase.table(
        "conversations"
    ).insert(
        {
            "user_email": user_email,
            "title": "New Chat",
            "project_id": project_id
        }
    ).execute()

    return result.data[0]["id"]

def get_user_chats(user_email):

    result = supabase.table(
        "conversations"
    ).select("*").eq(
        "user_email",
        user_email
    ).order(
        "created_at",
        desc=True
    ).execute()

    return result.data


def save_message(
    conversation_id,
    role,
    content
):

    supabase.table(
        "messages"
    ).insert(
        {
            "conversation_id": conversation_id,
            "role": role,
            "content": content
        }
    ).execute()


def load_messages(
    conversation_id
):

    result = supabase.table(
        "messages"
    ).select("*").eq(
        "conversation_id",
        conversation_id
    ).order(
        "created_at"
    ).execute()

    return result.data


def get_chat_messages(conversation_id):

    result = supabase.table(
        "messages"
    ).select("*").eq(
        "conversation_id",
        conversation_id
    ).order(
        "created_at"
    ).execute()

    return result.data


def update_chat_title(
    conversation_id,
    title
):

    supabase.table(
        "conversations"
    ).update(
        {
            "title": title
        }
    ).eq(
        "id",
        conversation_id
    ).execute()


def rename_chat(
    conversation_id,
    new_title
):

    supabase.table(
        "conversations"
    ).update(
        {
            "title": new_title
        }
    ).eq(
        "id",
        conversation_id
    ).execute()
    
def delete_chat(conversation_id):

    supabase.table(
        "conversations"
    ).delete().eq(
        "id",
        conversation_id
    ).execute()
    
def pin_chat(chat_id):

    supabase.table(
        "conversations"
    ).update(
        {
            "pinned": True
        }
    ).eq(
        "id",
        chat_id
    ).execute()


def unpin_chat(chat_id):

    supabase.table(
        "conversations"
    ).update(
        {
            "pinned": False
        }
    ).eq(
        "id",
        chat_id
    ).execute()


def archive_chat(chat_id):

    supabase.table(
        "conversations"
    ).update(
        {
            "archived": True
        }
    ).eq(
        "id",
        chat_id
    ).execute()


def unarchive_chat(chat_id):

    supabase.table(
        "conversations"
    ).update(
        {
            "archived": False
        }
    ).eq(
        "id",
        chat_id
    ).execute()

def get_pinned_chats(user_email):

    result = supabase.table(
        "conversations"
    ).select("*").eq(
        "user_email",
        user_email
    ).eq(
        "pinned",
        True
    ).eq(
        "archived",
        False
    ).order(
        "created_at",
        desc=True
    ).execute()

    return result.data


def get_normal_chats(user_email):

    result = supabase.table(
        "conversations"
    ).select("*").eq(
        "user_email",
        user_email
    ).eq(
        "pinned",
        False
    ).eq(
        "archived",
        False
    ).order(
        "created_at",
        desc=True
    ).execute()

    return result.data

def get_archived_chats(user_email):

    result = supabase.table(
        "conversations"
    ).select("*").eq(
        "user_email",
        user_email
    ).eq(
        "archived",
        True
    ).order(
        "created_at",
        desc=True
    ).execute()

    return result.data

def duplicate_chat(chat_id, user_email):

    chat = (
        supabase.table("conversations")
        .select("*")
        .eq("id", chat_id)
        .execute()
    )

    if not chat.data:
        return

    original = chat.data[0]

    new_chat = (
        supabase.table("conversations")
        .insert(
            {
                "user_email": user_email,
                "title": original["title"] + " Copy"
            }
        )
        .execute()
    )

    new_chat_id = new_chat.data[0]["id"]

    messages = (
        supabase.table("messages")
        .select("*")
        .eq("conversation_id", chat_id)
        .execute()
    )

    for msg in messages.data:

        supabase.table("messages").insert(
            {
                "conversation_id": new_chat_id,
                "role": msg["role"],
                "content": msg["content"]
            }
        ).execute()
        
def get_sorted_chats(
    user_email,
    sort_by="Recent"
):

    query = (
        supabase.table("conversations")
        .select("*")
        .eq("user_email", user_email)
        .eq("archived", False)
    )

    if sort_by == "Oldest":

        result = query.order(
            "created_at",
            desc=False
        ).execute()

    else:

        result = query.order(
            "created_at",
            desc=True
        ).execute()

    return result.data        