"""Command-line interface for the data automation toolkit."""

from __future__ import annotations

import argparse
from pathlib import Path

from datatoolkit.csv_cleaner import clean_csv
from datatoolkit.report_writer import write_summary_csv, write_summary_html
from datatoolkit.sqlite_report import load_csv_into_sqlite, monthly_summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="datatoolkit",
        description="Clean CSV data and turn it into summary reports.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    clean = subparsers.add_parser(
        "clean", help="Normalise and de-duplicate a CSV file"
    )
    clean.add_argument("source", type=Path, help="Input CSV file")
    clean.add_argument("destination", type=Path, help="Output CSV file")
    clean.add_argument(
        "--key", default="order_id", help="Column used to de-duplicate (default: order_id)"
    )

    report = subparsers.add_parser(
        "report", help="Load a CSV into SQLite and generate CSV + HTML summaries"
    )
    report.add_argument("source", type=Path, help="Input CSV file")
    report.add_argument(
        "--db", type=Path, default=Path("data/reports.db"), help="SQLite database path"
    )
    report.add_argument(
        "--out-dir", type=Path, default=Path("reports"), help="Report output directory"
    )
    report.add_argument("--table", default="sales", help="SQLite table name")
    report.add_argument(
        "--key",
        default="order_id",
        help="Column used to de-duplicate before loading (default: order_id)",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "clean":
        unique_rows = clean_csv(args.source, args.destination, args.key)
        print(f"Cleaned {unique_rows} unique rows -> {args.destination}")
        return 0

    if args.command == "report":
        args.db.parent.mkdir(parents=True, exist_ok=True)
        loaded = load_csv_into_sqlite(args.source, args.db, args.table, args.key)
        summary = monthly_summary(args.db, args.table)

        args.out_dir.mkdir(parents=True, exist_ok=True)
        csv_path = args.out_dir / "monthly_summary.csv"
        html_path = args.out_dir / "monthly_summary.html"
        write_summary_csv(summary, csv_path)
        write_summary_html(summary, html_path)

        print(f"Loaded {loaded} rows into {args.db}")
        print(f"Wrote {csv_path} and {html_path}")
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
