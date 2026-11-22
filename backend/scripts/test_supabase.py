import os
import sys

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")
if not url or not key:
    sys.exit("SUPABASE_URL or SUPABASE_SERVICE_KEY is missing. Check backend/.env.")

client = create_client(url, key)
result = client.table("projects").select("id", count="exact").execute()

print("Connected to Supabase.")
print(f"Rows in projects table: {result.count}")