"""Regression tests for language dispatch and return-contract fixes."""
import unittest

from ovos_number_parser import (extract_number, is_fractional, is_ordinal,
                                 numbers_to_digits, pronounce_number)
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


class TestPronounceNaNGuard(unittest.TestCase):
    """NaN has no cardinal reading; every backend must reject it the same way.

    Before the guard each language crashed differently while formatting NaN:
    scientific formatting did ``"%E" % nan`` -> ``"NAN"`` and then raised
    ``ValueError: not enough values to unpack`` splitting the (absent) exponent,
    while cardinal formatting raised ``ValueError: cannot convert float NaN to
    integer``. The dispatcher now raises one deliberate ValueError instead.
    """

    NAN = float("nan")
    # a spread across the scientific-notation backends, the decimal-expansion
    # backends, and the Romance / RBNF fallbacks
    LANGS = ["en", "fa", "it", "ru", "ar", "de", "es", "ca", "pt", "eu", "kab"]

    def test_nan_raises_valueerror_plain(self):
        for lang in self.LANGS:
            with self.subTest(lang=lang):
                with self.assertRaises(ValueError):
                    pronounce_number(self.NAN, lang=lang)

    def test_nan_raises_valueerror_scientific(self):
        for lang in self.LANGS:
            with self.subTest(lang=lang):
                with self.assertRaises(ValueError):
                    pronounce_number(self.NAN, lang=lang, scientific=True)

    def test_nan_message_is_explicit(self):
        with self.assertRaises(ValueError) as ctx:
            pronounce_number(self.NAN, lang="en")
        self.assertIn("NaN", str(ctx.exception))

    def test_finite_numbers_unaffected(self):
        # the guard must not touch ordinary values, including scientific ones
        self.assertEqual(pronounce_number(5.0, lang="en"), "five")
        self.assertEqual(
            pronounce_number(1.5e10, lang="en", scientific=True),
            "one point five times ten to the power of ten")

    def test_infinity_still_localized(self):
        # inf is a distinct sentinel with a real spoken form; keep it working
        self.assertEqual(pronounce_number(float("inf"), lang="en"), "infinity")
        self.assertEqual(pronounce_number(float("-inf"), lang="en"),
                         "negative infinity")


if __name__ == "__main__":
    unittest.main()
