import unittest

from ovos_number_parser.numbers_ca import (extract_number_ca,
                                           pronounce_number_ca)


class TestCatalanHundredsMultiplier(unittest.TestCase):
    def test_bare_hundred_after_thousand_adds(self):
        self.assertEqual(extract_number_ca("mil cent"), 1100)
        self.assertEqual(extract_number_ca("mil cent un"), 1101)
        self.assertEqual(extract_number_ca("dos mil cent"), 2100)

    def test_scale_multiplier_still_works(self):
        self.assertEqual(extract_number_ca("dos mil"), 2000)
        self.assertEqual(extract_number_ca("cent mil"), 100000)
        self.assertEqual(extract_number_ca("cent"), 100)
        self.assertEqual(extract_number_ca("dos-cents"), 200)

    def test_natural_sentence(self):
        self.assertEqual(
            extract_number_ca("necessito mil cent unitats"), 1100)

    def test_roundtrip_up_to_100000(self):
        bad = []
        for n in list(range(0, 3000)) + list(range(3000, 100001, 331)):
            if extract_number_ca(pronounce_number_ca(n)) != n:
                bad.append(n)
        self.assertEqual(bad, [], f"round-trip failures: {bad[:10]}")


if __name__ == "__main__":
    unittest.main()
