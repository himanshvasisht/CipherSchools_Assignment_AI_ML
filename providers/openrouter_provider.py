import os
import requests

from dotenv import load_dotenv
from providers.base_provider import BaseProvider


load_dotenv()


class OpenRouterProvider(BaseProvider):

    def __init__(self):

        self.api_key = os.getenv(
            "OPENROUTER_API_KEY"
        )

        self.url = (
            "https://openrouter.ai/api/v1/chat/completions"
        )

        self.model = (
            "google/gemini-2.5-flash:free"
        )
        
        # LLM timeout max 60 sec
        self.timeout = 60

    def generate(
        self,
        prompt,
        timeout_override=None
    ):
        """
        Generate LLM response with timeout protection.
        
        Args:
            prompt: input prompt
            timeout_override: optional custom timeout (default 60 sec)
        
        Returns:
            str: LLM response or fallback message if error
        """

        headers = {
            "Authorization":
                f"Bearer {self.api_key}",
            "Content-Type":
                "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        timeout_sec = (
            timeout_override 
            if timeout_override 
            else self.timeout
        )

        try:

            response = requests.post(
                self.url,
                headers=headers,
                json=payload,
                timeout=timeout_sec
            )

            response.raise_for_status()

            data = response.json()

            if (
                "choices" in data
                and len(data["choices"]) > 0
            ):
                return data[
                    "choices"
                ][0][
                    "message"
                ][
                    "content"
                ]

            # Fallback: no completion in response
            return "Review unavailable"

        except requests.Timeout:
            
            print("OpenRouter request timed out (60s limit)")
            return "Review unavailable"

        except requests.ConnectionError as e:
            
            print(f"OpenRouter connection error: {e}")
            return "Review unavailable"

        except requests.RequestException as e:
            
            print(f"OpenRouter request failed: {e}")
            return "Review unavailable"

        except ValueError as e:
            
            print(f"OpenRouter invalid JSON: {e}")
            return "Review unavailable"
        
        except Exception as e:
            
            print(f"Unexpected LLM error: {e}")
            return "Review unavailable"
        