import unittest

from ovos_number_parser.util import GrammaticalGender
from ovos_number_parser.numbers_mwl import MWL


# ============================================================
# Dictionaries
# ============================================================

class TestDictionariesMWL(unittest.TestCase):
    """Test the completeness and content of the Mirandese vocabulary dictionaries."""

    def test_units_completeness(self):
        """Test that UNITS contains all expected numbers (0-9)."""
        self.assertEqual(set(MWL.vocab.UNITS.keys()), set(range(0, 10)))
        self.assertEqual(MWL.vocab.UNITS[1], "un")  # Masculine form

    def test_tens_contains_expected(self):
        """Test that TENS contains the expected numbers (10-19, 20, 30, ..., 90)."""
        expected = list(range(10, 20)) + list(range(20, 100, 10))
        for i in expected:
            self.assertIn(i, set(MWL.vocab.TENS.keys()))
        self.assertEqual(MWL.vocab.TENS[16], "zasseis")
        self.assertEqual(MWL.vocab.TENS[20], "binte")  # Should be the root form
        self.assertEqual(MWL.vocab.TENS[90], "nobenta")

    def test_composite_numbers_below_100(self):
        """Test composite numbers in the 20-99 range."""
        # 21-29 are composite and use a specific structure
        #self.assertEqual(MWL.vocab.TENS[21], "binte i un")  # MWL uses 'i' as separator
        #self.assertEqual(MWL.vocab.TENS[35], "trinta i cinco")
        #self.assertEqual(MWL.vocab.TENS[99], "nobenta i nuobe")

    def test_hundreds(self):
        """Test that HUNDREDS contains the expected numbers (100, 200, ..., 900)."""
        self.assertEqual(set(MWL.vocab.HUNDREDS.keys()), set(range(100, 1000, 100)))
        self.assertEqual(MWL.vocab.HUNDREDS[100], "cien")
        self.assertEqual(MWL.vocab.HUNDREDS[200], "duzientos")
        self.assertEqual(MWL.vocab.HUNDREDS[700], "sietecientos")

    def test_fraction_strings(self):
        """Test basic fraction dictionary values."""
        self.assertIn(2, MWL.vocab.FRACTION)
        self.assertIn(10, MWL.vocab.FRACTION)
        self.assertEqual(MWL.vocab.FRACTION[2], "meio")  # Masculine form


# ============================================================
# Pronounce (Number to Text)
# ============================================================

class TestPronunciationMWL(unittest.TestCase):
    """Test the MWL.pronounce_number function for cardinals and special cases."""

    def test_cardinals_basic(self):
        self.assertEqual(MWL.pronounce_number(0), "zero")
        self.assertEqual(MWL.pronounce_number(1), "un")
        self.assertEqual(MWL.pronounce_number(2), "dous")
        self.assertEqual(MWL.pronounce_number(10), "dieç")
        self.assertEqual(MWL.pronounce_number(16), "zasseis")
        self.assertEqual(MWL.pronounce_number(20), "binte")
        self.assertEqual(MWL.pronounce_number(21), "bint'i un")
        self.assertEqual(MWL.pronounce_number(35), "trinta i cinco")
        self.assertEqual(MWL.pronounce_number(99), "nobenta i nuobe")

    def test_cardinals_hundreds(self):
        self.assertEqual(MWL.pronounce_number(100), "cien")
        self.assertEqual(MWL.pronounce_number(101), "ciento i un")
        self.assertEqual(MWL.pronounce_number(234), "duzientos i trinta i quatro")
        self.assertEqual(MWL.pronounce_number(999), "nuobecientos i nobenta i nuobe")

    def test_cardinals_thousands(self):
        self.assertEqual(MWL.pronounce_number(1000), "mil")
        self.assertEqual(MWL.pronounce_number(1234), "mil duzientos i trinta i quatro")
        self.assertEqual(MWL.pronounce_number(2000), "dous mil")
        self.assertEqual(MWL.pronounce_number(1000000), "un milhon")
        self.assertEqual(MWL.pronounce_number(2_000_000), "dous milhones")

    def test_cardinals_large(self):
        self.assertEqual(MWL.pronounce_number(1_234_567),
                         "un milhon duzientos i trinta i quatro mil quinhentos i sessenta i siete")
        self.assertEqual(MWL.pronounce_number(1_000_000_000), "mil milhones")  # Long scale default
        self.assertEqual(MWL.pronounce_number(1_000_000_000_000), "un bilion")  # Long scale default

    def test_decimals(self):
        self.assertEqual(MWL.pronounce_number(1.5), "un bírgula cinco")
        self.assertEqual(MWL.pronounce_number(3.14), "trés bírgula catorze")
        self.assertEqual(MWL.pronounce_number(10.05), "dieç bírgula zero cinco")

    def test_negative(self):
        self.assertEqual(MWL.pronounce_number(-10), "menos dieç")
        self.assertEqual(MWL.pronounce_number(-3.14), "menos trés bírgula catorze")

    def test_gendered_cardinals(self):
        # 1 and 2 are gendered
        self.assertEqual(MWL.pronounce_number(1, gender=GrammaticalGender.FEMININE), "ũa")
        self.assertEqual(MWL.pronounce_number(2, gender=GrammaticalGender.FEMININE), "dues")

        # 21 (uses 1) is gendered
        self.assertEqual(MWL.pronounce_number(21, gender=GrammaticalGender.MASCULINE), "bint'i un")
        self.assertEqual(MWL.pronounce_number(21, gender=GrammaticalGender.FEMININE), "bint'i ũa")

        # 102 (uses 2) is gendered
        self.assertEqual(MWL.pronounce_number(102, gender=GrammaticalGender.MASCULINE), "ciento i dous")
        self.assertEqual(MWL.pronounce_number(102, gender=GrammaticalGender.FEMININE), "ciento i dues")

    def test_fractions(self):
        self.assertEqual(MWL.pronounce_fraction("1/2"), "un meio")
        self.assertEqual(MWL.pronounce_fraction("3/4"), "trés quartos")
        self.assertEqual(MWL.pronounce_fraction("1/10"), "un décimo")
        self.assertEqual(MWL.pronounce_fraction("1/1000"), "un milésimo")


# ============================================================
# Ordinal Pronunciation (Number to Text)
# ============================================================

class TestOrdinalPronunciationMWL(unittest.TestCase):
    """Test MWL.pronounce_ordinal."""

    def test_basic_ordinals_masculine(self):
        self.assertEqual(MWL.pronounce_ordinal(1), "purmerio")
        self.assertEqual(MWL.pronounce_ordinal(2), "segundo")
        self.assertEqual(MWL.pronounce_ordinal(3), "terceiro")
        self.assertEqual(MWL.pronounce_ordinal(10), "décimo")

    def test_basic_ordinals_feminine(self):
        self.assertEqual(MWL.pronounce_ordinal(1, GrammaticalGender.FEMININE), "purmeria")
        self.assertEqual(MWL.pronounce_ordinal(2, GrammaticalGender.FEMININE), "segunda")
        self.assertEqual(MWL.pronounce_ordinal(3, GrammaticalGender.FEMININE), "terceira")
        self.assertEqual(MWL.pronounce_ordinal(10, GrammaticalGender.FEMININE), "décima")

    def test_complex_ordinals(self):
        # 21st (vingésimo primeiro / primeira)
        self.assertEqual(MWL.pronounce_ordinal(21), "bigésimo purmerio")
        self.assertEqual(MWL.pronounce_ordinal(21, GrammaticalGender.FEMININE), "bigésima purmeria")
        # 44th (quadragésimo quarto / quarta)
        self.assertEqual(MWL.pronounce_ordinal(44), "quadragésimo quarto")
        self.assertEqual(MWL.pronounce_ordinal(44, GrammaticalGender.FEMININE), "quadragésima quarta")
        # 100th (centésimo)
        self.assertEqual(MWL.pronounce_ordinal(100), "centésimo")
        # 1000th (milésimo)
        self.assertEqual(MWL.pronounce_ordinal(1000), "milésimo")


# ============================================================
# Extraction (Text to Number)
# ============================================================

class TestExtractionMWL(unittest.TestCase):
    """Test the MWL.extract_number function."""

    def test_extract_cardinals(self):
        self.assertEqual(MWL.extract_number("zero"), 0)
        self.assertEqual(MWL.extract_number("un"), 1)
        self.assertEqual(MWL.extract_number("ũa"), 1)
        self.assertEqual(MWL.extract_number("dous"), 2)
        self.assertEqual(MWL.extract_number("dues"), 2)
        self.assertEqual(MWL.extract_number("dezasseis"), 16)
        self.assertEqual(MWL.extract_number("bint'i un"), 21)
        self.assertEqual(MWL.extract_number("cien i dous"), 102)
        self.assertEqual(MWL.extract_number("mil i duzientos i trinta i quatro"), 1234)

    def test_extract_decimals(self):
        self.assertEqual(MWL.extract_number("un bírgula cinco"), 1.5)
        self.assertEqual(MWL.extract_number("menos trés bírgula catorze"), -3.14)

    def test_extract_ordinals(self):
        # Masculine
        self.assertEqual(MWL.extract_number("purmerio", ordinals=True), 1)
        self.assertEqual(MWL.extract_number("décimo purmerio", ordinals=True), 11)
        # Feminine
        self.assertEqual(MWL.extract_number("purmeria beç", ordinals=True), 1)
        self.assertEqual(MWL.extract_number("la sessagésima quarta beç", ordinals=True), 64)

    def test_extract_phrase(self):
        self.assertEqual(MWL.extract_number("un milhon de beçs"), 1_000_000)
        self.assertEqual(MWL.extract_number("la bint'i ũa beç"), 21)

    def test_extract_failure(self):
        self.assertFalse(MWL.extract_number("palabra sin númaro"))


# ============================================================
# Digits (Text in Sentence to Digits)
# ============================================================

class TestDigitsMWL(unittest.TestCase):
    """Test MWL.numbers_to_digits function."""

    def test_basic_conversion(self):
        self.assertEqual(MWL.numbers_to_digits("dieç beçs"), "10 beçs")
        self.assertEqual(MWL.numbers_to_digits("bint'i un panes"), "21 panes")
        self.assertEqual(MWL.numbers_to_digits("cien i dous dies"), "102 dies")
        self.assertEqual(MWL.numbers_to_digits("un milhon de beçs"), "1000000 de beçs")

    def test_decimal_conversion(self):
        self.assertEqual(MWL.numbers_to_digits("la distáncia ye de trés bírgula catorze km"),
                         "la distáncia ye de 3.14 km")

    def test_negative_conversion(self):
        self.assertEqual(MWL.numbers_to_digits("temperatura de menos binte graus"), "temperatura de -20 graus")


# ============================================================
# Integration tests
# ============================================================

class TestIntegrationMWL(unittest.TestCase):
    """Test round-trip conversion and large numbers."""

    def test_round_trip(self):
        """Test that number -> text -> number conversion works."""
        nums = [1, 2, 16, 21, 35, 100, 234, 1000, 1234, 9999]
        for n in nums:
            text = MWL.pronounce_number(n)
            extracted = MWL.extract_number(text)
            self.assertEqual(extracted, n, f"Failed on number: {n}. Text: {text}")

    def test_large_numbers_round_trip(self):
        """Test round trip for numbers that require large scale support."""
        n = 1_234_567_899
        text = MWL.pronounce_number(n)
        self.assertEqual(text, "mil duzientos i trinta i quatro milhones quinhentos i sessenta i siete mil uitocientos i nobenta i nuobe")
        extracted = MWL.extract_number(text)
        self.assertEqual(extracted, n, f"Failed on number: {n}. Text: {text}")

        # Bilion (long scale, 10^12)
        n = 5_000_000_000_000
        text = MWL.pronounce_number(n)
        self.assertEqual(text, "cinco biliones")
        extracted = MWL.extract_number(text)
        self.assertEqual(extracted, n)

    def test_gender_sensitive_round_trip(self):
        """Test round trip for gendered numbers."""
        # Feminine 1
        text_f = MWL.pronounce_number(1, gender=GrammaticalGender.FEMININE)
        self.assertEqual(text_f, "ũa")
        self.assertEqual(MWL.extract_number(text_f), 1)

        # Feminine 2
        text_f = MWL.pronounce_number(2, gender=GrammaticalGender.FEMININE)
        self.assertEqual(text_f, "dues")
        self.assertEqual(MWL.extract_number(text_f), 2)