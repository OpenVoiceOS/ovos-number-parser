"""Occitan number parser tests.

Anchor forms use the classical orthography (norma classica), Lengadocian
referential variety, verified against Lo Congrès resources, Wiktionary
Occitan numeral/ordinal entries and languagesandnumbers.com.
"""
import unittest

from ovos_number_parser.numbers_oc import OC
from ovos_number_parser.util import GrammaticalGender, Scale


# hand-verified pronounce anchors (Lengadocian, classical norm)
PRONOUNCE_ANCHORS = {
    0: "zèro",
    1: "un",
    2: "dos",
    3: "tres",
    4: "quatre",
    5: "cinc",
    6: "sièis",
    7: "sèt",
    8: "uèch",
    9: "nòu",
    10: "dètz",
    11: "onze",
    12: "dotze",
    13: "tretze",
    14: "catòrze",
    15: "quinze",
    16: "setze",
    17: "dètz-e-sèt",
    18: "dètz-e-uèch",
    19: "dètz-e-nòu",
    20: "vint",
    21: "vint e un",
    22: "vint e dos",
    29: "vint e nòu",
    30: "trenta",
    32: "trenta dos",
    40: "quaranta",
    50: "cinquanta",
    57: "cinquanta sèt",
    60: "seissanta",
    70: "setanta",
    80: "ochanta",
    90: "nonanta",
    99: "nonanta nòu",
    100: "cent",
    101: "cent un",
    120: "cent vint",
    200: "dos cents",
    234: "dos cents trenta quatre",
    300: "tres cents",
    900: "nòu cents",
    999: "nòu cents nonanta nòu",
    1000: "mila",
    2000: "dos mila",
    2300: "dos mila tres cents",
    1000000: "un milion",
    2000000: "dos milions",
    1000000000: "un miliard",
}


class TestPronounceOC(unittest.TestCase):
    def test_anchors(self):
        for n, spoken in PRONOUNCE_ANCHORS.items():
            self.assertEqual(OC.pronounce_number(n), spoken, n)

    def test_feminine(self):
        self.assertEqual(OC.pronounce_number(1, gender=GrammaticalGender.FEMININE), "una")
        self.assertEqual(OC.pronounce_number(2, gender=GrammaticalGender.FEMININE), "doas")
        self.assertEqual(OC.pronounce_number(21, gender=GrammaticalGender.FEMININE), "vint e una")

    def test_negative(self):
        self.assertEqual(OC.pronounce_number(-7), "mens sèt")

    def test_decimal(self):
        self.assertEqual(OC.pronounce_number(3.14, places=2), "tres virgula catòrze")
        self.assertEqual(OC.pronounce_number(0.5), "zèro virgula cinc")


class TestOrdinalsOC(unittest.TestCase):
    def test_units(self):
        self.assertEqual(OC.pronounce_ordinal(1), "primièr")
        self.assertEqual(OC.pronounce_ordinal(1, gender=GrammaticalGender.FEMININE), "primièra")
        self.assertEqual(OC.pronounce_ordinal(2), "segond")
        self.assertEqual(OC.pronounce_ordinal(2, gender=GrammaticalGender.FEMININE), "segonda")
        self.assertEqual(OC.pronounce_ordinal(3), "tresen")
        self.assertEqual(OC.pronounce_ordinal(3, gender=GrammaticalGender.FEMININE), "tresena")
        self.assertEqual(OC.pronounce_ordinal(4), "quatren")
        self.assertEqual(OC.pronounce_ordinal(5), "cinquen")
        self.assertEqual(OC.pronounce_ordinal(9), "noven")

    def test_teens(self):
        self.assertEqual(OC.pronounce_ordinal(10), "desen")
        self.assertEqual(OC.pronounce_ordinal(11), "onzen")
        self.assertEqual(OC.pronounce_ordinal(16), "setzen")
        self.assertEqual(OC.pronounce_ordinal(17), "dètz-e-seten")

    def test_tens_and_compounds(self):
        self.assertEqual(OC.pronounce_ordinal(20), "vinten")
        self.assertEqual(OC.pronounce_ordinal(21), "vint-e-unen")
        self.assertEqual(OC.pronounce_ordinal(30), "trenten")
        self.assertEqual(OC.pronounce_ordinal(90), "nonanten")

    def test_large(self):
        self.assertEqual(OC.pronounce_ordinal(100), "centen")
        self.assertEqual(OC.pronounce_ordinal(1000), "milen")
        self.assertEqual(OC.pronounce_ordinal(1000000), "milionen")

    def test_is_ordinal(self):
        self.assertEqual(OC.is_ordinal("primièr"), 1)
        self.assertEqual(OC.is_ordinal("tresen"), 3)
        self.assertEqual(OC.is_ordinal("vinten"), 20)
        self.assertFalse(OC.is_ordinal("ostal"))


class TestFractionsOC(unittest.TestCase):
    def test_pronounce_fraction(self):
        self.assertEqual(OC.pronounce_fraction("1/2"), "un mièg")
        self.assertEqual(OC.pronounce_fraction("2/3"), "dos tèrces")
        self.assertEqual(OC.pronounce_fraction("3/4"), "tres quarts")
        self.assertEqual(OC.pronounce_fraction("1/4"), "un quart")
        self.assertEqual(OC.pronounce_fraction("1/5"), "un cinquen")

    def test_is_fractional(self):
        self.assertEqual(OC.is_fractional("mièg"), 0.5)
        self.assertEqual(OC.is_fractional("mièja"), 0.5)
        self.assertEqual(OC.is_fractional("tèrç"), 1 / 3)
        self.assertEqual(OC.is_fractional("quart"), 0.25)
        self.assertFalse(OC.is_fractional("ostal"))


class TestExtractOC(unittest.TestCase):
    def test_units_and_teens(self):
        self.assertEqual(OC.extract_number("un"), 1)
        self.assertEqual(OC.extract_number("una"), 1)
        self.assertEqual(OC.extract_number("doas"), 2)
        self.assertEqual(OC.extract_number("setze"), 16)
        self.assertEqual(OC.extract_number("dètz-e-sèt"), 17)

    def test_hyphenated_compounds(self):
        self.assertEqual(OC.extract_number("vint-e-un"), 21)
        self.assertEqual(OC.extract_number("vint-e-una"), 21)
        self.assertEqual(OC.extract_number("vint-e-nòu"), 29)
        self.assertEqual(OC.extract_number("dètz-e-uèch"), 18)

    def test_juxtaposed_tens(self):
        self.assertEqual(OC.extract_number("trenta dos"), 32)
        self.assertEqual(OC.extract_number("cinquanta sèt"), 57)
        self.assertEqual(OC.extract_number("nonanta nòu"), 99)

    def test_alt_spellings(self):
        self.assertEqual(OC.extract_number("ueitanta"), 80)

    def test_analytic_hundreds(self):
        self.assertEqual(OC.extract_number("cent"), 100)
        self.assertEqual(OC.extract_number("cent vint"), 120)
        self.assertEqual(OC.extract_number("dos cents"), 200)
        self.assertEqual(OC.extract_number("dos cents trenta quatre"), 234)
        self.assertEqual(OC.extract_number("nòu cents nonanta nòu"), 999)

    def test_thousands(self):
        self.assertEqual(OC.extract_number("mila"), 1000)
        self.assertEqual(OC.extract_number("dos mila"), 2000)
        self.assertEqual(OC.extract_number("dos mila tres cents"), 2300)
        self.assertEqual(OC.extract_number("un milion"), 1000000)
        self.assertEqual(OC.extract_number("dos milions"), 2000000)
        self.assertEqual(OC.extract_number("un miliard"), 1000000000)

    def test_decimals(self):
        self.assertEqual(OC.extract_number("tres virgula catòrze"), 3.14)
        self.assertEqual(OC.extract_number("trenta cinc virgula quatre"), 35.4)

    def test_negative(self):
        self.assertEqual(OC.extract_number("mens sèt"), -7)
        self.assertEqual(OC.extract_number("mens vint e un"), -21)

    def test_fraction_words(self):
        self.assertEqual(OC.extract_number("un e mièg"), 1.5)
        self.assertEqual(OC.extract_number("tres quarts"), 0.75)

    def test_ordinal_extraction(self):
        self.assertEqual(OC.extract_number("lo tresen còp", ordinals=True), 3)
        self.assertEqual(OC.extract_number("la primièra vegada", ordinals=True), 1)
        self.assertEqual(OC.extract_number("vint-e-unen", ordinals=True), 21)

    def test_in_sentence(self):
        self.assertEqual(OC.extract_number("i a vint e un gats"), 21)
        self.assertEqual(OC.extract_number("son dos cents trenta quilòmetres"), 230)

    def test_no_number(self):
        self.assertFalse(OC.extract_number("bon jorn"))


class TestNumbersToDigitsOC(unittest.TestCase):
    def test_replace(self):
        self.assertEqual(OC.numbers_to_digits("i a vint e un gats"), "i a 21 gats")
        self.assertEqual(OC.numbers_to_digits("dos cents trenta quatre ostals"),
                         "234 ostals")

    def test_passthrough(self):
        self.assertEqual(OC.numbers_to_digits("bon jorn amics"), "bon jorn amics")


class TestRoundTripOC(unittest.TestCase):
    def test_sweep(self):
        for n in range(0, 1101):
            spoken = OC.pronounce_number(n)
            self.assertEqual(OC.extract_number(spoken), n, f"{n}: {spoken!r}")

    def test_sweep_large(self):
        for n in (2023, 9999, 12345, 100000, 654321, 1000000, 2500000,
                  1000000000, 2000000001):
            spoken = OC.pronounce_number(n)
            self.assertEqual(OC.extract_number(spoken), n, f"{n}: {spoken!r}")

    def test_sweep_feminine(self):
        for n in (1, 2, 21, 22, 31, 42, 101, 202):
            spoken = OC.pronounce_number(n, gender=GrammaticalGender.FEMININE)
            self.assertEqual(OC.extract_number(spoken), n, f"{n}: {spoken!r}")

    def test_sweep_ordinals(self):
        for n in (1, 2, 3, 9, 10, 11, 16, 20, 30, 90, 100, 1000):
            spoken = OC.pronounce_ordinal(n)
            self.assertEqual(OC.extract_number(spoken, ordinals=True), n,
                             f"{n}: {spoken!r}")


if __name__ == "__main__":
    unittest.main()
