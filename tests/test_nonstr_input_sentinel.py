import unittest

from ovos_number_parser import extract_number, is_fractional

# every language that has an extractor wired into the dispatch
LANGS = ["en", "es", "pt", "de", "fr", "it", "nl", "ru", "ar", "fa", "pl",
         "sv", "fi", "el", "he", "hu", "sl", "ro", "ast", "oc", "an", "kab",
         "id", "ms", "tr", "sk", "hr", "bg", "cs", "uk", "az", "da", "ca",
         "gl", "eu", "et", "fy", "nb", "nn", "mwl"]


class TestNonStringInputSentinel(unittest.TestCase):
    def test_extract_number_returns_false_for_non_string(self):
        for lang in LANGS:
            for value in (None, 123, 1.5, [], {}, object()):
                self.assertIs(
                    extract_number(value, lang), False,
                    f"extract_number({value!r}, {lang!r}) should be False")

    def test_is_fractional_returns_false_for_non_string(self):
        for lang in LANGS:
            for value in (None, 123, [], {}):
                self.assertIs(
                    is_fractional(value, lang), False,
                    f"is_fractional({value!r}, {lang!r}) should be False")

    def test_empty_string_handled_gracefully(self):
        # an empty string carries no number and must not raise
        for lang in LANGS:
            self.assertFalse(extract_number("", lang))

    def test_zero_denominator_fraction_does_not_raise(self):
        # a spoken "1/0" must not raise ZeroDivisionError for languages that
        # route fractions through the shared look_for_fractions helper
        shared = [l for l in LANGS if l not in ("pl", "id", "ms")]
        for lang in shared:
            for text in ("1/0", "5/0", "1/0 apples"):
                self.assertFalse(extract_number(text, lang),
                                 f"extract_number({text!r}, {lang!r})")


if __name__ == "__main__":
    unittest.main()
