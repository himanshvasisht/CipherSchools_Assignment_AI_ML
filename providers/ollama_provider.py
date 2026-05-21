import os
import requests
from providers.base_provider import BaseProvider

class OllamaProvider(BaseProvider):
    def __init__(self):
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:1.5b")
        self.timeout = 60

    def generate(self, prompt, timeout_override=None):
        url = f"{self.host}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        timeout_sec = timeout_override if timeout_override else self.timeout

        try:
            response = requests.post(url, json=payload, timeout=timeout_sec)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "Review unavailable")
        except Exception as e:
            print(f"Ollama error: {e}")
            return "Review unavailable"
