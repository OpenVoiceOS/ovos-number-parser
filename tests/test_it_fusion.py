"""Italian writes a cardinal below a million as one fused word.

Accademia della Crusca, consulenza 1077: "la grafia prevista è, tranne rare
eccezioni, senza spazi: duecentodiecimila e non *duecento dieci mila". So the
whole number up to 999999 is a single word with no spaces and no commas:
"centoventidue", "millecentoventidue", "novecentonovantanovemilanovecento-
novantanove". The library used to insert a space inside the hundreds and a
comma between scale groups ("mille, cento ventidue").

From a million up, milione/miliardo stand as separate words -- "un milione",
"due milioni", "un milione duecentomila" -- which Crusca notes as the practical
form for such large numbers; both ICU and num2words agree.

Two elisions surface once the word is fused, both confirmed by ICU + num2words:
"cento" drops its -o before an o-word ("centottanta", "trecentottantotto"), and
the singular scale word apocopates to "un" ("un milione", not "uno milioni").

Source archived under papers/linguistics/it/.
"""
import unittest

from ovos_number_parser import pronounce_number, extract_number


class TestFusedBelowMillion(unittest.TestCase):
    CASES = [
        (122, "centoventidue"),
        (123, "centoventitré"),
        (999, "novecentonovantanove"),
        (1122, "millecentoventidue"),
        (1234, "milleduecentotrentaquattro"),
        (2023, "duemilaventitré"),
        (100000, "centomila"),
        (210000, "duecentodiecimila"),         # Crusca's own example
        (999999, "novecentonovantanovemilanovecentonovantanove"),
    ]

    def test_one_fused_word(self):
        for value, expected in self.CASES:
            with self.subTest(value=value):
                out = pronounce_number(value, "it")
                self.assertEqual(out, expected)
                self.assertNotIn(" ", out)
                self.assertNotIn(",", out)


class TestCentoElision(unittest.TestCase):
    """cento drops -o before an o-word (both refs agree)."""

    CASES = [(108, "centotto"), (180, "centottanta"),
             (188, "centottantotto"), (380, "trecentottanta"),
             (788, "settecentottantotto"), (880, "ottocentottanta")]

    def test_elision(self):
        for value, expected in self.CASES:
            with self.subTest(value=value):
                self.assertEqual(pronounce_number(value, "it"), expected)

    def test_no_elision_before_non_o(self):
        # cento + uno keeps both vowels (centouno, not centuno)
        self.assertEqual(pronounce_number(101, "it"), "centouno")


class TestMillionsAreSeparateWords(unittest.TestCase):
    CASES = [
        (1000000, "un milione"),
        (2000000, "due milioni"),
        (1000000000, "un miliardo"),
        (1234567, "un milione duecentotrentaquattromilacinquecentosessantasette"),
    ]

    def test_millions(self):
        for value, expected in self.CASES:
            with self.subTest(value=value):
                self.assertEqual(pronounce_number(value, "it"), expected)


class TestRoundTrip(unittest.TestCase):
    """Every fused form must read back -- the extractor un-fuses and un-elides."""

    def test_exhaustive(self):
        values = list(range(0, 2001)) + [
            10000, 21000, 100000, 210000, 999999, 1000000, 1234567,
            3456789, 1000000000]
        for value in values:
            with self.subTest(value=value):
                spoken = pronounce_number(value, "it")
                self.assertEqual(extract_number(spoken, "it"), value)

    def test_old_spaced_forms_still_parse(self):
        # permissive: pre-fusion spellings remain valid input
        for spelled, value in [("cento ventidue", 122),
                              ("mille duecento", 1200)]:
            with self.subTest(spelled=spelled):
                self.assertEqual(extract_number(spelled, "it"), value)
