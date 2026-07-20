"""A hyphen, an underscore and a space are the same numeral separator.

"twenty-one", "twenty_one" and "twenty one" are the same number, and the
choice is a spelling convention that varies by language and by writer
(French hyphenates since the 1990 rectifications, Catalan writes
"vint-i-un", English allows either). Whichever the caller wrote, the value
must come out the same.

Only a separator between two LETTERS is rewritten: a leading "-" is a minus
sign, and a digit on either side means a range or a numeral glued to a word
("10-15", "10-segundos"), which must survive untouched.
"""
import unittest

from ovos_number_parser import extract_number, numbers_to_digits


class TestCompoundNumeralSeparators(unittest.TestCase):
    # lang -> (spellings that must agree, expected value)
    EQUIVALENT = [
        ("en", ["twenty-one", "twenty_one", "twenty one"], 21),
        ("en", ["thirty-four", "thirty_four", "thirty four"], 34),
        ("ca", ["vint-i-un", "vint i un"], 21),
        ("fr", ["quatre-vingt-dix", "quatre vingt dix"], 90),
        ("fr", ["vingt-et-un", "vingt et un"], 21),
        ("es", ["treinta-y-cuatro", "treinta y cuatro"], 34),
        ("pt", ["trinta-e-quatro", "trinta e quatro"], 34),
    ]
    # German (and the other solid-compound languages) write numerals as one
    # word - "einundzwanzig", never "einund-zwanzig" - so there is no separator
    # variant to normalise there and none is asserted.

    # a separator that is NOT between two letters keeps its meaning
    UNTOUCHED = [
        ("en", "-5", -5),        # minus sign
        ("es", "10-segundos", 10),  # numeral glued to a word: number still found
    ]

    def test_separators_are_equivalent(self):
        for lang, spellings, expected in self.EQUIVALENT:
            values = {s: extract_number(s, lang=lang) for s in spellings}
            for spelling, value in values.items():
                with self.subTest(lang=lang, spelling=spelling):
                    self.assertEqual(value, expected,
                                     f"{lang}: {spelling!r} -> {value!r}")

    def test_sign_and_glued_tokens_untouched(self):
        for lang, text, expected in self.UNTOUCHED:
            with self.subTest(lang=lang, text=text):
                self.assertEqual(extract_number(text, lang=lang), expected)

    def test_numbers_to_digits_handles_all_separators(self):
        self.assertEqual(numbers_to_digits("twenty-one seconds", "en"),
                         "21 seconds")
        self.assertEqual(numbers_to_digits("twenty_one seconds", "en"),
                         "21 seconds")
        self.assertEqual(numbers_to_digits("twenty one seconds", "en"),
                         "21 seconds")
        # a numeral glued to an ordinary word still keeps the word
        self.assertEqual(numbers_to_digits("10-segundos", "es"), "10-segundos")

    def test_hungarian_internal_hyphen_is_meaningful(self):
        # Hungarian spells numbers above two thousand with a hyphen at the
        # thousand boundary, so the separator is NOT interchangeable there and
        # must be left alone: rewriting it to a space loses the tail.
        self.assertEqual(extract_number("kétezer-ötszáz", lang="hu"), 2500)

    def test_natural_sentences(self):
        self.assertEqual(numbers_to_digits("I waited twenty-one minutes", "en"),
                         "I waited 21 minutes")
        self.assertEqual(
            numbers_to_digits("son les vint-i-un graus", "ca"),
            "son les 21 graus")


if __name__ == "__main__":
    unittest.main()
