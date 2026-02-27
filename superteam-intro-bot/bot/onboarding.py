"""
onboarding.py

Handles new member onboarding:
- Detects actual joins
- Restricts user from sending messages
- Marks them as PENDING in database
- Sends intro instructions via DM

Designed for python-telegram-bot v20.7
"""

import logging
from telegram import ChatPermissions, Update
from telegram.ext import ContextTypes
from config import GROUP_ID, INTRO_THREAD_ID
from database import set_user_status

logger = logging.getLogger(__name__)


async def handle_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Triggered when a user's chat member status changes.
    Only acts when a user genuinely joins the group.
    """

    if update.effective_chat.id != GROUP_ID:
        return

    member = update.chat_member

    old_status = member.old_chat_member.status
    new_status = member.new_chat_member.status

    # Only act when user joins (left/kicked → member)
    if old_status not in ("left", "kicked") or new_status != "member":
        return

    user = member.new_chat_member.user

    # Ignore bots (including this bot)
    if user.is_bot:
        return

    logger.info(f"New member joined: {user.id}")

    # Restrict user from sending messages
    try:
        await context.bot.restrict_chat_member(
            chat_id=GROUP_ID,
            user_id=user.id,
            permissions=ChatPermissions(can_send_messages=False),
        )
    except Exception as e:
        logger.error(f"Failed to restrict user {user.id}: {e}")
        return

    # Store user as PENDING intro
    set_user_status(user.id, GROUP_ID, "PENDING")

    # Send DM with intro instructions
    intro_link = f"https://t.me/SuperteamMY/{INTRO_THREAD_ID}"

    try:
        await context.bot.send_message(
            chat_id=user.id,
            text=(
                "👋 Welcome to Superteam MY!\n\n"
                "To get started, please introduce yourself in the intro thread:\n\n"
                f"{intro_link}\n\n"
                "Please follow this format:\n\n"
                "• Who are you & what do you do?\n"
                "• Where are you based?\n"
                "• One fun fact about you\n"
                "• How are you looking to contribute?\n\n"
                "No pressure to be perfect — just be you!\n\n"
                "Once posted, you'll automatically get access 🎉"
            ),
        )
    except Exception as e:
        logger.warning(
            f"Could not send DM to user {user.id}. They may have DMs disabled."
        )