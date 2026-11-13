"""Portuguese "bilhão" and "bilião" are two spellings of one word.

Ciberdúvidas, answer 30031 ("As grafias e as pronúncias de bilião e
bilhão"): "ambas as formas — bilião e bilhão — se encontram registadas",
and "bilhão" is of informal use "apesar de significar o mesmo que bilião".
The same holds for "trilhão/trilião" and "quatrilhão/quatrilião". Priberam,
"bilhão", sense 1: "[Informal] Um milhão de milhões (10^12)", synonym
"BILIÃO"; Priberam, "bilião", sense 2: "[Brasil] Mil milhões (10^9)".
So each variety reads the other spelling with its own value: 10^12 in pt-PT
(long scale), 10^9 in pt-BR (short scale). Expected values are powers of
ten written by hand.
"""
import unittest

from ovos_number_parser import extract_number, numbers_to_digits
from ovos_number_parser.numbers_pt import PT_PT
from ovos_number_parser.util import Scale


class TestBilhaoSpelling(unittest.TestCase):
    #: text, value, language tag
    ROWS = [("um bilhão", 10 ** 12, "pt-PT"),
            ("dois bilhões", 2 * 10 ** 12, "pt-PT"),
            ("um trilhão", 10 ** 18, "pt-PT"),
            ("três quatrilhões", 3 * 10 ** 24, "pt-PT"),
            ("um bilhão e meio", 15 * 10 ** 11, "pt-PT"),
            ("um bilião", 10 ** 9, "pt-BR"),
            ("dois biliões", 2 * 10 ** 9, "pt-BR"),
            ("um trilião", 10 ** 12, "pt-BR")]

    def test_extract_number(self):
        for text, value, lang in self.ROWS:
            with self.subTest(text=text, lang=lang):
                self.assertEqual(extract_number(text, lang=lang), value)

    def test_numbers_to_digits(self):
        for text, expected, lang in [
                ("custou dois bilhões de euros", "custou 2000000000000 de euros",
                 "pt-PT"),
                ("a cidade tem um bilião de habitantes",
                 "a cidade tem 1000000000 de habitantes", "pt-BR")]:
            with self.subTest(text=text, lang=lang):
                self.assertEqual(numbers_to_digits(text, lang=lang), expected)

    def test_the_spelling_follows_the_scale(self):
        # under the short scale "bilião" is 10^9 in pt-PT; so is "bilhão"
        self.assertEqual(PT_PT.extract_number("um bilhão", scale=Scale.SHORT),
                         10 ** 9)

    def test_milhao_has_one_spelling(self):
        # Ciberdúvidas, answer 30031, names the pairs from "bilião" up;
        # "milião" is no spelling of "milhão"
        self.assertEqual(extract_number("um milião", lang="pt-BR"), 1)
        self.assertEqual(extract_number("um milhão", lang="pt-BR"), 10 ** 6)

    def test_writing_keeps_the_variety_spelling(self):
        self.assertEqual(numbers_to_digits("um bilião", lang="pt-PT"),
                         "1000000000000")
        self.assertIn("bilião", PT_PT.pronounce_number(10 ** 12))


if __name__ == "__main__":
    unittest.main()
