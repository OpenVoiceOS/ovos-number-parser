import math
import unittest

from ovos_number_parser import extract_number

# every language that has an extractor wired into the dispatch
LANGS = ["en", "es", "pt", "de", "fr", "it", "nl", "ru", "ar", "fa", "pl",
         "sv", "fi", "el", "he", "hu", "sl", "ro", "ast", "oc", "an", "kab",
         "id", "ms", "tr", "sk", "hr", "bg", "cs", "uk", "az", "da", "ca",
         "gl", "eu", "et", "fy", "nb", "nn", "mwl"]

# pathological string tokens that overflow float() or parse to inf/nan
OVERFLOW_TOKENS = ["inf", "-inf", "nan", "1e309", "1e400", "9" * 400]


class TestOverflowStringSentinel(unittest.TestCase):
    def test_non_finite_string_tokens_never_raise(self):
        # a pathological string token must degrade to the "no number" sentinel
        # (or a finite parsed value) through the public API, never raise
        for lang in LANGS:
            for token in OVERFLOW_TOKENS:
                try:
                    result = extract_number(token, lang)
                except Exception as exc:  # pragma: no cover - failure path
                    self.fail(
                        f"extract_number({token!r}, {lang!r}) raised "
                        f"{type(exc).__name__}: {exc}")
                # whatever comes back must be either the False sentinel, an
                # exact integer (a huge digit string stays exact), or a finite
                # float - never a non-finite float such as inf or nan
                if isinstance(result, float):
                    self.assertTrue(
                        math.isfinite(result),
                        f"extract_number({token!r}, {lang!r}) returned a "
                        f"non-finite value {result!r}")

    def test_non_finite_with_trailing_words(self):
        # the same token embedded in a sentence must not raise either
        for lang in LANGS:
            for token in OVERFLOW_TOKENS:
                text = f"{token} apples"
                try:
                    extract_number(text, lang)
                except Exception as exc:  # pragma: no cover - failure path
                    self.fail(
                        f"extract_number({text!r}, {lang!r}) raised "
                        f"{type(exc).__name__}: {exc}")

    def test_finite_big_float_string_still_parses(self):
        # a huge but finite float string must keep parsing where the language
        # already did so - only the overflow/inf/nan path is guarded
        for lang in ("et", "fi", "hu", "sl", "da", "de", "nb", "nn"):
            result = extract_number("1e300", lang)
            self.assertIsNot(result, False)
            if isinstance(result, float):
                self.assertTrue(math.isfinite(result))


if __name__ == "__main__":
    unittest.main()
