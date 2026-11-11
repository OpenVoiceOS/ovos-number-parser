"""Digit input next to a fraction, a scale word or a sign extracts without
an exception, and the sign stays on the number it belongs to.

Every expected value is integer or Fraction arithmetic, a string written by
hand, or the reading of a second input that must agree, never the output of
the input under test.
"""
import unittest
from fractions import Fraction

from ovos_number_parser import (extract_number, extract_number_spans,
                                numbers_to_digits)

LANGS = ["an", "ar", "ast", "az", "bg", "ca", "cs", "da", "de", "el", "en",
         "es", "et", "eu", "fa", "fi", "fr", "fy", "gl", "he", "hr", "hu",
         "id", "it", "kab", "ms", "mwl", "nb", "nl", "nn", "oc", "pl", "pt",
         "ro", "ru", "sk", "sl", "sv", "tr", "uk"]

SLAVIC = ["bg", "cs", "hr", "pl", "ru", "sk", "uk"]

#: languages whose extractors multiply a digit run by a scale word
MILLION = {"ar": "ملايين", "bg": "милион", "da": "million", "de": "Million",
           "en": "million", "eu": "milioi", "fy": "miljoen", "hr": "milijun",
           "nb": "million", "nl": "miljoen", "nn": "million", "pl": "milion",
           "ru": "миллион", "uk": "мільйон"}

#: the word each Romance vocabulary reads as the minus sign
ROMANCE_MINUS = {"an": "menos", "ast": "menos", "ca": "menys", "es": "menos",
                 "fr": "moins", "gl": "menos", "it": "meno", "mwl": "menos",
                 "oc": "mens", "pt": "menos", "ro": "minus"}


class TestDigitFractionNeverRaises(unittest.TestCase):
    def test_digits_then_fraction(self):
        for lang in LANGS:
            for digits in ("5", "12345678901234567890", "9" * 400):
                text = digits + " 1/2"
                with self.subTest(lang=lang, digits=len(digits)):
                    extract_number(text, lang)
                    numbers_to_digits(text, lang)


#: per language: the minus word, the words for 20, for 100 + 20 and for 200
MIXED = {"bg": ("минус", "двадесет", "сто двадесет", "двеста"),
         "cs": ("minus", "dvacet", "sto dvacet", "dvě stě"),
         "hr": ("minus", "dvadeset", "sto dvadeset", "dvjesto"),
         "pl": ("minus", "dwadzieścia", "sto dwadzieścia", "dwieście"),
         "ru": ("минус", "двадцать", "сто двадцать", "двести"),
         "sk": ("mínus", "dvadsať", "sto dvadsať", "dvesto"),
         "uk": ("мінус", "двадцять", "сто двадцять", "двісті"),
         "en": ("minus", "twenty", "one hundred twenty", "two hundred"),
         "nl": ("min", "twintig", "honderdtwintig", "tweehonderd"),
         "fy": ("min", "tweintich", "hûnderttweintich", "twahûndert")}


class TestDoubleMinusNeverRaises(unittest.TestCase):
    """A token with two leading hyphens ("--3") carries no sign: one hyphen
    is the minus sign, and "--3" is no digit string."""

    def test_double_minus(self):
        for lang in LANGS:
            for text in ("--3", "--3 1/2", "minus --3", "--3/2", "x --3/2 y"):
                with self.subTest(lang=lang, text=text):
                    extract_number(text, lang)
                    numbers_to_digits(text, lang)
                    extract_number_spans(text, lang)

    def test_double_minus_is_no_number(self):
        self.assertIs(extract_number("--3", "da"), False)
        self.assertIs(extract_number("minus --3", "da"), False)
        for lang in ("id", "ms"):
            with self.subTest(lang=lang):
                self.assertIs(extract_number("--3/2", lang), False)
                self.assertEqual(extract_number("-3/2", lang), Fraction(-3, 2))


class TestMixedNumber(unittest.TestCase):
    """A whole number and a proper digit fraction after it are one mixed
    number: "5 1/2" is 5 + 1/2, and "-5 1/2" is -(5 + 1/2)."""

    def test_digit_whole_part(self):
        for lang in MIXED:
            minus = MIXED[lang][0]
            for whole in (5, 20, 120, 300):
                mixed = Fraction(2 * whole + 1, 2)
                with self.subTest(lang=lang, whole=whole):
                    self.assertEqual(extract_number(f"{whole} 1/2", lang), mixed)
                    self.assertEqual(extract_number(f"-{whole} 1/2", lang), -mixed)
                    self.assertEqual(extract_number(f"{minus} {whole} 1/2", lang),
                                     -mixed)
                    self.assertEqual(extract_number(f"{whole} 3/4", lang),
                                     whole + Fraction(3, 4))

    def test_spoken_whole_part(self):
        for lang, (minus, twenty, hundred_twenty, two_hundred) in MIXED.items():
            with self.subTest(lang=lang):
                self.assertEqual(extract_number(twenty + " 1/2", lang),
                                 Fraction(41, 2))
                self.assertEqual(extract_number(f"{minus} {twenty} 1/2", lang),
                                 Fraction(-41, 2))
                self.assertEqual(extract_number(hundred_twenty + " 1/2", lang),
                                 Fraction(241, 2))
                self.assertEqual(extract_number(two_hundred + " 1/2", lang),
                                 Fraction(401, 2))

    def test_digits_written_once(self):
        # the mixed number is one value: it is written once, whole part
        # included
        for lang, (minus, twenty, _, two_hundred) in MIXED.items():
            with self.subTest(lang=lang):
                self.assertEqual(numbers_to_digits("5 1/2", lang), "5.5")
                self.assertEqual(numbers_to_digits("x 20 1/2 y", lang), "x 20.5 y")
                self.assertEqual(numbers_to_digits("x 120 1/2 y", lang), "x 120.5 y")
                self.assertEqual(numbers_to_digits("-5 1/2", lang), "-5.5")
                self.assertEqual(numbers_to_digits(twenty + " 1/2", lang), "20.5")
                self.assertEqual(numbers_to_digits(two_hundred + " 1/2", lang),
                                 "200.5")
        self.assertEqual(numbers_to_digits("у меня 20 1/2 литра", "ru"),
                         "у меня 20.5 литра")

    def test_other_fraction_after_a_number_is_a_second_number(self):
        # only a whole number and a proper fraction form a mixed number: a
        # fraction after a decimal, or an improper fraction, starts a second
        # number, and the first keeps its sign
        for lang, (minus, *_) in MIXED.items():
            with self.subTest(lang=lang):
                self.assertEqual(extract_number(f"{minus} 3.5 1/2", lang),
                                 Fraction(-7, 2))
                self.assertEqual(extract_number("5 3/2", lang), 5)
                self.assertEqual(numbers_to_digits("x 3.5 1/2 y", lang),
                                 "x 3.5 0.5 y")
                self.assertEqual(numbers_to_digits("x 5 3/2 y", lang),
                                 "x 5 1.5 y")

    def test_signed_zero_whole_part(self):
        for lang in MIXED:
            with self.subTest(lang=lang):
                self.assertEqual(extract_number("-0 1/2", lang), Fraction(-1, 2))
                self.assertEqual(numbers_to_digits("-0 1/2", lang), "-0.5")
        for lang in ("da", "de", "nb", "nn"):
            with self.subTest(lang=lang):
                self.assertEqual(extract_number("-0 1/2", lang), Fraction(-1, 2))

    def test_zero_fraction_after_a_number(self):
        # 0/2 is the number 0: it adds nothing to the number before it and
        # is written as 0
        for lang in MIXED:
            with self.subTest(lang=lang):
                self.assertEqual(extract_number("5 0/2", lang), 5)
                self.assertEqual(numbers_to_digits("5 0/2", lang), "5 0")
                self.assertEqual(numbers_to_digits("x 0/2 y", lang), "x 0 y")

    def test_mixed_number_no_float_holds(self):
        # from 2**52 on a float cannot hold a whole part and a half; the
        # whole number keeps every digit and the fraction is a second number
        whole = 2 ** 53 + 1
        for lang in list(MIXED) + ["da", "de", "nb", "nn"]:
            with self.subTest(lang=lang):
                value = extract_number(f"{whole} 1/2", lang)
                self.assertIsInstance(value, int)
                self.assertEqual(value, whole)
                minus = MIXED[lang][0] if lang in MIXED else "minus"
                self.assertEqual(extract_number(f"{minus} {whole} 1/2", lang),
                                 -whole)
                self.assertEqual(extract_number(f"-{whole} 1/2", lang), -whole)
                self.assertEqual(numbers_to_digits(f"{whole} 1/2", lang),
                                 f"{whole} 0.5")
                self.assertEqual(numbers_to_digits(f"{10 ** 19 + 1} 1/2", lang),
                                 f"{10 ** 19 + 1} 0.5")
                # below 2**52 the float holds the mixed number exactly
                self.assertEqual(extract_number(f"{2 ** 52 - 1} 1/2", lang),
                                 Fraction(2 ** 53 - 1, 2))
                self.assertEqual(extract_number("5 1/3", lang),
                                 float(5 + Fraction(1, 3)))

    def test_fraction_after_a_sign_word_is_not_joined(self):
        # the number before the sign word ends there: "5 min 1/2" is no
        # mixed number 5.5
        for lang in ("nl", "fy"):
            with self.subTest(lang=lang):
                self.assertEqual(extract_number("5 min 1/2", lang), -5)
        self.assertEqual(numbers_to_digits("5 min 1/2", "nl"), "5 min 0.5")

    def test_mixed_whole_part_past_float_range(self):
        big = "9" * 400
        for lang in MIXED:
            with self.subTest(lang=lang):
                self.assertEqual(extract_number(big + " 1/2", lang),
                                 extract_number("zzz", lang))

    def test_sign_covers_the_whole_mixed_number(self):
        # -5 1/2 is -(5 + 1/2)
        for lang in ("da", "de", "nb", "nn"):
            with self.subTest(lang=lang):
                self.assertEqual(extract_number("5 1/2", lang), Fraction(11, 2))
                self.assertEqual(extract_number("-5 1/2", lang), Fraction(-11, 2))
                self.assertEqual(extract_number("minus 5 1/2", lang),
                                 Fraction(-11, 2))

    def test_non_integral_whole_part_is_its_own_number(self):
        # a decimal or fractional value before a fraction is no mixed number
        # whole part: the two are two numbers, as English reads them
        for lang in ("en", "da", "de", "nb", "nn"):
            with self.subTest(lang=lang):
                self.assertEqual(extract_number("-1/2 1/2", lang),
                                 Fraction(-1, 2))
                self.assertEqual(extract_number("-3.5 1/2", lang),
                                 Fraction(-7, 2))

    def test_whole_part_past_float_range(self):
        # the value has no float, so it is no number, as the digit string
        # "999...9.5" is none
        big = "9" * 400
        for lang in ("da", "de", "nb", "nn"):
            with self.subTest(lang=lang):
                self.assertEqual(extract_number(big + " 1/2", lang),
                                 extract_number("zzz", lang))
                self.assertFalse(extract_number(big + ".5", lang))


class TestValuePastIntStringLimit(unittest.TestCase):
    """str() refuses an integer with more than 4300 digits. A digit run and
    a scale word whose product passes that limit are no number."""

    def test_product_past_the_limit_is_no_number(self):
        text_of = "9" * 4300 + " {}"
        for lang, word in MILLION.items():
            text = text_of.format(word)
            with self.subTest(lang=lang):
                self.assertIs(extract_number(text, lang), False)
                out = numbers_to_digits(text, lang)
                self.assertIn(out, (text, "9" * 4300 + " " + str(10 ** 6)))

    def test_product_within_the_limit_is_exact(self):
        # bg, hr, ru and uk add a digit run larger than the scale word to it
        # instead of multiplying ("2000000 милион" = 3000000), so the
        # product is checked where it is formed
        for lang in sorted(set(MILLION) - {"bg", "hr", "ru", "uk"}):
            word = MILLION[lang]
            with self.subTest(lang=lang):
                self.assertEqual(extract_number("9" * 4290 + " " + word, lang),
                                 (10 ** 4290 - 1) * 10 ** 6)


#: per language: the word for 3 and phrases where the minus word is part
#: of an idiom ("pelo menos" = at least), with a slot for the number
IDIOMS = {
    "pt": ("três", ["pelo menos {} dias", "ao menos {} dias",
                    "a menos que tenhas {} dias", "mais ou menos {} dias"]),
    "es": ("tres", ["al menos {} días", "por lo menos {} días",
                    "a lo menos {} días", "a menos que tengas {} días",
                    "más o menos {} días", "cuando menos {} días"]),
    "fr": ("trois", ["au moins {} jours", "du moins {} jours",
                     "à moins que tu aies {} jours", "à moins de {} jours",
                     "plus ou moins {} jours", "pour le moins {} jours",
                     "à tout le moins {} jours", "{} heures moins dix"]),
    "it": ("tre", ["più o meno {} ore", "a meno che tu abbia {} ore",
                   "a meno di {} ore", "sono le {} meno dieci",
                   "per lo meno {} ore", "quanto meno {} ore",
                   "perlomeno {} ore", "quantomeno {} ore"]),
    "ca": ("tres", ["al menys {} dies", "a menys que tinguis {} dies",
                    "més o menys {} dies", "ni més ni menys {} dies"]),
    "gl": ("tres", ["polo menos {} días", "ao menos {} días",
                    "a menos que teñas {} días", "máis ou menos {} días"]),
    "ast": ("tres", ["más o menos {} díes"]),
    "oc": ("tres", ["mai o mens {} jorns"]),
}


class TestRomanceSigns(unittest.TestCase):
    def test_minus_word_before_digits(self):
        for lang, minus in ROMANCE_MINUS.items():
            with self.subTest(lang=lang):
                self.assertEqual(extract_number(minus + " 3", lang), -3)
                self.assertEqual(extract_number(minus + " 3,5", lang),
                                 Fraction(-7, 2))
                self.assertEqual(extract_number(minus + " 12345678901234567890", lang),
                                 -12345678901234567890)

    def test_minus_word_only_when_adjacent(self):
        # "menos de 3" is "fewer than 3", not -3
        self.assertEqual(extract_number("menos de 3", "pt"), 3)

    def test_minus_word_in_an_idiom_signs_nothing(self):
        for lang, (three, phrases) in IDIOMS.items():
            for phrase in phrases:
                for number in ("3", three):
                    text = phrase.format(number)
                    with self.subTest(lang=lang, text=text):
                        self.assertEqual(extract_number(text, lang), 3)
        self.assertEqual(extract_number("une heure moins dix", "fr"), 1)

    def test_minus_word_after_a_french_clock_head_signs_nothing(self):
        # a glued hour ("9h"), "midi" (noon) and "minuit" (midnight) head
        # the clock form "<hour> moins <minutes>"
        for text in ("il est 9h moins 10", "il est 21h30 moins 10",
                     "midi moins 10", "il est midi moins 10",
                     "minuit moins dix"):
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, "fr"), 10)
        self.assertEqual(numbers_to_digits("midi moins dix", "fr"),
                         "midi moins 10")

    def test_idiom_keeps_the_minus_word_in_digits(self):
        self.assertEqual(numbers_to_digits("pelo menos três dias", "pt"),
                         "pelo menos 3 dias")
        self.assertEqual(numbers_to_digits("mais ou menos três horas", "pt"),
                         "mais ou menos 3 horas")
        self.assertEqual(numbers_to_digits("polo menos tres días", "gl"),
                         "polo menos 3 días")

    def test_minus_word_before_a_number_still_signs(self):
        for lang, (three, _) in IDIOMS.items():
            minus = ROMANCE_MINUS[lang]
            for number in ("3", three):
                with self.subTest(lang=lang, number=number):
                    self.assertEqual(extract_number(f"{minus} {number}", lang), -3)
        for lang, text in (("pt", "a temperatura é menos três graus"),
                           ("pt", "desceu a menos três graus"),
                           ("pt", "desceu a menos 3 graus"),
                           ("es", "la temperatura es de menos tres grados"),
                           ("fr", "il fait moins trois degrés"),
                           ("fr", "descendue à moins trois degrés"),
                           ("it", "fuori ci sono meno tre gradi"),
                           ("ca", "fa menys tres graus")):
            with self.subTest(lang=lang, text=text):
                self.assertEqual(extract_number(text, lang), -3)
        self.assertEqual(numbers_to_digits("menos três", "pt"), "-3")
        self.assertEqual(numbers_to_digits("a temperatura é menos três graus", "pt"),
                         "a temperatura é -3 graus")

    def test_minus_word_after_a_number_signs_nothing(self):
        # between two numbers the word subtracts: the first number is read
        for lang, text in (("pt", "três menos dois"), ("es", "tres menos dos"),
                           ("fr", "trois moins deux"), ("it", "tre meno due"),
                           ("pt", "3 menos 2")):
            with self.subTest(lang=lang, text=text):
                self.assertEqual(extract_number(text, lang), 3)
        self.assertEqual(numbers_to_digits("três menos dois", "pt"), "3 menos 2")

    def test_leading_decimal_separator(self):
        for lang in ROMANCE_MINUS:
            with self.subTest(lang=lang):
                self.assertEqual(extract_number("-.5", lang), Fraction(-1, 2))
                self.assertEqual(extract_number(".5", lang), Fraction(1, 2))
                self.assertEqual(extract_number("-,5", lang), Fraction(-1, 2))


class TestNordicSignedPart(unittest.TestCase):
    """A sign after a summed part opens the next number, as English reads
    "five and minus three" as 5."""

    def test_signed_part_is_a_new_number(self):
        self.assertEqual(extract_number("five and minus three", "en"), 5)
        for lang in ("da", "nb", "nn"):
            with self.subTest(lang=lang):
                self.assertEqual(extract_number("5 og -3", lang), 5)
                self.assertEqual(extract_number("fem og minus tre", lang), 5)
                self.assertEqual(numbers_to_digits("5 og -3", lang), "5 og -3")

    def test_signed_part_after_an_article_only_part(self):
        # "en" alone is the number 1, as English reads "one and minus three"
        # as 1
        self.assertEqual(extract_number("one and minus three", "en"), 1)
        for lang, one in (("da", "en"), ("da", "et"), ("nb", "en"),
                          ("nb", "ett"), ("nn", "ein"), ("nn", "eitt")):
            with self.subTest(lang=lang, one=one):
                self.assertEqual(extract_number(f"{one} og -3", lang), 1)
                self.assertEqual(extract_number(f"{one} og minus tre", lang), 1)

    def test_swedish_signed_part_is_a_new_number(self):
        for text in ("5 och -3", "fem och -3", "5 och minus 3"):
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, "sv"), 5)
        self.assertEqual(extract_number("en och -3", "sv"), 1)
        self.assertEqual(extract_number("5 och 3", "sv"), 8)

    def test_leading_sign_still_covers_the_number(self):
        for lang in ("da", "nb"):
            with self.subTest(lang=lang):
                self.assertEqual(extract_number("minus fem og tyve", lang), -25)
                self.assertEqual(extract_number("-5 og 20", lang), -25)
                # nb "og" joins one number only after a hundred or a scale
                # word, for a unit before a tens word, or before a fraction.
                # Between two other numbers it is the plus sign (Bokmålsordboka
                # "og", sense 9: "brukt for å vise at to tall skal adderes"),
                # and the parser does not do sums, so "5 og 3" is 5 and 3, as
                # "fem pluss tre" is. da keeps its own rule.
                self.assertEqual(extract_number("5 og 3", lang),
                                 8 if lang == "da" else 5)
        for lang in ("nb", "nn"):
            with self.subTest(lang=lang):
                self.assertEqual(extract_number("fem pluss tre", lang), 5)
                self.assertEqual(numbers_to_digits("fem pluss tre", lang),
                                 "5 pluss 3")
                self.assertEqual(extract_number("five plus three", "en"), 5)

    def test_signed_part_after_og_and_a_hundred(self):
        # "-3" after "og" is a number of its own, also where "og" would join
        # a smaller number to a hundred
        for lang in ("nb", "nn"):
            with self.subTest(lang=lang):
                self.assertEqual(extract_number("hundre og -3", lang), 100)
                self.assertEqual(numbers_to_digits("hundre og -3", lang),
                                 "100 og -3")


if __name__ == "__main__":
    unittest.main()
