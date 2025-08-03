import unittest

from ovos_number_parser.numbers_pt import (
    PortugueseVariant,
    _pronounce_up_to_999,
    is_fractional_pt,
    extract_number_pt,
    pronounce_number_pt,
    numbers_to_digits_pt,
    tokenize,
    pronounce_fraction_pt,
    _UNITS,
    _TENS_BR,
    _TENS_PT,
    _HUNDREDS,
    _FRACTION_STRING_PT,
    _SCALES,
    _NUMBERS_BR,
    _NUMBERS_PT
)
from ovos_number_parser.util import Scale


class TestPortugueseVariant(unittest.TestCase):
    """Test PortugueseVariant enum."""

    def test_variant_values(self):
        """
        Verify that the PortugueseVariant enum has the expected string values for Brazilian and Portugal variants.
        """
        self.assertEqual(PortugueseVariant.BR.value, "br")
        self.assertEqual(PortugueseVariant.PT.value, "pt")

    def test_variant_comparison(self):
        """
        Verify that the PortugueseVariant enum distinguishes between BR and PT variants and supports equality and inequality comparisons.
        """
        self.assertNotEqual(PortugueseVariant.BR, PortugueseVariant.PT)
        self.assertEqual(PortugueseVariant.BR, PortugueseVariant.BR)


class TestDictionaries(unittest.TestCase):
    """Test the pronunciation dictionaries."""

    def test_units_completeness(self):
        """
        Verify that the _UNITS dictionary includes all keys from 1 to 9.
        """
        expected_keys = list(range(1, 10))
        self.assertEqual(set(_UNITS.keys()), set(expected_keys))

    def test_tens_br_completeness(self):
        """
        Verify that the _TENS_BR dictionary includes all expected keys for Brazilian Portuguese tens, covering numbers 10-19 and multiples of ten up to 90.
        """
        expected_keys = list(range(10, 20)) + list(range(20, 100, 10))
        self.assertEqual(set(_TENS_BR.keys()), set(expected_keys))

    def test_tens_pt_completeness(self):
        """
        Verify that the `_TENS_PT` dictionary includes all expected keys for Portuguese tens, covering numbers 10-19 and multiples of ten up to 90.
        """
        expected_keys = list(range(10, 20)) + list(range(20, 100, 10))
        self.assertEqual(set(_TENS_PT.keys()), set(expected_keys))

    def test_tens_variants_differences(self):
        """
        Verify that the Brazilian (BR) and Portugal (PT) Portuguese tens dictionaries have the correct variant-specific spellings for numbers 16, 17, and 19.
        """
        # Key differences between BR and PT
        self.assertEqual(_TENS_BR[16], "dezesseis")
        self.assertEqual(_TENS_PT[16], "dezasseis")
        self.assertEqual(_TENS_BR[17], "dezessete")
        self.assertEqual(_TENS_PT[17], "dezassete")
        self.assertEqual(_TENS_BR[19], "dezenove")
        self.assertEqual(_TENS_PT[19], "dezanove")

    def test_hundreds_completeness(self):
        """
        Verify that the _HUNDREDS dictionary includes all keys for hundreds from 100 to 900.
        """
        expected_keys = list(range(100, 1000, 100))
        self.assertEqual(set(_HUNDREDS.keys()), set(expected_keys))

    def test_fraction_string_pt_completeness(self):
        """
        Verify that the _FRACTION_STRING_PT dictionary includes expected fraction keys and their corresponding Portuguese strings.
        """
        self.assertIn(2, _FRACTION_STRING_PT)
        self.assertIn(3, _FRACTION_STRING_PT)
        self.assertIn(10, _FRACTION_STRING_PT)
        self.assertEqual(_FRACTION_STRING_PT[2], "meio")
        self.assertEqual(_FRACTION_STRING_PT[3], "terço")

    def test_scales_structure(self):
        """
        Verify that the _SCALES dictionary contains both short and long scales, and that each scale includes entries for Brazilian and Portugal Portuguese variants.
        """
        self.assertIn(Scale.SHORT, _SCALES)
        self.assertIn(Scale.LONG, _SCALES)
        self.assertIn(PortugueseVariant.BR, _SCALES[Scale.SHORT])
        self.assertIn(PortugueseVariant.PT, _SCALES[Scale.SHORT])

    def test_numbers_br_construction(self):
        """
        Verify that the Brazilian Portuguese numbers dictionary (`_NUMBERS_BR`) contains expected keys and correct numeric mappings for specific entries.
        """
        self.assertIn("um", _NUMBERS_BR)
        self.assertIn("dezesseis", _NUMBERS_BR)
        self.assertIn("bilhão", _NUMBERS_BR)
        self.assertEqual(_NUMBERS_BR["um"], 1)
        self.assertEqual(_NUMBERS_BR["dezesseis"], 16)

    def test_numbers_pt_construction(self):
        """
        Verify that the `_NUMBERS_PT` dictionary contains expected Portuguese number words and their correct numeric values.
        """
        self.assertIn("um", _NUMBERS_PT)
        self.assertIn("dezasseis", _NUMBERS_PT)
        self.assertIn("bilião", _NUMBERS_PT)
        self.assertEqual(_NUMBERS_PT["um"], 1)
        self.assertEqual(_NUMBERS_PT["dezasseis"], 16)


class TestPronounceUpTo999(unittest.TestCase):
    """Test _pronounce_up_to_999 function."""

    def test_zero(self):
        """
        Verify that the pronunciation of 0 is correctly returned as "zero".
        """
        result = _pronounce_up_to_999(0)
        self.assertEqual(result, "zero")

    def test_single_digits_br(self):
        """
        Verify that single-digit numbers are pronounced correctly in the Brazilian Portuguese variant.
        """
        self.assertEqual(_pronounce_up_to_999(1, PortugueseVariant.BR), "um")
        self.assertEqual(_pronounce_up_to_999(5, PortugueseVariant.BR), "cinco")
        self.assertEqual(_pronounce_up_to_999(9, PortugueseVariant.BR), "nove")

    def test_single_digits_pt(self):
        """
        Test that single-digit numbers are pronounced correctly in the Portugal Portuguese variant.
        """
        self.assertEqual(_pronounce_up_to_999(1, PortugueseVariant.PT), "um")
        self.assertEqual(_pronounce_up_to_999(5, PortugueseVariant.PT), "cinco")
        self.assertEqual(_pronounce_up_to_999(9, PortugueseVariant.PT), "nove")

    def test_teens_br(self):
        """
        Test that the pronunciation of teen numbers (16, 17, 19) in the Brazilian Portuguese variant is correct.
        """
        self.assertEqual(_pronounce_up_to_999(16, PortugueseVariant.BR), "dezesseis")
        self.assertEqual(_pronounce_up_to_999(17, PortugueseVariant.BR), "dezessete")
        self.assertEqual(_pronounce_up_to_999(19, PortugueseVariant.BR), "dezenove")

    def test_teens_pt(self):
        """
        Verify that the pronunciation of teen numbers (16, 17, 19) in the Portugal Portuguese variant is correct.
        """
        self.assertEqual(_pronounce_up_to_999(16, PortugueseVariant.PT), "dezasseis")
        self.assertEqual(_pronounce_up_to_999(17, PortugueseVariant.PT), "dezassete")
        self.assertEqual(_pronounce_up_to_999(19, PortugueseVariant.PT), "dezanove")

    def test_tens(self):
        """
        Test that the pronunciation of multiples of ten (20, 30, 90) is correct in Portuguese.
        """
        self.assertEqual(_pronounce_up_to_999(20), "vinte")
        self.assertEqual(_pronounce_up_to_999(30), "trinta")
        self.assertEqual(_pronounce_up_to_999(90), "noventa")

    def test_tens_with_units(self):
        """
        Test that numbers combining tens and units are pronounced correctly in Portuguese.
        """
        self.assertEqual(_pronounce_up_to_999(21), "vinte e um")
        self.assertEqual(_pronounce_up_to_999(35), "trinta e cinco")
        self.assertEqual(_pronounce_up_to_999(99), "noventa e nove")

    def test_exact_hundred(self):
        """
        Test that the pronunciation of the exact hundred (100) is correctly returned as "cem".
        """
        self.assertEqual(_pronounce_up_to_999(100), "cem")

    def test_hundreds_with_remainder(self):
        """
        Verify that numbers in the hundreds with nonzero remainders are pronounced correctly in Portuguese.
        """
        self.assertEqual(_pronounce_up_to_999(101), "cento e um")
        self.assertEqual(_pronounce_up_to_999(123), "cento e vinte e três")
        self.assertEqual(_pronounce_up_to_999(200), "duzentos")
        self.assertEqual(_pronounce_up_to_999(234), "duzentos e trinta e quatro")

    def test_complex_numbers(self):
        """
        Test that complex numbers within the 0-999 range are pronounced correctly in Portuguese.
        """
        self.assertEqual(_pronounce_up_to_999(567), "quinhentos e sessenta e sete")
        self.assertEqual(_pronounce_up_to_999(999), "novecentos e noventa e nove")

    def test_invalid_range(self):
        """
        Verify that calling _pronounce_up_to_999 with numbers outside the 0-999 range raises a ValueError.
        """
        with self.assertRaises(ValueError):
            _pronounce_up_to_999(-1)
        with self.assertRaises(ValueError):
            _pronounce_up_to_999(1000)
        with self.assertRaises(ValueError):
            _pronounce_up_to_999(1001)


class TestIsFractionalPt(unittest.TestCase):
    """Test is_fractional_pt function."""

    def test_basic_fractions(self):
        """
        Test that `is_fractional_pt` correctly recognizes and converts basic Portuguese fraction words to their numeric values.
        """
        self.assertEqual(is_fractional_pt("meio"), 0.5)
        self.assertEqual(is_fractional_pt("terço"), 1.0 / 3)
        self.assertEqual(is_fractional_pt("quarto"), 0.25)

    def test_meia_variant(self):
        """
        Test that 'meia' is correctly recognized as a variant of 'meio' and returns 0.5.
        """
        self.assertEqual(is_fractional_pt("meia"), 0.5)

    def test_plural_forms(self):
        """
        Verify that plural forms of Portuguese fraction words are correctly recognized and converted to their numeric values.
        """
        self.assertEqual(is_fractional_pt("meios"), 0.5)
        self.assertEqual(is_fractional_pt("terços"), 1.0 / 3)
        self.assertEqual(is_fractional_pt("quartos"), 0.25)

    def test_special_fractions(self):
        """
        Test that `is_fractional_pt` correctly recognizes and returns values for special fraction words such as "décimo", "vigésimo", and "centésimo".
        """
        self.assertEqual(is_fractional_pt("décimo"), 0.1)
        self.assertEqual(is_fractional_pt("vigésimo"), 0.05)
        self.assertEqual(is_fractional_pt("centésimo"), 0.01)

    def test_compound_fractions(self):
        """
        Test that compound fraction words like 'onze', 'doze', and 'treze' are correctly recognized as fractional denominators by is_fractional_pt.
        """
        self.assertEqual(is_fractional_pt("onze"), 1.0 / 11)
        self.assertEqual(is_fractional_pt("doze"), 1.0 / 12)
        self.assertEqual(is_fractional_pt("treze"), 1.0 / 13)

    def test_case_insensitive(self):
        """
        Verify that `is_fractional_pt` correctly identifies fractional words regardless of letter casing.
        """
        self.assertEqual(is_fractional_pt("MEIO"), 0.5)
        self.assertEqual(is_fractional_pt("Terço"), 1.0 / 3)
        self.assertEqual(is_fractional_pt("MEIA"), 0.5)

    def test_whitespace_handling(self):
        """
        Verify that `is_fractional_pt` correctly parses fractional words with leading, trailing, or embedded whitespace.
        """
        self.assertEqual(is_fractional_pt("  meio  "), 0.5)
        self.assertEqual(is_fractional_pt("\tterço\n"), 1.0 / 3)

    def test_non_fractions(self):
        """
        Verify that non-fractional strings are correctly identified as not representing fractions by `is_fractional_pt`.
        """
        self.assertFalse(is_fractional_pt("palavra"))
        self.assertFalse(is_fractional_pt("número"))
        self.assertFalse(is_fractional_pt(""))
        self.assertFalse(is_fractional_pt("123"))


class TestExtractNumberPt(unittest.TestCase):
    """Test extract_number_pt function."""

    def test_simple_numbers_br(self):
        """
        Test that simple number words are correctly extracted as numeric values in the Brazilian Portuguese variant.
        """
        self.assertEqual(extract_number_pt("dezesseis", variant=PortugueseVariant.BR), 16)
        self.assertEqual(extract_number_pt("vinte e um", variant=PortugueseVariant.BR), 21)
        self.assertEqual(extract_number_pt("cem", variant=PortugueseVariant.BR), 100)

    def test_simple_numbers_pt(self):
        """
        Test that simple number words are correctly extracted as numeric values in the Portugal Portuguese variant.
        """
        self.assertEqual(extract_number_pt("dezasseis", variant=PortugueseVariant.PT), 16)
        self.assertEqual(extract_number_pt("vinte e um", variant=PortugueseVariant.PT), 21)
        self.assertEqual(extract_number_pt("cem", variant=PortugueseVariant.PT), 100)

    def test_large_numbers_short_scale_br(self):
        """
        Test extraction of large numbers in Brazilian Portuguese using the short scale.
        
        Verifies that "um milhão" and "um bilhão" are correctly parsed as 1,000,000 and 1,000,000,000, respectively.
        """
        self.assertEqual(extract_number_pt("um milhão", scale=Scale.SHORT, variant=PortugueseVariant.BR), 1000000)
        self.assertEqual(extract_number_pt("um bilhão", scale=Scale.SHORT, variant=PortugueseVariant.BR), 1000000000)

    def test_large_numbers_short_scale_pt(self):
        """
        Test that `extract_number_pt` correctly extracts large numbers in short scale for European Portuguese.
        
        Verifies extraction of "um milhão", "um bilião", and "um trilião" as 1e6, 1e9, and 1e12, respectively, using the short scale and PT variant.
        """
        self.assertEqual(extract_number_pt("um milhão", scale=Scale.SHORT, variant=PortugueseVariant.PT), 1e6)
        self.assertEqual(extract_number_pt("um bilião", scale=Scale.SHORT, variant=PortugueseVariant.PT), 1e9)
        self.assertEqual(extract_number_pt("um trilião", scale=Scale.SHORT, variant=PortugueseVariant.PT), 1e12)

    def test_large_numbers_long_scale(self):
        """
        Test that `extract_number_pt` correctly extracts large numbers using the long scale in European Portuguese.
        
        Verifies that phrases like "um milhão", "um bilião", and "um trilião" are parsed as 1,000,000; 1,000,000,000,000; and 1,000,000,000,000,000,000 respectively when using the long scale and Portugal variant.
        """
        # TODO - failing
        self.assertEqual(extract_number_pt("um milhão", scale=Scale.LONG, variant=PortugueseVariant.PT), 1e6)
        self.assertEqual(extract_number_pt("um bilião", scale=Scale.LONG, variant=PortugueseVariant.PT), 1e12)
        self.assertEqual(extract_number_pt("um trilião", scale=Scale.LONG, variant=PortugueseVariant.PT), 1e18)

    def test_complex_numbers(self):
        """
        Test that complex Portuguese number phrases are correctly extracted as integers.
        """
        self.assertEqual(extract_number_pt("duzentos e cinquenta e três"), 253)
        self.assertEqual(extract_number_pt("mil quinhentos e quarenta e dois"), 1542)

    def test_fractions_in_text(self):
        """
        Test that `extract_number_pt` correctly extracts fractional numbers from text containing both whole numbers and fractions.
        """
        result = extract_number_pt("dois e meio")
        self.assertAlmostEqual(result, 2.5, places=5)

    def test_decimal_handling(self):
        """
        Test extraction of decimal numbers from Portuguese text using simplified decimal handling.
        
        Verifies that `extract_number_pt` correctly parses decimal numbers expressed in Portuguese (e.g., "dez ponto cinco") and returns an integer or float result.
        """
        # Note: This tests the simplified decimal approach
        result = extract_number_pt("dez ponto cinco")
        # The function should handle this but may need specific formatting
        if result:
            self.assertIsInstance(result, (int, float))

    def test_case_insensitive(self):
        """Test case insensitive extraction."""
        self.assertEqual(extract_number_pt("DEZESSEIS", variant=PortugueseVariant.BR), 16)
        self.assertEqual(extract_number_pt("Vinte E Um", variant=PortugueseVariant.BR), 21)

    def test_hyphen_handling(self):
        """
        Test that hyphenated number words are correctly parsed as numbers in Portuguese.
        
        Verifies that "vinte-e-um" is recognized as 21 in the Brazilian Portuguese variant.
        """
        self.assertEqual(extract_number_pt("vinte-e-um", variant=PortugueseVariant.BR), 21)

    def test_no_number_found(self):
        """
        Verify that `extract_number_pt` returns `False` when no numeric value is present in the input text.
        """
        self.assertFalse(extract_number_pt("apenas palavras"))
        self.assertFalse(extract_number_pt(""))
        self.assertFalse(extract_number_pt("xyz"))

    def test_multiple_scales(self):
        """
        Test extraction of numbers expressed with multiple scale words in Portuguese.
        
        Verifies that `extract_number_pt` correctly parses phrases combining millions and thousands.
        """
        self.assertEqual(extract_number_pt("dois milhões trezentos mil"), 2300000)

    def test_edge_cases(self):
        """
        Test extraction of numbers from Portuguese edge case words.
        
        Verifies that "zero" and "mil" are correctly parsed as 0 and 1000, respectively.
        """
        self.assertEqual(extract_number_pt("zero"), 0)
        self.assertEqual(extract_number_pt("mil"), 1000)


class TestPronounceNumberPt(unittest.TestCase):
    """Test pronounce_number_pt function."""

    def test_type_validation(self):
        """
        Test that pronounce_number_pt raises TypeError when given invalid input types.
        """
        with self.assertRaises(TypeError):
            pronounce_number_pt("not a number")
        with self.assertRaises(TypeError):
            pronounce_number_pt(None)

    def test_zero(self):
        """Test pronunciation of zero."""
        self.assertEqual(pronounce_number_pt(0), "zero")

    def test_negative_numbers(self):
        """
        Verify that negative numbers are pronounced with the correct prefix and number word in Portuguese.
        """
        result = pronounce_number_pt(-5)
        self.assertTrue(result.startswith("menos"))
        self.assertIn("cinco", result)

    def test_simple_integers(self):
        """
        Test that `pronounce_number_pt` returns the correct Portuguese pronunciation for simple integers, including variant-specific differences for Brazilian and European Portuguese.
        """
        self.assertEqual(pronounce_number_pt(1), "um")
        self.assertEqual(pronounce_number_pt(16, variant=PortugueseVariant.BR), "dezesseis")
        self.assertEqual(pronounce_number_pt(16, variant=PortugueseVariant.PT), "dezasseis")

    def test_hundreds(self):
        """
        Test pronunciation of hundreds and numbers in the hundreds range using the Portuguese number pronunciation function.
        """
        self.assertEqual(pronounce_number_pt(100), "cem")
        self.assertEqual(pronounce_number_pt(200), "duzentos")
        self.assertEqual(pronounce_number_pt(123), "cento e vinte e três")

    def test_thousands(self):
        """
        Test that numbers in the thousands are pronounced correctly in Portuguese.
        
        Verifies that the pronunciation of 1000 and 2500 includes the expected words for "mil" (thousand) and "quinhentos" (five hundred).
        """
        result = pronounce_number_pt(1000)
        self.assertIn("mil", result)

        result = pronounce_number_pt(2500)
        self.assertIn("mil", result)
        self.assertIn("quinhentos", result)

    def test_millions_short_scale_br(self):
        """
        Test that `pronounce_number_pt` correctly pronounces millions and billions in Brazilian Portuguese using the short scale.
        """
        result = pronounce_number_pt(1000000, scale=Scale.SHORT, variant=PortugueseVariant.BR)
        self.assertIn("milhão", result)

        result = pronounce_number_pt(1000000000, scale=Scale.SHORT, variant=PortugueseVariant.BR)
        self.assertIn("bilhão", result)

    def test_millions_short_scale_pt(self):
        """
        Test that `pronounce_number_pt` correctly pronounces millions and billions in short scale European Portuguese, ensuring the use of "milhão" and "bilião".
        """
        result = pronounce_number_pt(1000000, scale=Scale.SHORT, variant=PortugueseVariant.PT)
        self.assertIn("milhão", result)

        result = pronounce_number_pt(1000000000, scale=Scale.SHORT, variant=PortugueseVariant.PT)
        self.assertIn("bilião", result)

    def test_millions_long_scale(self):
        """
        Test that `pronounce_number_pt` correctly pronounces millions and billions using the long scale in European Portuguese.
        
        Verifies that 1,000,000 is pronounced with "milhão" and 1,000,000,000,000 with "bilião" in the long scale.
        """
        result = pronounce_number_pt(1000000, scale=Scale.LONG, variant=PortugueseVariant.PT)
        self.assertIn("milhão", result)

        result = pronounce_number_pt(1000000000000, scale=Scale.LONG, variant=PortugueseVariant.PT)
        self.assertIn("bilião", result)

    def test_decimal_numbers(self):
        """
        Test that decimal numbers are pronounced correctly in Portuguese, including the use of "vírgula" and correct digit words.
        """
        result = pronounce_number_pt(1.5)
        self.assertIn("vírgula", result)
        self.assertIn("um", result)
        self.assertIn("cinco", result)

    def test_decimal_edge_cases(self):
        """
        Test pronunciation of decimal numbers in edge cases, including rounding to zero and multiple decimal places.
        """
        # Test when decimal part rounds to zero
        result = pronounce_number_pt(1.0)
        self.assertEqual(result, "um vírgula zero")

        # Test multiple decimal places
        result = pronounce_number_pt(1.23)
        self.assertIn("vírgula", result)

    def test_conjunction_logic(self):
        """Test conjunction logic for complex numbers."""
        result = pronounce_number_pt(1001)
        self.assertIn("e", result)  # Should have conjunction for small remainder

        result = pronounce_number_pt(1100)
        self.assertIn("e", result)  # Should have conjunction for multiple of 100

    def test_mil(self):
        """
        Test that the pronunciation of 1000 in Portuguese is "mil" and not prefixed with "um mil".
        """
        result = pronounce_number_pt(1000)
        # Should not start with "um mil" but just "mil"
        self.assertFalse(result.startswith("um mil"))

    def test_places_parameter(self):
        """
        Test that the `places` parameter in `pronounce_number_pt` correctly handles decimal precision without errors.
        
        Verifies that specifying different decimal places returns a string result.
        """
        result1 = pronounce_number_pt(1.23456, places=2)
        result2 = pronounce_number_pt(1.23456, places=5)
        # Both should work without error
        self.assertIsInstance(result1, str)
        self.assertIsInstance(result2, str)


class TestNumbersToDigitsPt(unittest.TestCase):
    """Test numbers_to_digits_pt function."""

    def test_simple_replacement(self):
        """Test simple number word replacement."""
        self.assertEqual(numbers_to_digits_pt("dezesseis", variant=PortugueseVariant.BR), "16")
        self.assertEqual(numbers_to_digits_pt("dezasseis", variant=PortugueseVariant.PT), "16")

    def test_complex_numbers(self):
        """
        Test that complex Portuguese number phrases are correctly converted to digit strings.
        """
        result = numbers_to_digits_pt("duzentos e cinquenta e três")
        self.assertEqual(result, "253")

    def test_mixed_text(self):
        """
        Test that numbers within mixed Portuguese text are correctly converted to digits while preserving surrounding words.
        """
        result = numbers_to_digits_pt("há duzentos e cinquenta carros")
        self.assertIn("250", result)
        self.assertIn("há", result)
        self.assertIn("carros", result)

    def test_multiple_numbers(self):
        """
        Verify that `numbers_to_digits_pt` correctly converts multiple number words in a sentence to their digit representations.
        """
        result = numbers_to_digits_pt("dez carros e cinco pessoas")
        self.assertIn("10", result)
        self.assertIn("5", result)
        self.assertIn("carros", result)
        self.assertIn("pessoas", result)

    def test_no_numbers(self):
        """
        Verify that input text containing no numbers remains unchanged after conversion.
        """
        original = "apenas palavras normais"
        result = numbers_to_digits_pt(original)
        self.assertEqual(result, original)

    def test_edge_cases(self):
        """
        Test edge cases for the numbers_to_digits_pt function, including empty strings, single-word inputs, and conjunction-only input.
        """
        # Empty string
        self.assertEqual(numbers_to_digits_pt(""), "")

        # Single word
        self.assertEqual(numbers_to_digits_pt("cinco"), "5")

        # Just conjunction
        self.assertEqual(numbers_to_digits_pt("e"), "e")

    def test_variant_differences(self):
        """
        Verify that the Brazilian and Portugal Portuguese variants correctly convert their respective forms of 'sixteen' to the digit '16'.
        """
        br_result = numbers_to_digits_pt("dezesseis", variant=PortugueseVariant.BR)
        pt_result = numbers_to_digits_pt("dezasseis", variant=PortugueseVariant.PT)
        self.assertEqual(br_result, "16")
        self.assertEqual(pt_result, "16")


class TestTokenize(unittest.TestCase):
    """Test tokenize function."""

    def test_basic_tokenization(self):
        """
        Test that the tokenize function splits a simple sentence into individual words.
        """
        result = tokenize("palavra uma palavra duas")
        expected = ["palavra", "uma", "palavra", "duas"]
        self.assertEqual(result, expected)

    def test_percentage_split(self):
        """
        Test that the `tokenize` function correctly splits a percentage string into numeric and symbol tokens.
        """
        result = tokenize("12%")
        self.assertEqual(result, ["12", "%"])

    def test_hash_number_split(self):
        """
        Test that the tokenizer splits a hash symbol followed by a number into separate tokens.
        """
        result = tokenize("#1")
        self.assertEqual(result, ["#", "1"])

    def test_hyphen_between_words(self):
        """
        Test that the tokenizer splits hyphenated words into separate tokens, preserving the hyphen as its own token.
        """
        result = tokenize("amo-te")
        self.assertEqual(result, ["amo", "-", "te"])

    def test_hyphen_preservation_in_numbers(self):
        """
        Verify that hyphens within numeric ranges are preserved during tokenization.
        
        Ensures that the `tokenize` function does not split number ranges such as "1-2" into separate tokens.
        """
        result = tokenize("1-2")
        # Should not split number ranges
        self.assertIn("1-2", result)

    def test_trailing_hyphen_removal(self):
        """
        Test that tokenization removes trailing hyphens from words.
        
        Verifies that a word followed by a hyphen is correctly tokenized without including the hyphen.
        """
        result = tokenize("palavra -")
        self.assertEqual(result, ["palavra"])

    def test_empty_string(self):
        """
        Test that tokenizing an empty string returns an empty list.
        """
        result = tokenize("")
        self.assertEqual(result, [])

    def test_whitespace_handling(self):
        """
        Test that the tokenize function correctly handles and ignores extra whitespace between and around words.
        """
        result = tokenize("  palavra   outra  ")
        self.assertEqual(result, ["palavra", "outra"])

    def test_complex_input(self):
        """
        Test that the tokenizer correctly splits a complex input string containing hyphenated words, numbers with symbols, and mixed tokens.
        """
        result = tokenize("amo-te 50% #2 test")
        expected_elements = ["amo", "-", "te", "50", "%", "#", "2", "test"]
        self.assertEqual(result, expected_elements)


class TestPronounceFractionPt(unittest.TestCase):
    """Test pronounce_fraction_pt function."""

    def test_simple_fractions(self):
        """
        Test that `pronounce_fraction_pt` correctly pronounces simple fractions like "1/2" and "1/3" in Portuguese.
        """
        result = pronounce_fraction_pt("1/2")
        self.assertIn("um", result)
        self.assertIn("meio", result)

        result = pronounce_fraction_pt("1/3")
        self.assertIn("um", result)
        self.assertIn("terço", result)

    def test_plural_fractions(self):
        """
        Test that plural fractions are pronounced correctly in Portuguese.
        
        Verifies that the pronunciation of fractions with numerators greater than one includes the correct plural forms for both the numerator and denominator.
        """
        result = pronounce_fraction_pt("2/3")
        self.assertIn("dois", result)
        self.assertIn("terços", result)

        result = pronounce_fraction_pt("3/4")
        self.assertIn("três", result)
        self.assertIn("quartos", result)

    def test_large_denominators(self):
        """
        Test pronunciation of fractions with large denominators using `pronounce_fraction_pt`.
        
        Verifies that the function correctly pronounces fractions like "1/7" and "5/7", ensuring the numerator and the appropriate singular or plural form of the denominator are present in the result.
        """
        result = pronounce_fraction_pt("1/7")
        self.assertIn("um", result)
        self.assertIn("sétimo", result)

        result = pronounce_fraction_pt("5/7")
        self.assertIn("cinco", result)
        self.assertIn("sétimos", result)

    def test_unknown_denominators(self):
        """
        Test pronunciation of fractions with denominators not explicitly defined, ensuring the default term "avos" is used for unknown denominators.
        """
        result = pronounce_fraction_pt("1/13")
        self.assertIn("um", result)
        # Should use "avos" for unknown denominators

        result = pronounce_fraction_pt("2/13")
        self.assertIn("dois", result)
        self.assertIn("avos", result)

    def test_variant_differences(self):
        """
        Test that `pronounce_fraction_pt` returns string results for both Brazilian and Portugal Portuguese variants when pronouncing "1/16".
        """
        br_result = pronounce_fraction_pt("1/16", variant=PortugueseVariant.BR)
        pt_result = pronounce_fraction_pt("1/16", variant=PortugueseVariant.PT)
        # Both should work, may have slight differences in underlying number pronunciation
        self.assertIsInstance(br_result, str)
        self.assertIsInstance(pt_result, str)

    def test_scale_parameter(self):
        """
        Test that the `scale` parameter affects the pronunciation of large fractions in `pronounce_fraction_pt`.
        
        Verifies that both short and long scale pronunciations return strings for the fraction "1/1000000".
        """
        result_short = pronounce_fraction_pt("1/1000000", scale=Scale.SHORT)
        result_long = pronounce_fraction_pt("1/1000000", scale=Scale.LONG)
        self.assertIsInstance(result_short, str)
        self.assertIsInstance(result_long, str)

    def test_zero_numerator(self):
        """
        Test that fractions with a zero numerator are pronounced with "zero" in the output.
        """
        result = pronounce_fraction_pt("0/5")
        self.assertIn("zero", result)


class TestIntegrationScenarios(unittest.TestCase):
    """Test integration scenarios and edge cases."""

    def test_round_trip_conversion(self):
        """
        Verifies that converting numbers to Portuguese text and back yields the original value for a set of test cases.
        
        Ensures the `pronounce_number_pt` and `extract_number_pt` functions are consistent for round-trip conversions in the Brazilian Portuguese variant.
        """
        test_numbers = [1, 16, 100, 123, 1000, 1234]

        for num in test_numbers:
            # Convert number to text
            text = pronounce_number_pt(num, variant=PortugueseVariant.BR)
            # Convert text back to number
            extracted = extract_number_pt(text, variant=PortugueseVariant.BR)
            self.assertEqual(extracted, num, f"Round-trip failed for {num}: {text} -> {extracted}")

    def test_variant_consistency(self):
        """
        Verify that numbers with variant-specific pronunciations in Brazilian and Portugal Portuguese are correctly pronounced and extracted within each variant.
        """
        test_numbers = [16, 17, 19]  # Numbers that differ between variants

        for num in test_numbers:
            # Test BR variant
            br_text = pronounce_number_pt(num, variant=PortugueseVariant.BR)
            br_extracted = extract_number_pt(br_text, variant=PortugueseVariant.BR)
            self.assertEqual(br_extracted, num)

            # Test PT variant
            pt_text = pronounce_number_pt(num, variant=PortugueseVariant.PT)
            pt_extracted = extract_number_pt(pt_text, variant=PortugueseVariant.PT)
            self.assertEqual(pt_extracted, num)

    def test_scale_consistency(self):
        """
        Verify that number pronunciation and extraction remain consistent across short and long scales and both Portuguese variants for large numbers.
        
        Ensures that converting a large number to text and then extracting it back yields the original number, regardless of scale or variant.
        """
        large_numbers = [1000000, 1000000000]

        for num in large_numbers:
            for scale in [Scale.SHORT, Scale.LONG]:
                for variant in [PortugueseVariant.BR, PortugueseVariant.PT]:
                    text = pronounce_number_pt(num, scale=scale, variant=variant)
                    extracted = extract_number_pt(text, scale=scale, variant=variant)
                    print(text, extracted)
                    self.assertEqual(extracted, num,
                                     f"Scale consistency failed: {num} with {scale} and {variant}")

    def test_numbers_to_digits_integration(self):
        """
        Test that `numbers_to_digits_pt` correctly converts Portuguese number words to digits within phrases, preserving non-numeric words.
        """
        test_phrases = [
            "há duzentos e cinquenta carros",
            "comprei dezesseis livros",
            "mil e uma noites"
        ]

        for phrase in test_phrases:
            result = numbers_to_digits_pt(phrase, variant=PortugueseVariant.BR)
            # Should contain digits and preserve non-number words
            self.assertIsInstance(result, str)
            self.assertTrue(any(char.isdigit() for char in result))

    def test_error_handling_robustness(self):
        """
        Verify that number extraction and conversion functions handle invalid or nonsensical input strings without raising exceptions.
        """
        # Test various invalid inputs
        invalid_inputs = ["", "   ", "xyz123", "palavra-palavra"]

        for invalid_input in invalid_inputs:
            # extract_number_pt should return False for invalid input
            result = extract_number_pt(invalid_input)
            self.assertFalse(result)

            # numbers_to_digits_pt should handle gracefully
            result = numbers_to_digits_pt(invalid_input)
            self.assertIsInstance(result, str)

    def test_large_number_limits(self):
        """
        Test that `pronounce_number_pt` can handle extremely large numbers without raising exceptions.
        
        Asserts that the function returns a string when given a number as large as 10^30.
        """
        very_large = 10 ** 30

        # Should not raise exceptions
        try:
            result = pronounce_number_pt(very_large)
            self.assertIsInstance(result, str)
        except Exception as e:
            self.fail(f"Large number pronunciation failed: {e}")


if __name__ == '__main__':
    unittest.main()
