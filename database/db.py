import sqlite3
import os


DB_PATH = "database/soccer.db"


def get_connection():

    os.makedirs(
        "database",
        exist_ok=True
    )

    conn = sqlite3.connect(DB_PATH)

    return conn



def init_db():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS favorites (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        team_id INTEGER UNIQUE,

        team_name TEXT,

        logo TEXT

    )
    """)


    conn.commit()

    conn.close()


if __name__ == "__main__":

    init_db()

    print("Database initialized")