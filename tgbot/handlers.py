import os
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

router = Router()

# HTML formatting safe hoti hai aur parse_mode="HTML" use karne par crash nahi karti
WELCOME_TEXT = """
<b>🎉 Colour Trading Pro - Family Mein Swagat Hai!</b>

📌 <b>Sabse Pehle Aur Sabse Zaroori Baat:</b>
Yeh channel <u>bilkul FREE</u> hai.

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

def setup_handlers(bot_instance):
    
    @router.message(Command("start"))
    async def start_command(message: types.Message):
        try:
            # Safe HTML parsing use kar rahe hain taaki special characters crash na karein
            await message.answer(WELCOME_TEXT, parse_mode="HTML", disable_web_page_preview=True)
            
            # Voice Note logic (isolated)
            try:
                if os.path.exists("voice.mp3"):
                    voice = FSInputFile("voice.mp3")
                    await message.answer_voice(voice)
            except Exception as voice_err:
                print(f"⚠️ Voice note error: {voice_err}")
                
        except Exception as e:
            print(f"❌ Critical start_command error: {e}")
            # Agar abhi bhi koi galti ho toh actual error chat mein dikhega taaki hume pata chale exact dikkat kya hai
            await message.answer(f"⚠️ API Error: {str(e)}")
    
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
            
    @router.message(Command("getapk"))
    async def get_apk_command(message: types.Message):
        try:
            if os.path.exists("hack.apk"):
                apk = FSInputFile("hack.apk")
                await message.answer_document(
                    apk,
                    caption="📱 <b>Hack Mod APK</b>\n\nInstructions:\n1. APK install karein\n2. Apni UID daalein\n3. Enjoy! 🚀",
                    parse_mode="HTML"
                )
            else:
                await message.answer("⚠️ APK file currently unavailable. Please contact admin @tech_jadugar")
        except Exception as e:
            print(f"❌ get_apk_command error: {e}")
            await message.answer(f"⚠️ APK Error: {str(e)}")
            
    return router