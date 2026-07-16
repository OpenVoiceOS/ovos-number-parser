import unittest

from ovos_number_parser import (extract_number, is_fractional, is_ordinal,
                                pronounce_number, pronounce_ordinal)


class TestPronounceNumberHu(unittest.TestCase):
    def test_anchors(self):
        cases = [(0, "nulla"), (1, "egy"), (2, "kettő"), (7, "hét"),
                 (11, "tizenegy"), (20, "húsz"), (21, "huszonegy"),
                 (25, "huszonöt"), (30, "harminc"), (99, "kilencvenkilenc"),
                 (100, "száz"), (101, "százegy"), (200, "kétszáz"),
                 (222, "kétszázhuszonkettő"), (345, "háromszáznegyvenöt"),
                 (1000, "ezer"), (2500, "kétezer-ötszáz"),
                 (1000000, "egymillió"), (2000000, "kétmillió")]
        for n, expected in cases:
            self.assertEqual(pronounce_number(n, "hu"), expected, n)

    def test_negative(self):
        self.assertEqual(pronounce_number(-5, "hu"), "mínusz öt")

    def test_ordinals(self):
        cases = [(1, "első"), (2, "második"), (3, "harmadik"),
                 (10, "tizedik"), (20, "huszadik")]
        for n, expected in cases:
            self.assertEqual(pronounce_ordinal(n, "hu"), expected, n)


class TestExtractNumberHu(unittest.TestCase):
    def test_anchors(self):
        cases = [("nulla", 0), ("egy", 1), ("kettő", 2), ("két", 2),
                 ("tizenegy", 11), ("húsz", 20), ("huszonöt", 25),
                 ("kilencvenkilenc", 99), ("száz", 100),
                 ("kétszázhuszonkettő", 222), ("ezer", 1000),
                 ("ezeregy", 1001), ("kétezer-ötszáz", 2500),
                 ("tizenkétezer-háromszáznegyvenöt", 12345),
                 ("egymillió", 1000000), ("kétmillió", 2000000)]
        for spoken, expected in cases:
            self.assertEqual(extract_number(spoken, "hu"), expected, spoken)

    def test_digits(self):
        self.assertEqual(extract_number("5 macska", "hu"), 5)
        self.assertEqual(extract_number("5,2 kiló", "hu"), 5.2)

    def test_negative(self):
        self.assertEqual(extract_number("mínusz öt", "hu"), -5)
        self.assertEqual(extract_number("minusz húsz fok", "hu"), -20)

    def test_decimals(self):
        self.assertEqual(extract_number("öt egész két tized", "hu"), 5.2)
        self.assertEqual(
            extract_number("három egész tizenöt század", "hu"), 3.15)
        self.assertAlmostEqual(
            extract_number("mínusz három egész öt tized", "hu"), -3.5)

    def test_fractions(self):
        self.assertEqual(extract_number("fél", "hu"), 0.5)
        self.assertAlmostEqual(extract_number("két harmad", "hu"), 2 / 3)
        self.assertEqual(extract_number("három negyed", "hu"), 0.75)

    def test_in_sentence(self):
        self.assertEqual(
            extract_number("van huszonöt macskám", "hu"), 25)
        self.assertEqual(
            extract_number("kérek kétezer-ötszáz forintot", "hu"), 2500)

    def test_ordinals_flag(self):
        self.assertEqual(
            extract_number("a második emelet", "hu", ordinals=True), 2)
        self.assertEqual(
            extract_number("a huszadik alkalommal", "hu", ordinals=True), 20)

    def test_no_number(self):
        self.assertFalse(extract_number("jó reggelt", "hu"))
        self.assertFalse(extract_number("", "hu"))

    def test_round_trip_sweep(self):
        values = list(range(0, 121)) + [150, 222, 345, 999, 1000, 1001,
                                        2500, 9999, 12345, 100000, 123456,
                                        1000000, 2000000]
        for n in values:
            spoken = pronounce_number(n, "hu")
            self.assertEqual(extract_number(spoken, "hu"), n,
                             f"{n} -> {spoken!r}")

    def test_negative_round_trip(self):
        for n in (-1, -21, -100, -2500):
            spoken = pronounce_number(n, "hu")
            self.assertEqual(extract_number(spoken, "hu"), n,
                             f"{n} -> {spoken!r}")


class TestHelpersHu(unittest.TestCase):
    def test_is_fractional(self):
        self.assertEqual(is_fractional("fél", "hu"), 0.5)
        self.assertAlmostEqual(is_fractional("harmad", "hu"), 1 / 3)
        self.assertEqual(is_fractional("negyed", "hu"), 0.25)
        self.assertFalse(is_fractional("macska", "hu"))

    def test_is_ordinal(self):
        self.assertEqual(is_ordinal("első", "hu"), 1)
        self.assertEqual(is_ordinal("második", "hu"), 2)
        self.assertEqual(is_ordinal("tizedik", "hu"), 10)
        self.assertEqual(is_ordinal("huszonegyedik", "hu"), 21)
        self.assertFalse(is_ordinal("kutya", "hu"))


if __name__ == "__main__":
    unittest.main()
