"""
main.py

Entry point for the SuperteamMY Intro Gatekeeper Bot.

Initializes:
- Database
- Handlers
- Error handling
- Bot polling

Built for python-telegram-bot v20.7
"""

import logging
from telegram import Update
from telegram.ext import (
    Application,
    ChatMemberHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import BOT_TOKEN
from onboarding import handle_new_member
from intro_handler import handle_intro
from admin import get_admin_handlers
from database import initialize_database


# ---------------------------
# Logging Configuration
# ---------------------------

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# ---------------------------
# Global Error Handler
# ---------------------------

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Catches all unexpected errors so the bot doesn't crash silently.
    """
    logger.error("Exception while handling update:", exc_info=context.error)


# ---------------------------
# Main Entry
# ---------------------------

def main():
    """
    Bootstraps the Telegram bot.
    """

    # Ensure database is initialized
    initialize_database()

    # Build application
    app = Application.builder().token(BOT_TOKEN).build()

    # Handle new member joins
    app.add_handler(
        ChatMemberHandler(
            handle_new_member,
            ChatMemberHandler.CHAT_MEMBER
        )
    )

    # Handle intro messages (non-command text)
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_intro
        )
    )

    # Register admin command handlers
    for handler in get_admin_handlers():
        app.add_handler(handler)

    # Register global error handler
    app.add_error_handler(error_handler)

    logger.info("SuperteamMY Intro Gatekeeper Bot started successfully.")

    # Start polling
    app.run_polling()


if __name__ == "__main__":
    main()