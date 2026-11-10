"""Digit input next to a fraction, a scale word or a sign extracts without
an exception, and the sign stays on the number it belongs to.

Every expected value is integer or Fraction arithmetic, a string written by
hand, or the reading of a second input that must agree, never the output of
the input under test.
"""
import unittest
from fractions import Fraction

from ovos_number_parser import extract_number, numbers_to_digits

LANGS = ["an", "ar", "ast", "az", "bg", "ca", "cs", "da", "de", "el", "en",
         "es", "et", "eu", "fa", "fi", "fr", "fy", "gl", "he", "hr", "hu",
         "id", "it", "kab", "ms", "mwl", "nb", "nl", "nn", "oc", "pl", "pt",
         "ro", "ru", "sk", "sl", "sv", "tr", "uk"]

SLAVIC = ["bg", "cs", "hr", "pl", "ru", "sk", "uk"]

#: languages whose extractors multiply a digit run by a scale word
MILLION = {"ar": "ملايين", "bg": "милион", "da": "million", "de": "Million",
           "en": "million", "eu": "milioi", "fy": "miljoen", "hr": "milijun",
           "nb": "million", "nl": "miljoen", "nn": "million", "pl": "milion",
           "ru": "миллион", "uk": "мільйон"}

#: the word each Romance vocabulary reads as the minus sign
ROMANCE_MINUS = {"an": "menos", "ast": "menos", "ca": "menys", "es": "menos",
                 "fr": "moins", "gl": "menos", "it": "meno", "mwl": "menos",
                 "oc": "mens", "pt": "menos", "ro": "minus"}


class TestDigitFractionNeverRaises(unittest.TestCase):
    def test_digits_then_fraction(self):
        for lang in LANGS:
            for digits in ("5", "12345678901234567890", "9" * 400):
                text = digits + " 1/2"
                with self.subTest(lang=lang, digits=len(digits)):
                    extract_number(text, lang)
                    numbers_to_digits(text, lang)

    def test_slavic_fraction_reads_as_its_decimal(self):
        # a digit fraction after a number reads as the decimal it equals
        # does: "5 1/2" like "5 0.5"
        for lang in SLAVIC:
            with self.subTest(lang=lang):
                self.assertEqual(extract_number("5 1/2", lang), Fraction(1, 2))
                self.assertEqual(extract_number("5 1/2", lang),
                                 extract_number("5 0.5", lang))
                self.assertEqual(numbers_to_digits("5 1/2", lang), "5 0.5")


class TestMixedNumber(unittest.TestCase):
    def test_sign_covers_the_whole_mixed_number(self):
        # -5 1/2 is -(5 + 1/2)
        for lang in ("da", "de", "nb", "nn"):
            with self.subTest(lang=lang):
                self.assertEqual(extract_number("5 1/2", lang), Fraction(11, 2))
                self.assertEqual(extract_number("-5 1/2", lang), Fraction(-11, 2))
                self.assertEqual(extract_number("minus 5 1/2", lang),
                                 Fraction(-11, 2))

    def test_whole_part_past_float_range(self):
        # the value has no float, so it is no number, as the digit string
        # "999...9.5" is none
        big = "9" * 400
        for lang in ("da", "de", "nb", "nn"):
            with self.subTest(lang=lang):
                self.assertEqual(extract_number(big + " 1/2", lang),
                                 extract_number("zzz", lang))
                self.assertFalse(extract_number(big + ".5", lang))


class TestValuePastIntStringLimit(unittest.TestCase):
    """str() refuses an integer with more than 4300 digits. A digit run and
    a scale word whose product passes that limit are no number."""

    def test_product_past_the_limit_is_no_number(self):
        text_of = "9" * 4300 + " {}"
        for lang, word in MILLION.items():
            text = text_of.format(word)
            with self.subTest(lang=lang):
                self.assertIs(extract_number(text, lang), False)
                out = numbers_to_digits(text, lang)
                self.assertIn(out, (text, "9" * 4300 + " " + str(10 ** 6)))

    def test_product_within_the_limit_is_exact(self):
        # bg, hr, ru and uk add a digit run larger than the scale word to it
        # instead of multiplying ("2000000 милион" = 3000000), so the
        # product is checked where it is formed
        for lang in sorted(set(MILLION) - {"bg", "hr", "ru", "uk"}):
            word = MILLION[lang]
            with self.subTest(lang=lang):
                self.assertEqual(extract_number("9" * 4290 + " " + word, lang),
                                 (10 ** 4290 - 1) * 10 ** 6)


class TestRomanceSigns(unittest.TestCase):
    def test_minus_word_before_digits(self):
        for lang, minus in ROMANCE_MINUS.items():
            with self.subTest(lang=lang):
                self.assertEqual(extract_number(minus + " 3", lang), -3)
                self.assertEqual(extract_number(minus + " 3,5", lang),
                                 Fraction(-7, 2))
                self.assertEqual(extract_number(minus + " 12345678901234567890", lang),
                                 -12345678901234567890)

    def test_minus_word_only_when_adjacent(self):
        # "menos de 3" is "fewer than 3", not -3
        self.assertEqual(extract_number("menos de 3", "pt"), 3)

    def test_leading_decimal_separator(self):
        for lang in ROMANCE_MINUS:
            with self.subTest(lang=lang):
                self.assertEqual(extract_number("-.5", lang), Fraction(-1, 2))
                self.assertEqual(extract_number(".5", lang), Fraction(1, 2))
                self.assertEqual(extract_number("-,5", lang), Fraction(-1, 2))


class TestDanishNorwegianSignedPart(unittest.TestCase):
    """A sign after a summed part opens the next number, as English reads
    "five and minus three" as 5."""

    def test_signed_part_is_a_new_number(self):
        self.assertEqual(extract_number("five and minus three", "en"), 5)
        for lang in ("da", "nb", "nn"):
            with self.subTest(lang=lang):
                self.assertEqual(extract_number("5 og -3", lang), 5)
                self.assertEqual(extract_number("fem og minus tre", lang), 5)
                self.assertEqual(numbers_to_digits("5 og -3", lang), "5 og -3")

    def test_leading_sign_still_covers_the_number(self):
        for lang in ("da", "nb"):
            with self.subTest(lang=lang):
                self.assertEqual(extract_number("minus fem og tyve", lang), -25)
                self.assertEqual(extract_number("-5 og 20", lang), -25)
                self.assertEqual(extract_number("5 og 3", lang), 8)


if __name__ == "__main__":
    unittest.main()
