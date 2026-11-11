"""Spoken and written numbers that extraction misread.

Every expected value is integer arithmetic, a float literal of the same
digits, or the reading of an independently computed number by
pronounce_number, never the output of the extractor under test.
"""
import re
import unittest
from decimal import Decimal
from fractions import Fraction

from ovos_number_parser import (extract_number, extract_number_spans,
                                is_fractional, numbers_to_digits,
                                pronounce_number)
from ovos_number_parser.numbers_ar import extract_numbers_ar
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
                               ("one point oh oh five", "1.005"),
                               ("one point nought five", "1.05"),
                               ("one point o five", "1.05")):
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, "en"), float(expected))
                self.assertEqual(numbers_to_digits(text, "en"), expected)

    def test_o_before_the_point_stays_text(self):
        for text, expected in (("room o one", "room o 1"),
                               ("o five", "o 5")):
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, "en"), expected)

    def test_zero_digits_before_the_scale(self):
        for text, expected in (("one point five zero million", 15 * 10 ** 5),
                               ("one point five oh million", 15 * 10 ** 5),
                               ("one point two zero million", 12 * 10 ** 5),
                               ("one point five zero thousand", 1500)):
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, "en"), expected)
                self.assertEqual(numbers_to_digits(text, "en"), str(expected))

    def test_point_needs_digits_directly_after_it(self):
        text = "at one point there were two million users"
        self.assertEqual(numbers_to_digits(text, "en"),
                         f"at 1 point there were {2 * 10 ** 6} users")
        self.assertEqual(extract_number(text, "en"), 1)
        for text in ("one apple point five", "one point the five"):
            with self.subTest(text=text):
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

    def test_a_count_at_the_start_of_a_sentence(self):
        self.assertEqual(numbers_to_digits("Ein Viertel Liter", "de"),
                         f"{float(Fraction(1, 4))} Liter")
        self.assertEqual(extract_number("Ein Viertel Liter", "de",
                                        ordinals=True), Fraction(1, 4))
        self.assertEqual(
            [(span.surface, span.value)
             for span in extract_number_spans("Ein Viertel Liter", "de")],
            [("Ein Viertel", Fraction(1, 4))])
        self.assertEqual(extract_number("ein halbes Viertel", "de",
                                        ordinals=True), Fraction(1, 8))
        self.assertEqual(numbers_to_digits("ein halbes Viertel", "de"),
                         str(float(Fraction(1, 8))))
        self.assertEqual(numbers_to_digits("Zwölf Millionen Menschen", "de"),
                         f"{12 * 10 ** 6} Menschen")
        self.assertEqual(numbers_to_digits("Drei Viertel", "de"),
                         str(float(Fraction(3, 4))))

    def test_a_scale_noun_multiplies_the_decimal(self):
        for text, expected in (
                ("er hat zwei Komma fünf Millionen Euro",
                 f"er hat {25 * 10 ** 5} Euro"),
                ("eins Komma fünf Milliarden", str(15 * 10 ** 8)),
                ("drei Komma zwei Millionen Einwohner",
                 f"{32 * 10 ** 5} Einwohner")):
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, "de"), expected)
        for text, expected in (("zwei komma fünf millionen", 25 * 10 ** 5),
                               ("eins Komma fünf Milliarden", 15 * 10 ** 8),
                               ("minus zwei komma fünf millionen",
                                -25 * 10 ** 5)):
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, "de"), expected)

    def test_whole_values_are_written_as_integers(self):
        for text, expected in (("vier Halbe", 4 // 2), ("drei Drittel", 1)):
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, "de"), str(expected))

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
                # numbers_to_digits converts number words, never digits
                self.assertEqual(numbers_to_digits("0.500", lang), "0.500")
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
        for lang in ("ru", "uk", "hr"):
            for x in (345, 12345, 12 * 10 ** 6 + 345, 2300):
                spoken = pronounce_number(x, lang)
                with self.subTest(lang=lang, spoken=spoken):
                    self.assertEqual(numbers_to_digits(spoken, lang), str(x))

    def test_two_tens_stay_two_numbers(self):
        self.assertEqual(numbers_to_digits("двадцать тридцать", "ru"),
                         "20 30")


def _spans(text, lang):
    return [(span.surface, span.value)
            for span in extract_number_spans(text, lang)]


class TestSpansJoinOnlyOneNumber(unittest.TestCase):
    """A span grows past a number word only when the whole stretch converts
    to one number."""

    def test_a_whole_number_before_another_number_is_its_own_span(self):
        for tail, value in (("one million", 10 ** 6),
                            ("one third", 1 / 3)):
            with self.subTest(tail=tail):
                self.assertEqual(_spans(f"two hundred and one {tail}", "en"),
                                 [("two hundred and one", 201), (tail, value)])

    def test_a_mixed_number_is_one_span(self):
        for text, lang in (("two and three quarters", "en"),
                           ("dva a tri štvrtiny", "sk")):
            with self.subTest(text=text):
                self.assertEqual(_spans(text, lang),
                                 [(text, 2 + Fraction(3, 4))])

    def test_decimal_digits_after_a_zero_are_one_span(self):
        for text, lang, expected in (("one point zero five", "en", 1.05),
                                     ("null Komma null fünf", "de", 0.05)):
            with self.subTest(text=text):
                self.assertEqual(_spans(text, lang), [(text, expected)])
                self.assertEqual(
                    extract_number(text, lang, ordinals=True), expected)


class TestArabicSpansAcrossAnd(unittest.TestCase):
    """Arabic spans follow the Arabic extractor's own reading of "و"."""

    def test_unit_and_hundreds_is_one_number(self):
        # the Arabic extractor reads both as one number: 7 + 5 * 100
        for text in ("سبعة و خمسة مئة", "سبعة وخمسة مئة"):
            with self.subTest(text=text):
                self.assertEqual(extract_numbers_ar(text), [7 + 5 * 100])
                self.assertEqual(_spans(text, "ar"), [(text, 7 + 5 * 100)])

    def test_a_span_may_open_with_and(self):
        text = "لديه سيارة وواحد مليون دينار"
        self.assertEqual(extract_numbers_ar(text), [10 ** 6])
        self.assertEqual(_spans(text, "ar"), [("وواحد مليون", 10 ** 6)])

    def test_two_units_are_two_numbers(self):
        self.assertEqual(_spans("سبعة و خمسة", "ar"),
                         [("سبعة", 7), ("خمسة", 5)])


class TestDigitStringsStayAsWritten(unittest.TestCase):
    """numbers_to_digits converts number words, never digit strings."""

    LANGS = ["en", "de", "da", "sv", "nl", "pt", "es", "it",
             "fr", "ca", "pl", "ru", "eu", "el", "ar"]

    def test_digit_strings(self):
        for lang in self.LANGS:
            for text in ("Version 2.0", "12.0", "10.000 Euro", "0.500",
                         "2 5"):
                with self.subTest(lang=lang, text=text):
                    self.assertEqual(
                        numbers_to_digits(text, lang).casefold(),
                        text.casefold())

    def test_digits_joined_by_and(self):
        for lang in ("da",):
            for text in ("5 og 20", "-5 og 20"):
                with self.subTest(lang=lang, text=text):
                    self.assertEqual(numbers_to_digits(text, lang), text)

    def test_number_words_beside_digits_still_convert(self):
        self.assertEqual(numbers_to_digits("1 sixth", "en"), str(1 / 6))
        self.assertEqual(numbers_to_digits("minus 5", "en"), "-5")
        self.assertEqual(numbers_to_digits("12.0 und zwei", "de"),
                         "12.0 und 2")

    def test_german_clock_is_still_written_with_a_colon(self):
        self.assertEqual(numbers_to_digits("um 07.30 Uhr", "de"),
                         "um 07:30 Uhr")


class TestGermanDigitGroups(unittest.TestCase):
    """German groups digits with "." and marks the decimal with ","
    (CLDR de)."""

    def test_grouped_digits(self):
        for text, expected in (("12.000", 12000),
                               ("1.234.567", 1234567),
                               ("-12.000", -12000),
                               ("kostet 12.000 Euro", 12000),
                               ("12.000,5", 12000 + Fraction(1, 2)),
                               ("1.234.567,5", 1234567 + Fraction(1, 2))):
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, "de"), expected)

    def test_point_decimal_without_groups(self):
        for text, expected in (("1.5", Fraction(3, 2)),
                               ("0.500", Fraction(1, 2)),
                               ("3.14159", 3.14159)):
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, "de"), expected)


class TestNumberWordsBesideDigitsAndPunctuation(unittest.TestCase):
    """A digit string stays as written only where no number word joins it;
    punctuation and a capital letter do not hide the number word."""

    def test_number_words_join_the_digits(self):
        for text, lang, digits in (
                ("x 5 tusind, y", "da", f"x {5 * 1000}, y"),
                ("x 5 duizend. y", "nl", f"x {5 * 1000}. y"),
                ("5 Tusind", "da", str(5 * 1000)),
                ("2 point 5", "en", str(2.5)),
                ("2 запятая 5", "ru", str(2.5)),
                ("2 Komma 5", "de", str(2.5))):
            with self.subTest(lang=lang, text=text):
                self.assertEqual(numbers_to_digits(text, lang), digits)


class TestDecimalBeforeAFraction(unittest.TestCase):
    """The whole part of a mixed number is an integer; a decimal before a
    fraction is a number of its own."""

    def test_two_numbers(self):
        for lang in ("en", "de", "da"):
            with self.subTest(lang=lang):
                self.assertEqual(numbers_to_digits("x 3.5 1/2 y", lang),
                                 f"x 3.5 {1 / 2} y")
                self.assertEqual(extract_number("x 3.5 1/2 y", lang),
                                 Fraction(7, 2))
                self.assertEqual(_spans("x 3.5 1/2 y", lang),
                                 [("3.5", 3.5), ("1/2", 1 / 2)])
                self.assertEqual(extract_number("minus 3.5 1/2", lang),
                                 Fraction(-7, 2))

    def test_spoken_decimal_before_a_fraction(self):
        for lang, text in (("de", "drei Komma fünf ein halb"),
                           ("de", "drei Komma fünf 1/2"),
                           ("da", "tre komma fem en halv"),
                           ("da", "tre komma fem og en halv"),
                           ("da", "tre komma fem 1/2")):
            with self.subTest(lang=lang, text=text):
                self.assertEqual(extract_number(text, lang), Fraction(7, 2))
        self.assertEqual(numbers_to_digits("drei Komma fünf ein halb", "de"),
                         f"{7 / 2} {1 / 2}")
        self.assertEqual(numbers_to_digits("drei Komma fünf ein Viertel", "de"),
                         f"{7 / 2} {1 / 4}")

    def test_spoken_decimal_digits_still_join(self):
        for lang, text in (("de", "drei Komma fünf eins"),
                           ("da", "tre komma fem en")):
            with self.subTest(lang=lang, text=text):
                self.assertEqual(extract_number(text, lang), 3.51)

    def test_integer_whole_part_still_makes_a_mixed_number(self):
        for lang in ("en", "de", "da"):
            with self.subTest(lang=lang):
                self.assertEqual(numbers_to_digits("x 3 1/2 y", lang),
                                 f"x {3 + 1 / 2} y")


if __name__ == "__main__":
    unittest.main()
