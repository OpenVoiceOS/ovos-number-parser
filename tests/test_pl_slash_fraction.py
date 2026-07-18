import unittest

from ovos_number_parser.numbers_pl import extract_number_pl


class TestPolishSlashFraction(unittest.TestCase):
    """A written "N/M" fraction must be extracted, not raise IndexError when
    it is the final token."""

    def test_bare_slash_fraction(self):
        self.assertEqual(extract_number_pl("3/4"), 0.75)
        self.assertEqual(extract_number_pl("1/2"), 0.5)
        self.assertEqual(extract_number_pl("0/5"), 0.0)

    def test_slash_fraction_in_sentence(self):
        self.assertEqual(extract_number_pl("mam 3/4 jabłka"), 0.75)


if __name__ == "__main__":
    unittest.main()
