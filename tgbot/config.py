import os
from dotenv import load_dotenv
import json

load_dotenv()

# Environment variables se load karein
BOT_TOKEN = os.getenv("BOT_TOKEN")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
ALLOWED_USERS = os.getenv("ALLOWED_USER_IDS", "").split(",")

# Google Credentials - JSON string ko dict mein convert karein
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")
if GOOGLE_CREDENTIALS_JSON:
    try:
        GOOGLE_CREDS_DICT = json.loads(GOOGLE_CREDENTIALS_JSON)
    except json.JSONDecodeError:
        # Agar string mein newline issues hain toh fix karein
        GOOGLE_CREDENTIALS_JSON = GOOGLE_CREDENTIALS_JSON.replace('\n', '\\n')
        GOOGLE_CREDS_DICT = json.loads(GOOGLE_CREDENTIALS_JSON)
else:
    GOOGLE_CREDS_DICT = None