"""Mirandese hundreds are read periphrastically.

The spoken pattern is "<unit> cientos" ("dous cientos", "cinco cientos"), with
"cien" standalone and "ciento" before a remainder. The synthetic forms
(duzientos, trezientos, quinhentos, quatrocientos, ...) are understood by
speakers but carry a Portuguese flavour, so they are accepted when parsing text
and never produced when reading a number aloud.

Source: reviewed by a native central-dialect Mirandese speaker (2025-10-12).
"""
import unittest

from ovos_number_parser.numbers_mwl import MWL
from ovos_number_parser.util import GrammaticalGender


class TestMwlHundredsPronounce(unittest.TestCase):
    def test_round_hundreds(self):
        expected = {
            100: "cien",
            200: "dous cientos",
            300: "trés cientos",
            400: "quatro cientos",
            500: "cinco cientos",
            600: "seis cientos",
            700: "siete cientos",
            800: "uito cientos",
            900: "nuobe cientos",
        }
        for number, word in expected.items():
            with self.subTest(number=number):
                self.assertEqual(MWL.pronounce_number(number), word)

    def test_hundreds_with_remainder(self):
        self.assertEqual(MWL.pronounce_number(101), "ciento i un")
        self.assertEqual(MWL.pronounce_number(234), "dous cientos i trinta i quatro")
        self.assertEqual(MWL.pronounce_number(999), "nuobe cientos i nobenta i nuobe")

    def test_hundreds_after_a_larger_scale(self):
        self.assertEqual(MWL.pronounce_number(1234), "mil dous cientos i trinta i quatro")
        self.assertEqual(MWL.pronounce_number(1500), "mil cinco cientos")

    def test_feminine_hundreds(self):
        self.assertEqual(MWL.pronounce_number(200, gender=GrammaticalGender.FEMININE),
                         "dous cientas")


class TestMwlHundredsExtract(unittest.TestCase):
    def test_periphrastic_forms_are_read_back(self):
        for number in (100, 200, 234, 500, 999, 1234, 1500, 2_500_123_456):
            with self.subTest(number=number):
                self.assertEqual(MWL.extract_number(MWL.pronounce_number(number)), number)

    def test_synthetic_forms_still_parse(self):
        expected = {
            "un ciento": 100,
            "duzientos": 200,
            "trezientos": 300,
            "quatrocientos": 400,
            "quinhentos": 500,
            "seiscientos": 600,
            "sietecientos": 700,
            "uitocientos": 800,
            "nuobecientos": 900,
        }
        for text, number in expected.items():
            with self.subTest(text=text):
                self.assertEqual(MWL.extract_number(text), number)

    def test_synthetic_forms_in_a_phrase(self):
        self.assertEqual(MWL.extract_number("mil duzientos i trinta i quatro"), 1234)
        self.assertEqual(MWL.extract_number("dous milhones i quinhentos"), 2_000_500)

    def test_numbers_to_digits_accepts_both(self):
        self.assertEqual(MWL.numbers_to_digits("hai dous cientos i cinquenta carros"),
                         "hai 250 carros")
        self.assertEqual(MWL.numbers_to_digits("hai duzientos i cinquenta carros"),
                         "hai 250 carros")


if __name__ == "__main__":
    unittest.main()
