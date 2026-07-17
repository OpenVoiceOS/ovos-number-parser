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

    def test_scale_group_of_one_is_hyphenated(self):
        # above 2000 Hungarian hyphenates at every thousand-group boundary,
        # including when a million/billion group is exactly one
        cases = [
            (1000001, "egymillió-egy"),
            (1000100, "egymillió-száz"),
            (1234567, "egymillió-kétszázharmincnégyezer-ötszázhatvanhét"),
            (1001000, "egymillió-egyezer"),
            (2001001, "kétmillió-egyezer-egy"),
            (1000000001, "egymilliárd-egy"),
            (1001000000, "egymilliárd-egymillió"),
        ]
        for n, expected in cases:
            self.assertEqual(pronounce_number_hu(n), expected, n)

    def test_scale_group_of_one_still_bare_when_standalone(self):
        # a bare thousand/million group keeps no trailing hyphen or "egy"
        self.assertEqual(pronounce_number_hu(1000), "ezer")
        self.assertEqual(pronounce_number_hu(1500), "ezerötszáz")
        self.assertEqual(pronounce_number_hu(1000000), "egymillió")
        self.assertEqual(pronounce_number_hu(1000000000), "egymilliárd")

    def test_large_number_round_trip(self):
        from ovos_number_parser.numbers_hu import extract_number_hu
        for n in (1000001, 1001000, 1234567, 2001001, 1000000001,
                  1001000000):
            self.assertEqual(extract_number_hu(pronounce_number_hu(n)), n, n)

    def test_pronounce_ordinal_large(self):
        from ovos_number_parser.numbers_hu import pronounce_ordinal_hu
        self.assertEqual(pronounce_ordinal_hu(1000), "ezredik")
        self.assertEqual(pronounce_ordinal_hu(1000000), "egymilliomodik")


if __name__ == "__main__":
    unittest.main()
