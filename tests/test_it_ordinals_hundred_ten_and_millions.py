"""Italian ordinals of a hundred and ten, and of a million and above.

Gold values are worked by hand from these sources:

- Treccani, Vocabolario, "ordinale": the type that joins the ordinal of the
  hundred or thousand to the ordinal of the rest "è pressoché l'unico per
  alcuni ordinali per i quali l'altro tipo sarebbe sentito come poco
  eufonico: centesimo decimo, millesimo primo, millesimo secondo, millesimo
  decimo, millesimo undecimo o undicesimo, ecc. (in questi casi la grafia
  staccata è preferita)".
- Treccani, Vocabolario, "centesimo": "centesimo primo (o, più com.,
  centunesimo), centesimo secondo (o, più com., centoduesimo)".
- CLDR RBNF it, spellout-ordinal-masculine, for a million and above (worked
  out in test_it_native_ordinals): the count, the singular scale word and the
  ordinal of the rest in one word. No source settles the scale word of a
  compound ordinal, so the engine form stays.
"""
import unittest

from ovos_number_parser import pronounce_number, pronounce_ordinal
from ovos_number_parser.util import GrammaticalGender

MASCULINE = GrammaticalGender.MASCULINE
FEMININE = GrammaticalGender.FEMININE


class TestOrdinalsEndingInTen(unittest.TestCase):
    def assertOrdinals(self, cases, gender=MASCULINE):
        for number, expected in cases:
            with self.subTest(number=number, gender=gender.name):
                self.assertEqual(
                    pronounce_ordinal(number, "it", gender=gender), expected)
                self.assertEqual(
                    pronounce_number(number, "it", ordinals=True,
                                     gender=gender), expected)

    def test_hundred_and_ten(self):
        self.assertOrdinals([
            (110, "centesimo decimo"), (210, "duecentesimo decimo"),
            (910, "novecentesimo decimo"),
            (1110, "millecentesimo decimo"),
            (2010, "duemillesimo decimo"),
            (100010, "centomillesimo decimo")])

    def test_hundred_and_ten_feminine(self):
        self.assertOrdinals([
            (110, "centesima decima"), (310, "trecentesima decima"),
            (1110, "millecentesima decima")], gender=FEMININE)

    def test_sentence(self):
        self.assertEqual(
            f"Il {pronounce_ordinal(110, 'it')} giorno dell'anno.",
            "Il centesimo decimo giorno dell'anno.")

    def test_neighbours_keep_one_word(self):
        self.assertOrdinals([
            (10, "decimo"), (100, "centesimo"), (101, "centunesimo"),
            (109, "centonovesimo"), (111, "centoundicesimo"),
            (120, "centoventesimo"), (1000, "millesimo")])

    def test_inside_a_scale_word_the_tail_stays_fused(self):
        self.assertOrdinals([(1000110, "milionecentodecimo")])


class TestOrdinalsFromAMillion(unittest.TestCase):
    CASES = [(10 ** 6, "milionesimo", "milionesima"),
             (2 * 10 ** 6, "duemilionesimo", "duemilionesima"),
             (3500000, "tremilionecinquecentomillesimo",
              "tremilionecinquecentomillesima"),
             (21 * 10 ** 6, "ventunmilionesimo", "ventunmilionesima"),
             (10 ** 9, "miliardesimo", "miliardesima"),
             (10 ** 9 + 1001, "miliardomilleunesimo",
              "miliardomilleunesima"),
             (10 ** 12, "bilionesimo", "bilionesima")]

    def test_pronounce_ordinal_reads_the_engine(self):
        for number, masculine, feminine in self.CASES:
            with self.subTest(number=number):
                self.assertEqual(pronounce_ordinal(number, "it"), masculine)
                self.assertEqual(
                    pronounce_ordinal(number, "it", gender=FEMININE), feminine)

    def test_both_functions_agree(self):
        for number, _, _ in self.CASES + [(10 ** 40, "", "")]:
            for gender in (MASCULINE, FEMININE):
                with self.subTest(number=number, gender=gender.name):
                    self.assertEqual(
                        pronounce_ordinal(number, "it", gender=gender),
                        pronounce_number(number, "it", ordinals=True,
                                         gender=gender))

    def test_feminine_agrees_in_gender(self):
        # the fallback gave "ventunamilionesima"
        self.assertNotIn("ventuna", pronounce_ordinal(
            21 * 10 ** 6, "it", gender=FEMININE))


if __name__ == "__main__":
    unittest.main()
