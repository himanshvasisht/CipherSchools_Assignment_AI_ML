import os
import requests
from providers.base_provider import BaseProvider

class OpenAIProvider(BaseProvider):
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.url = "https://api.openai.com/v1/chat/completions"
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.timeout = 60

    def generate(self, prompt, timeout_override=None):
        if not self.api_key:
            return "OpenAI API Key is missing. Review unavailable."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2
        }

        timeout_sec = timeout_override if timeout_override else self.timeout

        try:
            response = requests.post(self.url, headers=headers, json=payload, timeout=timeout_sec)
            response.raise_for_status()
            data = response.json()
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
            return "Review unavailable"
        except Exception as e:
            print(f"OpenAI error: {e}")
            return "Review unavailable"
