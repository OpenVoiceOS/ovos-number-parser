"""Spanish cardinals above 999 agree with a feminine noun.

Expected values come from these sources:

- RAE and ASALE, *Diccionario panhispánico de dudas*, "uno" § 2.3: "Los
  numerales uno, una y sus compuestos concuerdan en género con el sustantivo
  al que acompañan cuando lo preceden inmediatamente: treinta y un kilos,
  veintiuna toneladas". Before "mil" the feminine is optional for "uno" and
  its compounds, and "se está imponiendo" ("cuarenta y una mil pesetas"). It
  is obligatory for the hundreds: "setecientas mil toneladas (no
  setecientos mil toneladas)".
- "uno" § 2.2: before a masculine noun "uno" and its compounds take "un"
  ("Tengo veintiún años").
- RAE, *Diccionario de la lengua española*, "doscientos, doscientas": "Es un
  teatro con un aforo de doscientas personas".
- DLE, "millón": "m. Mil millares", a masculine noun, so the count before
  "millón" stays masculine whatever noun follows.
"""
import unittest

from ovos_number_parser import pronounce_number
from ovos_number_parser.util import GrammaticalGender


class TestSpanishFeminineAboveThousand(unittest.TestCase):
    def assertReads(self, cases, gender):
        for number, expected in cases:
            with self.subTest(number=number, gender=gender.name):
                self.assertEqual(
                    pronounce_number(number, "es-ES", gender=gender), expected)

    def test_group_after_mil_agrees(self):
        # "mil una noches", "mil doscientas personas"
        self.assertReads([
            (1001, "mil una"),
            (1021, "mil veintiuna"),
            (1200, "mil doscientas"),
            (2500, "dos mil quinientas"),
            (1000001, "un millón una"),
            (2001200, "dos millones mil doscientas"),
        ], GrammaticalGender.FEMININE)

    def test_count_before_mil_agrees(self):
        # "setecientas mil toneladas", "cuarenta y una mil pesetas"
        self.assertReads([
            (700000, "setecientas mil"),
            (200000, "doscientas mil"),
            (41000, "cuarenta y una mil"),
            (21000, "veintiuna mil"),
        ], GrammaticalGender.FEMININE)

    def test_count_before_millon_stays_masculine(self):
        # "doscientos millones de personas": millón is a masculine noun
        self.assertReads([
            (200000000, "doscientos millones"),
            (21000000, "veintiún millones"),
            (200 * 10 ** 15, "doscientos mil billones"),
        ], GrammaticalGender.FEMININE)

    def test_masculine_keeps_its_forms(self):
        self.assertReads([
            (1001, "mil uno"),
            (1200, "mil doscientos"),
            (700000, "setecientos mil"),
            (21000, "veintiún mil"),
        ], GrammaticalGender.MASCULINE)

    def test_apocope_inside_a_count_before_a_scale_noun(self):
        # 1001 x 10**12 is "mil un billones", as "veintiún años"
        self.assertReads([
            (1001 * 10 ** 12, "mil un billones"),
        ], GrammaticalGender.MASCULINE)


if __name__ == "__main__":
    unittest.main()
