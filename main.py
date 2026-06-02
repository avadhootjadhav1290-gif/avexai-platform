from db import supabase

response = supabase.table("test").select("*").execute()

print("DATA FROM SUPABASE:")
print(response.data)