import json
from fastapi import FastAPI, Request, Response
from tgbot.main import tgbot

app = FastAPI()

@app.post("/api/bot")
async def webhook(request: Request):
    try:
        # Update data ko receive karo
        update_data = await request.json()
        print(f"📩 Received update: {update_data.get('update_id', 'unknown')}")
        
        # Update ko process karein
        await tgbot.update_bot(update_data)
        print("✅ Update processed successfully")
        return {"status": "ok"}
        
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        # Telegram ko fail response mat bhejein warna wo baar-baar retry karega
        return Response(status_code=200, content=json.dumps({"status": "error", "message": str(e)}))

@app.get("/")
async def root():
    return {"message": "Bot is running!"}

@app.get("/api/bot")
async def get_method_not_allowed():
    return {"error": "Method not allowed. Use POST for webhook."}