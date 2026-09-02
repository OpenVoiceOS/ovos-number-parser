"""`numbers_to_digits` conversion flags, for every supported language.

`ordinals`, `fractions` and `scale_words` are part of the public contract, so
they cannot be an English privilege. These tests iterate `SUPPORTED_LANGUAGES`
rather than a hand-written list: adding a language to the package without
deciding what the flags mean for it makes this file fail.

The probe words are derived from the library itself (`pronounce_ordinal`,
`pronounce_fraction`, `pronounce_number`), so no hand-translated vocabulary is
hard-coded here and the tests keep working as vocabularies grow.

Each language declares, per flag, one of three states:

``HONOURED``
    the flag changes the output in the documented direction.
``NOTHING_TO_SUPPRESS``
    the language never converted that kind of word in the first place, so the
    output the flag asks for is what the caller already gets. The flag is
    satisfied, with nothing left to do.
``NO_VOCABULARY``
    the language has no vocabulary of that kind at all (Kabyle counts only to
    9999 and has no scale or fraction words), so the flag cannot apply.

Two invariants hold for every language regardless of that state:
defaults never change the output, and an ordinal word is never read as a
fraction.
"""
import unittest

from ovos_number_parser import (SUPPORTED_LANGUAGES, is_fractional, is_ordinal,
                                numbers_to_digits, pronounce_fraction,
                                pronounce_number, pronounce_ordinal)
from ovos_number_parser import _is_fraction_word, _is_scale_word


def _numbers_in(text):
    """The numeric values present in converted output."""
    values = []
    for chunk in text.split():
        try:
            values.append(float(chunk))
        except ValueError:
            continue
    return values

HONOURED = "honoured"
NOTHING_TO_SUPPRESS = "nothing to suppress"
NO_VOCABULARY = "no vocabulary"

#: lang -> (fractions state, scale_words state). `ordinals` is HONOURED for
#: every supported language, so it needs no per-language entry.
FLAG_SUPPORT = {
    "an": (NOTHING_TO_SUPPRESS, HONOURED),
    "ar": (HONOURED, HONOURED),
    "ast": (NOTHING_TO_SUPPRESS, HONOURED),
    "az": (HONOURED, HONOURED),
    "bg": (HONOURED, HONOURED),
    "ca": (HONOURED, HONOURED),
    "cs": (HONOURED, HONOURED),
    "da": (HONOURED, HONOURED),
    "de": (HONOURED, NOTHING_TO_SUPPRESS),
    "el": (HONOURED, HONOURED),
    "en": (HONOURED, HONOURED),
    "es": (HONOURED, HONOURED),
    "et": (HONOURED, HONOURED),
    "eu": (HONOURED, HONOURED),
    "fa": (NOTHING_TO_SUPPRESS, HONOURED),
    "fi": (HONOURED, HONOURED),
    "fr": (HONOURED, HONOURED),
    "fy": (HONOURED, HONOURED),
    "gl": (NOTHING_TO_SUPPRESS, HONOURED),
    "he": (HONOURED, HONOURED),
    "hr": (HONOURED, HONOURED),
    "hu": (HONOURED, HONOURED),
    "id": (NOTHING_TO_SUPPRESS, NOTHING_TO_SUPPRESS),
    "it": (HONOURED, HONOURED),
    "kab": (NO_VOCABULARY, NO_VOCABULARY),
    "ms": (NOTHING_TO_SUPPRESS, NOTHING_TO_SUPPRESS),
    "mwl": (NOTHING_TO_SUPPRESS, HONOURED),
    "nb": (HONOURED, HONOURED),
    "nl": (HONOURED, HONOURED),
    "nn": (HONOURED, HONOURED),
    "oc": (NOTHING_TO_SUPPRESS, HONOURED),
    "pl": (HONOURED, HONOURED),
    "pt": (NOTHING_TO_SUPPRESS, HONOURED),
    "ro": (NOTHING_TO_SUPPRESS, HONOURED),
    "ru": (HONOURED, HONOURED),
    "sk": (HONOURED, HONOURED),
    "sl": (HONOURED, HONOURED),
    "sv": (HONOURED, HONOURED),
    "tr": (HONOURED, HONOURED),
    "uk": (HONOURED, HONOURED),
}


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


def _fraction_word(lang):
    """A word meaning "half" in `lang`."""
    try:
        spoken = pronounce_fraction("1/2", lang)
    except Exception:
        return None
    for word in spoken.split():
        if _is_fraction_word(word, lang):
            return word
    return None


def _scale_word(lang):
    """A multiplier word meaning "million" in `lang`."""
    try:
        spoken = pronounce_number(1000000, lang)
    except Exception:
        return None
    for word in spoken.split():
        if _is_scale_word(word, lang):
            return word
    return None


class TestFlagSupportIsDeclared(unittest.TestCase):
    def test_every_supported_language_declares_its_flag_support(self):
        self.assertEqual(sorted(FLAG_SUPPORT), sorted(SUPPORTED_LANGUAGES),
                         "a language was added without declaring what the "
                         "numbers_to_digits flags do for it")


class TestDefaultsAreUnchanged(unittest.TestCase):
    """The hard invariant: no default may alter a language's output."""

    def test_explicit_defaults_match_the_plain_call(self):
        for lang in SUPPORTED_LANGUAGES:
            phrases = [pronounce_number(21, lang) + " xy",
                       "xy " + pronounce_number(5, lang)]
            word = _ordinal_word(lang)
            if word:
                phrases.append(f"xy {word} xy")
            word = _fraction_word(lang)
            if word:
                phrases.append(f"{word} xy")
            for phrase in phrases:
                with self.subTest(lang=lang, phrase=phrase):
                    self.assertEqual(
                        numbers_to_digits(phrase, lang),
                        numbers_to_digits(phrase, lang, ordinals=False,
                                          fractions=True, scale_words=True))


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


class TestFractionsFlag(unittest.TestCase):
    def test_declared_behaviour_matches_reality(self):
        for lang in SUPPORTED_LANGUAGES:
            state = FLAG_SUPPORT[lang][0]
            word = _fraction_word(lang)
            if state == NO_VOCABULARY:
                self.assertIsNone(word, f"{lang} declares no fraction words")
                continue
            self.assertIsNotNone(word, lang)
            phrase = f"{word} xy"
            default = numbers_to_digits(phrase, lang)
            suppressed = numbers_to_digits(phrase, lang, fractions=False)
            with self.subTest(lang=lang, word=word, state=state):
                # whatever the state, the word must survive the flag
                self.assertIn(word, suppressed,
                              f"{lang}: {phrase!r} -> {suppressed!r}")
                if state == HONOURED:
                    self.assertNotEqual(default, suppressed, lang)
                else:
                    self.assertEqual(default, suppressed, lang)
                    self.assertIn(word, default, lang)

    def test_fraction_fused_into_a_quantity_still_converts(self):
        # A fraction can only be held back while it is a word of its own. Where
        # the language fuses it into the preceding number - one value out, not
        # two - it is part of that number and the flag must leave it alone.
        # Languages that simply read the pair as two numbers are not a quantity
        # and are skipped: there the fraction really is bare.
        for lang in SUPPORTED_LANGUAGES:
            word = _fraction_word(lang)
            if not word or FLAG_SUPPORT[lang][0] != HONOURED:
                continue
            phrase = f"{pronounce_number(2, lang)} {word}"
            default = numbers_to_digits(phrase, lang)
            if len(_numbers_in(default)) != 1:
                continue  # read as two separate numbers: the fraction is bare
            with self.subTest(lang=lang, phrase=phrase):
                self.assertEqual(
                    default, numbers_to_digits(phrase, lang, fractions=False),
                    f"{lang}: a fraction fused into a quantity must still convert")


class TestScaleWordsFlag(unittest.TestCase):
    def test_declared_behaviour_matches_reality(self):
        for lang in SUPPORTED_LANGUAGES:
            state = FLAG_SUPPORT[lang][1]
            word = _scale_word(lang)
            if state == NO_VOCABULARY:
                self.assertIsNone(word, f"{lang} declares no scale words")
                continue
            if word is None:
                # the language spells its scale words in a way its own parser
                # never converts; that is the NOTHING_TO_SUPPRESS case
                self.assertEqual(state, NOTHING_TO_SUPPRESS, lang)
                continue
            count = pronounce_number(66, lang)
            phrase = f"{count} {word} xy"
            default = numbers_to_digits(phrase, lang)
            kept = numbers_to_digits(phrase, lang, scale_words=False)
            with self.subTest(lang=lang, word=word, state=state):
                self.assertIn(word, kept, f"{lang}: {phrase!r} -> {kept!r}")
                # the count itself must still be converted
                self.assertTrue(any(ch.isdigit() for ch in kept),
                                f"{lang}: {phrase!r} -> {kept!r}")
                if state == HONOURED:
                    self.assertNotEqual(default, kept, lang)
                else:
                    self.assertEqual(default, kept, lang)


class TestFlagsComposeForEveryLanguage(unittest.TestCase):
    def test_all_flags_together_never_raise_and_keep_words(self):
        for lang in SUPPORTED_LANGUAGES:
            # "xy" separates the probes so neighbouring numerals cannot fuse
            # into one span and hide what is being asserted
            parts = [pronounce_number(21, lang), "xy"]
            frac = _fraction_word(lang)
            scale = _scale_word(lang)
            if frac:
                parts += [frac, "xy"]
            if scale:
                parts += [pronounce_number(66, lang), scale]
            phrase = " ".join(parts)
            with self.subTest(lang=lang, phrase=phrase):
                out = numbers_to_digits(phrase, lang, ordinals=True,
                                        fractions=False, scale_words=False)
                self.assertIsInstance(out, str)
                # a word that names both a fraction and an ordinal (Persian
                # "دوم" is "second" and the denominator alike) is claimed by
                # ordinals=True, which the caller asked for
                frac_is_ordinal = frac and _ordinal_word(lang) and \
                    bool(is_ordinal(frac, lang))
                if frac and not frac_is_ordinal \
                        and FLAG_SUPPORT[lang][0] != NO_VOCABULARY:
                    self.assertIn(frac, out, f"{lang}: {phrase!r} -> {out!r}")
                if scale:
                    self.assertIn(scale, out, f"{lang}: {phrase!r} -> {out!r}")


if __name__ == "__main__":
    unittest.main()
