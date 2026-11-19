"""A number written in digits extracts with every digit and its sign.

A float holds 53 bits of mantissa, so reading "12000000000000000345" through
float() gives 12000000000000000000, and numbers_to_digits writes
"-1.2e+19" for "-12000000000000000345". A digit string is read with int()
instead. Every expected value is a Python integer literal or integer
arithmetic, never parser output.
"""
import sys
import unittest

from ovos_number_parser import extract_number, numbers_to_digits

LANGS = ["an", "ar", "ast", "az", "bg", "ca", "cs", "da", "de", "el", "en",
         "es", "et", "eu", "fa", "fi", "fr", "fy", "gl", "he", "hr", "hu",
         "id", "it", "kab", "ms", "mwl", "nb", "nl", "nn", "oc", "pl", "pt",
         "ro", "ru", "sk", "sl", "sv", "tr", "uk"]

BIG = 12 * 10 ** 18 + 345


class TestDigitStringsExtractExactly(unittest.TestCase):
    def test_above_float_precision(self):
        for lang in LANGS:
            for text, expected in (("12000000000000000345", BIG),
                                   ("-12000000000000000345", -BIG)):
                with self.subTest(lang=lang, text=text):
                    result = extract_number(text, lang)
                    self.assertEqual(result, expected)
                    self.assertIs(type(result), int)

    def test_minus_sign_is_kept(self):
        for lang in LANGS:
            with self.subTest(lang=lang):
                result = extract_number("-12", lang)
                self.assertEqual(result, -12)
                self.assertIs(type(result), int)

    def test_numbers_to_digits_keeps_every_digit(self):
        for lang in LANGS:
            for text in ("12000000000000000345", "-12000000000000000345"):
                with self.subTest(lang=lang, text=text):
                    self.assertEqual(numbers_to_digits(text, lang), text)


class TestDigitStringsBeyondFloatRange(unittest.TestCase):
    def test_danish_signed_run_beyond_float_range(self):
        self.assertEqual(extract_number("+" + "9" * 400, "da"),
                         10 ** 400 - 1)


class TestDigitStringsBeyondIntLimit(unittest.TestCase):
    """int() refuses a digit string longer than sys.get_int_max_str_digits()
    (4300 by default), and str() refuses to write such an int back. The
    string carries no usable number and extracts as the language's own
    no-number value."""

    def test_no_number_and_no_error(self):
        text = "9" * 5000
        for lang in LANGS:
            with self.subTest(lang=lang):
                self.assertEqual(extract_number(text, lang),
                                 extract_number("zzz", lang))
                self.assertEqual(numbers_to_digits(text, lang), text)

    def test_number_before_an_unreadable_run(self):
        self.assertEqual(extract_number("12 " + "9" * 5000, "sv"), 12)

    def test_raised_limit_reads_exactly(self):
        limit = sys.get_int_max_str_digits()
        sys.set_int_max_str_digits(0)
        try:
            for lang in LANGS:
                with self.subTest(lang=lang):
                    self.assertEqual(extract_number("9" * 5000, lang),
                                     10 ** 5000 - 1)
        finally:
            sys.set_int_max_str_digits(limit)


if __name__ == "__main__":
    unittest.main()
