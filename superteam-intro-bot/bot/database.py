"""
database.py

SQLite persistence layer for the Superteam Intro Gatekeeper Bot.

Handles:
- Storing user intro status
- Fetching user status
- Resetting users

Designed for python-telegram-bot v20+
"""

import sqlite3
from typing import Optional

DB_NAME = "bot.db"

# Allowed intro statuses
VALID_STATUSES = {"PENDING", "COMPLETED"}


def get_connection():
    """
    Returns a new SQLite connection.

    Using a fresh connection per operation avoids
    concurrency issues in async environments.
    """
    return sqlite3.connect(DB_NAME)


def initialize_database():
    """
    Ensures required tables exist.
    Called at bot startup.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER,
                chat_id INTEGER,
                status TEXT,
                PRIMARY KEY (user_id, chat_id)
            )
            """
        )
        conn.commit()


def set_user_status(user_id: int, chat_id: int, status: str) -> None:
    """
    Inserts or updates a user's intro status.
    """
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status '{status}'")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO users (user_id, chat_id, status)
            VALUES (?, ?, ?)
            """,
            (user_id, chat_id, status),
        )
        conn.commit()


def get_user_status(user_id: int, chat_id: int) -> Optional[str]:
    """
    Returns user's intro status or None if not found.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT status FROM users
            WHERE user_id = ? AND chat_id = ?
            """,
            (user_id, chat_id),
        )
        result = cursor.fetchone()
        return result[0] if result else None


def delete_user(user_id: int, chat_id: int) -> None:
    """
    Removes user from database.
    Used for admin reset.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM users
            WHERE user_id = ? AND chat_id = ?
            """,
            (user_id, chat_id),
        )
        conn.commit()