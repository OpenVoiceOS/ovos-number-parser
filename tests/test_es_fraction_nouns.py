"""Spanish fractions read with the fraction noun (sustantivo fraccionario).

Expected values come from RAE and ASALE, *Diccionario panhispánico de dudas*,
2nd ed., entries "fraccionarios" and "uno":

- "fraccionarios" § 1 is a table of the forms ("treintavo o trigésimo",
  "cincuentaiseisavo", "doscientosavo o ... ducentésimo", "dosmilésimo",
  "milmillonésimo").
- § 2: "El resto se forma hoy añadiendo el sufijo -ava al numeral cardinal
  escrito en una sola palabra: treceava, catorceava, cientounava,
  doscientostreintaiunava". For tens and multiples of a hundred the -avo
  form is preferred: the ordinal forms "son de raro uso hoy" (§ 3 c).
- § 3 c): the noun is masculine, "veintiunavo, veintiunava (parte)"; § 3
  gives the plural "Dos tercios de los presentes".
- § 5: a cardinal in -a loses it ("cincuentavo"), one in -e or -o keeps it.
- "uno" § 2.2: "uno" before a masculine noun is "un", also inside compounds
  ("veintiún años").
"""
import unittest

from ovos_number_parser import pronounce_fraction, pronounce_number


class TestSpanishFractionNouns(unittest.TestCase):
    def assertReads(self, cases):
        for fraction, expected in cases:
            with self.subTest(fraction=fraction):
                self.assertEqual(pronounce_fraction(fraction, "es-ES"), expected)

    def test_dpd_table_denominators(self):
        # one noun per row of the "fraccionarios" § 1 table, first form
        self.assertReads([
            ("1/30", "un treintavo"),
            ("1/56", "un cincuentaiseisavo"),
            ("1/100", "un centésimo"),
            ("1/200", "un doscientosavo"),
            ("1/300", "un trescientosavo"),
            ("1/1000", "un milésimo"),
            ("1/2000", "un dosmilésimo"),
            ("1/3000", "un tresmilésimo"),
            ("1/10000", "un diezmilésimo"),
            ("1/100000", "un cienmilésimo"),
            ("1/1000000", "un millonésimo"),
            ("1/10000000", "un diezmillonésimo"),
            ("1/100000000", "un cienmillonésimo"),
            ("1/1000000000", "un milmillonésimo"),
            ("1/10000000000", "un diezmilmillonésimo"),
        ])

    def test_dpd_text_examples(self):
        # "veintiunavo" (§ 3 c), "cientounava", "doscientostreintaiunava" (§ 2)
        self.assertReads([
            ("1/21", "un veintiunavo"),
            ("1/101", "un cientounavo"),
            ("1/231", "un doscientostreintaiunavo"),
            ("1/500", "un quinientosavo"),
        ])

    def test_plural_after_numerator_other_than_one(self):
        self.assertReads([
            ("7/30", "siete treintavos"),
            ("3/1000", "tres milésimos"),
            ("2/21", "dos veintiunavos"),
            ("5/56", "cinco cincuentaiseisavos"),
        ])

    def test_numerator_apocope_before_the_noun(self):
        # "Tengo veintiún años", "treinta y un kilos"
        self.assertReads([
            ("21/50", "veintiún cincuentavos"),
            ("31/40", "treinta y un cuarentavos"),
        ])

    def test_suffix_joins_by_the_final_letter(self):
        # § 5: -a is dropped, -e and -o stay, the cardinal is one word
        self.assertReads([
            ("1/40", "un cuarentavo"),
            ("1/24", "un veinticuatroavo"),
            ("1/25", "un veinticincoavo"),
            ("1/27", "un veintisieteavo"),
            ("1/22", "un veintidosavo"),
            ("1/99", "un noventainueveavo"),
        ])

    def test_table_denominators_keep_their_reading(self):
        self.assertReads([
            ("1/2", "un medio"),
            ("2/3", "dos tercios"),
            ("3/4", "tres cuartos"),
            ("1/20", "un veinteavo"),
        ])

    def test_numerator_beyond_the_scale_words(self):
        # 10**43 has no scale word, so the numerator keeps its scientific
        # reading; the noun after it is still the plural fraction noun
        numerator = 10 ** 43
        self.assertEqual(pronounce_fraction(f"{numerator}/30", "es-ES"),
                         f"{pronounce_number(numerator, 'es-ES')} treintavos")

    def test_negative_fraction(self):
        self.assertReads([("-1/30", "menos un treintavo"),
                          ("7/-30", "menos siete treintavos")])


if __name__ == "__main__":
    unittest.main()
