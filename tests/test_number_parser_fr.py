import unittest

from ovos_number_parser import extract_number

from ovos_number_parser.numbers_fr import (_get_ordinal_fr, pronounce_number_fr, nice_number_fr, is_fractional_fr, normalize_fr)


class TestNumberParserFr(unittest.TestCase):
    def test_extract_numeric_ordinals(self):
        self.assertEqual(_get_ordinal_fr("2nde"), 2)
        self.assertEqual(_get_ordinal_fr("5ième"), 5)
        self.assertEqual(_get_ordinal_fr("21ème"), 21)

    def test_extract_number_from_ordinal_phrase(self):
        self.assertEqual(extract_number("la 2nde place", ordinals=True, lang="fr"), 2)

    def test_units_and_teens(self):
        for word, val in [("zéro", 0), ("un", 1), ("une", 1), ("sept", 7),
                          ("dix", 10), ("onze", 11), ("seize", 16)]:
            self.assertEqual(extract_number(word, lang="fr"), val, word)

    def test_tens(self):
        for word, val in [("vingt", 20), ("trente", 30), ("cinquante", 50),
                          ("soixante", 60)]:
            self.assertEqual(extract_number(word, lang="fr"), val, word)

    def test_et_un_joiners(self):
        self.assertEqual(extract_number("vingt et un", lang="fr"), 21)
        self.assertEqual(extract_number("trente et un", lang="fr"), 31)
        self.assertEqual(extract_number("quarante et un", lang="fr"), 41)
        self.assertEqual(extract_number("cinquante et un", lang="fr"), 51)
        self.assertEqual(extract_number("soixante et un", lang="fr"), 61)

    def test_vigesimal_seventies(self):
        self.assertEqual(extract_number("soixante-dix", lang="fr"), 70)
        self.assertEqual(extract_number("soixante et onze", lang="fr"), 71)
        self.assertEqual(extract_number("soixante-douze", lang="fr"), 72)
        self.assertEqual(extract_number("soixante-quinze", lang="fr"), 75)
        self.assertEqual(extract_number("soixante-dix-sept", lang="fr"), 77)
        self.assertEqual(extract_number("soixante-dix-neuf", lang="fr"), 79)

    def test_vigesimal_eighties(self):
        self.assertEqual(extract_number("quatre-vingts", lang="fr"), 80)
        self.assertEqual(extract_number("quatre-vingt-un", lang="fr"), 81)
        self.assertEqual(extract_number("quatre-vingt-cinq", lang="fr"), 85)

    def test_vigesimal_nineties(self):
        self.assertEqual(extract_number("quatre-vingt-dix", lang="fr"), 90)
        self.assertEqual(extract_number("quatre-vingt-onze", lang="fr"), 91)
        self.assertEqual(extract_number("quatre-vingt-dix-neuf", lang="fr"), 99)


    def test_hundreds(self):
        self.assertEqual(extract_number("cent", lang="fr"), 100)
        self.assertEqual(extract_number("cent un", lang="fr"), 101)
        self.assertEqual(extract_number("deux cents", lang="fr"), 200)
        self.assertEqual(extract_number("deux cent un", lang="fr"), 201)
        self.assertEqual(extract_number("trois cents", lang="fr"), 300)
        self.assertEqual(
            extract_number("neuf cent quatre-vingt-dix-neuf", lang="fr"), 999)

    def test_thousands_and_scales(self):
        self.assertEqual(extract_number("mille", lang="fr"), 1000)
        self.assertEqual(extract_number("deux mille", lang="fr"), 2000)
        self.assertEqual(
            extract_number("mille neuf cent quatre-vingt-dix-neuf", lang="fr"), 1999)
        self.assertEqual(extract_number("un million", lang="fr"), 1000000)
        self.assertEqual(extract_number("deux millions", lang="fr"), 2000000)
        self.assertEqual(extract_number("un milliard", lang="fr"), 1000000000)

    def test_decimals(self):
        self.assertEqual(extract_number("trois virgule quatorze", lang="fr"), 3.14)
        self.assertEqual(extract_number("zéro virgule cinq", lang="fr"), 0.5)
        self.assertEqual(extract_number("3.5", lang="fr"), 3.5)

    def test_negatives(self):
        self.assertEqual(extract_number("moins cinq", lang="fr"), -5)
        self.assertEqual(extract_number("moins quatre-vingts", lang="fr"), -80)

    def test_fractions(self):
        self.assertEqual(extract_number("un demi", lang="fr"), 0.5)
        self.assertEqual(extract_number("trois quarts", lang="fr"), 0.75)
        self.assertAlmostEqual(extract_number("deux tiers", lang="fr"), 2 / 3)

    def test_numeric_fraction_slash(self):
        self.assertAlmostEqual(extract_number("2/3", lang="fr"), 2 / 3)

    def test_embedded_in_sentence(self):
        self.assertEqual(extract_number("j'ai vingt ans", lang="fr"), 20)
        self.assertEqual(extract_number("il y a cent euros", lang="fr"), 100)
        self.assertEqual(extract_number("un chat noir", lang="fr"), 1)

    def test_case_insensitive(self):
        self.assertEqual(extract_number("VINGT", lang="fr"), 20)
        self.assertEqual(extract_number("Quatre-Vingts", lang="fr"), 80)

    def test_no_number(self):
        self.assertFalse(extract_number("", lang="fr"))
        self.assertFalse(extract_number("   ", lang="fr"))
        self.assertFalse(extract_number("bonjour", lang="fr"))
        self.assertFalse(extract_number("et", lang="fr"))
        self.assertFalse(extract_number("plus", lang="fr"))

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
            self.assertEqual(extract_number(pronounce_number_fr(n), lang="fr"), n, n)

    def test_round_trip_large_sample(self):
        for n in [1234, 2001, 10000, 80080, 999999, 1000000, 1234567,
                  1000000000, 2000000001]:
            self.assertEqual(extract_number(pronounce_number_fr(n), lang="fr"), n, n)

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

    def test_long_scale_billion_words(self):
        # French is long scale: milliard = 10^9, billion = 10^12.
        self.assertEqual(pronounce_number_fr(10 ** 6), "un million")
        self.assertEqual(pronounce_number_fr(10 ** 9), "un milliard")
        self.assertEqual(pronounce_number_fr(10 ** 12), "un billion")
        self.assertEqual(pronounce_number_fr(2 * 10 ** 12), "deux billions")
        self.assertEqual(extract_number("un billion", lang="fr"), 10 ** 12)
        self.assertEqual(extract_number("deux billions", lang="fr"), 2 * 10 ** 12)

    def test_long_scale_round_trip_both_directions(self):
        # word -> number and number -> word must agree at each magnitude.
        for n in [10 ** 6, 10 ** 9, 10 ** 12]:
            word = pronounce_number_fr(n)
            self.assertEqual(extract_number(word, lang="fr"), n, n)
        for word, n in [("un million", 10 ** 6),
                        ("un milliard", 10 ** 9),
                        ("un billion", 10 ** 12)]:
            self.assertEqual(extract_number(word, lang="fr"), n, word)
            self.assertEqual(extract_number(pronounce_number_fr(n), lang="fr"), n, n)

    def test_long_scale_mixed_magnitudes(self):
        # Adversarial nesting: billions must combine with lower scales.
        self.assertEqual(
            extract_number(pronounce_number_fr(10 ** 12 + 3 * 10 ** 9), lang="fr"),
            10 ** 12 + 3 * 10 ** 9)
        self.assertEqual(
            pronounce_number_fr(10 ** 12 + 3 * 10 ** 9),
            "un billion trois milliards")


    def test_round_trip_sweep_to_ten_million(self):
        # Strided sweep across 0..10,000,000 both signs.
        for n in range(0, 10 ** 7 + 1, 4999):
            self.assertEqual(extract_number(pronounce_number_fr(n), lang="fr"), n, n)
            self.assertEqual(extract_number(pronounce_number_fr(-n), lang="fr"), -n, -n)

    def test_scientific_notation_does_not_crash(self):
        # Very small / very large / scientific floats must not raise.
        for value in [1e-9, 1e-5, 6.022e23, 1e15, -1e-9]:
            try:
                pronounce_number_fr(value)
            except Exception as error:  # noqa: BLE001
                self.fail(f"pronounce_number_fr({value!r}) raised {error!r}")

    def test_non_decimal_unicode_ordinal_does_not_crash(self):
        # Superscripts (¹) and vulgar fractions (½) are digit-like
        # (str.isdigit()/isnumeric() is True) but int() rejects them; a
        # pseudo-ordinal built from them must not raise ValueError.
        for text in ("¹er", "²e", "½e"):
            with self.subTest(text=text):
                self.assertIsNone(_get_ordinal_fr(text))
                self.assertFalse(extract_number(text, lang="fr"))

    def test_arabic_indic_digit_ordinal_still_works(self):
        self.assertEqual(_get_ordinal_fr("١er"), 1)


if __name__ == "__main__":
    unittest.main()
