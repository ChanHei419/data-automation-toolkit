"""Load CSV data into SQLite and build summary queries."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from datatoolkit.csv_cleaner import dedupe, read_csv


def load_csv_into_sqlite(
    csv_path: str | Path,
    db_path: str | Path,
    table: str = "sales",
    key: str | None = None,
) -> int:
    """Create (or replace) a table from a CSV file.

    Headers and values are normalised (trimmed, lowercase keys). When ``key``
    is given, duplicate records are removed before loading (last one wins).

    Every column is stored as TEXT to keep the load simple and lossless —
    numeric conversion happens in SQL when building reports.

    Returns the number of rows inserted.
    """
    rows = read_csv(csv_path)
    if key:
        rows = dedupe(rows, key)

    if not rows:
        return 0

    columns = list(rows[0].keys())
    column_definitions = ", ".join(f'"{name}" TEXT' for name in columns)
    quoted_columns = ", ".join(f'"{name}"' for name in columns)
    placeholders = ", ".join("?" for _ in columns)

    with sqlite3.connect(db_path) as connection:
        connection.execute(f'DROP TABLE IF EXISTS "{table}"')
        connection.execute(f'CREATE TABLE "{table}" ({column_definitions})')
        connection.executemany(
            f'INSERT INTO "{table}" ({quoted_columns}) VALUES ({placeholders})',
            [[row.get(name, "") for name in columns] for row in rows],
        )

    return len(rows)


def monthly_summary(db_path: str | Path, table: str = "sales") -> list[dict]:
    """Aggregate total amount and order count per month.

    Expects the loaded table to have ``order_date`` (YYYY-MM-DD...) and
    ``amount`` columns.
    """
    query = f"""
        SELECT substr(order_date, 1, 7) AS month,
               COUNT(*) AS orders,
               SUM(CAST(amount AS REAL)) AS total
        FROM "{table}"
        GROUP BY month
        ORDER BY month
    """

    with sqlite3.connect(db_path) as connection:
        connection.row_factory = sqlite3.Row
        return [dict(row) for row in connection.execute(query)]
