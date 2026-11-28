"""German and Swedish cardinal spellings around "tausen"/"tusen"."""
import unittest

from ovos_number_parser import pronounce_number


class TestCardinalSpellings(unittest.TestCase):
    def test_german_ein_before_tausend(self):
        self.assertEqual(pronounce_number(101000, "de"),
                         "einhunderteintausend")
        self.assertEqual(pronounce_number(201000, "de"),
                         "zweihunderteintausend")
        self.assertEqual(pronounce_number(1000, "de"), "eintausend")

    def test_swedish_no_trailing_space_after_tusen(self):
        self.assertEqual(pronounce_number(1000, "sv"), "ettusen")
        self.assertEqual(pronounce_number(31000, "sv"),
                         "trettioettusen")
        self.assertEqual(pronounce_number(81000, "sv"),
                         "\u00e5ttioettusen")


if __name__ == "__main__":
    unittest.main()
