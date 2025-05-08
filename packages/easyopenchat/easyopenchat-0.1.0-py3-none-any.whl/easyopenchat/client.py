
import requests, time

class OpenRouterClient:
    def __init__(self, api_key, model):
        self.api_key = api_key
        self.model = model

    def chat(self, messages, stream=False, retries=3):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost",
            "X-Title": "easyopenchat"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream
        }
        for attempt in range(retries):
            try:
                r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, stream=stream)
                r.raise_for_status()
                return r if stream else r.json()
            except requests.RequestException:
                time.sleep(2)
        raise RuntimeError("Failed after retries")
