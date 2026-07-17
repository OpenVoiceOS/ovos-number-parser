import unittest

from ovos_number_parser import (extract_number, is_fractional, is_ordinal,
                                numbers_to_digits, pronounce_number,
                                pronounce_ordinal)
from ovos_number_parser.numbers_fi import extract_numbers_fi, nice_number_fi


class TestPronounceNumberFi(unittest.TestCase):
    def test_anchors(self):
        cases = [(0, "nolla"), (1, "yksi"), (2, "kaksi"), (7, "seitsemän"),
                 (10, "kymmenen"), (11, "yksitoista"), (12, "kaksitoista"),
                 (16, "kuusitoista"), (20, "kaksikymmentä"),
                 (21, "kaksikymmentäyksi"), (25, "kaksikymmentäviisi"),
                 (30, "kolmekymmentä"), (99, "yhdeksänkymmentäyhdeksän"),
                 (100, "sata"), (101, "satayksi"), (200, "kaksisataa"),
                 (222, "kaksisataakaksikymmentäkaksi"),
                 (345, "kolmesataaneljäkymmentäviisi"),
                 (1000, "tuhat"), (1001, "tuhatyksi"),
                 (2500, "kaksituhattaviisisataa"),
                 (12345, "kaksitoistatuhattakolmesataaneljäkymmentäviisi"),
                 (1000000, "miljoona"), (2000000, "kaksi miljoonaa"),
                 (2300000, "kaksi miljoonaa kolmesataatuhatta"),
                 (1000000000, "miljardi")]
        for n, expected in cases:
            self.assertEqual(pronounce_number(n, "fi"), expected, n)

    def test_negative(self):
        self.assertEqual(pronounce_number(-5, "fi"), "miinus viisi")

    def test_decimals(self):
        self.assertEqual(pronounce_number(5.2, "fi"), "viisi pilkku kaksi")
        self.assertEqual(pronounce_number(3.14, "fi"),
                         "kolme pilkku yksi neljä")

    def test_ordinals(self):
        cases = [(1, "ensimmäinen"), (2, "toinen"), (3, "kolmas"),
                 (4, "neljäs"), (5, "viides"), (6, "kuudes"),
                 (7, "seitsemäs"), (8, "kahdeksas"), (9, "yhdeksäs"),
                 (10, "kymmenes"), (11, "yhdestoista"), (12, "kahdestoista"),
                 (20, "kahdeskymmenes"), (21, "kahdeskymmenesensimmäinen"),
                 (30, "kolmaskymmenes"), (100, "sadas"), (200, "kahdessadas"),
                 (1000, "tuhannes"), (1000000, "miljoonas")]
        for n, expected in cases:
            self.assertEqual(pronounce_ordinal(n, "fi"), expected, n)

    def test_ordinals_scale_multiples(self):
        # a bare scale multiplier takes the compositive ordinal stem
        # (kahdes-/yhdes-), not the standalone ensimmäinen/toinen forms
        cases = [(2000, "kahdestuhannes"), (3000, "kolmastuhannes"),
                 (12000, "kahdestoistatuhannes"),
                 (200000, "kahdessadastuhannes"),
                 (2000000, "kahdesmiljoonas"),
                 (3000000, "kolmasmiljoonas"),
                 (25000000, "kahdeskymmenesviidesmiljoonas")]
        for n, expected in cases:
            self.assertEqual(pronounce_ordinal(n, "fi"), expected, n)

    def test_ordinals_no_recursion_or_crash(self):
        # exact multiples of a million once triggered unbounded recursion
        for n in (2000000, 3000000, 999000000):
            self.assertIsInstance(pronounce_ordinal(n, "fi"), str)
        # above the supported "miljoonas" scale falls back to digits cleanly
        self.assertEqual(pronounce_ordinal(10 ** 9, "fi"), "1000000000")
        self.assertEqual(pronounce_ordinal(999999999999, "fi"),
                         "999999999999")


class TestExtractNumberFi(unittest.TestCase):
    def test_anchors(self):
        cases = [("nolla", 0), ("yksi", 1), ("kaksi", 2), ("kymmenen", 10),
                 ("yksitoista", 11), ("kaksikymmentä", 20),
                 ("kaksikymmentäyksi", 21),
                 ("yhdeksänkymmentäyhdeksän", 99), ("sata", 100),
                 ("satayksi", 101), ("kaksisataa", 200),
                 ("kaksisataakaksikymmentäkaksi", 222), ("tuhat", 1000),
                 ("tuhatyksi", 1001), ("kaksituhattaviisisataa", 2500),
                 ("kaksitoistatuhattakolmesataaneljäkymmentäviisi", 12345),
                 ("miljoona", 1000000), ("kaksi miljoonaa", 2000000),
                 ("kaksi miljoonaa kolmesataatuhatta", 2300000)]
        for spoken, expected in cases:
            self.assertEqual(extract_number(spoken, "fi"), expected, spoken)

    def test_in_sentence(self):
        self.assertEqual(
            extract_number("minulla on kolme omenaa", "fi"), 3)
        self.assertEqual(
            extract_number("odota kaksikymmentäviisi minuuttia", "fi"), 25)

    def test_colloquial(self):
        cases = [("yks", 1), ("kaks", 2), ("viis", 5), ("kuus", 6),
                 ("seittemän", 7)]
        for spoken, expected in cases:
            self.assertEqual(extract_number(spoken, "fi"), expected, spoken)

    def test_digits(self):
        self.assertEqual(extract_number("5 kissaa", "fi"), 5)
        self.assertEqual(extract_number("5,2 kiloa", "fi"), 5.2)

    def test_negative(self):
        self.assertEqual(extract_number("miinus viisi", "fi"), -5)
        self.assertEqual(
            extract_number("miinus kaksikymmentä astetta", "fi"), -20)

    def test_decimals(self):
        self.assertEqual(extract_number("viisi pilkku kaksi", "fi"), 5.2)
        self.assertEqual(
            extract_number("kolme pilkku yksi neljä", "fi"), 3.14)

    def test_fractions(self):
        self.assertEqual(extract_number("puoli", "fi"), 0.5)
        self.assertEqual(extract_number("puolitoista", "fi"), 1.5)
        self.assertAlmostEqual(
            extract_number("kaksi kolmasosaa", "fi"), 2 / 3)
        self.assertEqual(extract_number("kolme neljäsosaa", "fi"), 0.75)
        self.assertAlmostEqual(extract_number("kolmannes", "fi"), 1 / 3)
        self.assertEqual(extract_number("neljännes", "fi"), 0.25)

    def test_ordinals(self):
        self.assertEqual(
            extract_number("toinen kerros", "fi", ordinals=True), 2)
        self.assertEqual(
            extract_number("kahdeskymmenesensimmäinen", "fi",
                           ordinals=True), 21)

    def test_no_number(self):
        self.assertFalse(extract_number("ei mitään täällä", "fi"))

    def test_roundtrip_sweep(self):
        for n in list(range(0, 1000)) + [1234, 9999, 12345, 100000,
                                         999999, 1000000, 2000000]:
            spoken = pronounce_number(n, "fi")
            self.assertEqual(extract_number(spoken, "fi"), n, spoken)

    def test_post_million_remainder(self):
        # a bare leading scale noun ("miljoona", "miljardi") must not swallow
        # the remainder that follows it
        cases = {
            1500000: "miljoona viisisataatuhatta",
            1000001: "miljoona yksi",
            1000300000: "miljardi kolmesataatuhatta",
            1002000000: "miljardi kaksi miljoonaa",
            1001000000: "miljardi miljoona",
            1234567: None,
            7654321: None,
        }
        for n, spoken in cases.items():
            said = pronounce_number(n, "fi")
            if spoken is not None:
                self.assertEqual(said, spoken)
            self.assertEqual(extract_number(said, "fi"), n, said)

    def test_roundtrip_millions_sweep(self):
        for n in range(1000000, 10000001, 12345):
            spoken = pronounce_number(n, "fi")
            self.assertEqual(extract_number(spoken, "fi"), n, spoken)

    def test_ordinal_roundtrip_sweep(self):
        for n in list(range(1, 101)) + [200, 1000, 1000000]:
            spoken = pronounce_ordinal(n, "fi")
            self.assertEqual(is_ordinal(spoken, "fi"), n, spoken)


class TestExtractNumbersFi(unittest.TestCase):
    def test_multiple(self):
        self.assertEqual(
            extract_numbers_fi("kaksi kissaa ja kolme koiraa"), [2, 3])
        self.assertEqual(
            extract_numbers_fi("miinus viisi ja kaksikymmentä"), [-5, 20])


class TestMiscFi(unittest.TestCase):
    def test_is_fractional(self):
        self.assertEqual(is_fractional("puoli", "fi"), 0.5)
        self.assertAlmostEqual(is_fractional("kolmasosa", "fi"), 1 / 3)
        self.assertAlmostEqual(is_fractional("kolmannes", "fi"), 1 / 3)
        self.assertEqual(is_fractional("neljäsosa", "fi"), 0.25)
        self.assertEqual(is_fractional("neljännes", "fi"), 0.25)
        self.assertFalse(is_fractional("kissa", "fi"))

    def test_nice_number(self):
        self.assertEqual(nice_number_fi(4.5), "4 ja puoli")
        self.assertEqual(nice_number_fi(0.75), "kolme neljäsosaa")
        self.assertEqual(nice_number_fi(1 / 3), "kolmasosa")
        self.assertEqual(nice_number_fi(4.5, speech=False), "4 1/2")

    def test_numbers_to_digits(self):
        self.assertEqual(
            numbers_to_digits("odota kaksikymmentäyksi minuuttia", "fi"),
            "odota 21 minuuttia")


if __name__ == "__main__":
    unittest.main()
