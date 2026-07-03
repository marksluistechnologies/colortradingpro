import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Handle Allowed Users safely
allowed_users_raw = os.getenv("ALLOWED_USER_IDS", "")
ALLOWED_USERS = [u.strip() for u in allowed_users_raw.split(",") if u.strip()]

GOOGLE_CREDS_DICT = None
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")

def clean_json_string(raw_string):
    if not raw_string:
        return None
    cleaned = re.sub(r'\s+', ' ', raw_string.strip())
    cleaned = cleaned.replace('\\n', '\\\\n')
    return cleaned

if GOOGLE_CREDENTIALS_JSON:
    try:
        GOOGLE_CREDS_DICT = json.loads(GOOGLE_CREDENTIALS_JSON)
        print("✅ JSON loaded successfully (Method 1)")
    except json.JSONDecodeError:
        try:
            cleaned = clean_json_string(GOOGLE_CREDENTIALS_JSON)
            GOOGLE_CREDS_DICT = json.loads(cleaned)
            print("✅ JSON loaded successfully (Method 2)")
        except json.JSONDecodeError as e:
            print(f"❌ All JSON parsing methods failed: {e}")
            GOOGLE_CREDS_DICT = None