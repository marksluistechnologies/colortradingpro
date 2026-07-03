import asyncio
import json
import gspread
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from google.oauth2.service_account import Credentials
from gtts import gTTS
import os
from .config import BOT_TOKEN, GOOGLE_SHEET_ID, GOOGLE_CREDENTIALS_JSON, WEBHOOK_URL
from .handlers import router

class TGBot:
    def __init__(self):
        self.bot = Bot(token=BOT_TOKEN)
        self.dp = Dispatcher()
        self.dp.include_router(router)
        
        # Google Sheets Setup
        creds_dict = json.loads(GOOGLE_CREDENTIALS_JSON)
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        self.gc = gspread.authorize(creds)
        self.sheet = self.gc.open_by_key(GOOGLE_SHEET_ID).sheet1
        
        # Set Webhook
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.set_webhook())
    
    async def set_webhook(self):
        await self.bot.set_webhook(WEBHOOK_URL)
    
    async def update_bot(self, update_dict: dict):
        update = types.Update(**update_dict)
        await self.dp.feed_update(self.bot, update)
    
    def verify_uid(self, uid: str) -> bool:
        """Check if UID exists in Google Sheet Column A"""
        try:
            uid_column = self.sheet.col_values(1)  # Column A
            return uid in uid_column
        except Exception as e:
            print(f"Google Sheet Error: {e}")
            return False

tgbot = TGBot()