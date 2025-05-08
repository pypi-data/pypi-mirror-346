
from fastapi import FastAPI, Request
from pydantic import BaseModel
from .chatbot import EasyChatBot

app = FastAPI()
bot = None

class ChatRequest(BaseModel):
    message: str

@app.post("/configure")
def configure(api_key: str, model: str = "openai/gpt-3.5-turbo", prompt: str = "You are a helpful AI."):
    global bot
    bot = EasyChatBot(api_key, model, system_prompt=prompt)
    return {"status": "configured"}

@app.post("/chat")
def chat(req: ChatRequest):
    if not bot:
        return {"error": "Bot not configured"}
    reply = bot.ask(req.message)
    return {"reply": reply}
