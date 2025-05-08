# EasyOpenChat

**An easy, beginner-friendly Python SDK for building chatbots powered by OpenRouter.**
Create, customize, and deploy your own chatbot using this simple package with minimal setup.

---

## 🚀 Features

* **Customizable prompts**: Use your own templates or adjust existing ones.
* **Easy chatbot creation**: Just a few lines of code to create powerful chatbots.
* **FastAPI integration**: Expose a REST API for your chatbot.
* **Gradio UI**: Quickly deploy a chatbot GUI for testing and interaction.
* **Plugin support**: Extend functionality with plugins.
* **Memory support**: Use memory features for long conversations.

---

## 📦 Installation

Install `easyopenchat` directly from **PyPI**:

```bash
pip install easyopenchat
```

---

## 🔑 Quick Start

### 1. **Create a Simple Chatbot**

```python
from easyopenchat import EasyChatBot

# Initialize the bot with your OpenRouter API key
bot = EasyChatBot(api_key="your-openrouter-key", model="gpt-3.5-turbo")

# Send a message to the bot and get a response
response = bot.ask("Hello, chatbot!")
print(response)
```

### 2. **Customizing the Chatbot with Prompts**

You can define your own prompt templates for different scenarios. Just use the `add_prompt` method:

```python
# Define a custom prompt template
bot.add_prompt("greeting", "Hello, I am your assistant. How can I help you today?")
response = bot.ask("greeting")
print(response)
```

---

## 🛠️ Advanced Features

### 1. **Using Plugins**

You can extend the functionality of your chatbot by adding plugins. For example, load a plugin:

```python
from easyopenchat.plugins import load_plugins

# Load plugins from the specified folder
plugins = load_plugins(plugin_folder="plugins/")
```

Make sure you define and organize your plugins in the `plugins/` directory.

---

### 2. **Gradio GUI (Optional)**

Launch a simple GUI to interact with your chatbot using Gradio:

```python
import gradio as gr

def chatbot_ui(user_input):
    response = bot.ask(user_input)
    return response

# Create and launch the Gradio interface
interface = gr.Interface(fn=chatbot_ui, inputs="text", outputs="text")
interface.launch()
```

---

### 3. **FastAPI Web API (Optional)**

Host your chatbot as a REST API using FastAPI:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define request body
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    response = bot.ask(request.message)
    return {"response": response}

# Run the FastAPI app (use `uvicorn` to run it in the terminal)
```

---

## ⚙️ Configuration

You can configure your chatbot by editing the `EasyChatBot` class constructor.

```python
bot = EasyChatBot(
    api_key="your-openrouter-key",  # Your OpenRouter API key
    model="gpt-3.5-turbo",         # Choose your model
    memory=True,                    # Enable memory (optional)
    max_tokens=2000,                # Limit token usage
)
```

---

## 🧩 Plugin Architecture

To add your own plugins, place them in the `plugins/` directory. A plugin is just a Python file with a function to execute.

### Example plugin (`plugins/my_plugin.py`):

```python
def run_plugin():
    print("Hello from the plugin!")
```

---

## 💾 Memory Feature

You can enable the memory feature so that the chatbot can "remember" past conversations:

```python
bot.enable_memory()
bot.ask("Hello")
bot.ask("What did I say earlier?")
```

---

## 📑 Documentation

For more detailed information, check the full documentation here:

* **Installation Guide**
* **API Reference**
* **Advanced Tutorials**

---

## 🛠️ Development

### Local Development

To make changes locally and test them, install the package in "editable" mode:

```bash
pip install -e .
```

This allows you to make changes without reinstalling every time.

### Testing

We use **pytest** for testing. To run the tests, simply use:

```bash
pytest
```

---

## 🧑‍🤝‍🧑 Contributing

We welcome contributions! If you find any bugs or want to suggest new features, feel free to open an issue or submit a pull request.

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

Created by **Sriram G**
You can reach me at: [sriramkrish379@gmail.com](mailto:sriramkrish379@gmail.com)

---

### 📍 Notes

* The library is powered by **OpenRouter API** for chatbot generation.
* Make sure to replace the `"your-openrouter-key"` with your actual OpenRouter API key.
* Use Gradio to quickly launch a UI and FastAPI to deploy your chatbot as a service.
* **Plugin support** is flexible, and you can expand it for custom integrations.

---
