
from .client import OpenRouterClient
from .memory import Memory
from .prompts import PromptTemplate
from .plugins import load_plugins

class EasyChatBot:
    def __init__(self, api_key, model, system_prompt=""):
        self.client = OpenRouterClient(api_key, model)
        self.memory = Memory()
        self.plugins = load_plugins()
        self.system_prompt = system_prompt
        if system_prompt:
            self.memory.add("system", system_prompt)

    def ask(self, user_input):
        if user_input.startswith("!"):
            command = user_input[1:]
            if command in self.plugins:
                return self.plugins[command]()
        self.memory.add("user", user_input)
        response = self.client.chat(self.memory.history)
        reply = response['choices'][0]['message']['content']
        self.memory.add("assistant", reply)
        return reply
