import os
import tempfile
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from gtts import gTTS

router = Router()

WELCOME_TEXT = """
🎉 **Colour Trading Pro – Family Mein Swagat Hai!**

📌 Sabse Pehle Aur Sabse Zaroori Baat:
Yeh channel **bilkul FREE** hai.

🔥 Hamara Unique System:
✅ Accurate Signals – Green/Red/Violet prediction
✅ Free Hack Mod APK – Sirf verified members ke liye
✅ Daily Lucky Winners – 10 members ko ₹100 free deposit

⚠️ **Golden Rule:**
1. Register karein: https://13lgame18.com/register?inviteCode=HTJ65XW&from=web
2. UID DM karein @tech_jadugar ko
3. Verification ke baad hack APK milega

📌 **Commands:**
/start – Welcome message
/verify <UID> – Apni UID verify karayein
/getapk – Verified hone par hack APK milega
"""

def setup_handlers(bot_instance):
    
    @router.message(Command("start"))
    async def start_command(message: types.Message):
        try:
            await message.answer(WELCOME_TEXT, parse_mode="Markdown")
            
            # Voice note generation
            try:
                tts = gTTS(text="Welcome to Colour Trading Pro family. Hamare saare tools aur signals bilkul free hain.", lang="hi", slow=False)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                    tts.save(tmp.name)
                    tmp_name = tmp.name
                
                voice = FSInputFile(tmp_name)
                await message.answer_voice(voice)
                os.unlink(tmp_name)
            except Exception as e:
                print(f"⚠️ Voice note error: {e}")
                
        except Exception as e:
            print(f"❌ start_command error: {e}")
            await message.answer("⚠️ Kuch technical issue hai. Please try again later.")
    
    @router.message(Command("verify"))
    async def verify_command(message: types.Message):
        try:
            args = message.text.split()
            if len(args) < 2:
                await message.answer("❌ UID likh kar bhejein. Format: `/verify 12345`", parse_mode="Markdown")
                return
            
            uid = args[1]
            
            # Non-blocking execution fallback handle karne ke liye simple call
            if bot_instance.verify_uid(uid):
                await message.answer(f"✅ Verified! UID: {uid}\nAb /getapk use karein hack APK ke liye.")
            else:
                await message.answer("❌ UID nahi mili. Pehle hamare link se register karein:\nhttps://13lgame18.com/register?inviteCode=HTJ65XW&from=web")
        except Exception as e:
            print(f"❌ verify_command error: {e}")
            await message.answer("⚠️ Verification complete nahi ho saki. Please contact admin @tech_jadugar.")
            
    @router.message(Command("getapk"))
    async def get_apk_command(message: types.Message):
        try:
            # Check if file exists safely
            if os.path.exists("hack.apk"):
                apk = FSInputFile("hack.apk")
                await message.answer_document(
                    apk,
                    caption="📱 Hack Mod APK\n\nInstructions:\n1. APK install karein\n2. Apni UID daalein\n3. Enjoy! 🚀"
                )
            else:
                await message.answer("⚠️ APK file currently unavailable. Please contact admin @tech_jadugar")
        except Exception as e:
            print(f"❌ get_apk_command error: {e}")
            await message.answer("⚠️ APK file send nahi ho paayi. Please try again later.")
            
    return router