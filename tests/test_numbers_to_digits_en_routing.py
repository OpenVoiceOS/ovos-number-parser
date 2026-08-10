"""English `numbers_to_digits` routing and correctness.

The public dispatcher must route English to the English implementation rather
than the generic fallback. The generic fallback mis-read compound ordinals as
arithmetic ("the twenty fifth" -> "the 20 0.2") and split hyphenated compounds
("nineteen ninety-nine" -> "19 90 - 9"). These tests pin the routed behaviour
and the two correctness fixes it depends on, using only the current public
signature (no keyword flags).
"""
import unittest

from ovos_number_parser import numbers_to_digits
from ovos_number_parser.numbers_en import numbers_to_digits_en


class TestEnglishDispatchRoute(unittest.TestCase):
    """English must reach numbers_to_digits_en, not the generic fallback."""

    def test_ordinal_compound_is_not_arithmetic(self):
        # the generic fallback turned the ordinal into the reciprocal 1/5
        self.assertEqual(numbers_to_digits("the twenty fifth", "en"), "the 20")

    def test_plain_sentences_unchanged(self):
        self.assertEqual(numbers_to_digits("two thousand and one", "en"), "2001")
        self.assertEqual(numbers_to_digits("one hundred and one degrees", "en"),
                         "101 degrees")
        self.assertEqual(numbers_to_digits("it was five days ago", "en"),
                         "it was 5 days ago")


class TestOrdinalWordsAreNeverReciprocals(unittest.TestCase):
    """An ordinal word must never be fabricated into a fraction."""

    def test_ordinal_left_alone_when_ordinals_off(self):
        self.assertEqual(numbers_to_digits_en("the twenty fifth"), "the 20")
        self.assertEqual(numbers_to_digits_en("the third week of june"),
                         "the third week of june")
        self.assertEqual(numbers_to_digits_en("march fifth"), "march fifth")

    def test_ordinal_parsed_when_asked(self):
        self.assertEqual(numbers_to_digits_en("the twenty fifth", ordinals=True),
                         "the 25")
        self.assertEqual(
            numbers_to_digits_en("the third week of june", ordinals=True),
            "the 3 week of june")

    def test_plural_denominators_are_still_fractions(self):
        # "fifths"/"thirds" are unambiguously denominators, unlike the singular
        self.assertEqual(numbers_to_digits_en("two fifths"), "0.4")
        self.assertEqual(numbers_to_digits_en("three quarters"), "0.75")


class TestHyphenatedCompounds(unittest.TestCase):
    """A hyphen inside a compound numeral spells a space, not a break."""

    def test_hyphen_does_not_split_the_number(self):
        self.assertEqual(numbers_to_digits("nineteen ninety-nine", "en"),
                         "19 99")
        self.assertEqual(numbers_to_digits("twenty-four hours", "en"),
                         "24 hours")
        self.assertEqual(numbers_to_digits("thirty-one days", "en"), "31 days")

    def test_hyphenated_ordinal(self):
        self.assertEqual(numbers_to_digits_en("the twenty-fifth", ordinals=True),
                         "the 25")

    def test_minus_sign_and_ranges_survive(self):
        self.assertEqual(numbers_to_digits_en("-5"), "-5.0")
        self.assertEqual(numbers_to_digits_en("10-15 people"), "10-15 people")


if __name__ == "__main__":
    unittest.main()
