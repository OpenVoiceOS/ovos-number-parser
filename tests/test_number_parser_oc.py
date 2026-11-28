"""Occitan number parser tests.

Anchor forms use the classical orthography (norma classica), Lengadocian
referential variety, verified against Lo Congrès resources, Wiktionary
Occitan numeral/ordinal entries and languagesandnumbers.com.
"""
import unittest

from ovos_number_parser import extract_number, numbers_to_digits, is_fractional, is_ordinal

from ovos_number_parser.numbers_oc import OC, pluralize_oc
from ovos_number_parser.util import GrammaticalGender


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
        self.assertEqual(is_ordinal("primièr", "oc"), 1)
        self.assertEqual(is_ordinal("tresen", "oc"), 3)
        self.assertEqual(is_ordinal("vinten", "oc"), 20)
        self.assertFalse(is_ordinal("ostal", "oc"))


class TestFractionsOC(unittest.TestCase):
    def test_pronounce_fraction(self):
        self.assertEqual(OC.pronounce_fraction("1/2"), "un mièg")
        self.assertEqual(OC.pronounce_fraction("2/3"), "dos tèrces")
        self.assertEqual(OC.pronounce_fraction("3/4"), "tres quarts")
        self.assertEqual(OC.pronounce_fraction("1/4"), "un quart")
        self.assertEqual(OC.pronounce_fraction("1/5"), "un cinquen")

    def test_is_fractional(self):
        with self.subTest(case='is_fractional("mièg", "oc")'):
            self.assertEqual(is_fractional("mièg", "oc"), 0.5)
        with self.subTest(case='is_fractional("mièja", "oc")'):
            self.assertEqual(is_fractional("mièja", "oc"), 0.5)
        with self.subTest(case='is_fractional("tèrç", "oc")'):
            self.assertEqual(is_fractional("tèrç", "oc"), 1 / 3)
        with self.subTest(case='is_fractional("quart", "oc")'):
            self.assertEqual(is_fractional("quart", "oc"), 0.25)
        with self.subTest(case='is_fractional("ostal", "oc")'):
            self.assertFalse(is_fractional("ostal", "oc"))


class TestExtractOC(unittest.TestCase):
    def test_units_and_teens(self):
        self.assertEqual(extract_number("un", lang="oc"), 1)
        self.assertEqual(extract_number("una", lang="oc"), 1)
        self.assertEqual(extract_number("doas", lang="oc"), 2)
        self.assertEqual(extract_number("setze", lang="oc"), 16)
        self.assertEqual(extract_number("dètz-e-sèt", lang="oc"), 17)

    def test_hyphenated_compounds(self):
        self.assertEqual(extract_number("vint-e-un", lang="oc"), 21)
        self.assertEqual(extract_number("vint-e-una", lang="oc"), 21)
        self.assertEqual(extract_number("vint-e-nòu", lang="oc"), 29)
        self.assertEqual(extract_number("dètz-e-uèch", lang="oc"), 18)

    def test_juxtaposed_tens(self):
        self.assertEqual(extract_number("trenta dos", lang="oc"), 32)
        self.assertEqual(extract_number("cinquanta sèt", lang="oc"), 57)
        self.assertEqual(extract_number("nonanta nòu", lang="oc"), 99)

    def test_alt_spellings(self):
        # variant spellings of 8 and 80 from issue #302
        self.assertEqual(extract_number("ueit", lang="oc"), 8)
        self.assertEqual(extract_number("uòch", lang="oc"), 8)
        self.assertEqual(extract_number("ueitanta", lang="oc"), 80)
        self.assertEqual(extract_number("uechanta", lang="oc"), 80)
        self.assertEqual(extract_number("uòchanta", lang="oc"), 80)

    def test_alt_spellings_named_by_the_native_reporter(self):
        # issue #302: "8: uèch and uèit and locally uòch in Montpellier",
        # "8th: ochen, uechen, ueiten, oiten", Montpellier "8th: uòchen",
        # "80th: uòchanten"
        self.assertEqual(extract_number("uèit", lang="oc"), 8)
        self.assertEqual(extract_number("ai uèit cats", lang="oc"), 8)
        for word in ("ochen", "uechen", "ueiten", "oiten", "uòchen"):
            with self.subTest(word=word):
                self.assertEqual(is_ordinal(word, "oc"), 8)
                self.assertEqual(
                    extract_number(f"lo {word} jorn", ordinals=True, lang="oc"), 8)
        self.assertEqual(is_ordinal("uòchanten", "oc"), 80)
        self.assertEqual(extract_number("la uòchena", ordinals=True, lang="oc"), 8)

    def test_alt_ordinal_spellings_take_the_feminine_and_plural(self):
        # the variants inflect as the referential "ochen" does: "ochena",
        # "los ochens" and "las ochenas" read 8 on dev
        for text in ("los uechens", "las uechenas", "los ueitens",
                     "los uòchens", "las uòchantenas"):
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, ordinals=True, lang="oc"),
                                 80 if "uòchanten" in text else 8)

    def test_ueitena_and_oitena_read_as_the_feminine_8th(self):
        # issue #302 lists "ueitena, oitena" beside the forms for 80; whether
        # they are cardinals for 80 waits on the native speaker. Here they are
        # the regular feminine of "ueiten" and "oiten", like "ochena".
        for word in ("ueitena", "oitena"):
            with self.subTest(word=word):
                self.assertEqual(extract_number(word, ordinals=True, lang="oc"), 8)
                self.assertIs(extract_number(word, lang="oc"), False)

    def test_alt_ordinal_spellings_are_never_written(self):
        self.assertEqual(OC.pronounce_number(8, ordinals=True), "ochen")
        self.assertEqual(OC.pronounce_number(80, ordinals=True), "ochanten")

    def test_pluralize_classes(self):
        # noun classes per Ubaud (issue #302)
        self.assertEqual(pluralize_oc("peis"), "peises")    # -is
        self.assertEqual(pluralize_oc("serf"), "serfes")    # -f
        self.assertEqual(pluralize_oc("text"), "textes")    # -xt
        self.assertEqual(pluralize_oc("votz"), "voses")     # -tz
        self.assertEqual(pluralize_oc("cinc"), "cincs")
        self.assertEqual(pluralize_oc("ostal"), "ostals")

    def test_half_words(self):
        # bare half spellings from issue #302
        self.assertEqual(extract_number("mièg", lang="oc"), 0.5)
        self.assertEqual(extract_number("mièja", lang="oc"), 0.5)
        self.assertEqual(extract_number("mèg", lang="oc"), 0.5)
        self.assertEqual(extract_number("mèja", lang="oc"), 0.5)

    def test_analytic_hundreds(self):
        self.assertEqual(extract_number("cent", lang="oc"), 100)
        self.assertEqual(extract_number("cent vint", lang="oc"), 120)
        self.assertEqual(extract_number("dos cents", lang="oc"), 200)
        self.assertEqual(extract_number("dos cents trenta quatre", lang="oc"), 234)
        self.assertEqual(extract_number("nòu cents nonanta nòu", lang="oc"), 999)

    def test_thousands(self):
        self.assertEqual(extract_number("mila", lang="oc"), 1000)
        self.assertEqual(extract_number("dos mila", lang="oc"), 2000)
        self.assertEqual(extract_number("dos mila tres cents", lang="oc"), 2300)
        self.assertEqual(extract_number("un milion", lang="oc"), 1000000)
        self.assertEqual(extract_number("dos milions", lang="oc"), 2000000)
        self.assertEqual(extract_number("un miliard", lang="oc"), 1000000000)

    def test_decimals(self):
        self.assertEqual(extract_number("tres virgula catòrze", lang="oc"), 3.14)
        self.assertEqual(extract_number("trenta cinc virgula quatre", lang="oc"), 35.4)

    def test_negative(self):
        self.assertEqual(extract_number("mens sèt", lang="oc"), -7)
        self.assertEqual(extract_number("mens vint e un", lang="oc"), -21)

    def test_fraction_words(self):
        self.assertEqual(extract_number("un e mièg", lang="oc"), 1.5)
        self.assertEqual(extract_number("tres quarts", lang="oc"), 0.75)

    def test_ordinal_extraction(self):
        self.assertEqual(extract_number("lo tresen còp", ordinals=True, lang="oc"), 3)
        self.assertEqual(extract_number("la primièra vegada", ordinals=True, lang="oc"), 1)
        self.assertEqual(extract_number("vint-e-unen", ordinals=True, lang="oc"), 21)

    def test_in_sentence(self):
        self.assertEqual(extract_number("i a vint e un gats", lang="oc"), 21)
        self.assertEqual(extract_number("son dos cents trenta quilòmetres", lang="oc"), 230)

    def test_no_number(self):
        self.assertFalse(extract_number("bon jorn", lang="oc"))


class TestNumbersToDigitsOC(unittest.TestCase):
    def test_replace(self):
        self.assertEqual(numbers_to_digits("i a vint e un gats", lang="oc"), "i a 21 gats")
        self.assertEqual(numbers_to_digits("dos cents trenta quatre ostals", lang="oc"),
                         "234 ostals")

    def test_passthrough(self):
        self.assertEqual(numbers_to_digits("bon jorn amics", lang="oc"), "bon jorn amics")


class TestRoundTripOC(unittest.TestCase):


    def test_sweep_feminine(self):
        for n in (1, 2, 21, 22, 31, 42, 101, 202):
            spoken = OC.pronounce_number(n, gender=GrammaticalGender.FEMININE)
            self.assertEqual(extract_number(spoken, lang="oc"), n, f"{n}: {spoken!r}")

    def test_sweep_ordinals(self):
        for n in (1, 2, 3, 9, 10, 11, 16, 20, 30, 90, 100, 1000):
            spoken = OC.pronounce_ordinal(n)
            self.assertEqual(extract_number(spoken, ordinals=True, lang="oc"), n,
                             f"{n}: {spoken!r}")


if __name__ == "__main__":
    unittest.main()
