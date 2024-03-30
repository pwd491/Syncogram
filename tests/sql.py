from contextlib import closing
import sqlite3

class SQLite:
    def __init__(self):
        self.database = sqlite3.connect("test.db", check_same_thread=False)
        self.users_table = """
                            CREATE TABLE IF NOT EXISTS users (
                            user_id INTEGER,
                            name TEXT NOT NULL,
                            prime BOOLEAN NOT NULL DEFAULT (0),
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
                                INSERT INTO options (
                                                user_id,
                                                is_sync_fav,
                                                is_sync_pin_fav
                                            )
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

        self.database.cursor().execute(self.users_table)
        self.database.cursor().execute(self.options_table)
        self.database.cursor().execute(self.trigger_insert_options)
        self.database.cursor().execute(self.trigger_delete_options)
        self.database.cursor().close()


    def get_users(self):
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                return cursor.execute("SELECT * FROM users").fetchall()
            
    def add_user(self, name):
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                request = cursor.execute("INSERT INTO `users` (name) VALUES (?)", (name,))
                if request:
                    return True
                return False
    
    def set_options(self, *args):
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                request = cursor.execute("UPDATE INTO `options` WHERE  (name) VALUES (?)", ())
                if request:
                    return True
                return False
    
    def test(self):
        with self.database as connect:
            with closing(connect.cursor()) as cursor:
                request = cursor.execute("UPDATE `options` SET is_sync_fav = 1123113213 FROM (SELECT user_id FROM users WHERE prime = 1) as users WHERE users.user_id = options.user_id")
                return request
            
if __name__ == "__main__":
    abs = SQLite()
    res = abs.add_user("Sergey")      
    print(res)