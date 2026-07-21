"""French: "quatre-vingt" and "cent" drop their plural -s before "mille".

Académie française (Dictionnaire, 9e éd., entries "vingt" / "cent"): vingt and
cent take an -s "quand ils sont précédés d'un nombre qui les multiplie, mais
ils restent invariables s'ils sont suivis d'un autre nombre ou de mille"
-- so "quatre-vingt mille", "trois cent mille". They DO agree, however, before
"millier/million/milliard, qui sont des noms et non des adjectifs numéraux":
"deux cents millions". "mille" is the only scale word that is a numeral
adjective, so it is the only one that strips the -s.

The library kept the -s before "mille" ("quatre-vingts mille", "trois cents
mille"). It was already correct before "millions" and when the round hundred
ends the number. Source archived under papers/linguistics/fr/.

Note ICU RBNF drops the -s before "millions" too ("quatre-vingt millions"),
which is wrong per the Académie; the expected values here follow the Académie,
not ICU.
"""
import unittest

from ovos_number_parser import pronounce_number, extract_number


class TestNoSBeforeMille(unittest.TestCase):
    CASES = [
        (80000, "quatre-vingt mille"),
        (300000, "trois cent mille"),
        (380000, "trois cent quatre-vingt mille"),
        (280000, "deux cent quatre-vingt mille"),
        (2080000, "deux millions quatre-vingt mille"),
    ]

    def test_drops_s(self):
        for value, expected in self.CASES:
            with self.subTest(value=value):
                self.assertEqual(pronounce_number(value, "fr"), expected)


class TestSKeptBeforeNounScalesAndWhenTerminal(unittest.TestCase):
    """-s stays before million/milliard (nouns) and at the end of the number."""

    CASES = [
        (80, "quatre-vingts"),
        (200, "deux cents"),
        (280, "deux cent quatre-vingts"),
        (80000000, "quatre-vingts millions"),
        (300000000, "trois cents millions"),
        (80000000000, "quatre-vingts milliards"),
    ]

    def test_keeps_s(self):
        for value, expected in self.CASES:
            with self.subTest(value=value):
                self.assertEqual(pronounce_number(value, "fr"), expected)


class TestUnaffectedCases(unittest.TestCase):
    def test_hundred_and_ninety_forms(self):
        # h==1 has no -s anyway; quatre-vingt-dix has no trailing -s
        self.assertEqual(pronounce_number(100000, "fr"), "cent mille")
        self.assertEqual(pronounce_number(90000, "fr"), "quatre-vingt-dix mille")


class TestRoundTrip(unittest.TestCase):
    def test_round_trip(self):
        for value in [80, 200, 280, 80000, 90000, 100000, 300000, 380000,
                      2080000, 80000000, 300000000]:
            with self.subTest(value=value):
                spoken = pronounce_number(value, "fr")
                self.assertEqual(extract_number(spoken, "fr"), value)
