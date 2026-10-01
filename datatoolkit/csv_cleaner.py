"""Normalise and de-duplicate CSV data."""

from __future__ import annotations

import csv
from pathlib import Path


def normalise_row(row: dict[str, str]) -> dict[str, str]:
    """Strip whitespace from keys and values, and lowercase the keys."""
    return {
        (key or "").strip().lower(): (value or "").strip()
        for key, value in row.items()
    }


def read_csv(path: str | Path) -> list[dict[str, str]]:
    """Read a CSV file into a list of normalised dictionaries."""
    with open(path, newline="", encoding="utf-8") as handle:
        return [normalise_row(row) for row in csv.DictReader(handle)]


def dedupe(rows: list[dict[str, str]], key: str) -> list[dict[str, str]]:
    """Remove duplicate records by key; the last occurrence wins."""
    deduplicated: dict[str, dict[str, str]] = {}
    for row in rows:
        deduplicated[row[key]] = row
    return list(deduplicated.values())


def write_csv(rows: list[dict[str, str]], path: str | Path) -> None:
    """Write dictionaries to a CSV file."""
    destination = Path(path)
    if not rows:
        destination.write_text("", encoding="utf-8")
        return

    with open(destination, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def clean_csv(source: str | Path, destination: str | Path, key: str) -> int:
    """Read, normalise, and de-duplicate a CSV file.

    Returns the number of unique rows written.
    """
    cleaned = dedupe(read_csv(source), key)
    write_csv(cleaned, destination)
    return len(cleaned)
