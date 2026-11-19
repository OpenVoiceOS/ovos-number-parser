"""Decimal readings use the words of the language.

Each expected reading is composed from the reading of whole numbers below
100, which this change leaves as they are, and from the words of the
language:

- da says the zero before the decimal word: "nul komma fem" (0.5)
- kk and ky read the fraction as a numerator after the word for its power of
  ten: "нөл бүтін оннан бес" (0.5), "он екі бүтін жүзден жиырма бес" (12.25).
  The CLDR rule sets have words up to hundred billionths ("жүз миллиардтан",
  "жүз миллиарддан"), so a longer fraction is rounded half up to 11 digits
- mt reads the digits in the absolute form used for counting ("tnejn",
  "ħamsa"), not the attributive form used before a noun ("żewġ", "ħames")
- cy reads the digits in the counting form ("dau", "tri"), not the forms used
  only before a feminine noun ("dwy", "tair")
- in mt and cy the whole part reads as the integer does for the gender, and
  the digits after the point read in the counting form for every gender
- lo uses the Lao words for zero, minus and the decimal point, not the Thai
  words the CLDR data holds
"""
import unittest
from decimal import ROUND_HALF_UP, Decimal

from unicode_rbnf import RbnfEngine

from ovos_number_parser import pronounce_number, pronounce_ordinal
from ovos_number_parser.util import GrammaticalGender

F = GrammaticalGender.FEMININE
ZWSP = "​"


def _say(number, lang):
    return pronounce_number(number, lang)


class TestDanishZeroBeforeComma(unittest.TestCase):

    def test_zero_whole_part_is_spoken(self):
        expected = {
            0.5: f"{_say(0, 'da')} komma fem nul nul",
            -0.5: f"minus {_say(0, 'da')} komma fem nul nul",
            0.05: f"{_say(0, 'da')} komma nul fem nul",
            12.25: f"{_say(12, 'da')} komma to fem nul",
            -3.75: f"{_say(-3, 'da')} komma syv fem nul",
        }
        for number, spoken in expected.items():
            with self.subTest(number=number):
                reading = pronounce_number(number, "da")
                self.assertEqual(reading, spoken)
                self.assertFalse(reading.startswith("komma"))
                self.assertNotIn("minus komma", reading)


class TestFractionAsNumerator(unittest.TestCase):
    #: the decimal-point word and the words for tenths and hundredths
    WORDS = {
        "kk": ("бүтін", "оннан", "жүзден"),
        "ky": ("бүтүн", "ондон", "жүздөн"),
    }

    def test_fraction_is_read_over_its_power_of_ten(self):
        for lang, (point, tenths, hundredths) in self.WORDS.items():
            expected = {
                0.5: f"{_say(0, lang)} {point} {tenths} {_say(5, lang)}",
                0.05: f"{_say(0, lang)} {point} {hundredths} {_say(5, lang)}",
                12.25: f"{_say(12, lang)} {point} {hundredths} {_say(25, lang)}",
                -3.75: f"{_say(-3, lang)} {point} {hundredths} {_say(75, lang)}",
            }
            for number, spoken in expected.items():
                with self.subTest(lang=lang, number=number):
                    reading = pronounce_number(number, lang)
                    self.assertEqual(reading, spoken)
                    self.assertNotIn(f"{tenths} {_say(0, lang)}", reading)

    #: the word for hundred billionths, the longest power of ten the CLDR
    #: fraction rule set has a word for
    HUNDRED_BILLIONTHS = {"kk": "жүз миллиардтан", "ky": "жүз миллиарддан"}

    def test_fraction_longer_than_eleven_digits_is_rounded_to_eleven(self):
        third = (Decimal(1) / Decimal(3)).quantize(Decimal("1e-11"), ROUND_HALF_UP)
        numerator = int(third.scaleb(11))
        self.assertEqual(numerator, 33333333333)
        for lang, (point, _, _) in self.WORDS.items():
            words = self.HUNDRED_BILLIONTHS[lang]
            third_reading = f"{_say(0, lang)} {point} {words} {_say(numerator, lang)}"
            for places in (12, 13):
                with self.subTest(lang=lang, number="1/3", places=places):
                    self.assertEqual(pronounce_number(1 / 3, lang, places=places),
                                     third_reading)
            with self.subTest(lang=lang, number=0.999999999999):
                self.assertEqual(pronounce_number(0.999999999999, lang, places=12),
                                 _say(1, lang))

    #: the word for ten millionths in the CLDR fraction rule set
    TEN_MILLIONTHS = {"kk": "он миллионнан", "ky": "он миллиондон"}

    def test_fraction_below_one_millionth_is_read_over_its_power_of_ten(self):
        for lang, (point, _, _) in self.WORDS.items():
            words = self.TEN_MILLIONTHS[lang]
            with self.subTest(lang=lang):
                self.assertEqual(pronounce_number(3e-7, lang, places=8),
                                 f"{_say(0, lang)} {point} {words} {_say(3, lang)}")

    def test_fraction_below_eleven_digits_reads_as_its_whole_part(self):
        cases = ((0.1 + 0.2 - 0.3, 3), (2e-14, 3), (3 + 4e-13, 13))
        for lang in self.WORDS:
            for number, places in cases:
                with self.subTest(lang=lang, number=number, places=places):
                    self.assertEqual(pronounce_number(number, lang, places=places),
                                     _say(int(number), lang))


class TestCountingFormDigits(unittest.TestCase):
    #: the decimal-point word and the attributive or feminine forms that a
    #: bare number never takes
    WORDS = {
        "mt": ("punt", {"żewġ", "tliet", "ħames", "sebaʼ", "tnax-il"}),
        "cy": ("pwynt", {"dwy", "tair"}),
    }

    def test_value_below_one_millionth_reads_each_digit(self):
        for lang, (point, _) in self.WORDS.items():
            expected = " ".join([_say(0, lang), point] + [_say(0, lang)] * 6
                                + [_say(2, lang), _say(5, lang)])
            with self.subTest(lang=lang):
                self.assertEqual(pronounce_number(2.5e-7, lang, places=8),
                                 expected)

    def test_digits_take_the_counting_form(self):
        for lang, (point, wrong) in self.WORDS.items():
            expected = {
                0.5: f"{_say(0, lang)} {point} {_say(5, lang)}",
                12.25: f"{_say(12, lang)} {point} {_say(2, lang)} {_say(5, lang)}",
                -3.75: f"{_say(-3, lang)} {point} {_say(7, lang)} {_say(5, lang)}",
            }
            for number, spoken in expected.items():
                with self.subTest(lang=lang, number=number):
                    reading = pronounce_number(number, lang)
                    self.assertEqual(reading, spoken)
                    self.assertFalse(wrong & set(reading.split()), reading)

    def test_whole_part_follows_gender_and_digits_count(self):
        cases = {
            "mt": {1.1: (1, (1,)), 1.5: (1, (5,)), 21.1: (21, (1,)),
                   12.25: (12, (2, 5))},
            "cy": {12.25: (12, (2, 5)), 2.2: (2, (2,)), 21.1: (21, (1,))},
        }
        for lang, values in cases.items():
            point, wrong = self.WORDS[lang]
            for gender in (GrammaticalGender.MASCULINE, F):
                for number, (whole, digits) in values.items():
                    with self.subTest(lang=lang, gender=gender.name, number=number):
                        reading = pronounce_number(number, lang, gender=gender)
                        expected = " ".join(
                            [pronounce_number(whole, lang, gender=gender), point]
                            + [_say(d, lang) for d in digits])
                        self.assertEqual(reading, expected)
                        after_point = reading.split(f" {point} ")[1].split()
                        self.assertFalse(wrong & set(after_point), reading)
                        self.assertNotIn("waħda", after_point)


class TestLaoWords(unittest.TestCase):
    ZERO, MINUS, POINT = "ສູນ", "ລົບ", "ຈຸດ"
    THAI = ("ศูนย์", "ลบ", "จุด")

    def test_decimal_words_are_lao(self):
        two, three, five, seven, twelve = (
            _say(n, "lo") for n in (2, 3, 5, 7, 12))
        point = ZWSP + self.POINT + ZWSP
        expected = {
            0.5: self.ZERO + point + five,
            0.05: self.ZERO + point + self.ZERO + five,
            12.25: twelve + point + two + five,
            -3.75: self.MINUS + ZWSP + three + point + seven + five,
        }
        for number, spoken in expected.items():
            with self.subTest(number=number):
                reading = pronounce_number(number, "lo")
                self.assertEqual(reading, spoken)
                for word in self.THAI:
                    self.assertNotIn(word, reading)

    def test_whole_numbers_and_ordinals_are_lao(self):
        one = _say(1, "lo")
        expected = {
            0: self.ZERO,
            -3: self.MINUS + ZWSP + _say(3, "lo"),
            100: one + ZWSP + "ຮ້ອຍ",
            1000: one + ZWSP + "ພັນ",
            10000: one + ZWSP + "ໝື່ນ",
            100000: one + ZWSP + "ແສນ",
            1000000: one + ZWSP + "ລ້ານ",
        }
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, "lo"), spoken)
        self.assertEqual(pronounce_ordinal(1, "lo"), "ທີ່" + ZWSP + one)

    def test_no_thai_letter_in_any_reading(self):
        for number in (0, -7, 100.5, 1234.567, -999999.25, 2000000, 0.001):
            with self.subTest(number=number):
                reading = pronounce_number(number, "lo")
                self.assertFalse(any("฀" <= c <= "๿" for c in reading),
                                 reading)


class TestIntegersUnchanged(unittest.TestCase):

    def test_integers_read_as_the_engine_reads_them(self):
        numbers = list(range(-30, 131)) + [1000, 2023, 123456]
        for lang in ("kk", "ky", "mt", "cy"):
            engine = RbnfEngine.for_language(lang)
            for number in numbers:
                with self.subTest(lang=lang, number=number):
                    self.assertEqual(pronounce_number(number, lang),
                                     engine.format_number(number).text)

    def test_lao_integers_without_thai_words_are_unchanged(self):
        engine = RbnfEngine.for_language("lo")
        for number in range(1, 100):
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, "lo"),
                                 engine.format_number(number).text)

    def test_danish_integers_are_unchanged(self):
        expected = {0: "nul", 12: "tolv", -3: "minus tre", 100: "hundrede"}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, "da"), spoken)


if __name__ == "__main__":
    unittest.main()
