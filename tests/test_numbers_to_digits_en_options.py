"""English number-to-digit conversion: routing, ordinals, and the caller knobs.

The public dispatcher routes English to the English implementation, which knows
about ordinals, hyphenated compounds and spoken fractions. This file pins that
routing, the values it produces, and the three keyword flags a downstream
date/time grammar needs: ``ordinals``, ``fractions`` and ``scale_words``. Every
flag defaults to today's behaviour, so the "defaults" tests double as a guard
against a future change quietly altering what existing callers see.
"""
import unittest

from ovos_number_parser import numbers_to_digits
from ovos_number_parser.numbers_en import numbers_to_digits_en


class TestEnglishDispatchRoute(unittest.TestCase):
    """English must reach numbers_to_digits_en, not the generic fallback."""

    def test_ordinal_compound_is_not_arithmetic(self):
        # the generic fallback read "the twenty fifth" as "the 20 0.2":
        # the ordinal was silently turned into the reciprocal 1/5
        self.assertEqual(numbers_to_digits("the twenty fifth", "en"),
                         "the 20")
        self.assertEqual(numbers_to_digits("the twenty fifth", "en",
                                           ordinals=True),
                         "the 25")

    def test_plain_sentences_unchanged(self):
        self.assertEqual(numbers_to_digits("two thousand and one", "en"), "2001")
        self.assertEqual(numbers_to_digits("one hundred and one degrees", "en"),
                         "101 degrees")
        self.assertEqual(numbers_to_digits("it was five days ago", "en"),
                         "it was 5 days ago")

    def test_flags_accepted_for_other_languages(self):
        # the flags are part of the public contract for every language;
        # the cross-language behaviour itself lives in
        # test_numbers_to_digits_flags_all_langs.py
        for lang in ("es", "de", "pt", "ru", "nl", "fr", "it"):
            with self.subTest(lang=lang):
                out = numbers_to_digits("veinte", lang, ordinals=True,
                                        fractions=False, scale_words=False)
                self.assertIsInstance(out, str)


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
        self.assertEqual(numbers_to_digits("the twenty-fifth", "en",
                                           ordinals=True), "the 25")

    def test_minus_sign_and_ranges_survive(self):
        self.assertEqual(numbers_to_digits_en("-5"), "-5.0")
        self.assertEqual(numbers_to_digits_en("10-15 people"), "10-15 people")


class TestFractionsFlag(unittest.TestCase):
    """``fractions=False`` keeps a bare fraction word as a word."""

    def test_default_converts_bare_fractions(self):
        self.assertEqual(numbers_to_digits("half past nine", "en"),
                         "0.5 past 9")
        self.assertEqual(numbers_to_digits("a quarter to five", "en"),
                         "a 0.25 to 5")

    def test_bare_fraction_kept_when_disabled(self):
        self.assertEqual(numbers_to_digits("half past nine", "en",
                                           fractions=False), "half past 9")
        self.assertEqual(numbers_to_digits("a quarter to five", "en",
                                           fractions=False), "a quarter to 5")

    def test_fraction_inside_a_quantity_still_converts(self):
        # here the fraction is part of the number, not a separate word
        for flag in (True, False):
            with self.subTest(fractions=flag):
                self.assertEqual(
                    numbers_to_digits("two and a half hours", "en",
                                      fractions=flag), "2.5 hours")
                self.assertEqual(
                    numbers_to_digits("three quarters", "en", fractions=flag),
                    "0.75")


class TestScaleWordsFlag(unittest.TestCase):
    """``scale_words=False`` converts the count and keeps the scale word."""

    def test_default_expands_scale_words(self):
        self.assertEqual(numbers_to_digits("66 million years ago", "en"),
                         "66000000 years ago")
        self.assertEqual(
            numbers_to_digits("sixty six million years ago", "en"),
            "66000000 years ago")
        self.assertEqual(numbers_to_digits("two thousand and one", "en"), "2001")

    def test_scale_word_kept_when_disabled(self):
        self.assertEqual(
            numbers_to_digits("66 million years ago", "en", scale_words=False),
            "66 million years ago")
        self.assertEqual(
            numbers_to_digits("sixty six million years ago", "en",
                              scale_words=False),
            "66 million years ago")
        self.assertEqual(
            numbers_to_digits("three hundred years ago", "en",
                              scale_words=False),
            "3 hundred years ago")
        # a compound spanning a scale word splits into its parts, by design
        self.assertEqual(
            numbers_to_digits("two thousand and one", "en", scale_words=False),
            "2 thousand and 1")


class TestFlagsCompose(unittest.TestCase):
    """The realistic downstream call passes all three flags together."""

    def setUp(self):
        self.kwargs = dict(ordinals=True, fractions=False, scale_words=False)

    def test_combined_call(self):
        cases = {
            "the twenty fifth of march": "the 25 of march",
            "half past nine": "half past 9",
            "a quarter to five": "a quarter to 5",
            "sixty six million years ago": "66 million years ago",
            "the third week of june": "the 3 week of june",
            "wake me in twenty-four hours": "wake me in 24 hours",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(
                    numbers_to_digits(text, "en", **self.kwargs), expected)

    def test_flags_are_independent(self):
        # turning one flag off must not change what the others do
        self.assertEqual(
            numbers_to_digits("half past nine", "en", scale_words=False),
            "0.5 past 9")
        self.assertEqual(
            numbers_to_digits("three hundred years ago", "en", fractions=False),
            "300 years ago")


class TestNotBugsGuard(unittest.TestCase):
    """Correct behaviour that has been mistaken for a bug before. Leave it."""

    def test_scale_expansion_is_correct_by_default(self):
        # a number utility spells out the value it was given; the caller that
        # wants the scale word kept asks for it with scale_words=False
        self.assertEqual(numbers_to_digits("66 million years ago", "en"),
                         "66000000 years ago")

    def test_year_and_offset_forms(self):
        self.assertEqual(numbers_to_digits("two thousand and one", "en"), "2001")
        self.assertEqual(numbers_to_digits("five days ago", "en"), "5 days ago")


if __name__ == "__main__":
    unittest.main()
