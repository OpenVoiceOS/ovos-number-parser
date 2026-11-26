import unittest
from unittest.mock import patch

from ovos_number_parser.util import (
    Token, Scale, tokenize,
    invert_dict, is_numeric, convert_to_mixed_fraction, word_tokenize
)


class TestToken(unittest.TestCase):
    """Test cases for the Token namedtuple."""

    def test_token_creation(self):
        """Test Token namedtuple creation with valid inputs."""
        token = Token("hello", 0)
        self.assertEqual(token.word, "hello")
        self.assertEqual(token.index, 0)

    def test_token_creation_with_different_types(self):
        """Test Token creation with various data types."""
        token_str = Token("world", 1)
        token_num = Token(123, 2)
        token_none = Token(None, 3)

        self.assertEqual(token_str.word, "world")
        self.assertEqual(token_num.word, 123)
        self.assertEqual(token_none.word, None)

    def test_token_immutability(self):
        """Test that Token behaves as an immutable namedtuple."""
        token = Token("test", 0)
        with self.assertRaises(AttributeError):
            token.word = "changed"
        with self.assertRaises(AttributeError):
            token.index = 5

    def test_token_indexing(self):
        """Test Token can be accessed by index like a tuple."""
        token = Token("word", 42)
        self.assertEqual(token[0], "word")
        self.assertEqual(token[1], 42)

    def test_token_iteration(self):
        """Test Token can be iterated over."""
        token = Token("test", 5)
        word, index = token
        self.assertEqual(word, "test")
        self.assertEqual(index, 5)

    def test_token_equality(self):
        """Test Token equality comparison."""
        token1 = Token("hello", 0)
        token2 = Token("hello", 0)
        token3 = Token("world", 0)

        self.assertEqual(token1, token2)
        self.assertNotEqual(token1, token3)

    def test_token_repr(self):
        """Test Token string representation."""
        token = Token("test", 42)
        repr_str = repr(token)
        self.assertIn("Token", repr_str)
        self.assertIn("test", repr_str)
        self.assertIn("42", repr_str)


class TestScale(unittest.TestCase):
    """Test cases for the Scale enum."""

    def test_scale_enum_values(self):
        """Test Scale enum has correct values."""
        self.assertEqual(Scale.SHORT.value, "short")
        self.assertEqual(Scale.LONG.value, "long")

    def test_scale_enum_inheritance(self):
        """Test Scale enum inherits from str and Enum."""
        self.assertIsInstance(Scale.SHORT, str)
        self.assertIsInstance(Scale.LONG, str)

    def test_scale_enum_comparison(self):
        """Test Scale enum string comparison."""
        self.assertEqual(Scale.SHORT, "short")
        self.assertEqual(Scale.LONG, "long")
        self.assertNotEqual(Scale.SHORT, Scale.LONG)

    def test_scale_enum_membership(self):
        """Test Scale enum membership."""
        self.assertIn(Scale.SHORT, Scale)
        self.assertIn(Scale.LONG, Scale)

    def test_scale_enum_iteration(self):
        """Test Scale enum can be iterated."""
        scales = list(Scale)
        self.assertEqual(len(scales), 2)
        self.assertIn(Scale.SHORT, scales)
        self.assertIn(Scale.LONG, scales)

    def test_scale_enum_case_sensitivity(self):
        """Test Scale enum case sensitivity."""
        self.assertNotEqual(Scale.SHORT, "SHORT")
        self.assertNotEqual(Scale.LONG, "LONG")

    def test_scale_enum_hash(self):
        """Test Scale enum can be used as dictionary keys."""
        scale_dict = {Scale.SHORT: "9 digits", Scale.LONG: "12 digits"}
        self.assertEqual(scale_dict[Scale.SHORT], "9 digits")
        self.assertEqual(scale_dict[Scale.LONG], "12 digits")


class TestTokenize(unittest.TestCase):
    """Test cases for the tokenize function."""

    @patch('ovos_number_parser.util.word_tokenize')
    def test_tokenize_basic(self, mock_word_tokenize):
        """Test basic tokenize functionality."""
        mock_word_tokenize.return_value = ["hello", "world"]
        result = tokenize("hello world")

        expected = [Token("hello", 0), Token("world", 1)]
        self.assertEqual(result, expected)
        mock_word_tokenize.assert_called_once_with("hello world")

    @patch('ovos_number_parser.util.word_tokenize')
    def test_tokenize_empty_string(self, mock_word_tokenize):
        """Test tokenize with empty string."""
        mock_word_tokenize.return_value = []
        result = tokenize("")

        self.assertEqual(result, [])
        mock_word_tokenize.assert_called_once_with("")

    @patch('ovos_number_parser.util.word_tokenize')
    def test_tokenize_single_word(self, mock_word_tokenize):
        """Test tokenize with single word."""
        mock_word_tokenize.return_value = ["hello"]
        result = tokenize("hello")

        expected = [Token("hello", 0)]
        self.assertEqual(result, expected)

    @patch('ovos_number_parser.util.word_tokenize')
    def test_tokenize_special_characters(self, mock_word_tokenize):
        """Test tokenize with special characters."""
        mock_word_tokenize.return_value = ["hello", ",", "world", "!"]
        result = tokenize("hello, world!")

        expected = [Token("hello", 0), Token(",", 1), Token("world", 2), Token("!", 3)]
        self.assertEqual(result, expected)

    @patch('ovos_number_parser.util.word_tokenize')
    def test_tokenize_numbers(self, mock_word_tokenize):
        """Test tokenize with numeric strings."""
        mock_word_tokenize.return_value = ["I", "have", "5", "apples"]
        result = tokenize("I have 5 apples")

        expected = [Token("I", 0), Token("have", 1), Token("5", 2), Token("apples", 3)]
        self.assertEqual(result, expected)

    @patch('ovos_number_parser.util.word_tokenize')
    def test_tokenize_preserves_order(self, mock_word_tokenize):
        """Test tokenize preserves word order and assigns correct indices."""
        mock_word_tokenize.return_value = ["first", "second", "third", "fourth"]
        result = tokenize("first second third fourth")

        for i, token in enumerate(result):
            self.assertEqual(token.index, i)

    def test_tokenize_function_exists(self):
        """Test that tokenize function exists and is callable."""
        self.assertTrue(callable(tokenize))


class TestInvertDict(unittest.TestCase):
    """Test cases for the invert_dict function."""

    def test_invert_dict_basic(self):
        """Test basic invert_dict functionality."""
        original = {"a": 1, "b": 2, "c": 3}
        result = invert_dict(original)
        expected = {1: "a", 2: "b", 3: "c"}
        self.assertEqual(result, expected)

    def test_invert_dict_empty(self):
        """Test invert_dict with empty dictionary."""
        original = {}
        result = invert_dict(original)
        expected = {}
        self.assertEqual(result, expected)

    def test_invert_dict_single_item(self):
        """Test invert_dict with single item dictionary."""
        original = {"key": "value"}
        result = invert_dict(original)
        expected = {"value": "key"}
        self.assertEqual(result, expected)

    def test_invert_dict_numeric_keys_string_values(self):
        """Test invert_dict with numeric keys and string values."""
        original = {1: "one", 2: "two", 3: "three"}
        result = invert_dict(original)
        expected = {"one": 1, "two": 2, "three": 3}
        self.assertEqual(result, expected)

    def test_invert_dict_mixed_types(self):
        """Test invert_dict with mixed key-value types."""
        original = {"str_key": 1, 2: "str_value", "another": 3.14}
        result = invert_dict(original)
        expected = {1: "str_key", "str_value": 2, 3.14: "another"}
        self.assertEqual(result, expected)

    def test_invert_dict_duplicate_values_behavior(self):
        """Test invert_dict behavior with duplicate values."""
        original = {"a": 1, "b": 1, "c": 2}
        result = invert_dict(original)

        # Due to dict iteration order, one of "a" or "b" will be the final value for key 1
        self.assertEqual(len(result), 2)
        self.assertIn(1, result)
        self.assertIn(2, result)
        self.assertEqual(result[2], "c")
        self.assertIn(result[1], ["a", "b"])

    def test_invert_dict_none_values(self):
        """Test invert_dict with None values."""
        original = {"key1": None, "key2": "value"}
        result = invert_dict(original)
        expected = {None: "key1", "value": "key2"}
        self.assertEqual(result, expected)

    def test_invert_dict_tuple_values(self):
        """Test invert_dict with tuple values (hashable)."""
        original = {"key1": (1, 2), "key2": (3, 4)}
        result = invert_dict(original)
        expected = {(1, 2): "key1", (3, 4): "key2"}
        self.assertEqual(result, expected)

    def test_invert_dict_boolean_values(self):
        """Test invert_dict with boolean values."""
        original = {"true_key": True, "false_key": False}
        result = invert_dict(original)
        expected = {True: "true_key", False: "false_key"}
        self.assertEqual(result, expected)

    def test_invert_dict_comprehension_equivalent(self):
        """Test invert_dict produces same result as dict comprehension."""
        original = {"x": 10, "y": 20, "z": 30}
        result = invert_dict(original)
        expected = {v: k for k, v in original.items()}
        self.assertEqual(result, expected)


class TestIsNumeric(unittest.TestCase):
    """Test cases for the is_numeric function."""

    def test_is_numeric_integer_strings(self):
        """Test is_numeric with integer strings."""
        self.assertTrue(is_numeric("123"))
        self.assertTrue(is_numeric("-456"))
        self.assertTrue(is_numeric("0"))
        self.assertTrue(is_numeric("+789"))

    def test_is_numeric_float_strings(self):
        """Test is_numeric with float strings."""
        self.assertTrue(is_numeric("123.45"))
        self.assertTrue(is_numeric("-67.89"))
        self.assertTrue(is_numeric("0.0"))
        self.assertTrue(is_numeric(".5"))
        self.assertTrue(is_numeric("5."))
        self.assertTrue(is_numeric("+3.14"))

    def test_is_numeric_scientific_notation(self):
        """Test is_numeric with scientific notation."""
        self.assertTrue(is_numeric("1e5"))
        self.assertTrue(is_numeric("1.5e-3"))
        self.assertTrue(is_numeric("-2.5E+10"))
        self.assertTrue(is_numeric("1E0"))

    def test_is_numeric_special_float_values(self):
        """Non-finite tokens carry no usable number and are rejected."""
        self.assertFalse(is_numeric("inf"))
        self.assertFalse(is_numeric("-inf"))
        self.assertFalse(is_numeric("nan"))
        self.assertFalse(is_numeric("infinity"))
        self.assertFalse(is_numeric("-infinity"))
        # a digit string that overflows float to inf is still an exact integer
        self.assertTrue(is_numeric("9" * 400))
        # scientific notation that overflows to inf is not a usable number
        self.assertFalse(is_numeric("1e309"))

    def test_is_numeric_non_numeric_strings(self):
        """Test is_numeric with non-numeric strings."""
        self.assertFalse(is_numeric("abc"))
        self.assertFalse(is_numeric("12.34.56"))
        self.assertFalse(is_numeric(""))
        self.assertFalse(is_numeric(" "))
        self.assertFalse(is_numeric("123abc"))
        self.assertFalse(is_numeric("abc123"))
        self.assertFalse(is_numeric("12 34"))

    def test_is_numeric_edge_cases(self):
        """Test is_numeric with edge cases."""
        self.assertFalse(is_numeric("--5"))
        self.assertFalse(is_numeric("++5"))
        self.assertFalse(is_numeric("5-"))
        self.assertFalse(is_numeric("5+"))
        self.assertFalse(is_numeric("..5"))
        self.assertFalse(is_numeric("5.."))
        self.assertFalse(is_numeric("e5"))
        self.assertFalse(is_numeric("5e"))

    def test_is_numeric_whitespace(self):
        """Test is_numeric with whitespace."""
        self.assertTrue(is_numeric("  123  "))  # Leading/trailing whitespace is handled by float()
        self.assertFalse(is_numeric("1 2 3"))  # Internal whitespace is not valid
        self.assertTrue(is_numeric("\t42\n"))  # Tab and newline are handled

    def test_is_numeric_hexadecimal(self):
        """Test is_numeric with hexadecimal strings."""
        self.assertFalse(is_numeric("0x1A"))  # Hex not supported by float()
        self.assertFalse(is_numeric("0xFF"))

    def test_is_numeric_octal_binary(self):
        """Test is_numeric with octal and binary strings."""
        self.assertFalse(is_numeric("0o777"))  # Octal not supported by float()
        self.assertFalse(is_numeric("0b1010"))  # Binary not supported by float()

    def test_is_numeric_unicode_digits(self):
        """Test is_numeric with unicode digit characters."""
        self.assertTrue(is_numeric("１２３"))  # Unicode digits are supported by float()

    def test_is_numeric_currency_symbols(self):
        """Test is_numeric with currency symbols."""
        self.assertFalse(is_numeric("$123"))
        self.assertFalse(is_numeric("€456"))
        self.assertFalse(is_numeric("123%"))


class TestConvertToMixedFraction(unittest.TestCase):
    """Test cases for the convert_to_mixed_fraction function."""

    def test_convert_whole_numbers(self):
        """Test convert_to_mixed_fraction with whole numbers."""
        result = convert_to_mixed_fraction(5.0)
        self.assertEqual(result, (5, 0, 1))

        result = convert_to_mixed_fraction(0.0)
        self.assertEqual(result, (0, 0, 1))

        result = convert_to_mixed_fraction(-3.0)
        self.assertEqual(result, (-3, 0, 1))

    def test_convert_simple_fractions(self):
        """Test convert_to_mixed_fraction with simple fractions."""
        result = convert_to_mixed_fraction(0.5)
        self.assertEqual(result, (0, 1, 2))

        result = convert_to_mixed_fraction(0.25)
        self.assertEqual(result, (0, 1, 4))

        result = convert_to_mixed_fraction(0.75)
        self.assertEqual(result, (0, 3, 4))

    def test_convert_mixed_fractions(self):
        """Test convert_to_mixed_fraction with mixed numbers."""
        result = convert_to_mixed_fraction(2.5)
        self.assertEqual(result, (2, 1, 2))

        result = convert_to_mixed_fraction(3.25)
        self.assertEqual(result, (3, 1, 4))

        result = convert_to_mixed_fraction(1.75)
        self.assertEqual(result, (1, 3, 4))

    def test_convert_negative_mixed_fractions(self):
        """Test convert_to_mixed_fraction with negative mixed numbers."""
        result = convert_to_mixed_fraction(-2.5)
        self.assertEqual(result, (-2, 1, 2))

        result = convert_to_mixed_fraction(-1.25)
        self.assertEqual(result, (-1, 1, 4))

    def test_convert_with_custom_denominators(self):
        """Test convert_to_mixed_fraction with custom denominators."""
        # Only allow denominators 2, 3, 4
        result = convert_to_mixed_fraction(0.5, denominators=[2, 3, 4])
        self.assertEqual(result, (0, 1, 2))

        result = convert_to_mixed_fraction(1.0 / 3, denominators=[2, 3, 4])
        self.assertEqual(result, (0, 1, 3))

    def test_convert_no_good_approximation(self):
        """Test convert_to_mixed_fraction when no good approximation exists."""
        # Use very limited denominators that can't represent 1/7 well
        result = convert_to_mixed_fraction(1.0 / 7, denominators=[2, 3])
        self.assertIsNone(result)

    def test_convert_empty_denominators(self):
        """Test convert_to_mixed_fraction with empty denominators list."""
        # Should use default range(1, 21)
        result = convert_to_mixed_fraction(0.5, denominators=[])
        self.assertEqual(result, (0, 1, 2))

    def test_convert_none_denominators(self):
        """Test convert_to_mixed_fraction with None denominators."""
        # Should use default range(1, 21)
        result = convert_to_mixed_fraction(0.5, denominators=None)
        self.assertEqual(result, (0, 1, 2))

    def test_convert_close_to_whole_number(self):
        """Test convert_to_mixed_fraction with numbers very close to whole numbers."""
        # 4.500002 should become 4 1/2 due to the 0.01 accuracy threshold
        result = convert_to_mixed_fraction(4.500002)
        self.assertEqual(result, (4, 1, 2))

        # Test number very close to 5
        result = convert_to_mixed_fraction(4.9999)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 4)  # Whole part should be 4

    def test_convert_accuracy_threshold(self):
        """Test convert_to_mixed_fraction accuracy threshold behavior."""
        # Test a value that's close to 1/3 but not exact
        result = convert_to_mixed_fraction(1.0 / 3 + 0.001)  # Slightly off from 1/3
        # Should still find a reasonable approximation
        self.assertIsNotNone(result)

    def test_convert_large_denominators(self):
        """Test convert_to_mixed_fraction with large denominators."""
        result = convert_to_mixed_fraction(0.05, denominators=range(1, 30))
        self.assertIsNotNone(result)
        self.assertEqual(result, (0, 1, 20))  # 1/20 = 0.05

    def test_convert_edge_case_very_small_fraction(self):
        """Test convert_to_mixed_fraction with very small fractional parts."""
        result = convert_to_mixed_fraction(5.00001)
        # Should be treated as whole number due to accuracy threshold
        self.assertEqual(result, (5, 0, 1))

    def test_convert_repeating_decimals(self):
        """Test convert_to_mixed_fraction with repeating decimals."""
        # 1/3 = 0.333...
        result = convert_to_mixed_fraction(1.0 / 3)
        self.assertEqual(result, (0, 1, 3))

        # 2/3 = 0.666...
        result = convert_to_mixed_fraction(2.0 / 3)
        self.assertEqual(result, (0, 2, 3))

    def test_convert_single_denominator(self):
        """Test convert_to_mixed_fraction with single denominator."""
        result = convert_to_mixed_fraction(0.5, denominators=[2])
        self.assertEqual(result, (0, 1, 2))

        # Should return None if the single denominator can't represent the fraction well
        result = convert_to_mixed_fraction(1.0 / 3, denominators=[2])
        self.assertIsNone(result)

    def test_convert_large_whole_numbers(self):
        """Test convert_to_mixed_fraction with large whole numbers."""
        result = convert_to_mixed_fraction(1000.0)
        self.assertEqual(result, (1000, 0, 1))

        result = convert_to_mixed_fraction(1000.25)
        self.assertEqual(result, (1000, 1, 4))

    def test_convert_complex_fractions(self):
        """Test convert_to_mixed_fraction with complex fractions."""
        # Test fifths
        result = convert_to_mixed_fraction(0.2)  # 1/5
        self.assertEqual(result, (0, 1, 5))

        result = convert_to_mixed_fraction(0.6)  # 3/5
        self.assertEqual(result, (0, 3, 5))

        # Test sixths
        result = convert_to_mixed_fraction(1.0 / 6)
        self.assertEqual(result, (0, 1, 6))

    def test_convert_edge_denominator_boundary(self):
        """Test convert_to_mixed_fraction at denominator boundaries."""
        # Test with denominator exactly at boundary (20 in default range)
        result = convert_to_mixed_fraction(1.0 / 20)
        self.assertEqual(result, (0, 1, 20))

        # Test with fraction that would need denominator > 20
        result = convert_to_mixed_fraction(1.0 / 25, denominators=range(1, 21))
        # Should not find good approximation with default range
        self.assertIsNone(result)



class TestWordTokenize(unittest.TestCase):
    """Test tokenize function."""

    def test_basic_tokenization(self):
        """Test basic word tokenization."""
        result = word_tokenize("palavra uma palavra duas")
        expected = ["palavra", "uma", "palavra", "duas"]
        self.assertEqual(result, expected)

    def test_percentage_split(self):
        """Test splitting percentages."""
        result = word_tokenize("12%")
        self.assertEqual(result, ["12", "%"])

    def test_hash_number_split(self):
        """Test splitting hash with numbers."""
        result = word_tokenize("#1")
        self.assertEqual(result, ["#", "1"])

    def test_hyphen_between_words(self):
        """Test hyphen handling between words."""
        result = word_tokenize("amo-te")
        self.assertEqual(result, ["amo", "-", "te"])

    def test_hyphen_preservation_in_numbers(self):
        """Test that hyphens in numbers are preserved."""
        result = word_tokenize("1-2")
        # Should not split number ranges
        self.assertIn("1-2", result)

    def test_trailing_hyphen_removal(self):
        """Test removal of trailing hyphens."""
        result = word_tokenize("palavra -")
        self.assertEqual(result, ["palavra"])

    def test_empty_string(self):
        """Test tokenization of empty string."""
        result = word_tokenize("")
        self.assertEqual(result, [])

    def test_whitespace_handling(self):
        """Test handling of various whitespace."""
        result = word_tokenize("  palavra   outra  ")
        self.assertEqual(result, ["palavra", "outra"])

    def test_complex_input(self):
        """Test complex input with multiple patterns."""
        result = word_tokenize("amo-te 50% #2 test")
        expected_elements = ["amo", "-", "te", "50", "%", "#", "2", "test"]
        self.assertEqual(result, expected_elements)


class TestRomanceNumberExtractorNonDecimalUnicodeDigits(unittest.TestCase):
    """Regression: RomanceNumberExtractor backs pt/es/ca/it/gl/an/ast/mwl/oc/ro.

    Superscripts (¹²³) and vulgar fractions (½) are digit-like
    (str.isdigit()/isnumeric() is True) but float()/int() reject them; the
    "digit token" fast path must not raise ValueError. Arabic-Indic digits
    (real decimal digits, str.isdecimal() is True) must keep working.
    """

    def test_superscripts_and_vulgar_fractions_do_not_crash(self):
        from ovos_number_parser import extract_number
        for lang in ("pt", "es", "ca", "it", "gl", "an", "ast", "mwl", "oc", "ro"):
            for text in ("¹", "²", "³", "½"):
                with self.subTest(lang=lang, text=text):
                    self.assertFalse(extract_number(text, lang=lang))

    def test_arabic_indic_digits_still_work(self):
        from ovos_number_parser import extract_number
        for lang in ("pt", "es", "ca", "it", "gl", "an", "ast", "mwl", "oc", "ro"):
            with self.subTest(lang=lang):
                self.assertEqual(extract_number('١', lang=lang), 1)
                self.assertEqual(extract_number('٢', lang=lang), 2)


if __name__ == '__main__':
    # Run the tests with verbose output
    unittest.main(verbosity=2)
