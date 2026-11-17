import unittest

from ovos_number_parser import extract_number, pronounce_number


class TestNegativeCompoundsk(unittest.TestCase):
    def test_negative_compound_roundtrip(self):
        for n in (-9, -21, -200, -1200, -1234, -999999, -1000000):
            self.assertEqual(
                extract_number(pronounce_number(n, "sk"), "sk"), n)

    def test_negative_compound_written_solid(self):
        expected = {-200: "mínus dvesto",
                    -1200: "mínus tisícdvesto",
                    -1234: "mínus tisícdvestotridsaťštyri"}
        for n, spoken in expected.items():
            with self.subTest(n=n):
                self.assertEqual(pronounce_number(n, "sk"), spoken)

    def test_signed_roundtrip_to_one_million(self):
        bad = []
        for n in list(range(0, 3000)) + list(range(3000, 1000001, 997)):
            for m in (n, -n):
                if extract_number(pronounce_number(m, "sk"), "sk") != m:
                    bad.append(m)
        self.assertEqual(bad, [], f"round-trip failures: {bad[:10]}")


if __name__ == "__main__":
    unittest.main()
