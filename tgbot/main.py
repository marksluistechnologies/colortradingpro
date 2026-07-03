import asyncio
import gspread
from aiogram import Bot, Dispatcher, types
from google.oauth2.service_account import Credentials
from .config import BOT_TOKEN, GOOGLE_SHEET_ID, GOOGLE_CREDS_DICT, WEBHOOK_URL
from .handlers import setup_handlers

class TGBot:
    def __init__(self):
        self.bot = Bot(token=BOT_TOKEN)
        self.dp = Dispatcher()
        self.sheet = None
        
        # Google Sheets Setup
        if GOOGLE_CREDS_DICT and GOOGLE_SHEET_ID:
            try:
                scopes = ["https://www.googleapis.com/auth/spreadsheets"]
                creds = Credentials.from_service_account_info(GOOGLE_CREDS_DICT, scopes=scopes)
                self.gc = gspread.authorize(creds)
                self.sheet = self.gc.open_by_key(GOOGLE_SHEET_ID).sheet1
                print("✅ Google Sheet connected successfully!")
            except Exception as e:
                print(f"⚠️ Google Sheet connection failed: {e}")
        else:
            print("⚠️ Google Sheets credentials missing. Bot will run without sheet access.")
        
        # Handlers setup
        router = setup_handlers(self)
        self.dp.include_router(router)
        
        # Webhook set karein (sirf local ya first deploy mein)
        if WEBHOOK_URL and "vercel" in WEBHOOK_URL:
            try:
                # Event loop handle karein
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.set_webhook())
                print(f"✅ Webhook set to: {WEBHOOK_URL}")
            except Exception as e:
                print(f"⚠️ Webhook setup failed: {e}")
    
    async def set_webhook(self):
        if WEBHOOK_URL:
            await self.bot.set_webhook(WEBHOOK_URL)
    
    async def update_bot(self, update_dict: dict):
        """Update ko process karein - safe version"""
        try:
            update = types.Update(**update_dict)
            # Aiogram ke feed_update ko call karein
            await self.dp.feed_update(self.bot, update)
        except Exception as e:
            print(f"❌ update_bot error: {e}")
            raise e  # Error ko upar bhejein
    
    def verify_uid(self, uid: str) -> bool:
        """Check if UID exists in Google Sheet Column A"""
        if not self.sheet:
            print("❌ Sheet not available")
            return False
        try:
            uid_column = self.sheet.col_values(1)
            return uid in uid_column
        except Exception as e:
            print(f"Google Sheet Error: {e}")
            return False

# Singleton instance
tgbot = TGBot()