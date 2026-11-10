"""Spoken and written numbers that extraction misread.

Every expected value is integer arithmetic, a float literal of the same
digits, or the reading of an independently computed number by
pronounce_number, never the output of the extractor under test.
"""
import re
import unittest
from decimal import Decimal
from fractions import Fraction

from ovos_number_parser import (extract_number, is_fractional,
                                numbers_to_digits, pronounce_number)
from ovos_number_parser.util import Scale


class TestEnglishDecimalBeforeScale(unittest.TestCase):
    """A scale word after the decimal digits multiplies the whole reading."""

    def test_short_scale(self):
        cases = [("one point five million", 15 * 10 ** 5),
                 ("one point five billion", 15 * 10 ** 8),
                 ("two point five trillion", 25 * 10 ** 11),
                 ("one point two five million", 125 * 10 ** 4),
                 ("one point zero five million", 105 * 10 ** 4),
                 ("one point twenty five million", 125 * 10 ** 4),
                 ("twelve point three four five billion", 12345 * 10 ** 6),
                 ("two point five thousand", 2500),
                 ("minus one point five million", -15 * 10 ** 5)]
        for text, expected in cases:
            with self.subTest(text=text):
                result = extract_number(text, "en")
                self.assertEqual(result, expected)
                self.assertIs(type(result), int)
                self.assertEqual(numbers_to_digits(text, "en"), str(expected))

    def test_long_scale(self):
        self.assertEqual(extract_number("one point five billion", "en",
                                        short_scale=False), 15 * 10 ** 11)

    def test_decimal_digits_are_exact(self):
        self.assertEqual(extract_number("one point one four", "en"), 1.14)
        self.assertEqual(extract_number("one point five", "en"), 1.5)

    def test_scale_words_multiply_together(self):
        self.assertEqual(extract_number("one point five thousand million",
                                        "en"), 15 * 10 ** 8)
        self.assertEqual(extract_number("one point five hundred thousand",
                                        "en"), 15 * 10 ** 4)

    def test_a_smaller_number_after_the_scale_adds(self):
        for text, expected in (
                ("two point five million three hundred", 25 * 10 ** 5 + 300),
                ("one point five million two thousand", 15 * 10 ** 5 + 2000),
                ("minus two point five million three hundred",
                 -(25 * 10 ** 5 + 300))):
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, "en"), expected)
                self.assertEqual(numbers_to_digits(text, "en"), str(expected))

    def test_oh_after_point_is_zero(self):
        for text, expected in (("one point oh five", "1.05"),
                               ("one point five oh five", "1.505"),
                               ("one point oh oh five", "1.005")):
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, "en"), float(expected))
                self.assertEqual(numbers_to_digits(text, "en"), expected)

    def test_point_needs_digits_directly_after_it(self):
        text = "at one point there were two million users"
        self.assertEqual(numbers_to_digits(text, "en"),
                         f"at 1 point there were {2 * 10 ** 6} users")
        self.assertEqual(extract_number(text, "en"), 1)


class TestGermanSpacedHundreds(unittest.TestCase):
    def test_hundreds_after_a_scale_word(self):
        cases = [("zwölf millionen dreihundert fünfundvierzig",
                  12 * 10 ** 6 + 345),
                 ("zwölf trillionen dreihundert fünfundvierzig",
                  12 * 10 ** 18 + 345),
                 ("zwölf tausend dreihundert fünfundvierzig", 12345),
                 ("eine Million dreihundert zwei Tausend",
                  10 ** 6 + 302 * 1000)]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, "de"), expected)

    def test_capitalised_scale_nouns_convert(self):
        for x in (12 * 10 ** 6 + 345, 2 * 10 ** 9 + 7, 12 * 10 ** 18 + 345):
            spoken = pronounce_number(x, "de")
            with self.subTest(spoken=spoken):
                self.assertEqual(numbers_to_digits(spoken, "de"), str(x))
        self.assertEqual(numbers_to_digits(
            "er zahlte zwölf Millionen dreihundert fünfundvierzig Euro",
            "de"), f"er zahlte {12 * 10 ** 6 + 345} Euro")

    def test_capitalised_nouns_without_a_count_stay_text(self):
        for text in ("Er hat es außer Acht gelassen", "Nimm dich in Acht",
                     "Der Elf Legolas", "Tausend Dank",
                     "Millionen Menschen protestierten"):
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, "de"), text)

    def test_capitalised_fraction_nouns_need_a_count(self):
        for text, expected in (("ein Viertel", Fraction(1, 4)),
                               ("drei Viertel", Fraction(3, 4)),
                               ("zwei Drittel", Fraction(2, 3))):
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, "de"),
                                 str(float(expected)))
        for text in ("das erste Viertel", "Er wohnt im Viertel"):
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, "de"), text)

    def test_clock_time_keeps_its_rewrite(self):
        self.assertEqual(numbers_to_digits("um 07.30 Uhr", "de"),
                         "um 07:30 Uhr")

    def test_decimal_digits_are_exact(self):
        for text in ("eins komma eins vier null", "eins Komma eins vier null"):
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, "de"), "1.14")
        self.assertEqual(extract_number("minus eins komma eins vier", "de"),
                         -1.14)


class TestDigitGroups(unittest.TestCase):
    """"." groups thousands where the decimal mark is the comma."""

    GROUPED = ["pt", "pt-PT", "pt-BR", "it", "ca", "ro", "ast", "id"]

    def test_grouped_digits(self):
        for lang in self.GROUPED:
            for text, expected in (("12.000", 12000),
                                   ("1.234.567", 1234567),
                                   ("-12.000", -12000),
                                   ("custa 12.000 euros", 12000),
                                   ("12.000,5", 12000.5)):
                with self.subTest(lang=lang, text=text):
                    self.assertEqual(extract_number(text, lang), expected)

    def test_decimal_comma(self):
        for lang in self.GROUPED + ["ms", "es", "fr", "gl"]:
            with self.subTest(lang=lang):
                self.assertEqual(extract_number("8,5", lang), 8.5)

    def test_malay_comma_groups(self):
        self.assertEqual(extract_number("1,000", "ms"), 1000)
        self.assertEqual(extract_number("1,234.5", "ms"), 1234.5)

    def test_point_decimal_without_groups(self):
        # three digits after the point are a group only when the language
        # groups with the point; a shorter or longer tail stays a decimal
        for lang in self.GROUPED:
            with self.subTest(lang=lang):
                self.assertEqual(extract_number("3.14159", lang), 3.14159)
                self.assertEqual(extract_number("1.5", lang), 1.5)

    def test_a_group_never_starts_with_zero(self):
        for lang in self.GROUPED:
            for text, expected in (("0.500", 0.5), ("-0.500", -0.5),
                                   ("0.050", 0.05), ("1.5", 1.5),
                                   ("12.000", 12000),
                                   ("1.234.567", 1234567)):
                with self.subTest(lang=lang, text=text):
                    self.assertEqual(extract_number(text, lang), expected)
        for lang in ("it", "ca"):
            with self.subTest(lang=lang):
                self.assertEqual(numbers_to_digits("0.500", lang), "0.5")
        self.assertEqual(extract_number("0,500", "ms"), 0.5)

    def test_commas_that_are_no_group_separate_numbers(self):
        for lang in ("id", "ms"):
            with self.subTest(lang=lang):
                self.assertEqual(extract_number("1,2,3", lang), 1)
        self.assertEqual(extract_number("12,000,000", "id"), 12)
        self.assertEqual(extract_number("12,000,000", "ms"), 12 * 10 ** 6)
        self.assertEqual(extract_number("100,000.25", "id"), 100)


class TestRomanceDecimalAboveFloatPrecision(unittest.TestCase):
    BIG = 12 * 10 ** 18 + 345

    def test_whole_part_keeps_its_digits(self):
        for lang in ("pt", "es", "fr", "it", "ca", "gl", "ro", "an", "ast",
                     "mwl", "oc", "id", "ms"):
            for text, expected in (("12000000000000000345,25", self.BIG),
                                   ("-12000000000000000345,25", -self.BIG),
                                   ("12000000000000000345,5", self.BIG + 1)):
                with self.subTest(lang=lang, text=text):
                    self.assertEqual(extract_number(text, lang), expected)


class TestFrenchExponentIsNoOrdinal(unittest.TestCase):
    def test_exponent_strings(self):
        none = extract_number("zzz", "fr")
        for text in ("1e309", "1e5", "5e3"):
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, "fr"), none)
                self.assertFalse(is_fractional(text, "fr"))

    def test_ordinal_suffixes_still_read(self):
        self.assertEqual(extract_number("2e", "fr"), 2)
        self.assertEqual(is_fractional("3ième", "fr"), 1 / 3)


class TestHyphenatedRomanceNumbers(unittest.TestCase):
    def test_numbers_to_digits(self):
        cases = [("pt", "vinte-e-dois", 20 + 2),
                 ("gl", "vinte-e-dous", 20 + 2),
                 ("oc", "trenta-e-dos", 30 + 2),
                 ("ro", "douăzeci-și-unu", 20 + 1)]
        for lang, text, expected in cases:
            with self.subTest(lang=lang):
                self.assertEqual(numbers_to_digits(text, lang), str(expected))
        self.assertEqual(numbers_to_digits("vinte-e-dois gatos", "pt"),
                         "22 gatos")

    def test_a_chain_without_a_joiner_is_no_sum(self):
        for lang, text, numbers in (("ro", "au venit doi-trei oameni", [2, 3]),
                                    ("ro", "vreo cinci-șase zile", []),
                                    ("pt", "zero-zero", [0, 0]),
                                    ("pt", "cinco-cinco", [5, 5])):
            with self.subTest(lang=lang, text=text):
                digits = re.findall(r"\d+", numbers_to_digits(text, lang))
                self.assertEqual([int(d) for d in digits], numbers)


class TestHungarianDecimalRoundTrip(unittest.TestCase):
    def test_every_denominator(self):
        for places in range(1, 25):
            for numerator in (1, 7, 2500, 10 ** places - 1):
                if numerator >= 10 ** places:
                    continue
                for whole in (0, 3):
                    x = float(Decimal(whole)
                              + Decimal(numerator) / 10 ** places)
                    spoken = pronounce_number(x, "hu", places=places)
                    with self.subTest(spoken=spoken):
                        self.assertEqual(extract_number(spoken, "hu"), x)


class TestDutchOrdinalTable(unittest.TestCase):
    def test_ordinals(self):
        for word, expected in (("honderdste", 100),
                               ("miljoenste", 10 ** 6),
                               ("triljardste", 10 ** 21)):
            with self.subTest(word=word):
                self.assertEqual(extract_number(word, "nl", ordinals=True),
                                 expected)
                self.assertEqual(is_fractional(word, "nl"), 1 / expected)


class TestSlavicPluralScaleWords(unittest.TestCase):
    def test_czech(self):
        cases = [("dvanáct milionů", 12 * 10 ** 6),
                 ("dva miliony", 2 * 10 ** 6),
                 ("pět miliard", 5 * 10 ** 9),
                 ("dvě miliardy", 2 * 10 ** 9),
                 ("dvanáct trilionů tři sta čtyřicet pět",
                  12 * 10 ** 18 + 345)]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, "cs"), expected)

    def test_czech_short_scale(self):
        # "milion" and "miliarda" have one value in both scales
        for text, expected in (("dvanáct milionů", 12 * 10 ** 6),
                               ("dvě miliardy", 2 * 10 ** 9)):
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, "cs",
                                                scale=Scale.SHORT), expected)
                self.assertEqual(extract_number(text, "cs", ordinals=True),
                                 expected)

    def test_slovak(self):
        cases = [("dvanásť triliónov", 12 * 10 ** 18),
                 ("tri trilióny", 3 * 10 ** 18),
                 ("päť triliárd", 5 * 10 ** 21),
                 ("dve triliardy", 2 * 10 ** 21),
                 ("dvanásť kvadriliónov", 12 * 10 ** 24),
                 ("dvanásť triliónov tristo štyridsaťpäť",
                  12 * 10 ** 18 + 345)]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, "sk"), expected)


class TestScaleAfterScaleRoundTrip(unittest.TestCase):
    """A larger scale word multiplies the number before it, as the
    pronunciation writes it ("dua belas juta triliun")."""

    VALUES = [10 ** 15, 10 ** 18, 12 * 10 ** 18 + 345,
              123456 * 10 ** 12 + 789, 1001 * 10 ** 12]

    def test_round_trip(self):
        for lang in ("id", "ms", "ar", "he", "oc"):
            for x in self.VALUES:
                spoken = pronounce_number(x, lang)
                with self.subTest(lang=lang, spoken=spoken):
                    self.assertEqual(extract_number(spoken, lang), x)

    def test_romance_scale_after_scale(self):
        cases = [("es", "doce millones de billones", 12 * 10 ** 6 * 10 ** 12),
                 ("pt", "doze milhões de biliões", 12 * 10 ** 6 * 10 ** 12),
                 ("ca", "dotze milions de bilions", 12 * 10 ** 6 * 10 ** 12),
                 ("it", "dodici milioni di miliardi", 12 * 10 ** 6 * 10 ** 9)]
        for lang, text, expected in cases:
            with self.subTest(lang=lang, text=text):
                self.assertEqual(extract_number(text, lang), expected)

    def test_and_adds_a_larger_scale(self):
        # "و" and "ו" join two numbers by addition
        cases = [("ar", "ألفان ومليون", 2 * 1000 + 10 ** 6),
                 ("ar", "خمسة آلاف ومليون", 5 * 1000 + 10 ** 6),
                 ("he", "אלפיים ומיליון", 2 * 1000 + 10 ** 6)]
        for lang, text, expected in cases:
            with self.subTest(lang=lang, text=text):
                self.assertEqual(extract_number(text, lang), expected)

    def test_romance_scale_groups_unchanged(self):
        cases = [("pt", "mil milhões", 10 ** 9),
                 ("pt", "dois mil milhões trezentos mil", 2 * 10 ** 9 + 300000),
                 ("es", "mil millones", 10 ** 9),
                 ("ro", "un miliard două sute de milioane", 12 * 10 ** 8)]
        for lang, text, expected in cases:
            with self.subTest(lang=lang, text=text):
                self.assertEqual(extract_number(text, lang), expected)


class TestNumbersToDigitsKeepsOneSpan(unittest.TestCase):
    def test_round_trip(self):
        for lang in ("ru", "uk", "hr", "nb", "nn"):
            for x in (345, 12345, 12 * 10 ** 6 + 345, 2300):
                spoken = pronounce_number(x, lang)
                with self.subTest(lang=lang, spoken=spoken):
                    self.assertEqual(numbers_to_digits(spoken, lang), str(x))

    def test_two_tens_stay_two_numbers(self):
        self.assertEqual(numbers_to_digits("двадцать тридцать", "ru"),
                         "20 30")


class TestNorwegianNumbersToDigits(unittest.TestCase):
    """numbers_to_digits for nb and nn uses the module converter."""

    def test_and_a_half(self):
        for lang, text in (("nb", "tre og en halv"), ("nn", "tre og ein halv")):
            with self.subTest(lang=lang):
                self.assertEqual(extract_number(text, lang), 3 + 0.5)
                self.assertEqual(numbers_to_digits(text, lang), "3.5")
        self.assertEqual(
            numbers_to_digits("sett en timer på tre og en halv time", "nb"),
            "sett en timer på 3.5 time")
        self.assertEqual(numbers_to_digits("hundre og en halv", "nb"), "100.5")

    def test_plural_fractions_count_the_number_before_them(self):
        for lang, plural in (("nb", "er"), ("nn", "ar")):
            for count, word, fraction, denominator in (
                    (2, "to", "tredjedel", 3), (3, "tre", "fjerdedel", 4)):
                text = f"{word} {fraction}{plural}"
                expected = float(Fraction(count, denominator))
                with self.subTest(lang=lang, text=text):
                    self.assertEqual(extract_number(text, lang), expected)
                    self.assertEqual(numbers_to_digits(text, lang),
                                     str(expected))

    def test_og_before_an_ordinal_stays_text(self):
        for lang in ("nb", "nn"):
            with self.subTest(lang=lang):
                self.assertEqual(numbers_to_digits("hundre og femte gang", lang),
                                 "100 og femte gang")
                self.assertEqual(numbers_to_digits("tre og", lang), "3 og")

    def test_clock_half_is_two_numbers(self):
        # "halv tre" is half past two; the date parser reads the clock
        for lang in ("nb", "nn"):
            with self.subTest(lang=lang):
                self.assertEqual(numbers_to_digits("klokka er halv tre", lang),
                                 "klokka er 0.5 3")

    def test_decimal_digits_are_exact(self):
        for lang, text in (("nb", "en komma en fire null"),
                           ("nn", "ein komma ein fire null")):
            with self.subTest(lang=lang):
                self.assertEqual(numbers_to_digits(text, lang), "1.14")


if __name__ == "__main__":
    unittest.main()
