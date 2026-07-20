"""Backends that do not raise past their named scale must not speak nonsense.

`pronounce_number` guards values beyond a language's named-scale table, but the
guard was an exception handler, so it only ever rescued the languages whose
backend actually *raised* (Kabyle's OverflowError, Italian's IndexError).

Several backends fail differently: they return a value, so the guard never
fires and the caller receives it as a success. Two failure shapes were observed
on a 400-digit integer:

    pt  "doze mil quinhentos sextiliões vigintiliões vigintiliões vigintiliões"
    fr  "1250000000000000000000000 ... 000"   (the raw numeral, unread)

The first pads the magnitude by repeating the largest scale word it knows; the
second gives up and hands back digits. Both reach a TTS engine and are spoken.

The output of a large composed reading is now validated, and anything matching
those shapes falls back to the scientific reading instead.
"""
import unittest

from ovos_number_parser import pronounce_number
from ovos_number_parser import (_has_padded_scale_words,
                                _has_unread_digits)

#: languages that previously returned padded or unread output rather than
#: raising, plus the ones that raised, so the whole class is covered at once
LANGS = ["pt", "es", "fr", "de", "nl", "eu", "it", "en", "ca", "gl", "ro"]

#: a 400-digit integer: past every named-scale table in the library
HUGE = 10 ** 400 + 25 * 10 ** 398


class TestNoSilentGarbage(unittest.TestCase):

    #: languages with a localized connective, where a bare numeral is
    #: replaced by a real reading. Languages without one (fi, et) keep the
    #: numeral deliberately -- English glue would be worse than digits.
    LOCALIZED = ["pt", "es", "fr", "de", "nl", "it", "en", "ca", "gl", "ro"]

    def test_no_raw_digit_runs(self):
        """Digits in 'spoken' output mean the numeral was never read."""
        for lang in self.LOCALIZED:
            with self.subTest(lang=lang):
                out = pronounce_number(HUGE, lang)
                self.assertFalse(any(c.isdigit() for c in out),
                                 f"{lang} returned unread digits: {out[:60]!r}")

    def test_no_repeated_adjacent_scale_words(self):
        """No natural numeral repeats a scale word back to back."""
        for lang in LANGS:
            with self.subTest(lang=lang):
                words = pronounce_number(HUGE, lang).split()
                repeats = [a for a, b in zip(words, words[1:]) if a == b]
                self.assertEqual(repeats, [],
                                 f"{lang} padded with {repeats}")

    def test_reading_mentions_the_exponent(self):
        """The fallback is a scientific reading, so 400 must be spoken."""
        expected = {"pt": "quatrocentos", "es": "cuatrocientos",
                    "fr": "quatre cents", "it": "quattrocento",
                    "en": "four hundred", "de": "vierhundert"}
        for lang, word in expected.items():
            with self.subTest(lang=lang):
                self.assertIn(word, pronounce_number(HUGE, lang))

    def test_negative_huge_is_signed(self):
        for lang in LANGS:
            with self.subTest(lang=lang):
                out = pronounce_number(-HUGE, lang)
                self.assertNotEqual(out, pronounce_number(HUGE, lang))


class TestOrdinaryMagnitudesUnaffected(unittest.TestCase):
    """The validation must not divert numbers the backends read correctly."""

    CASES = [
        ("pt", 10 ** 18, "trilião"),
        ("fr", 10 ** 12, "billion"),
        ("de", 10 ** 9, "Milliarde"),
        ("en", 1234567, "million"),
        ("es", 10 ** 6, "millón"),
    ]

    def test_named_scales_still_used(self):
        for lang, value, word in self.CASES:
            with self.subTest(lang=lang, value=value):
                out = pronounce_number(value, lang)
                self.assertIn(word, out)
                self.assertNotIn("ten to the power", out)


class TestReadingValidator(unittest.TestCase):
    """Unit coverage for the validator, including why it is scoped.

    The repeated-word signal is only sound for a *composed* reading. A
    digit-by-digit rendering repeats words legitimately ("11" -> "um um"),
    which is why the caller applies the check only when digits ==
    FULL_NUMBER. Asserted here on the helper rather than through
    pronounce_number, because the digit-by-digit flag is not honoured by
    every backend.
    """

    def test_detects_padded_scale_words(self):
        self.assertTrue(_has_padded_scale_words(
            "doze mil quinhentos sextiliões vigintiliões vigintiliões"))
        self.assertTrue(_has_padded_scale_words("bostehun trilioi trilioi"))

    def test_detects_unread_digits(self):
        self.assertTrue(_has_unread_digits("125" + "0" * 400))

    def test_accepts_real_readings(self):
        for good in ("um vírgula vinte e cinco", "one million, two hundred"):
            self.assertFalse(_has_padded_scale_words(good))
            self.assertFalse(_has_unread_digits(good))
        # short digit groups are ordinary, e.g. a year
        self.assertFalse(_has_unread_digits("1984"))

    def test_digit_by_digit_shape_would_be_rejected(self):
        # exactly why the caller scopes the check to composed readings
        self.assertTrue(_has_padded_scale_words("um um dois"))


class TestKabyleCeilingPreserved(unittest.TestCase):
    """Kabyle's finite ceiling is a documented contract, not a bug."""

    def test_kab_still_raises_above_ceiling(self):
        with self.assertRaises(OverflowError):
            pronounce_number(HUGE, "kab")
