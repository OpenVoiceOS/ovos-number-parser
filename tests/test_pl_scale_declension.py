"""Polish scale-word declension and the dropped "jeden" before a single scale.

Polish agreement (standard grammar, e.g. zpe.gov.pl "Odmiana liczebnika i
zaimka", archived under papers/linguistics/pl/):

* a quantity ending in 2, 3 or 4 -- but NOT 12, 13, 14 -- puts the scale word
  in the NOMINATIVE plural: "dwa tysiące", "dwadzieścia dwa tysiące",
  "dwa miliony";
* everything else -- 1, 5-9, the teens, and crucially anything ending in 1
  above one (21, 31, ...) -- puts it in the GENITIVE plural: "pięć tysięcy",
  "dwanaście tysięcy", "dwadzieścia jeden tysięcy", "dwanaście milionów";
* a single scale unit is just the bare scale word: 1000 is "tysiąc", never
  "jeden tysiąc".

The library had two bugs: it applied the nominative-plural ending to numbers
ending in 1 ("dwadzieścia jeden tysiące") and to the million teens, and it
prefixed a spurious "jeden" to a lone thousand ("jeden tysiąc, sto"). It also
joined groups with a comma; Polish speaks them with a space.

Both errors were caught by a differential harness where ICU RBNF and num2words
agreed with each other against us. Expected values here follow the grammar,
not either library.
"""
import unittest

from ovos_number_parser import pronounce_number, extract_number


class TestGenitivePluralEndingInOne(unittest.TestCase):
    """Ending in 1 (but not 1 itself) -> genitive plural, never nominative."""

    CASES = [
        (21000, "dwadzieścia jeden tysięcy"),
        (31000, "trzydzieści jeden tysięcy"),
        (121000, "sto dwadzieścia jeden tysięcy"),
        (21000000, "dwadzieścia jeden milionów"),
    ]

    def test_genitive(self):
        for value, expected in self.CASES:
            with self.subTest(value=value):
                self.assertEqual(pronounce_number(value, "pl"), expected)


class TestNominativePluralTwoThreeFour(unittest.TestCase):
    CASES = [
        (2000, "dwa tysiące"),
        (22000, "dwadzieścia dwa tysiące"),
        (23000, "dwadzieścia trzy tysiące"),
        (24000, "dwadzieścia cztery tysiące"),
        (2000000, "dwa miliony"),
    ]

    def test_nominative(self):
        for value, expected in self.CASES:
            with self.subTest(value=value):
                self.assertEqual(pronounce_number(value, "pl"), expected)


class TestTeensAreGenitive(unittest.TestCase):
    """12, 13, 14 are the exception: genitive, not nominative plural."""

    CASES = [
        (12000, "dwanaście tysięcy"),
        (13000, "trzynaście tysięcy"),
        (14000, "czternaście tysięcy"),
        (12000000, "dwanaście milionów"),
    ]

    def test_teens(self):
        for value, expected in self.CASES:
            with self.subTest(value=value):
                self.assertEqual(pronounce_number(value, "pl"), expected)


class TestNoLeadingJeden(unittest.TestCase):
    def test_single_thousand_is_bare(self):
        self.assertEqual(pronounce_number(1000, "pl"), "tysiąc")
        self.assertEqual(pronounce_number(1100, "pl"), "tysiąc sto")
        self.assertEqual(pronounce_number(1000000, "pl"), "milion")

    def test_no_comma_between_groups(self):
        self.assertNotIn(",", pronounce_number(2023, "pl"))
        self.assertEqual(pronounce_number(2023, "pl"),
                         "dwa tysiące dwadzieścia trzy")


class TestRoundTrip(unittest.TestCase):
    def test_round_trip(self):
        values = [1000, 1100, 1500, 2000, 5000, 12000, 21000, 22000, 25000,
                  31000, 112000, 121000, 1000000, 2000000, 12000000, 21000000]
        for value in values:
            with self.subTest(value=value):
                spoken = pronounce_number(value, "pl")
                self.assertEqual(extract_number(spoken, "pl"), value)
