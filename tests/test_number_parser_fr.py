import unittest

from ovos_number_parser.numbers_fr import _get_ordinal_fr, extract_number_fr


class TestNumberParserFr(unittest.TestCase):
    def test_extract_numeric_ordinals(self):
        self.assertEqual(_get_ordinal_fr("2nde"), 2)
        self.assertEqual(_get_ordinal_fr("5ième"), 5)
        self.assertEqual(_get_ordinal_fr("21ème"), 21)

    def test_extract_number_from_ordinal_phrase(self):
        self.assertEqual(extract_number_fr("la 2nde place", ordinals=True), 2)


if __name__ == "__main__":
    unittest.main()
