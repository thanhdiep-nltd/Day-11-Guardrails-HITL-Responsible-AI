"""
Lab 11 — Configuration & API Key Setup
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Set LiteLLM to use local resources to prevent slow start/timeout fetching pricing maps
os.environ["LITELLM_LOCAL_RESOURCES"] = "True"

# Load .env file from the root directory of the workspace
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# LLM provider configuration: 'gemini' or 'fireworks'
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()

# Model identifier for Fireworks (e.g. accounts/fireworks/models/kimi-k2.6 or kimi-k2.6)
FIREWORKS_MODEL = os.getenv("FIREWORKS_MODEL", "accounts/fireworks/models/kimi-k2.6")


def setup_api_key():
    """Load API keys from environment or prompt based on the chosen provider."""
    global LLM_PROVIDER
    if LLM_PROVIDER == "gemini":
        if "GOOGLE_API_KEY" not in os.environ:
            os.environ["GOOGLE_API_KEY"] = input("Enter Google API Key: ")
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "0"
        print("Google API key loaded.")
    elif LLM_PROVIDER == "fireworks":
        if "FIREWORKS_API_KEY" not in os.environ:
            os.environ["FIREWORKS_API_KEY"] = input("Enter Fireworks API Key: ")
        print("Fireworks API key loaded.")


# Allowed banking topics (used by topic_filter)
ALLOWED_TOPICS = [
    "banking", "account", "transaction", "transfer",
    "loan", "interest", "savings", "credit",
    "deposit", "withdrawal", "balance", "payment",
    "tai khoan", "giao dich", "tiet kiem", "lai suat",
    "chuyen tien", "the tin dung", "so du", "vay",
    "ngan hang", "atm",
]

# Blocked topics (immediate reject)
BLOCKED_TOPICS = [
    "hack", "exploit", "weapon", "drug", "illegal",
    "violence", "gambling", "bomb", "kill", "steal",
]
