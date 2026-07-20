"""The caller's DigitPronunciation choice must reach the backend.

`DigitPronunciation` selects how the digits *after the decimal marker* are
read -- composed ("três vírgula catorze") or one at a time ("três vírgula um
quatro"). Integers have no decimal part, so the flag correctly does nothing
for them.

Several languages were dispatched through legacy wrappers whose signatures
have no `digits` parameter:

    return pronounce_number_es(number, places)

so the argument was accepted by the public API and then silently dropped --
along with `gender` and `ordinals`. Those languages run on the shared engine,
which supports all three, so the dispatcher now routes to the engine and
forwards them.

Language convention vs caller choice
------------------------------------
How the decimal part is read is a property of the *language*: Spanish and
Catalan read it digit by digit, Portuguese composes it. `digits=None` (the
default) means "use the language's convention", so routing through the engine
does not silently change what those languages say. An explicit argument always
wins over the convention -- that is the whole point of the parameter.
"""
import unittest

from ovos_number_parser import pronounce_number, DigitPronunciation

#: languages routed through the shared engine, which honours `digits`
ENGINE_LANGS = ["pt", "es", "ca", "gl"]


class TestExplicitChoiceIsHonoured(unittest.TestCase):

    def test_modes_differ(self):
        """The two modes must produce different readings of a decimal."""
        for lang in ENGINE_LANGS:
            with self.subTest(lang=lang):
                dbd = pronounce_number(1.25, lang,
                                       digits=DigitPronunciation.DIGIT_BY_DIGIT)
                full = pronounce_number(1.25, lang,
                                        digits=DigitPronunciation.FULL_NUMBER)
                self.assertNotEqual(dbd, full,
                                    f"{lang} ignored the digits argument")

    def test_digit_by_digit_reads_each_digit(self):
        """"25" after the marker is read as two separate digits."""
        expected = {"pt": "dois cinco", "es": "dos cinco",
                    "ca": "dos cinc", "gl": "dous cinco"}
        for lang, tail in expected.items():
            with self.subTest(lang=lang):
                out = pronounce_number(1.25, lang,
                                       digits=DigitPronunciation.DIGIT_BY_DIGIT)
                self.assertTrue(out.endswith(tail), out)

    def test_full_number_composes_the_tail(self):
        """"25" after the marker is read as the numeral twenty-five."""
        expected = {"pt": "vinte e cinco", "es": "veinticinco",
                    "ca": "vint-i-cinc", "gl": "vinte e cinco"}
        for lang, tail in expected.items():
            with self.subTest(lang=lang):
                out = pronounce_number(1.25, lang,
                                       digits=DigitPronunciation.FULL_NUMBER)
                self.assertTrue(out.endswith(tail), out)


class TestLanguageConventionIsTheDefault(unittest.TestCase):
    """Omitting the argument keeps each language's own convention."""

    def test_spanish_and_catalan_default_to_digit_by_digit(self):
        # documented in pronounce_number_es: "Decimals are read digit by digit"
        self.assertEqual(pronounce_number(3.14, "es"), "tres coma uno cuatro")
        self.assertEqual(pronounce_number(3.14, "ca"), "tres coma un quatre")

    def test_portuguese_defaults_to_composed(self):
        self.assertEqual(pronounce_number(1.25, "pt"),
                         "um vírgula vinte e cinco")

    def test_explicit_argument_overrides_the_convention(self):
        # Spanish reads digits one by one by default, but an explicit
        # FULL_NUMBER must still win
        self.assertEqual(pronounce_number(1.25, "es",
                                          digits=DigitPronunciation.FULL_NUMBER),
                         "uno coma veinticinco")


class TestIntegersUnaffected(unittest.TestCase):
    """No decimal part means nothing for the flag to change."""

    def test_integers_identical_in_both_modes(self):
        for lang in ENGINE_LANGS:
            for value in (7, 21, 1122, 1000000):
                with self.subTest(lang=lang, value=value):
                    self.assertEqual(
                        pronounce_number(value, lang,
                                         digits=DigitPronunciation.DIGIT_BY_DIGIT),
                        pronounce_number(value, lang,
                                         digits=DigitPronunciation.FULL_NUMBER))


class TestLegacyRoutedLanguagesStillCorrect(unittest.TestCase):
    """fr and it stay on the legacy path; their readings must not regress.

    The shared engine is not yet a replacement for either: it has no tens
    entry for French 70/80/90 (built by composition, "soixante-dix",
    "quatre-vingts") and it spaces Italian tens where they elide
    ("venti cinque" vs "venticinque"). Pinned so a future migration cannot
    land these regressions unnoticed.
    """

    def test_french_vigesimal_tens(self):
        self.assertEqual(pronounce_number(71, "fr"), "soixante-et-onze")
        self.assertEqual(pronounce_number(80, "fr"), "quatre-vingts")
        self.assertEqual(pronounce_number(21, "fr"), "vingt-et-un")

    def test_italian_elides_tens(self):
        self.assertEqual(pronounce_number(21, "it"), "ventuno")
        self.assertEqual(pronounce_number(25, "it"), "venticinque")
