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
/getapk [UID] - Verified hone par hack APK milega
"""

# Aapki final working Catbox URL Link (Voice Note)
VOICE_URL = "https://files.catbox.moe/xs2289.mp3"

# Aapki final working Catbox URL Link (APK File)
APK_URL = "https://files.catbox.moe/uxlk3s.apk" 
APK_CAPTION = "🔥 <b>Colour Trading Pro Hack APK (v3.2)</b>\n\n✅ 100% Anti-Ban\n✅ Accurate Predictions\n\nInstall karein aur enjoy karein!"

def setup_handlers(bot_instance):
    
    # 1. Start Command Handler
    @router.message(Command("start"))
    async def start_command(message: types.Message):
        try:
            # Welcome Text bhejein (Safe HTML)
            await message.answer(WELCOME_TEXT, parse_mode="HTML", disable_web_page_preview=True)
            
            # Voice Note via URL
            try:
                await message.answer_voice(voice=VOICE_URL)
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
                await message.answer(f"✅ Verified! UID: {uid}\nAb /getapk {uid} use karein hack APK ke liye.")
            else:
                await message.answer("❌ UID nahi mili. Pehle hamare link se register karein:\n\nhttps://13lgame18.com/register?inviteCode=HTJ65XW&from=web\n\n Phir apni UID DM karein @tech_jadugar ko.", disable_web_page_preview=True)
        except Exception as e:
            print(f"❌ verify_command error: {e}")
            await message.answer(f"⚠️ Verification Error: {str(e)}")
            
    # 3. GetAPK Command Handler (With UID Check Logic & File Send)
    @router.message(Command("getapk"))
    async def get_apk_command(message: types.Message):
        try:
            args = message.text.split()
            
            # Agar user ne UID nahi bheji
            if len(args) < 2:
                await message.answer("❌ APK download karne ke liye apni UID sath mein bhejein.\nFormat: <b>/getapk 12345</b>", parse_mode="HTML")
                return
                
            uid = args[1]
            
            # Google Sheet/Airtable mein check karein ki UID verified hai ya nahi
            if bot_instance.verify_uid(uid):
                # Agar UID mil gayi (Verified User) -> Send APK File
                await message.answer("🔄 File bheji jaa rahi hai, kripya wait karein...")
                
                try:
                    await message.answer_document(
                        document=APK_URL,
                        caption=APK_CAPTION,
                        parse_mode="HTML"
                    )

                except Exception as doc_err:
                    print(f"❌ File send fail: {doc_err}")
                    await message.answer("⚠️ System overloaded. APK file generate nahi ho paayi. Admin se contact karein: @tech_jadugar")
                    
            else:
                # Agar UID nahi mili (Unverified User)
                await message.answer(
                    "❌ Aapki UID verified nahi hai! Pehle hamare link se register karke UID @tech_jadugar ko verify karwaye, tab jaa kar aap hack download kar paenge.\n\n"
                    "🔗 Register Link: https://13lgame18.com/register?inviteCode=HTJ65XW&from=web", 
                    parse_mode="HTML", 
                    disable_web_page_preview=True
                )
        except Exception as e:
            print(f"❌ get_apk_command error: {e}")
            await message.answer(f"⚠️ Error: {str(e)}")
            
    return router