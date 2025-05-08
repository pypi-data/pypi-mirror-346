
import gradio as gr
from .chatbot import EasyChatBot

bot = None

def setup(api_key, model, system_prompt):
    global bot
    bot = EasyChatBot(api_key, model, system_prompt)

def chat_interface(message, history):
    if not bot:
        return "Please configure the bot first.", history
    response = bot.ask(message)
    history.append((message, response))
    return "", history

with gr.Blocks() as demo:
    with gr.Row():
        api_key = gr.Textbox(label="API Key", type="password")
        model = gr.Textbox(label="Model", value="openai/gpt-3.5-turbo")
        sys_prompt = gr.Textbox(label="System Prompt", value="You are a helpful AI.")
        config_btn = gr.Button("Configure Bot")
    
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Your message")
    send_btn = gr.Button("Send")

    config_btn.click(setup, [api_key, model, sys_prompt], None)
    send_btn.click(chat_interface, [msg, chatbot], [msg, chatbot])

demo.launch()
