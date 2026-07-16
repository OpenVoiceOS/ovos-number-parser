import unittest

from ovos_number_parser import (extract_number, is_fractional, is_ordinal,
                                pronounce_number, pronounce_ordinal)


class TestPronounceNumberSl(unittest.TestCase):
    def test_anchors(self):
        cases = [(0, "nič"), (1, "ena"), (2, "dve"), (5, "pet"),
                 (11, "enajst"), (20, "dvajset"), (21, "enaindvajset"),
                 (25, "petindvajset"), (99, "devetindevetdeset"),
                 (100, "sto"), (200, "dvesto"), (1000, "tisoč")]
        for n, expected in cases:
            self.assertEqual(pronounce_number(n, "sl"), expected, n)

    def test_negative(self):
        self.assertEqual(pronounce_number(-5, "sl"), "minus pet")

    def test_ordinals(self):
        cases = [(1, "prvi"), (2, "drugi"), (3, "tretji"), (10, "deseti"),
                 (21, "enaindvajseti"), (100, "stoti")]
        for n, expected in cases:
            self.assertEqual(pronounce_ordinal(n, "sl"), expected, n)


class TestExtractNumberSl(unittest.TestCase):
    def test_anchors(self):
        cases = [("nič", 0), ("ena", 1), ("dve", 2), ("dva", 2),
                 ("enajst", 11), ("dvajset", 20), ("enaindvajset", 21),
                 ("petindvajset", 25), ("devetindevetdeset", 99),
                 ("sto", 100), ("dvesto", 200), ("sto enaindvajset", 121),
                 ("tisoč", 1000), ("dva tisoč tristo", 2300),
                 ("milijon", 1000000), ("dva milijona", 2000000)]
        for spoken, expected in cases:
            self.assertEqual(extract_number(spoken, "sl"), expected, spoken)

    def test_digits(self):
        self.assertEqual(extract_number("5 mačk", "sl"), 5)
        self.assertEqual(extract_number("5,2 kilograma", "sl"), 5.2)

    def test_negative(self):
        self.assertEqual(extract_number("minus pet", "sl"), -5)
        self.assertEqual(extract_number("minus dvajset stopinj", "sl"), -20)

    def test_decimals(self):
        self.assertEqual(extract_number("pet celih dve", "sl"), 5.2)
        self.assertEqual(extract_number("dve celi tri pet", "sl"), 2.35)

    def test_fractions(self):
        self.assertEqual(extract_number("polovica", "sl"), 0.5)
        self.assertAlmostEqual(extract_number("dve tretjini", "sl"), 2 / 3)

    def test_in_sentence(self):
        self.assertEqual(extract_number("imam petindvajset mačk", "sl"), 25)
        self.assertEqual(
            extract_number("to stane dva tisoč evrov", "sl"), 2000)

    def test_ordinals_flag(self):
        self.assertEqual(
            extract_number("drugi poskus", "sl", ordinals=True), 2)
        self.assertEqual(
            extract_number("enaindvajseti dan", "sl", ordinals=True), 21)

    def test_no_number(self):
        self.assertFalse(extract_number("dobro jutro", "sl"))
        self.assertFalse(extract_number("", "sl"))

    def test_round_trip_sweep(self):
        values = list(range(0, 121)) + [150, 222, 345, 999, 1000, 1001,
                                        2500, 9999, 12345, 100000, 123456,
                                        1000000, 2000000]
        for n in values:
            spoken = pronounce_number(n, "sl")
            self.assertEqual(extract_number(spoken, "sl"), n,
                             f"{n} -> {spoken!r}")

    def test_negative_round_trip(self):
        for n in (-1, -21, -100, -2500):
            spoken = pronounce_number(n, "sl")
            self.assertEqual(extract_number(spoken, "sl"), n,
                             f"{n} -> {spoken!r}")


class TestHelpersSl(unittest.TestCase):
    def test_is_fractional(self):
        self.assertEqual(is_fractional("polovica", "sl"), 0.5)
        self.assertAlmostEqual(is_fractional("tretjina", "sl"), 1 / 3)
        # inflected forms used after numerals
        self.assertAlmostEqual(is_fractional("tretjini", "sl"), 1 / 3)
        self.assertAlmostEqual(is_fractional("tretjine", "sl"), 1 / 3)
        self.assertFalse(is_fractional("mačka", "sl"))

    def test_is_ordinal(self):
        self.assertEqual(is_ordinal("prvi", "sl"), 1)
        self.assertEqual(is_ordinal("deseti", "sl"), 10)
        self.assertEqual(is_ordinal("enaindvajseti", "sl"), 21)
        self.assertFalse(is_ordinal("pes", "sl"))


if __name__ == "__main__":
    unittest.main()
