import unittest

from ovos_number_parser import extract_number


class TestPolishSlashFraction(unittest.TestCase):
    """A written "N/M" fraction must be extracted, not raise IndexError when
    it is the final token."""

    def test_bare_slash_fraction(self):
        self.assertEqual(extract_number("3/4", lang="pl"), 0.75)
        self.assertEqual(extract_number("1/2", lang="pl"), 0.5)
        self.assertEqual(extract_number("0/5", lang="pl"), 0.0)

    def test_slash_fraction_in_sentence(self):
        self.assertEqual(extract_number("mam 3/4 jabłka", lang="pl"), 0.75)


if __name__ == "__main__":
    unittest.main()
