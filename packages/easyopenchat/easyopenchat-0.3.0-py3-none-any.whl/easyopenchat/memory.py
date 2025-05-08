
# import json, os

# class Memory:
#     def __init__(self, memory_file="chat_history.json"):
#         self.memory_file = memory_file
#         self.load()

#     def load(self):
#         if os.path.exists(self.memory_file):
#             with open(self.memory_file, "r") as f:
#                 self.history = json.load(f)
#         else:
#             self.history = []

#     def save(self):
#         with open(self.memory_file, "w") as f:
#             json.dump(self.history, f, indent=2)

#     def add(self, role, content):
#         self.history.append({"role": role, "content": content})
#         self.save()

#     def reset(self):
#         self.history = []
#         self.save()




import json
import os
from datetime import datetime

class Memory:
    def __init__(self, memory_file="chat_history.json", max_history=100):
        """
        Initialize memory with persistent storage.
        
        Args:
            memory_file (str): File to store chat history.
            max_history (int): Maximum number of messages to store.
        """
        self.memory_file = memory_file
        self.max_history = max_history
        self.history = []
        self.load()

    def load(self):
        """Load chat history from file."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r") as f:
                    self.history = json.load(f)
            except json.JSONDecodeError:
                self.history = []
        self._prune_history()

    def save(self):
        """Save chat history to file."""
        self._prune_history()
        try:
            with open(self.memory_file, "w") as f:
                json.dump(self.history, f, indent=2)
        except Exception:
            pass

    def add(self, role, content):
        """Add a message to history."""
        self.history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.save()

    def _prune_history(self):
        """Prune history to maintain max_history limit."""
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
            self.save()

    def reset(self):
        """Reset chat history."""
        self.history = []
        self.save()