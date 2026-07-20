"""Persian writes 15-18 in their standard dictionary forms, not colloquial.

The library emitted the Tehrani colloquial spellings for the teens -- پونزده,
شونزده, هیفده, هیجده -- as output. The standard written forms, used in
dictionaries and formal text, are پانزده (15), شانزده (16), هفده (17) and هجده
(18). For a TTS/normalisation surface the standard forms are what belongs on
screen and in the output stream.

Source: ویراستاران (virastaran.net) "عددنویسی"; the correct form of 18 is هجده
per Persian dictionaries. Archived under papers/linguistics/fa/. Confirmed
against ICU RBNF and num2words, which both spell the standard forms.

Parsing stays permissive: the colloquial spellings are still accepted, since a
speaker or ASR system will produce them.
"""
import unittest

from ovos_number_parser import pronounce_number, extract_number


class TestStandardOutput(unittest.TestCase):
    CASES = [(15, "پانزده"), (16, "شانزده"), (17, "هفده"), (18, "هجده")]

    def test_standalone(self):
        for value, expected in self.CASES:
            with self.subTest(value=value):
                self.assertEqual(pronounce_number(value, "fa"), expected)

    def test_inside_larger_numbers(self):
        self.assertEqual(pronounce_number(115, "fa"), "صد و پانزده")
        self.assertEqual(pronounce_number(1918, "fa"), "هزار و نهصد و هجده")


class TestColloquialStillParses(unittest.TestCase):
    def test_both_spellings_accepted(self):
        for spelled, value in [("پانزده", 15), ("پونزده", 15),
                              ("شانزده", 16), ("شونزده", 16),
                              ("هفده", 17), ("هیفده", 17),
                              ("هجده", 18), ("هیجده", 18)]:
            with self.subTest(spelled=spelled):
                self.assertEqual(extract_number(spelled, "fa"), value)


class TestRoundTrip(unittest.TestCase):
    def test_round_trip(self):
        for value in [15, 16, 17, 18, 115, 216, 1017, 1918, 2018]:
            with self.subTest(value=value):
                spoken = pronounce_number(value, "fa")
                self.assertEqual(extract_number(spoken, "fa"), value)
