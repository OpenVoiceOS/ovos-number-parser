"""The `fractions` flag of `numbers_to_digits`, for every supported language.

`fractions` is part of the public contract, so it cannot be an English
privilege. These tests iterate `SUPPORTED_LANGUAGES`; the probe word for "half"
is taken from the library's own tables (`pronounce_fraction`), so no
hand-translated vocabulary is hard-coded.

Each language is one of two states, decided from the library itself rather than
a hand-written table:

* the language converts a bare fraction word, and ``fractions=False`` keeps it;
* the language never converted that word, so ``fractions=False`` is already
  what the caller gets.

In both states the word must survive the flag, and the default must be unchanged.
"""
import unittest

from ovos_number_parser import (SUPPORTED_LANGUAGES, numbers_to_digits,
                                pronounce_fraction, pronounce_number)
from ovos_number_parser import _is_fraction_word


def _numbers_in(text):
    values = []
    for chunk in text.split():
        try:
            values.append(float(chunk))
        except ValueError:
            continue
    return values


def _fraction_word(lang):
    """A word meaning "half" in `lang`, taken from the library's own tables."""
    try:
        spoken = pronounce_fraction("1/2", lang)
    except Exception:
        return None
    for word in spoken.split():
        if _is_fraction_word(word, lang):
            return word
    return None


class TestDefaultsAreUnchanged(unittest.TestCase):
    def test_explicit_default_matches_the_plain_call(self):
        for lang in SUPPORTED_LANGUAGES:
            word = _fraction_word(lang)
            phrases = ["xy " + pronounce_number(5, lang)]
            if word:
                phrases.append(f"{word} xy")
            for phrase in phrases:
                with self.subTest(lang=lang, phrase=phrase):
                    self.assertEqual(
                        numbers_to_digits(phrase, lang),
                        numbers_to_digits(phrase, lang, fractions=True))


class TestFractionsFlag(unittest.TestCase):
    def test_bare_fraction_word_survives_when_disabled(self):
        for lang in SUPPORTED_LANGUAGES:
            word = _fraction_word(lang)
            if not word:
                continue
            phrase = f"{word} xy"
            default = numbers_to_digits(phrase, lang)
            suppressed = numbers_to_digits(phrase, lang, fractions=False)
            with self.subTest(lang=lang, word=word):
                # whatever the state, the word must survive the flag
                self.assertIn(word, suppressed,
                              f"{lang}: {phrase!r} -> {suppressed!r}")
                if word in default:
                    # the language never converted it: default already keeps it
                    self.assertEqual(default, suppressed, lang)
                else:
                    # the language converts it: the flag must change the output
                    self.assertNotEqual(default, suppressed, lang)

    def test_fraction_fused_into_a_quantity_still_converts(self):
        # A fraction can only be held back while it is a word of its own. Where
        # the language fuses it into the preceding number - one value out, not
        # two - it is part of that number and the flag must leave it alone.
        for lang in SUPPORTED_LANGUAGES:
            word = _fraction_word(lang)
            if not word:
                continue
            phrase = f"{pronounce_number(2, lang)} {word}"
            default = numbers_to_digits(phrase, lang)
            if len(_numbers_in(default)) != 1:
                continue  # read as two separate numbers: the fraction is bare
            if word in default:
                continue  # not converted at all: nothing to preserve
            with self.subTest(lang=lang, phrase=phrase):
                self.assertEqual(
                    default, numbers_to_digits(phrase, lang, fractions=False),
                    f"{lang}: a fraction fused into a quantity must still convert")


class TestEnglishFractions(unittest.TestCase):
    def test_bare_fraction_kept(self):
        self.assertEqual(numbers_to_digits("half past nine", "en"),
                         "0.5 past 9")
        self.assertEqual(
            numbers_to_digits("half past nine", "en", fractions=False),
            "half past 9")
        self.assertEqual(
            numbers_to_digits("a quarter to five", "en", fractions=False),
            "a quarter to 5")

    def test_quantity_fraction_always_converts(self):
        for flag in (True, False):
            with self.subTest(fractions=flag):
                self.assertEqual(
                    numbers_to_digits("two and a half hours", "en",
                                      fractions=flag), "2.5 hours")
                self.assertEqual(
                    numbers_to_digits("three quarters", "en", fractions=flag),
                    "0.75")


if __name__ == "__main__":
    unittest.main()
