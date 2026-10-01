import tempfile
import unittest
from pathlib import Path

from datatoolkit.sqlite_report import load_csv_into_sqlite, monthly_summary

SAMPLE_CSV = (
    "order_id,order_date,amount\n"
    "A-1,2026-01-05,100\n"
    "A-2,2026-01-20,50\n"
    "A-2,2026-01-20,50\n"
    "A-3,2026-02-02,25\n"
)


class SqliteReportTests(unittest.TestCase):
    def _write_sample(self, tmp: str) -> Path:
        csv_path = Path(tmp) / "sales.csv"
        csv_path.write_text(SAMPLE_CSV, encoding="utf-8")
        return csv_path

    def test_load_without_key_keeps_every_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = self._write_sample(tmp)
            db_path = Path(tmp) / "sales.db"

            loaded = load_csv_into_sqlite(csv_path, db_path, "sales")

            self.assertEqual(loaded, 4)

    def test_load_with_key_removes_duplicates(self):
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = self._write_sample(tmp)
            db_path = Path(tmp) / "sales.db"

            loaded = load_csv_into_sqlite(csv_path, db_path, "sales", key="order_id")

            self.assertEqual(loaded, 3)

    def test_monthly_summary_groups_by_month(self):
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = self._write_sample(tmp)
            db_path = Path(tmp) / "sales.db"
            load_csv_into_sqlite(csv_path, db_path, "sales", key="order_id")

            summary = monthly_summary(db_path, "sales")

            self.assertEqual([row["month"] for row in summary], ["2026-01", "2026-02"])
            self.assertEqual(summary[0]["orders"], 2)
            self.assertAlmostEqual(summary[0]["total"], 150.0)
            self.assertEqual(summary[1]["orders"], 1)
            self.assertAlmostEqual(summary[1]["total"], 25.0)


if __name__ == "__main__":
    unittest.main()
