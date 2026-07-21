import unittest

from ovos_number_parser.numbers_az import (extract_number_az,
                                           pronounce_number_az)


class TestAzerbaijaniHundredsAfterThousand(unittest.TestCase):
    def test_bare_hundred_after_thousand_adds(self):
        self.assertEqual(extract_number_az("min yüz"), 1100)
        self.assertEqual(extract_number_az("iki min yüz"), 2100)

    def test_multiplier_uses_unchanged(self):
        self.assertEqual(extract_number_az("iki yüz"), 200)
        self.assertEqual(extract_number_az("yüz min"), 100000)
        self.assertEqual(extract_number_az("min"), 1000)

    def test_roundtrip_to_one_million(self):
        bad = []
        for n in list(range(0, 5000)) + list(range(5000, 1000001, 997)):
            if extract_number_az(pronounce_number_az(n)) != n:
                bad.append(n)
        self.assertEqual(bad, [], f"round-trip failures: {bad[:10]}")


if __name__ == "__main__":
    unittest.main()
