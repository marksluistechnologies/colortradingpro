from fastapi import FastAPI, Request
from tgbot.main import tgbot

app = FastAPI()

@app.post("/api/bot")
async def webhook(request: Request):
    update_data = await request.json()
    await tgbot.update_bot(update_data)
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Bot is running!"}

# Vercel serverless function ke liye handler
handler = app