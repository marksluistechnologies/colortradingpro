import os
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

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

def setup_handlers(bot_instance):
    
    @router.message(Command("start"))
    async def start_command(message: types.Message):
        try:
            # 1. Welcome Text bhejein
            await message.answer(WELCOME_TEXT, parse_mode="HTML", disable_web_page_preview=True)
            
            # 2. Dynamic Root Path nikalyein
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # Aapke root files ki scanning karein (Case-insensitive check)
            all_files = os.listdir(BASE_DIR)
            voice_file_name = None
            
            for file in all_files:
                if file.lower() == "voice.mp3":
                    voice_file_name = file
                    break
            
            # Voice Note logic
            if voice_file_name:
                voice_path = os.path.join(BASE_DIR, voice_file_name)
                try:
                    voice = FSInputFile(voice_path)
                    await message.answer_voice(voice)
                except Exception as voice_err:
                    print(f"❌ Voice send fail: {voice_err}")
                    await message.answer(f"⚠️ Voice Sending Error: {str(voice_err)}")
            else:
                # Agar file nahi mili, toh debug list dikhayein taaki pata chale file kahan hai
                files_found = ", ".join([f for f in all_files if not f.startswith('.')][:10])
                await message.answer(f"🔍 <b>Debug Info:</b> <code>voice.mp3</code> root par nahi mili.\nRoot folder mein ye files hain: <code>{files_found}</code>", parse_mode="HTML")
                
        except Exception as e:
            print(f"❌ Critical start_command error: {e}")
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
        # Kyunki aapne bataya hack.apk abhi nahi hai, directly message de dete hain
        await message.answer("⚠️ APK file currently unavailable. Please contact admin @tech_jadugar")
            
    return router