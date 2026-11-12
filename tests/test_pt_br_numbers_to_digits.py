"""numbers_to_digits reads Brazilian Portuguese with the pt-BR vocabulary.

Priberam, "bilhão", sense 2: "[Brasil, Informal] Mil milhões (10^9)."
extract_number already reads it so for pt-BR; numbers_to_digits must agree.
"""
import unittest

from ovos_number_parser import extract_number, numbers_to_digits


class TestPtBrNumbersToDigits(unittest.TestCase):
    cases = {
        "a cidade tem um bilhão de habitantes":
            "a cidade tem 1000000000 de habitantes",
        "custou dois bilhões de reais": "custou 2000000000 de reais",
    }

    def test_br_vocabulary(self):
        for lang in ("pt-BR", "pt-br", "pt_BR"):
            for text, expected in self.cases.items():
                with self.subTest(lang=lang, text=text):
                    self.assertEqual(numbers_to_digits(text, lang), expected)

    def test_agrees_with_extract_number(self):
        self.assertEqual(extract_number("um bilhão", "pt-BR"), 10 ** 9)
        self.assertEqual(numbers_to_digits("um bilhão", "pt-BR"), str(10 ** 9))

    def test_pt_pt_unchanged(self):
        self.assertEqual(numbers_to_digits("um bilião de euros", "pt-PT"),
                         "1000000000000 de euros")


if __name__ == "__main__":
    unittest.main()
