"""Inspect a local VBF 2.2 container and compare its digest with the catalog."""

import argparse
import csv
import hashlib
import json
import re
import struct
import sys
from pathlib import Path


CATALOG = Path(__file__).resolve().parents[1] / "docs" / "firmware-catalog.csv"
TOKEN = re.compile(
    rb'\s+|//[^\r\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|[A-Za-z0-9_.-]+|.',
    re.DOTALL,
)


def read_header(data):
    position = 0

    def token():
        nonlocal position
        while position < len(data):
            start = position
            match = TOKEN.match(data, start)
            value = match[0]
            position = match.end()
            if value.isspace() or value.startswith((b"//", b"/*")):
                continue
            if value == b'"' or (value == b"/" and data.startswith(b"/*", start)):
                raise ValueError(f"unterminated string or comment at byte {start}")
            return value
        raise ValueError("unexpected end of VBF header")

    def expect(value):
        if token() != value:
            raise ValueError(f"expected {value.decode()!r} near byte {position}")

    expect(b"vbf_version")
    expect(b"=")
    version = token().strip(b'"')
    if version != b"2.2":
        raise ValueError(f"unsupported VBF version {version!r} (expected 2.2)")
    expect(b";")
    expect(b"header")
    expect(b"{")
    fields = {}
    while (key := token()) != b"}":
        if not re.fullmatch(rb"[A-Za-z_][A-Za-z_0-9]*", key):
            raise ValueError(f"expected a header field near byte {position}")
        expect(b"=")
        depth = 0
        parts = []
        while True:
            value = token()
            if value == b";" and depth == 0:
                break
            if value == b"{":
                depth += 1
            elif value == b"}":
                if depth == 0:
                    raise ValueError(f"missing semicolon after {key!r}")
                depth -= 1
            parts.append(value)
        if key in (b"sw_part_number", b"sw_part_type"):
            if len(parts) != 1 or key in fields:
                raise ValueError(f"invalid or repeated {key.decode()}")
            fields[key] = parts[0].strip(b'"').decode("ascii")
    return position, fields


def inspect(data, catalog):
    offset, fields = read_header(data)
    blocks = []
    while offset < len(data):
        if len(data) - offset < 10:
            raise ValueError(f"incomplete block at byte {offset}")
        address, length = struct.unpack_from(">II", data, offset)
        end = offset + 8 + length
        if end + 2 > len(data):
            raise ValueError(f"truncated block at byte {offset} (declares {length} bytes)")
        blocks.append({
            "declared_address": f"0x{address:08X}",
            "stored_bytes": length,
            "sha256": hashlib.sha256(memoryview(data)[offset + 8:end]).hexdigest(),
        })
        offset = end + 2
    if not blocks:
        raise ValueError("container has no data blocks")
    digest = hashlib.sha256(data).hexdigest()
    return {
        "vbf_version": "2.2",
        "header_part_number": fields.get(b"sw_part_number"),
        "header_part_type": fields.get(b"sw_part_type"),
        "file_bytes": len(data),
        "sha256": digest,
        "catalog_part_number_by_sha256": catalog.get(digest),
        "blocks": blocks,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path, help="local VBF 2.2 files")
    args = parser.parse_args()
    with CATALOG.open(encoding="utf-8", newline="") as stream:
        catalog = {row["sha256"]: row["part_number"] for row in csv.DictReader(stream)}
    reports = []
    failed = False
    for path in args.files:
        try:
            reports.append({"file": path.name, **inspect(path.read_bytes(), catalog)})
        except (OSError, ValueError) as error:
            print(f"{path}: {error}", file=sys.stderr)
            failed = True
    print(json.dumps(reports, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
