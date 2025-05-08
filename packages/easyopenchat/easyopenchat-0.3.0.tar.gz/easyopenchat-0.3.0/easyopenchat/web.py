
# from fastapi import FastAPI, Request
# from pydantic import BaseModel
# from .chatbot import EasyChatBot

# app = FastAPI()
# bot = None

# class ChatRequest(BaseModel):
#     message: str

# @app.post("/configure")
# def configure(api_key: str, model: str = "openai/gpt-3.5-turbo", prompt: str = "You are a helpful AI."):
#     global bot
#     bot = EasyChatBot(api_key, model, system_prompt=prompt)
#     return {"status": "configured"}

# @app.post("/chat")
# def chat(req: ChatRequest):
#     if not bot:
#         return {"error": "Bot not configured"}
#     reply = bot.ask(req.message)
#     return {"reply": reply}






from fastapi import FastAPI, Request
from pydantic import BaseModel
from .chatbot import EasyChatBot
from starlette.responses import StreamingResponse
import json

app = FastAPI(title="EasyOpenChat API")
bot = None

class ConfigRequest(BaseModel):
    api_key: str
    model: str = "google/gemini-2.0-flash-exp:free"
    prompt: str = ""
    template: str = ""

class ChatRequest(BaseModel):
    message: str
    stream: bool = False

@app.post("/configure")
async def configure(req: ConfigRequest):
    global bot
    prompt = req.prompt or req.template
    bot = EasyChatBot(req.api_key, req.model, system_prompt=prompt)
    return {"status": "configured"}

@app.post("/chat")
async def chat(req: ChatRequest):
    if not bot:
        return {"error": "Bot not configured"}
    if req.stream:
        async def stream_response():
            for chunk in bot.ask(req.message, stream=True):
                yield json.dumps({"chunk": chunk}) + "\n"
        return StreamingResponse(stream_response(), media_type="application/x-ndjson")
    reply = bot.ask(req.message)
    return {"reply": reply}

@app.post("/reset")
async def reset():
    if not bot:
        return {"error": "Bot not configured"}
    bot.reset_memory()
    return {"status": "history reset"}