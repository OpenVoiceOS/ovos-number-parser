import unittest

from ovos_number_parser import extract_number, numbers_to_digits, is_fractional

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
        self.assertAlmostEqual(is_fractional("mediu", "ast"), 0.5)
        self.assertAlmostEqual(is_fractional("terciu", "ast"), 1/3)

    def test_fraction_plurals(self):
        self.assertAlmostEqual(is_fractional("medios", "ast"), 0.5)
        self.assertAlmostEqual(is_fractional("cuartos", "ast"), 1/4)

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
        self.assertEqual(extract_number("dieciséis", lang="ast"), 16)
        self.assertEqual(extract_number("ventiuno", lang="ast"), 21)

    def test_hundreds(self):
        self.assertEqual(extract_number("ciento un", lang="ast"), 101)
        self.assertEqual(extract_number("doscientos trenta y cuatro", lang="ast"), 234)

    def test_scale_thousand(self):
        self.assertEqual(extract_number("mil", lang="ast"), 1000)
        self.assertEqual(extract_number("mil doscientos trenta y cuatro", lang="ast"), 1234)

    def test_million(self):
        self.assertEqual(extract_number("un millón", lang="ast"), 1_000_000)

    def test_million_plus(self):
        self.assertEqual(extract_number("dos millones trescientos", lang="ast"), 2_000_300)

    def test_fraction_phrase(self):
        self.assertAlmostEqual(extract_number("tres cuartos", lang="ast"), 0.75)

    def test_negative(self):
        self.assertEqual(extract_number("menos cinco", lang="ast"), -5)

    def test_no_number(self):
        self.assertFalse(extract_number("nada aquí", lang="ast"))
        self.assertFalse(extract_number("palabres", lang="ast"))


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
        self.assertEqual(numbers_to_digits("dieciséis", lang="ast"), "16")
        self.assertEqual(numbers_to_digits("ventiuno", lang="ast"), "21")

    def test_phrase(self):
        result = numbers_to_digits("hai dos millones cincuenta persones", lang="ast")
        self.assertIn("2000050", result)

    def test_mixed(self):
        result = numbers_to_digits("merquei ventiuno panes", lang="ast")
        self.assertEqual(result, "merquei 21 panes")

    def test_no_number(self):
        original = "nada equí"
        self.assertEqual(numbers_to_digits(original, lang="ast"), original)


# ============================================================
# Integration tests
# ============================================================

class TestIntegrationAST(unittest.TestCase):

    def test_round_trip(self):
        nums = [1, 16, 21, 35, 100, 234 , 1000, 1234]
        for n in nums:
            text = AST.pronounce_number(n)
            extracted = extract_number(text, lang="ast")
            self.assertEqual(extracted, n)

    def test_large_numbers(self):
        text = AST.pronounce_number(1_234_567)
        extracted = extract_number(text, lang="ast")
        self.assertEqual(extracted, 1_234_567)

    def test_decimals(self):
        res = AST.pronounce_number(1.234)
        self.assertIn("punto", res)
        self.assertIn("un", res)

    def test_negative(self):
        text = AST.pronounce_number(-234)
        self.assertTrue(text.startswith("menos"))
        self.assertEqual(extract_number(text, lang="ast"), -234)


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


# ============================================================
# Round-trip sweep + boundaries
# ============================================================

class TestSweepAST(unittest.TestCase):


    def test_negatives(self):
        for n in [-1, -5, -234, -1000, -1_000_000]:
            text = AST.pronounce_number(n)
            self.assertTrue(text.startswith("menos"))
            self.assertEqual(extract_number(text, lang="ast"), n)


# ============================================================
# Adversarial / malformed input
# ============================================================

class TestAdversarialAST(unittest.TestCase):

    def test_empty_string(self):
        self.assertFalse(extract_number("", lang="ast"))

    def test_whitespace_only(self):
        self.assertFalse(extract_number("   ", lang="ast"))

    def test_numbers_to_digits_empty(self):
        self.assertEqual(numbers_to_digits("", lang="ast"), "")

    def test_junk_around_number(self):
        self.assertEqual(extract_number("xyz ventiuno qqq", lang="ast"), 21)

    def test_mixed_case(self):
        self.assertEqual(extract_number("Dieciséis", lang="ast"), 16)
        self.assertEqual(extract_number("VENTIUNO", lang="ast"), 21)

    def test_alt_spellings(self):
        self.assertEqual(extract_number("unu", lang="ast"), 1)
        self.assertEqual(extract_number("oito", lang="ast"), 8)


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
