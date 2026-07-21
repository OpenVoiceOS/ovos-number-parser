import unittest

from ovos_number_parser.numbers_id import (extract_number_id,
                                           extract_number_ms)


class TestIndonesianMalayZeroDenominator(unittest.TestCase):
    """A written "N/0" must not raise ZeroDivisionError; valid fractions still
    parse."""

    def test_zero_denominator_does_not_raise(self):
        for extract in (extract_number_id, extract_number_ms):
            self.assertFalse(extract("1/0"))
            self.assertFalse(extract("5/0"))

    def test_valid_fractions_unchanged(self):
        for extract in (extract_number_id, extract_number_ms):
            self.assertEqual(extract("3/4"), 0.75)
            self.assertEqual(extract("1/2"), 0.5)


if __name__ == "__main__":
    unittest.main()
