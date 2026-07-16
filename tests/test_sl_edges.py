"""Edge-path tests for the Slovenian number module."""
import unittest

from ovos_number_parser.numbers_sl import (extract_number_sl, nice_number_sl,
                                           pronounce_number_sl)


class TestSlovenianEdges(unittest.TestCase):
    def test_decimal_digit_run_stops_at_word(self):
        self.assertEqual(extract_number_sl("pet celih dve mačke"), 5.2)

    def test_long_scale_pronounce(self):
        self.assertEqual(pronounce_number_sl(1000000, short_scale=False),
                         "milijon")

    def test_scientific(self):
        spoken = pronounce_number_sl(2e100, scientific=True)
        self.assertIn("krat deset na", spoken)

    def test_nice_number(self):
        self.assertEqual(nice_number_sl(0.5), "1 polovica")
        self.assertEqual(nice_number_sl(4.5, speech=False), "4 1/2")

    def test_declined_scale_words(self):
        self.assertEqual(extract_number_sl("pet milijonov"), 5000000)
        self.assertEqual(extract_number_sl("trije milijoni"), 3000000)

    def test_ordinal_pronounce_flag(self):
        self.assertEqual(pronounce_number_sl(3, ordinals=True), "tretji")
        self.assertEqual(pronounce_number_sl(21, ordinals=True),
                         "enaindvajseti")





class TestSlovenianPronounceLegacy(unittest.TestCase):
    """Anchors for the plural/declension branches of pronounce_number_sl."""

    def test_decimals(self):
        self.assertEqual(pronounce_number_sl(5.2), "pet celih dve")
        self.assertEqual(pronounce_number_sl(-5.2), "minus pet celih dve")
        self.assertEqual(pronounce_number_sl(2.5), "dve celi pet")

    def test_million_declension(self):
        self.assertEqual(pronounce_number_sl(2000000), "dve milijona")
        self.assertEqual(pronounce_number_sl(3000000), "tri milijoni")
        self.assertEqual(pronounce_number_sl(5000000), "pet milijonov")

    def test_long_scale(self):
        self.assertEqual(
            pronounce_number_sl(1000000000, short_scale=False), "milijarda")
        self.assertEqual(extract_number_sl("milijarda"), 1000000000)
        self.assertEqual(
            extract_number_sl("dva bilijona", short_scale=False),
            2000000000000)

    def test_large_composite_round_trip(self):
        for n in (1234567, 2000001, 100100100):
            spoken = pronounce_number_sl(n)
            self.assertEqual(extract_number_sl(spoken), n, spoken)


if __name__ == "__main__":
    unittest.main()
