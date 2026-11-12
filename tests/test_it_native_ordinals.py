"""Italian ordinals from pronounce_number(..., ordinals=True) and pronounce_ordinal.

Expected values come from these sources:

- Treccani, *Vocabolario*: "-esimo" ("Suffisso dei numerali ordinali:
  undicesimo, dodicesimo, ventesimo, ecc. (a eccezione dei primi numeri, da 1
  a 10). [...] 0-esimo (zeresimo, di posto zero)"); "ventesimo" ("Gli
  ordinali successivi sono: ventunèsimo, ventiduèsimo, ... ventiseèsimo (o
  ventiseièsimo), ecc."); "centesimo" ("centesimo primo (o, più com.,
  centunesimo), centesimo secondo (o, più com., centoduesimo)");
  "tremillesimo" ("der. di tremila, secondo l'agg. millesimo");
  "centomillesimo"; "millesimo"; "milionesimo" ("(f. -a)"); "miliardesimo";
  "bilionesimo". Treccani gives "ventiseèsimo" first and "ventiseièsimo" as
  the second form; the engine writes the second, as CLDR does.
- CLDR RBNF it, spellout-ordinal-masculine: "20: vent→%%ordinal-esimo-with-i→"
  with "3: itreesimo", "6: iseiesimo", "8: ottesimo"; 110 "centodecimo",
  2000 "duemillesimo"; "1000000: milione→%%ordinal-esimo→",
  "2000000: ←%spellout-cardinal-masculine←milione→%%ordinal-esimo→",
  "1000000000: miliard→%%ordinal-esimo-with-o→", with "%%ordinal-esimo"
  giving "simo" for 0, "treesimo" for 3 and the ordinal itself from 10, and
  "%%ordinal-esimo-with-o" giving "esimo", "unesimo", "otreesimo",
  "ottesimo" and "o" before the ordinal from 10. The count before
  "milione" is %spellout-cardinal-masculine: "20: vent→%%msc-with-i→" with
  "1: un" ("ventun") and "100: cent→%%msc-with-o→" with "1: ouno"
  ("centouno"). The values from a million
  up are worked by hand from these rules; unicode_rbnf gives the same for
  1000003, 1000023, 1000100, 2000003 and 10^9 + 3.
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

    def test_from_a_million_one_word(self):
        # pronounce_ordinal keeps the CLDR reading from a million up
        self.assertOrdinal([
            (1000001, "milioneunesimo"), (1000003, "milionetreesimo"),
            (1000008, "milioneottesimo"), (1000010, "milionedecimo"),
            (1000023, "milioneventitreesimo"),
            (1000100, "milionecentesimo"), (1001000, "milionemillesimo"),
            (1234567, "milioneduecentotrentaquattromila"
                      "cinquecentosessantasettesimo"),
            (2000003, "duemilionetreesimo"),
            (21 * 10 ** 6, "ventunmilionesimo"),
            (23 * 10 ** 6, "ventitremilionesimo"),
            (101 * 10 ** 6, "centounomilionesimo"),
            (10 ** 9 + 1, "miliardunesimo"), (10 ** 9 + 3, "miliardotreesimo"),
            (10 ** 9 + 8, "miliardottesimo"),
            (10 ** 9 + 23, "miliardoventitreesimo"),
            (10 ** 9 + 10 ** 6, "miliardomilionesimo"),
            (10 ** 12 + 5, "bilionecinquesimo")], routed=False)
        self.assertOrdinal([(1000003, "milionetreesima")], gender=FEMININE,
                           routed=False)

    def test_cardinal_unchanged(self):
        self.assertEqual(pronounce_number(23, "it"), "ventitré")
        self.assertEqual(pronounce_number(3000, "it"), "tremila")


if __name__ == "__main__":
    unittest.main()
