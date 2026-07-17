"""Canonical short/long scale defaults for the top-level dispatch API.

A caller that passes no ``scale=`` must get the language's canonical
convention, not a hard-coded short scale. Short scale: 10^9 = "billion",
10^12 = "trillion". Long scale: 10^9 = "thousand million / milliard",
10^12 = "billion".

Conventions verified against Wikipedia "Long and short scales"
(https://en.wikipedia.org/wiki/Long_and_short_scales), which tabulates the
convention per language/country and cites the national language academies.
"""
import unittest

from ovos_number_parser import pronounce_number, extract_number
from ovos_number_parser.util import Scale


class TestCanonicalScaleWords(unittest.TestCase):
    # canonical 10^9 / 10^12 spoken word per language, from the source above.
    # LONG-scale languages say a "thousand-million" phrase or a dedicated
    # "milliard" word at 10^9 and reuse the "billion" cognate for 10^12.
    LONG = {
        "pt": ("mil milhões", "um bilião"),      # European Portuguese
        "mwl": ("mil milhones", "un bilion"),    # Mirandese
        "gl": ("mil millóns", "un billón"),      # Galician
        "cs": ("miliarda", "bilion"),            # Czech
        "sl": ("milijarda", "bilijon"),          # Slovene
        "sk": ("miliarda", "bilión"),            # Slovak
        "hr": ("milijarda", "bilijun"),          # Croatian
        "hu": ("egymilliárd", "egybillió"),      # Hungarian
        "pl": ("miliard", "bilion"),             # Polish
        "de": ("eine Milliarde", "eine Billion"),  # German
        "nl": ("één miljard", "één biljoen"),    # Dutch
        "sv": ("en miljard", "en biljon"),       # Swedish
        "da": ("en milliard", "en billion"),     # Danish
        "ro": ("un miliard", "un bilion"),       # Romanian
    }
    # SHORT-scale languages reach the "billion" cognate already at 10^9 and
    # the "trillion" cognate at 10^12.
    SHORT = {
        "pt-BR": ("um bilhão", "um trilhão"),    # Brazilian Portuguese
        "en": ("one billion", "one trillion"),
        "ru": ("миллиард", "триллион"),
        "tr": ("bir milyar", "bir trilyon"),
        "id": ("satu miliar", "satu triliun"),
        "az": ("bir milyard", "bir trilyon"),
        "bg": ("един милиард", "един трилион"),
    }

    def test_long_scale_default_words(self):
        for lang, (w9, w12) in self.LONG.items():
            with self.subTest(lang=lang):
                self.assertEqual(pronounce_number(10 ** 9, lang).strip(), w9)
                self.assertEqual(pronounce_number(10 ** 12, lang).strip(), w12)

    def test_short_scale_default_words(self):
        for lang, (w9, w12) in self.SHORT.items():
            with self.subTest(lang=lang):
                self.assertEqual(pronounce_number(10 ** 9, lang).strip(), w9)
                self.assertEqual(pronounce_number(10 ** 12, lang).strip(), w12)

    def test_round_trip_at_canonical_default(self):
        # pronounce -> extract returns the same value in both scale families,
        # with no scale argument on either call.
        roundtrip = {
            "pt": (10 ** 9, 10 ** 12), "pt-BR": (10 ** 9, 10 ** 12),
            "mwl": (10 ** 9, 10 ** 12), "gl": (10 ** 9, 10 ** 12),
            "cs": (10 ** 9, 10 ** 12), "sl": (10 ** 9, 10 ** 12),
            "sk": (10 ** 9, 10 ** 12), "hr": (10 ** 9, 10 ** 12),
            "hu": (10 ** 9, 10 ** 12), "pl": (10 ** 9, 10 ** 12),
            "de": (10 ** 9, 10 ** 12), "sv": (10 ** 9, 10 ** 12),
            "da": (10 ** 9, 10 ** 12), "ro": (10 ** 9, 10 ** 12),
            "en": (10 ** 9, 10 ** 12), "ru": (10 ** 9, 10 ** 12),
            "tr": (10 ** 9, 10 ** 12), "id": (10 ** 9, 10 ** 12),
            "az": (10 ** 9, 10 ** 12), "bg": (10 ** 9, 10 ** 12),
        }
        for lang, values in roundtrip.items():
            for n in values:
                with self.subTest(lang=lang, n=n):
                    spoken = pronounce_number(n, lang)
                    self.assertEqual(extract_number(spoken, lang), n)


class TestScaleOverrideStillHonoured(unittest.TestCase):
    """An explicit ``scale=`` overrides the canonical default in both directions."""

    def test_explicit_short_scale_on_long_language(self):
        # forcing short scale on European Portuguese reuses the "bilião"
        # cognate at 10^9
        self.assertEqual(
            pronounce_number(10 ** 9, "pt", scale=Scale.SHORT).strip(),
            "um bilião")
        self.assertEqual(
            extract_number("um bilião", "pt", scale=Scale.SHORT), 10 ** 9)

    def test_explicit_long_scale_on_short_language_pt_br(self):
        # forcing long scale on Brazilian Portuguese pushes "bilhão" out to 10^12
        self.assertEqual(
            pronounce_number(10 ** 9, "pt-BR", scale=Scale.LONG).strip(),
            "mil milhões")

    def test_deprecated_short_scale_flag_still_selects_scale(self):
        # the legacy boolean is honoured when no scale enum is given
        self.assertEqual(
            pronounce_number(10 ** 9, "pt", short_scale=True).strip(),
            "um bilião")
        self.assertEqual(
            pronounce_number(10 ** 9, "pt", short_scale=False).strip(),
            "mil milhões")


class TestShortScaleLanguagesUnchanged(unittest.TestCase):
    """The clean short-scale languages keep their pre-existing behaviour."""

    def test_english_unchanged(self):
        self.assertEqual(pronounce_number(10 ** 9, "en"), "one billion")
        self.assertEqual(pronounce_number(10 ** 12, "en"), "one trillion")
        self.assertEqual(extract_number("one billion", "en"), 10 ** 9)
        self.assertEqual(extract_number("one trillion", "en"), 10 ** 12)

    def test_russian_turkish_indonesian_unchanged(self):
        self.assertEqual(pronounce_number(10 ** 12, "ru"), "триллион")
        self.assertEqual(pronounce_number(10 ** 12, "tr"), "bir trilyon")
        self.assertEqual(pronounce_number(10 ** 12, "id"), "satu triliun")


if __name__ == "__main__":
    unittest.main()
