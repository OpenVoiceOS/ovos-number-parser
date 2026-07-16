"""Romanian number parsing and pronunciation.

Anchor expectations follow the Romanian Academy orthography (DOOM,
ă/â/î/ș/ț with comma diacritics): compound tens join units with "și"
("douăzeci și unu"), counts of twenty and above link to their scale word
with "de" ("douăzeci de mii"), "mie" takes feminine agreement
("două mii", "douăzeci și una de mii") while "milion"/"miliard" are
neuter ("un milion", "două milioane", "douăzeci și unu de milioane"),
and ordinals take the particles "al"/"a" ("al doilea"/"a doua").
"""
import unittest

from ovos_number_parser.numbers_ro import RO
from ovos_number_parser.util import GrammaticalGender


class TestPronunciationRO(unittest.TestCase):

    def test_units(self):
        anchors = {0: "zero", 1: "unu", 2: "doi", 3: "trei", 4: "patru",
                   5: "cinci", 6: "șase", 7: "șapte", 8: "opt", 9: "nouă",
                   10: "zece"}
        for n, expected in anchors.items():
            self.assertEqual(RO.pronounce_number(n), expected)

    def test_gendered_units(self):
        self.assertEqual(RO.pronounce_number(1, gender=GrammaticalGender.FEMININE), "una")
        self.assertEqual(RO.pronounce_number(2, gender=GrammaticalGender.FEMININE), "două")
        self.assertEqual(RO.pronounce_number(12, gender=GrammaticalGender.FEMININE),
                         "douăsprezece")

    def test_teens(self):
        anchors = {11: "unsprezece", 12: "doisprezece", 13: "treisprezece",
                   14: "paisprezece", 15: "cincisprezece", 16: "șaisprezece",
                   17: "șaptesprezece", 18: "optsprezece", 19: "nouăsprezece"}
        for n, expected in anchors.items():
            self.assertEqual(RO.pronounce_number(n), expected)

    def test_tens(self):
        anchors = {20: "douăzeci", 30: "treizeci", 40: "patruzeci",
                   50: "cincizeci", 60: "șaizeci", 70: "șaptezeci",
                   80: "optzeci", 90: "nouăzeci"}
        for n, expected in anchors.items():
            self.assertEqual(RO.pronounce_number(n), expected)

    def test_si_joins(self):
        self.assertEqual(RO.pronounce_number(21), "douăzeci și unu")
        self.assertEqual(RO.pronounce_number(22), "douăzeci și doi")
        self.assertEqual(RO.pronounce_number(22, gender=GrammaticalGender.FEMININE),
                         "douăzeci și două")
        self.assertEqual(RO.pronounce_number(35), "treizeci și cinci")
        self.assertEqual(RO.pronounce_number(68), "șaizeci și opt")
        self.assertEqual(RO.pronounce_number(99), "nouăzeci și nouă")

    def test_hundreds(self):
        self.assertEqual(RO.pronounce_number(100), "o sută")
        self.assertEqual(RO.pronounce_number(101), "o sută unu")
        self.assertEqual(RO.pronounce_number(120), "o sută douăzeci")
        self.assertEqual(RO.pronounce_number(123), "o sută douăzeci și trei")
        self.assertEqual(RO.pronounce_number(200), "două sute")
        self.assertEqual(RO.pronounce_number(245), "două sute patruzeci și cinci")
        self.assertEqual(RO.pronounce_number(999), "nouă sute nouăzeci și nouă")

    def test_thousands(self):
        self.assertEqual(RO.pronounce_number(1000), "o mie")
        self.assertEqual(RO.pronounce_number(1001), "o mie unu")
        self.assertEqual(RO.pronounce_number(2000), "două mii")
        self.assertEqual(RO.pronounce_number(2001), "două mii unu")
        self.assertEqual(RO.pronounce_number(1234),
                         "o mie două sute treizeci și patru")
        self.assertEqual(RO.pronounce_number(2023), "două mii douăzeci și trei")

    def test_de_insertion(self):
        # counts of twenty and above link to the scale word with "de"
        self.assertEqual(RO.pronounce_number(20_000), "douăzeci de mii")
        self.assertEqual(RO.pronounce_number(21_000), "douăzeci și una de mii")
        self.assertEqual(RO.pronounce_number(100_000), "o sută de mii")
        self.assertEqual(RO.pronounce_number(100_000_000), "o sută de milioane")
        self.assertEqual(RO.pronounce_number(45_000),
                         "patruzeci și cinci de mii")
        # counts below twenty take no "de"
        self.assertEqual(RO.pronounce_number(15_000), "cincisprezece mii")

    def test_millions(self):
        self.assertEqual(RO.pronounce_number(1_000_000), "un milion")
        self.assertEqual(RO.pronounce_number(2_000_000), "două milioane")
        self.assertEqual(RO.pronounce_number(21_000_000),
                         "douăzeci și unu de milioane")
        self.assertEqual(RO.pronounce_number(22_000_000),
                         "douăzeci și două de milioane")
        self.assertEqual(RO.pronounce_number(1_000_000_000), "un miliard")
        self.assertEqual(RO.pronounce_number(2_000_000_000), "două miliarde")
        self.assertEqual(
            RO.pronounce_number(1_234_567),
            "un milion două sute treizeci și patru de mii cinci sute șaizeci și șapte")

    def test_decimals(self):
        self.assertEqual(RO.pronounce_number(5.2), "cinci virgulă doi")
        self.assertEqual(RO.pronounce_number(3.14), "trei virgulă paisprezece")
        self.assertEqual(RO.pronounce_number(10.05), "zece virgulă zero cinci")

    def test_negative(self):
        self.assertEqual(RO.pronounce_number(-3), "minus trei")
        self.assertEqual(RO.pronounce_number(-5.2), "minus cinci virgulă doi")

    def test_ordinals_masculine(self):
        anchors = {1: "primul", 2: "al doilea", 3: "al treilea",
                   4: "al patrulea", 5: "al cincilea", 6: "al șaselea",
                   7: "al șaptelea", 8: "al optulea", 9: "al nouălea",
                   10: "al zecelea", 12: "al doisprezecelea",
                   20: "al douăzecilea", 21: "al douăzeci și unulea",
                   45: "al patruzeci și cincilea", 100: "al sutălea",
                   1000: "al miilea"}
        for n, expected in anchors.items():
            self.assertEqual(RO.pronounce_ordinal(n), expected)
            self.assertEqual(RO.pronounce_number(n, ordinals=True), expected)

    def test_ordinals_feminine(self):
        anchors = {1: "prima", 2: "a doua", 3: "a treia", 4: "a patra",
                   5: "a cincea", 6: "a șasea", 7: "a șaptea", 8: "a opta",
                   9: "a noua", 10: "a zecea", 20: "a douăzecea",
                   1000: "a mia"}
        for n, expected in anchors.items():
            self.assertEqual(
                RO.pronounce_ordinal(n, gender=GrammaticalGender.FEMININE),
                expected)

    def test_fractions(self):
        self.assertEqual(RO.pronounce_fraction("1/2"), "o jumătate")
        self.assertEqual(RO.pronounce_fraction("1/3"), "o treime")
        self.assertEqual(RO.pronounce_fraction("1/4"), "un sfert")
        self.assertEqual(RO.pronounce_fraction("1/5"), "o cincime")
        self.assertEqual(RO.pronounce_fraction("2/3"), "două treimi")
        self.assertEqual(RO.pronounce_fraction("3/4"), "trei sferturi")
        self.assertEqual(RO.pronounce_fraction("3/2"), "trei jumătăți")
        self.assertEqual(RO.pronounce_fraction("5/8"), "cinci optimi")
        self.assertEqual(RO.pronounce_fraction("7/10"), "șapte zecimi")


class TestExtractionRO(unittest.TestCase):

    def test_units_and_gender_variants(self):
        self.assertEqual(RO.extract_number("unu"), 1)
        self.assertEqual(RO.extract_number("una"), 1)
        self.assertEqual(RO.extract_number("un milion"), 1_000_000)
        self.assertEqual(RO.extract_number("doi"), 2)
        self.assertEqual(RO.extract_number("două"), 2)
        self.assertEqual(RO.extract_number("doisprezece"), 12)
        self.assertEqual(RO.extract_number("douăsprezece"), 12)

    def test_si_joins(self):
        self.assertEqual(RO.extract_number("douăzeci și unu"), 21)
        self.assertEqual(RO.extract_number("douăzeci și una"), 21)
        self.assertEqual(RO.extract_number("treizeci și cinci"), 35)
        self.assertEqual(RO.extract_number("nouăzeci și nouă"), 99)

    def test_hundreds_multiply(self):
        self.assertEqual(RO.extract_number("o sută"), 100)
        self.assertEqual(RO.extract_number("două sute"), 200)
        self.assertEqual(RO.extract_number("două sute treizeci și cinci"), 235)
        self.assertEqual(RO.extract_number("nouă sute nouăzeci și nouă"), 999)

    def test_de_insertion(self):
        # "de" is number-internal when it links a count to a scale word
        self.assertEqual(RO.extract_number("douăzeci de mii"), 20_000)
        self.assertEqual(RO.extract_number("douăzeci și una de mii"), 21_000)
        self.assertEqual(RO.extract_number("o sută de milioane"), 100_000_000)
        self.assertEqual(RO.extract_number("patruzeci și cinci de mii"), 45_000)

    def test_thousands(self):
        self.assertEqual(RO.extract_number("o mie"), 1000)
        self.assertEqual(RO.extract_number("două mii"), 2000)
        self.assertEqual(RO.extract_number("două mii unu"), 2001)
        self.assertEqual(RO.extract_number("o mie două sute"), 1200)
        self.assertEqual(
            RO.extract_number("un milion două sute treizeci și patru de mii "
                              "cinci sute șaizeci și șapte"),
            1_234_567)

    def test_colloquial_teens(self):
        # short spoken forms are accepted for extraction only
        self.assertEqual(RO.extract_number("unșpe"), 11)
        self.assertEqual(RO.extract_number("doișpe"), 12)
        self.assertEqual(RO.extract_number("paișpe"), 14)
        self.assertEqual(RO.extract_number("șaișpe"), 16)
        self.assertEqual(RO.extract_number("nouășpe"), 19)

    def test_decimals(self):
        self.assertEqual(RO.extract_number("cinci virgulă doi"), 5.2)
        self.assertEqual(RO.extract_number("trei virgulă paisprezece"), 3.14)
        self.assertEqual(RO.extract_number("zece virgulă zero cinci"), 10.05)

    def test_negative(self):
        self.assertEqual(RO.extract_number("minus zece"), -10)
        self.assertEqual(RO.extract_number("minus cinci virgulă doi"), -5.2)

    def test_fractions(self):
        self.assertEqual(RO.extract_number("doi și jumătate"), 2.5)
        self.assertEqual(RO.extract_number("două treimi"), 2 / 3)
        self.assertEqual(RO.extract_number("trei sferturi"), 3 / 4)
        self.assertEqual(RO.is_fractional("jumătate"), 1 / 2)
        self.assertEqual(RO.is_fractional("treime"), 1 / 3)
        self.assertEqual(RO.is_fractional("sfert"), 1 / 4)
        self.assertEqual(RO.is_fractional("pătrime"), 1 / 4)
        self.assertEqual(RO.is_fractional("cincime"), 1 / 5)
        self.assertFalse(RO.is_fractional("pisică"))

    def test_ordinals(self):
        self.assertEqual(RO.extract_number("al doilea om", ordinals=True), 2)
        self.assertEqual(RO.extract_number("a treia oară", ordinals=True), 3)
        self.assertEqual(RO.extract_number("primul loc", ordinals=True), 1)
        self.assertEqual(RO.extract_number("prima oară", ordinals=True), 1)
        self.assertEqual(
            RO.extract_number("al douăzeci și unulea etaj", ordinals=True), 21)
        self.assertEqual(RO.is_ordinal("al doilea"), 2)
        self.assertEqual(RO.is_ordinal("doua"), 2)
        self.assertEqual(RO.is_ordinal("primul"), 1)
        self.assertEqual(RO.is_ordinal("prima"), 1)
        self.assertEqual(RO.is_ordinal("miilea"), 1000)
        self.assertFalse(RO.is_ordinal("pisică"))

    def test_digits_win(self):
        self.assertEqual(RO.extract_number("7"), 7)
        self.assertEqual(RO.extract_number("am 7 mere"), 7)
        self.assertEqual(RO.extract_number("3,5"), 3.5)

    def test_no_number(self):
        self.assertFalse(RO.extract_number("nicio cifră aici"))

    def test_in_sentence(self):
        self.assertEqual(RO.extract_number("am douăzeci și cinci de mere"), 25)
        self.assertEqual(RO.extract_number("peste trei zile"), 3)


class TestNumbersToDigitsRO(unittest.TestCase):

    def test_plain(self):
        self.assertEqual(RO.numbers_to_digits("douăzeci și cinci"), "25")
        self.assertEqual(RO.numbers_to_digits("două sute cincizeci"), "250")
        self.assertEqual(RO.numbers_to_digits("un milion"), "1000000")

    def test_in_sentence(self):
        self.assertEqual(
            RO.numbers_to_digits("am douăzeci și cinci de mere și trei pere"),
            "am 25 de mere și 3 pere")


class TestRoundTripRO(unittest.TestCase):
    def test_round_trip_sweep(self):
        values = list(range(0, 1000)) + [
            1000, 1001, 1015, 1200, 2000, 2001, 9999, 10_000, 20_000, 21_000,
            45_678, 100_000, 123_456, 999_999, 1_000_000, 2_000_000,
            2_500_123, 21_000_000, 100_000_000, 123_456_789, 1_000_000_000,
            2_000_000_001]
        for n in values:
            spoken = RO.pronounce_number(n)
            self.assertEqual(RO.extract_number(spoken), n, spoken)

    def test_round_trip_feminine(self):
        for n in (1, 2, 12, 22, 42, 101):
            spoken = RO.pronounce_number(n, gender=GrammaticalGender.FEMININE)
            self.assertEqual(RO.extract_number(spoken), n, spoken)

    def test_round_trip_ordinals(self):
        for n in (1, 2, 3, 7, 10, 13, 20, 21, 45, 100, 1000):
            spoken = RO.pronounce_ordinal(n)
            self.assertEqual(RO.extract_number(spoken, ordinals=True), n, spoken)
            # is_ordinal only matches single ordinal words (plus particle)
            if len(spoken.split()) <= 2:
                self.assertEqual(RO.is_ordinal(spoken), n, spoken)

    def test_round_trip_decimals(self):
        for n in (0.5, 5.2, 3.14, 12.34, 100.01):
            spoken = RO.pronounce_number(n)
            self.assertAlmostEqual(RO.extract_number(spoken), n, places=2,
                                   msg=spoken)


if __name__ == "__main__":
    unittest.main()
