"""Digits before a scale word are one number: "2 milhões" is 2000000.

CLDR writes large numbers in this form (long compact decimal patterns
"0 milhões", "0 millones", "0 de milioane").
"""
import unittest

from ovos_number_parser import extract_number, numbers_to_digits


class TestDigitsBeforeScale(unittest.TestCase):
    def test_the_digits_count_the_scale(self):
        for lang, text, value in [
                ("pt-PT", "2 milhões de pessoas", 2000000),
                ("pt-PT", "5 mil euros", 5000),
                ("pt-PT", "2,5 milhões", 2500000),
                ("pt-PT", "2 mil milhões de euros", 2000000000),
                ("pt-PT", "1.500 milhões", 1500000000),
                ("pt-PT", "-3 mil", -3000),
                ("pt-PT", "menos 3 mil", -3000),
                ("pt-BR", "2 bilhões de reais", 2000000000),
                ("es-ES", "7,2 mil millones", 7200000000),
                ("fr-FR", "3 millions", 3000000),
                ("it-IT", "12 milioni", 12000000),
                ("ro-RO", "250 de milioane", 250000000)]:
            with self.subTest(lang=lang, text=text):
                result = extract_number(text, lang=lang)
                self.assertEqual(result, value)
                self.assertIs(type(result), int)

    def test_a_decimal_count_is_exact(self):
        # 4.1 * 10 ** 6 in floats is 4099999.9999999995
        for text, value in [("2,5 mil", 2500), ("1,25 mil", 1250),
                            ("4,1 milhões", 4100000), ("0,0005 mil", 0.5)]:
            with self.subTest(text=text):
                result = extract_number(text, lang="pt-PT")
                self.assertEqual(result, value)
                self.assertIs(type(result), type(value))

    def test_numbers_to_digits_writes_one_number(self):
        for lang, text, digits in [
                ("pt-PT", "custou 2 milhões de euros", "custou 2000000 de euros"),
                ("pt-PT", "5 mil euros", "5000 euros"),
                ("pt-PT", "2,5 milhões de pessoas", "2500000 de pessoas"),
                ("pt-PT", "custaram 2020 milhões de euros",
                 "custaram 2020000000 de euros"),
                ("es-ES", "2 millones", "2000000"),
                ("ro-RO", "25 de mii de lei", "25000 de lei"),
                # the mark after the scale word stays
                ("pt-PT", "custou 2 milhões.", "custou 2000000."),
                ("pt-PT", "custou 2 milhões, disse", "custou 2000000, disse"),
                ("pt-PT", "2 mil, 3 mil", "2000, 3000"),
                ("pt-PT", "2 mil, milhões de pessoas",
                 "2000, milhões de pessoas")]:
            with self.subTest(lang=lang, text=text):
                self.assertEqual(numbers_to_digits(text, lang=lang), digits)

    def test_digits_with_no_scale_word_are_unchanged(self):
        for lang, text, value, digits in [
                ("pt-PT", "2 euros", 2, "2 euros"),
                ("pt-PT", "10.000 euros", 10000, "10.000 euros"),
                # "de" joins a count to its scale only in ro
                ("pt-PT", "2 de milhões", 2, "2 de milhões"),
                # a mark after the digits ends the number
                ("pt-PT", "nota 2, mil vezes", 2, "nota 2, 1000 vezes")]:
            with self.subTest(lang=lang, text=text):
                self.assertEqual(extract_number(text, lang=lang), value)
                self.assertEqual(numbers_to_digits(text, lang=lang), digits)


if __name__ == "__main__":
    unittest.main()
