import unittest
from unittest.mock import patch

from ovos_number_parser.util import (
    Token, Scale, ReplaceableNumber, tokenize, partition_list,
    invert_dict, is_numeric, look_for_fractions, convert_to_mixed_fraction
)


class TestToken(unittest.TestCase):
    """Test cases for the Token namedtuple."""

    def test_token_creation(self):
        """
        Test that a Token namedtuple is created correctly with valid word and index values.
        """
        token = Token("hello", 0)
        self.assertEqual(token.word, "hello")
        self.assertEqual(token.index, 0)

    def test_token_creation_with_different_types(self):
        """
        Test that Token instances can be created with string, numeric, and None values, and that their fields are set correctly.
        """
        token_str = Token("world", 1)
        token_num = Token(123, 2)
        token_none = Token(None, 3)

        self.assertEqual(token_str.word, "world")
        self.assertEqual(token_num.word, 123)
        self.assertEqual(token_none.word, None)

    def test_token_immutability(self):
        """
        Test that Token instances are immutable and do not allow attribute reassignment.
        """
        token = Token("test", 0)
        with self.assertRaises(AttributeError):
            token.word = "changed"
        with self.assertRaises(AttributeError):
            token.index = 5

    def test_token_indexing(self):
        """
        Test that Token instances support tuple-like indexing to access their fields.
        """
        token = Token("word", 42)
        self.assertEqual(token[0], "word")
        self.assertEqual(token[1], 42)

    def test_token_iteration(self):
        """
        Test that a Token instance supports iteration and yields its word and index in order.
        """
        token = Token("test", 5)
        word, index = token
        self.assertEqual(word, "test")
        self.assertEqual(index, 5)

    def test_token_equality(self):
        """
        Test that Token instances with identical values are equal and those with differing values are not.
        """
        token1 = Token("hello", 0)
        token2 = Token("hello", 0)
        token3 = Token("world", 0)

        self.assertEqual(token1, token2)
        self.assertNotEqual(token1, token3)

    def test_token_repr(self):
        """
        Test that the string representation of a Token includes the class name and field values.
        """
        token = Token("test", 42)
        repr_str = repr(token)
        self.assertIn("Token", repr_str)
        self.assertIn("test", repr_str)
        self.assertIn("42", repr_str)


class TestScale(unittest.TestCase):
    """Test cases for the Scale enum."""

    def test_scale_enum_values(self):
        """
        Test that the Scale enum members have the expected string values.
        """
        self.assertEqual(Scale.SHORT.value, "short")
        self.assertEqual(Scale.LONG.value, "long")

    def test_scale_enum_inheritance(self):
        """
        Test that the Scale enum members are instances of both str and Enum.
        """
        self.assertIsInstance(Scale.SHORT, str)
        self.assertIsInstance(Scale.LONG, str)

    def test_scale_enum_comparison(self):
        """
        Test that Scale enum members compare correctly to their string values and to each other.
        """
        self.assertEqual(Scale.SHORT, "short")
        self.assertEqual(Scale.LONG, "long")
        self.assertNotEqual(Scale.SHORT, Scale.LONG)

    def test_scale_enum_membership(self):
        """
        Verify that the Scale enum contains the SHORT and LONG members.
        """
        self.assertIn(Scale.SHORT, Scale)
        self.assertIn(Scale.LONG, Scale)

    def test_scale_enum_iteration(self):
        """
        Test that the Scale enum can be iterated and contains both SHORT and LONG members.
        """
        scales = list(Scale)
        self.assertEqual(len(scales), 2)
        self.assertIn(Scale.SHORT, scales)
        self.assertIn(Scale.LONG, scales)

    def test_scale_enum_case_sensitivity(self):
        """
        Verify that the Scale enum members are case-sensitive and do not equal their uppercase string representations.
        """
        self.assertNotEqual(Scale.SHORT, "SHORT")
        self.assertNotEqual(Scale.LONG, "LONG")

    def test_scale_enum_hash(self):
        """
        Test that Scale enum members are hashable and can be used as dictionary keys.
        """
        scale_dict = {Scale.SHORT: "9 digits", Scale.LONG: "12 digits"}
        self.assertEqual(scale_dict[Scale.SHORT], "9 digits")
        self.assertEqual(scale_dict[Scale.LONG], "12 digits")


class TestReplaceableNumber(unittest.TestCase):
    """Test cases for the ReplaceableNumber class."""

    def setUp(self):
        """
        Initialize sample Token instances and a token list for use in ReplaceableNumber tests.
        """
        self.token1 = Token("one", 0)
        self.token2 = Token("hundred", 1)
        self.token3 = Token("twenty", 2)
        self.tokens = [self.token1, self.token2, self.token3]

    def test_init_basic(self):
        """
        Test that ReplaceableNumber initializes correctly with a value and tokens.
        """
        rn = ReplaceableNumber(100, self.tokens)
        self.assertEqual(rn.value, 100)
        self.assertEqual(rn.tokens, self.tokens)

    def test_init_with_none_value(self):
        """
        Test that initializing ReplaceableNumber with a None value sets the value to None and retains the provided tokens.
        """
        rn = ReplaceableNumber(None, self.tokens)
        self.assertIsNone(rn.value)
        self.assertEqual(rn.tokens, self.tokens)

    def test_init_with_false_value(self):
        """
        Test that initializing ReplaceableNumber with a False value sets the value to False and retains the provided tokens.
        """
        rn = ReplaceableNumber(False, self.tokens)
        self.assertFalse(rn.value)
        self.assertEqual(rn.tokens, self.tokens)

    def test_init_with_zero_value(self):
        """
        Test that initializing ReplaceableNumber with a value of zero correctly sets the value and tokens.
        """
        rn = ReplaceableNumber(0, self.tokens)
        self.assertEqual(rn.value, 0)
        self.assertEqual(rn.tokens, self.tokens)

    def test_init_with_float_value(self):
        """
        Test that ReplaceableNumber initializes correctly with a float value and associated tokens.
        """
        rn = ReplaceableNumber(3.14, self.tokens)
        self.assertEqual(rn.value, 3.14)
        self.assertEqual(rn.tokens, self.tokens)

    def test_bool_method_truthy(self):
        """
        Test that ReplaceableNumber instances with non-None, non-False values evaluate as True in boolean contexts.
        """
        rn_positive = ReplaceableNumber(100, self.tokens)
        rn_negative = ReplaceableNumber(-50, self.tokens)
        rn_zero = ReplaceableNumber(0, self.tokens)
        rn_float = ReplaceableNumber(3.14, self.tokens)

        self.assertTrue(bool(rn_positive))
        self.assertTrue(bool(rn_negative))
        self.assertTrue(bool(rn_zero))
        self.assertTrue(bool(rn_float))

    def test_bool_method_falsy(self):
        """
        Test that the __bool__ method of ReplaceableNumber returns False for None and False values.
        """
        rn_none = ReplaceableNumber(None, self.tokens)
        rn_false = ReplaceableNumber(False, self.tokens)

        self.assertFalse(bool(rn_none))
        self.assertFalse(bool(rn_false))

    def test_start_index_property(self):
        """
        Test that the start_index property of ReplaceableNumber returns the index of the first token.
        """
        rn = ReplaceableNumber(100, self.tokens)
        self.assertEqual(rn.start_index, 0)

    def test_end_index_property(self):
        """
        Test that the end_index property of ReplaceableNumber returns the index of the last token.
        """
        rn = ReplaceableNumber(100, self.tokens)
        self.assertEqual(rn.end_index, 2)

    def test_start_end_index_single_token(self):
        """
        Test that `start_index` and `end_index` properties return the correct index for a `ReplaceableNumber` initialized with a single token.
        """
        single_token = [Token("five", 5)]
        rn = ReplaceableNumber(5, single_token)
        self.assertEqual(rn.start_index, 5)
        self.assertEqual(rn.end_index, 5)

    def test_start_end_index_non_sequential_tokens(self):
        """
        Test that `start_index` and `end_index` properties of `ReplaceableNumber` return the correct minimum and maximum indices when tokens have non-sequential indices.
        """
        tokens = [Token("ten", 5), Token("thousand", 10), Token("five", 15)]
        rn = ReplaceableNumber(10005, tokens)
        self.assertEqual(rn.start_index, 5)
        self.assertEqual(rn.end_index, 15)

    def test_text_property(self):
        """
        Test that the `text` property of `ReplaceableNumber` returns the concatenated words from its tokens.
        """
        rn = ReplaceableNumber(120, self.tokens)
        self.assertEqual(rn.text, "one hundred twenty")

    def test_text_property_single_token(self):
        """
        Test that the text property returns the word of a single token in ReplaceableNumber.
        """
        single_token = [Token("five", 5)]
        rn = ReplaceableNumber(5, single_token)
        self.assertEqual(rn.text, "five")

    def test_text_property_empty_tokens(self):
        """
        Test that the text property of ReplaceableNumber returns an empty string when initialized with an empty tokens list.
        """
        rn = ReplaceableNumber(0, [])
        self.assertEqual(rn.text, "")

    def test_text_property_with_none_words(self):
        """
        Test that the text property of ReplaceableNumber skips tokens with None as their word.
        
        Verifies that when tokens contain None for the word attribute, the text property concatenates only the valid words.
        """
        tokens_with_none = [Token(None, 0), Token("test", 1)]
        rn = ReplaceableNumber(5, tokens_with_none)
        self.assertEqual(rn.text, "test")

    def test_text_property_with_numeric_words(self):
        """
        Test that the text property concatenates token words correctly when tokens include numeric values.
        """
        tokens_with_nums = [Token(1, 0), Token("and", 1), Token(2, 2)]
        rn = ReplaceableNumber(3, tokens_with_nums)
        self.assertEqual(rn.text, "1 and 2")

    def test_immutability_enforcement(self):
        """
        Test that the ReplaceableNumber instance raises an exception when attempting to reassign existing attributes, enforcing immutability.
        """
        rn = ReplaceableNumber(100, self.tokens)

        # Attempting to reassign existing attributes should raise exception
        with self.assertRaises(Exception) as context:
            rn.value = 200
        self.assertEqual(str(context.exception), "Immutable!")

        with self.assertRaises(Exception) as context:
            rn.tokens = []
        self.assertEqual(str(context.exception), "Immutable!")

    def test_new_attribute_assignment(self):
        """
        Test that a new attribute can be assigned to a ReplaceableNumber instance once, after which it becomes immutable and further assignment raises an exception.
        """
        rn = ReplaceableNumber(100, self.tokens)
        rn.new_attr = "test"
        self.assertEqual(rn.new_attr, "test")

        # But then it becomes immutable
        with self.assertRaises(Exception) as context:
            rn.new_attr = "changed"
        self.assertEqual(str(context.exception), "Immutable!")

    def test_str_method(self):
        """
        Test that the __str__ method of ReplaceableNumber includes the value and token information in its output.
        """
        rn = ReplaceableNumber(100, self.tokens)
        result = str(rn)
        self.assertIn("100", result)
        self.assertIn("Token", result)

    def test_repr_method(self):
        """
        Test that the `__repr__` method of `ReplaceableNumber` includes the class name, value, and token information in its output.
        """
        rn = ReplaceableNumber(100, self.tokens)
        result = repr(rn)
        self.assertIn("ReplaceableNumber", result)
        self.assertIn("100", result)
        self.assertIn("Token", result)

    def test_edge_case_empty_tokens_list(self):
        """
        Test that accessing start_index or end_index on a ReplaceableNumber with an empty tokens list raises IndexError.
        """
        with self.assertRaises(IndexError):
            rn = ReplaceableNumber(100, [])
            _ = rn.start_index  # Should raise IndexError

        with self.assertRaises(IndexError):
            rn = ReplaceableNumber(100, [])
            _ = rn.end_index  # Should raise IndexError

    def test_multiple_new_attributes(self):
        """
        Test that multiple new attributes can be assigned to a ReplaceableNumber instance and that each becomes immutable after initial assignment.
        """
        rn = ReplaceableNumber(50, self.tokens)
        rn.attr1 = "first"
        rn.attr2 = "second"

        self.assertEqual(rn.attr1, "first")
        self.assertEqual(rn.attr2, "second")

        # Both should become immutable
        with self.assertRaises(Exception):
            rn.attr1 = "changed"
        with self.assertRaises(Exception):
            rn.attr2 = "changed"

    def test_immutability_with_property_access(self):
        """
        Verify that property access on ReplaceableNumber remains functional despite immutability, while direct attribute assignment raises an exception.
        """
        rn = ReplaceableNumber(100, self.tokens)

        # Property access should work normally
        self.assertEqual(rn.start_index, 0)
        self.assertEqual(rn.end_index, 2)
        self.assertEqual(rn.text, "one hundred twenty")

        # But direct attribute assignment should still fail
        with self.assertRaises(Exception):
            rn.value = 200


class TestTokenize(unittest.TestCase):
    """Test cases for the tokenize function."""

    @patch('ovos_number_parser.util.word_tokenize')
    def test_tokenize_basic(self, mock_word_tokenize):
        """
        Test that `tokenize` returns a list of Token objects with correct words and indices for a simple input string.
        """
        mock_word_tokenize.return_value = ["hello", "world"]
        result = tokenize("hello world")

        expected = [Token("hello", 0), Token("world", 1)]
        self.assertEqual(result, expected)
        mock_word_tokenize.assert_called_once_with("hello world")

    @patch('ovos_number_parser.util.word_tokenize')
    def test_tokenize_empty_string(self, mock_word_tokenize):
        """
        Test that `tokenize` returns an empty list when given an empty string.
        """
        mock_word_tokenize.return_value = []
        result = tokenize("")

        self.assertEqual(result, [])
        mock_word_tokenize.assert_called_once_with("")

    @patch('ovos_number_parser.util.word_tokenize')
    def test_tokenize_single_word(self, mock_word_tokenize):
        """
        Test that the `tokenize` function returns a single `Token` for a single-word input.
        """
        mock_word_tokenize.return_value = ["hello"]
        result = tokenize("hello")

        expected = [Token("hello", 0)]
        self.assertEqual(result, expected)

    @patch('ovos_number_parser.util.word_tokenize')
    def test_tokenize_special_characters(self, mock_word_tokenize):
        """
        Test that the tokenize function correctly handles input strings containing special characters, ensuring each character is tokenized as a separate token.
        """
        mock_word_tokenize.return_value = ["hello", ",", "world", "!"]
        result = tokenize("hello, world!")

        expected = [Token("hello", 0), Token(",", 1), Token("world", 2), Token("!", 3)]
        self.assertEqual(result, expected)

    @patch('ovos_number_parser.util.word_tokenize')
    def test_tokenize_numbers(self, mock_word_tokenize):
        """
        Tests that the `tokenize` function correctly tokenizes a string containing numeric values into a list of `Token` objects with appropriate words and indices.
        """
        mock_word_tokenize.return_value = ["I", "have", "5", "apples"]
        result = tokenize("I have 5 apples")

        expected = [Token("I", 0), Token("have", 1), Token("5", 2), Token("apples", 3)]
        self.assertEqual(result, expected)

    @patch('ovos_number_parser.util.word_tokenize')
    def test_tokenize_preserves_order(self, mock_word_tokenize):
        """
        Test that the tokenize function preserves the original word order and assigns sequential indices to each token.
        """
        mock_word_tokenize.return_value = ["first", "second", "third", "fourth"]
        result = tokenize("first second third fourth")

        for i, token in enumerate(result):
            self.assertEqual(token.index, i)

    def test_tokenize_function_exists(self):
        """
        Verify that the `tokenize` function is defined and can be called.
        """
        self.assertTrue(callable(tokenize))


class TestPartitionList(unittest.TestCase):
    """Test cases for the partition_list function."""

    def test_partition_list_basic(self):
        """
        Test that partition_list splits a list into sublists at elements matching a condition.
        
        Verifies that the function correctly partitions the input list when a specific value is encountered.
        """
        items = [1, 2, 3, 4, 5]
        result = partition_list(items, lambda x: x == 3)
        expected = [[1, 2], [3], [4, 5]]
        self.assertEqual(result, expected)

    def test_partition_list_no_matches(self):
        """
        Test that partition_list returns the entire list as a single sublist when no elements match the split condition.
        """
        items = [1, 2, 3, 4, 5]
        result = partition_list(items, lambda x: x == 10)
        expected = [[1, 2, 3, 4, 5]]
        self.assertEqual(result, expected)

    def test_partition_list_all_matches(self):
        """
        Test that partition_list splits a list into single-item sublists when all elements match the split condition.
        """
        items = [1, 1, 1]
        result = partition_list(items, lambda x: x == 1)
        expected = [[1], [1], [1]]
        self.assertEqual(result, expected)

    def test_partition_list_empty_list(self):
        """
        Test that partition_list returns an empty list when given an empty input list.
        """
        items = []
        result = partition_list(items, lambda x: x == 1)
        expected = []
        self.assertEqual(result, expected)

    def test_partition_list_first_item_matches(self):
        """
        Test that partition_list correctly splits the list when the first item matches the condition.
        """
        items = [1, 2, 3, 4]
        result = partition_list(items, lambda x: x == 1)
        expected = [[1], [2, 3, 4]]
        self.assertEqual(result, expected)

    def test_partition_list_last_item_matches(self):
        """
        Test that partition_list correctly splits a list when the last item matches the condition.
        """
        items = [1, 2, 3, 4]
        result = partition_list(items, lambda x: x == 4)
        expected = [[1, 2, 3], [4]]
        self.assertEqual(result, expected)

    def test_partition_list_multiple_consecutive_matches(self):
        """
        Test that partition_list correctly splits a list at consecutive matching elements.
        
        Verifies that consecutive items matching the condition each result in their own partition.
        """
        items = [1, 2, 2, 3, 4]
        result = partition_list(items, lambda x: x == 2)
        expected = [[1], [2], [2], [3, 4]]
        self.assertEqual(result, expected)

    def test_partition_list_strings(self):
        """
        Test that partition_list correctly splits a list of strings at elements matching a specific value.
        """
        items = ["a", "b", "separator", "c", "d"]
        result = partition_list(items, lambda x: x == "separator")
        expected = [["a", "b"], ["separator"], ["c", "d"]]
        self.assertEqual(result, expected)

    def test_partition_list_complex_condition(self):
        """
        Test that partition_list correctly splits a list into sublists using a complex condition function.
        
        Verifies that the list is partitioned at elements where the condition (divisible by 3) is met, resulting in expected sublists.
        """
        items = [1, 2, 3, 4, 5, 6, 7, 8]
        result = partition_list(items, lambda x: x % 3 == 0)
        expected = [[1, 2], [3], [4, 5], [6], [7, 8]]
        self.assertEqual(result, expected)

    def test_partition_list_boolean_condition(self):
        """
        Test that partition_list correctly splits a list of boolean values at each occurrence of False.
        """
        items = [True, False, True, True, False]
        result = partition_list(items, lambda x: x is False)
        expected = [[True], [False], [True, True], [False]]
        self.assertEqual(result, expected)

    def test_partition_list_filters_empty_sublists(self):
        """
        Test that partition_list excludes empty sublists when partitioning a list.
        """
        items = [1, 1, 2, 1]
        result = partition_list(items, lambda x: x == 1)
        # Should not include empty lists
        for sublist in result:
            self.assertGreater(len(sublist), 0)

    def test_partition_list_with_none_items(self):
        """
        Test that partition_list correctly splits a list at None items, treating each None as its own partition.
        """
        items = [1, None, 2, None, 3]
        result = partition_list(items, lambda x: x is None)
        expected = [[1], [None], [2], [None], [3]]
        self.assertEqual(result, expected)


class TestInvertDict(unittest.TestCase):
    """Test cases for the invert_dict function."""

    def test_invert_dict_basic(self):
        """
        Test that invert_dict correctly swaps keys and values in a simple dictionary.
        """
        original = {"a": 1, "b": 2, "c": 3}
        result = invert_dict(original)
        expected = {1: "a", 2: "b", 3: "c"}
        self.assertEqual(result, expected)

    def test_invert_dict_empty(self):
        """
        Test that invert_dict returns an empty dictionary when given an empty input.
        """
        original = {}
        result = invert_dict(original)
        expected = {}
        self.assertEqual(result, expected)

    def test_invert_dict_single_item(self):
        """
        Test that `invert_dict` correctly inverts a dictionary with a single key-value pair.
        """
        original = {"key": "value"}
        result = invert_dict(original)
        expected = {"value": "key"}
        self.assertEqual(result, expected)

    def test_invert_dict_numeric_keys_string_values(self):
        """
        Test that invert_dict correctly inverts a dictionary with numeric keys and string values.
        """
        original = {1: "one", 2: "two", 3: "three"}
        result = invert_dict(original)
        expected = {"one": 1, "two": 2, "three": 3}
        self.assertEqual(result, expected)

    def test_invert_dict_mixed_types(self):
        """
        Test that invert_dict correctly inverts a dictionary with mixed key and value types.
        """
        original = {"str_key": 1, 2: "str_value", "another": 3.14}
        result = invert_dict(original)
        expected = {1: "str_key", "str_value": 2, 3.14: "another"}
        self.assertEqual(result, expected)

    def test_invert_dict_duplicate_values_behavior(self):
        """
        Test that invert_dict handles duplicate values by retaining only the last key for each value.
        
        Verifies that when multiple keys share the same value, the inverted dictionary contains only the last encountered key for each value.
        """
        original = {"a": 1, "b": 1, "c": 2}
        result = invert_dict(original)

        # Due to dict iteration order, one of "a" or "b" will be the final value for key 1
        self.assertEqual(len(result), 2)
        self.assertIn(1, result)
        self.assertIn(2, result)
        self.assertEqual(result[2], "c")
        self.assertIn(result[1], ["a", "b"])

    def test_invert_dict_none_values(self):
        """
        Test that invert_dict correctly inverts a dictionary containing None values.
        """
        original = {"key1": None, "key2": "value"}
        result = invert_dict(original)
        expected = {None: "key1", "value": "key2"}
        self.assertEqual(result, expected)

    def test_invert_dict_tuple_values(self):
        """
        Test that invert_dict correctly inverts a dictionary with tuple values as keys in the result.
        """
        original = {"key1": (1, 2), "key2": (3, 4)}
        result = invert_dict(original)
        expected = {(1, 2): "key1", (3, 4): "key2"}
        self.assertEqual(result, expected)

    def test_invert_dict_boolean_values(self):
        """
        Test that invert_dict correctly inverts a dictionary with boolean values as values, ensuring the resulting dictionary maps booleans to their original keys.
        """
        original = {"true_key": True, "false_key": False}
        result = invert_dict(original)
        expected = {True: "true_key", False: "false_key"}
        self.assertEqual(result, expected)

    def test_invert_dict_comprehension_equivalent(self):
        """
        Verify that invert_dict returns the same inverted dictionary as a standard dictionary comprehension.
        """
        original = {"x": 10, "y": 20, "z": 30}
        result = invert_dict(original)
        expected = {v: k for k, v in original.items()}
        self.assertEqual(result, expected)


class TestIsNumeric(unittest.TestCase):
    """Test cases for the is_numeric function."""

    def test_is_numeric_integer_strings(self):
        """
        Test that is_numeric returns True for valid integer string representations.
        """
        self.assertTrue(is_numeric("123"))
        self.assertTrue(is_numeric("-456"))
        self.assertTrue(is_numeric("0"))
        self.assertTrue(is_numeric("+789"))

    def test_is_numeric_float_strings(self):
        """
        Test that is_numeric correctly identifies valid float string representations as numeric.
        """
        self.assertTrue(is_numeric("123.45"))
        self.assertTrue(is_numeric("-67.89"))
        self.assertTrue(is_numeric("0.0"))
        self.assertTrue(is_numeric(".5"))
        self.assertTrue(is_numeric("5."))
        self.assertTrue(is_numeric("+3.14"))

    def test_is_numeric_scientific_notation(self):
        """
        Test that is_numeric correctly identifies strings in scientific notation as numeric.
        """
        self.assertTrue(is_numeric("1e5"))
        self.assertTrue(is_numeric("1.5e-3"))
        self.assertTrue(is_numeric("-2.5E+10"))
        self.assertTrue(is_numeric("1E0"))

    def test_is_numeric_special_float_values(self):
        """
        Test that is_numeric correctly identifies special float values such as infinity and NaN as numeric strings.
        """
        self.assertTrue(is_numeric("inf"))
        self.assertTrue(is_numeric("-inf"))
        self.assertTrue(is_numeric("nan"))
        self.assertTrue(is_numeric("infinity"))
        self.assertTrue(is_numeric("-infinity"))

    def test_is_numeric_non_numeric_strings(self):
        """
        Verify that is_numeric returns False for various non-numeric string inputs, including alphabetic characters, malformed numbers, empty strings, whitespace, and mixed alphanumeric values.
        """
        self.assertFalse(is_numeric("abc"))
        self.assertFalse(is_numeric("12.34.56"))
        self.assertFalse(is_numeric(""))
        self.assertFalse(is_numeric(" "))
        self.assertFalse(is_numeric("123abc"))
        self.assertFalse(is_numeric("abc123"))
        self.assertFalse(is_numeric("12 34"))

    def test_is_numeric_edge_cases(self):
        """
        Test that is_numeric returns False for malformed numeric strings and edge cases.
        
        Covers cases with multiple signs, misplaced decimal points, and incomplete scientific notation.
        """
        self.assertFalse(is_numeric("--5"))
        self.assertFalse(is_numeric("++5"))
        self.assertFalse(is_numeric("5-"))
        self.assertFalse(is_numeric("5+"))
        self.assertFalse(is_numeric("..5"))
        self.assertFalse(is_numeric("5.."))
        self.assertFalse(is_numeric("e5"))
        self.assertFalse(is_numeric("5e"))

    def test_is_numeric_whitespace(self):
        """
        Test that is_numeric correctly handles strings with whitespace.
        
        Verifies that leading and trailing whitespace are ignored, but internal whitespace causes the string to be considered non-numeric.
        """
        self.assertTrue(is_numeric("  123  "))  # Leading/trailing whitespace is handled by float()
        self.assertFalse(is_numeric("1 2 3"))  # Internal whitespace is not valid
        self.assertTrue(is_numeric("\t42\n"))  # Tab and newline are handled

    def test_is_numeric_hexadecimal(self):
        """
        Test that is_numeric returns False for hexadecimal string inputs.
        
        Hexadecimal strings prefixed with '0x' are not recognized as numeric by is_numeric.
        """
        self.assertFalse(is_numeric("0x1A"))  # Hex not supported by float()
        self.assertFalse(is_numeric("0xFF"))

    def test_is_numeric_octal_binary(self):
        """
        Test that `is_numeric` returns False for octal and binary string representations.
        """
        self.assertFalse(is_numeric("0o777"))  # Octal not supported by float()
        self.assertFalse(is_numeric("0b1010"))  # Binary not supported by float()

    def test_is_numeric_unicode_digits(self):
        """
        Test that `is_numeric` correctly identifies strings containing Unicode digit characters as numeric.
        """
        self.assertTrue(is_numeric("１２３"))  # Unicode digits are supported by float()

    def test_is_numeric_currency_symbols(self):
        """
        Test that is_numeric returns False for strings containing currency symbols or percent signs.
        """
        self.assertFalse(is_numeric("$123"))
        self.assertFalse(is_numeric("€456"))
        self.assertFalse(is_numeric("123%"))


class TestLookForFractions(unittest.TestCase):
    """Test cases for the look_for_fractions function."""

    def test_look_for_fractions_valid_integer_fractions(self):
        """
        Test that look_for_fractions returns True for lists of two valid integer numeric strings.
        """
        self.assertTrue(look_for_fractions(["1", "2"]))
        self.assertTrue(look_for_fractions(["3", "4"]))
        self.assertTrue(look_for_fractions(["0", "1"]))
        self.assertTrue(look_for_fractions(["-1", "2"]))
        self.assertTrue(look_for_fractions(["1", "-2"]))

    def test_look_for_fractions_valid_float_fractions(self):
        """
        Test that look_for_fractions returns True for lists of two numeric strings representing valid float fractions.
        """
        self.assertTrue(look_for_fractions(["1.5", "2"]))
        self.assertTrue(look_for_fractions(["3", "4.0"]))
        self.assertTrue(look_for_fractions(["1.2", "3.4"]))

    def test_look_for_fractions_invalid_non_numeric(self):
        """
        Test that look_for_fractions returns False when given lists containing non-numeric strings.
        """
        self.assertFalse(look_for_fractions(["a", "2"]))
        self.assertFalse(look_for_fractions(["1", "b"]))
        self.assertFalse(look_for_fractions(["abc", "def"]))
        self.assertFalse(look_for_fractions(["", "2"]))
        self.assertFalse(look_for_fractions(["1", ""]))

    def test_look_for_fractions_wrong_length(self):
        """
        Verify that look_for_fractions returns False when given lists with lengths other than two.
        """
        self.assertFalse(look_for_fractions(["1"]))  # Too short
        self.assertFalse(look_for_fractions([]))  # Empty
        self.assertFalse(look_for_fractions(["1", "2", "3"]))  # Too long
        self.assertFalse(look_for_fractions(["1", "2", "3", "4"]))  # Too long

    def test_look_for_fractions_edge_cases(self):
        """
        Test that look_for_fractions correctly identifies edge cases such as zero, infinity, and NaN as valid numeric fractions.
        """
        self.assertTrue(look_for_fractions(["0", "0"]))  # Zero fraction
        self.assertTrue(look_for_fractions(["inf", "1"]))  # Infinity (is_numeric returns True)
        self.assertTrue(look_for_fractions(["1", "inf"]))  # Infinity denominator
        self.assertTrue(look_for_fractions(["nan", "1"]))  # NaN (is_numeric returns True)

    def test_look_for_fractions_mixed_valid_invalid(self):
        """
        Test that look_for_fractions returns False when given lists containing both valid and invalid numeric strings.
        """
        self.assertFalse(look_for_fractions(["1.5", "abc"]))
        self.assertFalse(look_for_fractions(["xyz", "2.5"]))
        self.assertFalse(look_for_fractions(["12.34.56", "2"]))

    def test_look_for_fractions_whitespace(self):
        """
        Test that look_for_fractions correctly handles numeric strings with leading or trailing whitespace, and rejects numbers with internal spaces.
        """
        self.assertTrue(look_for_fractions(["  1  ", "  2  "]))  # Whitespace around numbers
        self.assertFalse(look_for_fractions(["1 2", "3"]))  # Space within number

    def test_look_for_fractions_large_numbers(self):
        """
        Test that `look_for_fractions` correctly identifies pairs of large numeric strings as valid fractions.
        """
        self.assertTrue(look_for_fractions(["123456789", "987654321"]))

    def test_look_for_fractions_scientific_notation(self):
        """
        Test that `look_for_fractions` correctly identifies pairs of numeric strings in scientific notation as valid fractions.
        """
        self.assertTrue(look_for_fractions(["1e5", "2e3"]))
        self.assertTrue(look_for_fractions(["1.5e-3", "2.7e+2"]))


class TestConvertToMixedFraction(unittest.TestCase):
    """Test cases for the convert_to_mixed_fraction function."""

    def test_convert_whole_numbers(self):
        """
        Test that convert_to_mixed_fraction correctly converts whole numbers to (whole, numerator, denominator) tuples.
        """
        result = convert_to_mixed_fraction(5.0)
        self.assertEqual(result, (5, 0, 1))

        result = convert_to_mixed_fraction(0.0)
        self.assertEqual(result, (0, 0, 1))

        result = convert_to_mixed_fraction(-3.0)
        self.assertEqual(result, (-3, 0, 1))

    def test_convert_simple_fractions(self):
        """
        Test that convert_to_mixed_fraction correctly converts simple decimal fractions to mixed fraction tuples.
        """
        result = convert_to_mixed_fraction(0.5)
        self.assertEqual(result, (0, 1, 2))

        result = convert_to_mixed_fraction(0.25)
        self.assertEqual(result, (0, 1, 4))

        result = convert_to_mixed_fraction(0.75)
        self.assertEqual(result, (0, 3, 4))

    def test_convert_mixed_fractions(self):
        """
        Test that convert_to_mixed_fraction correctly converts decimal numbers to mixed fraction tuples for typical mixed number cases.
        """
        result = convert_to_mixed_fraction(2.5)
        self.assertEqual(result, (2, 1, 2))

        result = convert_to_mixed_fraction(3.25)
        self.assertEqual(result, (3, 1, 4))

        result = convert_to_mixed_fraction(1.75)
        self.assertEqual(result, (1, 3, 4))

    def test_convert_negative_mixed_fractions(self):
        """
        Test that convert_to_mixed_fraction correctly converts negative mixed numbers to (whole, numerator, denominator) tuples.
        """
        result = convert_to_mixed_fraction(-2.5)
        self.assertEqual(result, (-2, 1, 2))

        result = convert_to_mixed_fraction(-1.25)
        self.assertEqual(result, (-1, 1, 4))

    def test_convert_with_custom_denominators(self):
        """
        Test that convert_to_mixed_fraction returns correct mixed fractions when restricted to specific denominators.
        """
        # Only allow denominators 2, 3, 4
        result = convert_to_mixed_fraction(0.5, denominators=[2, 3, 4])
        self.assertEqual(result, (0, 1, 2))

        result = convert_to_mixed_fraction(1.0 / 3, denominators=[2, 3, 4])
        self.assertEqual(result, (0, 1, 3))

    def test_convert_no_good_approximation(self):
        """
        Test that convert_to_mixed_fraction returns None when no suitable mixed fraction approximation can be found with the given denominators.
        """
        # Use very limited denominators that can't represent 1/7 well
        result = convert_to_mixed_fraction(1.0 / 7, denominators=[2, 3])
        self.assertIsNone(result)

    def test_convert_empty_denominators(self):
        """
        Test that convert_to_mixed_fraction uses the default denominator range when given an empty denominators list.
        """
        # Should use default range(1, 21)
        result = convert_to_mixed_fraction(0.5, denominators=[])
        self.assertEqual(result, (0, 1, 2))

    def test_convert_none_denominators(self):
        """
        Test that convert_to_mixed_fraction uses the default denominator range when denominators is None.
        """
        # Should use default range(1, 21)
        result = convert_to_mixed_fraction(0.5, denominators=None)
        self.assertEqual(result, (0, 1, 2))

    def test_convert_close_to_whole_number(self):
        """
        Test that convert_to_mixed_fraction correctly handles numbers very close to whole numbers, ensuring proper rounding and fraction extraction near integer boundaries.
        """
        # 4.500002 should become 4 1/2 due to the 0.01 accuracy threshold
        result = convert_to_mixed_fraction(4.500002)
        self.assertEqual(result, (4, 1, 2))

        # Test number very close to 5
        result = convert_to_mixed_fraction(4.9999)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 4)  # Whole part should be 4

    def test_convert_accuracy_threshold(self):
        """
        Test that `convert_to_mixed_fraction` returns a reasonable approximation for values near a simple fraction, within the default accuracy threshold.
        """
        # Test a value that's close to 1/3 but not exact
        result = convert_to_mixed_fraction(1.0 / 3 + 0.001)  # Slightly off from 1/3
        # Should still find a reasonable approximation
        self.assertIsNotNone(result)

    def test_convert_large_denominators(self):
        """
        Test that convert_to_mixed_fraction correctly finds a mixed fraction representation for a float with large possible denominators.
        
        Verifies that 0.05 is accurately converted to (0, 1, 20) when denominators up to 29 are allowed.
        """
        result = convert_to_mixed_fraction(0.05, denominators=range(1, 30))
        self.assertIsNotNone(result)
        self.assertEqual(result, (0, 1, 20))  # 1/20 = 0.05

    def test_convert_edge_case_very_small_fraction(self):
        """
        Test that convert_to_mixed_fraction treats numbers with very small fractional parts as whole numbers due to the accuracy threshold.
        """
        result = convert_to_mixed_fraction(5.00001)
        # Should be treated as whole number due to accuracy threshold
        self.assertEqual(result, (5, 0, 1))

    def test_convert_repeating_decimals(self):
        """
        Test that convert_to_mixed_fraction correctly converts repeating decimals to their fractional representations.
        """
        # 1/3 = 0.333...
        result = convert_to_mixed_fraction(1.0 / 3)
        self.assertEqual(result, (0, 1, 3))

        # 2/3 = 0.666...
        result = convert_to_mixed_fraction(2.0 / 3)
        self.assertEqual(result, (0, 2, 3))

    def test_convert_single_denominator(self):
        """
        Test that convert_to_mixed_fraction correctly handles cases with a single allowed denominator.
        
        Verifies that the function returns the expected mixed fraction tuple when the value can be represented with the given denominator, and returns None when it cannot.
        """
        result = convert_to_mixed_fraction(0.5, denominators=[2])
        self.assertEqual(result, (0, 1, 2))

        # Should return None if the single denominator can't represent the fraction well
        result = convert_to_mixed_fraction(1.0 / 3, denominators=[2])
        self.assertIsNone(result)

    def test_convert_large_whole_numbers(self):
        """
        Test that convert_to_mixed_fraction correctly handles large whole numbers and mixed fractions.
        
        Verifies that whole numbers return a zero numerator and denominator of one, and that mixed fractions with large whole parts are accurately decomposed.
        """
        result = convert_to_mixed_fraction(1000.0)
        self.assertEqual(result, (1000, 0, 1))

        result = convert_to_mixed_fraction(1000.25)
        self.assertEqual(result, (1000, 1, 4))

    def test_convert_complex_fractions(self):
        """
        Test that convert_to_mixed_fraction correctly converts decimal values representing complex fractions, such as fifths and sixths, into mixed fraction tuples.
        """
        # Test fifths
        result = convert_to_mixed_fraction(0.2)  # 1/5
        self.assertEqual(result, (0, 1, 5))

        result = convert_to_mixed_fraction(0.6)  # 3/5
        self.assertEqual(result, (0, 3, 5))

        # Test sixths
        result = convert_to_mixed_fraction(1.0 / 6)
        self.assertEqual(result, (0, 1, 6))

    def test_convert_edge_denominator_boundary(self):
        """
        Test that convert_to_mixed_fraction correctly handles cases at the boundary of allowed denominators.
        
        Verifies that the function returns the correct mixed fraction when the denominator is at the upper limit of the default range, and returns None when no suitable denominator is found within the specified range.
        """
        # Test with denominator exactly at boundary (20 in default range)
        result = convert_to_mixed_fraction(1.0 / 20)
        self.assertEqual(result, (0, 1, 20))

        # Test with fraction that would need denominator > 20
        result = convert_to_mixed_fraction(1.0 / 25, denominators=range(1, 21))
        # Should not find good approximation with default range
        self.assertIsNone(result)


if __name__ == '__main__':
    # Run the tests with verbose output
    unittest.main(verbosity=2)
