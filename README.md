# Data Automation Toolkit

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/dependencies-zero-success)
![Tests](https://img.shields.io/badge/tests-unittest-blue)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?logo=githubactions&logoColor=white)

A small, **dependency-free** Python toolkit for the boring-but-important parts of data work:

- **Clean CSV data** — normalise headers, trim whitespace, de-duplicate records
- **Load CSV into SQLite** — instantly queryable, no setup
- **Generate summary reports** — aggregated CSV plus a standalone HTML report you can open in any browser

Built to practise writing clean, testable, standard-library-only Python — the kind of automation that replaces manual spreadsheet work.

---

## Quick start

```bash
# No installation needed — Python 3.10+ and the standard library only.

# 1. Clean a messy CSV (de-duplicate by order_id)
python -m datatoolkit.cli clean data/sample_sales.csv reports/clean_sales.csv

# 2. Load it into SQLite and generate monthly summary reports
python -m datatoolkit.cli report data/sample_sales.csv

# 3. Open the generated report
#    reports/monthly_summary.html
```

### Example output

```
$ python -m datatoolkit.cli report data/sample_sales.csv
Loaded 5 rows into data/reports.db
Wrote reports/monthly_summary.csv and reports/monthly_summary.html
```

| month | orders | total |
| --- | --- | --- |
| 2026-01 | 2 | 200.5 |
| 2026-02 | 2 | 245.24 |
| 2026-03 | 1 | 60.0 |

---

## Features

| Command | What it does |
| --- | --- |
| `clean <source> <destination> --key order_id` | Normalises column names, trims values, removes duplicates (last record wins) |
| `report <source> --db data/reports.db --out-dir reports` | De-duplicates, creates a SQLite table from the CSV, then writes `monthly_summary.csv` + `monthly_summary.html` |

## Project structure

```
.
├── datatoolkit/
│   ├── __init__.py
│   ├── cli.py              # argparse command-line interface
│   ├── csv_cleaner.py      # normalise + de-duplicate CSV rows
│   ├── sqlite_report.py    # CSV → SQLite, monthly aggregation query
│   └── report_writer.py    # CSV and HTML report writers
├── data/
│   └── sample_sales.csv    # sample data with deliberate duplicates
├── tests/
│   ├── test_csv_cleaner.py
│   └── test_sqlite_report.py
└── .github/workflows/tests.yml
```

## Design notes

- **Zero dependencies** — runs anywhere Python 3.10+ runs; nothing to install or audit
- **Testable core** — pure functions in small modules, unit-tested with `unittest`
- **CI included** — GitHub Actions runs the test suite on Python 3.10 and 3.12
- **HTML reports are self-contained** — no CDN, no build step; open the file and it works

## Running the tests

```bash
python -m unittest discover -s tests -v
```

## Author

**HeiChan (Chan Hei Lun)** — BEng in Information Engineering, CUHK
[github.com/ChanHei419](https://github.com/ChanHei419)
