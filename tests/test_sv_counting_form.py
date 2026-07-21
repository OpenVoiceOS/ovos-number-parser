"""Swedish spells a bare cardinal 1 as the neuter counting form "ett".

Swedish inflects only the numeral 1: "en" is the common-gender form (used
before an en-word: "en person") and "ett" the neuter form ("ett äpple"). The
bare *counting* form -- how you recite the numbers -- is the neuter one:
"ett, två, tre ... tjugo, tjugoett, trettio ..." (Wikipedia "Räkneord"; the
standard cardinal series). The library emitted the common-gender "en" for a
lone 1 and for the ones digit of the round tens ("tjugoen"), while already
using "ett" inside the hundreds ("etthundraett") -- an internal inconsistency
that both ICU RBNF and num2words resolve to "ett".

Millions and milliards are separate common-gender nouns, so 1 before them keeps
"en" ("en miljon", "en miljard") and they are written as separate words
("två miljoner"), unlike the glued "tvåtusen".

Sources archived under papers/linguistics/sv/.
"""
import unittest

from ovos_number_parser import pronounce_number, extract_number


class TestCountingFormIsEtt(unittest.TestCase):
    CASES = [
        (1, "ett"),
        (21, "tjugoett"),
        (31, "trettioett"),
        (41, "fyrtioett"),
        (91, "nittioett"),
        (101, "etthundraett"),
        (121, "etthundratjugoett"),
        (1021, "ettusen tjugoett"),
    ]

    def test_bare_cardinal_uses_ett(self):
        for value, expected in self.CASES:
            with self.subTest(value=value):
                self.assertEqual(pronounce_number(value, "sv"), expected)


class TestMillionKeepsEnAndSpace(unittest.TestCase):
    """miljon/miljard are en-words and stand as separate words."""

    def test_million(self):
        self.assertEqual(pronounce_number(1000000, "sv").strip(), "en miljon")
        self.assertEqual(pronounce_number(2000000, "sv").strip(),
                         "två miljoner")
        self.assertEqual(pronounce_number(1000000000, "sv").strip(),
                         "en miljard")


class TestParsingPermissive(unittest.TestCase):
    """Both "en" and "ett" forms must parse -- speakers and ASR use both."""

    def test_both_forms_accepted(self):
        for spelled, value in [("ett", 1), ("en", 1),
                              ("tjugoett", 21), ("tjugoen", 21),
                              ("trettioett", 31), ("trettioen", 31)]:
            with self.subTest(spelled=spelled):
                self.assertEqual(extract_number(spelled, "sv"), value)


class TestRoundTrip(unittest.TestCase):
    def test_round_trip(self):
        values = list(range(0, 101)) + [
            101, 121, 1000, 1001, 1021, 21000, 100000, 1000000, 2000000,
            21000000]
        for value in values:
            with self.subTest(value=value):
                spoken = pronounce_number(value, "sv")
                self.assertEqual(extract_number(spoken, "sv"), value)
