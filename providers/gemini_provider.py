import os
import requests
from providers.base_provider import BaseProvider

class GeminiProvider(BaseProvider):
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.timeout = 60

    def generate(self, prompt, timeout_override=None):
        if not self.api_key:
            return "Gemini API Key is missing. Review unavailable."

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }

        timeout_sec = timeout_override if timeout_override else self.timeout

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=timeout_sec)
            response.raise_for_status()
            data = response.json()
            if "candidates" in data and len(data["candidates"]) > 0:
                candidate = data["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    return candidate["content"]["parts"][0]["text"]
            return "Review unavailable"
        except Exception as e:
            print(f"Gemini error: {e}")
            return "Review unavailable"
