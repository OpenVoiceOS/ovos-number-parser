"""Russian: the zero ordinal, the count before a scale word, and the long scale.

Expected values:

- Zero: CLDR RBNF ``ru`` gives "нулевой" (spellout-ordinal-masculine) and
  "нулевое" (spellout-ordinal-neuter). ru.wiktionary "нулевой" declines it as
  an adjective of type 1b, so the feminine is "нулевая".
- The count before a scale word: CLDR RBNF ``ru`` spellout-cardinal,
  ``1000000: ←%spellout-cardinal-masculine← $(cardinal,one{миллион}
  few{миллиона}other{миллионов})$``. A count in the plural category "one"
  (21, 101) takes "миллион".
- The long scale: ru.wikipedia "Системы наименования чисел", table "Таблица
  от значения к названию": 10^9 миллиард, 10^12 биллион, 10^15 биллиард
  (тысяча биллионов), 10^18 триллион, 10^21 триллиард (тысяча триллионов).
  ru.wiktionary "триллион": "в системе наименования чисел с длинной шкалой:
  миллион биллионов (не миллиардов); число, равное 10^18".
"""
import unittest

from ovos_number_parser import pronounce_number
from ovos_number_parser.util import GrammaticalGender, Scale


class TestRussianZeroOrdinal(unittest.TestCase):
    def test_zero_ordinal_in_each_gender(self):
        for gender, expected in ((GrammaticalGender.MASCULINE, "нулевой"),
                                 (GrammaticalGender.FEMININE, "нулевая"),
                                 (GrammaticalGender.NEUTRAL, "нулевое")):
            with self.subTest(gender=gender.name):
                self.assertEqual(
                    pronounce_number(0, "ru", ordinals=True, gender=gender),
                    expected)

    def test_zero_cardinal_stays(self):
        self.assertEqual(pronounce_number(0, "ru"), "ноль")


class TestRussianScaleCount(unittest.TestCase):
    def test_count_ending_in_one_takes_the_singular(self):
        for number, expected in (
                (21 * 10 ** 6, "двадцать один миллион"),
                (101 * 10 ** 9, "сто один миллиард"),
                (22 * 10 ** 6, "двадцать два миллиона"),
                (11 * 10 ** 6, "одиннадцать миллионов"),
                (21000, "двадцать одна тысяча")):
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, "ru"), expected)


class TestRussianLongScale(unittest.TestCase):
    def assertLong(self, cases, **kwargs):
        for number, expected in cases:
            with self.subTest(number=number):
                self.assertEqual(
                    pronounce_number(number, "ru", scale=Scale.LONG, **kwargs),
                    expected)

    def test_cardinal(self):
        self.assertLong([
            (10 ** 9 + 1, "миллиард один"),
            (10 ** 12 + 1, "биллион один"),
            (2 * 10 ** 12, "два биллиона"),
            (10 ** 15 + 1, "биллиард один"),
            (10 ** 18 + 1, "триллион один"),
            (10 ** 19 + 1, "десять триллионов один"),
            (2 * 10 ** 21, "два триллиарда"),
            (1_500_000_000, "миллиард пятьсот миллионов"),
        ])

    def test_ordinal(self):
        self.assertLong([
            (10 ** 12 + 1, "биллион первый"),
            (10 ** 19 + 1, "десять триллионов первый"),
            (2 * 10 ** 21 + 5, "два триллиарда пятый"),
        ], ordinals=True)


if __name__ == "__main__":
    unittest.main()
