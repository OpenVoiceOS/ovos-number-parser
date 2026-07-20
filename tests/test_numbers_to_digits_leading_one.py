"""Regression guard for a leading "one" before a scale word.

Multiplying a scale word by one leaves the value unchanged, so a purely
numeric comparison cannot tell that the multiplier is grammatically required.
The span builder used to stop after the "one" and emit two numbers
("one hundred and one" -> "1 101"). These assertions run through the PUBLIC
``numbers_to_digits`` entry point, which is where the defect surfaced; a
per-language guard would not have caught it.
"""
import unittest

from ovos_number_parser import numbers_to_digits


class TestLeadingOneBeforeScale(unittest.TestCase):
    # lang -> (spoken, expected)
    LEADING_ONE = {
        "en": [("one hundred and one dollars", "101 dollars"),
               ("one thousand and one", "1001"),
               ("one hundred", "100"),
               ("one million", "1000000")],
        "sv": [("ett hundra och ett kronor", "101 kronor")],
        "da": [("et hundrede og et kroner", "101 kroner")],
    }

    # multipliers other than one always worked; they must keep working
    CONTROLS = {
        "en": [("two hundred and one", "201"),
               ("twenty one", "21"),
               ("I have one dog", "I have 1 dog")],
    }

    # a number behind a connector is a SEPARATE number and must not be
    # absorbed into the preceding span, even when that span is "one"
    NOT_ABSORBED = {
        "en": [("one and three", "1 and 3")],
        "it": [("due e tre", "2 e 3"), ("uno e tre", "1 e 3")],
    }

    def test_leading_one_before_scale_word(self):
        for lang, cases in self.LEADING_ONE.items():
            for spoken, expected in cases:
                self.assertEqual(numbers_to_digits(spoken, lang), expected,
                                 f"{lang}: {spoken!r}")

    def test_other_multipliers_unchanged(self):
        for lang, cases in self.CONTROLS.items():
            for spoken, expected in cases:
                self.assertEqual(numbers_to_digits(spoken, lang), expected,
                                 f"{lang}: {spoken!r}")

    def test_connector_separated_numbers_stay_separate(self):
        for lang, cases in self.NOT_ABSORBED.items():
            for spoken, expected in cases:
                self.assertEqual(numbers_to_digits(spoken, lang), expected,
                                 f"{lang}: {spoken!r}")


if __name__ == "__main__":
    unittest.main()
