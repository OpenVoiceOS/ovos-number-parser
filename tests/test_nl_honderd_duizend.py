"""Dutch drops the "een" before "honderd" and "duizend".

100 is "honderd", not "eenhonderd"; 1000 is "duizend", not "eenduizend". The
leading "one" is written only from two hundred / two thousand up.

Source: Nederlandse Taalunie, Taaladvies "Aaneenschrijven van telwoorden
(algemeen)" (https://taaladvies.net/aaneenschrijven-van-telwoorden-algemeen/),
whose own examples are "achthonderd" (800), "honderdvijfendertig" (135) and
"honderdduizend" (100 000) -- never "een" before the scale word. Confirmed
against ICU RBNF and num2words, which both spell "honderd" / "duizend".
Archived under papers/linguistics/nl/.

From a million up the count word IS written, and there "één miljoen" (accented)
marks the numeral apart from the article "een" ("a million"), so that form is
intentionally left in place.
"""
import unittest

from ovos_number_parser import pronounce_number, extract_number


class TestNoLeadingEen(unittest.TestCase):
    CASES = [
        (100, "honderd"),
        (101, "honderdeen"),
        (135, "honderdvijfendertig"),       # Taalunie example
        (1000, "duizend"),
        (1135, "duizendhonderdvijfendertig"),
        (100000, "honderdduizend"),          # Taalunie example
    ]

    def test_no_een_prefix(self):
        for value, expected in self.CASES:
            with self.subTest(value=value):
                out = pronounce_number(value, "nl")
                self.assertEqual(out, expected)
                self.assertFalse(out.startswith("een"),
                                 f"{value} kept a leading een: {out!r}")


class TestLeadingCountFromTwoUp(unittest.TestCase):
    CASES = [(200, "tweehonderd"), (800, "achthonderd"),   # Taalunie example
             (235, "tweehonderdvijfendertig"), (2000, "tweeduizend")]

    def test_count_written_from_two(self):
        for value, expected in self.CASES:
            with self.subTest(value=value):
                self.assertEqual(pronounce_number(value, "nl"), expected)


class TestMillionKeepsAccentedEen(unittest.TestCase):
    """"één miljoen" is intentional: it marks the numeral, not the article."""

    def test_million(self):
        self.assertEqual(pronounce_number(1000000, "nl").strip(), "één miljoen")


class TestRoundTrip(unittest.TestCase):
    def test_round_trip(self):
        for value in list(range(0, 1001)) + [
                1100, 1135, 2000, 21000, 100000, 123456, 1000000]:
            with self.subTest(value=value):
                spoken = pronounce_number(value, "nl")
                self.assertEqual(extract_number(spoken, "nl"), value)


class TestParsingPermissive(unittest.TestCase):
    """The old "eenhonderd"/"eenduizend" spellings must still parse."""

    def test_old_spellings_accepted(self):
        for spelled, value in [("eenhonderd", 100), ("eenduizend", 1000),
                              ("honderd", 100), ("duizend", 1000)]:
            with self.subTest(spelled=spelled):
                self.assertEqual(extract_number(spelled, "nl"), value)
