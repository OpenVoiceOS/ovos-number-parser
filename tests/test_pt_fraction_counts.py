"""A cardinal before a fraction word counts its parts in Portuguese.

Priberam, "vigésimo", noun sense 2: "Cada uma das vinte partes iguais em que
se divide um todo." One such part, "um vigésimo", is 1/20.

Priberam, "avo", [Matemática]: "Palavra que se junta a um denominador maior
que dez para indicar a divisão da unidade no número de partes iguais indicado
por esse denominador (ex.: doze vinte e cinco avos = 12/25)."

Expected values are the arithmetic of those definitions.
"""
import unittest
from fractions import Fraction

from ovos_number_parser import extract_number, numbers_to_digits


class TestCountBeforeSingularFraction(unittest.TestCase):
    cases = {
        "bebi um quinto da garrafa": Fraction(1, 5),
        "um terço da turma faltou": Fraction(1, 3),
        "um vigésimo do prémio": Fraction(1, 20),
        "um milésimo de segundo": Fraction(1, 1000),
        "a receita leva dois e um quarto de chávena": 2 + Fraction(1, 4),
        "três e um terço de litro": 3 + Fraction(1, 3),
    }

    def test_extract(self):
        for text, expected in self.cases.items():
            with self.subTest(text=text):
                self.assertAlmostEqual(extract_number(text, lang="pt"),
                                       float(expected))

    def test_joiner_still_adds(self):
        self.assertEqual(extract_number("dois e meio", lang="pt"), 2.5)
        self.assertAlmostEqual(extract_number("dois quintos", lang="pt"), 0.4)

    def test_digits_keep_the_count_apart(self):
        self.assertEqual(numbers_to_digits("dois e um quarto de chávena", "pt"),
                         "2 e 1 quarto de chávena")


class TestAvosDenominator(unittest.TestCase):
    cases = {
        "doze avos": Fraction(1, 12),
        "comi três doze avos do bolo": Fraction(3, 12),
        "quinze doze avos": Fraction(15, 12),
        "doze vinte e cinco avos": Fraction(12, 25),
        "menos três doze avos": -Fraction(3, 12),
    }

    def test_extract(self):
        for text, expected in self.cases.items():
            with self.subTest(text=text):
                self.assertAlmostEqual(extract_number(text, lang="pt"),
                                       float(expected))

    def test_digits_keep_count_and_denominator_apart(self):
        self.assertEqual(numbers_to_digits("comi três doze avos do bolo", "pt"),
                         "comi 3 12 avos do bolo")
        self.assertEqual(numbers_to_digits("doze vinte e cinco avos", "pt"),
                         "12 25 avos")


if __name__ == "__main__":
    unittest.main()
