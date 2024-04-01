from contextlib import closing
from typing import Any
import sqlite3


class SQLite:
    def __init__(self) -> None:
        self.database: sqlite3.Connection = sqlite3.connect(
            "test.db", check_same_thread=False
        )
        self.users_table = """
                            CREATE TABLE IF NOT EXISTS users (
                            user_id INTEGER,
                            name TEXT NOT NULL,
                            is_primary BOOLEAN NOT NULL DEFAULT (0),
                            session TEXT,
                            PRIMARY KEY (
                                user_id AUTOINCREMENT
                                )
                            )
                            """

        self.options_table = """
                            CREATE TABLE IF NOT EXISTS options (
                                user_id INTEGER REFERENCES users (user_id) UNIQUE,
                                is_sync_fav INTEGER DEFAULT 0,
                                is_sync_pin_fav INTEGER DEFAULT 0,
                                PRIMARY KEY (
                                    user_id
                                )
                            )
                            """

        self.trigger_insert_options = """
                            CREATE TRIGGER IF NOT EXISTS defaults_options_on_insert
                            AFTER INSERT ON users 
                            BEGIN 
                                INSERT INTO options 
                                            VALUES (
                                                NEW.user_id,
                                                1,
                                                0
                                            );
                                END;
                            """

        self.trigger_delete_options = """
                            CREATE TRIGGER IF NOT EXISTS delete_options_on_delete
                                    BEFORE DELETE
                                        ON users
                            BEGIN
                                DELETE FROM options
                                    WHERE (old.user_id = options.user_id);
                            END;
                            """

        self.database.cursor().execute(self.users_table).close()
        self.database.cursor().execute(self.options_table).close()
        self.database.cursor().execute(self.trigger_insert_options).close()
        self.database.cursor().execute(self.trigger_delete_options).close()

    def get_users(self) -> list[Any]:
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                return cursor.execute("SELECT * FROM users").fetchall()

    def add_user(self, id: int, name: str, is_primary: int, session: str) -> bool:
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                request = cursor.execute(
                    "INSERT INTO `users` (user_id, name, is_primary, session) VALUES (?,?,?,?)", (id,name,is_primary,session,)
                )
                return True if request else False
            

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
                    "UPDATE `options` SET is_sync_fav = (?), is_sync_pin_fav = (?) FROM (SELECT user_id FROM users WHERE is_primary = 1) as users WHERE (options.user_id = users.user_id)",
                    (*args,),
                )
                return True if request else False


if __name__ == "__main__":
    abs = SQLite()
    res = abs.get_options()
    print(res)
