"""Italian ordinals from pronounce_number(..., ordinals=True) and pronounce_ordinal.

Expected values come from these sources:

- Treccani, *La grammatica italiana* (2012), "Ordinali, aggettivi numerali":
  "I primi dieci ordinali presentano una forma propria derivata dal latino:
  primo, secondo, terzo, quarto, quinto, sesto, settimo, ottavo, nono,
  decimo. Da undicesimo in poi, invece, si formano con il suffisso -esimo
  aggiunto all'aggettivo numerale cardinale senza la vocale finale sedici ▶
  sedicesimo ventiquattro ▶ ventiquattresimo trentotto ▶ trentottesimo Nei
  composti con tre la -e finale si conserva ventitré ▶ ventitreesimo
  trentatré ▶ trentatreesimo Nei composti con sei la -i finale si conserva
  ventisei ▶ ventiseiesimo". The same page: "Sono variabili in genere e
  numero il decimo posto, la decima puntata".
- Treccani, *Vocabolario*: "-esimo" ("Suffisso dei numerali ordinali:
  undicesimo, dodicesimo, ventesimo, ecc. [...] 0-esimo (zeresimo, di posto
  zero)"); "ventesimo" ("Gli ordinali successivi sono: ventunèsimo,
  ventiduèsimo, ..."); "centesimo" ("centesimo primo (o, più com.,
  centunesimo), centesimo secondo (o, più com., centoduesimo)");
  "tremillesimo" ("der. di tremila, secondo l'agg. millesimo");
  "centomillesimo"; "millesimo"; "milionesimo"; "miliardesimo"; "bilionesimo".
- CLDR RBNF it, spellout-ordinal-masculine: 110 "centodecimo", 2000
  "duemillesimo", 2000000 "duemilionesimo".
"""
import unittest

from ovos_number_parser import pronounce_number, pronounce_ordinal
from ovos_number_parser.util import GrammaticalGender

FEMININE = GrammaticalGender.FEMININE


class TestItalianOrdinals(unittest.TestCase):
    def assertOrdinal(self, cases, gender=GrammaticalGender.MASCULINE,
                      routed=True):
        for number, expected in cases:
            with self.subTest(number=number, gender=gender.name):
                self.assertEqual(
                    pronounce_number(number, "it", ordinals=True,
                                     gender=gender), expected)
                if routed:
                    self.assertEqual(
                        pronounce_ordinal(number, "it", gender=gender),
                        expected)

    def test_first_ten(self):
        self.assertOrdinal([
            (1, "primo"), (2, "secondo"), (3, "terzo"), (4, "quarto"),
            (5, "quinto"), (6, "sesto"), (7, "settimo"), (8, "ottavo"),
            (9, "nono"), (10, "decimo")])

    def test_zero(self):
        self.assertOrdinal([(0, "zeresimo")])

    def test_cardinal_without_final_vowel(self):
        self.assertOrdinal([
            (11, "undicesimo"), (12, "dodicesimo"), (16, "sedicesimo"),
            (20, "ventesimo"), (21, "ventunesimo"), (22, "ventiduesimo"),
            (24, "ventiquattresimo"), (30, "trentesimo"),
            (38, "trentottesimo"), (90, "novantesimo"), (100, "centesimo"),
            (101, "centunesimo"), (102, "centoduesimo")])

    def test_tre_and_sei_keep_the_final_vowel(self):
        self.assertOrdinal([
            (23, "ventitreesimo"), (33, "trentatreesimo"),
            (26, "ventiseiesimo")])

    def test_thousands_follow_millesimo(self):
        self.assertOrdinal([
            (1000, "millesimo"), (2000, "duemillesimo"),
            (3000, "tremillesimo"), (100000, "centomillesimo")])

    def test_final_ten(self):
        self.assertOrdinal([(110, "centodecimo")])

    def test_feminine(self):
        self.assertOrdinal([
            (1, "prima"), (10, "decima"), (21, "ventunesima"),
            (23, "ventitreesima"), (3000, "tremillesima")], gender=FEMININE)

    def test_scale_words(self):
        # pronounce_ordinal keeps the CLDR reading from a million up
        self.assertOrdinal([
            (10 ** 6, "milionesimo"), (2 * 10 ** 6, "duemilionesimo"),
            (10 ** 9, "miliardesimo"), (10 ** 12, "bilionesimo")],
            routed=False)

    def test_cardinal_unchanged(self):
        self.assertEqual(pronounce_number(23, "it"), "ventitré")
        self.assertEqual(pronounce_number(3000, "it"), "tremila")


if __name__ == "__main__":
    unittest.main()
