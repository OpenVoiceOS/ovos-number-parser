import glob
import math
import os
import unittest

from ovos_number_parser import pronounce_number
from ovos_number_parser.numbers_kab import pronounce_number_kab

# every shipped language, derived from the numbers_*.py modules
_PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = sorted(
    os.path.basename(f)[len("numbers_"):-len(".py")]
    for f in glob.glob(os.path.join(_PKG, "ovos_number_parser", "numbers_*.py"))
)


class TestInfinity(unittest.TestCase):
    def test_localized_infinity_words(self):
        self.assertEqual(pronounce_number(float("inf"), "en"), "infinity")
        self.assertEqual(pronounce_number(float("-inf"), "en"),
                         "negative infinity")
        self.assertEqual(pronounce_number(float("inf"), "it"), "infinito")
        self.assertEqual(pronounce_number(float("-inf"), "it"), "meno infinito")
        self.assertEqual(pronounce_number(float("inf"), "de"), "unendlich")

    def test_english_default_for_unmapped_language(self):
        # eu and kab used to crash converting infinity to an integer
        self.assertEqual(pronounce_number(float("inf"), "eu"), "infinity")
        self.assertEqual(pronounce_number(float("-inf"), "kab"),
                         "negative infinity")

    def test_region_suffix_still_matches(self):
        self.assertEqual(pronounce_number(float("inf"), "pt-br"), "infinito")

    def test_infinity_never_crashes_any_language(self):
        for lang in LANGS:
            for value in (float("inf"), float("-inf")):
                with self.subTest(lang=lang, value=value):
                    out = pronounce_number(value, lang)
                    self.assertIsInstance(out, str)
                    self.assertTrue(out)


class TestHugeFiniteIntegers(unittest.TestCase):
    def test_beyond_scale_falls_back_to_scientific(self):
        # it previously raised IndexError on numbers past its named scale.
        # The connective is spoken in the target language, not in English.
        out = pronounce_number(10 ** 400, "it")
        self.assertIn("per dieci alla", out)
        self.assertIn("quattrocento", out)
        self.assertNotIn("times ten to the power of", out)

    def test_negative_huge_integer(self):
        # the sign rides on the mantissa, so each language speaks its own
        # minus word rather than an English "negative" prefix
        out = pronounce_number(-(10 ** 400), "it")
        self.assertTrue(out.startswith("meno "), out)
        self.assertNotIn("negative", out)

    def test_mantissa_pronounced_in_target_language(self):
        # Czech has no entry in _SCIENTIFIC_WORDS, so the connective falls
        # back to English while the mantissa and exponent stay Czech. This
        # pins the documented fallback, not a claim of Czech coverage.
        out = pronounce_number(2 ** 2000, "cs")
        self.assertIsInstance(out, str)
        self.assertIn("times ten to the power of", out)

    def test_representative_langs_never_crash_on_huge_int(self):
        for lang in ("en", "it", "eu", "cs", "pl", "ru", "de", "fr"):
            for value in (10 ** 400, 2 ** 2000):
                with self.subTest(lang=lang, value=value):
                    out = pronounce_number(value, lang)
                    self.assertIsInstance(out, str)

    def test_ordinary_numbers_unchanged(self):
        # the fallback must not touch in-range values
        self.assertEqual(pronounce_number(1234, "it"),
                         "milleduecentotrentaquattro")
        self.assertEqual(pronounce_number(10 ** 20, "en"),
                         "one hundred quintillion")


class TestKabyleDocumentedCeiling(unittest.TestCase):
    def test_finite_above_cap_still_raises(self):
        # Kabyle intentionally supports finite numbers only up to 9999
        with self.assertRaises(OverflowError):
            pronounce_number_kab(10 ** 400)
        with self.assertRaises(OverflowError):
            pronounce_number(10 ** 400, "kab")

    def test_infinity_bypasses_the_finite_cap(self):
        # infinity is not a finite-above-cap value; it must be spoken
        self.assertEqual(pronounce_number(float("inf"), "kab"), "infinity")


if __name__ == "__main__":
    unittest.main()
