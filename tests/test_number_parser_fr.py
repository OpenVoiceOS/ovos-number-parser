import unittest

from ovos_number_parser.numbers_fr import (
    _get_ordinal_fr,
    extract_number_fr,
    pronounce_number_fr,
    nice_number_fr,
    is_fractional_fr,
    normalize_fr,
)


class TestNumberParserFr(unittest.TestCase):
    def test_extract_numeric_ordinals(self):
        self.assertEqual(_get_ordinal_fr("2nde"), 2)
        self.assertEqual(_get_ordinal_fr("5ième"), 5)
        self.assertEqual(_get_ordinal_fr("21ème"), 21)

    def test_extract_number_from_ordinal_phrase(self):
        self.assertEqual(extract_number_fr("la 2nde place", ordinals=True), 2)

    def test_units_and_teens(self):
        for word, val in [("zéro", 0), ("un", 1), ("une", 1), ("sept", 7),
                          ("dix", 10), ("onze", 11), ("seize", 16)]:
            self.assertEqual(extract_number_fr(word), val, word)

    def test_tens(self):
        for word, val in [("vingt", 20), ("trente", 30), ("cinquante", 50),
                          ("soixante", 60)]:
            self.assertEqual(extract_number_fr(word), val, word)

    def test_et_un_joiners(self):
        self.assertEqual(extract_number_fr("vingt et un"), 21)
        self.assertEqual(extract_number_fr("trente et un"), 31)
        self.assertEqual(extract_number_fr("quarante et un"), 41)
        self.assertEqual(extract_number_fr("cinquante et un"), 51)
        self.assertEqual(extract_number_fr("soixante et un"), 61)

    def test_vigesimal_seventies(self):
        self.assertEqual(extract_number_fr("soixante-dix"), 70)
        self.assertEqual(extract_number_fr("soixante et onze"), 71)
        self.assertEqual(extract_number_fr("soixante-douze"), 72)
        self.assertEqual(extract_number_fr("soixante-quinze"), 75)
        self.assertEqual(extract_number_fr("soixante-dix-sept"), 77)
        self.assertEqual(extract_number_fr("soixante-dix-neuf"), 79)

    def test_vigesimal_eighties(self):
        self.assertEqual(extract_number_fr("quatre-vingts"), 80)
        self.assertEqual(extract_number_fr("quatre-vingt-un"), 81)
        self.assertEqual(extract_number_fr("quatre-vingt-cinq"), 85)

    def test_vigesimal_nineties(self):
        self.assertEqual(extract_number_fr("quatre-vingt-dix"), 90)
        self.assertEqual(extract_number_fr("quatre-vingt-onze"), 91)
        self.assertEqual(extract_number_fr("quatre-vingt-dix-neuf"), 99)

    def test_belgian_swiss_variants(self):
        self.assertEqual(extract_number_fr("septante"), 70)
        self.assertEqual(extract_number_fr("huitante"), 80)
        self.assertEqual(extract_number_fr("octante"), 80)
        self.assertEqual(extract_number_fr("nonante"), 90)

    def test_hundreds(self):
        self.assertEqual(extract_number_fr("cent"), 100)
        self.assertEqual(extract_number_fr("cent un"), 101)
        self.assertEqual(extract_number_fr("deux cents"), 200)
        self.assertEqual(extract_number_fr("deux cent un"), 201)
        self.assertEqual(extract_number_fr("trois cents"), 300)
        self.assertEqual(
            extract_number_fr("neuf cent quatre-vingt-dix-neuf"), 999)

    def test_thousands_and_scales(self):
        self.assertEqual(extract_number_fr("mille"), 1000)
        self.assertEqual(extract_number_fr("deux mille"), 2000)
        self.assertEqual(
            extract_number_fr("mille neuf cent quatre-vingt-dix-neuf"), 1999)
        self.assertEqual(extract_number_fr("un million"), 1000000)
        self.assertEqual(extract_number_fr("deux millions"), 2000000)
        self.assertEqual(extract_number_fr("un milliard"), 1000000000)

    def test_decimals(self):
        self.assertEqual(extract_number_fr("trois virgule quatorze"), 3.14)
        self.assertEqual(extract_number_fr("zéro virgule cinq"), 0.5)
        self.assertEqual(extract_number_fr("3.5"), 3.5)

    def test_negatives(self):
        self.assertEqual(extract_number_fr("moins cinq"), -5)
        self.assertEqual(extract_number_fr("moins quatre-vingts"), -80)

    def test_fractions(self):
        self.assertEqual(extract_number_fr("un demi"), 0.5)
        self.assertEqual(extract_number_fr("trois quarts"), 0.75)
        self.assertAlmostEqual(extract_number_fr("deux tiers"), 2 / 3)

    def test_numeric_fraction_slash(self):
        self.assertAlmostEqual(extract_number_fr("2/3"), 2 / 3)

    def test_embedded_in_sentence(self):
        self.assertEqual(extract_number_fr("j'ai vingt ans"), 20)
        self.assertEqual(extract_number_fr("il y a cent euros"), 100)
        self.assertEqual(extract_number_fr("un chat noir"), 1)

    def test_case_insensitive(self):
        self.assertEqual(extract_number_fr("VINGT"), 20)
        self.assertEqual(extract_number_fr("Quatre-Vingts"), 80)

    def test_no_number(self):
        self.assertFalse(extract_number_fr(""))
        self.assertFalse(extract_number_fr("   "))
        self.assertFalse(extract_number_fr("bonjour"))
        self.assertFalse(extract_number_fr("et"))
        self.assertFalse(extract_number_fr("plus"))

    def test_pronounce_vigesimal(self):
        self.assertEqual(pronounce_number_fr(21), "vingt-et-un")
        self.assertEqual(pronounce_number_fr(71), "soixante-et-onze")
        self.assertEqual(pronounce_number_fr(80), "quatre-vingts")
        self.assertEqual(pronounce_number_fr(81), "quatre-vingt-un")
        self.assertEqual(pronounce_number_fr(91), "quatre-vingt-onze")
        self.assertEqual(pronounce_number_fr(99), "quatre-vingt-dix-neuf")
        self.assertEqual(pronounce_number_fr(100), "cent")
        self.assertEqual(pronounce_number_fr(200), "deux cents")
        self.assertEqual(pronounce_number_fr(-80), "moins quatre-vingts")

    def test_round_trip_small(self):
        for n in range(0, 1001):
            self.assertEqual(extract_number_fr(pronounce_number_fr(n)), n, n)

    def test_round_trip_large_sample(self):
        for n in [1234, 2001, 10000, 80080, 999999, 1000000, 1234567,
                  1000000000, 2000000001]:
            self.assertEqual(extract_number_fr(pronounce_number_fr(n)), n, n)

    def test_is_fractional(self):
        self.assertEqual(is_fractional_fr("demi"), 0.5)
        self.assertEqual(is_fractional_fr("quart"), 0.25)
        self.assertEqual(is_fractional_fr("quarts"), 0.25)
        self.assertEqual(is_fractional_fr("QUART"), 0.25)
        self.assertAlmostEqual(is_fractional_fr("tiers"), 1 / 3)
        self.assertEqual(is_fractional_fr("centième"), 0.01)
        self.assertEqual(is_fractional_fr("millième"), 0.001)
        self.assertFalse(is_fractional_fr("bonjour"))

    def test_nice_number_speech(self):
        self.assertEqual(nice_number_fr(4.5), "4 et demi")
        self.assertEqual(nice_number_fr(0.5), "un demi")
        self.assertEqual(nice_number_fr(6.75), "6 et 3 quarts")
        self.assertEqual(nice_number_fr(2.0), "2")

    def test_nice_number_text(self):
        self.assertEqual(nice_number_fr(4.5, speech=False), "4 1/2")
        self.assertEqual(nice_number_fr(6.75, speech=False), "6 3/4")

    def test_normalize_numbers_to_digits(self):
        self.assertEqual(normalize_fr("j'ai vingt et un ans"), "j'ai 21 ans")
        self.assertEqual(normalize_fr("quatre-vingt-dix euros"), "90 euros")
        self.assertEqual(normalize_fr("trois cents personnes"),
                         "300 personnes")

    def test_normalize_articles(self):
        self.assertEqual(normalize_fr("le chat"), "chat")
        self.assertEqual(normalize_fr("le chat", remove_articles=False),
                         "le chat")


if __name__ == "__main__":
    unittest.main()
