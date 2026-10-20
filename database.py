import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "trustgate.db"


def create_database():
    connection = sqlite3.connect(DB_PATH)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)

    connection.execute("""
        INSERT OR IGNORE INTO students (id, name, phone)
        VALUES
            (1, 'Student One', '9000000001'),
            (2, 'Student Two', '9000000002'),
            (3, 'Student Three', '9000000003')
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
    print("TRUSTGATE AI database created successfully!")
    print("Sample student records added.")
def create_audit_table():
    connection = sqlite3.connect(DB_PATH)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            decision TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def log_action(action, decision):
    connection = sqlite3.connect(DB_PATH)

    connection.execute("""
        INSERT INTO audit_logs (action, decision)
        VALUES (?, ?)
    """, (action, decision))

    connection.commit()
    connection.close()


def get_audit_logs():
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.execute("""
        SELECT id, action, decision, timestamp
        FROM audit_logs
        ORDER BY id DESC
    """)

    logs = cursor.fetchall()
    connection.close()

    return logs
