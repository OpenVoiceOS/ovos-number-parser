"""Regression tests for language dispatch and return-contract fixes."""
import unittest

from ovos_number_parser import extract_number, is_fractional, is_ordinal, numbers_to_digits
from ovos_number_parser.numbers_es import nice_number_es


class TestDispatchFixes(unittest.TestCase):
    def test_nl_is_fractional_uses_dutch(self):
        # "derde" is Dutch for third; the Polish table does not know it
        self.assertAlmostEqual(is_fractional("derde", "nl"), 1 / 3)
        self.assertEqual(is_fractional("kwart", "nl"), 0.25)
        # Polish words must not leak into Dutch
        self.assertFalse(is_fractional("trzecie", "nl"))

    def test_da_extract_returns_false_not_none(self):
        self.assertIs(extract_number("hej med dig", "da"), False)

    def test_de_is_ordinal_returns_value(self):
        self.assertEqual(is_ordinal("dritte", "de"), 3)
        self.assertEqual(is_ordinal("einundzwanzigste", "de"), 21)
        self.assertFalse(is_ordinal("hund", "de"))

    def test_de_numbers_to_digits_compounds(self):
        self.assertEqual(numbers_to_digits("einundzwanzig katzen", "de"),
                         "21 katzen")
        self.assertEqual(
            numbers_to_digits("zweitausendfünfhundert euro", "de"),
            "2500 euro")

    def test_es_nice_number_pluralizes_tercios(self):
        self.assertEqual(nice_number_es(2 / 3), "2 tercios")
        self.assertEqual(nice_number_es(0.75), "3 cuartos")


if __name__ == "__main__":
    unittest.main()
