from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from gtts import gTTS
import os
import tempfile

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
    """Handlers ko bot instance ke saath setup karein"""
    
    @router.message(Command("start"))
    async def start_command(message: types.Message):
        try:
            await message.answer(WELCOME_TEXT, parse_mode="Markdown")
            
            # Voice note - try-except ke saath
            try:
                tts = gTTS(text=WELCOME_TEXT[:500], lang="hi", slow=False)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                    tts.save(tmp.name)
                    voice = FSInputFile(tmp.name)
                    await message.answer_voice(voice)
                    os.unlink(tmp.name)
            except Exception as e:
                print(f"⚠️ Voice note error: {e}")
                # Voice note fail ho toh sirf text bhejo
                await message.answer("📢 Voice note generate nahi ho paaya, lekin aap commands use kar sakte hain.")
                
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
            if bot_instance.verify_uid(uid):
                await message.answer(f"✅ Verified! UID: {uid}\nAb /getapk use karein hack APK ke liye.")
            else:
                await message.answer("❌ UID nahi mili. Pehle hamare link se register karein:\nhttps://13lgame18.com/register?inviteCode=HTJ65XW&from=web")
        except Exception as e:
            print(f"❌ verify_command error: {e}")
            await message.answer("⚠️ Kuch technical issue hai. Please try again later.")
    
    @router.message(Command("getapk"))
    async def get_apk_command(message: types.Message):
        try:
            apk = FSInputFile("hack.apk")
            await message.answer_document(
                apk,
                caption="📱 Hack Mod APK\n\nInstructions:\n1. APK install karein\n2. Apni UID daalein\n3. Enjoy! 🚀"
            )
        except FileNotFoundError:
            await message.answer("⚠️ APK file currently unavailable. Please contact admin @tech_jadugar")
        except Exception as e:
            print(f"❌ get_apk_command error: {e}")
            await message.answer("⚠️ APK file send nahi ho paayi. Please try again later.")
    
    return router