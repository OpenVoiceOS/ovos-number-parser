"""Contract tests for RomanceNumberExtractor and the Galician wiring."""
import unittest

from ovos_number_parser import (extract_number, is_fractional, is_ordinal,
                                pronounce_fraction, pronounce_ordinal)


class TestDigitTokens(unittest.TestCase):
    def test_digits_extract(self):
        for lang in ("pt", "gl", "mwl", "ast"):
            self.assertEqual(extract_number("7", lang), 7, lang)
            self.assertEqual(extract_number("tengo 7 gatos", lang), 7, lang)
            self.assertEqual(extract_number("3,5", lang), 3.5, lang)

    def test_spoken_word_before_digit_wins(self):
        self.assertEqual(extract_number("dous gatos e 7 cans", "gl"), 2)


class TestIsOrdinalReturnsValue(unittest.TestCase):
    def test_value_not_bool(self):
        cases = [("pt", "terceiro", 3), ("gl", "segundo", 2),
                 ("mwl", "segundo", 2), ("ast", "terceru", 3)]
        for lang, word, expected in cases:
            val = is_ordinal(word, lang)
            self.assertEqual(val, expected, f"{lang} {word}")
            self.assertNotIsInstance(val, bool, f"{lang} {word}")

    def test_not_ordinal(self):
        self.assertFalse(is_ordinal("gato", "gl"))
        self.assertFalse(is_ordinal("gato", "pt"))


class TestGalicianWiring(unittest.TestCase):
    def test_pronounce_fraction(self):
        self.assertEqual(pronounce_fraction("2/3", "gl"), "dous terzos")
        self.assertEqual(pronounce_fraction("1/2", "gl"), "un medio")

    def test_pronounce_ordinal(self):
        self.assertEqual(pronounce_ordinal(1, "gl"), "primeiro")
        self.assertEqual(pronounce_ordinal(2, "gl"), "segundo")
        self.assertEqual(pronounce_ordinal(3, "gl"), "terceiro")

    def test_is_fractional(self):
        self.assertEqual(is_fractional("medio", "gl"), 0.5)
        self.assertFalse(is_fractional("can", "gl"))


if __name__ == "__main__":
    unittest.main()
