"""
config.py

Loads and validates required environment variables
for the SuperteamMY Intro Gatekeeper Bot.
"""

import os
from dotenv import load_dotenv


# Load .env file
load_dotenv()


def get_required_env(name: str) -> str:
    """
    Fetch an environment variable and ensure it exists.
    Raises a clear error if missing.
    """
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def get_int_env(name: str) -> int:
    """
    Fetch an environment variable and ensure it is a valid integer.
    """
    value = get_required_env(name)
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"Environment variable {name} must be an integer.")


# Required configuration
BOT_TOKEN = get_required_env("BOT_TOKEN")
GROUP_ID = get_int_env("GROUP_ID")
INTRO_THREAD_ID = get_int_env("INTRO_THREAD_ID")