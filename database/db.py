import sqlite3
DB_NAME = "database/database.db"

conn = sqlite3.connect("database/database.db")

cursor = conn.cursor()


def create_tables():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS downloads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        song_name TEXT
    )
    """)

    conn.commit()

def add_user(telegram_id):

    cursor.execute(
        "INSERT OR IGNORE INTO users (telegram_id) VALUES (?)",
        (telegram_id,)
    )

    conn.commit()

def add_download(user_id, song_name):

    cursor.execute(
        """
        INSERT INTO downloads
        (user_id, song_name)
        VALUES (?, ?)
        """,
        (user_id, song_name)
    )

    conn.commit()

def get_total_users():

    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )

    return cursor.fetchone()[0]

def get_total_downloads():

    cursor.execute(
        "SELECT COUNT(*) FROM downloads"
    )

    return cursor.fetchone()[0]

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_links (
    user_id INTEGER PRIMARY KEY,
    url TEXT
)
""")

def save_user_link(user_id, url):

    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO user_links
    (user_id, url)
    VALUES (?, ?)
    """, (user_id, url))

    conn.commit()
    conn.close()


def get_user_link(user_id):

    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT url FROM user_links
    WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return None

def delete_user_link(user_id):

    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM user_links
    WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()


def get_all_users():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT user_id FROM users"
    )

    users = cursor.fetchall()

    conn.close()

    return [u[0] for u in users]
