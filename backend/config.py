import os
from dotenv import load_dotenv

load_dotenv()

# =====================
# API Configuration
# =====================
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
API_REVIEW_ENDPOINT = f"{API_BASE_URL}/review"
API_REQUEST_TIMEOUT = int(os.getenv("API_REQUEST_TIMEOUT", "600"))

# =====================
# LLM Providers Configuration
# =====================
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openrouter").lower()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

LLM_TIMEOUT_SEC = int(os.getenv("LLM_TIMEOUT_SEC", "60"))

# =====================
# Routing Configuration
# =====================
ROUTING_TOP_K = int(os.getenv("ROUTING_TOP_K", "2"))
CODE_SNIPPET_MAX_LENGTH = int(os.getenv("CODE_SNIPPET_MAX_LENGTH", "700"))
SECURITY_REPORT_MAX_LENGTH = int(os.getenv("SECURITY_REPORT_MAX_LENGTH", "300"))
QUALITY_REPORT_MAX_LENGTH = int(os.getenv("QUALITY_REPORT_MAX_LENGTH", "400"))

# =====================
# Repository Configuration
# =====================
CLONE_TIMEOUT_SEC = int(os.getenv("CLONE_TIMEOUT_SEC", "300"))
TEMP_REPO_DIR = os.getenv("TEMP_REPO_DIR", "temp_repos")

# =====================
# Deployment
# =====================
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = ENVIRONMENT == "development"
