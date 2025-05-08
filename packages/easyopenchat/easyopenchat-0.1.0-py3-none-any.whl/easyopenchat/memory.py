
import json, os

class Memory:
    def __init__(self, memory_file="chat_history.json"):
        self.memory_file = memory_file
        self.load()

    def load(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                self.history = json.load(f)
        else:
            self.history = []

    def save(self):
        with open(self.memory_file, "w") as f:
            json.dump(self.history, f, indent=2)

    def add(self, role, content):
        self.history.append({"role": role, "content": content})
        self.save()

    def reset(self):
        self.history = []
        self.save()
