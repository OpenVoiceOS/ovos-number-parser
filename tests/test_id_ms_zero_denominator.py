import unittest

from ovos_number_parser import extract_number


class TestIndonesianMalayZeroDenominator(unittest.TestCase):
    """A written "N/0" must not raise ZeroDivisionError; valid fractions still
    parse."""

    def test_zero_denominator_does_not_raise(self):
        for lang in ("id", "ms"):
            self.assertFalse(extract_number("1/0", lang))
            self.assertFalse(extract_number("5/0", lang))

    def test_valid_fractions_unchanged(self):
        for lang in ("id", "ms"):
            self.assertEqual(extract_number("3/4", lang), 0.75)
            self.assertEqual(extract_number("1/2", lang), 0.5)


if __name__ == "__main__":
    unittest.main()
