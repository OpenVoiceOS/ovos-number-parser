"""A numeral glued to an ordinary word by a hyphen must keep the word.

``extract_number`` deliberately finds a number *inside* a token, so
``extract_number("10-segundos", "es")`` is 10. ``numbers_to_digits`` used that
same test to decide whether a whole token was a number, so "10-segundos"
was replaced wholesale by "10" and the unit word disappeared — which broke
ovos-date-parser's ``extract_duration`` (it normalises through
``numbers_to_digits`` before matching the unit).

A hyphenated token only counts as one number when every part is itself a
numeral or a joiner, so genuine hyphenated numerals ("vint-i-un",
"quatre-vingt-dix") still convert. The bug was found in Spanish; these cases
sweep the whole supported set, since the token classifier is shared.
"""
import unittest

from ovos_number_parser import numbers_to_digits


class TestHyphenGluedTokens(unittest.TestCase):
    # numeral + hyphen + ordinary word -> the text must survive untouched
    GLUED = [
        ("es", "10-segundos"), ("ca", "10-segons"), ("fr", "10-secondes"),
        ("it", "10-secondi"), ("pt", "10-segundos"), ("gl", "10-segundos"),
        ("ro", "10-secunde"), ("an", "10-segundos"), ("oc", "10-segondas"),
        ("ast", "10-segundos"), ("mwl", "10-segundos"),
        ("en", "10-seconds"), ("de", "10-sekunden"), ("da", "10-sekunder"),
        ("sv", "10-sekunder"), ("nl", "10-seconden"), ("pl", "10-sekund"),
        ("ru", "10-секунд"), ("tr", "10-saniye"), ("fi", "10-sekuntia"),
    ]

    # genuine hyphenated numerals must still convert
    NUMERALS = [
        ("ca", "vint-i-un", "21"),
        ("fr", "quatre-vingt-dix", "90"),
        ("fr", "vingt-et-un", "21"),
    ]

    def test_glued_word_is_preserved(self):
        for lang, text in self.GLUED:
            with self.subTest(lang=lang):
                self.assertEqual(numbers_to_digits(text, lang), text,
                                 f"{lang}: {text!r} lost its word")

    def test_hyphenated_numerals_still_convert(self):
        for lang, text, expected in self.NUMERALS:
            with self.subTest(lang=lang):
                self.assertEqual(numbers_to_digits(text, lang), expected,
                                 f"{lang}: {text!r}")

    def test_glued_word_in_a_sentence(self):
        # the natural-language shape this surfaced in: a duration phrase
        self.assertEqual(numbers_to_digits("espera 10-segundos por favor", "es"),
                         "espera 10-segundos por favor")
        self.assertEqual(numbers_to_digits("attends 10-secondes", "fr"),
                         "attends 10-secondes")


if __name__ == "__main__":
    unittest.main()
