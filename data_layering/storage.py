def init_storage() -> None:

    conn.execute(
            """
            CREATE TABLE IF NOT EXISTS websites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                url TEXT NOT NULL UNIQUE,
                enabled INTEGER DEFAULT 1
            )
            """
        )

conn.execute(
            """
            CREATE TABLE IF NOT EXISTS scrape_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                start_time TEXT,
                end_time TEXT,
                duration_ms INTEGER,
                status TEXT,
                found INTEGER DEFAULT 0,
                saved INTEGER DEFAULT 0,
                duplicates INTEGER DEFAULT 0,
                created_at TEXT
            )
            """
        )

def init_storage() -> None:
    with _get_connection() as conn:
        conn.execute(""" CREATE TABLE IF NOT EXISTS articles (...) """)  
        conn.execute(""" CREATE TABLE IF NOT EXISTS websites (...) """)  
        conn.execute(""" CREATE TABLE IF NOT EXISTS scrape_logs (...) """)  
        conn.commit()

