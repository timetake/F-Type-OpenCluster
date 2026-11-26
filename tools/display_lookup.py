"""Look up an early F-TYPE center display identifier in published records."""

import argparse
import csv
import json
from pathlib import Path


CATALOG = Path(__file__).resolve().parents[1] / "docs" / "center-display-catalog.csv"
IDENTIFIERS = ("visual_number", "article_number", "part_number")


def normalized(number):
    return number.strip().replace("-", "").upper()


def lookup(number):
    key = normalized(number)
    with CATALOG.open(encoding="utf-8", newline="") as stream:
        return [
            row for row in csv.DictReader(stream)
            if any(row[field] and normalized(row[field]) == key for field in IDENTIFIERS)
        ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("number", help="complete display identifier, e.g. EX53-10E889-CF")
    records = lookup(parser.parse_args().number)
    print(json.dumps(records, indent=2))
    return 0 if records else 1


if __name__ == "__main__":
    raise SystemExit(main())
