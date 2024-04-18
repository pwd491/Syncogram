SQL_CREATE_USERS = """
                CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER,
                name TEXT NOT NULL,
                is_primary BOOLEAN NOT NULL DEFAULT (0),
                session TEXT,
                PRIMARY KEY (user_id AUTOINCREMENT))
                """

SQL_CREATE_OPTIONS = """
                CREATE TABLE IF NOT EXISTS options (
                    user_id INTEGER REFERENCES users (user_id) UNIQUE,
                    is_sync_fav INTEGER DEFAULT 0,
                    is_sync_pin_fav INTEGER DEFAULT 0,
                    is_sync_profile_name INTEGER DEFAULT 0,
                    PRIMARY KEY (
                        user_id
                    )
                )
                """

SQL_TRIGGER_DEFAULT_OPTIONS = """
                CREATE TRIGGER IF NOT EXISTS defaults_options_on_insert
                AFTER INSERT ON users 
                BEGIN 
                    INSERT INTO options 
                                VALUES (
                                    NEW.user_id,
                                    0,
                                    0,
                                    0
                                );
                    END;
                """

SQL_TRIGGER_DROP_OPTIONS = """
                CREATE TRIGGER IF NOT EXISTS delete_options_on_delete
                        BEFORE DELETE
                            ON users
                BEGIN
                    DELETE FROM options
                        WHERE (old.user_id = options.user_id);
                END;
                """