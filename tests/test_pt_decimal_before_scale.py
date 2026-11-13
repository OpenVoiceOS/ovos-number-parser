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

    def test_a_scale_word_later_in_the_sentence_counts_nothing(self):
        # the decimal part is the run of number words right after the
        # marker: "anos" and "quilos" end the number at 2.5
        for text in ("tenho dois vírgula cinco anos e mil euros",
                     "dois vírgula cinco quilos e um milhão de vezes",
                     "dois vírgula cinco quilos e três"):
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, lang="pt-PT"), 2.5)
        self.assertEqual(
            extract_number("dois vírgula vinte e cinco milhões", lang="pt-PT"),
            2 * 10 ** 6 + 25 * 10 ** 4)

    def test_the_number_ends_after_the_scale_word(self):
        # a joiner after the scale run starts a second number, in both
        # functions: 2,5 milhões and then 3
        self.assertEqual(
            extract_number("dois vírgula cinco milhões e três", lang="pt-PT"),
            25 * 10 ** 5)
        for text, digits in [("dois vírgula cinco milhões e três",
                              "2500000 e 3"),
                             ("zero vírgula um mil e três", "100 e 3")]:
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, lang="pt-PT"), digits)

    def test_a_composed_decimal_keeps_its_joiner(self):
        # the joiner inside "noventa e nove" belongs to the decimal: 42.99
        for text, digits in [
                ("quarenta e dois vírgula noventa e nove euros",
                 "42.99 euros"),
                ("doze vírgula trinta e cinco", "12.35"),
                ("dois vírgula vinte e cinco milhões", "2250000"),
                # "cinco e três" is no compound: 2.5 and then 3
                ("dois vírgula cinco e três", "2.5 e 3"),
                # a compound descends: "vinte e trinta" is two numbers
                ("dois vírgula vinte e trinta", "2.2 e 30")]:
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, lang="pt-PT"), digits)

    def test_a_scale_word_after_a_joiner_is_a_second_number(self):
        # "e mil" after the decimal is another number: the decimal is 2.5
        for text, value in [("entre dois vírgula cinco e mil", 2.5),
                            ("dois vírgula cinco e três", 2.5),
                            ("custa entre um vírgula cinco e dois mil euros",
                             1.5)]:
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, lang="pt-PT"), value)

    def test_a_decimal_sums_without_a_float_error(self):
        # 7 + 0.94 in binary floats is 7.9399999999999995
        self.assertEqual(extract_number("sete vírgula noventa e quatro",
                                        lang="pt-PT"), 7.94)
        self.assertEqual(numbers_to_digits("sete vírgula noventa e quatro",
                                           lang="pt-PT"), "7.94")

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
