"""A comma or a sentence mark after a number word ends the number there.

The mark is not part of the word: "vinte e dois, disse ele" holds 22, as
"vinte e dois" does. Expected values are hand arithmetic.
"""
import unittest

from ovos_number_parser import extract_number, numbers_to_digits


class TestNumberEndMarks(unittest.TestCase):
    #: text, value, language tag
    ROWS = [("vinte e dois, disse ele", 20 + 2, "pt-PT"),
            ("dois milhões, disse", 2 * 10 ** 6, "pt-PT"),
            ("mil e quinhentos, talvez", 1000 + 500, "pt-BR"),
            ("um milhão e meio, disse ele", 10 ** 6 + 5 * 10 ** 5, "pt-PT"),
            ("dois e meio, mais ou menos", 2.5, "pt-PT"),
            ("três quartos, disse", 3 / 4, "pt-PT"),
            ("são vinte e dois?", 22, "pt-BR"),
            ("ganhou dois.", 2, "pt-PT"),
            # the mark ends the first number: the second is not added
            ("cento e vinte, cento e trinta", 100 + 20, "pt-PT"),
            ("um, dois, três", 1, "pt-PT"),
            ("vinte e dous, dixo", 22, "gl-ES")]

    def test_the_mark_ends_the_number(self):
        for text, value, lang in self.ROWS:
            with self.subTest(text=text, lang=lang):
                self.assertEqual(extract_number(text, lang=lang), value)

    def test_numbers_to_digits_keeps_the_mark(self):
        for text, digits, lang in [
                ("vinte e dois, disse ele", "22, disse ele", "pt-PT"),
                ("um milhão e meio, disse ele", "1500000, disse ele", "pt-PT"),
                ("cento e vinte, cento e trinta", "120, 130", "pt-PT"),
                ("são vinte e dois?", "são 22?", "pt-BR"),
                ("um, dois, três", "1, 2, 3", "pt-PT")]:
            with self.subTest(text=text, lang=lang):
                self.assertEqual(numbers_to_digits(text, lang=lang), digits)
