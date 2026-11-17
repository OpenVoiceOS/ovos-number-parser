import unittest

from ovos_number_parser.numbers_sk import (extract_number_sk,
                                           pronounce_number_sk)


class TestNegativeCompoundsk(unittest.TestCase):
    def test_negative_compound_roundtrip(self):
        # numtag reads separated words, so the round trip covers the values
        # the writer spells as separate words or as one short word
        for n in (-9, -21, -1000000):
            self.assertEqual(
                extract_number_sk(pronounce_number_sk(n)), n)

    def test_negative_compound_written_solid(self):
        expected = {-200: "mínus dvesto",
                    -1200: "mínus tisícdvesto",
                    -1234: "mínus tisícdvestotridsaťštyri"}
        for n, spoken in expected.items():
            with self.subTest(n=n):
                self.assertEqual(pronounce_number_sk(n), spoken)

    def test_signed_roundtrip_below_one_hundred(self):
        bad = []
        for n in range(0, 100):
            for m in (n, -n):
                if extract_number_sk(pronounce_number_sk(m)) != m:
                    bad.append(m)
        self.assertEqual(bad, [], f"round-trip failures: {bad[:10]}")


if __name__ == "__main__":
    unittest.main()
