import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB = Path(__file__).with_name("memory.sqlite3")

def connect(path=DB):
    db = sqlite3.connect(path)
    db.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    db.commit()
    return db

def save(role, content, path=DB):
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with connect(path) as db:
        db.execute(
            "INSERT INTO messages(role,content,timestamp) VALUES(?,?,?)",
            (role, content, timestamp)
        )
    return timestamp

def history(limit=20, path=DB):
    with connect(path) as db:
        return db.execute("""
            SELECT role, content, timestamp FROM (
                SELECT * FROM messages ORDER BY id DESC LIMIT ?
            ) ORDER BY id
        """, (limit,)).fetchall()

def clear(path=DB):
    with connect(path) as db:
        db.execute("DELETE FROM messages")
