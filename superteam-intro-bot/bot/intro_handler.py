"""
intro_handler.py

Handles intro submissions in the intro thread.
- Validates intro quality
- Updates user status to COMPLETED
- Restores full chat permissions

Designed for python-telegram-bot v20.7
"""

import logging
from telegram import ChatPermissions, Update
from telegram.ext import ContextTypes
from bot.config import GROUP_ID, INTRO_THREAD_ID
from bot.database import get_user_status, set_user_status
from bot.validators import is_valid_intro

logger = logging.getLogger(__name__)


async def handle_intro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Triggered on every text message.
    Only processes valid intro submissions inside intro thread.
    """

    # Ensure correct group
    if update.effective_chat.id != GROUP_ID:
        return

    message = update.message

    # Ignore non-text messages
    if not message or not message.text:
        return

    # Ensure correct topic/thread
    if message.message_thread_id != INTRO_THREAD_ID:
        return

    user = update.effective_user

    # Ignore bots
    if user.is_bot:
        return

    user_id = user.id

    status = get_user_status(user_id, GROUP_ID)

    # Only process users who are pending
    if status != "PENDING":
        return

    # Validate intro quality
    if not is_valid_intro(message.text):
        await message.reply_text(
            "🙏 Please provide a slightly more detailed intro.\n\n"
            "Minimum: 3 lines and at least 150 characters."
        )
        return

    # Mark as completed
    set_user_status(user_id, GROUP_ID, "COMPLETED")

    # Restore full permissions
    try:
        await context.bot.restrict_chat_member(
            chat_id=GROUP_ID,
            user_id=user_id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_audios=True,
                can_send_documents=True,
                can_send_photos=True,
                can_send_videos=True,
                can_send_video_notes=True,
                can_send_voice_notes=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_change_info=False,
                can_invite_users=True,
                can_pin_messages=False,
            ),
        )
    except Exception as e:
        logger.error(f"Failed to restore permissions for {user_id}: {e}")
        return

    logger.info(f"User {user_id} completed intro successfully.")

    await message.reply_text("✅ Intro complete! Welcome officially 🎉")