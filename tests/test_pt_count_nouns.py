"""Collective nouns count groups of a fixed size.

Priberam: "dezena" is "Grupo de dez.", "dúzia" is "Conjunto de doze." and
"meia dúzia" is "Conjunto de seis.", "centena" is "Conjunto de 100
elementos.". The numbers_pt module docstring holds the quotes. Expected
values are hand arithmetic: the count times the group size.
"""
import unittest

from ovos_number_parser import extract_number, numbers_to_digits


class TestCountNouns(unittest.TestCase):
    #: text, value
    ROWS = [("uma dúzia de ovos", 12),
            ("duas dúzias", 2 * 12),
            ("meia dúzia de ovos", 12 // 2),
            ("dúzia e meia", 12 + 12 // 2),
            ("duas dúzias e meia", 2 * 12 + 12 // 2),
            ("doze dúzias", 12 * 12),
            ("cento e vinte dúzias", 120 * 12),
            ("mil e duas dúzias", 1000 + 2 * 12),
            ("uma dúzia e três", 12 + 3),
            ("um milhão e meia dúzia", 10 ** 6 + 12 // 2),
            ("meio milhão e meia dúzia", 10 ** 6 // 2 + 12 // 2),
            ("uma dezena de dias", 10),
            ("três dezenas", 3 * 10),
            ("uma centena de pessoas", 100),
            ("duas centenas", 2 * 100)]

    def test_the_count_multiplies_the_group(self):
        for lang in ("pt-PT", "pt-BR"):
            for text, value in self.ROWS:
                with self.subTest(text=text, lang=lang):
                    got = extract_number(text, lang=lang)
                    self.assertEqual(got, value)
                    self.assertIsInstance(got, int)

    def test_a_plural_with_no_count_is_no_number(self):
        for text in ("dúzias de ovos", "centenas de pessoas",
                     "dezenas de carros"):
            with self.subTest(text=text):
                self.assertFalse(extract_number(text, lang="pt-PT"))
                self.assertEqual(numbers_to_digits(text, lang="pt-PT"), text)

    def test_numbers_to_digits_writes_the_group(self):
        for text, digits in [("uma dúzia de ovos", "12 de ovos"),
                             ("meia dúzia de ovos", "6 de ovos"),
                             ("dúzia e meia de ovos", "18 de ovos"),
                             ("duas dúzias e meia", "30"),
                             ("um milhão e meia dúzia", "1000006"),
                             ("três dezenas de carros", "30 de carros")]:
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, lang="pt-PT"), digits)

    def test_a_half_before_a_scale_noun_is_a_whole_number(self):
        # half of a thousand is 500 units, written without a decimal part
        for text, digits in [("meio milhar de euros", "500 de euros"),
                             ("meio milhão de pessoas", "500000 de pessoas")]:
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, lang="pt-PT"), digits)
                self.assertIsInstance(extract_number(text, lang="pt-PT"), int)


class TestDecimalBeforeCountNoun(unittest.TestCase):
    def test_a_decimal_counts_the_group(self):
        # as before a scale word ("dois vírgula cinco milhões"), the decimal
        # times the group size
        for text, value, digits in [
                ("dois vírgula cinco dúzias", 30, "30"),
                ("um vírgula cinco centenas", 150, "150"),
                ("dois vírgula cinco dezenas de pessoas", 25, "25 de pessoas"),
                # the noun counts the whole compound, not its unit
                ("dois vírgula vinte e cinco centenas", 225, "225")]:
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, lang="pt-PT"), value)
                self.assertEqual(numbers_to_digits(text, lang="pt-PT"), digits)

    def test_a_decimal_after_a_scale_does_not_count_the_group(self):
        # a scale word before the marker keeps the plain decimal, so the
        # collective noun counts nothing and stays text
        for text, value, digits in [
                ("um milhão vírgula cinco dúzias", 1000000.5,
                 "1000000.5 dúzias"),
                ("mil vírgula cinco dúzias de ovos", 1000.5,
                 "1000.5 dúzias de ovos")]:
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, lang="pt-PT"), value)
                self.assertEqual(numbers_to_digits(text, lang="pt-PT"), digits)

    def test_a_half_before_a_plural_stays_text(self):
        # a half halves one group, so before a plural it builds no number
        for text, digits in [
                ("meio milhões de pessoas", "meio milhões de pessoas"),
                ("dois e meio milhares de pessoas",
                 "2 e meio milhares de pessoas"),
                ("meias dúzias de ovos", "meias dúzias de ovos")]:
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, lang="pt-PT"), digits)

    def test_a_marker_before_a_collective_noun_stays_text(self):
        # no number word follows the marker, so no decimal starts there
        self.assertEqual(
            numbers_to_digits("custou dois vírgula dúzias de ovos", lang="pt-PT"),
            "custou 2 vírgula dúzias de ovos")
