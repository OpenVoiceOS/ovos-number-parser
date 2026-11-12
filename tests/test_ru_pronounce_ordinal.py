"""pronounce_ordinal reads Russian ordinals with the Russian engine.

Expected values come from *Правила русской орфографии и пунктуации* (1956),
§ 82, п. 2: "Порядковые числительные, последним элементом которых является
-сотый, -тысячный, -миллионный и т.д., если первая часть их написана
буквами, например: восьмисотый, двадцатипятитысячный,
стовосьмидесятитрёхмиллионный, но: восемьдесят шестой, тысяча девятьсот
сорок первый." *Русская грамматика* (1980), § 1367, writes "тысяча девятьсот
семьдесят шесть", with no "одна" before "тысяча".
"""
import unittest

from ovos_number_parser import pronounce_number, pronounce_ordinal
from ovos_number_parser.util import GrammaticalGender, Scale


class TestRussianPronounceOrdinal(unittest.TestCase):
    def assertReads(self, cases, **kwargs):
        for number, expected in cases:
            with self.subTest(number=number, **{k: str(v) for k, v in kwargs.items()}):
                self.assertEqual(pronounce_ordinal(number, "ru", **kwargs), expected)

    def test_rules_1956_examples(self):
        self.assertReads([
            (86, "восемьдесят шестой"),
            (1941, "тысяча девятьсот сорок первый"),
            (800, "восьмисотый"),
            (25000, "двадцатипятитысячный"),
            (183000000, "стовосьмидесятитрёхмиллионный"),
        ])

    def test_no_odna_before_tysyacha(self):
        # "в тысяча девятьсот восемьдесят пятом году"
        self.assertReads([
            (1001, "тысяча первый"),
            (1985, "тысяча девятьсот восемьдесят пятый"),
        ])
        self.assertReads([(1985, "тысяча девятьсот восемьдесят пятая")],
                         gender=GrammaticalGender.FEMININE)
        self.assertReads([(1985, "тысяча девятьсот восемьдесят пятое")],
                         gender=GrammaticalGender.NEUTRAL)

    def test_million_ordinals(self):
        self.assertReads([
            (10 ** 6, "миллионный"),
            (2 * 10 ** 6, "двухмиллионный"),
            (10 ** 6 + 1, "миллион первый"),
        ])

    def test_same_reading_as_pronounce_number(self):
        for number in (21, 1941, 2000, 10 ** 6, 10 ** 9):
            for gender in GrammaticalGender:
                with self.subTest(number=number, gender=gender.name):
                    self.assertEqual(
                        pronounce_ordinal(number, "ru", gender=gender),
                        pronounce_number(number, "ru", ordinals=True, gender=gender))

    def test_zero_keeps_its_ordinal(self):
        # CLDR RBNF ru "spellout-ordinal": 0 is "нулевой"
        self.assertEqual(pronounce_ordinal(0, "ru"), "нулевой")

    def test_scale_reaches_the_russian_engine(self):
        # 10**12 is "триллион" in the short scale and "биллион" in the long
        long_reading = pronounce_number(10 ** 12, "ru", ordinals=True, scale=Scale.LONG)
        short_reading = pronounce_number(10 ** 12, "ru", ordinals=True, scale=Scale.SHORT)
        self.assertNotEqual(long_reading, short_reading)
        self.assertEqual(pronounce_ordinal(10 ** 12, "ru", scale=Scale.LONG), long_reading)
        self.assertEqual(pronounce_ordinal(10 ** 12, "ru", scale=Scale.SHORT), short_reading)

    def test_no_ordinal_scale_word_from_ten_to_the_24(self):
        # the Russian engine names no ordinal scale from 10**24 up, so these
        # stay on the RBNF fallback, which has no rule for them either
        for number in (10 ** 24, -10 ** 24, 10 ** 30):
            with self.subTest(number=number):
                with self.assertRaises(NotImplementedError):
                    pronounce_ordinal(number, "ru")


if __name__ == "__main__":
    unittest.main()
