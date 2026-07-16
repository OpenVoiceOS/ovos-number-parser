import unittest

from ovos_number_parser import (extract_number, is_fractional, is_ordinal,
                                pronounce_number, pronounce_ordinal)
from ovos_number_parser.util import GrammaticalGender


class TestPronounceNumberKab(unittest.TestCase):
    def test_amazigh_units(self):
        cases = [(0, "ilem"), (1, "yiwen"), (2, "sin"), (3, "kṛaḍ"),
                 (4, "kuẓ"), (5, "semmus"), (6, "sḍis"), (7, "sa"),
                 (8, "tam"), (9, "tẓa"), (10, "mraw")]
        for n, expected in cases:
            self.assertEqual(pronounce_number(n, "kab"), expected, n)

    def test_feminine(self):
        self.assertEqual(pronounce_number(1, "kab",
                                          gender=GrammaticalGender.FEMININE),
                         "yiwet")
        self.assertEqual(pronounce_number(2, "kab",
                                          gender=GrammaticalGender.FEMININE),
                         "snat")

    def test_teens(self):
        cases = [(11, "ḥḍac"), (12, "tnac"), (13, "tleṭṭac"),
                 (15, "xemseṭṭac"), (19, "tseɛṭac")]
        for n, expected in cases:
            self.assertEqual(pronounce_number(n, "kab"), expected, n)

    def test_tens_and_compounds(self):
        cases = [(20, "ɛecrin"), (21, "waḥed u ɛecrin"),
                 (22, "tnayn u ɛecrin"), (30, "tlatin"),
                 (45, "xemsa u ṛebɛin"), (58, "tmanya u xemsin"),
                 (90, "tsɛin"), (99, "tesɛa u tsɛin")]
        for n, expected in cases:
            self.assertEqual(pronounce_number(n, "kab"), expected, n)

    def test_hundreds_and_thousands(self):
        cases = [(100, "mya"), (200, "mitin"), (300, "telt-mya"),
                 (101, "mya u waḥed"), (121, "mya u waḥed u ɛecrin"),
                 (1000, "alef"), (2000, "juǧ alaf"), (3000, "tlat-alaf"),
                 (2500, "juǧ alaf u xems-mya")]
        for n, expected in cases:
            self.assertEqual(pronounce_number(n, "kab"), expected, n)

    def test_unsupported(self):
        with self.assertRaises(OverflowError):
            pronounce_number(10000, "kab")
        with self.assertRaises(ValueError):
            pronounce_number(-5, "kab")
        with self.assertRaises(ValueError):
            pronounce_number(1.5, "kab")

    def test_ordinals(self):
        cases = [(1, "amezwaru"), (2, "wis sin"), (3, "wis kṛaḍ"),
                 (10, "wis mraw"), (21, "wis waḥed u ɛecrin")]
        for n, expected in cases:
            self.assertEqual(pronounce_ordinal(n, "kab"), expected, n)
        self.assertEqual(
            pronounce_ordinal(1, "kab", gender=GrammaticalGender.FEMININE),
            "tamezwarut")
        self.assertEqual(
            pronounce_ordinal(2, "kab", gender=GrammaticalGender.FEMININE),
            "tis snat")


class TestExtractNumberKab(unittest.TestCase):
    def test_amazigh(self):
        cases = [("yiwen", 1), ("yiwet", 1), ("sin", 2), ("snat", 2),
                 ("kṛaḍ", 3), ("kuẓ", 4), ("semmus", 5), ("sḍis", 6),
                 ("sa", 7), ("tam", 8), ("tẓa", 9), ("mraw", 10),
                 ("mraw d yiwen", 11), ("mraw d sin", 12)]
        for spoken, expected in cases:
            self.assertEqual(extract_number(spoken, "kab"), expected, spoken)

    def test_loans(self):
        cases = [("waḥed", 1), ("tnayn", 2), ("tlata", 3), ("ṛebɛa", 4),
                 ("xemsa", 5), ("setta", 6), ("sebɛa", 7), ("tmanya", 8),
                 ("tesɛa", 9), ("ɛecṛa", 10), ("ḥḍac", 11), ("tnac", 12),
                 ("ɛecrin", 20), ("waḥed u ɛecrin", 21),
                 ("tlata u ṛebɛin", 43), ("mya", 100), ("mitin", 200),
                 ("telt-mya", 300), ("telt mya", 300), ("alef", 1000),
                 ("juǧ alaf", 2000)]
        for spoken, expected in cases:
            self.assertEqual(extract_number(spoken, "kab"), expected, spoken)

    def test_diacritic_tolerance(self):
        self.assertEqual(extract_number("hdac", "kab"), 11)
        self.assertEqual(extract_number("krad", "kab"), 3)

    def test_in_sentence(self):
        self.assertEqual(extract_number("sin n yirgazen", "kab"), 2)
        self.assertEqual(extract_number("7 n wussan", "kab"), 7)

    def test_digits_and_negatives(self):
        self.assertEqual(extract_number("5 kilu", "kab"), 5)
        self.assertEqual(extract_number("5.2", "kab"), 5.2)
        self.assertEqual(extract_number("5,2", "kab"), 5.2)

    def test_no_number(self):
        self.assertFalse(extract_number("xyzzy", "kab"))
        self.assertFalse(extract_number("azul fell-awen", "kab"))

    def test_fraction_word(self):
        self.assertEqual(extract_number("azgen", "kab"), 0.5)

    def test_ordinals_flag(self):
        self.assertEqual(extract_number("wis sin", "kab", ordinals=True), 2)
        self.assertEqual(extract_number("amezwaru", "kab", ordinals=True), 1)

    def test_roundtrip_sweep(self):
        nums = list(range(0, 200)) + [222, 300, 345, 999, 1000, 1001,
                                      2000, 2500, 3333, 9999]
        for n in nums:
            spoken = pronounce_number(n, "kab")
            self.assertEqual(extract_number(spoken, "kab"), n,
                             f"{n}: {spoken!r}")

    def test_ordinal_roundtrip_sweep(self):
        for n in list(range(1, 100)) + [100, 999]:
            spoken = pronounce_ordinal(n, "kab")
            self.assertEqual(is_ordinal(spoken, "kab"), n,
                             f"{n}: {spoken!r}")


class TestIsFractionalKab(unittest.TestCase):
    def test_half(self):
        self.assertEqual(is_fractional("azgen", "kab"), 0.5)

    def test_not_fraction(self):
        self.assertFalse(is_fractional("xyzzy", "kab"))
        self.assertFalse(is_fractional("yiwen", "kab"))


class TestIsOrdinalKab(unittest.TestCase):
    def test_ordinals(self):
        self.assertEqual(is_ordinal("amezwaru", "kab"), 1)
        self.assertEqual(is_ordinal("tamezwarut", "kab"), 1)
        self.assertEqual(is_ordinal("wis sin", "kab"), 2)
        self.assertEqual(is_ordinal("tis snat", "kab"), 2)
        self.assertEqual(is_ordinal("wis tlata", "kab"), 3)

    def test_not_ordinal(self):
        self.assertFalse(is_ordinal("xyzzy", "kab"))
        self.assertFalse(is_ordinal("sin", "kab"))


if __name__ == "__main__":
    unittest.main()
