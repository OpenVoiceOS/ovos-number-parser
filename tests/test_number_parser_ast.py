import unittest

from ovos_number_parser.util import GrammaticalGender
from ovos_number_parser.numbers_ast import AST

# ============================================================
# Dictionaries
# ============================================================

class TestDictionaries(unittest.TestCase):

    def test_units_completeness(self):
        self.assertEqual(set(AST.vocab.UNITS.keys()), set(range(0, 10)))

    def test_tens_contains_expected(self):
        expected = list(range(10, 20)) + list(range(20, 100, 10))
        for i in expected:
            self.assertIn(i, set(AST.vocab.TENS.keys()))

    def test_composite_20s(self):
        # 21–29 must exist
        for i in range(21, 30):
            self.assertIn(i, AST.vocab.TENS)
        self.assertEqual(AST.vocab.TENS[21], "ventiún")

    def test_hundreds(self):
        self.assertEqual(set(AST.vocab.HUNDREDS.keys()), set(range(100, 1000, 100)))

    def test_fraction_strings(self):
        self.assertIn(2, AST.vocab.FRACTION)
        self.assertIn(10, AST.vocab.FRACTION)
        self.assertEqual(AST.vocab.FRACTION[2], "mediu")


# ============================================================
# Pronounce up to 999 (through AST.pronounce_number)
# ============================================================

class TestPronounceUpTo999_AST(unittest.TestCase):

    def test_zero(self):
        self.assertEqual(AST.pronounce_number(0), "cero")

    def test_units(self):
        self.assertEqual(AST.pronounce_number(1), "un")
        self.assertEqual(AST.pronounce_number(5), "cinco")

    def test_teens(self):
        self.assertEqual(AST.pronounce_number(16), "dieciséis")
        self.assertEqual(AST.pronounce_number(18), "dieciocho")

    def test_composite_20s(self):
        self.assertEqual(AST.pronounce_number(21), "ventiún")
        self.assertEqual(AST.pronounce_number(29), "ventinueve")

    def test_tens_and_units(self):
        self.assertEqual(AST.pronounce_number(35), "trenta y cinco")
        self.assertEqual(AST.pronounce_number(47), "cuarenta y siete")

    def test_hundreds_exact(self):
        self.assertEqual(AST.pronounce_number(100), "cien")
        self.assertEqual(AST.pronounce_number(500), "quinientos")

    def test_hundreds_with_remainder(self):
        self.assertEqual(AST.pronounce_number(101), "ciento un")
        self.assertEqual(AST.pronounce_number(234), "doscientos trenta y cuatro")


# ============================================================
# Fractions
# ============================================================

class TestFractionsAst(unittest.TestCase):

    def test_basic_fraction_words(self):
        self.assertAlmostEqual(AST.is_fractional("mediu"), 0.5)
        self.assertAlmostEqual(AST.is_fractional("terciu"), 1/3)

    def test_fraction_plurals(self):
        self.assertAlmostEqual(AST.is_fractional("medios"), 0.5)
        self.assertAlmostEqual(AST.is_fractional("cuartos"), 1/4)

    def test_fraction_pronounce(self):
        result = AST.pronounce_fraction("1/4")
        self.assertIn("un", result)
        self.assertIn("cuartu", result)
        result2 = AST.pronounce_fraction("3/4")
        self.assertIn("tres", result2)
        self.assertIn("cuartos", result2)


# ============================================================
# Extraction
# ============================================================

class TestExtractAST(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(AST.extract_number("dieciséis"), 16)
        self.assertEqual(AST.extract_number("ventiuno"), 21)

    def test_hundreds(self):
        self.assertEqual(AST.extract_number("ciento un"), 101)
        self.assertEqual(AST.extract_number("doscientos trenta y cuatro"), 234)

    def test_scale_thousand(self):
        self.assertEqual(AST.extract_number("mil"), 1000)
        self.assertEqual(AST.extract_number("mil doscientos trenta y cuatro"), 1234)

    def test_million(self):
        self.assertEqual(AST.extract_number("un millón"), 1_000_000)

    def test_million_plus(self):
        self.assertEqual(AST.extract_number("dos millones trescientos"), 2_000_300)

    def test_fraction_phrase(self):
        self.assertAlmostEqual(AST.extract_number("tres cuartos"), 0.75)

    def test_negative(self):
        self.assertEqual(AST.extract_number("menos cinco"), -5)

    def test_no_number(self):
        self.assertFalse(AST.extract_number("nada aquí"))
        self.assertFalse(AST.extract_number("palabres"))


# ============================================================
# Ordinals
# ============================================================

class TestOrdinalsAST(unittest.TestCase):

    def test_basic_ordinals(self):
        self.assertEqual(AST.pronounce_ordinal(1), "primeru")
        self.assertEqual(AST.pronounce_ordinal(1, gender=GrammaticalGender.FEMININE), "primera")

    def test_teens_ordinal(self):
        self.assertIn("décimu", AST.pronounce_ordinal(12))

    def test_tens_ordinal(self):
        self.assertEqual(AST.pronounce_ordinal(20), "ventenu")

    def test_composed_ordinal(self):
        self.assertEqual(AST.pronounce_ordinal(23), "ventenu terceru")

    def test_hundredth(self):
        self.assertEqual(AST.pronounce_ordinal(100), "centésimu")


# ============================================================
# Numbers to digits
# ============================================================

class TestNumbersToDigitsAST(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(AST.numbers_to_digits("dieciséis"), "16")
        self.assertEqual(AST.numbers_to_digits("ventiuno"), "21")

    def test_phrase(self):
        result = AST.numbers_to_digits("hai dos millones cincuenta persones")
        self.assertIn("2000050", result)

    def test_mixed(self):
        result = AST.numbers_to_digits("merquei ventiuno panes")
        self.assertEqual(result, "merquei 21 panes")

    def test_no_number(self):
        original = "nada equí"
        self.assertEqual(AST.numbers_to_digits(original), original)


# ============================================================
# Integration tests
# ============================================================

class TestIntegrationAST(unittest.TestCase):

    def test_round_trip(self):
        nums = [1, 16, 21, 35, 100, 234 , 1000, 1234]
        for n in nums:
            text = AST.pronounce_number(n)
            extracted = AST.extract_number(text)
            self.assertEqual(extracted, n)

    def test_large_numbers(self):
        text = AST.pronounce_number(1_234_567)
        extracted = AST.extract_number(text)
        self.assertEqual(extracted, 1_234_567)

    def test_decimals(self):
        res = AST.pronounce_number(1.234)
        self.assertIn("punto", res)
        self.assertIn("un", res)

    def test_negative(self):
        text = AST.pronounce_number(-234)
        self.assertTrue(text.startswith("menos"))
        self.assertEqual(AST.extract_number(text), -234)


# ============================================================
# Long-scale ladder (billón, trillón, ...)
# ============================================================

class TestLongScaleAST(unittest.TestCase):

    def test_billon(self):
        self.assertEqual(AST.pronounce_number(10 ** 12), "un billón")

    def test_trillon(self):
        self.assertEqual(AST.pronounce_number(10 ** 18), "un trillón")

    def test_thousand_millions(self):
        # long scale: 10^9 is "mil millones", not a distinct word
        self.assertEqual(AST.pronounce_number(10 ** 9), "mil millones")

    def test_long_scale_round_trip(self):
        for n in [10 ** 6, 10 ** 9, 10 ** 12, 5 * 10 ** 12,
                  10 ** 18, 3 * 10 ** 24, 10 ** 30, 10 ** 36]:
            text = AST.pronounce_number(n)
            self.assertEqual(AST.extract_number(text), n, text)


# ============================================================
# Round-trip sweep + boundaries
# ============================================================

class TestSweepAST(unittest.TestCase):

    def test_full_sweep_0_2000(self):
        for n in range(0, 2001):
            text = AST.pronounce_number(n)
            self.assertEqual(AST.extract_number(text), n, f"{n} -> {text}")

    def test_negatives(self):
        for n in [-1, -5, -234, -1000, -1_000_000]:
            text = AST.pronounce_number(n)
            self.assertTrue(text.startswith("menos"))
            self.assertEqual(AST.extract_number(text), n)

    def test_decimal_round_trip(self):
        for n in [0.5, 1.5, 2.75, 3.25, -1.5]:
            text = AST.pronounce_number(n)
            self.assertAlmostEqual(AST.extract_number(text), n)


# ============================================================
# Adversarial / malformed input
# ============================================================

class TestAdversarialAST(unittest.TestCase):

    def test_empty_string(self):
        self.assertFalse(AST.extract_number(""))

    def test_whitespace_only(self):
        self.assertFalse(AST.extract_number("   "))

    def test_numbers_to_digits_empty(self):
        self.assertEqual(AST.numbers_to_digits(""), "")

    def test_junk_around_number(self):
        self.assertEqual(AST.extract_number("xyz ventiuno qqq"), 21)

    def test_mixed_case(self):
        self.assertEqual(AST.extract_number("Dieciséis"), 16)
        self.assertEqual(AST.extract_number("VENTIUNO"), 21)

    def test_alt_spellings(self):
        self.assertEqual(AST.extract_number("unu"), 1)
        self.assertEqual(AST.extract_number("oito"), 8)


# ============================================================
# Gender agreement
# ============================================================

class TestGenderAST(unittest.TestCase):

    def test_feminine_one(self):
        self.assertEqual(
            AST.pronounce_number(1, gender=GrammaticalGender.FEMININE), "una")

    def test_feminine_ordinal(self):
        self.assertEqual(
            AST.pronounce_ordinal(1, gender=GrammaticalGender.FEMININE), "primera")


if __name__ == "__main__":
    unittest.main()
