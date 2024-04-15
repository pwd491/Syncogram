import os, sys
import sqlite3
from contextlib import closing
from typing import Any

from .consts import (
    SQL_CREATE_USERS,
    SQL_CREATE_OPTIONS,
    SQL_TRIGGER_DROP_OPTIONS,
    SQL_TRIGGER_DEFAULT_OPTIONS
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

DB_PATH = os.path.join(WORK_DIR, "test.db")

class SQLite:
    def __init__(self) -> None:
        self.database: sqlite3.Connection = sqlite3.connect(
            DB_PATH, check_same_thread=False
        )
        self.database.cursor().execute(SQL_CREATE_USERS).close()
        self.database.cursor().execute(SQL_CREATE_OPTIONS).close()
        self.database.cursor().execute(SQL_TRIGGER_DROP_OPTIONS).close()
        self.database.cursor().execute(SQL_TRIGGER_DEFAULT_OPTIONS).close()

    def get_users(self) -> list[Any]:
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                return cursor.execute("SELECT * FROM users").fetchall()
    
    def get_user_by_id(self, account_id):
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                return cursor.execute("SELECT session FROM users WHERE user_id = ?", (account_id,)).fetchone()

    def get_user_by_status(self, is_primary: int):
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                return cursor.execute("SELECT session FROM users WHERE is_primary = ?", (is_primary,)).fetchone()

    def add_user(self, user_id: int, name: str, is_primary: int, session: str) -> bool:
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                request = cursor.execute(
                    "INSERT INTO `users` VALUES (?,?,?,?)",
                    (
                        user_id,
                        name,
                        is_primary,
                        session,
                    ),
                )
                return bool(request)
            
    def delete_user_by_id(self, account_id):
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                return cursor.execute("DELETE FROM users WHERE user_id = ?", (account_id,))

    def get_options(self):
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                return cursor.execute(
                    "SELECT * FROM options WHERE options.user_id = (SELECT user_id FROM users WHERE is_primary = 1)"
                ).fetchone()

    def set_options(self, *args) -> bool:
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                request = cursor.execute(
                    "UPDATE `options` SET is_sync_fav = (?), is_sync_pin_fav = (?), is_sync_profile_name = (?) FROM (SELECT user_id FROM users WHERE is_primary = 1) as users WHERE (options.user_id = users.user_id)",
                    (*args,),
                )
                return bool(request)
