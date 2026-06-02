from fastapi import FastAPI
from db import supabase
from ai import get_ai_response

app = FastAPI()

# --------------------
# HOME
# --------------------
@app.get("/")
def home():
    return {"message": "AvexAI Running 🚀"}

# --------------------
# SIGNUP
# --------------------
@app.post("/signup")
def signup(user: dict):
    data = supabase.table("users").insert({
        "name": user["name"],
        "email": user["email"],
        "password": user["password"]
    }).execute()

    return {"status": "user created", "data": data.data}

# --------------------
# LOGIN
# --------------------
@app.post("/login")
def login(user: dict):
    data = supabase.table("users") \
        .select("*") \
        .eq("email", user["email"]) \
        .eq("password", user["password"]) \
        .execute()

    if len(data.data) == 0:
        return {"status": "failed", "message": "invalid credentials"}

    return {
        "status": "success",
        "user": data.data[0]
    }
# --------------------
# SEND MESSAGE
# --------------------
@app.post("/chat")
def chat(msg: dict):
    user_id = msg["user_id"]
    message = msg["message"]

    ai_response = get_ai_response(message)

    supabase.table("chats").insert({
        "user_id": user_id,
        "message": message,
        "response": ai_response
    }).execute()

    return {
        "message": message,
        "response": ai_response
    }
# --------------------
# GET CHAT HISTORY
# --------------------
@app.get("/history/{user_id}")
def history(user_id: int):
    data = supabase.table("chats") \
        .select("*") \
        .eq("user_id", user_id) \
        .order("id", desc=True) \
        .execute()

    return data.data