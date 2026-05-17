import sqlite3
import hashlib
import os
from datetime import datetime
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "candidate_store.db")


def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS candidates (
                resume_hash TEXT PRIMARY KEY,
                resume_text TEXT NOT NULL,
                jd_hash     TEXT,
                jd_text     TEXT,
                skills      TEXT,
                scores      TEXT,
                created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_seen   DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()



def hash_bytes(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


def get_candidate(resume_hash: str) -> dict | None:
    """Return cached candidate data or None if not found."""
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM candidates WHERE resume_hash = ?", (resume_hash,)
        ).fetchone()
        if row:
            # Update last_seen timestamp
            conn.execute(
                "UPDATE candidates SET last_seen = ? WHERE resume_hash = ?",
                (datetime.now().isoformat(), resume_hash)
            )
            conn.commit()
            return dict(row)
    return None


def save_candidate(resume_hash: str, resume_text: str):
    """Save a new candidate's resume to the store."""
    with _get_conn() as conn:
        conn.execute(
            """INSERT OR REPLACE INTO candidates (resume_hash, resume_text, last_seen)
               VALUES (?, ?, ?)""",
            (resume_hash, resume_text, datetime.now().isoformat())
        )
        conn.commit()

def save_scores(resume_hash: str, scores: dict, jd_text: str = None):
    with _get_conn() as conn:
        conn.execute(
            """UPDATE candidates 
               SET scores = ?, jd_text = ?, last_seen = ?
               WHERE resume_hash = ?""",
            (json.dumps(scores), jd_text, datetime.now().isoformat(), resume_hash)
        )
        conn.commit()


def get_scores(resume_hash: str) -> dict | None:
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT scores FROM candidates WHERE resume_hash = ?", (resume_hash,)
        ).fetchone()
        if row and row["scores"]:
            return json.loads(row["scores"])
    return None



init_db()
