import sqlite3
import time
from pathlib import Path

_DB_PATH = Path(__file__).parent / "facts.sqlite"
_TTL = 86400  # 1 day in seconds


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS facts (
            slug       TEXT PRIMARY KEY,
            content    TEXT NOT NULL,
            fetched_at REAL NOT NULL
        )
        """
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_fetched_at ON facts (fetched_at)"
    )
    return conn


def evict_expired() -> None:
    """Delete cache entries older than TTL."""
    with _connect() as conn:
        conn.execute(
            "DELETE FROM facts WHERE fetched_at < ?",
            (time.time() - _TTL,),
        )


def get(slug: str) -> str | None:
    """Return cached content for slug if still fresh, otherwise None."""
    with _connect() as conn:
        row = conn.execute(
            "SELECT content FROM facts WHERE slug = ? AND fetched_at >= ?",
            (slug, time.time() - _TTL),
        ).fetchone()
    return row[0] if row else None


def put(slug: str, content: str) -> None:
    """Insert or replace cache entry with current timestamp."""
    with _connect() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO facts (slug, content, fetched_at) VALUES (?, ?, ?)",
            (slug, content, time.time()),
        )


# Evict stale entries on startup so the DB doesn't grow unboundedly.
evict_expired()
