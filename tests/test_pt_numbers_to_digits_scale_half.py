"""numbers_to_digits reads Portuguese "e meio" after a scale word as
extract_number does: half of that scale.

"Um milhão e meio" is 1500000 and a decimal needs the decimal marker
("um milhão vírgula cinco" is 1000000.5); the numbers_pt module docstring
states the rule. Expected values are hand arithmetic: the scale times 1.5,
plus the count before the scale.
"""
import unittest

from ovos_number_parser import extract_number, numbers_to_digits


class TestNumbersToDigitsScaleAndAHalf(unittest.TestCase):
    #: text, expected output, language tag
    ROWS = [("um milhão e meio", "1500000", "pt-PT"),
            ("dois milhões e meio", "2500000", "pt-PT"),
            ("mil e meio", "1500", "pt-PT"),
            ("dois mil e meio", "2500", "pt-PT"),
            ("mil milhões e meio", "1500000000", "pt-PT"),
            ("um bilião e meio", "1500000000000", "pt-PT"),
            ("vendeu um milhão e meio de discos",
             "vendeu 1500000 de discos", "pt-PT"),
            ("menos um milhão e meio", "-1500000", "pt-PT"),
            ("um milhão e meio", "1500000", "pt-BR"),
            ("dois bilhões e meio", "2500000000", "pt-BR"),
            ("mil e meio", "1500", "pt-BR")]

    def test_half_of_the_scale(self):
        for text, expected, lang in self.ROWS:
            with self.subTest(text=text, lang=lang):
                self.assertEqual(numbers_to_digits(text, lang=lang), expected)

    def test_agrees_with_extract_number(self):
        for text, expected, lang in self.ROWS:
            with self.subTest(text=text, lang=lang):
                digits = [w for w in expected.split()
                          if w.lstrip("-").isdigit()]
                self.assertEqual([str(extract_number(text, lang=lang))],
                                 digits)

    def test_the_decimal_reading_needs_the_marker(self):
        for lang in ("pt-PT", "pt-BR"):
            with self.subTest(lang=lang):
                self.assertEqual(
                    numbers_to_digits("um milhão vírgula cinco", lang=lang),
                    "1000000.5")

    def test_a_half_after_a_number_below_a_thousand_stays_a_word(self):
        # extract_number reads "dois e meio" as 2.5; numbers_to_digits
        # writes the whole number in digits and keeps the fraction word
        for text, expected in [("dois e meio", "2 e meio"),
                               ("cem e meio", "100 e meio"),
                               ("mil e quinhentos e meio", "1500 e meio"),
                               ("uma hora e meia", "1 hora e meia")]:
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, lang="pt"), expected)

    def test_the_half_does_not_cross_another_word(self):
        for text, expected in [
                ("mil euros e meio", "1000 euros e meio"),
                ("comprei mil livros e meio quilo de café",
                 "comprei 1000 livros e meio quilo de café"),
                ("um milhão de pessoas e meia hora",
                 "1000000 de pessoas e meia hora")]:
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, lang="pt"), expected)

    def test_only_the_half_is_of_the_scale(self):
        # extract_number adds a quarter after a scale as a quarter of one
        # ("dois milhões e um quarto" = 2000000.25), so the quarter keeps
        # its fraction word here too
        for text, expected in [("dois milhões e um quarto",
                                "2000000 e 1 quarto"),
                               ("dois milhões e quarto",
                                "2000000 e quarto")]:
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, lang="pt"), expected)


if __name__ == "__main__":
    unittest.main()
