
# from .client import OpenRouterClient
# from .memory import Memory
# from .prompts import PromptTemplate
# from .plugins.plugin_loader import load_plugins


# class EasyChatBot:
#     def __init__(self, api_key, model, system_prompt=""):
#         self.client = OpenRouterClient(api_key, model)
#         self.memory = Memory()
#         self.plugins = load_plugins()
#         self.system_prompt = system_prompt
#         if system_prompt:
#             self.memory.add("system", system_prompt)

#     def ask(self, user_input):
#         if user_input.startswith("!"):
#             command = user_input[1:]
#             if command in self.plugins:
#                 return self.plugins[command]()
#         self.memory.add("user", user_input)
#         response = self.client.chat(self.memory.history)
#         reply = response['choices'][0]['message']['content']
#         self.memory.add("assistant", reply)
#         return reply





from .client import OpenRouterClient
from .memory import Memory
from .vector_memory import VectorMemory
from .prompts import PromptTemplate
from .plugins.plugin_loader import load_plugins
import os
import uuid

class EasyChatBot:
    def __init__(self, api_key, model="google/gemini-2.0-flash-exp:free", system_prompt="", use_vector_memory=False, max_history=100):
        """
        Initialize the chatbot with API key, model, and optional configurations.
        
        Args:
            api_key (str): OpenRouter API key.
            model (str): Model name (default: google/gemini-2.0-flash-exp:free).
            system_prompt (str): Custom system prompt or template name.
            use_vector_memory (bool): Enable vector memory for semantic search.
            max_history (int): Maximum number of messages to store in memory.
        """
        self.client = OpenRouterClient(api_key, model)
        self.memory = Memory(max_history=max_history)
        self.vector_memory = VectorMemory() if use_vector_memory else None
        self.plugins = load_plugins()
        self.max_history = max_history

        # Load system prompt (either custom or from template)
        if system_prompt and os.path.exists(os.path.join("easyopenchat/templates", f"{system_prompt}.j2")):
            with open(os.path.join("easyopenchat/templates", f"{system_prompt}.j2"), "r") as f:
                self.prompt_template = PromptTemplate(f.read())
            self.system_prompt = self.prompt_template.render()
        else:
            self.system_prompt = system_prompt or "You are a helpful AI assistant."
        
        self.memory.add("system", self.system_prompt)

    def ask(self, user_input, stream=False):
        """
        Process user input and return the chatbot's response.
        
        Args:
            user_input (str): User's message or command.
            stream (bool): Enable streaming response.
        
        Returns:
            str or generator: Response text or streamed chunks.
        """
        # Handle plugin commands
        if user_input.startswith("!"):
            command = user_input[1:].split()[0]
            args = user_input[len(command) + 1:].strip()
            if command in self.plugins:
                return self.plugins[command](args)
            return f"Unknown command: {command}"

        # Add user input to memory
        self.memory.add("user", user_input)
        
        # Optional: Add to vector memory
        if self.vector_memory:
            # Placeholder for embedding generation (requires additional dependency)
            embedding = str(uuid.uuid4())  # Dummy embedding
            self.vector_memory.add(embedding, {"role": "user", "content": user_input})

        # Get response from LLM
        if stream:
            return self._stream_response()
        else:
            response = self.client.chat(self.memory.history)
            reply = response['choices'][0]['message']['content']
            self.memory.add("assistant", reply)
            return reply

    def _stream_response(self):
        """
        Stream response chunks from the LLM.
        
        Yields:
            str: Response chunk.
        """
        full_reply = ""
        for chunk in self.client.chat(self.memory.history, stream=True):
            full_reply += chunk
            yield chunk
        self.memory.add("assistant", full_reply)

    def reset_memory(self):
        """Reset conversation history."""
        self.memory.reset()
        self.memory.add("system", self.system_prompt)

    def run_cli(self):
        """Run the chatbot in CLI mode."""
        from rich.console import Console
        from rich.prompt import Prompt
        console = Console()
        console.print("[bold green]EasyOpenChat CLI[/bold green]")
        console.print("Type 'exit' to quit, '!reset' to clear memory, or any message to chat.")

        while True:
            user_input = Prompt.ask("[bold blue]You[/bold blue]")
            if user_input.lower() == "exit":
                break
            if user_input.lower() == "!reset":
                self.reset_memory()
                console.print("[yellow]Memory reset.[/yellow]")
                continue

            if user_input.startswith("!"):
                response = self.ask(user_input)
                console.print(f"[bold magenta]Bot[/bold magenta]: {response}")
            else:
                console.print("[bold magenta]Bot[/bold magenta]: ", end="")
                for chunk in self.ask(user_input, stream=True):
                    console.print(chunk, end="", soft_wrap=True)
                console.print()

    def run_gui(self):
        """Run the chatbot in Gradio GUI mode."""
        from .gui import run_gui
        run_gui(self)