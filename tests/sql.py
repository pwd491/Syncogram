from contextlib import closing
import sqlite3

class SQLite:
    def __init__(self):
        self.database = sqlite3.connect("test.db", check_same_thread=False)

    def get_accounts(self):
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                return cursor.execute("SELECT * FROM account").fetchall()
            
    def add_account(self, name):
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                request = cursor.execute("INSERT INTO `account` (name) VALUES (?)", (name,))
                if request:
                    return True
                return False
    
    def set_options(self, *args):
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                request = cursor.execute("UPDATE INTO `options` WHERE  (name) VALUES (?)", (name,))
                if request:
                    return True
                return False
    