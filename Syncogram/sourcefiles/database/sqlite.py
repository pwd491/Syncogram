"""Database module of Syncogram application."""

import os
import sqlite3

from contextlib import closing
from typing import Any

from ..utils import check_db_version
from ..utils import get_work_dir
from ..utils import logging
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

logger = logging()
WORK_DIR = get_work_dir()
logger.info(f"Working directory path [{WORK_DIR}]")
if not os.path.exists(WORK_DIR) or not os.path.isdir(WORK_DIR):
    logger.info("Working directory creating")
    os.mkdir(WORK_DIR)

DB_NAME = "syncogram"
DB_EXTENSION = ".sqlite3"
DB_FILE = os.path.join(WORK_DIR, DB_NAME + DB_EXTENSION)


class SQLite:
    """The main class of Database."""
    @logger.catch()
    def __init__(self) -> None:
        self.database: sqlite3.Connection = sqlite3.connect(
            DB_FILE, check_same_thread=False
        )
        self.database.cursor().execute(SQL_TABLE_DB_DATA).close()
        self.database.cursor().execute(SQL_TABLE_USERS).close()
        self.database.cursor().execute(SQL_TABLE_OPTIONS).close()
        self.database.cursor().execute(SQL_TRIGGER_DROP_OPTIONS).close()

    @logger.catch()
    def add_user(self, *args) -> bool | int:
        """Get user data and save to database."""
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                try:
                    request = cursor.execute(SQL_ADD_USER, (*args,))
                    return bool(request)
                except sqlite3.IntegrityError as error:
                    return error.sqlite_errorcode
                
    @logger.catch()
    def get_users(self) -> list[Any]:
        """Get all users."""
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                return cursor.execute(SQL_GET_USERS).fetchall()

    @logger.catch()
    def get_session_by_id(self, account_id) -> list[int]:
        """Get user by id"""
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                return cursor.execute(
                    SQL_GET_SESSION_BY_ID, (account_id,)
                ).fetchone()[0]

    @logger.catch()
    def get_user_id_by_status(self, status: int) -> list[str]:
        """Get user by id"""
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                request = cursor.execute(
                    SQL_GET_USER_ID_BY_STATUS, (status,)
                ).fetchone()
                return request[0] if request is not None else request

    @logger.catch()
    def get_session_by_status(self, is_primary: int) -> list[str]:
        """Get user by status (sender or recepient)."""
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                return cursor.execute(
                    SQL_GET_SESSION_BY_STATUS, (is_primary,)
                ).fetchone()[0]

    @logger.catch()
    def get_username_by_status(self, is_primary: int) -> str:
        """Get username by status (sender or recepient)."""
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                return cursor.execute(
                    SQL_GET_USERNAME_BY_STATUS, (is_primary,)
                ).fetchone()[0]

    @logger.catch()
    def delete_user_by_id(self, account_id) -> None:
        """Delete user by id."""
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                return cursor.execute(
                    SQL_DELETE_USER_BY_ID, (account_id,)
                )

    @logger.catch()
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

    @logger.catch()
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

    @logger.catch()
    def get_version(self) -> str | None:
        """Get database version from db_data table."""
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                request = cursor.execute(SQL_GET_DATABASE_VERSION).fetchone()
                if bool(request):
                    return request[0]
                return None

    @logger.catch()
    def set_version(self, version) -> None:
        """Set database version if not exists."""
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                cursor.execute(SQL_INSERT_DB_VERSION, (version,))

    @logger.catch()
    def update_version(self, version) -> None:
        """Update database version if exists newest."""
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                cursor.execute(SQL_UPDATE_DB_VERSION, (version,))

    @logger.catch()
    def check_update(self):
        """Check and update database options."""
        current_db_version = self.get_version()
        logger.info(f"Local Database version: [{current_db_version}]")
        if current_db_version is not None:
            need_to_update = check_db_version(current_db_version)
            logger.info(f"Remote Database version: [{current_db_version}]")
            if isinstance(need_to_update, tuple):
                logger.info("Re-creating database cause new version.")
                self.database.cursor().execute(SQL_DROP_OPTIONS).close()
                self.database.cursor().execute(SQL_TABLE_OPTIONS).close()
                self.update_version(need_to_update[1])
        else:
            from ..utils import get_local_database_version
            self.set_version(get_local_database_version())
