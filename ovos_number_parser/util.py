from dataclasses import dataclass, field
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

    # restrict the tens joiner to the twenties ("vint-e-un" but "trenta dos"),
    # for languages that only join 21-29
    JOINER_ONLY_ON_TWENTYS: bool = False

    # prefer explicit ORDINAL_TENS entries ("onzen", "vint-e-unen") over
    # composing tens + units ordinals
    PREFER_EXPLICIT_ORDINALS: bool = False

    # join the "hundred" particle to its remainder ("cento e un") even when
    # JOINER_ON_HUNDREDS is off, but only for the top-level group of the number
    JOINER_ON_HUNDRED_PARTICLE: bool = False

    # use the conjunction between a scale group and its final sub-100
    # remainder ("dous mil e un"); languages that say the remainder bare
    # ("două mii unu") turn this off
    JOINER_ON_SCALE_REMAINDER: bool = True

    # linker word inserted between a count and its scale word when the count
    # ends in 00 or in 20-99 ("douăzeci DE mii", "o sută DE milioane")
    SCALE_LINKER: str = ""

    # extraction: the word for 100 multiplies the preceding units
    # ("două sute" = 200) instead of being added to them
    MULTIPLY_HUNDREDS: bool = False

    # full spelling of "one <scale>" groups when they use an article or a
    # special form of "one" ("o mie", "un milion")
    SCALE_ONE: Dict[int, str] = field(default_factory=dict)

    # grammatical gender the count before each scale word agrees with
    # ("două mii" - feminine "două", not masculine "doi")
    SCALE_GENDERS: Dict[int, GrammaticalGender] = field(default_factory=dict)

    # full spelling of "1/x" fractions when they use an article
    # ("o jumătate", "un sfert")
    FRACTION_ONE: Dict[int, str] = field(default_factory=dict)

    # gender the fraction numerator agrees with ("două treimi")
    FRACTION_NUMERATOR_GENDER: Optional[GrammaticalGender] = None

    # ordinal particle placed before the ordinal word ("al doilea"/"a doua")
    ORDINAL_PREFIX: Dict[GrammaticalGender, str] = field(default_factory=dict)
    # values whose ordinal word already stands alone and takes no particle
    # ("primul")
    ORDINAL_UNPREFIXED: List[int] = field(default_factory=list)
    # compound ordinals over 20 keep the cardinal tens joined to an ordinal
    # unit ("al douăzeci și unulea"); also prefers exact ORDINAL_TENS entries
    # for 11-19
    ORDINAL_COMPOUND_CARDINAL_TENS: bool = False
    # unit spellings used inside compound ordinals when they differ from the
    # standalone ordinal ("unulea" vs "primul")
    ORDINAL_COMPOUND_UNITS: Dict[int, str] = field(default_factory=dict)

    def get_number_strings(self, scale: Optional[Scale] = None) -> Dict[str, int]:
        scale = scale or self.DEFAULT_SCALE
        SCALES = self.SHORT_SCALE if scale == Scale.SHORT else self.LONG_SCALE
        male = {
            **self.ALT_SPELLINGS,
            **{v: k for k, v in self.UNITS.items()},
            **{v: k for k, v in self.TENS.items()},
            **{v: k for k, v in self.HUNDREDS.items()},
            **{v: k for k, v in SCALES.items()},
            **{v: k for k, v in self.GENDERED_SPELLINGS.get(GrammaticalGender.MASCULINE, {}).items()},
        }

        female = {
            **{self.swap_gender(k, GrammaticalGender.FEMININE): v for k, v in male.items()},
            **{v: k for k, v in self.GENDERED_SPELLINGS.get(GrammaticalGender.FEMININE, {}).items()},
        }

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

    def get_ordinal_strings(self, scale: Optional[Scale] = None) -> Dict[str, int]:
        scale = scale or self.DEFAULT_SCALE
        SCALES = self.ORDINAL_SHORT_SCALE if scale == Scale.SHORT else self.ORDINAL_LONG_SCALE
        male = {
            **{v: k for k, v in self.ORDINAL_COMPOUND_UNITS.items()},
            **{v: k for k, v in self.ORDINAL_UNITS.items()},
            **{v: k for k, v in self.ORDINAL_TENS.items()},
            **{v: k for k, v in self.ORDINAL_HUNDREDS.items()},
            **{v: k for k, v in SCALES.items()}
        }
        female = {
            **{self.swap_gender(k, GrammaticalGender.FEMININE): v for k, v in male.items()},
        }
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

    def is_ordinal(self, input_str: str, scale: Optional[Scale] = None) -> Union[int, bool]:
        """
        Determine if a string is an ordinal word.

        Returns:
            (int or bool): the value of the ordinal if the input string is
            recognized as an ordinal, otherwise False.
        """
        scale = scale or self.vocab.DEFAULT_SCALE
        if self.vocab.ORDINAL_PREFIX:
            # drop the ordinal particles ("al doilea" -> "doilea")
            particles = set(self.vocab.ORDINAL_PREFIX.values())
            input_str = " ".join(w for w in input_str.strip().split()
                                 if w not in particles)
        ordinals_map = self.vocab.get_ordinal_strings(scale)
        if input_str in ordinals_map:
            return ordinals_map[input_str]
        return False

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

        # a digit token wins if it appears before any spoken number word
        for tok in tokens:
            t = tok.strip(".,!?;:").replace(",", ".")
            if t and t.lstrip("-").replace(".", "", 1).isdigit():
                val = float(t)
                return int(val) if val.is_integer() else val
            if tok in numbers_map or tok in ordinals_map or tok in scales_map:
                break

        # plural fraction words ("cuartos", "terzos") multiply by the preceding
        # cardinal ("tres cuartos" = 3/4), singular ones add ("dois e meio" = 2.5)
        singular_fractions = set(self.vocab.FRACTION.values()) | set(self.vocab.FRACTION_FEMALE.values())
        plural_fractions = {self.vocab.pluralize(w) for w in singular_fractions} - singular_fractions

        result = 0
        current = 0
        saw_number = False
        is_negative = False

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token in self.vocab.NEGATIVE_SIGN:
                is_negative = True
                i += 1
                continue

            val = numbers_map.get(token)
            if val is not None:
                saw_number = True
                if val >= 1000:
                    # scale multiplier (mil, milhão, ...)
                    if val == 1000:
                        # thousand-level: keep accumulating so a bigger scale
                        # (e.g. milhão) can still multiply the whole group
                        current = (current or 1) * 1000
                    else:
                        current = (current or 1) * val
                        result += current
                        current = 0
                elif val == 100 and self.vocab.MULTIPLY_HUNDREDS:
                    # the hundreds word multiplies the preceding units
                    # ("două sute" = 200, "dos cents" = 200), leaving higher
                    # groups untouched ("două mii trei sute" -> 2000 + 3*100)
                    below = current % 100
                    current += (below or 1) * 100 - below
                else:
                    current += val
                i += 1
                continue

            if ordinals and self.is_ordinal(token):
                saw_number = True
                current += ordinals_map[token]
                i += 1
                continue

            fraction = self.is_fractional(token)
            if fraction is not False:
                saw_number = True
                next_token = tokens[i + 1] if i + 1 < len(tokens) else None
                next_val = numbers_map.get(next_token) if next_token else None
                if token not in plural_fractions and next_val is not None \
                        and next_val >= 1000:
                    # a singular fraction before a scale word multiplies that
                    # scale ("meio milhão" = 500000, "medio millón" = 500000),
                    # so leave it pending for the scale branch to multiply
                    current += fraction
                else:
                    if token in plural_fractions:
                        result += (current or 1) * fraction
                    else:
                        result += current + fraction
                    current = 0
                i += 1
                continue

            if token in self.vocab.DECIMAL_MARKER:
                tail = tokens[i + 1:]
                tail_vals = [numbers_map[t] for t in tail if t in numbers_map]
                if tail_vals and all(
                        0 <= v <= 9 and float(v) == int(v)
                        for v in tail_vals):
                    # digit-by-digit reading ("vírgula um quatro" -> .14)
                    decimal_str = ''.join(str(int(v)) for v in tail_vals)
                else:
                    # composed reading ("vírgula trinta e quatro" -> .34)
                    zeros = 0
                    for t in tail:
                        if numbers_map.get(t) == 0:
                            zeros += 1
                        else:
                            break
                    tail_num = self.extract_number(" ".join(tail))
                    if tail_num is not False and tail_num >= 0 \
                            and float(tail_num) == int(tail_num):
                        decimal_str = "0" * zeros + str(int(tail_num))
                    else:
                        decimal_str = ''
                if decimal_str:
                    result += current + float(f"0.{decimal_str}")
                    current = 0
                    saw_number = True
                    break
                i += 1
                continue

            i += 1

        result += current

        if not saw_number:
            return False

        if is_negative:
            result = -result
        return result

    def numbers_to_digits(self,
                          utterance: str,
                          scale: Optional[Scale] = None
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
        scale = scale or self.vocab.DEFAULT_SCALE
        words = word_tokenize(utterance)
        output = []
        i = 0

        numbers_map = self.vocab.get_number_strings(scale)

        def next_word(idx):
            return words[idx + 1] if idx + 1 < len(words) else None

        def continues_span(idx):
            w = words[idx]
            if w in numbers_map or w in self.vocab.JOIN_WORD:
                return True
            # a negative sign or decimal marker only extends a span if it is
            # immediately followed by a number word ("menos vinte", "tres coma catorze")
            if w in self.vocab.NEGATIVE_SIGN or w in self.vocab.DECIMAL_MARKER:
                return next_word(idx) in numbers_map
            return False

        def starts_span(idx):
            w = words[idx]
            if w in numbers_map:
                return True
            if w in self.vocab.NEGATIVE_SIGN:
                return next_word(idx) in numbers_map
            return False

        while i < len(words):
            # Look for the start of a number span
            if starts_span(i):
                # Start a new span
                number_span_words = []
                j = i
                while j < len(words) and continues_span(j):
                    number_span_words.append(words[j])
                    j += 1

                # a joiner at the end of the span belongs to the surrounding
                # text ("trei de mere" -> "3 de mere"), not to the number
                while number_span_words and number_span_words[-1] in self.vocab.JOIN_WORD:
                    number_span_words.pop()
                    j -= 1

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
                         scale: Optional[Scale] = None,
                         ordinals: bool = False,
                         digits: DigitPronunciation = DigitPronunciation.FULL_NUMBER,
                         gender: GrammaticalGender = GrammaticalGender.MASCULINE,
                         _force_hundreds_join: bool = False,
                         _under_higher_scale: bool = False
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
        scale = scale or self.vocab.DEFAULT_SCALE
        if not isinstance(number, (int, float)):
            raise TypeError("Number must be an int or float.")

        if ordinals:
            return self.pronounce_ordinal(number, gender, scale)

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
                        decimal_pronunciation_parts.append(self._pronounce_up_to_999(last_digit, gender=gender))
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
            return self._pronounce_up_to_999(n, gender, _force_hundreds_join,
                                             terminal_group=not _under_higher_scale)

        scales_map = self.vocab.SHORT_SCALE if scale == Scale.SHORT else self.vocab.LONG_SCALE

        # Find the largest scale that fits the number
        scale_candidates = [(scale_val, scale_str)
                            for scale_val, scale_str in scales_map.items()
                            if n >= scale_val]
        scale_val: Tuple[int, str] = max(scale_candidates, key=lambda x: x[0])

        count = n // scale_val[0]
        remainder = n % scale_val[0]

        # Pronounce the 'count' part of the number
        is_singular = count == 1 or scale_val[0] in self.vocab.NO_PLURAL
        scale_word = scale_val[1] if is_singular else self.vocab.pluralize(scale_val[1])
        # any group nested under this scale must not force a terminal conjunction
        nested_under_higher = _under_higher_scale or scale_val[0] >= 10 ** 6
        if count == 1 and scale_val[0] in self.vocab.SCALE_ONE:
            count_str = self.vocab.SCALE_ONE[scale_val[0]]
        elif count == 1 and scale_val[0] in self.vocab.NO_PREV_UNIT:
            count_str = scale_word
        else:
            count_gender = self.vocab.SCALE_GENDERS.get(scale_val[0],
                                                        GrammaticalGender.MASCULINE)
            count_pronunciation = self.pronounce_number(count, places, scale,
                                                        gender=count_gender,
                                                        _under_higher_scale=True)
            # counts ending in 00 or 20-99 link to the scale word
            # ("douăzeci de mii")
            if self.vocab.SCALE_LINKER and (count % 100 == 0 or count % 100 >= 20):
                count_str = f"{count_pronunciation} {self.vocab.SCALE_LINKER} {scale_word}"
            else:
                count_str = f"{count_pronunciation} {scale_word}"

        # If there's no remainder, we're done
        if remainder == 0:
            return count_str

        # the sub-1000 remainder that directly follows the thousands group of a
        # number below one million takes the terminal conjunction on its hundreds
        remainder_force = scale_val[0] == 1000 and not _under_higher_scale \
            and self.vocab.JOINER_ON_SCALE_REMAINDER
        remainder_str = self.pronounce_number(remainder, places, scale,
                                              _force_hundreds_join=remainder_force,
                                              _under_higher_scale=nested_under_higher)
        # Conjunction logic: add JOIN_WORD if the remainder is the last group and is
        # less than 100 or a multiple of 100.
        join_word = self.vocab.JOIN_WORD[0] if len(self.vocab.JOIN_WORD) else ""
        if self.vocab.JOINER_ON_SCALE_REMAINDER and \
                (remainder < 100 or (remainder < 1000 and remainder % 100 == 0
                                     and self.vocab.JOINER_ON_THOUSANDS)):
            return f"{count_str} {join_word} {remainder_str}"
        else:
            return f"{count_str} {remainder_str}"

    def pronounce_fraction(self,
                           word: str,
                           scale: Optional[Scale] = None) -> str:
        """
        Return the pronunciation of a fraction given as a string (e.g., "1/2").

        The numerator is pronounced as a cardinal number, and the denominator as an ordinal or fraction name, pluralized if appropriate. For denominators not in the known fraction list, the denominator is pronounced as a cardinal number followed by "avos" if plural.

        Parameters:
            word (str): Fraction in the form "numerator/denominator" (e.g., "3/4").

        Returns:
            str: The pronunciation of the fraction.
        """
        scale = scale or self.vocab.DEFAULT_SCALE
        n1, n2 = word.split("/")
        n1_int, n2_int = int(n1), int(n2)

        if n1_int == 1 and n2_int in self.vocab.FRACTION_ONE:
            # "1/x" fractions with an article ("o jumătate", "un sfert")
            return self.vocab.FRACTION_ONE[n2_int]

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
        numerator_gender = self.vocab.FRACTION_NUMERATOR_GENDER or GrammaticalGender.MASCULINE
        num = self.pronounce_number(n1_int, scale=scale, gender=numerator_gender)
        return f"{num} {denom}"

    def pronounce_ordinal(self,
                          number: Union[int, float],
                          gender: GrammaticalGender = GrammaticalGender.MASCULINE,
                          scale: Optional[Scale] = None
                          ) -> str:
        result = self._pronounce_ordinal_core(number, gender, scale)
        prefix = self.vocab.ORDINAL_PREFIX.get(gender)
        if prefix and number > 0 and int(number) not in self.vocab.ORDINAL_UNPREFIXED:
            result = f"{prefix} {result}"
        return result

    def _pronounce_ordinal_core(self,
                                number: Union[int, float],
                                gender: GrammaticalGender = GrammaticalGender.MASCULINE,
                                scale: Optional[Scale] = None
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
        scale = scale or self.vocab.DEFAULT_SCALE
        if not isinstance(number, (int, float)):
            raise TypeError("Number must be an int or float.")
        if number == 0:
            return self.vocab.UNITS[0]

        if number < 0:
            return f"{self.vocab.NEGATIVE_SIGN[0]} {self._pronounce_ordinal_core(abs(number), gender, scale)}"

        n = int(number)
        if n < 1000:
            return self._pronounce_ordinal_up_to_999(n, gender)

        scales_map = self.vocab.ORDINAL_SHORT_SCALE if scale == Scale.SHORT else self.vocab.ORDINAL_LONG_SCALE

        # Find the largest scale that fits the number
        scale_candidates = [(scale_val, scale_str)
                            for scale_val, scale_str in scales_map.items()
                            if n >= scale_val]
        scale_val: Tuple[int, str] = max(scale_candidates, key=lambda x: x[0])

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
        remainder_str = self._pronounce_ordinal_core(remainder, gender, scale)

        return f"{count_str} {remainder_str}"

    def _pronounce_up_to_999(self,
                             n: int,
                             gender: GrammaticalGender = GrammaticalGender.MASCULINE,
                             force_hundreds_join: bool = False,
                             terminal_group: bool = True
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

        def gendered(val: int, base: str) -> str:
            # prefer an explicit gendered spelling, else derive it via swap_gender
            special = self.vocab.GENDERED_SPELLINGS.get(gender, {}).get(val)
            if special is not None:
                return special
            # base spellings are already masculine/neutral, only derive for other genders
            if gender == GrammaticalGender.MASCULINE:
                return base
            return self.vocab.swap_gender(base, gender)

        if n in self.vocab.GENDERED_SPELLINGS.get(gender, {}):
            return self.vocab.GENDERED_SPELLINGS[gender][n]
        if n in self.vocab.UNITS:
            return gendered(n, self.vocab.UNITS[n])
        if n in self.vocab.TENS:
            return gendered(n, self.vocab.TENS[n])
        if n in self.vocab.HUNDREDS:
            return gendered(n, self.vocab.HUNDREDS[n])

        parts = []
        tens_map = self.vocab.TENS

        # Hundreds
        if n >= 100:
            hundred = n // 100 * 100
            if hundred == 100:
                parts.append(self.vocab.HUNDRED_PARTICLE)
            else:
                parts.append(gendered(hundred, self.vocab.HUNDREDS[hundred]))
            n %= 100
            if n > 0 and self.vocab.JOIN_WORD:
                # a conjunction between the hundreds and the rest of the group is
                # used when the language always joins, when the terminal group of a
                # thousands-number forces it, or - for languages that opt in - after
                # the "hundred" particle of a top-level group ("cento e vinte e tres")
                join = self.vocab.JOINER_ON_HUNDREDS or force_hundreds_join
                if hundred == 100 and self.vocab.JOINER_ON_HUNDRED_PARTICLE and terminal_group:
                    join = True
                if join:
                    parts.append(self.vocab.JOIN_WORD[0])

        # Tens and Units
        if n > 0:
            if n < 20:
                base = tens_map.get(n) or self.vocab.UNITS.get(n, "")
                parts.append(gendered(n, base))
            else:
                ten = n // 10 * 10
                unit = n % 10
                parts.append(gendered(ten, tens_map[ten]))
                if unit > 0:
                    if self.vocab.JOINER_ON_TWENTYS and self.vocab.JOIN_WORD \
                            and (ten == 20 or not self.vocab.JOINER_ONLY_ON_TWENTYS):
                        parts.append(self.vocab.JOIN_WORD[0])
                    parts.append(gendered(unit, self.vocab.UNITS[unit]))

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
            if self.vocab.ORDINAL_COMPOUND_CARDINAL_TENS and n >= 20 and n % 10 != 0:
                # cardinal tens joined to an ordinal unit
                # ("al douăzeci și unulea")
                ten = n // 10 * 10
                unit = n % 10
                unit_word = self.vocab.ORDINAL_COMPOUND_UNITS.get(
                    unit, self.vocab.ORDINAL_UNITS[unit])
                joiner = f" {self.vocab.JOIN_WORD[0]} " if self.vocab.JOIN_WORD else " "
                parts.append(f"{self.vocab.TENS[ten]}{joiner}"
                             f"{self.vocab.swap_gender(unit_word, gender)}")
            elif self.vocab.ORDINAL_COMPOUND_CARDINAL_TENS and n in self.vocab.ORDINAL_TENS:
                # exact single-word entry for 11-19 ("treisprezecelea")
                parts.append(self.vocab.swap_gender(self.vocab.ORDINAL_TENS[n], gender))
            # Ordinal numbers don't use 'e' as a separator
            elif n % 10 == 0:
                tens_word_masc = self.vocab.ORDINAL_TENS[n]
                parts.append(self.vocab.swap_gender(tens_word_masc, gender))
            elif n < 10:
                units_word_masc = self.vocab.ORDINAL_UNITS[n]
                parts.append(self.vocab.swap_gender(units_word_masc, gender))
            elif self.vocab.PREFER_EXPLICIT_ORDINALS and n in self.vocab.ORDINAL_TENS:
                # explicit compound ordinal ("onzen", "vint-e-unen")
                parts.append(self.vocab.swap_gender(self.vocab.ORDINAL_TENS[n], gender))
            elif n < 20:
                tens_word_masc = self.vocab.ORDINAL_TENS[10]
                units_word_masc = self.vocab.ORDINAL_UNITS[n - 10]
                parts.append(f"{self.vocab.swap_gender(tens_word_masc, gender)} {self.vocab.swap_gender(units_word_masc, gender)}")
            else:
                tens_word_masc = self.vocab.ORDINAL_TENS[n // 10 * 10]
                units_word_masc = self.vocab.ORDINAL_UNITS[n % 10]
                parts.append(f"{self.vocab.swap_gender(tens_word_masc, gender)} {self.vocab.swap_gender(units_word_masc, gender)}")

        return self.vocab.swap_gender(" ".join(parts), gender)
