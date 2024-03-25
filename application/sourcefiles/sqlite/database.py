from typing import Any
import sqlite3

class SQLite:
    def __init__(self):
        self.database: sqlite3.Connection = sqlite3.connect("test.db")
        self.cursor: sqlite3.Cursor = self.database.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS account \
            ("id" INTEGER PRIMARY KEY AUTOINCREMENT,\
            "name" TEXT NOT NULL, \
            "primary" BOOLEAN NOT NULL DEFAULT False,\
            "session" TEXT)
        """)

    def execute_all(self) -> list[Any]:
        return self.cursor.execute("SELECT * FROM account").fetchall()
    
    
test = SQLite()
print(test.execute_all())