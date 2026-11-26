import unittest

from tools.display_lookup import lookup


class DisplayLookupTest(unittest.TestCase):
    def test_label_retains_both_donor_records(self):
        rows = lookup("ex5310e889cf")
        self.assertEqual({r["part_number"] for r in rows}, {"T2R19384", "T2R20045E"})
        self.assertEqual(rows, lookup("EX53-10E889-CF"))

    def test_service_number_finds_direct_records_only(self):
        self.assertEqual({r["source_record"] for r in lookup("T2R19384")},
                         {"G-L2858336", "Jaguar Cary parts"})

    def test_partial_or_different_revision_has_no_match(self):
        for number in ("EX53-10E889", "EX53-10E889-AF", ""):
            with self.subTest(number=number):
                self.assertEqual(lookup(number), [])
