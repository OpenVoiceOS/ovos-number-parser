"""Edge-path tests for the Hungarian number module."""
import unittest

from ovos_number_parser.numbers_hu import (extract_number_hu,
                                           extract_numbers_hu,
                                           nice_number_hu,
                                           pronounce_number_hu)


class TestHungarianEdges(unittest.TestCase):
    def test_negative_fraction(self):
        self.assertAlmostEqual(
            extract_number_hu("mínusz két harmad"), -2 / 3)

    def test_bare_egesz_defaults_to_tenths(self):
        self.assertEqual(extract_number_hu("öt egész kettő"), 5.2)

    def test_non_number_compound_rejected(self):
        self.assertIsNone(
            __import__("ovos_number_parser.numbers_hu",
                       fromlist=["_parse_number_word_hu"]
                       )._parse_number_word_hu("macskaegér"))

    def test_extract_numbers(self):
        self.assertEqual(extract_numbers_hu("öt macska és három kutya"),
                         [5, 3])
        self.assertEqual(extract_numbers_hu("nincs itt szám"), [])

    def test_nice_number(self):
        self.assertEqual(nice_number_hu(4.5), "4 és fél")
        self.assertEqual(nice_number_hu(0.5), "fél")
        self.assertEqual(nice_number_hu(5), "5")
        self.assertEqual(nice_number_hu(4.5, speech=False), "4 1/2")

    def test_pronounce_decimals(self):
        self.assertEqual(pronounce_number_hu(5.2), "öt egész húsz század")
        self.assertEqual(pronounce_number_hu(5.2, places=1), "öt egész két tized")

    def test_pronounce_ordinal_large(self):
        from ovos_number_parser.numbers_hu import pronounce_ordinal_hu
        self.assertEqual(pronounce_ordinal_hu(1000), "ezredik")
        self.assertEqual(pronounce_ordinal_hu(1000000), "egymilliomodik")


if __name__ == "__main__":
    unittest.main()
