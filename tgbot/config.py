import os
from dotenv import load_dotenv
import json
import re

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
ALLOWED_USERS = os.getenv("ALLOWED_USER_IDS", "").split(",")

# Google Credentials - Multiple fallback methods
GOOGLE_CREDS_DICT = None
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")

def clean_json_string(raw_string):
    """JSON string ko clean karein - newlines, extra spaces hatao"""
    if not raw_string:
        return None
    # Extra spaces aur newlines hatao
    cleaned = re.sub(r'\s+', ' ', raw_string.strip())
    # \n ko properly escape karo
    cleaned = cleaned.replace('\\n', '\\\\n')
    return cleaned

if GOOGLE_CREDENTIALS_JSON:
    try:
        # Method 1: Direct load
        GOOGLE_CREDS_DICT = json.loads(GOOGLE_CREDENTIALS_JSON)
        print("✅ JSON loaded successfully (Method 1)")
    except json.JSONDecodeError as e1:
        try:
            # Method 2: Clean karke load
            cleaned = clean_json_string(GOOGLE_CREDENTIALS_JSON)
            GOOGLE_CREDS_DICT = json.loads(cleaned)
            print("✅ JSON loaded successfully (Method 2 - Cleaned)")
        except json.JSONDecodeError as e2:
            try:
                # Method 3: Raw string ko manually parse karein (last resort)
                # Private key ko alag se handle karein
                raw = GOOGLE_CREDENTIALS_JSON
                # Private key ko properly escape karein
                raw = raw.replace('\\n', '\\\\n')
                raw = raw.replace('\n', ' ')
                GOOGLE_CREDS_DICT = json.loads(raw)
                print("✅ JSON loaded successfully (Method 3 - Manual)")
            except Exception as e3:
                print(f"❌ All JSON parsing methods failed: {e3}")
                GOOGLE_CREDS_DICT = None

if not GOOGLE_CREDS_DICT:
    print("⚠️ WARNING: Google credentials not loaded. Sheet verification will not work.")