import os
from aiogram import Router, types
from aiogram.filters import Command

router = Router()

WELCOME_TEXT = """
<b>🎉 Colour Trading Pro - Family Mein Swagat Hai!</b>

📌 <b>Sabse Pehle Aur Sabse Zaroori Baat:</b>
Yeh channel bilkul <b>FREE</b> hai.

🔥 <b>Hamara Unique System:</b>
✅ Accurate Signals - Green/Red/Violet prediction
✅ Free Hack Mod APK - Sirf verified members ke liye
✅ Daily Lucky Winners - 10 members ko ₹100 free deposit

⚠️ <b>Golden Rule:</b>
1. Register karein: https://13lgame18.com/register?inviteCode=HTJ65XW&from=web
2. UID DM karein @tech_jadugar ko
3. Verification ke baad hack APK milega

📌 <b>Commands:</b>
/start - Welcome message
/verify [UID] - Apni UID verify karayein
/getapk - Verified hone par hack APK milega
"""

# Aapki final working Telegram Voice File ID
VOICE_FILE_ID = "CQACAgUAAxkBAAFOI89qSCLIzJ69hkwHLzw7juL1_uAp7wAC4CIAAmXWQFa2p41-fjAp-zwE"

def setup_handlers(bot_instance):
    
    # 1. Start Command Handler
    @router.message(Command("start"))
    async def start_command(message: types.Message):
        try:
            await message.answer(WELCOME_TEXT, parse_mode="HTML", disable_web_page_preview=True)
            try:
                await message.answer_voice(voice=VOICE_FILE_ID)
            except Exception as voice_err:
                print(f"❌ Voice send fail: {voice_err}")
        except Exception as e:
            print(f"❌ Critical start_command error: {e}")
            await message.answer(f"⚠️ API Error: {str(e)}")

    # 2. Verify Command Handler
    @router.message(Command("verify"))
    async def verify_command(message: types.Message):
        try:
            args = message.text.split()
            if len(args) < 2:
                await message.answer("❌ UID likh kar bhejein. Format: <b>/verify 12345</b>", parse_mode="HTML")
                return
            
            uid = args[1]
            if bot_instance.verify_uid(uid):
                await message.answer(f"✅ Verified! UID: {uid}\nAb /getapk use karein hack APK ke liye.")
            else:
                await message.answer("❌ UID nahi mili. Pehle hamare link se register karein:\nhttps://13lgame18.com/register?inviteCode=HTJ65XW&from=web")
        except Exception as e:
            print(f"❌ verify_command error: {e}")
            await message.answer(f"⚠️ Verification Error: {str(e)}")
            
    # 3. GetAPK Command Handler
    @router.message(Command("getapk"))
    async def get_apk_command(message: types.Message):
        await message.answer("⚠️ APK file currently unavailable. Please contact admin @tech_jadugar")
            
    return router