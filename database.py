

import sqlite3
from contextlib import closing
from pathlib import Path


DB_PATH = Path(__file__).parent / "trustgate.db"


def create_database():
    with closing(sqlite3.connect(DB_PATH, timeout=10)) as connection:
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL
                )
            """)

            connection.executemany("""
                INSERT OR IGNORE INTO students (id, name, phone)
                VALUES (?, ?, ?)
            """, [
                (1, "Student One", "DEMO-0001"),
                (2, "Student Two", "DEMO-0002"),
                (3, "Student Three", "DEMO-0003"),
            ])


def create_audit_table():
    with closing(sqlite3.connect(DB_PATH, timeout=10)) as connection:
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action TEXT NOT NULL,
                    decision TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)


def log_action(action, decision):
    if not isinstance(action, str) or not action.strip():
        raise ValueError("Action must be a non-empty string.")

    if decision not in ("ALLOW", "REVIEW", "BLOCK"):
        raise ValueError("Invalid policy decision.")

    create_audit_table()

    with closing(sqlite3.connect(DB_PATH, timeout=10)) as connection:
        with connection:
            connection.execute("""
                INSERT INTO audit_logs (action, decision)
                VALUES (?, ?)
            """, (action, decision))


def get_audit_logs():
    create_audit_table()

    with closing(sqlite3.connect(DB_PATH, timeout=10)) as connection:
        cursor = connection.execute("""
            SELECT id, action, decision, timestamp
            FROM audit_logs
            ORDER BY id DESC
        """)

        return cursor.fetchall()


if __name__ == "__main__":
    create_database()
    create_audit_table()
    print("TRUSTGATE AI database initialized.")
