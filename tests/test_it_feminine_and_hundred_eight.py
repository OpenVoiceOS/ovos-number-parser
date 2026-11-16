"""Italian feminine "una", "centootto" and the ordinals after "millesimo".

Gold values are worked by hand from these sources:

- Treccani, Enciclopedia dell'Italiano, "Numerali": "uno [...] al femminile
  assume la forma una"; "con cento seguito da una decina o da un'unità,
  l'elisione è poco comune con uno, otto e undici [...] centootto [raramente
  centotto]".
- Treccani, Vocabolario, "uno": "ventuna pagina, le mille e una notte,
  centouna volte".
- Accademia della Crusca, consulenza 1077: "108: centootto, meno bene
  centotto"; "180: centottanta o centoottanta"; "21.000: ventunomila o
  ventunmila: entrambe le forme vanno bene".
- Treccani, Vocabolario, "ordinale": "centesimo decimo, millesimo primo,
  millesimo secondo, millesimo decimo, millesimo undecimo o undicesimo".
"""
import unittest

from ovos_number_parser import pronounce_number, pronounce_ordinal
from ovos_number_parser.util import GrammaticalGender

FEMININE = GrammaticalGender.FEMININE


def feminine(number):
    return pronounce_number(number, "it", gender=FEMININE)


class TestFeminineOne(unittest.TestCase):
    def test_one_before_a_feminine_noun(self):
        self.assertEqual(f"{feminine(1)} volta", "una volta")
        self.assertEqual(f"Ho letto {feminine(1)} pagina.",
                         "Ho letto una pagina.")

    def test_compounds_ending_in_one(self):
        # Treccani, "uno": "ventuna pagina", "centouna volte"
        self.assertEqual(f"{feminine(21)} pagina", "ventuna pagina")
        self.assertEqual(f"{feminine(101)} volte", "centouna volte")
        self.assertEqual(feminine(31), "trentuna")
        self.assertEqual(feminine(121), "centoventuna")
        self.assertEqual(feminine(1001), "milleuna")
        self.assertEqual(feminine(2001), "duemilauna")
        self.assertEqual(feminine(101001), "centounomilauna")

    def test_negative(self):
        self.assertEqual(feminine(-1), "meno una")
        self.assertEqual(feminine(-21), "meno ventuna")

    def test_after_a_million(self):
        self.assertEqual(feminine(1000001), "un milione una")
        self.assertEqual(feminine(2000021), "due milioni ventuna")

    def test_masculine_is_unchanged(self):
        self.assertEqual(pronounce_number(1, "it"), "uno")
        self.assertEqual(pronounce_number(21, "it"), "ventuno")
        self.assertEqual(pronounce_number(101, "it"), "centouno")
        self.assertEqual(pronounce_number(21, "it",
                                          gender=GrammaticalGender.NEUTRAL),
                         "ventuno")

    def test_other_numbers_keep_their_form(self):
        self.assertEqual(feminine(11), "undici")
        self.assertEqual(feminine(2), "due")
        self.assertEqual(feminine(23), "ventitré")
        self.assertEqual(feminine(10), "dieci")

    def test_a_scale_word_stays_masculine(self):
        self.assertEqual(feminine(21000), "ventunomila")
        self.assertEqual(feminine(21000000), "ventuno milioni")
        self.assertEqual(feminine(1000000), "un milione")

    def test_decimals_keep_uno(self):
        self.assertEqual(feminine(1.5), "uno virgola cinque")


class TestCentoOtto(unittest.TestCase):
    def test_hundreds_keep_o_before_otto(self):
        for number, expected in [
                (108, "centootto"), (208, "duecentootto"),
                (308, "trecentootto"), (908, "novecentootto"),
                (1108, "millecentootto"), (108000, "centoottomila"),
                (100008, "centomilaotto")]:
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, "it"), expected)

    def test_hundreds_elide_before_ottanta(self):
        for number, expected in [
                (180, "centottanta"), (188, "centottantotto"),
                (880, "ottocentottanta"), (788, "settecentottantotto")]:
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, "it"), expected)

    def test_no_elision_before_uno_or_undici(self):
        self.assertEqual(pronounce_number(101, "it"), "centouno")
        self.assertEqual(pronounce_number(111, "it"), "centoundici")

    def test_sentence(self):
        self.assertEqual(
            f"Il numero {pronounce_number(108, 'it')} è pari.",
            "Il numero centootto è pari.")

    def test_ordinal_follows_the_cardinal(self):
        self.assertEqual(pronounce_ordinal(108, "it"), "centoottesimo")
        self.assertEqual(pronounce_ordinal(108, "it", gender=FEMININE),
                         "centoottesima")


class TestOrdinalsAfterMillesimo(unittest.TestCase):
    def assertOrdinals(self, cases, gender=GrammaticalGender.MASCULINE):
        for number, expected in cases:
            with self.subTest(number=number, gender=gender.name):
                self.assertEqual(pronounce_ordinal(number, "it",
                                                   gender=gender), expected)
                self.assertEqual(pronounce_number(number, "it", ordinals=True,
                                                  gender=gender), expected)

    def test_two_words(self):
        self.assertOrdinals([
            (1001, "millesimo primo"), (1002, "millesimo secondo"),
            (1010, "millesimo decimo"), (1011, "millesimo undicesimo")])

    def test_two_words_feminine(self):
        self.assertOrdinals([
            (1001, "millesima prima"), (1002, "millesima seconda"),
            (1010, "millesima decima"), (1011, "millesima undicesima")],
            gender=FEMININE)

    def test_sentence(self):
        self.assertEqual(
            f"Il {pronounce_ordinal(1001, 'it')} cliente riceve un premio.",
            "Il millesimo primo cliente riceve un premio.")

    def test_neighbours_keep_one_word(self):
        self.assertOrdinals([
            (1000, "millesimo"), (1003, "milletreesimo"),
            (1012, "milledodicesimo"), (1100, "millecentesimo"),
            (2001, "duemilaunesimo")])

    def test_ventunomila_is_kept(self):
        # Crusca: "ventunomila o ventunmila: entrambe le forme vanno bene"
        self.assertOrdinals([(21000, "ventunomillesimo"),
                             (31000, "trentunomillesimo")])


if __name__ == "__main__":
    unittest.main()
