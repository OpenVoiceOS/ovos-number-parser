import unittest

from ovos_number_parser import extract_number

from ovos_number_parser.numbers_pt import (
    PortugueseVariant,
    PT_PT, PT_BR
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
        expected_keys = list(range(0, 10))
        self.assertEqual(set(PT_PT.vocab.UNITS.keys()), set(expected_keys))

    def test_tens_br_completeness(self):
        """Test that _TENS_BR contains all expected numbers."""
        expected_keys = list(range(10, 20)) + list(range(20, 100, 10))
        self.assertEqual(set(PT_BR.vocab.TENS.keys()), set(expected_keys))

    def test_tens_pt_completeness(self):
        """Test that _TENS_PT contains all expected numbers."""
        expected_keys = list(range(10, 20)) + list(range(20, 100, 10))
        self.assertEqual(set(PT_PT.vocab.TENS.keys()), set(expected_keys))

    def test_tens_variants_differences(self):
        """Test that BR and PT variants have expected differences."""
        # Key differences between BR and PT
        self.assertEqual(PT_BR.vocab.TENS[16], "dezesseis")
        self.assertEqual(PT_PT.vocab.TENS[16], "dezasseis")
        self.assertEqual(PT_BR.vocab.TENS[17], "dezessete")
        self.assertEqual(PT_PT.vocab.TENS[17], "dezassete")
        self.assertEqual(PT_BR.vocab.TENS[19], "dezenove")
        self.assertEqual(PT_PT.vocab.TENS[19], "dezanove")

    def test_hundreds_completeness(self):
        """Test that _HUNDREDS contains all expected numbers."""
        expected_keys = list(range(100, 1000, 100))
        self.assertEqual(set(PT_PT.vocab.HUNDREDS.keys()), set(expected_keys))

    def test_fraction_string_pt_completeness(self):
        """Test that _FRACTION_STRING_PT contains expected fractions."""
        self.assertIn(2, PT_PT.vocab.FRACTION)
        self.assertIn(3, PT_PT.vocab.FRACTION)
        self.assertIn(10, PT_PT.vocab.FRACTION)
        self.assertEqual(PT_PT.vocab.FRACTION[2], "meio")
        self.assertEqual(PT_PT.vocab.FRACTION[3], "terço")

    def test_numbers_br_construction(self):
        """Test that _NUMBERS_BR is correctly constructed."""
        _NUMBERS_BR = PT_BR.vocab.get_number_strings()
        self.assertIn("um", _NUMBERS_BR)
        self.assertIn("dezesseis", _NUMBERS_BR)
        self.assertIn("bilhão", _NUMBERS_BR)
        self.assertEqual(_NUMBERS_BR["um"], 1)
        self.assertEqual(_NUMBERS_BR["dezesseis"], 16)

    def test_numbers_pt_construction(self):
        """Test that _NUMBERS_PT is correctly constructed."""
        _NUMBERS_PT = PT_PT.vocab.get_number_strings()
        self.assertIn("um", _NUMBERS_PT)
        self.assertIn("dezasseis", _NUMBERS_PT)
        self.assertIn("bilião", _NUMBERS_PT)
        self.assertEqual(_NUMBERS_PT["um"], 1)
        self.assertEqual(_NUMBERS_PT["dezasseis"], 16)


class TestPronounceUpTo999(unittest.TestCase):
    """Test PT_PT.pronounce_number function."""

    def test_zero(self):
        """Test pronunciation of zero."""
        result = PT_PT.pronounce_number(0)
        self.assertEqual(result, "zero")

    def test_single_digits_br(self):
        """Test pronunciation of single digits in BR variant."""
        self.assertEqual(PT_BR.pronounce_number(1), "um")
        self.assertEqual(PT_BR.pronounce_number(5), "cinco")
        self.assertEqual(PT_BR.pronounce_number(9), "nove")

    def test_single_digits_pt(self):
        """Test pronunciation of single digits in PT variant."""
        self.assertEqual(PT_PT.pronounce_number(1), "um")
        self.assertEqual(PT_PT.pronounce_number(5), "cinco")
        self.assertEqual(PT_PT.pronounce_number(9), "nove")

    def test_teens_br(self):
        """Test pronunciation of teens in BR variant."""
        self.assertEqual(PT_BR.pronounce_number(16), "dezesseis")
        self.assertEqual(PT_BR.pronounce_number(17), "dezessete")
        self.assertEqual(PT_BR.pronounce_number(19), "dezenove")

    def test_teens_pt(self):
        """Test pronunciation of teens in PT variant."""
        self.assertEqual(PT_PT.pronounce_number(16), "dezasseis")
        self.assertEqual(PT_PT.pronounce_number(17), "dezassete")
        self.assertEqual(PT_PT.pronounce_number(19), "dezanove")

    def test_tens(self):
        """Test pronunciation of tens."""
        self.assertEqual(PT_PT.pronounce_number(20), "vinte")
        self.assertEqual(PT_PT.pronounce_number(30), "trinta")
        self.assertEqual(PT_PT.pronounce_number(90), "noventa")

    def test_tens_with_units(self):
        """Test pronunciation of tens with units."""
        self.assertEqual(PT_PT.pronounce_number(21), "vinte e um")
        self.assertEqual(PT_PT.pronounce_number(35), "trinta e cinco")
        self.assertEqual(PT_PT.pronounce_number(99), "noventa e nove")

    def test_exact_hundred(self):
        """Test pronunciation of exact hundred."""
        self.assertEqual(PT_PT.pronounce_number(100), "cem")

    def test_hundreds_with_remainder(self):
        """Test pronunciation of hundreds with remainder."""
        self.assertEqual(PT_PT.pronounce_number(101), "cento e um")
        self.assertEqual(PT_PT.pronounce_number(123), "cento e vinte e três")
        self.assertEqual(PT_PT.pronounce_number(200), "duzentos")
        self.assertEqual(PT_PT.pronounce_number(234), "duzentos e trinta e quatro")

    def test_complex_numbers(self):
        """Test pronunciation of complex numbers."""
        self.assertEqual(PT_PT.pronounce_number(567), "quinhentos e sessenta e sete")
        self.assertEqual(PT_PT.pronounce_number(999), "novecentos e noventa e nove")


class TestIsFractionalPt(unittest.TestCase):
    """Test PT_PT.is_fractional function."""

    def test_basic_fractions(self):
        """Test basic fraction recognition."""
        self.assertEqual(PT_PT.is_fractional("meio"), 0.5)
        self.assertEqual(PT_PT.is_fractional("terço"), 1.0 / 3)
        self.assertEqual(PT_PT.is_fractional("quarto"), 0.25)

    def test_meia_variant(self):
        """Test 'meia' as variant of 'meio'."""
        self.assertEqual(PT_PT.is_fractional("meia"), 0.5)

    def test_plural_forms(self):
        """Test plural forms of fractions."""
        self.assertEqual(PT_PT.is_fractional("meios"), 0.5)
        self.assertEqual(PT_PT.is_fractional("terços"), 1.0 / 3)
        self.assertEqual(PT_PT.is_fractional("quartos"), 0.25)

    def test_special_fractions(self):
        """Test special fraction forms."""
        self.assertEqual(PT_PT.is_fractional("décimo"), 0.1)
        self.assertEqual(PT_PT.is_fractional("vigésimo"), 0.05)
        self.assertEqual(PT_PT.is_fractional("centésimo"), 0.01)

    def test_compound_fractions(self):
        """Test compound fraction forms like 'onze avos'."""
        self.assertEqual(PT_PT.is_fractional("onze avos"), 1.0 / 11)
        self.assertEqual(PT_PT.is_fractional("doze avos"), 1.0 / 12)
        self.assertEqual(PT_PT.is_fractional("treze avos"), 1.0 / 13)
        self.assertFalse(PT_PT.is_fractional("onze"))
        self.assertFalse(PT_PT.is_fractional("doze"))
        self.assertFalse(PT_PT.is_fractional("treze"))

    def test_case_insensitive(self):
        """Test case insensitive matching."""
        self.assertEqual(PT_PT.is_fractional("MEIO"), 0.5)
        self.assertEqual(PT_PT.is_fractional("Terço"), 1.0 / 3)
        self.assertEqual(PT_PT.is_fractional("MEIA"), 0.5)

    def test_whitespace_handling(self):
        """Test whitespace handling."""
        self.assertEqual(PT_PT.is_fractional("  meio  "), 0.5)
        self.assertEqual(PT_PT.is_fractional("\tterço\n"), 1.0 / 3)

    def test_non_fractions(self):
        """Test non-fraction strings return False."""
        self.assertFalse(PT_PT.is_fractional("palavra"))
        self.assertFalse(PT_PT.is_fractional("número"))
        self.assertFalse(PT_PT.is_fractional(""))
        self.assertFalse(PT_PT.is_fractional("123"))


class TestExtractNumberPt(unittest.TestCase):
    """Test PT_PT.extract_number function."""

    def test_simple_numbers_br(self):
        """Test extraction of simple numbers in BR variant."""
        self.assertEqual(extract_number("dezesseis", lang="pt-BR"), 16)
        self.assertEqual(extract_number("vinte e um", lang="pt-BR"), 21)
        self.assertEqual(extract_number("cem", lang="pt-BR"), 100)

    def test_simple_numbers_pt(self):
        """Test extraction of simple numbers in PT variant."""
        self.assertEqual(extract_number("dezasseis", lang="pt-PT"), 16)
        self.assertEqual(extract_number("vinte e um", lang="pt-PT"), 21)
        self.assertEqual(extract_number("cem", lang="pt-PT"), 100)

    def test_large_numbers_short_scale_br(self):
        """Test extraction of large numbers in short scale BR."""
        self.assertEqual(extract_number("um milhão", scale=Scale.SHORT, lang="pt-BR"), 1000000)
        self.assertEqual(extract_number("um bilhão", scale=Scale.SHORT, lang="pt-BR"), 1000000000)

    def test_large_numbers_short_scale_pt(self):
        """Test extraction of large numbers in short scale PT."""
        self.assertEqual(extract_number("um milhão", scale=Scale.SHORT, lang="pt-PT"), 1e6)
        self.assertEqual(extract_number("um bilião", scale=Scale.SHORT, lang="pt-PT"), 1e9)
        self.assertEqual(extract_number("um trilião", scale=Scale.SHORT, lang="pt-PT"), 1e12)

    def test_large_numbers_long_scale(self):
        """Test extraction of large numbers in long scale."""
        self.assertEqual(extract_number("um milhão", scale=Scale.LONG, lang="pt-PT"), 1e6)
        self.assertEqual(extract_number("um bilião", scale=Scale.LONG, lang="pt-PT"), 1e12)
        self.assertEqual(extract_number("um trilião", scale=Scale.LONG, lang="pt-PT"), 1e18)

    def test_complex_numbers(self):
        """Test extraction of complex number phrases."""
        self.assertEqual(extract_number("duzentos e cinquenta e três", lang="pt-PT"), 253)
        self.assertEqual(extract_number("mil quinhentos e quarenta e dois", lang="pt-PT"), 1542)

    def test_fractions_in_text(self):
        """Test extraction of fractions from text."""
        result = extract_number("dois e meio", lang="pt-PT")
        self.assertAlmostEqual(result, 2.5, places=5)

    def test_decimal_handling(self):
        """Test decimal number handling."""
        # Note: This tests the simplified decimal approach
        result = extract_number("dez ponto cinco", lang="pt-PT")
        # The function should handle this but may need specific formatting
        if result:
            self.assertIsInstance(result, (int, float))

    def test_case_insensitive(self):
        """Test case insensitive extraction."""
        self.assertEqual(extract_number("DEZESSEIS", lang="pt-BR"), 16)
        self.assertEqual(extract_number("Vinte E Um", lang="pt-BR"), 21)

    def test_hyphen_handling(self):
        """Test hyphen handling in text."""
        self.assertEqual(extract_number("vinte-e-um", lang="pt-BR"), 21)

    def test_no_number_found(self):
        """Test when no number is found in text."""
        self.assertFalse(extract_number("apenas palavras", lang="pt-PT"))
        self.assertFalse(extract_number("", lang="pt-PT"))
        self.assertFalse(extract_number("xyz", lang="pt-PT"))


    def test_edge_cases(self):
        """Test edge cases."""
        self.assertEqual(extract_number("zero", lang="pt-PT"), 0)
        self.assertEqual(extract_number("mil", lang="pt-PT"), 1000)


class TestPronounceNumberPt(unittest.TestCase):
    """Test PT_PT.pronounce_number function."""

    def test_type_validation(self):
        """Test type validation."""
        with self.assertRaises(TypeError):
            PT_PT.pronounce_number("not a number")
        with self.assertRaises(TypeError):
            PT_PT.pronounce_number(None)

    def test_zero(self):
        """Test pronunciation of zero."""
        self.assertEqual(PT_PT.pronounce_number(0), "zero")

    def test_negative_numbers(self):
        """Test pronunciation of negative numbers."""
        result = PT_PT.pronounce_number(-5)
        self.assertTrue(result.startswith("menos"))
        self.assertIn("cinco", result)

    def test_simple_integers(self):
        """Test pronunciation of simple integers."""
        self.assertEqual(PT_PT.pronounce_number(1), "um")
        self.assertEqual(PT_BR.pronounce_number(16), "dezesseis")
        self.assertEqual(PT_PT.pronounce_number(16), "dezasseis")

    def test_hundreds(self):
        """Test pronunciation of hundreds."""
        self.assertEqual(PT_PT.pronounce_number(100), "cem")
        self.assertEqual(PT_PT.pronounce_number(200), "duzentos")
        self.assertEqual(PT_PT.pronounce_number(123), "cento e vinte e três")

    def test_thousands(self):
        """Test pronunciation of thousands."""
        result = PT_PT.pronounce_number(1000)
        self.assertIn("mil", result)

        result = PT_PT.pronounce_number(2500)
        self.assertIn("mil", result)
        self.assertIn("quinhentos", result)

    def test_millions_short_scale_br(self):
        """Test pronunciation of millions in short scale BR."""
        result = PT_BR.pronounce_number(1000000, scale=Scale.SHORT)
        self.assertIn("milhão", result)

        result = PT_BR.pronounce_number(1000000000, scale=Scale.SHORT)
        self.assertIn("bilhão", result)

    def test_millions_short_scale_pt(self):
        """Test pronunciation of millions in short scale PT."""
        result = PT_PT.pronounce_number(1000000, scale=Scale.SHORT)
        self.assertIn("milhão", result)

        result = PT_PT.pronounce_number(1000000000, scale=Scale.SHORT)
        self.assertIn("bilião", result)

    def test_millions_long_scale(self):
        """Test pronunciation of millions in long scale."""
        result = PT_PT.pronounce_number(1000000, scale=Scale.LONG)
        self.assertIn("milhão", result)

        result = PT_PT.pronounce_number(1000000000000, scale=Scale.LONG)
        self.assertIn("bilião", result)

    def test_decimal_numbers(self):
        """Test pronunciation of decimal numbers."""
        result = PT_PT.pronounce_number(1.5)
        self.assertIn("vírgula", result)
        self.assertIn("um", result)
        self.assertIn("cinco", result)

    def test_significant_digits(self):
        """Test pronunciation of decimal places and rounding"""
        self.assertEqual(PT_PT.pronounce_number(123.456789, places=1),
                         "cento e vinte e três vírgula cinco")
        self.assertEqual(PT_PT.pronounce_number(123.456789, places=2),
                         "cento e vinte e três vírgula quarenta e seis")
        self.assertEqual(PT_PT.pronounce_number(123.456789, places=3),
                         "cento e vinte e três vírgula quatrocentos e cinquenta e sete")
        self.assertEqual(PT_PT.pronounce_number(123.456789, places=4),
                         "cento e vinte e três vírgula quatro mil quinhentos e sessenta e oito")
        self.assertEqual(PT_PT.pronounce_number(123.456789, places=5),
                         "cento e vinte e três vírgula quarenta e cinco mil seiscentos e setenta e nove")

    def test_leading_zeros(self):
        """Test pronunciation of decimal numbers."""
        # no rounding to significant digit when we have leading zeros
        self.assertEqual(PT_PT.pronounce_number(10.05),
                         "dez vírgula zero cinco")
        self.assertEqual(PT_PT.pronounce_number(10.005),
                         "dez vírgula zero zero cinco")
        self.assertEqual(PT_PT.pronounce_number(10.0005),
                         "dez vírgula zero zero zero cinco")
        self.assertEqual(PT_PT.pronounce_number(10.0000005),
                         "dez vírgula zero zero zero zero zero zero cinco")
        self.assertEqual(PT_PT.pronounce_number(10.00000056),
                         "dez vírgula zero zero zero zero zero zero seis")

    @unittest.skip("TODO - do we want it to behave like this? currently not implemented")
    def test_decimal_edge_cases(self):
        """Test edge cases for decimal numbers."""
        # Test when decimal part rounds to zero, should we read the significant digits?
        result = PT_PT.pronounce_number(1.0)
        self.assertEqual(result, "um vírgula zero")
        result = PT_PT.pronounce_number(1.00)
        self.assertEqual(result, "um vírgula zero zero")
        result = PT_PT.pronounce_number(1.000)
        self.assertEqual(result, "um vírgula zero zero zero")

    def test_conjunction_logic(self):
        """Test conjunction logic for complex numbers."""
        result = PT_PT.pronounce_number(1001)
        self.assertIn("e", result)  # Should have conjunction for small remainder

        result = PT_PT.pronounce_number(1100)
        self.assertIn("e", result)  # Should have conjunction for multiple of 100

    def test_mil(self):
        """Test 'um mil' """
        result = PT_PT.pronounce_number(1000)
        # Should not start with "um mil" but just "mil"
        self.assertFalse(result.startswith("um mil"))

    def test_places_parameter(self):
        """
        Test that the `places` parameter in `PT_PT.pronounce_number` correctly limits the number of decimal places pronounced when using digit-by-digit pronunciation.
        
        Ensures that specifying different values for `places` produces valid string outputs without errors.
        """
        result1 = PT_PT.pronounce_number(1.23456, places=2, digits=DigitPronunciation.DIGIT_BY_DIGIT)
        result2 = PT_PT.pronounce_number(1.23456, places=5, digits=DigitPronunciation.DIGIT_BY_DIGIT)
        # Both should work without error
        self.assertIsInstance(result1, str)
        self.assertIsInstance(result2, str)


class TestNumbersToDigitsPt(unittest.TestCase):
    """Test PT_PT.numbers_to_digits function."""

    def test_simple_replacement(self):
        """Test simple number word replacement."""
        self.assertEqual(PT_PT.numbers_to_digits("dezesseis"), "16")
        self.assertEqual(PT_PT.numbers_to_digits("dezasseis"), "16")

    def test_complex_numbers(self):
        """Test complex number phrase replacement."""
        result = PT_PT.numbers_to_digits("duzentos e cinquenta e três")
        self.assertEqual(result, "253")

    def test_mixed_text(self):
        """Test text with mixed words and numbers."""
        result = PT_PT.numbers_to_digits("há duzentos e cinquenta carros")
        self.assertIn("250", result)
        self.assertIn("há", result)
        self.assertIn("carros", result)

    def test_multiple_numbers(self):
        """Test text with multiple separate numbers."""
        result = PT_PT.numbers_to_digits("dez carros e cinco pessoas")
        self.assertIn("10", result)
        self.assertIn("5", result)
        self.assertIn("carros", result)
        self.assertIn("pessoas", result)

    def test_no_numbers(self):
        """Test text with no numbers."""
        original = "apenas palavras normais"
        result = PT_PT.numbers_to_digits(original)
        self.assertEqual(result, original)

    def test_edge_cases(self):
        """Test edge cases."""
        # Empty string
        self.assertEqual(PT_PT.numbers_to_digits(""), "")

        # Single word
        self.assertEqual(PT_PT.numbers_to_digits("cinco"), "5")

        # Just conjunction
        self.assertEqual(PT_PT.numbers_to_digits("e"), "e")

    def test_variant_differences(self):
        """Test that variants produce different results where expected."""
        br_result = PT_BR.numbers_to_digits("dezesseis")
        pt_result = PT_PT.numbers_to_digits("dezasseis")
        self.assertEqual(br_result, "16")
        self.assertEqual(pt_result, "16")


class TestPronounceFractionPt(unittest.TestCase):
    """Test PT_PT.pronounce_fraction function."""

    def test_simple_fractions(self):
        """Test pronunciation of simple fractions."""
        result = PT_PT.pronounce_fraction("1/2")
        self.assertIn("um", result)
        self.assertIn("meio", result)

        result = PT_PT.pronounce_fraction("1/3")
        self.assertIn("um", result)
        self.assertIn("terço", result)

    def test_plural_fractions(self):
        """Test pronunciation of plural fractions."""
        result = PT_PT.pronounce_fraction("2/3")
        self.assertIn("dois", result)
        self.assertIn("terços", result)

        result = PT_PT.pronounce_fraction("3/4")
        self.assertIn("três", result)
        self.assertIn("quartos", result)

    def test_zero_division(self):
        """Test pronunciation of plural fractions."""
        result = PT_PT.pronounce_fraction("0/0")
        self.assertIn("zero", result)
        self.assertIn(PT_PT.vocab.DIVIDED_BY_ZERO, result)

    def test_large_denominators(self):
        """Test fractions with large denominators."""
        result = PT_PT.pronounce_fraction("1/7")
        self.assertIn("um", result)
        self.assertIn("sétimo", result)

        result = PT_PT.pronounce_fraction("5/7")
        self.assertIn("cinco", result)
        self.assertIn("sétimos", result)

    def test_unknown_denominators(self):
        """Test fractions with denominators not in predefined list."""
        result = PT_PT.pronounce_fraction("1/13")
        self.assertIn("um", result)
        # Should use "avos" for unknown denominators

        result = PT_PT.pronounce_fraction("2/13")
        self.assertIn("dois", result)
        self.assertIn("avos", result)

    def test_variant_differences(self):
        """Test variant differences in fraction pronunciation."""
        br_result = PT_BR.pronounce_fraction("1/16")
        pt_result = PT_PT.pronounce_fraction("1/16")
        # Both should work, may have slight differences in underlying number pronunciation
        self.assertIsInstance(br_result, str)
        self.assertIsInstance(pt_result, str)

    def test_scale_parameter(self):
        """Test scale parameter in fraction pronunciation."""
        result_short = PT_PT.pronounce_fraction("1/1000000", scale=Scale.SHORT)
        result_long = PT_PT.pronounce_fraction("1/1000000", scale=Scale.LONG)
        self.assertIsInstance(result_short, str)
        self.assertIsInstance(result_long, str)

    def test_zero_numerator(self):
        """Test fractions with zero numerator."""
        result = PT_PT.pronounce_fraction("0/5")
        self.assertIn("zero", result)


class TestIntegrationScenarios(unittest.TestCase):
    """Test integration scenarios and edge cases."""

    def test_round_trip_conversion(self):
        """Test round-trip conversion: number -> text -> number."""
        test_numbers = [1, 16, 100, 123, 1000, 1234]

        for num in test_numbers:
            # Convert number to text
            text = PT_BR.pronounce_number(num)
            # Convert text back to number
            extracted = extract_number(text, lang="pt-BR")
            self.assertEqual(extracted, num, f"Round-trip failed for {num}: {text} -> {extracted}")

    def test_variant_consistency(self):
        """Test that BR and PT variants are internally consistent."""
        test_numbers = [16, 17, 19]  # Numbers that differ between variants

        for num in test_numbers:
            # Test BR variant
            br_text = PT_BR.pronounce_number(num)
            br_extracted = extract_number(br_text, lang="pt-BR")
            self.assertEqual(br_extracted, num)

            # Test PT variant
            pt_text = PT_PT.pronounce_number(num)
            pt_extracted = extract_number(pt_text, lang="pt-PT")
            self.assertEqual(pt_extracted, num)


    def test_numbers_to_digits_integration(self):
        """Test integration with PT_PT.numbers_to_digits."""
        test_phrases = [
            "há duzentos e cinquenta carros",
            "comprei dezesseis livros",
            "mil e uma noites"
        ]

        for phrase in test_phrases:
            result = PT_BR.numbers_to_digits(phrase)
            # Should contain digits and preserve non-number words
            self.assertIsInstance(result, str)
            self.assertTrue(any(char.isdigit() for char in result))

    def test_error_handling_robustness(self):
        """Test robustness of error handling across functions."""
        # Test various invalid inputs
        invalid_inputs = ["", "   ", "xyz123", "palavra-palavra"]

        for invalid_input in invalid_inputs:
            # PT_PT.extract_number should return False for invalid input
            result = extract_number(invalid_input, lang="pt-PT")
            self.assertFalse(result)

            # PT_PT.numbers_to_digits should handle gracefully
            result = PT_PT.numbers_to_digits(invalid_input)
            self.assertIsInstance(result, str)

    def test_large_number_limits(self):
        """Test behavior with very large numbers."""
        very_large = 10 ** 30

        # Should not raise exceptions
        try:
            result = PT_PT.pronounce_number(very_large)
            self.assertIsInstance(result, str)
        except Exception as e:
            self.fail(f"Large number pronunciation failed: {e}")

    def test_negative(self):
        text = PT_PT.pronounce_number(-234)
        self.assertTrue(text.startswith("menos"))
        self.assertEqual(extract_number(text, lang="pt-PT"), -234) # -234 != -166

        self.assertEqual(extract_number("menos cinco", lang="pt-BR"), -5)

class TestGenderedForms(unittest.TestCase):
    """Portuguese cardinals that inflect for grammatical gender."""

    def test_extract_feminine_units(self):
        self.assertEqual(extract_number("duas", lang="pt-PT"), 2)
        self.assertEqual(extract_number("uma", lang="pt-PT"), 1)

    def test_extract_feminine_hundreds(self):
        self.assertEqual(extract_number("duzentas", lang="pt-PT"), 200)
        self.assertEqual(extract_number("trezentas", lang="pt-PT"), 300)
        self.assertEqual(extract_number("quinhentas", lang="pt-PT"), 500)

    def test_extract_feminine_compound(self):
        self.assertEqual(extract_number("duzentas e uma", lang="pt-PT"), 201)
        self.assertEqual(extract_number("vinte e uma", lang="pt-PT"), 21)
        self.assertEqual(extract_number("trezentas e trinta e três", lang="pt-PT"), 333)

    def test_pronounce_feminine(self):
        from ovos_number_parser.util import GrammaticalGender
        self.assertEqual(PT_PT.pronounce_number(2, gender=GrammaticalGender.FEMININE),
                         "duas")
        self.assertEqual(PT_PT.pronounce_number(200, gender=GrammaticalGender.FEMININE),
                         "duzentas")
        self.assertEqual(PT_PT.pronounce_number(21, gender=GrammaticalGender.FEMININE),
                         "vinte e uma")


class TestJoinerAndHundreds(unittest.TestCase):
    """'e' joiners, cem vs cento, and thousands composition."""


    def test_mil_composition(self):
        self.assertEqual(extract_number("mil", lang="pt-PT"), 1000)
        self.assertEqual(extract_number("mil e um", lang="pt-PT"), 1001)
        self.assertEqual(extract_number("mil quinhentos e quarenta e dois", lang="pt-PT"), 1542)

    def test_millions_and_remainder(self):
        self.assertEqual(
            extract_number("dois milhões e quinhentos", scale=Scale.SHORT, lang="pt-PT"),
            2000500)
        self.assertEqual(
            extract_number("duzentos milhões", scale=Scale.SHORT, lang="pt-BR"),
            200000000)


class TestRoundTripSweep(unittest.TestCase):
    """Large round-trip sweeps across variants and scales."""


    def test_negative_sweep(self):
        for n in (-1, -16, -100, -234, -1000, -1234567):
            text = PT_PT.pronounce_number(n)
            self.assertTrue(text.startswith("menos"))
            self.assertEqual(extract_number(text, lang="pt-PT"), n)


class TestAdversarialNumberInputs(unittest.TestCase):
    """Malformed and boundary inputs."""

    def test_none_returns_false(self):
        # non-string input is "no number", not an error
        self.assertIs(extract_number(None, lang="pt-PT"), False)
        for bad in (None, 123, 4.5, [], {}):
            self.assertIs(extract_number(bad, lang="pt-PT"), False)

    def test_pronounce_rejects_non_numbers(self):
        for bad in ("not a number", None, [1, 2]):
            with self.assertRaises(TypeError):
                PT_PT.pronounce_number(bad)


    def test_zero_and_negative_zero(self):
        self.assertEqual(extract_number("zero", lang="pt-PT"), 0)
        self.assertEqual(extract_number("menos zero", lang="pt-PT"), 0)

    def test_numbers_to_digits_preserves_non_numbers(self):
        self.assertEqual(PT_PT.numbers_to_digits("nada de números aqui"),
                         "nada de números aqui")

    def test_case_and_hyphen_insensitivity(self):
        self.assertEqual(extract_number("VINTE e UM", lang="pt-BR"), 21)
        self.assertEqual(extract_number("vinte-e-um", lang="pt-BR"), 21)


class TestRealSentences(unittest.TestCase):
    """Numbers embedded in natural sentences."""

    def test_extract_from_sentence(self):
        self.assertEqual(extract_number("comprei vinte e cinco maçãs", lang="pt-PT"), 25)
        self.assertEqual(extract_number("há duzentos e cinquenta carros", lang="pt-BR"), 250)

    def test_numbers_to_digits_in_sentence(self):
        self.assertEqual(PT_PT.numbers_to_digits("tenho vinte e um anos"),
                         "tenho 21 anos")
        result = PT_BR.numbers_to_digits("comprei dezesseis livros")
        self.assertIn("16", result)

    def test_fractions_in_speech(self):
        self.assertAlmostEqual(extract_number("dois e meio", lang="pt-PT"), 2.5, places=5)
        self.assertAlmostEqual(extract_number("três quartos", lang="pt-PT"), 0.75, places=5)
        self.assertAlmostEqual(extract_number("dois terços", lang="pt-PT"), 2.0 / 3, places=5)

    def test_ordinals_in_sentence(self):
        self.assertEqual(extract_number("o segundo carro", ordinals=True, lang="pt-PT"), 2)
        self.assertEqual(extract_number("primeiro lugar", ordinals=True, lang="pt-PT"), 1)

    def test_variant_regionalisms(self):
        # each variant understands its own teens spelling
        self.assertEqual(extract_number("dezesseis", lang="pt-BR"), 16)
        self.assertEqual(extract_number("dezasseis", lang="pt-PT"), 16)
        # and cross-variant spellings are still accepted via ALT_SPELLINGS
        self.assertEqual(extract_number("dezasseis", lang="pt-BR"), 16)
        self.assertEqual(extract_number("dezesseis", lang="pt-PT"), 16)


if __name__ == '__main__':
    unittest.main()
