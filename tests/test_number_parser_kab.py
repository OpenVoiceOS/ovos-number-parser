import unittest

from ovos_number_parser import (extract_number, is_fractional, is_ordinal,
                                pronounce_number, pronounce_ordinal,
                                numbers_to_digits)
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
        cases = [(11, "ḥḍac"), (12, "tnac"), (13, "telṭac"),
                 (15, "xemseṭṭac"), (19, "tseɛṭac")]
        for n, expected in cases:
            self.assertEqual(pronounce_number(n, "kab"), expected, n)

    def test_tens_and_compounds(self):
        cases = [(20, "ɛecrin"), (21, "waḥed u ɛecrin"),
                 (22, "tnayn u ɛecrin"), (30, "tlatin"),
                 (45, "xemsa u ṛebɛin"), (58, "tmanya u xemsin"),
                 (90, "tesɛin"), (99, "tesɛa u tesɛin")]
        for n, expected in cases:
            self.assertEqual(pronounce_number(n, "kab"), expected, n)

    def test_hundreds_and_thousands(self):
        cases = [(100, "mya"), (200, "mitin"), (300, "telt-mya"),
                 (101, "mya u waḥed"), (121, "mya u waḥed u ɛecrin"),
                 (1000, "alef"), (2000, "juǧ alaf"), (3000, "telt-alaf"),
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

    def test_pan_amazigh_proposal(self):
        cases = [
            ("mrayan", 11), ("mrasḍis", 16),
            ("snan", 20), ("kraḍan", 30), ("kṛaḍan", 30), ("semmusan", 50),
            ("imdi", 100), ("imda", 100),
            ("agim", 1000), ("igiman", 1000),
            ("amelyun", 1000000), ("amelyar", 1000000000),
            ("snan yiwen", 21), ("kuẓan sḍis", 46),
            ("sin imda", 200), ("tam imda", 800),
            ("sin igiman", 2000), ("kṛaḍ igiman", 3000),
            ("sin igiman tam imda", 2800),
            ("agim kuẓ imda sḍisan sin", 1462),
            ("sin imelyunen", 2000000)
        ]
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
        self.assertEqual(extract_number("kradan", "kab"), 30)

    def test_in_sentence(self):
        self.assertEqual(extract_number("sin n yergazen", "kab"), 2)
        self.assertEqual(extract_number("7 n wussan", "kab"), 7)
        self.assertEqual(extract_number("Sɛeddaɣ sin igiman tam imda n yiseggasen", "kab"), 2800)

    def test_digits_and_negatives(self):
        self.assertEqual(extract_number("5 kilu", "kab"), 5)
        self.assertEqual(extract_number("5.2", "kab"), 5.2)
        self.assertEqual(extract_number("5,2", "kab"), 5.2)

    def test_no_number(self):
        self.assertFalse(extract_number("xyzzy", "kab"))
        self.assertFalse(extract_number("azul fell-awen", "kab"))

    def test_fraction_word(self):
        self.assertEqual(extract_number("azgen", "kab"), 0.5)
        self.assertEqual(extract_number("nnefṣ", "kab"), 0.5)
        self.assertAlmostEqual(extract_number("afkṛad", "kab"), 1/3)
        self.assertEqual(extract_number("afkuẓ", "kab"), 0.25)

    def test_ordinals_flag(self):
        self.assertEqual(extract_number("wis sin", "kab", ordinals=True), 2)
        self.assertEqual(extract_number("amezwaru", "kab", ordinals=True), 1)
        self.assertEqual(extract_number("wiss kṛaḍ", "kab", ordinals=True), 3)

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
        self.assertEqual(is_fractional("nnefṣ", "kab"), 0.5)

    def test_amazigh_fractions(self):
        cases = [
            ("afkṛad", 1/3), ("afkuẓ", 0.25), ("afsemmus", 0.2),
            ("afesmus", 0.2), ("afsḍis", 1/6), ("afsa", 1/7),
            ("aftam", 0.125), ("afṭza", 1/9)
        ]
        for spoken, expected in cases:
            self.assertAlmostEqual(is_fractional(spoken, "kab"), expected, places=5)

    def test_not_fraction(self):
        self.assertFalse(is_fractional("xyzzy", "kab"))
        self.assertFalse(is_fractional("yiwen", "kab"))


class TestIsOrdinalKab(unittest.TestCase):
    def test_ordinals(self):
        cases = [
            ("amezwaru", 1), ("tamezwarut", 1),
            ("wis sin", 2), ("tis snat", 2), ("wis tlata", 3),
            ("wiss kuẓ", 4), ("tis semmuset", 5)
        ]
        for spoken, expected in cases:
            self.assertEqual(is_ordinal(spoken, "kab"), expected)

    def test_not_ordinal(self):
        self.assertFalse(is_ordinal("xyzzy", "kab"))
        self.assertFalse(is_ordinal("sin", "kab"))


class TestNumbersToDigitsKab(unittest.TestCase):
    def test_in_sentence(self):
        self.assertEqual(
            numbers_to_digits("sɛeddaɣ ḥḍac n yiseggasen", "kab"),
            "sɛeddaɣ 11 n yiseggasen")
        self.assertEqual(
            numbers_to_digits("ɣur-i mraw d sin n wussan", "kab"),
            "ɣur-i 12 n wussan")
        self.assertEqual(
            numbers_to_digits("Awi-d agim kuẓ imda sḍisan sin n idularen.", "kab"),
            "Awi-d 1462 n idularen.")

    def test_compound(self):
        self.assertEqual(numbers_to_digits("waḥed u ɛecrin", "kab"), "21")
        self.assertEqual(
            numbers_to_digits("Awi-d telt-mya n idularen.", "kab"),
            "Awi-d 300 n idularen.")

    def test_leaves_non_numbers_untouched(self):
        self.assertEqual(
            numbers_to_digits("kra n wawalen war amḍan", "kab"),
            "kra n wawalen war amḍan")

    def test_digits_passthrough(self):
        self.assertEqual(numbers_to_digits("7 n wussan", "kab"),
                         "7 n wussan")

    def test_punctuation_preserved(self):
        self.assertEqual(numbers_to_digits("(mraw) n yiwet.", "kab"),
                         "(10) n 1.")
        # Bot requested this case to prove boundary check is correct
        self.assertEqual(numbers_to_digits("(agim kuẓ imda) n idularen", "kab"),
                         "(1400) n idularen")

    def test_punctuation_boundary_comma(self):
        self.assertEqual(extract_number("mraw, sin", "kab"), 10)
        self.assertEqual(numbers_to_digits("mraw, sin", "kab"), "10, 2")

    def test_roundtrip_sweep(self):
        nums = list(range(0, 200)) + [222, 300, 345, 999, 1000, 1001,
                                      2000, 2500, 3333, 9999]
        for n in nums:
            spoken = pronounce_number(n, "kab")
            sentence = f"ɣur-i {spoken} n wussan."
            self.assertEqual(numbers_to_digits(sentence, "kab"),
                             f"ɣur-i {n} n wussan.", spoken)


if __name__ == "__main__":
    unittest.main()
