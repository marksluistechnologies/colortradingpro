from fastapi import FastAPI, Request, BackgroundTasks
from tgbot.main import tgbot

app = FastAPI()

def process_update(update_data: dict):
    """Background task mein update process karein"""
    import asyncio
    try:
        # Agar event loop already running hai toh use karo, nahi toh naya banayein
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Update ko process karein
        loop.run_until_complete(tgbot.update_bot(update_data))
    except Exception as e:
        print(f"❌ Background task error: {e}")

@app.post("/api/bot")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    update_data = await request.json()
    # Background task mein process karein taaki response jaldi bhej sakein
    background_tasks.add_task(process_update, update_data)
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Bot is running!"}

@app.get("/api/bot")
async def get_method_not_allowed():
    return {"error": "Method not allowed. Use POST for webhook."}

# Vercel serverless function ke liye handler
handler = app