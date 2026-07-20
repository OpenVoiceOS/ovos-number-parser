"""Dutch compound numerals take a trema at a vowel collision.

"twee" and "drie" end in a vowel, so the "e" of the joining "en" would be read
together with it -- "tweeen" invites the reading "twee-en" as one sound. Dutch
resolves this with a trema.

Source: Taaladvies.net (Nederlandse Taalunie), entry "Klinkerbotsing":

    "Deze dubbelzinnigheid wordt opgeheven door de aparte klinkers van elkaar
     te scheiden met een trema (in afleidingen en samengestelde telwoorden) of
     een koppelteken (in samenstellingen). Voorbeelden: zeeën, geëvenaard,
     tweeëntwintig, ..."

Compound numerals are an explicit *exception* to the hyphen used in ordinary
compounds (`gala-avond`, `zee-egel`): they take a trema, and `tweeëntwintig`
is the Taalunie's own example. Archived under papers/linguistics/nl/.

Only "twee" and "drie" end in a vowel; every other unit ends in a consonant
and joins with a plain "en" (`vierentwintig`, `vijfenveertig`).

Parsing already accepted both spellings and must keep doing so -- an ASR
transcript or a user typing without the diacritic is still a valid input.
"""
import unittest

from ovos_number_parser import pronounce_number, extract_number


class TestTremaWritten(unittest.TestCase):
    """Units ending in a vowel take "ën"."""

    CASES = [
        (22, "tweeëntwintig"),          # the Taalunie's own example
        (23, "drieëntwintig"),
        (32, "tweeëndertig"),
        (33, "drieëndertig"),           # cited by Taaladvies as drieëndertig
        (42, "tweeënveertig"),
        (52, "tweeënvijftig"),
        (53, "drieënvijftig"),
        (93, "drieënnegentig"),
    ]

    def test_vowel_final_units_take_trema(self):
        for value, expected in self.CASES:
            with self.subTest(value=value):
                self.assertEqual(pronounce_number(value, "nl"), expected)


class TestNoTremaElsewhere(unittest.TestCase):
    """Units ending in a consonant join with a plain "en"."""

    CASES = [
        (21, "eenentwintig"),
        (24, "vierentwintig"),
        (25, "vijfentwintig"),
        (26, "zesentwintig"),
        (27, "zevenentwintig"),
        (28, "achtentwintig"),
        (29, "negenentwintig"),
        (99, "negenennegentig"),
    ]

    def test_consonant_final_units_have_no_trema(self):
        for value, expected in self.CASES:
            with self.subTest(value=value):
                out = pronounce_number(value, "nl")
                self.assertEqual(out, expected)
                self.assertNotIn("ë", out)


class TestInsideLargerNumbers(unittest.TestCase):
    """The trema survives when the pair sits inside a bigger numeral."""

    def test_hundreds_and_thousands(self):
        self.assertEqual(pronounce_number(122, "nl"),
                         "honderdtweeëntwintig")
        self.assertIn("drieëntwintig", pronounce_number(1023, "nl"))


class TestParsingStaysPermissive(unittest.TestCase):
    """Both spellings must parse: ASR and typing often drop the diacritic."""

    def test_both_spellings_accepted(self):
        for spelled, bare, value in [("tweeëntwintig", "tweeentwintig", 22),
                                     ("drieëndertig", "drieendertig", 33),
                                     ("drieënvijftig", "drieenvijftig", 53)]:
            with self.subTest(value=value):
                self.assertEqual(extract_number(spelled, "nl"), value)
                self.assertEqual(extract_number(bare, "nl"), value)


class TestRoundTrip(unittest.TestCase):
    """What we write must read back as the same number."""

    def test_round_trip(self):
        for value in list(range(20, 100)) + [122, 1023]:
            with self.subTest(value=value):
                spoken = pronounce_number(value, "nl")
                self.assertEqual(extract_number(spoken, "nl"), value)
