from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Iterator

import psycopg2
from psycopg2.extras import RealDictCursor


def _get_db_config() -> dict:
    """Read DB config from environment variables.

    This mirrors the information that was previously configured for
    Flask, but without any framework dependency.
    """

    return {
        "dbname": os.getenv("POSTGRES_DB", "bus_tracking"),
        "user": os.getenv("POSTGRES_USER", "postgres"),
        "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": int(os.getenv("POSTGRES_PORT", "5432")),
    }


@contextmanager
def get_connection() -> Iterator[psycopg2.extensions.connection]:
    """Yield a PostgreSQL connection using psycopg2.

    Usage:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
    """

    config = _get_db_config()
    conn = psycopg2.connect(**config)
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def get_cursor(dict_cursor: bool = True) -> Iterator[psycopg2.extensions.cursor]:
    """Yield a cursor, optionally as a RealDictCursor."""

    with get_connection() as conn:
        cursor_factory = RealDictCursor if dict_cursor else None
        with conn.cursor(cursor_factory=cursor_factory) as cur:
            yield cur
            conn.commit()
