import unittest

from ovos_number_parser import extract_number

from ovos_number_parser.numbers_ca import pronounce_number_ca


class TestCatalanHundredsMultiplier(unittest.TestCase):
    def test_bare_hundred_after_thousand_adds(self):
        self.assertEqual(extract_number("mil cent", lang="ca"), 1100)
        self.assertEqual(extract_number("mil cent un", lang="ca"), 1101)
        self.assertEqual(extract_number("dos mil cent", lang="ca"), 2100)

    def test_scale_multiplier_still_works(self):
        self.assertEqual(extract_number("dos mil", lang="ca"), 2000)
        self.assertEqual(extract_number("cent mil", lang="ca"), 100000)
        self.assertEqual(extract_number("cent", lang="ca"), 100)
        self.assertEqual(extract_number("dos-cents", lang="ca"), 200)

    def test_natural_sentence(self):
        self.assertEqual(
            extract_number("necessito mil cent unitats", lang="ca"), 1100)

    def test_roundtrip_up_to_100000(self):
        bad = []
        for n in list(range(0, 3000)) + list(range(3000, 100001, 331)):
            if extract_number(pronounce_number_ca(n), lang="ca") != n:
                bad.append(n)
        self.assertEqual(bad, [], f"round-trip failures: {bad[:10]}")


if __name__ == "__main__":
    unittest.main()
