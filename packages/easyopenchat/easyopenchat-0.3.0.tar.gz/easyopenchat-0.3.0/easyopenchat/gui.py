
# import gradio as gr
# from .chatbot import EasyChatBot

# bot = None

# def setup(api_key, model, system_prompt):
#     global bot
#     bot = EasyChatBot(api_key, model, system_prompt)

# def chat_interface(message, history):
#     if not bot:
#         return "Please configure the bot first.", history
#     response = bot.ask(message)
#     history.append((message, response))
#     return "", history

# with gr.Blocks() as demo:
#     with gr.Row():
#         api_key = gr.Textbox(label="API Key", type="password")
#         model = gr.Textbox(label="Model", value="openai/gpt-3.5-turbo")
#         sys_prompt = gr.Textbox(label="System Prompt", value="You are a helpful AI.")
#         config_btn = gr.Button("Configure Bot")
    
#     chatbot = gr.Chatbot()
#     msg = gr.Textbox(label="Your message")
#     send_btn = gr.Button("Send")

#     config_btn.click(setup, [api_key, model, sys_prompt], None)
#     send_btn.click(chat_interface, [msg, chatbot], [msg, chatbot])

# demo.launch()




import gradio as gr
from .chatbot import EasyChatBot

def run_gui(bot):
    """
    Run a Gradio-based GUI for the chatbot.
    
    Args:
        bot (EasyChatBot): Configured chatbot instance.
    """
    def configure(api_key, model, sys_prompt, template):
        try:
            bot.__init__(api_key, model, system_prompt=sys_prompt or template)
            return "Bot configured successfully!"
        except Exception as e:
            return f"Error configuring bot: {str(e)}"

    def chat_interface(message, history):
        if not bot.client.api_key:
            return "Please configure the bot first.", history
        try:
            # Collect all chunks before updating history
            response = ""
            for chunk in bot.ask(message, stream=True):
                response += chunk
            history = history or []  # Ensure history is a list
            history.append((message, response))
            return "", history
        except Exception as e:
            history = history or []
            history.append((message, f"Error: {str(e)}"))
            return "", history

    with gr.Blocks(title="EasyOpenChat") as demo:
        gr.Markdown("# EasyOpenChat")
        with gr.Row():
            api_key = gr.Textbox(label="API Key", type="password")
            model = gr.Textbox(label="Model", value="google/gemini-2.0-flash-exp:free")
            sys_prompt = gr.Textbox(label="Custom System Prompt", placeholder="Enter custom prompt or leave empty")
            template = gr.Dropdown(label="Prompt Template", choices=["helpful_assistant", "code_assistant"])
            config_btn = gr.Button("Configure Bot")
        
        chatbot = gr.Chatbot()
        msg = gr.Textbox(label="Your Message")
        send_btn = gr.Button("Send")
        reset_btn = gr.Button("Reset History")

        config_btn.click(configure, [api_key, model, sys_prompt, template], None)
        send_btn.click(chat_interface, [msg, chatbot], [msg, chatbot])
        reset_btn.click(bot.reset_memory, None, None)

    demo.launch()  # No queue parameter needed