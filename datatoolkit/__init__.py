"""Small, dependency-free toolkit for cleaning CSV data and building reports."""

__version__ = "1.0.0"

from datatoolkit.csv_cleaner import clean_csv, dedupe, normalise_row
from datatoolkit.report_writer import write_summary_csv, write_summary_html
from datatoolkit.sqlite_report import load_csv_into_sqlite, monthly_summary

__all__ = [
    "clean_csv",
    "dedupe",
    "normalise_row",
    "write_summary_csv",
    "write_summary_html",
    "load_csv_into_sqlite",
    "monthly_summary",
]
