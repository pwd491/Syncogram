SQL_TABLE_USERS = \
"""
CREATE TABLE IF NOT EXISTS users
    (
        user_id INTEGER PRIMARY KEY,
        is_primary INTEGER,
        username VARCHAR(32),
        phone VARCHAR(16),
        first_name VARCHAR(64),
        last_name VARCHAR(64),
        restricted INTEGER,
        restriction_reason TEXT,
        stories_hidden INTEGER,
        stories_unavailable INTEGER,
        contact_require_premium INTEGER,
        scam INTEGER,
        fake INTEGER,
        premium INTEGER,
        photo INTEGER,
        emoji_status TEXT,
        usernames TEXT,
        color TEXT,
        profile_color TEXT,
        session TEXT,
        access_hash INTEGER
    )
"""

SQL_TABLE_OPTIONS = \
"""
CREATE TABLE IF NOT EXISTS options 
(
    user_id INTEGER PREFERENCE UNIQUE,
    is_sync_fav INTEGER DEFAULT 0,
    is_sync_profile_name INTEGER DEFAULT 0,
    is_sync_profile_media INTEGER DEFAULT 0,
    is_sync_public_channels_and_groups INTEGER DEFAULT 0,
    is_sync_privacy INTEGER DEFAULT 0,
    is_sync_secure INTEGER DEFAULT 0,
    is_sync_stickers_emojis_gifs INTEGER DEFAULT 0
)
"""

SQL_UPDATE_OPTIONS = \
"""
UPDATE `options`
SET 
is_sync_fav = (?),
is_sync_profile_name = (?),
is_sync_profile_media = (?),
is_sync_public_channels_and_groups = (?),
is_sync_privacy = (?),
is_sync_secure = (?),
is_sync_stickers_emojis_gifs = (?)
FROM 
(
    SELECT user_id FROM users WHERE is_primary = 1
) as users 
WHERE 
(
    options.user_id = users.user_id
)
"""

SQL_INSERT_OPTIONS = \
"""
INSERT INTO options
VALUES 
(
(SELECT user_id FROM users WHERE is_primary = 1),
(?), 
(?),
(?),
(?),
(?),
(?),
(?)
)
"""


SQL_TABLE_DB_DATA = \
"""
CREATE TABLE IF NOT EXISTS db_data (version VARCHAR)
"""

# SQL_TRIGGER_DEFAULT_OPTIONS = \
# """
# CREATE TRIGGER IF NOT EXISTS defaults_options_on_insert
# AFTER INSERT ON users 
# BEGIN 
#     INSERT INTO options 
#                 VALUES 
#                 (
#                     NEW.user_id,
#                     0,
#                     0,
#                     0
#                 );
#     END;
# """

SQL_TRIGGER_DROP_OPTIONS = \
"""
CREATE TRIGGER IF NOT EXISTS delete_options_on_delete
BEFORE DELETE
    ON users
BEGIN
    DELETE FROM options
        WHERE 
        (
            old.user_id = options.user_id
        );
END;
"""

SQL_ADD_USER = \
"""
INSERT INTO users
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
"""

SQL_GET_USERS = """SELECT * FROM users"""
SQL_GET_USER_ID_BY_STATUS = """SELECT user_id FROM users WHERE is_primary = (?) """
SQL_GET_USERNAME_BY_STATUS = """SELECT username FROM users WHERE is_primary = (?)"""
SQL_GET_SESSION_BY_ID = """SELECT session FROM users WHERE user_id = ?"""
SQL_GET_SESSION_BY_STATUS = """SELECT session FROM users WHERE is_primary = ?"""
SQL_DELETE_USER_BY_ID = """DELETE FROM users WHERE user_id = ?"""
SQL_DROP_OPTIONS = """DROP TABLE options"""
SQL_GET_DATABASE_VERSION = """SELECT version FROM db_data"""
SQL_INSERT_DB_VERSION = """INSERT INTO db_data VALUES (?)"""
SQL_UPDATE_DB_VERSION = """UPDATE db_data SET version = (?)"""

SQL_GET_OPTIONS = \
"""
SELECT *
FROM options 
WHERE options.user_id = 
(
    SELECT user_id FROM users WHERE is_primary = 1
)
"""
