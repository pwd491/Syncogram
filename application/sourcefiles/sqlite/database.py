from contextlib import closing
from typing import Any
import sqlite3

class SQLite:
    def __init__(self):
        self.database: sqlite3.Connection = sqlite3.connect("test.db", check_same_thread=False)
        # self.cursor.execute("""
        #     CREATE TABLE IF NOT EXISTS account \
        #     ("id" INTEGER PRIMARY KEY AUTOINCREMENT,\
        #     "name" TEXT NOT NULL, \
        #     "primary" BOOLEAN NOT NULL DEFAULT False,\
        #     "session" TEXT)
        # """)

    def execute_all(self) -> list[Any]:
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                return cursor.execute("SELECT * FROM account").fetchall()

    def execute_accs(self, *args) -> list[Any]:
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                return cursor.execute("""SELECT * FROM account WHERE prime == ?""", (bool(*args),)).fetchall()

    def add_account(self, id, name, prime, *session) -> bool:
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                request: sqlite3.Cursor = cursor.execute("INSERT INTO account (id,name,prime) VALUES (?, ?, ?)", (id, name, prime,))
                return bool(request)



if __name__ == "__main__":
    print(123)
    sql = SQLite()
    res = sql.execute_accs(0)
    print(res)