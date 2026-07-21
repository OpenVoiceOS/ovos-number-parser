"""Danish writes numerals above 100 as separate words, and 100/1000 plainly.

Sources (Dansk Sprognævn / Retskrivningsordbogen, via sproget.dk):

* Politikens sprogklumme "Den 101. dalmatiner møder den 101. stryger"
  (https://sproget.dk/.../den-101-dalmatiner-moeder-den-101-stryger/):
  "en helt fjerde form, hundrede, er den korrekte form ifølge
  Retskrivningsordbogen" -- 100 is "hundrede", not "et hundrede"; and
  "talord over 100 [...] deles op i modsætning til talord under 100" --
  numerals above 100 are split into separate words, those below 100 are one
  word. The linking "og" is optional ("hundred(e) (og) syttende").
* svarbase SV00000047 for the vigesimal tens (halvtreds 50 ... halvfems 90).

The library previously fused everything and prefixed "et": 100 was
"ethundrede", 1000 "ettusinde", 1500 "ettusindefemhundrede". The last even
broke parsing -- it round-tripped to 100500.

Archived under papers/linguistics/da/.
"""
import unittest

from ovos_number_parser import pronounce_number, extract_number


class TestHundredIsPlain(unittest.TestCase):
    def test_100_has_no_et_prefix(self):
        self.assertEqual(pronounce_number(100, "da"), "hundrede")

    def test_1000_is_tusind(self):
        self.assertEqual(pronounce_number(1000, "da"), "tusind")

    def test_multiples_prefix_the_count(self):
        self.assertEqual(pronounce_number(200, "da"), "to hundrede")
        self.assertEqual(pronounce_number(500, "da"), "fem hundrede")


class TestSplitAboveHundred(unittest.TestCase):
    """Groups above 100 are separate words joined by "og" before the rest."""

    CASES = [
        (101, "hundrede og et"),
        (111, "hundrede og elleve"),
        (123, "hundrede og treogtyve"),
        (253, "to hundrede og treoghalvtreds"),
        (999, "ni hundrede og nioghalvfems"),
        (5953, "fem tusinde ni hundrede og treoghalvtreds"),  # sproget.dk example
    ]

    def test_split_forms(self):
        for value, expected in self.CASES:
            with self.subTest(value=value):
                self.assertEqual(pronounce_number(value, "da"), expected)

    def test_below_hundred_stays_one_word(self):
        # the split rule applies ONLY above 100
        for value, word in [(24, "fireogtyve"), (42, "toogfyrre"),
                            (99, "nioghalvfems")]:
            with self.subTest(value=value):
                self.assertEqual(pronounce_number(value, "da"), word)


class TestParsingStillPermissive(unittest.TestCase):
    """The old fused spellings must keep parsing -- they are valid input."""

    FUSED = {
        "ethundrede": 100,
        "ettusinde": 1000,
        "tohundrede": 200,
        "ethundredeettusinde": 101000,
        "nihundredenioghalvfems": 999,
    }

    def test_fused_forms_accepted(self):
        for spelled, value in self.FUSED.items():
            with self.subTest(spelled=spelled):
                self.assertEqual(extract_number(spelled, "da"), value)

    def test_new_split_forms_also_parse(self):
        for spelled, value in [("hundrede", 100), ("tusind", 1000),
                              ("tusind fem hundrede", 1500),
                              ("fem tusinde ni hundrede og treoghalvtreds", 5953)]:
            with self.subTest(spelled=spelled):
                self.assertEqual(extract_number(spelled, "da"), value)


class TestRoundTrip(unittest.TestCase):
    """Every spoken form must read back as the same integer."""

    def test_exhaustive_round_trip(self):
        values = list(range(0, 1001)) + [
            1001, 1500, 2000, 2023, 5953, 10000, 21000, 100000, 123456,
            1000000, 2500000]
        for value in values:
            with self.subTest(value=value):
                spoken = pronounce_number(value, "da")
                self.assertEqual(extract_number(spoken, "da"), value)


class TestNaturalSentences(unittest.TestCase):
    def test_sentences(self):
        cases = [
            ("jeg har hundrede kroner", 100),
            ("der var fem hundrede mennesker", 500),
            ("bogen koster tusind kroner", 1000),
            ("tusind fem hundrede meter", 1500),
        ]
        for sentence, value in cases:
            with self.subTest(sentence=sentence):
                self.assertEqual(extract_number(sentence, "da"), value)


class TestAdversarial(unittest.TestCase):
    """Cases written to break the folder, not to confirm it."""

    def test_bare_addends_not_summed(self):
        # "tre en halv" is 3 and a half, not 3+1 folded to 4
        self.assertEqual(extract_number("tre en halv", "da"), 3.5)

    def test_decimal_digits_not_folded(self):
        # digits after "komma" are read one by one, never summed
        self.assertEqual(extract_number("tre komma et fire", "da"), 3.14)

    def test_scale_word_without_multiplier(self):
        self.assertEqual(extract_number("hundrede", "da"), 100)
        self.assertEqual(extract_number("tusind", "da"), 1000)

    def test_non_number_text_survives_folding(self):
        # a folded group must not eat following words
        self.assertEqual(extract_number("to hundrede og halvtreds huse", "da"),
                         250)

    def test_negative_scaled_group(self):
        self.assertEqual(extract_number("minus to tusinde", "da"), -2000)
