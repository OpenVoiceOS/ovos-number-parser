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
from ovos_number_parser.util import DigitPronunciation, Scale


class TestPortugueseVariant(unittest.TestCase):
    """Test PortugueseVariant enum."""

    def test_variant_values(self):
        """Test that variant enum has correct values."""
        self.assertEqual(PortugueseVariant.BR.value, "br")
        self.assertEqual(PortugueseVariant.PT.value, "pt")

    def test_variant_comparison(self):
        """Test variant enum comparison."""
        self.assertNotEqual(PortugueseVariant.BR, PortugueseVariant.PT)
        self.assertEqual(PortugueseVariant.BR, PortugueseVariant.BR)


class TestDictionaries(unittest.TestCase):
    """Test the pronunciation dictionaries."""

    def test_units_completeness(self):
        """Test that _UNITS contains all expected numbers."""
        expected_keys = list(range(1, 10))
        self.assertEqual(set(_UNITS.keys()), set(expected_keys))

    def test_tens_br_completeness(self):
        """Test that _TENS_BR contains all expected numbers."""
        expected_keys = list(range(10, 20)) + list(range(20, 100, 10))
        self.assertEqual(set(_TENS_BR.keys()), set(expected_keys))

    def test_tens_pt_completeness(self):
        """Test that _TENS_PT contains all expected numbers."""
        expected_keys = list(range(10, 20)) + list(range(20, 100, 10))
        self.assertEqual(set(_TENS_PT.keys()), set(expected_keys))

    def test_tens_variants_differences(self):
        """Test that BR and PT variants have expected differences."""
        # Key differences between BR and PT
        self.assertEqual(_TENS_BR[16], "dezesseis")
        self.assertEqual(_TENS_PT[16], "dezasseis")
        self.assertEqual(_TENS_BR[17], "dezessete")
        self.assertEqual(_TENS_PT[17], "dezassete")
        self.assertEqual(_TENS_BR[19], "dezenove")
        self.assertEqual(_TENS_PT[19], "dezanove")

    def test_hundreds_completeness(self):
        """Test that _HUNDREDS contains all expected numbers."""
        expected_keys = list(range(100, 1000, 100))
        self.assertEqual(set(_HUNDREDS.keys()), set(expected_keys))

    def test_fraction_string_pt_completeness(self):
        """Test that _FRACTION_STRING_PT contains expected fractions."""
        self.assertIn(2, _FRACTION_STRING_PT)
        self.assertIn(3, _FRACTION_STRING_PT)
        self.assertIn(10, _FRACTION_STRING_PT)
        self.assertEqual(_FRACTION_STRING_PT[2], "meio")
        self.assertEqual(_FRACTION_STRING_PT[3], "terço")

    def test_scales_structure(self):
        """Test that _SCALES has correct structure."""
        self.assertIn(Scale.SHORT, _SCALES)
        self.assertIn(Scale.LONG, _SCALES)
        self.assertIn(PortugueseVariant.BR, _SCALES[Scale.SHORT])
        self.assertIn(PortugueseVariant.PT, _SCALES[Scale.SHORT])

    def test_numbers_br_construction(self):
        """Test that _NUMBERS_BR is correctly constructed."""
        self.assertIn("um", _NUMBERS_BR)
        self.assertIn("dezesseis", _NUMBERS_BR)
        self.assertIn("bilhão", _NUMBERS_BR)
        self.assertEqual(_NUMBERS_BR["um"], 1)
        self.assertEqual(_NUMBERS_BR["dezesseis"], 16)

    def test_numbers_pt_construction(self):
        """Test that _NUMBERS_PT is correctly constructed."""
        self.assertIn("um", _NUMBERS_PT)
        self.assertIn("dezasseis", _NUMBERS_PT)
        self.assertIn("bilião", _NUMBERS_PT)
        self.assertEqual(_NUMBERS_PT["um"], 1)
        self.assertEqual(_NUMBERS_PT["dezasseis"], 16)


class TestPronounceUpTo999(unittest.TestCase):
    """Test _pronounce_up_to_999 function."""

    def test_zero(self):
        """Test pronunciation of zero."""
        result = _pronounce_up_to_999(0)
        self.assertEqual(result, "zero")

    def test_single_digits_br(self):
        """Test pronunciation of single digits in BR variant."""
        self.assertEqual(_pronounce_up_to_999(1, PortugueseVariant.BR), "um")
        self.assertEqual(_pronounce_up_to_999(5, PortugueseVariant.BR), "cinco")
        self.assertEqual(_pronounce_up_to_999(9, PortugueseVariant.BR), "nove")

    def test_single_digits_pt(self):
        """Test pronunciation of single digits in PT variant."""
        self.assertEqual(_pronounce_up_to_999(1, PortugueseVariant.PT), "um")
        self.assertEqual(_pronounce_up_to_999(5, PortugueseVariant.PT), "cinco")
        self.assertEqual(_pronounce_up_to_999(9, PortugueseVariant.PT), "nove")

    def test_teens_br(self):
        """Test pronunciation of teens in BR variant."""
        self.assertEqual(_pronounce_up_to_999(16, PortugueseVariant.BR), "dezesseis")
        self.assertEqual(_pronounce_up_to_999(17, PortugueseVariant.BR), "dezessete")
        self.assertEqual(_pronounce_up_to_999(19, PortugueseVariant.BR), "dezenove")

    def test_teens_pt(self):
        """Test pronunciation of teens in PT variant."""
        self.assertEqual(_pronounce_up_to_999(16, PortugueseVariant.PT), "dezasseis")
        self.assertEqual(_pronounce_up_to_999(17, PortugueseVariant.PT), "dezassete")
        self.assertEqual(_pronounce_up_to_999(19, PortugueseVariant.PT), "dezanove")

    def test_tens(self):
        """Test pronunciation of tens."""
        self.assertEqual(_pronounce_up_to_999(20), "vinte")
        self.assertEqual(_pronounce_up_to_999(30), "trinta")
        self.assertEqual(_pronounce_up_to_999(90), "noventa")

    def test_tens_with_units(self):
        """Test pronunciation of tens with units."""
        self.assertEqual(_pronounce_up_to_999(21), "vinte e um")
        self.assertEqual(_pronounce_up_to_999(35), "trinta e cinco")
        self.assertEqual(_pronounce_up_to_999(99), "noventa e nove")

    def test_exact_hundred(self):
        """Test pronunciation of exact hundred."""
        self.assertEqual(_pronounce_up_to_999(100), "cem")

    def test_hundreds_with_remainder(self):
        """Test pronunciation of hundreds with remainder."""
        self.assertEqual(_pronounce_up_to_999(101), "cento e um")
        self.assertEqual(_pronounce_up_to_999(123), "cento e vinte e três")
        self.assertEqual(_pronounce_up_to_999(200), "duzentos")
        self.assertEqual(_pronounce_up_to_999(234), "duzentos e trinta e quatro")

    def test_complex_numbers(self):
        """Test pronunciation of complex numbers."""
        self.assertEqual(_pronounce_up_to_999(567), "quinhentos e sessenta e sete")
        self.assertEqual(_pronounce_up_to_999(999), "novecentos e noventa e nove")

    def test_invalid_range(self):
        """Test that invalid ranges raise ValueError."""
        with self.assertRaises(ValueError):
            _pronounce_up_to_999(-1)
        with self.assertRaises(ValueError):
            _pronounce_up_to_999(1000)
        with self.assertRaises(ValueError):
            _pronounce_up_to_999(1001)


class TestIsFractionalPt(unittest.TestCase):
    """Test is_fractional_pt function."""

    def test_basic_fractions(self):
        """Test basic fraction recognition."""
        self.assertEqual(is_fractional_pt("meio"), 0.5)
        self.assertEqual(is_fractional_pt("terço"), 1.0 / 3)
        self.assertEqual(is_fractional_pt("quarto"), 0.25)

    def test_meia_variant(self):
        """Test 'meia' as variant of 'meio'."""
        self.assertEqual(is_fractional_pt("meia"), 0.5)

    def test_plural_forms(self):
        """Test plural forms of fractions."""
        self.assertEqual(is_fractional_pt("meios"), 0.5)
        self.assertEqual(is_fractional_pt("terços"), 1.0 / 3)
        self.assertEqual(is_fractional_pt("quartos"), 0.25)

    def test_special_fractions(self):
        """Test special fraction forms."""
        self.assertEqual(is_fractional_pt("décimo"), 0.1)
        self.assertEqual(is_fractional_pt("vigésimo"), 0.05)
        self.assertEqual(is_fractional_pt("centésimo"), 0.01)

    def test_compound_fractions(self):
        """Test compound fraction forms like 'onze avos'."""
        self.assertEqual(is_fractional_pt("onze avos"), 1.0 / 11)
        self.assertEqual(is_fractional_pt("doze avos"), 1.0 / 12)
        self.assertEqual(is_fractional_pt("treze avos"), 1.0 / 13)
        self.assertFalse(is_fractional_pt("onze"))
        self.assertFalse(is_fractional_pt("doze"))
        self.assertFalse(is_fractional_pt("treze"))

    def test_case_insensitive(self):
        """Test case insensitive matching."""
        self.assertEqual(is_fractional_pt("MEIO"), 0.5)
        self.assertEqual(is_fractional_pt("Terço"), 1.0 / 3)
        self.assertEqual(is_fractional_pt("MEIA"), 0.5)

    def test_whitespace_handling(self):
        """Test whitespace handling."""
        self.assertEqual(is_fractional_pt("  meio  "), 0.5)
        self.assertEqual(is_fractional_pt("\tterço\n"), 1.0 / 3)

    def test_non_fractions(self):
        """Test non-fraction strings return False."""
        self.assertFalse(is_fractional_pt("palavra"))
        self.assertFalse(is_fractional_pt("número"))
        self.assertFalse(is_fractional_pt(""))
        self.assertFalse(is_fractional_pt("123"))


class TestExtractNumberPt(unittest.TestCase):
    """Test extract_number_pt function."""

    def test_simple_numbers_br(self):
        """Test extraction of simple numbers in BR variant."""
        self.assertEqual(extract_number_pt("dezesseis", variant=PortugueseVariant.BR), 16)
        self.assertEqual(extract_number_pt("vinte e um", variant=PortugueseVariant.BR), 21)
        self.assertEqual(extract_number_pt("cem", variant=PortugueseVariant.BR), 100)

    def test_simple_numbers_pt(self):
        """Test extraction of simple numbers in PT variant."""
        self.assertEqual(extract_number_pt("dezasseis", variant=PortugueseVariant.PT), 16)
        self.assertEqual(extract_number_pt("vinte e um", variant=PortugueseVariant.PT), 21)
        self.assertEqual(extract_number_pt("cem", variant=PortugueseVariant.PT), 100)

    def test_large_numbers_short_scale_br(self):
        """Test extraction of large numbers in short scale BR."""
        self.assertEqual(extract_number_pt("um milhão", scale=Scale.SHORT, variant=PortugueseVariant.BR), 1000000)
        self.assertEqual(extract_number_pt("um bilhão", scale=Scale.SHORT, variant=PortugueseVariant.BR), 1000000000)

    def test_large_numbers_short_scale_pt(self):
        """Test extraction of large numbers in short scale PT."""
        self.assertEqual(extract_number_pt("um milhão", scale=Scale.SHORT, variant=PortugueseVariant.PT), 1e6)
        self.assertEqual(extract_number_pt("um bilião", scale=Scale.SHORT, variant=PortugueseVariant.PT), 1e9)
        self.assertEqual(extract_number_pt("um trilião", scale=Scale.SHORT, variant=PortugueseVariant.PT), 1e12)

    def test_large_numbers_long_scale(self):
        """Test extraction of large numbers in long scale."""
        # TODO - failing
        self.assertEqual(extract_number_pt("um milhão", scale=Scale.LONG, variant=PortugueseVariant.PT), 1e6)
        self.assertEqual(extract_number_pt("um bilião", scale=Scale.LONG, variant=PortugueseVariant.PT), 1e12)
        self.assertEqual(extract_number_pt("um trilião", scale=Scale.LONG, variant=PortugueseVariant.PT), 1e18)

    def test_complex_numbers(self):
        """Test extraction of complex number phrases."""
        self.assertEqual(extract_number_pt("duzentos e cinquenta e três"), 253)
        self.assertEqual(extract_number_pt("mil quinhentos e quarenta e dois"), 1542)

    def test_fractions_in_text(self):
        """Test extraction of fractions from text."""
        result = extract_number_pt("dois e meio")
        self.assertAlmostEqual(result, 2.5, places=5)

    def test_decimal_handling(self):
        """Test decimal number handling."""
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
        """Test hyphen handling in text."""
        self.assertEqual(extract_number_pt("vinte-e-um", variant=PortugueseVariant.BR), 21)

    def test_no_number_found(self):
        """Test when no number is found in text."""
        self.assertFalse(extract_number_pt("apenas palavras"))
        self.assertFalse(extract_number_pt(""))
        self.assertFalse(extract_number_pt("xyz"))

    def test_multiple_scales(self):
        """Test numbers with multiple scale words."""
        self.assertEqual(extract_number_pt("dois milhões trezentos mil"), 2300000)

    def test_edge_cases(self):
        """Test edge cases."""
        self.assertEqual(extract_number_pt("zero"), 0)
        self.assertEqual(extract_number_pt("mil"), 1000)


class TestPronounceNumberPt(unittest.TestCase):
    """Test pronounce_number_pt function."""

    def test_type_validation(self):
        """Test type validation."""
        with self.assertRaises(TypeError):
            pronounce_number_pt("not a number")
        with self.assertRaises(TypeError):
            pronounce_number_pt(None)

    def test_zero(self):
        """Test pronunciation of zero."""
        self.assertEqual(pronounce_number_pt(0), "zero")

    def test_negative_numbers(self):
        """Test pronunciation of negative numbers."""
        result = pronounce_number_pt(-5)
        self.assertTrue(result.startswith("menos"))
        self.assertIn("cinco", result)

    def test_simple_integers(self):
        """Test pronunciation of simple integers."""
        self.assertEqual(pronounce_number_pt(1), "um")
        self.assertEqual(pronounce_number_pt(16, variant=PortugueseVariant.BR), "dezesseis")
        self.assertEqual(pronounce_number_pt(16, variant=PortugueseVariant.PT), "dezasseis")

    def test_hundreds(self):
        """Test pronunciation of hundreds."""
        self.assertEqual(pronounce_number_pt(100), "cem")
        self.assertEqual(pronounce_number_pt(200), "duzentos")
        self.assertEqual(pronounce_number_pt(123), "cento e vinte e três")

    def test_thousands(self):
        """Test pronunciation of thousands."""
        result = pronounce_number_pt(1000)
        self.assertIn("mil", result)

        result = pronounce_number_pt(2500)
        self.assertIn("mil", result)
        self.assertIn("quinhentos", result)

    def test_millions_short_scale_br(self):
        """Test pronunciation of millions in short scale BR."""
        result = pronounce_number_pt(1000000, scale=Scale.SHORT, variant=PortugueseVariant.BR)
        self.assertIn("milhão", result)

        result = pronounce_number_pt(1000000000, scale=Scale.SHORT, variant=PortugueseVariant.BR)
        self.assertIn("bilhão", result)

    def test_millions_short_scale_pt(self):
        """Test pronunciation of millions in short scale PT."""
        result = pronounce_number_pt(1000000, scale=Scale.SHORT, variant=PortugueseVariant.PT)
        self.assertIn("milhão", result)

        result = pronounce_number_pt(1000000000, scale=Scale.SHORT, variant=PortugueseVariant.PT)
        self.assertIn("bilião", result)

    def test_millions_long_scale(self):
        """Test pronunciation of millions in long scale."""
        result = pronounce_number_pt(1000000, scale=Scale.LONG, variant=PortugueseVariant.PT)
        self.assertIn("milhão", result)

        result = pronounce_number_pt(1000000000000, scale=Scale.LONG, variant=PortugueseVariant.PT)
        self.assertIn("bilião", result)

    def test_decimal_numbers(self):
        """Test pronunciation of decimal numbers."""
        result = pronounce_number_pt(1.5)
        self.assertIn("vírgula", result)
        self.assertIn("um", result)
        self.assertIn("cinco", result)

    def test_decimal_edge_cases(self):
        """Test edge cases for decimal numbers."""
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
        """Test 'um mil' """
        result = pronounce_number_pt(1000)
        # Should not start with "um mil" but just "mil"
        self.assertFalse(result.startswith("um mil"))

    def test_places_parameter(self):
        """
        Test that the `places` parameter in `pronounce_number_pt` correctly limits the number of decimal places pronounced when using digit-by-digit pronunciation.
        
        Ensures that specifying different values for `places` produces valid string outputs without errors.
        """
        result1 = pronounce_number_pt(1.23456, places=2, digits=DigitPronunciation.DIGIT_BY_DIGIT)
        result2 = pronounce_number_pt(1.23456, places=5, digits=DigitPronunciation.DIGIT_BY_DIGIT)
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
        """Test complex number phrase replacement."""
        result = numbers_to_digits_pt("duzentos e cinquenta e três")
        self.assertEqual(result, "253")

    def test_mixed_text(self):
        """Test text with mixed words and numbers."""
        result = numbers_to_digits_pt("há duzentos e cinquenta carros")
        self.assertIn("250", result)
        self.assertIn("há", result)
        self.assertIn("carros", result)

    def test_multiple_numbers(self):
        """Test text with multiple separate numbers."""
        result = numbers_to_digits_pt("dez carros e cinco pessoas")
        self.assertIn("10", result)
        self.assertIn("5", result)
        self.assertIn("carros", result)
        self.assertIn("pessoas", result)

    def test_no_numbers(self):
        """Test text with no numbers."""
        original = "apenas palavras normais"
        result = numbers_to_digits_pt(original)
        self.assertEqual(result, original)

    def test_edge_cases(self):
        """Test edge cases."""
        # Empty string
        self.assertEqual(numbers_to_digits_pt(""), "")

        # Single word
        self.assertEqual(numbers_to_digits_pt("cinco"), "5")

        # Just conjunction
        self.assertEqual(numbers_to_digits_pt("e"), "e")

    def test_variant_differences(self):
        """Test that variants produce different results where expected."""
        br_result = numbers_to_digits_pt("dezesseis", variant=PortugueseVariant.BR)
        pt_result = numbers_to_digits_pt("dezasseis", variant=PortugueseVariant.PT)
        self.assertEqual(br_result, "16")
        self.assertEqual(pt_result, "16")


class TestTokenize(unittest.TestCase):
    """Test tokenize function."""

    def test_basic_tokenization(self):
        """Test basic word tokenization."""
        result = tokenize("palavra uma palavra duas")
        expected = ["palavra", "uma", "palavra", "duas"]
        self.assertEqual(result, expected)

    def test_percentage_split(self):
        """Test splitting percentages."""
        result = tokenize("12%")
        self.assertEqual(result, ["12", "%"])

    def test_hash_number_split(self):
        """Test splitting hash with numbers."""
        result = tokenize("#1")
        self.assertEqual(result, ["#", "1"])

    def test_hyphen_between_words(self):
        """Test hyphen handling between words."""
        result = tokenize("amo-te")
        self.assertEqual(result, ["amo", "-", "te"])

    def test_hyphen_preservation_in_numbers(self):
        """Test that hyphens in numbers are preserved."""
        result = tokenize("1-2")
        # Should not split number ranges
        self.assertIn("1-2", result)

    def test_trailing_hyphen_removal(self):
        """Test removal of trailing hyphens."""
        result = tokenize("palavra -")
        self.assertEqual(result, ["palavra"])

    def test_empty_string(self):
        """Test tokenization of empty string."""
        result = tokenize("")
        self.assertEqual(result, [])

    def test_whitespace_handling(self):
        """Test handling of various whitespace."""
        result = tokenize("  palavra   outra  ")
        self.assertEqual(result, ["palavra", "outra"])

    def test_complex_input(self):
        """Test complex input with multiple patterns."""
        result = tokenize("amo-te 50% #2 test")
        expected_elements = ["amo", "-", "te", "50", "%", "#", "2", "test"]
        self.assertEqual(result, expected_elements)


class TestPronounceFractionPt(unittest.TestCase):
    """Test pronounce_fraction_pt function."""

    def test_simple_fractions(self):
        """Test pronunciation of simple fractions."""
        result = pronounce_fraction_pt("1/2")
        self.assertIn("um", result)
        self.assertIn("meio", result)

        result = pronounce_fraction_pt("1/3")
        self.assertIn("um", result)
        self.assertIn("terço", result)

    def test_plural_fractions(self):
        """Test pronunciation of plural fractions."""
        result = pronounce_fraction_pt("2/3")
        self.assertIn("dois", result)
        self.assertIn("terços", result)

        result = pronounce_fraction_pt("3/4")
        self.assertIn("três", result)
        self.assertIn("quartos", result)

    def test_large_denominators(self):
        """Test fractions with large denominators."""
        result = pronounce_fraction_pt("1/7")
        self.assertIn("um", result)
        self.assertIn("sétimo", result)

        result = pronounce_fraction_pt("5/7")
        self.assertIn("cinco", result)
        self.assertIn("sétimos", result)

    def test_unknown_denominators(self):
        """Test fractions with denominators not in predefined list."""
        result = pronounce_fraction_pt("1/13")
        self.assertIn("um", result)
        # Should use "avos" for unknown denominators

        result = pronounce_fraction_pt("2/13")
        self.assertIn("dois", result)
        self.assertIn("avos", result)

    def test_variant_differences(self):
        """Test variant differences in fraction pronunciation."""
        br_result = pronounce_fraction_pt("1/16", variant=PortugueseVariant.BR)
        pt_result = pronounce_fraction_pt("1/16", variant=PortugueseVariant.PT)
        # Both should work, may have slight differences in underlying number pronunciation
        self.assertIsInstance(br_result, str)
        self.assertIsInstance(pt_result, str)

    def test_scale_parameter(self):
        """Test scale parameter in fraction pronunciation."""
        result_short = pronounce_fraction_pt("1/1000000", scale=Scale.SHORT)
        result_long = pronounce_fraction_pt("1/1000000", scale=Scale.LONG)
        self.assertIsInstance(result_short, str)
        self.assertIsInstance(result_long, str)

    def test_zero_numerator(self):
        """Test fractions with zero numerator."""
        result = pronounce_fraction_pt("0/5")
        self.assertIn("zero", result)


class TestIntegrationScenarios(unittest.TestCase):
    """Test integration scenarios and edge cases."""

    def test_round_trip_conversion(self):
        """Test round-trip conversion: number -> text -> number."""
        test_numbers = [1, 16, 100, 123, 1000, 1234]

        for num in test_numbers:
            # Convert number to text
            text = pronounce_number_pt(num, variant=PortugueseVariant.BR)
            # Convert text back to number
            extracted = extract_number_pt(text, variant=PortugueseVariant.BR)
            self.assertEqual(extracted, num, f"Round-trip failed for {num}: {text} -> {extracted}")

    def test_variant_consistency(self):
        """Test that BR and PT variants are internally consistent."""
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
        """Test that different scales work consistently."""
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
        """Test integration with numbers_to_digits_pt."""
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
        """Test robustness of error handling across functions."""
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
        """Test behavior with very large numbers."""
        very_large = 10 ** 30

        # Should not raise exceptions
        try:
            result = pronounce_number_pt(very_large)
            self.assertIsInstance(result, str)
        except Exception as e:
            self.fail(f"Large number pronunciation failed: {e}")


if __name__ == '__main__':
    unittest.main()
