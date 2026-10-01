import tempfile
import unittest
from pathlib import Path

from datatoolkit.csv_cleaner import clean_csv, dedupe, normalise_row


class NormaliseRowTests(unittest.TestCase):
    def test_strips_whitespace_and_lowercases_keys(self):
        row = {" Order_ID ": " A-1 ", "Amount": " 12.5 "}
        self.assertEqual(
            normalise_row(row), {"order_id": "A-1", "amount": "12.5"}
        )

    def test_handles_missing_values(self):
        row = {"name": None}
        self.assertEqual(normalise_row(row), {"name": ""})


class DedupeTests(unittest.TestCase):
    def test_keeps_last_duplicate(self):
        rows = [
            {"order_id": "A-1", "amount": "10"},
            {"order_id": "A-1", "amount": "99"},
            {"order_id": "A-2", "amount": "5"},
        ]
        result = dedupe(rows, "order_id")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["amount"], "99")


class CleanCsvTests(unittest.TestCase):
    def test_clean_csv_writes_unique_rows_with_normalised_headers(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "raw.csv"
            destination = Path(tmp) / "clean.csv"
            source.write_text(
                "Order_ID, Amount\n"
                " A-1 , 10 \n"
                "A-1,10\n"
                "A-2,5\n",
                encoding="utf-8",
            )

            count = clean_csv(source, destination, "order_id")

            self.assertEqual(count, 2)
            lines = destination.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(lines[0], "order_id,amount")
            self.assertEqual(len(lines), 3)


if __name__ == "__main__":
    unittest.main()
