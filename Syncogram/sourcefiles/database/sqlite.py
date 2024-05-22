"""Database module of Syncogram application."""

import os
import sys
import sqlite3

from contextlib import closing
from typing import Any

from ..utils import check_db_version
from .constants import (
    SQL_TABLE_USERS,
    SQL_TABLE_OPTIONS,
    SQL_TABLE_DB_DATA,
    SQL_ADD_USER,
    SQL_GET_USERS,
    SQL_GET_OPTIONS,
    SQL_GET_SESSION_BY_ID,
    SQL_GET_SESSION_BY_STATUS,
    SQL_GET_USER_ID_BY_STATUS,
    SQL_GET_USERNAME_BY_STATUS,
    SQL_DELETE_USER_BY_ID,
    SQL_INSERT_OPTIONS,
    SQL_UPDATE_OPTIONS,
    SQL_DROP_OPTIONS,
    SQL_GET_DATABASE_VERSION,
    SQL_INSERT_DB_VERSION,
    SQL_UPDATE_DB_VERSION,
    SQL_TRIGGER_DROP_OPTIONS
)

WORK_DIR = ""

match sys.platform:
    case "win32":
        WORK_DIR = "./AppData/Local"
    case _:
        WORK_DIR = "./.local/share"

WORK_DIR = os.path.join(os.path.expanduser("~"), WORK_DIR, "Syncogram")

if not os.path.exists(WORK_DIR) or not os.path.isdir(WORK_DIR):
    os.mkdir(WORK_DIR)

DB_NAME = "syncogram"
DB_EXTENSION = ".sqlite3"
DB_FILE = os.path.join(WORK_DIR, DB_NAME + DB_EXTENSION)


class SQLite:
    """The main class of Database."""

    def __init__(self) -> None:
        self.database: sqlite3.Connection = sqlite3.connect(
            DB_FILE, check_same_thread=False
        )
        self.database.cursor().execute(SQL_TABLE_DB_DATA).close()
        self.database.cursor().execute(SQL_TABLE_USERS).close()
        self.database.cursor().execute(SQL_TABLE_OPTIONS).close()
        self.database.cursor().execute(SQL_TRIGGER_DROP_OPTIONS).close()

    def add_user(self, *args) -> bool | int:
        """Get user data and save to database."""
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                try:
                    request = cursor.execute(SQL_ADD_USER, (*args,))
                    return bool(request)
                except sqlite3.IntegrityError as error:
                    return error.sqlite_errorcode

    def get_users(self) -> list[Any]:
        """Get all users."""
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                return cursor.execute(SQL_GET_USERS).fetchall()

    def get_session_by_id(self, account_id) -> list[int]:
        """Get user by id"""
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                return cursor.execute(
                    SQL_GET_SESSION_BY_ID, (account_id,)
                ).fetchone()[0]

    def get_user_id_by_status(self, status: int) -> list[str]:
        """Get user by id"""
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                request = cursor.execute(
                    SQL_GET_USER_ID_BY_STATUS, (status,)
                ).fetchone()
                return request[0] if request is not None else request

    def get_session_by_status(self, is_primary: int) -> list[str]:
        """Get user by status (sender or recepient)."""
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                return cursor.execute(
                    SQL_GET_SESSION_BY_STATUS, (is_primary,)
                ).fetchone()[0]

    def get_username_by_status(self, is_primary: int) -> str:
        """Get username by status (sender or recepient)."""
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                return cursor.execute(
                    SQL_GET_USERNAME_BY_STATUS, (is_primary,)
                ).fetchone()[0]

    def delete_user_by_id(self, account_id) -> None:
        """Delete user by id."""
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                return cursor.execute(
                    SQL_DELETE_USER_BY_ID, (account_id,)
                )

    def get_options(self) -> list[int] | None:
        """Get options values only for primary account (sender)."""
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                request = cursor.execute(
                    SQL_GET_OPTIONS
                ).fetchone()
                if bool(request):
                    return request
                return None

    def set_options(self, *args) -> bool:
        """Set options values only for primary account (sender)."""
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                user = bool(self.get_options())
                if user:
                    request = cursor.execute(SQL_UPDATE_OPTIONS, (*args,))
                else:
                    user = self.get_user_id_by_status(1)
                    if user:
                        request = cursor.execute(SQL_INSERT_OPTIONS, (*args,))
                    else:
                        return False
                return bool(request)

    def get_version(self) -> str | None:
        """Get database version from db_data table."""
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                request = cursor.execute(SQL_GET_DATABASE_VERSION).fetchone()
                if bool(request):
                    return request[0]
                return None
    
    def set_version(self, version) -> None:
        """Set database version if not exists."""
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                cursor.execute(SQL_INSERT_DB_VERSION, (version,))

    def update_version(self, version) -> None:
        """Update database version if exists newest."""
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                cursor.execute(SQL_UPDATE_DB_VERSION, (version,))

    def check_update(self):
        """Check and update database options."""
        current_db_version = self.get_version()
        if current_db_version is not None:
            need_to_update = check_db_version(current_db_version)
            if isinstance(need_to_update, tuple):
                self.database.cursor().execute(SQL_DROP_OPTIONS).close()
                self.database.cursor().execute(SQL_TABLE_OPTIONS).close()
                self.update_version(need_to_update[1])
        else:
            from ..utils import get_local_database_version
            self.set_version(get_local_database_version())
