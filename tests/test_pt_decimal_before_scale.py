"""A decimal said before a scale word is a count of that scale.

"dois vírgula cinco milhões" is 2,5 milhões, 2500000. Só Matemática, "Como
ler números grandes (acima de 1 milhão)": "o correto é 1,4 milhão", and
"se escrevermos esse número por extenso, teremos "um milhão e quatrocentos
mil""; "Somente a partir de 2 é que a concordância é feita no plural: 2,5
milhões". The numbers_pt module docstring holds the quotes. Expected values
are hand arithmetic: the decimal times the scale.
"""
import unittest

from ovos_number_parser import extract_number, numbers_to_digits


class TestDecimalBeforeScale(unittest.TestCase):
    #: text, value, language tag
    ROWS = [("dois vírgula cinco milhões", 2 * 10 ** 6 + 5 * 10 ** 5, "pt-PT"),
            ("dois vírgula cinco milhões", 2 * 10 ** 6 + 5 * 10 ** 5, "pt-BR"),
            ("um vírgula quatro milhão", 10 ** 6 + 4 * 10 ** 5, "pt-BR"),
            ("um vírgula três dois milhões", 10 ** 6 + 32 * 10 ** 4, "pt-PT"),
            ("dois vírgula zero cinco milhões", 2 * 10 ** 6 + 5 * 10 ** 4,
             "pt-PT"),
            ("doze vírgula cinco milhões", 12 * 10 ** 6 + 5 * 10 ** 5,
             "pt-PT"),
            ("zero vírgula cinco milhões", 5 * 10 ** 5, "pt-PT"),
            ("um vírgula dois mil", 1200, "pt-PT"),
            # long scale: "mil milhões" is 10 ** 9 in pt-PT
            ("dois vírgula cinco mil milhões", 25 * 10 ** 8, "pt-PT"),
            # short scale: "bilhões" is 10 ** 9 in pt-BR
            ("dois vírgula cinco bilhões", 25 * 10 ** 8, "pt-BR"),
            ("dois vírgula cinco milhões de biliões", 25 * 10 ** 17, "pt-PT"),
            ("custou seis vírgula quatro milhões de euros",
             64 * 10 ** 5, "pt-PT")]

    def test_the_decimal_counts_the_scale(self):
        for text, value, lang in self.ROWS:
            with self.subTest(text=text, lang=lang):
                got = extract_number(text, lang=lang)
                self.assertEqual(got, value)
                self.assertIsInstance(got, int)

    def test_numbers_to_digits_keeps_the_scale(self):
        self.assertEqual(
            numbers_to_digits("custou seis vírgula quatro milhões de euros",
                              lang="pt-PT"),
            "custou 6400000 de euros")
        self.assertEqual(
            numbers_to_digits("dois vírgula cinco milhões de pessoas",
                              lang="pt-BR"),
            "2500000 de pessoas")

    def test_a_decimal_after_a_scale_is_unchanged(self):
        # the scale before the marker counts whole units, and the decimal
        # adds to them: 1000000 + 0.5
        self.assertEqual(extract_number("um milhão vírgula cinco",
                                        lang="pt-PT"), 1000000.5)
        self.assertEqual(extract_number("dois vírgula cinco", lang="pt-PT"),
                         2.5)
        # a scale word on both sides: the decimal digits after the marker
        # ("cinco mil", .5000) add to the million and multiply nothing
        self.assertEqual(extract_number("um milhão vírgula cinco mil",
                                        lang="pt-PT"), 1000000.5)
