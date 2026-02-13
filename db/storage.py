import sqlite3
from pathlib import Path

DB_PATH = Path("repos.db")


class Storage:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.create_tables()

    def create_tables(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS repos (
            id INTEGER PRIMARY KEY,
            path TEXT UNIQUE
        )
        """)

    def add_repo(self, path: str):
        self.conn.execute("INSERT OR IGNORE INTO repos(path) VALUES(?)", (path,))
        self.conn.commit()

    def get_repos(self):
        cur = self.conn.execute("SELECT path FROM repos")
        return [r[0] for r in cur.fetchall()]

    def remove_repo(self, path: str):
        self.conn.execute("DELETE FROM repos WHERE path=?", (path,))
        self.conn.commit()