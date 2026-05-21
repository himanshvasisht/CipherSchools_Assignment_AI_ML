import os
from dotenv import load_dotenv

from providers.openrouter_provider import OpenRouterProvider
from providers.openai_provider import OpenAIProvider
from providers.gemini_provider import GeminiProvider
from providers.ollama_provider import OllamaProvider

load_dotenv()

def get_llm_client(provider_name=None):
    """
    Returns LLM client instance.
    Uses provider_name parameter if passed, otherwise falls back to LLM_PROVIDER env var.
    """
    if not provider_name:
        provider_name = os.getenv("LLM_PROVIDER", "openrouter")
        
    provider_name = provider_name.lower().strip()

    if provider_name == "openai":
        return OpenAIProvider()
    elif provider_name == "gemini":
        return GeminiProvider()
    elif provider_name == "ollama":
        return OllamaProvider()
    
    # Default fallback
    return OpenRouterProvider()
