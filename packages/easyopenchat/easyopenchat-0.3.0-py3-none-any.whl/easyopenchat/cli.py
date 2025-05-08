from .chatbot import EasyChatBot

def run_cli(api_key, model="google/gemini-2.0-flash-exp:free", system_prompt=""):
    """
    Run the chatbot in CLI mode.
    
    Args:
        api_key (str): OpenRouter API key.
        model (str): Model name.
        system_prompt (str): System prompt or template name.
    """
    bot = EasyChatBot(api_key, model, system_prompt)
    bot.run_cli()