"""Write summary reports as CSV and standalone HTML."""

from __future__ import annotations

import csv
import html
from pathlib import Path


def write_summary_csv(rows: list[dict], path: str | Path) -> None:
    """Write summary rows to a CSV file."""
    destination = Path(path)
    if not rows:
        destination.write_text("", encoding="utf-8")
        return

    with open(destination, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_summary_html(rows: list[dict], path: str | Path, title: str = "Monthly Summary") -> None:
    """Write summary rows to a self-contained HTML report."""
    headers = list(rows[0].keys()) if rows else []

    header_html = "".join(f"<th>{html.escape(str(name))}</th>" for name in headers)
    body_html = "\n".join(
        "<tr>"
        + "".join(f"<td>{html.escape(str(row[name]))}</td>" for name in headers)
        + "</tr>"
        for row in rows
    )

    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: system-ui, -apple-system, sans-serif; margin: 2rem; color: #1f2937; }}
    h1 {{ font-size: 1.4rem; }}
    table {{ border-collapse: collapse; margin-top: 1rem; }}
    th, td {{ border: 1px solid #d1d5db; padding: 0.5rem 1rem; text-align: right; }}
    th {{ background: #f3f4f6; }}
    td:first-child, th:first-child {{ text-align: left; }}
  </style>
</head>
<body>
  <h1>{html.escape(title)}</h1>
  <table>
    <thead><tr>{header_html}</tr></thead>
    <tbody>{body_html}</tbody>
  </table>
</body>
</html>
"""

    Path(path).write_text(document, encoding="utf-8")
