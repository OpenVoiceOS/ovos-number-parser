import unittest

from ovos_number_parser import (extract_number, is_fractional, is_ordinal,
                                numbers_to_digits, pronounce_number,
                                pronounce_ordinal)
from ovos_number_parser.numbers_et import extract_numbers_et, nice_number_et


class TestPronounceNumberEt(unittest.TestCase):
    def test_anchors(self):
        # tens and hundreds agglutinate ("kakskümmend", "kakssada") but the
        # following units are separate words per EKI orthography
        cases = [(0, "null"), (1, "üks"), (2, "kaks"), (7, "seitse"),
                 (10, "kümme"), (11, "üksteist"), (12, "kaksteist"),
                 (16, "kuusteist"), (20, "kakskümmend"),
                 (21, "kakskümmend üks"), (25, "kakskümmend viis"),
                 (30, "kolmkümmend"), (99, "üheksakümmend üheksa"),
                 (100, "sada"), (101, "sada üks"), (200, "kakssada"),
                 (222, "kakssada kakskümmend kaks"),
                 (345, "kolmsada nelikümmend viis"),
                 (1000, "tuhat"), (1001, "tuhat üks"),
                 (2500, "kaks tuhat viissada"),
                 (12345, "kaksteist tuhat kolmsada nelikümmend viis"),
                 (1000000, "miljon"), (2000000, "kaks miljonit"),
                 (1000000000, "miljard")]
        for n, expected in cases:
            self.assertEqual(pronounce_number(n, "et"), expected, n)

    def test_negative(self):
        self.assertEqual(pronounce_number(-5, "et"), "miinus viis")

    def test_decimals(self):
        self.assertEqual(pronounce_number(5.2, "et"), "viis koma kaks")
        self.assertEqual(pronounce_number(3.14, "et"),
                         "kolm koma üks neli")

    def test_ordinals(self):
        cases = [(1, "esimene"), (2, "teine"), (3, "kolmas"), (4, "neljas"),
                 (5, "viies"), (6, "kuues"), (7, "seitsmes"),
                 (8, "kaheksas"), (9, "üheksas"), (10, "kümnes"),
                 (11, "üheteistkümnes"), (12, "kaheteistkümnes"),
                 (20, "kahekümnes"), (21, "kahekümne esimene"),
                 (30, "kolmekümnes"), (100, "sajas"), (200, "kahesajas"),
                 (1000, "tuhandes"), (1000000, "miljones")]
        for n, expected in cases:
            self.assertEqual(pronounce_ordinal(n, "et"), expected, n)


class TestExtractNumberEt(unittest.TestCase):
    def test_anchors(self):
        cases = [("null", 0), ("üks", 1), ("kaks", 2), ("kümme", 10),
                 ("üksteist", 11), ("kakskümmend", 20),
                 ("kakskümmend üks", 21), ("üheksakümmend üheksa", 99),
                 ("sada", 100), ("sada üks", 101), ("kakssada", 200),
                 ("kakssada kakskümmend kaks", 222), ("tuhat", 1000),
                 ("tuhat üks", 1001), ("kaks tuhat viissada", 2500),
                 ("kaksteist tuhat kolmsada nelikümmend viis", 12345),
                 ("miljon", 1000000), ("kaks miljonit", 2000000)]
        for spoken, expected in cases:
            self.assertEqual(extract_number(spoken, "et"), expected, spoken)

    def test_in_sentence(self):
        self.assertEqual(extract_number("mul on kolm õuna", "et"), 3)
        self.assertEqual(
            extract_number("oota kakskümmend viis minutit", "et"), 25)

    def test_digits(self):
        self.assertEqual(extract_number("5 kassi", "et"), 5)
        self.assertEqual(extract_number("5,2 kilo", "et"), 5.2)

    def test_negative(self):
        self.assertEqual(extract_number("miinus viis", "et"), -5)
        self.assertEqual(
            extract_number("miinus kakskümmend kraadi", "et"), -20)

    def test_decimals(self):
        self.assertEqual(extract_number("viis koma kaks", "et"), 5.2)
        self.assertEqual(extract_number("kolm koma üks neli", "et"), 3.14)

    def test_fractions(self):
        self.assertEqual(extract_number("pool", "et"), 0.5)
        self.assertEqual(extract_number("poolteist", "et"), 1.5)
        self.assertEqual(extract_number("veerand", "et"), 0.25)
        self.assertAlmostEqual(
            extract_number("kaks kolmandikku", "et"), 2 / 3)
        self.assertEqual(extract_number("kolm neljandikku", "et"), 0.75)

    def test_ordinals(self):
        self.assertEqual(
            extract_number("teine korrus", "et", ordinals=True), 2)
        self.assertEqual(
            extract_number("kolmas koht", "et", ordinals=True), 3)

    def test_no_number(self):
        self.assertFalse(extract_number("siin pole midagi", "et"))

    def test_roundtrip_sweep(self):
        for n in list(range(0, 1000)) + [1234, 9999, 12345, 100000,
                                         999999, 1000000, 2000000]:
            spoken = pronounce_number(n, "et")
            self.assertEqual(extract_number(spoken, "et"), n, spoken)

    def test_ordinal_roundtrip_sweep(self):
        for n in list(range(1, 101)) + [200, 1000, 1000000]:
            spoken = pronounce_ordinal(n, "et")
            self.assertEqual(is_ordinal(spoken, "et"), n, spoken)


class TestExtractNumbersEt(unittest.TestCase):
    def test_multiple(self):
        self.assertEqual(
            extract_numbers_et("kaks kassi ja kolm koera"), [2, 3])
        self.assertEqual(
            extract_numbers_et("miinus viis ja kakskümmend"), [-5, 20])


class TestMiscEt(unittest.TestCase):
    def test_is_fractional(self):
        self.assertEqual(is_fractional("pool", "et"), 0.5)
        self.assertAlmostEqual(is_fractional("kolmandik", "et"), 1 / 3)
        self.assertEqual(is_fractional("neljandik", "et"), 0.25)
        self.assertEqual(is_fractional("veerand", "et"), 0.25)
        self.assertFalse(is_fractional("kass", "et"))

    def test_nice_number(self):
        self.assertEqual(nice_number_et(4.5), "4 ja pool")
        self.assertEqual(nice_number_et(2 / 3), "kaks kolmandikku")
        self.assertEqual(nice_number_et(1 / 3), "kolmandik")
        self.assertEqual(nice_number_et(4.5, speech=False), "4 1/2")

    def test_numbers_to_digits(self):
        self.assertEqual(
            numbers_to_digits("oota kakskümmend üks minutit", "et"),
            "oota 21 minutit")


if __name__ == "__main__":
    unittest.main()
