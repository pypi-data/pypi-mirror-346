
# import requests, time

# class OpenRouterClient:
#     def __init__(self, api_key, model):
#         self.api_key = api_key
#         self.model = model

#     def chat(self, messages, stream=False, retries=3):
#         headers = {
#             "Authorization": f"Bearer {self.api_key}",
#             "HTTP-Referer": "http://localhost",
#             "X-Title": "easyopenchat"
#         }
#         payload = {
#             "model": self.model,
#             "messages": messages,
#             "stream": stream
#         }
#         for attempt in range(retries):
#             try:
#                 r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, stream=stream)
#                 r.raise_for_status()
#                 return r if stream else r.json()
#             except requests.RequestException:
#                 time.sleep(2)
#         raise RuntimeError("Failed after retries")


import requests
import time
import json

class OpenRouterClient:
    def __init__(self, api_key, model):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    def chat(self, messages, stream=False, retries=3, timeout=30):
        """
        Send a chat request to OpenRouter.
        
        Args:
            messages (list): List of message dictionaries.
            stream (bool): Enable streaming response.
            retries (int): Number of retry attempts.
            timeout (int): Request timeout in seconds.
        
        Returns:
            dict or generator: JSON response or streaming content chunks.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost",
            "X-Title": "easyopenchat",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream
        }

        for attempt in range(retries):
            try:
                if stream:
                    response = requests.post(self.base_url, headers=headers, json=payload, stream=True, timeout=timeout)
                    response.raise_for_status()
                    return self._stream_chunks(response)
                else:
                    r = requests.post(self.base_url, headers=headers, json=payload, timeout=timeout)
                    r.raise_for_status()
                    return r.json()
            except requests.RequestException as e:
                if attempt == retries - 1:
                    raise RuntimeError(f"Failed after {retries} retries: {str(e)}")
                time.sleep(2 ** attempt)  # Exponential backoff
        return None

    def _stream_chunks(self, response):
        """
        Parse SSE stream and yield content chunks.
        
        Args:
            response: Streaming response object.
        
        Yields:
            str: Content from the delta field.
        """
        for line in response.iter_lines(decode_unicode=True):
            if line:
                # Skip non-data lines (e.g., OPENROUTER PROCESSING)
                if not line.startswith("data:"):
                    continue
                # Handle [DONE] or empty data
                if line == "data: [DONE]":
                    return
                try:
                    # Parse JSON data
                    data = json.loads(line[5:].strip())  # Remove "data:" prefix
                    # Extract content from choices[0].delta.content
                    if (
                        "choices" in data
                        and len(data["choices"]) > 0
                        and "delta" in data["choices"][0]
                        and "content" in data["choices"][0]["delta"]
                    ):
                        content = data["choices"][0]["delta"]["content"]
                        if content:  # Only yield non-empty content
                            yield content
                except (json.JSONDecodeError, KeyError):
                    continue  # Skip malformed or irrelevant chunks