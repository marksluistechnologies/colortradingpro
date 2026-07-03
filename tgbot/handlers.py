import os
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

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
            # 1. Pehle text message har haal mein bhejein
            await message.answer(WELCOME_TEXT, parse_mode="Markdown")
            
            # 2. Voice note ko alag try-except mein rakhein taaki iski wajah se bot crash na ho
            try:
                # OPTION A: Agar aapke paas voice.mp3 file repository mein hai:
                if os.path.exists("voice.mp3"):
                    voice = FSInputFile("voice.mp3")
                    await message.answer_voice(voice)
                else:
                    # OPTION B: Best Tarika (Telegram File ID)
                    # Apne bot ko manually ek voice note bhejein, uski file_id nikaal kar yahan daal dein:
                    # await message.answer_voice(voice="AAQDAgADgQcAAl...aapki_file_id_yahan")
                    pass
            except Exception as voice_err:
                print(f"⚠️ Voice note sending skipped/failed: {voice_err}")
                
        except Exception as e:
            print(f"❌ Critical start_command error: {e}")
            # Ab yeh error tabhi aayega jab Telegram API hi down hogi
            await message.answer("⚠️ System update ho raha hai. Please try again after 1 minute.")
    
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
            await message.answer("⚠️ Verification service temporarily unavailable.")
            
    @router.message(Command("getapk"))
    async def get_apk_command(message: types.Message):
        try:
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