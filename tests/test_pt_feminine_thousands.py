"""Portuguese cardinals in the feminine, from one thousand up.

Only "um", "dois" and the hundreds from "duzentos" inflect for gender
(linguagem.pt, "Numerais": "Um, dois e as centenas concordam em género com o
substantivo que contam"). "Mil" is an invariable numeral, so the count before
it agrees with the counted noun: "duas mil pessoas", "duzentas mil casas"
(elon.io, European Portuguese, "Cardinal Numbers 100+"; Só Português, FAQ 359:
"o numeral que a antecede deve ser flexionado de acordo com o gênero do
substantivo seguinte"). "Milhão" is a masculine noun, so its own count stays
masculine: "dois milhões de pessoas" (Só Português, FAQ 359). The group after
a scale word counts the noun too: Priberam "mil" gives "mil e uma artimanhas".
"""
import unittest

from ovos_number_parser import extract_number, pronounce_number
from ovos_number_parser.util import GrammaticalGender

FEM = GrammaticalGender.FEMININE
MASC = GrammaticalGender.MASCULINE

# number -> feminine reading, every row written from the sources above
GOLD = {
    18: "dezoito",
    818: "oitocentas e dezoito",
    1001: "mil e uma",
    2000: "duas mil",
    2002: "duas mil e duas",
    21000: "vinte e uma mil",
    200000: "duzentas mil",
    201000: "duzentas e uma mil",
    1000001: "um milhão e uma",
    2000000: "dois milhões",
}

# the only words whose form changes with gender
FEMININE_ONLY = {"uma", "duas", "duzentas", "trezentas", "quatrocentas",
                 "quinhentas", "seiscentas", "setecentas", "oitocentas",
                 "novecentas"}


class TestPortugueseFeminineThousands(unittest.TestCase):
    def test_gold(self):
        for lang in ("pt-PT", "pt-BR"):
            for number, said in GOLD.items():
                with self.subTest(lang=lang, number=number):
                    self.assertEqual(
                        pronounce_number(number, lang=lang, gender=FEM), said)

    def test_masculine_count_before_milhao(self):
        for lang in ("pt-PT", "pt-BR"):
            with self.subTest(lang=lang):
                said = pronounce_number(2200000, lang=lang, gender=FEM)
                self.assertTrue(said.startswith("dois milhões "), said)
                self.assertTrue(said.endswith("duzentas mil"), said)

    def test_only_the_inflecting_words_change(self):
        """A feminine reading differs from the masculine one only where the
        masculine word is the counterpart of a FEMININE_ONLY word."""
        numbers = list(range(1000, 3100)) + [10 ** 6 + n for n in range(0, 2000, 7)] \
            + [123456, 234567, 987654321, 1818818]
        for lang in ("pt-PT", "pt-BR"):
            for number in numbers:
                masc = pronounce_number(number, lang=lang, gender=MASC).split()
                fem = pronounce_number(number, lang=lang, gender=FEM).split()
                with self.subTest(lang=lang, number=number):
                    self.assertEqual(len(masc), len(fem))
                    for m, f in zip(masc, fem):
                        if m != f:
                            self.assertIn(f, FEMININE_ONLY)

    def test_round_trip(self):
        for lang in ("pt-PT", "pt-BR"):
            for number in list(GOLD) + [2345678, 999999]:
                said = pronounce_number(number, lang=lang, gender=FEM)
                with self.subTest(lang=lang, said=said):
                    self.assertEqual(extract_number(said, lang=lang), number)


if __name__ == "__main__":
    unittest.main()
