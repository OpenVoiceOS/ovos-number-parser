from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Union, Any, Tuple, Optional, Callable
import re


@dataclass
class Token:
    word: str
    index: int

    def __iter__(self):
        yield self.word
        yield self.index

    def __getitem__(self, item):
        if item == 0:
            return self.word
        elif item == 1:
            return self.index
        raise IndexError

    def __setattr__(self, key, value):
        """
        Prevent modification of existing attributes, allowing only new attributes to be set.

        Raises:
            Exception: If attempting to modify an attribute that already exists.
        """
        try:
            getattr(self, key)
        except AttributeError:
            super().__setattr__(key, value)
        else:
            raise AttributeError("Immutable!")


class Scale(str, Enum):
    """
    Defines the numerical scale to be used.
    - SHORT: Short scale (e.g., billion = 10^9).
    - LONG: Long scale (e.g., billion = 10^12).
    """
    SHORT = "short"
    LONG = "long"


class GrammaticalGender(str, Enum):
    """
    Defines the grammatical gender for number pronunciation.
    """
    MASCULINE = "masculine"
    FEMININE = "feminine"
    NEUTRAL = "neutral"


class DigitPronunciation(str, Enum):
    DIGIT_BY_DIGIT = "digit"
    FULL_NUMBER = "number"


@dataclass
class ReplaceableNumber:
    """
    Similar to Token, this class is used in number parsing.

    Once we've found a number in a string, this class contains all
    the info about the value, and where it came from in the original text.
    In other words, it is the text, and the number that can replace it in
    the string.
    """
    value: Union[int, float]
    tokens: List[Token]

    def __bool__(self) -> bool:
        return bool(self.value is not None and self.value is not False)

    @property
    def start_index(self) -> int:
        return self.tokens[0].index

    @property
    def end_index(self) -> int:
        return self.tokens[-1].index

    @property
    def text(self) -> str:
        """
        Return the concatenated text represented by the tokens, separated by spaces.
        """
        return ' '.join([str(t.word) for t in self.tokens if t.word])

    def __setattr__(self, key, value):
        """
        Prevent modification of existing attributes, allowing only new attributes to be set.

        Raises:
            Exception: If attempting to modify an attribute that already exists.
        """
        try:
            getattr(self, key)
        except AttributeError:
            super().__setattr__(key, value)
        else:
            raise Exception("Immutable!")

    def __str__(self):
        return "({v}, {t})".format(v=self.value, t=self.tokens)

    def __repr__(self):
        return "{n}({v}, {t})".format(n=self.__class__.__name__, v=self.value,
                                      t=self.tokens)


def word_tokenize(utterance: str) -> List[str]:
    """
    Splits a Portuguese text string into a list of tokens, separating words and punctuation.

    Returns:
        A list of tokens, where each token is a word or punctuation mark from the input string.
    """
    # Split things like 12%
    utterance = re.sub(r"([0-9]+)([\%])", r"\1 \2", utterance)
    # Split things like #1
    utterance = re.sub(r"(\#)([0-9]+\b)", r"\1 \2", utterance)
    # Split things like amo-te, but preserve numbers like 1-2
    utterance = re.sub(r"([a-zA-Z]+)(-)([a-zA-Z]+\b)", r"\1 \2 \3",
                       utterance)

    tokens = utterance.split()
    # Remove a trailing hyphen if it's the last token
    if tokens and tokens[-1] == '-':
        tokens = tokens[:-1]

    return tokens


def tokenize(text: str) -> List[Token]:
    """
    Generate a list of token object, given a string.
    Args:
        text str: Text to tokenize.

    Returns:
        [Token]

    """
    return [Token(word, index) for index, word in enumerate(word_tokenize(text))]


def partition_list(items: List[Any], split_on: Any) -> List[List[Any]]:
    """
    Partition a list of items.

    Works similarly to str.partition

    Args:
        items:
        split_on callable:
            Should return a boolean. Each item will be passed to
            this callable in succession, and partitions will be
            created any time it returns True.

    Returns:
        [[any]]

    """
    splits = []
    current_split = []
    for item in items:
        if split_on(item):
            splits.append(current_split)
            splits.append([item])
            current_split = []
        else:
            current_split.append(item)
    splits.append(current_split)
    return list(filter(lambda x: len(x) != 0, splits))


def invert_dict(original: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Produce a dictionary with the keys and values
    inverted, relative to the dict passed in.

    Args:
        original dict: The dict like object to invert

    Returns:
        dict

    """
    return {value: key for key, value in original.items()}


def is_numeric(input_str: str) -> bool:
    """
    Return True if the input string represents a valid number, otherwise False.

    Parameters:
        input_str (str): The string to test for numeric value.

    Returns:
        bool: True if the string can be converted to a float, False otherwise.
    """
    try:
        float(input_str)
        return True
    except ValueError:
        return False


def look_for_fractions(split_list: List[str]) -> bool:
    """"
    This function takes a list made by fraction & determines if a fraction.

    Args:
        split_list (list): list created by splitting on '/'
    Returns:
        (bool): False if not a fraction, otherwise True

    """

    if len(split_list) == 2:
        if is_numeric(split_list[0]) and is_numeric(split_list[1]):
            return True

    return False


def convert_to_mixed_fraction(number: Union[int, float], denominators=range(1, 21)) -> Optional[Tuple[int, int, int]]:
    """
    Convert floats to components of a mixed fraction representation

    Returns the closest fractional representation using the
    provided denominators.  For example, 4.500002 would become
    the whole number 4, the numerator 1 and the denominator 2

    Args:
        number (float): number for convert
        denominators (iter of ints): denominators to use, default [1 .. 20]
    Returns:
        whole, numerator, denominator (int): Integers of the mixed fraction
    """
    int_number = int(number)
    if int_number == number:
        return int_number, 0, 1  # whole number, no fraction

    frac_number = abs(number - int_number)
    if not denominators:
        denominators = range(1, 21)

    for denominator in denominators:
        numerator = abs(frac_number) * denominator
        if abs(numerator - round(numerator)) < 0.01:  # 0.01 accuracy
            break
    else:
        return None

    return int_number, int(round(numerator)), denominator


@dataclass
class NumberVocabulary:
    LANG: str
    DEFAULT_SCALE: Scale

    # first entry also used for pronouncing, others only for extraction
    JOIN_WORD: List[str]
    JOINER_ON_TWENTYS: bool # add JOIN_WORD from 20-30 - "vinte e um"
    JOINER_ON_HUNDREDS: bool # add JOIN_WORD from 100-1000 - "duzentos e um"
    JOINER_ON_THOUSANDS: bool # add JOIN_WORD from 1000-10000 - "mil e duzentos"
    DECIMAL_MARKER: List[str]
    NEGATIVE_SIGN: List[str]
    HUNDRED_PARTICLE: str  # how to read "1XX"
    DENOMINATOR_PARTICLE: str  # for fractions  X / N {PARTICLE}
    DIVIDED_BY_ZERO: str  # how to read X/0 values

    UNITS: Dict[int, str]  # 0-10 range
    TENS: Dict[int, str]  # 10-100 range
    HUNDREDS: Dict[int, str]  # 100-1000 range
    FRACTION: Dict[int, str]  # spellings for 1/x
    SHORT_SCALE: Dict[int, str]  # 1000+
    LONG_SCALE: Dict[int, str]  # 1000+

    FRACTION_FEMALE: Dict[int, str]  # spellings for 1/x feminine grammatical gender

    ALT_SPELLINGS: Dict[str, int]  # special cases eg. archaisms/colloquialisms

    # mappings default to neutral, use swap_gender/self.GENDERED_SPELLINGS if needed
    GENDERED_SPELLINGS: Dict[GrammaticalGender, Dict[int, str]]  # grammatical gender
    DIGIT_SPELLINGS: Dict[int, str]  # for numbers that should be pronounced differently when reading digit-by-digit

    ORDINAL_UNITS: Dict[int, str]
    ORDINAL_TENS: Dict[int, str]
    ORDINAL_HUNDREDS: Dict[int, str]
    ORDINAL_SHORT_SCALE: Dict[int, str]
    ORDINAL_LONG_SCALE: Dict[int, str]

    NUMBER_OVERFLOW: str  # "número exageradamente grande"
    NO_PREV_UNIT: List[int]  # cases where "1" should not be spelled before the unit. eg. "one hundred" vs "hundred" if 100 in lit
    NO_PLURAL: List[int]

    swap_gender: Callable[[str, GrammaticalGender], str] = lambda word, gender: word
    pluralize: Callable[[str], str] = lambda word: word
    singularize: Callable[[str], str] = lambda word: word

    def get_number_strings(self, scale: Scale = Scale.LONG) -> Dict[str, int]:
        SCALES = self.SHORT_SCALE if scale == Scale.SHORT else self.LONG_SCALE
        male = {
            **self.ALT_SPELLINGS,
            **{v: k for k, v in self.UNITS.items()},
            **{v: k for k, v in self.TENS.items()},
            **{v: k for k, v in self.HUNDREDS.items()},
            **{v: k for k, v in SCALES.items()}
        }

        female = {self.swap_gender(k, GrammaticalGender.FEMININE): v
                  for k, v in male.items()}

        plural = {
            **{self.pluralize(k): v for k, v in male.items()},
            **{self.pluralize(k): v for k, v in female.items()}
        }
        return {
            **male,
            **female,
            **dict({self.HUNDRED_PARTICLE: 100} if self.HUNDRED_PARTICLE else {}),
            **plural
        }

    def get_ordinal_strings(self, scale: Scale = Scale.LONG) -> Dict[str, int]:
        SCALES = self.ORDINAL_SHORT_SCALE if scale == Scale.SHORT else self.ORDINAL_LONG_SCALE
        male = {
            **{v: k for k, v in self.ORDINAL_UNITS.items()},
            **{v: k for k, v in self.ORDINAL_TENS.items()},
            **{v: k for k, v in self.ORDINAL_HUNDREDS.items()},
            **{v: k for k, v in SCALES.items()}
        }
        female = {self.swap_gender(k, GrammaticalGender.FEMININE): v
                  for k, v in male.items()}
        plural = {
            **{self.pluralize(k): v for k, v in male.items()},
            **{self.pluralize(k): v for k, v in female.items()}
        }
        return {
            **male,
            **female,
            **plural
        }

    def get_fraction_strings(self) -> Dict[str, int]:
        male = {v: k for k, v in self.FRACTION.items()}
        female = {v: k for k, v in self.FRACTION_FEMALE.items()}
        plural = {self.pluralize(k): v for k, v in male.items()}
        return {
            **male,
            **female,
            **plural
        }


class RomanceNumberExtractor:
    """vocabulary based number parser that should work for most romance-like languages"""

    def __init__(self, vocab: NumberVocabulary):
        self.vocab = vocab

    def is_ordinal(self, input_str: str, scale: Optional[Scale] = None) -> bool:
        """
        Determine if a string is a Portuguese ordinal word.

        Returns:
            bool: True if the input string is recognized as a Portuguese ordinal, otherwise False.
        """
        scale = scale or self.vocab.DEFAULT_SCALE
        ordinals_map = self.vocab.get_ordinal_strings(scale)
        return input_str in ordinals_map

    def is_fractional(self, input_str: str) -> Union[float, bool]:
        """
        Checks if the input string corresponds to a recognized Portuguese fractional word.

        Returns:
            The fractional value as a float if recognized; otherwise, False.
        """
        fractions_map = self.vocab.get_fraction_strings()
        input_str = input_str.lower().strip()

        # handle fraction denominator strings
        for word, den in fractions_map.items():
            if input_str == word:
                return 1.0 / den

        return False

    def extract_number(self,
                       text: str,
                       ordinals: bool = False,
                       scale: Scale = None,
                       ) -> Union[int, float, bool]:
        """
        Extracts a numeric value from a text phrase, supporting cardinals, ordinals, fractions, and large scales.

        Parameters:
            text (str): The input phrase potentially containing a number.
            ordinals (bool): If True, recognizes ordinal words as numbers.
            scale (Scale): Specifies whether to use the short or long numerical scale.

        Returns:
            int or float: The extracted number if found; otherwise, False.
        """
        scale = scale or self.vocab.DEFAULT_SCALE
        numbers_map = self.vocab.get_number_strings(scale)
        ordinals_map = self.vocab.get_ordinal_strings(scale)
        scales_map = self.vocab.SHORT_SCALE if scale == Scale.SHORT else self.vocab.LONG_SCALE

        # normalize and tokenize
        clean_text = text.lower().replace('-', ' ')
        tokens = [t for t in clean_text.split() if t not in self.vocab.JOIN_WORD]

        result = None
        current_number = None
        number_consumed = False
        is_negative = False

        for i, token in enumerate(tokens):
            if token is None:
                continue  # consumed in previous idx
            prev_token = tokens[i - 1] if i > 0 else None
            next_token = tokens[i + 1] if i < len(tokens) - 1 else None
            next_digit = numbers_map.get(next_token) if next_token else None
            val = numbers_map.get(token)
            if val is not None:
                current_number = current_number or 0
                result = result or 0
                if prev_token in self.vocab.NEGATIVE_SIGN:
                    is_negative = True
                if next_digit and next_digit > abs(val):
                    tokens[i + 1] = None
                    current_number += val * next_digit
                else:
                    current_number += val
            elif ordinals and self.is_ordinal(token):
              #  token = self.vocab.swap_gender(token, GrammaticalGender.MASCULINE)
                current_number = current_number or 0
                result = result or 0
                current_number += ordinals_map[token]
            elif self.is_fractional(token):
                current_number = current_number or 0
                result = result or 0
                fraction = self.is_fractional(token)
                result += current_number + fraction
                current_number = None
                number_consumed = True
            else:
                # Handle large scales like milhão, bilhão
                found_scale = False
                for scale_val, w  in scales_map.items():
                    if token == w or token == self.vocab.pluralize(w):
                        current_number = current_number or 0
                        result = result or 0
                        if current_number is None:
                            current_number = 1
                        result += current_number * scale_val
                        current_number = None
                        found_scale = True
                        number_consumed = True
                        break

                # Handle decimal numbers
                if not found_scale:
                    if token in self.vocab.DECIMAL_MARKER:
                        current_number = current_number or 0
                        result = result or 0
                        decimal_str = ''.join(
                            str(numbers_map.get(t, '')) for t in tokens[i + 1:]
                            if t in numbers_map
                        )
                        if decimal_str:
                            result += current_number + float(f"0.{decimal_str}")
                            number_consumed = True
                        current_number = None
                        break

        if not number_consumed and current_number:
            result = result or 0
            result += current_number

        if result and is_negative:
            result = -result
        return result if result is not None else False

    def numbers_to_digits(self,
                          utterance: str,
                          scale: Scale = Scale.LONG
                          ) -> str:
        """
        Converts written numbers in a text string to their digit equivalents, preserving all other text.

        Identifies spans of number words (including the joiner "e"), extracts their numeric values, and replaces them with digit strings. Non-number words and context are left unchanged.

        Parameters:
            utterance (str): Input text possibly containing written numbers.
            scale (Scale, optional): Numerical scale (short or long) to interpret large numbers. Defaults to Scale.LONG.

        Returns:
            str: The input text with written numbers replaced by their digit representations.
        """
        words = word_tokenize(utterance)
        output = []
        i = 0

        numbers_map = self.vocab.get_number_strings(scale)

        while i < len(words):
            # Look for the start of a number span
            if words[i] in numbers_map:
                # Start a new span
                number_span_words = []
                j = i
                # Continue the span as long as we find number words or the joiner 'e'
                while j < len(words) and (words[j] in numbers_map or words[j] in self.vocab.JOIN_WORD):
                    number_span_words.append(words[j])
                    j += 1

                # Form the phrase from the span and extract the number value
                phrase = " ".join(number_span_words)
                number_val = self.extract_number(phrase)

                if number_val is not False:
                    # If a valid number is found, add its digit representation to the output
                    output.append(str(number_val))
                    # Advance the main index 'i' past the entire span
                    i = j
                else:
                    # If the span doesn't form a valid number, treat the first word as non-numeric
                    # and move to the next word. This handles cases like "e" at the beginning of a sentence.
                    output.append(words[i])
                    i += 1
            else:
                # If the current word is not a number word, add it to the output
                # and move to the next word
                output.append(words[i])
                i += 1

        return " ".join(output)

    def pronounce_number(self,
                         number: Union[int, float],
                         places: int = 5,
                         scale: Scale = Scale.LONG,
                         ordinals: bool = False,
                         digits: DigitPronunciation = DigitPronunciation.FULL_NUMBER,
                         gender: GrammaticalGender = GrammaticalGender.MASCULINE
                         ) -> str:
        """
        Return the full pronunciation of a number, supporting cardinal and ordinal forms, decimals, large scales, grammatical gender, and both Brazilian and European Portuguese variants.

        Parameters:
            number (int or float): The number to pronounce.
            places (int): Number of decimal places to include for floats.
            scale (Scale): Numerical scale to use (short or long).
            ordinals (bool): If True, pronounce as an ordinal number.
            gender (GrammaticalGender): Grammatical gender for ordinal numbers.

        Returns:
            str: The number expressed as a phrase.
        """
        if not isinstance(number, (int, float)):
            raise TypeError("Number must be an int or float.")

        if ordinals:
            return self.pronounce_ordinal(number, gender, scale)

        if number in self.vocab.UNITS:
            return self.vocab.UNITS[number]

        if number < 0:
            return f"{self.vocab.NEGATIVE_SIGN[0]} {self.pronounce_number(abs(number), places, scale=scale, digits=digits, gender=gender)}"

        # Handle decimals
        if "." in str(number):
            integer_part = int(number)
            decimal_part_str = str(number).split('.')[1].rstrip("0")

            # Handle cases where the decimal part rounds to zero
            if decimal_part_str and int(decimal_part_str) == 0:
                return self.pronounce_number(integer_part, places,
                                           scale=scale,
                                           digits=digits, gender=gender)

            int_pronunciation = self.pronounce_number(integer_part, places,
                                                    scale=scale,
                                                    digits=digits, gender=gender)

            decimal_pronunciation_parts = []
            #  pronounce decimals either as a whole number or digit by digit
            if decimal_part_str:
                if digits == DigitPronunciation.FULL_NUMBER:

                    # handle leading zeros
                    no_z = decimal_part_str.lstrip("0") # without zeros
                    n_zeros = len(decimal_part_str) - len(no_z)
                    for i in range(n_zeros):
                        decimal_pronunciation_parts.append(self.vocab.UNITS[0])

                    if n_zeros >= places:
                        # read all zeros
                        last_digit = int(decimal_part_str[n_zeros])
                        after_last_digit = int(decimal_part_str[n_zeros + 1]) if len(decimal_part_str) > n_zeros + 1 else 0
                        # round up last digit if needed
                        if after_last_digit >= 5:
                            last_digit += 1
                        decimal_pronunciation_parts.append(self._pronounce_up_to_999(last_digit, gender))
                    else:
                        if len(decimal_part_str) > places:
                            last_digit = int(decimal_part_str[places - 1])
                            after_last_digit = int(decimal_part_str[places])
                            # round up last digit if needed
                            if after_last_digit >= 5:
                                last_digit += 1
                            decimal_part_str = decimal_part_str[:places - 1] + str(last_digit)
                        decimal_pronunciation_parts.append(self.pronounce_number(int(decimal_part_str), gender=gender))
                else:
                    for digit in decimal_part_str:
                        decimal_pronunciation_parts.append(self.pronounce_number(int(digit), gender=gender))

            decimal_pronunciation = " ".join(decimal_pronunciation_parts) or self.vocab.UNITS[0]
            decimal_word = self.vocab.DECIMAL_MARKER[0]
            return f"{int_pronunciation} {decimal_word} {decimal_pronunciation}"

        # --- Integer Pronunciation Logic ---
        n = int(number)

        # Base case for recursion: numbers less than 1000
        if n < 1000:
            return self._pronounce_up_to_999(n, gender)

        scales_map = self.vocab.SHORT_SCALE if scale == Scale.SHORT else self.vocab.LONG_SCALE

        # Find the smallest scale that fits the number
        scale_candidates = [(scale_val, scale_str)
                            for scale_val, scale_str in scales_map.items()
                            if n >= scale_val]
        scale_val: Tuple[int, str] = scale_candidates[0]

        count = n // scale_val[0]
        remainder = n % scale_val[0]

        # Pronounce the 'count' part of the number
        is_singular = count == 1 or scale_val[0] in self.vocab.NO_PLURAL
        scale_word = scale_val[1] if is_singular else self.vocab.pluralize(scale_val[1])
        if count == 1 and scale_val[0] in self.vocab.NO_PREV_UNIT:
            count_str = scale_word
        else:
            count_pronunciation = self.pronounce_number(count, places, scale)
            count_str = f"{count_pronunciation} {scale_word}"

        # If there's no remainder, we're done
        if remainder == 0:
            return count_str

        # Pronounce the remainder and join with the correct conjunction
        remainder_str = self.pronounce_number(remainder, places, scale)

        # Conjunction logic: add JOIN_WORD if the remainder is the last group and is
        # less than 100 or a multiple of 100.
        join_word = self.vocab.JOIN_WORD[0] if len(self.vocab.JOIN_WORD) else ""
        if remainder < 100 or (remainder < 1000 and remainder % 100 == 0):
            return f"{count_str} {join_word} {remainder_str}"
        else:
            return f"{count_str} {remainder_str}"

    def pronounce_fraction(self,
                           word: str,
                           scale: Scale = Scale.LONG) -> str:
        """
        Return the pronunciation of a fraction given as a string (e.g., "1/2").

        The numerator is pronounced as a cardinal number, and the denominator as an ordinal or fraction name, pluralized if appropriate. For denominators not in the known fraction list, the denominator is pronounced as a cardinal number followed by "avos" if plural.

        Parameters:
            word (str): Fraction in the form "numerator/denominator" (e.g., "3/4").

        Returns:
            str: The pronunciation of the fraction.
        """
        n1, n2 = word.split("/")
        n1_int, n2_int = int(n1), int(n2)

        if n2_int == 0:
            denom = self.vocab.DIVIDED_BY_ZERO

        # Pronounce the denominator (second number) as an ordinal, and pluralize it if needed.
        elif n2_int in self.vocab.FRACTION:
            denom = self.vocab.FRACTION[n2_int]
            if n1_int != 1:
                denom = self.vocab.pluralize(denom)  # plural
        else:
            # For other numbers
            denom = self.pronounce_number(n2_int, scale=scale)
            if n1_int > 1:  # plural
                denom = f"{denom} {self.vocab.DENOMINATOR_PARTICLE}"


        # Pronounce the numerator (first number) as a cardinal.
        num = self.pronounce_number(n1_int, scale=scale)
        return f"{num} {denom}"

    def pronounce_ordinal(self,
                          number: Union[int, float],
                          gender: GrammaticalGender = GrammaticalGender.MASCULINE,
                          scale: Scale = Scale.LONG
                          ) -> str:
        """
        Return the ordinal pronunciation of a number, supporting grammatical gender, scale (short or long), and language variant (Brazilian or European Portuguese).

        Parameters:
            number (int or float): The number to pronounce as an ordinal.
            gender (GrammaticalGender, optional): The grammatical gender for the ordinal form (masculine or feminine).
            scale (Scale, optional): The numerical scale to use (short or long).

        Returns:
            str: The ordinal pronunciation of the number.

        Raises:
            TypeError: If `number` is not an int or float.
        """
        if not isinstance(number, (int, float)):
            raise TypeError("Number must be an int or float.")
        if number == 0:
            return self.vocab.UNITS[0]

        if number < 0:
            return f"{self.vocab.NEGATIVE_SIGN[0]} {self.pronounce_ordinal(abs(number), gender, scale)}"

        n = int(number)
        if n < 1000:
            return self._pronounce_ordinal_up_to_999(n, gender)

        scales_map = self.vocab.ORDINAL_SHORT_SCALE if scale == Scale.SHORT else self.vocab.ORDINAL_LONG_SCALE

        # Find the smallest scale that fits the number
        scale_candidates = [(scale_val, scale_str)
                            for scale_val, scale_str in scales_map.items()
                            if n >= scale_val]
        scale_val: Tuple[int, str] = scale_candidates[0]

        count = n // scale_val[0]
        remainder = n % scale_val[0]

        # Special case for "milésimo" and other large scales where 'um' is not needed
        if count == 1:
            count_str = self.vocab.swap_gender(scale_val[1], gender)
        else:
            # Pronounce the 'count' part of the number and the scale word
            count_pronunciation = self.pronounce_number(count, scale=scale)
            scale_word = self.vocab.swap_gender(scale_val[1], gender)
            count_str = f"{count_pronunciation} {scale_word}"

        # If there's no remainder, we're done
        if remainder == 0:
            return count_str

        # Pronounce the remainder and join
        remainder_str = self.pronounce_ordinal(remainder, gender, scale)

        return f"{count_str} {remainder_str}"

    def _pronounce_up_to_999(self,
                             n: int,
                             gender: GrammaticalGender = GrammaticalGender.MASCULINE
                             ) -> str:
        """
        Returns the cardinal pronunciation of an integer from 0 to 999, using the specified language variant.

        Parameters:
            n (int): Integer to pronounce (must be between 0 and 999).

        Returns:
            str: The pronounced number.

        Raises:
            ValueError: If n is not in the range 0 to 999.
        """
        if not 0 <= n <= 999:
            raise ValueError("Number must be between 0 and 999.")
        if n in self.vocab.UNITS:
            return self.vocab.UNITS[n]
        if n in self.vocab.TENS:
            return self.vocab.TENS[n]
        if n in self.vocab.HUNDREDS:
            return self.vocab.HUNDREDS[n]

        parts = []
        tens_map = self.vocab.TENS

        # Hundreds
        if n >= 100:
            hundred = n // 100 * 100
            parts.append(self.vocab.HUNDRED_PARTICLE if hundred == 100 else self.vocab.HUNDREDS[hundred])
            n %= 100
            if n > 0 and self.vocab.JOIN_WORD and self.vocab.JOINER_ON_HUNDREDS:
                parts.append(self.vocab.JOIN_WORD[0])

        # Tens and Units
        if n > 0:
            if n < 20:
                parts.append(tens_map.get(n) or self.vocab.UNITS.get(n, ""))
            else:
                ten = n // 10 * 10
                unit = n % 10
                parts.append(tens_map[ten])
                if unit > 0:
                    if self.vocab.JOINER_ON_TWENTYS and self.vocab.JOIN_WORD:
                        parts.append(self.vocab.JOIN_WORD[0])
                    parts.append(self.vocab.UNITS[unit])

        return " ".join(parts)

    def _pronounce_ordinal_up_to_999(self,
                                     n: int,
                                     gender: GrammaticalGender = GrammaticalGender.MASCULINE
                                     ) -> str:
        """
        Returns the ordinal word for an integer between 0 and 999, adjusting for grammatical gender and language variant.

        Parameters:
            n (int): The integer to convert (must be between 0 and 999).

        Returns:
            str: The ordinal representation of the number.

        Raises:
            ValueError: If n is not between 0 and 999.
        """
        if not 0 <= n <= 999:
            raise ValueError("Number must be between 0 and 999.")
        if n == 0:
            return self.vocab.UNITS[0]

        parts = []

        # Handle hundreds
        if n >= 100:
            hundred_val = n // 100 * 100
            hundred_word_masc = self.vocab.ORDINAL_HUNDREDS.get(hundred_val)
            if hundred_word_masc:
                parts.append(self.vocab.swap_gender(hundred_word_masc, gender))
            n %= 100

        # Handle tens and units
        if n > 0:
            # Ordinal numbers don't use 'e' as a separator
            if n % 10 == 0 and n > 10:
                tens_word_masc = self.vocab.ORDINAL_TENS[n]
                parts.append(self.vocab.swap_gender(tens_word_masc, gender))
            elif n < 10:
                units_word_masc = self.vocab.ORDINAL_UNITS[n]
                parts.append(self.vocab.swap_gender(units_word_masc, gender))
            elif n < 20:
                tens_word_masc = self.vocab.ORDINAL_TENS[10]
                units_word_masc = self.vocab.ORDINAL_UNITS[n - 10]
                parts.append(f"{self.vocab.swap_gender(tens_word_masc, gender)} {self.vocab.swap_gender(units_word_masc, gender)}")
            else:
                tens_word_masc = self.vocab.ORDINAL_TENS[n // 10 * 10]
                units_word_masc = self.vocab.ORDINAL_UNITS[n % 10]
                parts.append(f"{self.vocab.swap_gender(tens_word_masc, gender)} {self.vocab.swap_gender(units_word_masc, gender)}")

        return " ".join(parts)
