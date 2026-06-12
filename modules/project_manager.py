# modules/project_manager.py

from db import supabase


def create_project(
    user_email,
    project_name
):

    result = supabase.table(
        "projects"
    ).insert(
        {
            "user_email": user_email,
            "name": project_name
        }
    ).execute()

    return result.data[0]["id"]


def get_projects(user_email):

    result = supabase.table(
        "projects"
    ).select("*").eq(
        "user_email",
        user_email
    ).order(
        "created_at",
        desc=True
    ).execute()

    return result.data


def rename_project(
    project_id,
    new_name
):

    supabase.table(
        "projects"
    ).update(
        {
            "name": new_name
        }
    ).eq(
        "id",
        project_id
    ).execute()


def delete_project(
    project_id
):

    supabase.table(
        "projects"
    ).delete().eq(
        "id",
        project_id
    ).execute()

def move_chat_to_project(
    chat_id,
    project_id
):

    supabase.table(
        "conversations"
    ).update(
        {
            "project_id": project_id
        }
    ).eq(
        "id",
        chat_id
    ).execute()
    
def get_project_chats(
    project_id
):

    result = supabase.table(
        "conversations"
    ).select("*").eq(
        "project_id",
        project_id
    ).execute()

    return result.data

def get_project_name(
    project_id
):

    result = supabase.table(
        "projects"
    ).select(
        "name"
    ).eq(
        "id",
        project_id
    ).execute()

    if len(result.data) == 0:

        return "Unknown Project"

    return result.data[0]["name"]