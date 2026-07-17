import unittest

from ovos_number_parser.numbers_bg import (extract_number_bg,
                                           pronounce_number_bg)


class TestNegativeCompoundbg(unittest.TestCase):
    def test_negative_compound_roundtrip(self):
        for n in (-9, -21, -200, -1200, -1234, -999999, -1000000):
            self.assertEqual(
                extract_number_bg(pronounce_number_bg(n)), n)

    def test_signed_roundtrip_to_one_million(self):
        bad = []
        for n in list(range(0, 3000)) + list(range(3000, 1000001, 997)):
            for m in (n, -n):
                if extract_number_bg(pronounce_number_bg(m)) != m:
                    bad.append(m)
        self.assertEqual(bad, [], f"round-trip failures: {bad[:10]}")


if __name__ == "__main__":
    unittest.main()
