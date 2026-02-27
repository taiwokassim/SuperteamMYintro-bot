"""
admin.py

Contains administrative command handlers for the SuperteamMY Intro Bot.

Currently implemented:
- /reset <user_id> → Resets a user's intro status (admin only)

This file is designed for python-telegram-bot v20+
"""

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from bot.database import set_user_status, delete_user
from bot.config import GROUP_ID


async def reset_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Admin-only command to reset a user's intro status.

    Usage:
        /reset <user_id>

    This removes the user from the database, forcing them to re-introduce
    if needed.
    """

    # Ensure command is executed in the correct group
    if update.effective_chat.id != GROUP_ID:
        return

    # Ensure only admins can run this command
    member = await context.bot.get_chat_member(
        chat_id=GROUP_ID,
        user_id=update.effective_user.id,
    )

    if member.status not in ["administrator", "creator"]:
        await update.message.reply_text("❌ You must be an admin to use this command.")
        return

    # Ensure user_id argument is provided
    if not context.args:
        await update.message.reply_text("Usage: /reset <user_id>")
        return

    # Validate user_id is an integer
    try:
        user_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Invalid user_id. It must be a number.")
        return

    # Check if user exists in database
    status = get_user_status(user_id, GROUP_ID)

    if not status:
        await update.message.reply_text("⚠️ That user is not in the database.")
        return

    # Delete user record
    delete_user(user_id, GROUP_ID)

    await update.message.reply_text(
        f"✅ User {user_id} has been reset successfully."
    )


def get_admin_handlers():
    """
    Returns a list of admin command handlers
    to be registered in main.py.
    """
    return [
        CommandHandler("reset", reset_user),
    ]