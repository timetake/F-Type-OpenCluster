import csv
import hashlib
import json
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools import vbf_inventory as inventory


HEADER = (
    b'vbf_version = 2.2;\r\nheader {\r\n'
    b'// } sw_part_number = "WRONG";\r\n'
    b'description = {"test } //", "braces { and \\"quotes\\""};\r\n'
    b'/* } */ ranges = {{0, 4}, {8, 4}};\r\n'
    b'sw_part_number = "DEMO-A"; sw_part_type = EXE;\r\n}'
)


def block(address, data):
    return struct.pack(">II", address, len(data)) + data + b"\0\0"


SAMPLE = HEADER + block(0x0A000020, b"\xff\x00\xff") + block(0x20000000, b"abcd")


class InventoryTest(unittest.TestCase):
    def test_reads_nested_header_and_preserves_binary_whitespace(self):
        report = inventory.inspect(SAMPLE, {})
        self.assertEqual(report["header_part_number"], "DEMO-A")
        self.assertEqual(report["header_part_type"], "EXE")
        self.assertEqual(report["file_bytes"], len(SAMPLE))
        self.assertIsNone(report["catalog_part_number_by_sha256"])
        self.assertEqual([b["declared_address"] for b in report["blocks"]],
                         ["0x0A000020", "0x20000000"])
        self.assertEqual([b["stored_bytes"] for b in report["blocks"]], [3, 4])
        self.assertEqual(report["blocks"][1]["sha256"], hashlib.sha256(b"abcd").hexdigest())

    def test_exact_digest_controls_identity(self):
        catalog = {hashlib.sha256(SAMPLE).hexdigest(): "DEMO-A"}
        self.assertEqual(inventory.inspect(SAMPLE, catalog)["catalog_part_number_by_sha256"], "DEMO-A")
        changed = SAMPLE.replace(b"abcd", b"ABCD")
        self.assertIsNone(inventory.inspect(changed, catalog)["catalog_part_number_by_sha256"])

    def test_rejects_incomplete_or_unsupported_inputs(self):
        for data in (HEADER, SAMPLE[:-1], SAMPLE + b"\r\n",
                     SAMPLE.replace(b"2.2", b"1.0"), HEADER[:-1],
                     SAMPLE.replace(b"EXE;", b"EXE"), b"not a VBF"):
            with self.subTest(data=data[-24:]), self.assertRaises(ValueError):
                inventory.inspect(data, {})

    def test_catalog_has_distinct_valid_identifiers(self):
        with inventory.CATALOG.open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(len({r["part_number"] for r in rows}), len(rows))
        self.assertEqual(len({r["sha256"] for r in rows}), len(rows))
        for row in rows:
            self.assertRegex(row["sha256"], r"^[a-f0-9]{64}$")
            self.assertGreater(int(row["file_bytes"]), 0)

    def test_cli_returns_valid_reports_and_flags_failed_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            good = Path(tmp) / "renamed.vbf"
            bad = Path(tmp) / "incomplete.vbf"
            good.write_bytes(SAMPLE)
            bad.write_bytes(SAMPLE[:-1])
            cmd = [sys.executable, inventory.__file__, str(good)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            mixed = subprocess.run([*cmd, str(bad)], capture_output=True, text=True)
            self.assertEqual(mixed.returncode, 1)
            self.assertIn("incomplete.vbf", mixed.stderr)
            self.assertEqual(json.loads(result.stdout), json.loads(mixed.stdout))
            self.assertEqual(json.loads(mixed.stdout)[0]["file"], "renamed.vbf")
            self.assertEqual(good.read_bytes(), SAMPLE)


if __name__ == "__main__":
    unittest.main()
