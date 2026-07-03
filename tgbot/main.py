import asyncio
import gspread
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from google.oauth2.service_account import Credentials
from gtts import gTTS
import os
import tempfile
from .config import BOT_TOKEN, GOOGLE_SHEET_ID, GOOGLE_CREDS_DICT, WEBHOOK_URL
from .handlers import router

class TGBot:
    def __init__(self):
        self.bot = Bot(token=BOT_TOKEN)
        self.dp = Dispatcher()
        self.dp.include_router(router)
        
        # Google Sheets Setup - Sirf tabhi agar credentials available hain
        if GOOGLE_CREDS_DICT and GOOGLE_SHEET_ID:
            try:
                scopes = ["https://www.googleapis.com/auth/spreadsheets"]
                creds = Credentials.from_service_account_info(GOOGLE_CREDS_DICT, scopes=scopes)
                self.gc = gspread.authorize(creds)
                self.sheet = self.gc.open_by_key(GOOGLE_SHEET_ID).sheet1
                print("✅ Google Sheet connected successfully!")
            except Exception as e:
                print(f"❌ Google Sheet connection failed: {e}")
                self.sheet = None
        else:
            print("⚠️ Google Sheets credentials missing. Bot will run without sheet access.")
            self.sheet = None
        
        # Webhook set karein
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.set_webhook())
        except Exception as e:
            print(f"⚠️ Webhook setup failed (maybe already set): {e}")
    
    async def set_webhook(self):
        if WEBHOOK_URL:
            await self.bot.set_webhook(WEBHOOK_URL)
            print(f"✅ Webhook set to: {WEBHOOK_URL}")
        else:
            print("⚠️ WEBHOOK_URL not set, skipping webhook setup")
    
    async def update_bot(self, update_dict: dict):
        update = types.Update(**update_dict)
        await self.dp.feed_update(self.bot, update)
    
    def verify_uid(self, uid: str) -> bool:
        """Check if UID exists in Google Sheet Column A"""
        if not self.sheet:
            print("❌ Sheet not available")
            return False
        try:
            uid_column = self.sheet.col_values(1)  # Column A
            return uid in uid_column
        except Exception as e:
            print(f"Google Sheet Error: {e}")
            return False

# Singleton instance
tgbot = TGBot()