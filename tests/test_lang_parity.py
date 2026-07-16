"""Every supported language must provide every public function.

These tests guard against partial language support: a language listed in the
README must never raise NotImplementedError from any public entry point.
"""
import unittest

from ovos_number_parser import (extract_number, is_fractional, is_ordinal,
                                numbers_to_digits, pronounce_fraction,
                                pronounce_number, pronounce_ordinal)

LANGS = ["az", "ast", "ca", "cs", "da", "de", "en", "es", "eu", "fa", "fr",
         "gl", "hu", "it", "mwl", "nl", "pl", "pt", "ru", "sl", "sv", "uk"]


class TestLanguageParity(unittest.TestCase):
    def test_pronounce_number(self):
        for lang in LANGS:
            spoken = pronounce_number(7, lang)
            self.assertIsInstance(spoken, str, lang)
            self.assertTrue(spoken.strip(), lang)

    def test_pronounce_ordinal(self):
        for lang in LANGS:
            for n in (1, 2, 3, 10, 21):
                spoken = pronounce_ordinal(n, lang)
                self.assertIsInstance(spoken, str, f"{lang} {n}")
                self.assertTrue(spoken.strip(), f"{lang} {n}")

    def test_pronounce_fraction(self):
        for lang in LANGS:
            for frac in ("1/2", "3/4", "2/3", "3/2"):
                spoken = pronounce_fraction(frac, lang)
                self.assertIsInstance(spoken, str, f"{lang} {frac}")
                self.assertTrue(spoken.strip(), f"{lang} {frac}")

    def test_extract_number(self):
        for lang in LANGS:
            self.assertEqual(extract_number("7", lang), 7, lang)
            self.assertFalse(extract_number("xyzzy", lang), lang)

    def test_extract_pronounced_number(self):
        for lang in LANGS:
            for n in (2, 15, 21):
                spoken = pronounce_number(n, lang)
                self.assertEqual(extract_number(spoken, lang), n,
                                 f"{lang}: {spoken!r}")

    def test_is_fractional(self):
        for lang in LANGS:
            self.assertFalse(is_fractional("xyzzy", lang), lang)

    def test_is_ordinal(self):
        for lang in LANGS:
            self.assertFalse(is_ordinal("xyzzy", lang), lang)

    def test_is_ordinal_roundtrip(self):
        # native en/pt/mwl/ast/gl/de/da implementations only match single
        # words, so probe with a single-word ordinal
        for lang in LANGS:
            spoken = pronounce_ordinal(3, lang)
            self.assertEqual(is_ordinal(spoken, lang), 3,
                             f"{lang}: {spoken!r}")

    def test_numbers_to_digits(self):
        for lang in LANGS:
            spoken = pronounce_number(21, lang)
            converted = numbers_to_digits(f"{spoken} !", lang)
            self.assertIn("21", converted, f"{lang}: {spoken!r} -> {converted!r}")
            # text without numbers is returned intact
            self.assertEqual(
                numbers_to_digits("xyzzy grue", lang).strip(), "xyzzy grue")


class TestPronounceFractionAnchors(unittest.TestCase):
    """Hand-verified per-language fraction pronunciations."""
    ANCHORS = {
        "en": [("1/2", "one half"), ("3/4", "three quarters"),
               ("2/3", "two thirds"), ("3/2", "three halves"),
               ("1/4", "one quarter"), ("1/3", "one third")],
        "es": [("1/2", "un medio"), ("2/3", "dos tercios"),
               ("3/4", "tres cuartos")],
        "de": [("1/2", "ein halb"), ("2/3", "zwei drittel")],
        "fr": [("1/2", "un demi"), ("2/3", "deux tiers")],
        "it": [("1/2", "un mezzo"), ("2/3", "due terzi")],
        "cs": [("1/2", "polovina"), ("2/3", "dvě třetiny")],
        "pl": [("1/2", "jedna druga"), ("2/3", "dwie trzecie")],
        "ru": [("1/2", "половина"), ("2/3", "две трети")],
        "uk": [("1/2", "одна друга"), ("2/3", "дві треті")],
        "sl": [("1/2", "ena polovica"), ("2/3", "dve tretjini")],
        "hu": [("1/2", "fél"), ("2/3", "két harmad")],
        "sv": [("1/2", "en halv"), ("2/3", "två tredjedelar")],
        "da": [("1/2", "en halv")],
        "nl": [("1/2", "één half"), ("2/3", "twee derde")],
        "eu": [("1/2", "erdi bat"), ("2/3", "bi heren")],
        "fa": [("1/2", "یک دوم"), ("2/3", "دو سوم")],
        "ca": [("1/2", "un mig")],
        "az": [("1/2", "yarım"), ("2/3", "üçdə iki")],
        "pt": [("1/2", "um meio"), ("2/3", "dois terços")],
    }

    def test_anchors(self):
        for lang, pairs in self.ANCHORS.items():
            for frac, expected in pairs:
                self.assertEqual(pronounce_fraction(frac, lang), expected,
                                 f"{lang} {frac}")

    def test_negative_fraction(self):
        self.assertEqual(pronounce_fraction("-1/2", "en"), "minus one half")
        self.assertEqual(pronounce_fraction("1/-2", "en"), "minus one half")
        self.assertEqual(pronounce_fraction("-2/3", "de"),
                         "minus zwei drittel")

    def test_large_denominator_falls_back_to_ordinal(self):
        # out-of-table denominators: cardinal numerator + ordinal denominator
        self.assertEqual(pronounce_fraction("1/25", "en"),
                         "one twenty-fifths".replace("fifths", "fifth"))
        spoken = pronounce_fraction("3/25", "fr")
        self.assertTrue(spoken.startswith("trois "), spoken)

    def test_zero_denominator_raises(self):
        for lang in ("en", "de", "sl"):
            with self.assertRaises(Exception, msg=lang):
                pronounce_fraction("1/0", lang)


class TestPronounceOrdinalAnchors(unittest.TestCase):
    """Hand-verified ordinals for the newly wired languages."""
    ANCHORS = {
        "cs": [(1, "první"), (2, "druhý"), (21, "dvacátý první"),
               (45, "čtyřicátý pátý"), (100, "stý"), (200, "dvoustý"),
               (1000, "tisící")],
        "pl": [(1, "pierwszy"), (2, "drugi"), (21, "dwudziesty pierwszy"),
               (45, "czterdziesty piąty"), (100, "setny"), (200, "dwusetny"),
               (1000, "tysięczny")],
        "uk": [(1, "перший"), (2, "другий"), (21, "двадцять перший"),
               (100, "сотий"), (200, "двохсотий"), (1000, "тисячний")],
        "eu": [(1, "lehen"), (2, "bigarren"), (3, "hirugarren"),
               (4, "laugarren"), (5, "bosgarren"), (10, "hamargarren"),
               (20, "hogeigarren")],
        "fa": [(1, "اول"), (2, "دوم"), (3, "سوم"), (5, "پنجم"),
               (10, "دهم"), (20, "بیستم")],
        "sl": [(1, "prvi"), (2, "drugi"), (3, "tretji"), (10, "deseti"),
               (21, "enaindvajseti"), (100, "stoti")],
        "gl": [(1, "primeiro"), (2, "segundo"), (3, "terceiro")],
    }

    def test_anchors(self):
        for lang, pairs in self.ANCHORS.items():
            for n, expected in pairs:
                self.assertEqual(pronounce_ordinal(n, lang), expected,
                                 f"{lang} {n}")

    def test_invalid_ordinals_raise(self):
        for lang in ("cs", "pl", "uk", "eu", "fa"):
            with self.assertRaises(ValueError, msg=lang):
                pronounce_ordinal(0, lang)


class TestIsOrdinalAnchors(unittest.TestCase):
    def test_new_languages(self):
        cases = [
            ("cs", "druhý", 2), ("cs", "dvacátý první", 21),
            ("pl", "drugi", 2), ("pl", "dwudziesty pierwszy", 21),
            ("uk", "другий", 2), ("uk", "двадцять перший", 21),
            ("eu", "lehen", 1), ("eu", "bigarren", 2),
            ("fa", "اول", 1), ("fa", "دوم", 2),
            ("sl", "prvi", 1), ("sl", "enaindvajseti", 21),
            ("hu", "első", 1), ("hu", "második", 2), ("hu", "huszadik", 20),
            ("gl", "segundo", 2),
        ]
        for lang, word, expected in cases:
            self.assertEqual(is_ordinal(word, lang), expected,
                             f"{lang} {word}")

    def test_gender_variants(self):
        # generic reverse lookup registers both -o and -a final vowels
        self.assertEqual(is_ordinal("segundo", "es"), 2)
        self.assertEqual(is_ordinal("segunda", "es"), 2)
        self.assertEqual(is_ordinal("terzo", "it"), 3)
        self.assertEqual(is_ordinal("terza", "it"), 3)

    def test_not_ordinal(self):
        for lang, word in [("cs", "pes"), ("pl", "kot"), ("uk", "кіт"),
                           ("eu", "etxe"), ("fa", "خانه"), ("sl", "hiša"),
                           ("hu", "ház"), ("es", "casa"), ("it", "casa")]:
            self.assertFalse(is_ordinal(word, lang), f"{lang} {word}")


class TestNumbersToDigitsGeneric(unittest.TestCase):
    """The generic fallback used by eu, fa, fr, hu, it, sl and sv."""

    def test_in_sentence(self):
        cases = [
            ("fr", "j'ai vingt et un chats", "j'ai 21 chats"),
            ("it", "ho venticinque gatti", "ho 25 gatti"),
            ("sv", "jag har tjugofem katter", "jag har 25 katter"),
            ("eu", "hogeita bost etxe", "25 etxe"),
            ("hu", "huszonöt macska", "25 macska"),
            ("sl", "petindvajset mačk", "25 mačk"),
        ]
        for lang, text, expected in cases:
            self.assertEqual(numbers_to_digits(text, lang), expected,
                             lang)

    def test_trailing_punctuation_preserved(self):
        self.assertEqual(numbers_to_digits("ho venticinque gatti, ciao", "it"),
                         "ho 25 gatti, ciao")
        self.assertEqual(numbers_to_digits("vingt et un!", "fr"), "21!")

    def test_separate_numbers_not_merged(self):
        # "e"/"et" only joins when it extends the numeric value
        out = numbers_to_digits("due e tre", "it")
        self.assertIn("2", out)
        self.assertIn("3", out)


if __name__ == "__main__":
    unittest.main()
