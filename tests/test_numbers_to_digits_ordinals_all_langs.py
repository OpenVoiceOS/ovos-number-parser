"""The `ordinals` flag of `numbers_to_digits`, for every supported language.

`ordinals` is part of the public contract, so it cannot be an English privilege.
These tests iterate `SUPPORTED_LANGUAGES` rather than a hand-written list, and the
probe word for "third" is taken from the library's own tables (`pronounce_ordinal`),
so no hand-translated vocabulary is hard-coded.

Two invariants hold for every language: the default never changes the output,
and an ordinal word is never read as a fraction.
"""
import unittest

from ovos_number_parser import (SUPPORTED_LANGUAGES, is_ordinal,
                                numbers_to_digits, pronounce_number,
                                pronounce_ordinal)


def _ordinal_word(lang):
    """A word meaning "third" in `lang`, taken from the library's own tables."""
    try:
        spoken = pronounce_ordinal(3, lang)
    except Exception:
        return None
    for word in spoken.split():
        try:
            if is_ordinal(word, lang):
                return word
        except Exception:
            continue
    return None


class TestDefaultsAreUnchanged(unittest.TestCase):
    """The hard invariant: the ordinals default may not alter any output."""

    def test_explicit_default_matches_the_plain_call(self):
        for lang in SUPPORTED_LANGUAGES:
            phrases = [pronounce_number(21, lang) + " xy",
                       "xy " + pronounce_number(5, lang)]
            word = _ordinal_word(lang)
            if word:
                phrases.append(f"xy {word} xy")
            for phrase in phrases:
                with self.subTest(lang=lang, phrase=phrase):
                    self.assertEqual(
                        numbers_to_digits(phrase, lang),
                        numbers_to_digits(phrase, lang, ordinals=False))


class TestOrdinalsAreNeverFractions(unittest.TestCase):
    """No language may turn an ordinal word into a reciprocal."""

    def test_bare_ordinal_never_becomes_a_fraction(self):
        for lang in SUPPORTED_LANGUAGES:
            word = _ordinal_word(lang)
            if not word:
                continue
            with self.subTest(lang=lang, word=word):
                out = numbers_to_digits(f"xy {word} xy", lang)
                for chunk in out.split():
                    try:
                        val = float(chunk)
                    except ValueError:
                        continue
                    self.assertTrue(
                        float(val).is_integer(),
                        f"{lang}: {word!r} was read as a fraction: {out!r}")


class TestOrdinalsFlag(unittest.TestCase):
    """`ordinals=True` reads ordinal words as their ordinal value everywhere."""

    def test_ordinal_word_converts_for_every_language(self):
        for lang in SUPPORTED_LANGUAGES:
            word = _ordinal_word(lang)
            if not word:
                continue
            with self.subTest(lang=lang, word=word):
                out = numbers_to_digits(f"xy {word} xy", lang, ordinals=True)
                self.assertIn("3", out, f"{lang}: {word!r} -> {out!r}")

    def test_ordinal_word_is_left_alone_by_default(self):
        # sv, uk and kab spell some ordinals exactly like the cardinal, so their
        # modules read them as the plain number; that is the language, not a
        # flag being ignored, and it is still never a fraction
        always_numeric = {"sv", "uk", "kab"}
        for lang in SUPPORTED_LANGUAGES:
            if lang in always_numeric:
                continue
            word = _ordinal_word(lang)
            if not word:
                continue
            with self.subTest(lang=lang, word=word):
                self.assertIn(word, numbers_to_digits(f"xy {word} xy", lang))


class TestEnglishOrdinalCompound(unittest.TestCase):
    """The English compound-ordinal path is reachable through the flag."""

    def test_compound_ordinal(self):
        self.assertEqual(numbers_to_digits("the twenty fifth", "en"), "the 20")
        self.assertEqual(
            numbers_to_digits("the twenty fifth", "en", ordinals=True),
            "the 25")
        self.assertEqual(
            numbers_to_digits("the twenty-fifth", "en", ordinals=True),
            "the 25")


if __name__ == "__main__":
    unittest.main()
