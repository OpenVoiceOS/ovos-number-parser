import math
import threading
from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP, localcontext
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


def exact_int(value: Any) -> Any:
    """
    Return a whole float as the integer that its literal spells.

    Scale tables write constants as ``1e24``, which is the float nearest to
    10 ** 24 and not 10 ** 24 itself. ``repr`` keeps the written digits, so
    ``exact_int(1e24) == 10 ** 24``. A value that is not a finite whole float
    is returned unchanged.

    Args:
        value: a number from a scale table

    Returns:
        int for a finite whole float, else ``value`` unchanged
    """
    if isinstance(value, float) and math.isfinite(value) and value.is_integer():
        return int(Decimal(repr(value)))
    return value


def exact_sum(values: List[Union[int, float]]) -> float:
    """
    Add numbers as the decimals their literals spell.

    Spoken decimal digits are summed one place at a time ("eins Komma eins
    vier" is 1 + 0.1 + 0.04), and float addition gives 1.1400000000000001.
    ``repr`` keeps the written digits of each part, so the sum is exact
    before it becomes a float.

    Args:
        values: the parts of one number

    Returns:
        float nearest to the exact sum
    """
    return float(sum(Decimal(repr(value)) for value in values))


def is_numeric(input_str: str) -> bool:
    """
    Return True if the input string represents a valid number, otherwise False.

    Parameters:
        input_str (str): The string to test for numeric value.

    Returns:
        bool: True if the string is a finite number or a plain integer string
            that ``int`` can read, False for a non-finite token such as "inf",
            "nan" or "1e309".
    """
    try:
        val = float(input_str)
    except ValueError:
        return False
    if input_str.strip().lstrip("+-").isdigit():
        # a plain integer string is read exactly, even beyond float range.
        # One longer than the interpreter's integer string conversion limit
        # (sys.get_int_max_str_digits) cannot be read or written back, so it
        # carries no usable number
        try:
            int(input_str)
        except ValueError:
            return False
        return True
    return math.isfinite(val)


def fits_str_limit(value: Any) -> bool:
    """
    Return False for an integer that ``str`` cannot write.

    An integer with more digits than the interpreter's integer string
    conversion limit (``sys.get_int_max_str_digits``) has no decimal string.
    It is no number, as a digit string past that limit is none for
    ``is_numeric``.

    Args:
        value: a value an extractor produced

    Returns:
        bool: False for an integer past the limit, else True
    """
    if isinstance(value, int):
        try:
            str(value)
        except ValueError:
            return False
    return True


def numeric_value(input_str: str) -> Union[int, float]:
    """
    Return the value of a string that ``is_numeric`` accepts.

    A plain integer string, signed or not, is read with ``int`` and keeps
    every digit, where ``float`` keeps only about 17 significant digits. Any
    other numeric string, a decimal or an exponent, is read as a float.

    Args:
        input_str (str): a string for which ``is_numeric`` is True

    Returns:
        int for a plain integer string, else float
    """
    if input_str.strip().lstrip("+-").isdigit():
        return int(input_str)
    return float(input_str)


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
            # a zero denominator is not a fraction; callers divide by it, so
            # reject it here rather than raise ZeroDivisionError downstream
            return float(split_list[1]) != 0

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


def scientific_notation(number: Union[int, float]) -> str:
    """
    Format ``number`` as ``'%E' % number`` does, ints beyond the float range
    included.

    ``'%E'`` converts to float, which raises OverflowError for an int such as
    10 ** 400; such an int is then formatted from its exact decimal value.

    Args:
        number (int or float): finite number to format
    Returns:
        (str): the number as "<mantissa>E<signed exponent>", e.g. "1.000000E+400"
    """
    try:
        return '%E' % number
    except OverflowError:
        return format(Decimal(number), '.6E')


def round_half_up(value: Decimal, places: int) -> Decimal:
    """
    ``value`` rounded half away from zero to ``places`` decimals.

    The context precision holds every digit the rounding keeps, so a long
    Decimal or a large ``places`` rounds instead of raising InvalidOperation
    at the default precision of 28 digits.
    """
    with localcontext() as context:
        context.prec = max(context.prec, value.adjusted() + places + 2)
        return value.quantize(Decimal(1).scaleb(-places), ROUND_HALF_UP)


def scientific_parts(number: Union[int, float, Decimal],
                     places: int) -> Tuple[Union[int, float], int]:
    """
    Mantissa and exponent of ``number`` in scientific notation, with the
    mantissa rounded half away from zero to ``places`` decimals.

    The mantissa is rounded from the decimal digits of ``number``, so an int
    or a Decimal beyond the float range rounds exactly. A mantissa that rounds
    to ten carries into the exponent: 9.9996 at 3 places is 1 and exponent 1.

    Args:
        number (int, float or Decimal): finite number to split
        places (int): decimals of the mantissa
    Returns:
        (tuple): the signed mantissa (an int when it has no fraction) and the
            exponent, e.g. (1.235, 400) for 12346 * 10 ** 396 at 3 places
    """
    exact = Decimal(number) if isinstance(number, int) else Decimal(str(number))
    if not exact:
        return 0, 0
    sign, digits, _ = exact.as_tuple()
    exponent = exact.adjusted()
    # decimals past the last digit add nothing but zeros
    places = min(places, len(digits) - 1)
    with localcontext() as context:
        context.prec = len(digits) + 1
        mantissa = Decimal((sign, digits, 1 - len(digits))).quantize(
            Decimal(1).scaleb(-places), ROUND_HALF_UP)
    if abs(mantissa) == 10:
        mantissa, exponent = mantissa / 10, exponent + 1
    if mantissa == mantissa.to_integral_value():
        return int(mantissa), exponent
    return float(mantissa), exponent


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

    # a count of the largest scale word from this value up has no reading in
    # words: it would stack scale words past the compounds the language uses
    # ("trilioane de trilioane"). None reads every count.
    MAX_SCALE_COUNT: Optional[int] = None

    # extraction: the word for 100 multiplies the preceding units
    # ("două sute" = 200) instead of being added to them
    MULTIPLY_HUNDREDS: bool = False

    # extraction: a denominator above ten is the cardinal plus
    # DENOMINATOR_PARTICLE ("doze avos" = 1/12), and a cardinal before it
    # counts the parts ("três doze avos" = 3/12)
    CARDINAL_DENOMINATORS: bool = False

    # extraction: the mark that groups the thousands of a digit string whose
    # decimal mark is the comma ("12.000" = 12000, "1.234,5" = 1234.5).
    # Empty when no such mark is set, and "12.000" reads as 12.0
    DIGIT_GROUP_MARK: str = ""

    # extraction: a fraction noun always multiplies the preceding cardinal
    # ("un quarto" = 1/4, "tre quarti" = 3/4) instead of adding to it, even in
    # its singular form. Languages that also say "e mezzo" ("two and a half")
    # keep this off so the singular still adds.
    FRACTIONS_ALWAYS_MULTIPLY: bool = False

    # extraction: a half right after a scale word is half of the scale ("um
    # milhão e meio" = 1500000, "mil milhões e meio" = 1500000000), not half
    # of one; a decimal reading needs the decimal marker ("um milhão vírgula
    # cinco" = 1000000.5)
    HALF_OF_SCALE: bool = False
    #: scale words that are numerals, not nouns: a half after one of them is
    #: half of one, as after any other numeral ("mil e meio" = 1000.5)
    SCALE_NUMERALS: List[str] = field(default_factory=list)
    #: words that may follow such a half in numbers_to_digits, besides the end
    #: of the text and a joiner: a preposition that opens what is counted ("um
    #: milhão e meio de discos"). Any other word is a noun the half counts
    #: itself ("um milhão e meia dúzia" is a million and half a dozen)
    HALF_OF_SCALE_FOLLOWERS: List[str] = field(default_factory=list)

    # full spelling of "one <scale>" groups when they use an article or a
    # special form of "one" ("o mie", "un milion")
    #: entries of JOIN_WORD that are *not* additive joiners but partitive or
    #: multiplicative prepositions, where the value after the word is larger
    #: than the one before it by design. Romanian inserts "de" before a scale
    #: above twenty ("douăzeci de mii" = 20 x 1000) and before a fraction's
    #: base ("jumătate de milion" = half *of* a million), unlike the additive
    #: "și" ("douăzeci și unu" = 21). Listed here so the descending-joiner rule
    #: skips them.
    MULTIPLICATIVE_JOIN_WORD: List[str] = field(default_factory=list)
    #: fixed phrases that hold a NEGATIVE_SIGN word without a sign meaning
    #: ("pelo menos" = at least): the minus word in them never signs a number
    NEGATIVE_IDIOMS: List[Tuple[str, ...]] = field(default_factory=list)

    SCALE_ONE: Dict[int, str] = field(default_factory=dict)

    # grammatical gender the count before each scale word agrees with
    # ("două mii" - feminine "două", not masculine "doi")
    SCALE_GENDERS: Dict[int, GrammaticalGender] = field(default_factory=dict)
    # scale words that are not nouns: a feminine count before them agrees
    # with the counted noun ("setecientas mil toneladas")
    AGREEING_SCALES: List[int] = field(default_factory=list)
    # the group after a scale word agrees with the counted noun
    # ("mil doscientas personas")
    AGREE_AFTER_SCALE: bool = False

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

    def _signs(self, tokens: List[str], idx: int, numbers_map: Dict[str, Any]) -> bool:
        """
        Tell if the NEGATIVE_SIGN word at tokens[idx] signs the number after it.

        The word signs a number only as a prefix: a number must follow it, no
        number may come before it ("tres menos dos" is a subtraction), nor a
        token that starts with digits ("9h moins 10" is clock time), and it
        must not be part of a NEGATIVE_IDIOMS phrase ("pelo menos tres").
        """
        def is_number(tok: str) -> bool:
            digits = tok.rstrip(".,!?;:").replace(",", ".").removeprefix("-")
            return tok in numbers_map or self.is_fractional(tok) is not False \
                or digits.replace(".", "", 1).isdecimal()

        if idx + 1 >= len(tokens) or not is_number(tokens[idx + 1]):
            return False
        if idx and (is_number(tokens[idx - 1])
                    or tokens[idx - 1].removeprefix("-")[:1].isdigit()):
            return False
        for idiom in self.vocab.NEGATIVE_IDIOMS:
            for k, word in enumerate(idiom):
                start = idx - k
                if word == tokens[idx] and start >= 0 \
                        and tuple(tokens[start:start + len(idiom)]) == idiom:
                    return False
        return True

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
        # no text, no number: honour the "no number" sentinel instead of
        # raising on None or other non-string input
        if not isinstance(text, str):
            return False

        scale = scale or self.vocab.DEFAULT_SCALE
        numbers_map = self.vocab.get_number_strings(scale)
        ordinals_map = self.vocab.get_ordinal_strings(scale)
        scales_map = self.vocab.SHORT_SCALE if scale == Scale.SHORT else self.vocab.LONG_SCALE

        # normalize and tokenize; a hyphen joins words ("vinte-e-dois"), but
        # a hyphen that opens a token before a digit or a decimal separator
        # is the minus sign ("-12", "-.5")
        clean_text = re.sub(r"(?<=\S)-|-(?![.,]?\d)", " ", text.lower())
        # the joiner is kept: it is what tells "vinte e um" (21, one number)
        # apart from "tres e vinte" (3 and 20, two numbers)
        tokens = clean_text.split()

        # a digit token wins if it appears before any spoken number word
        group = self.vocab.DIGIT_GROUP_MARK
        # a group number never starts with 0 ("0.500" is a decimal)
        grouped = re.compile(rf"-?[1-9]\d{{0,2}}(?:{re.escape(group)}\d{{3}})+(?:,\d+)?")
        for idx, tok in enumerate(tokens):
            # a leading decimal separator belongs to the number (".5")
            t = tok.rstrip(".,!?;:").lstrip("!?;:")
            if group and grouped.fullmatch(t):
                t = t.replace(group, "")
            t = t.replace(",", ".")
            if t and t.lstrip("-").replace(".", "", 1).isdecimal():
                # an out-of-range token (a 400-digit decimal, or a digit
                # string longer than int() reads) carries no usable number,
                # so skip it rather than return a non-finite value
                if not is_numeric(t):
                    continue
                val = numeric_value(t)
                if idx and tokens[idx - 1] in self.vocab.NEGATIVE_SIGN \
                        and self._signs(tokens, idx - 1, numbers_map):
                    # the minus word signs digits as it signs number words
                    sign = -1
                else:
                    sign = 1
                if val == int(val):
                    # a whole float rounds the digit string; above 2 ** 53
                    # it also drops digits of the whole part
                    return sign * int(Decimal(t).to_integral_value(ROUND_HALF_UP))
                return sign * val
            if tok in numbers_map or tok in ordinals_map or tok in scales_map:
                break

        # plural fraction words ("cuartos", "terzos") multiply by the preceding
        # cardinal ("tres cuartos" = 3/4), singular ones add ("dois e meio" = 2.5)
        singular_fractions = set(self.vocab.FRACTION.values()) | set(self.vocab.FRACTION_FEMALE.values())
        scales_words = {w for w, v in numbers_map.items() if v >= 1000}
        plural_fractions = {self.vocab.pluralize(w) for w in singular_fractions} - singular_fractions
        particle = self.vocab.DENOMINATOR_PARTICLE
        cardinal_denominators = self.vocab.CARDINAL_DENOMINATORS

        result = 0
        current = 0
        largest_scale = 0
        # the value of the run of scale words just read ("mil milhões" =
        # 10 ** 9), 0 once another number word follows
        trailing_scale = 0
        # the last scale word read, which decides what a half after it halves
        last_scale_word = None
        saw_number = False
        is_negative = False
        # the value of ``current`` where a second cardinal follows a cardinal
        # below 1000 with no joiner: "três doze" is 3 and 12, not one number
        numerator = None

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token in self.vocab.NEGATIVE_SIGN:
                if self._signs(tokens, i, numbers_map):
                    if saw_number:
                        # a signed number after a number is a second number
                        break
                    is_negative = True
                elif saw_number:
                    break
                i += 1
                continue

            if token in self.vocab.JOIN_WORD:
                if token in self.vocab.MULTIPLICATIVE_JOIN_WORD:
                    i += 1
                    continue
                # Romance additive joiners are strictly descending: the value
                # after the joiner is smaller than the one before it
                # ("vinte e um" = 21, "mil e quinhentos" = 1500). An ascending
                # pair is not one number but two ("tres y veinte" = "3:20"),
                # so the number ends here.
                nxt = numbers_map.get(tokens[i + 1]) if i + 1 < len(tokens) else None
                pending = current or result
                if saw_number and nxt is not None and pending and nxt >= pending:
                    break
                i += 1
                continue

            val = numbers_map.get(token)
            if val is not None:
                saw_number = True
                if val >= 1000:
                    after_scale = i and tokens[i - 1] in scales_words
                    trailing_scale = (trailing_scale if after_scale else 1) * val
                    last_scale_word = token
                else:
                    trailing_scale = 0
                if val >= 1000:
                    # scale multiplier (mil, milhão, ...)
                    if val == 1000:
                        # thousand-level: keep accumulating so a bigger scale
                        # (e.g. milhão) can still multiply the whole group
                        current = (current or 1) * 1000
                    elif val > largest_scale:
                        # a scale word above every scale before it
                        # multiplies the whole number so far ("dotze milions
                        # bilions" = 12 * 10 ** 6 * 10 ** 12)
                        result = (result + current or 1) * val
                        current = 0
                    else:
                        current = (current or 1) * val
                        result += current
                        current = 0
                    largest_scale = max(largest_scale, val)
                elif val == 100 and self.vocab.MULTIPLY_HUNDREDS:
                    # the hundreds word multiplies the preceding units
                    # ("două sute" = 200, "dos cents" = 200), leaving higher
                    # groups untouched ("două mii trei sute" -> 2000 + 3*100)
                    below = current % 100
                    current += (below or 1) * 100 - below
                else:
                    if i and val < 1000 and numbers_map.get(tokens[i - 1], 1000) < 1000:
                        numerator = current
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
                # look past a joiner: the scale a fraction multiplies may sit
                # behind one ("jumătate de milion" = half a million)
                nxt_i = i + 1
                while nxt_i < len(tokens) and tokens[nxt_i] in self.vocab.JOIN_WORD:
                    nxt_i += 1
                next_token = tokens[nxt_i] if nxt_i < len(tokens) else None
                next_val = numbers_map.get(next_token) if next_token else None
                if token not in plural_fractions and next_val is not None \
                        and next_val >= 1000:
                    # a singular fraction before a scale word multiplies that
                    # scale ("meio milhão" = 500000, "medio millón" = 500000),
                    # so leave it pending for the scale branch to multiply
                    current += fraction
                else:
                    count = numbers_map.get(tokens[i - 1]) if i else None
                    if token in plural_fractions or self.vocab.FRACTIONS_ALWAYS_MULTIPLY:
                        result += (current or 1) * fraction
                    elif count is not None and count < 1000:
                        # a cardinal said right before a singular fraction
                        # counts its parts ("um quinto" = 1/5), and only a
                        # joiner makes the fraction add ("dois e meio" = 2.5)
                        result += current - count + count * fraction
                    elif self.vocab.HALF_OF_SCALE and trailing_scale and fraction == 0.5 \
                            and last_scale_word not in self.vocab.SCALE_NUMERALS:
                        part = fraction * trailing_scale
                        result += current + (int(part) if part == int(part) else part)
                    else:
                        result += current + fraction
                    current = 0
                    numerator = None
                trailing_scale = 0
                i += 1
                continue

            # "doze vinte e cinco avos" = 12/25: the cardinal before the
            # particle is the denominator, a cardinal before that counts
            denominator = current - (numerator or 0)
            if token == particle and cardinal_denominators and denominator > 10 \
                    and i and tokens[i - 1] in numbers_map:
                result += (1 if numerator is None else numerator) / denominator
                current = 0
                numerator = None
                saw_number = True
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

            trailing_scale = 0
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
        numbers_map = self.vocab.get_number_strings(scale)
        particle = self.vocab.DENOMINATOR_PARTICLE
        cardinal_denominators = self.vocab.CARDINAL_DENOMINATORS
        singular_fractions = set(self.vocab.FRACTION.values()) | set(self.vocab.FRACTION_FEMALE.values())
        # a hyphen chain of number words around a joiner is one spoken
        # number ("vinte-e-dois"); without a joiner it is a range
        # ("doi-trei"), and other hyphenated words keep their hyphens
        joiners = set(self.vocab.JOIN_WORD) - set(self.vocab.MULTIPLICATIVE_JOIN_WORD)
        half_words = {self.vocab.FRACTION.get(2), self.vocab.FRACTION_FEMALE.get(2)} - {None}
        utterance = re.sub(
            r"[^\W\d_]+(?:-[^\W\d_]+)+",
            lambda m: m.group().replace("-", " ") if all(
                w in numbers_map or w in joiners
                for w in m.group().split("-"))
            and joiners & set(m.group().split("-")) else m.group(),
            utterance)
        words = word_tokenize(utterance)
        output = []
        i = 0

        def next_word(idx):
            return words[idx + 1] if idx + 1 < len(words) else None

        def continues_span(idx):
            w = words[idx]
            if w in numbers_map or w in self.vocab.JOIN_WORD:
                return True
            # a decimal marker only extends a span if it is immediately
            # followed by a number word ("tres coma catorze")
            if w in self.vocab.DECIMAL_MARKER:
                return next_word(idx) in numbers_map
            return False

        def starts_span(idx):
            w = words[idx]
            if w in numbers_map:
                return True
            # a sign word opens a span before a number word ("menos vinte")
            if w in self.vocab.NEGATIVE_SIGN:
                return next_word(idx) in numbers_map \
                    and self._signs(words, idx, numbers_map)
            return False

        while i < len(words):
            # Look for the start of a number span
            if starts_span(i):
                # Start a new span
                number_span_words = []
                j = i
                if words[i] in self.vocab.NEGATIVE_SIGN:
                    number_span_words.append(words[i])
                    j += 1
                while j < len(words) and continues_span(j):
                    if words[j] in self.vocab.JOIN_WORD and number_span_words \
                            and words[j] not in self.vocab.MULTIPLICATIVE_JOIN_WORD:
                        # the span only crosses a joiner when the value after
                        # it is smaller than the value before it ("vinte e um").
                        # An ascending pair is two numbers, not one, and the
                        # span has to end so the tail survives ("tres y veinte").
                        nxt = numbers_map.get(next_word(j))
                        sofar = self.extract_number(" ".join(number_span_words))
                        if nxt is None or sofar is False or nxt >= sofar:
                            break
                    number_span_words.append(words[j])
                    j += 1

                # a joiner at the end of the span belongs to the surrounding
                # text ("trei de mere" -> "3 de mere"), not to the number
                while number_span_words and number_span_words[-1] in self.vocab.JOIN_WORD:
                    number_span_words.pop()
                    j -= 1

                if self.vocab.HALF_OF_SCALE and number_span_words \
                        and numbers_map.get(number_span_words[-1], 0) >= 1000 \
                        and number_span_words[-1] not in self.vocab.SCALE_NUMERALS \
                        and j + 1 < len(words) and words[j] in joiners \
                        and words[j + 1] in half_words \
                        and (j + 2 == len(words) or words[j + 2] in joiners
                             or words[j + 2] in self.vocab.HALF_OF_SCALE_FOLLOWERS):
                    # a half right after a scale word that is not a numeral
                    # is half of that scale ("um milhão e meio" = 1500000),
                    # as extract_number reads it
                    number_span_words += words[j:j + 2]
                    j += 2

                if words[j:j + 1] == [particle] and cardinal_denominators:
                    # "três doze avos" holds two numbers, the count and the
                    # denominator: end the span where the denominator starts
                    for k in range(len(number_span_words) - 1, 0, -1):
                        if numbers_map.get(number_span_words[k - 1], 1000) < 1000 \
                                and numbers_map.get(number_span_words[k], 1000) < 1000:
                            del number_span_words[k:]
                            j = i + k
                            break
                elif j < len(words) and len(number_span_words) > 2 \
                        and number_span_words[-2] in joiners \
                        and words[j] in singular_fractions:
                    # the cardinal before a singular fraction counts its parts
                    # and is a number of its own: "dois e um quarto" is 2 and
                    # 1/4, so the span ends before the joiner
                    del number_span_words[-2:]
                    j -= 2

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
                         _under_higher_scale: bool = False,
                         _fraction_digits: bool = False
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

        # Non-finite floats (nan, inf) have no spoken numeric form; return a
        # clean textual sentinel rather than crashing downstream int() calls.
        if isinstance(number, float) and not math.isfinite(number):
            return str(number)

        if ordinals:
            return self.pronounce_ordinal(number, gender, scale)

        if number < 0:
            return f"{self.vocab.NEGATIVE_SIGN[0]} {self.pronounce_number(abs(number), places, scale=scale, digits=digits, gender=gender)}"

        # Normalize the textual form so very large or scientific-notation floats
        # (e.g. 6.022e23 -> "602200000000000000000000") do not leak an "e" into
        # the decimal-splitting / int() logic below and crash.
        num_str = str(number)
        if isinstance(number, float) and ("e" in num_str or "E" in num_str):
            num_str = format(Decimal(num_str), 'f')

        # Handle decimals
        if "." in num_str:
            integer_part = int(number)
            decimal_part_str = num_str.split('.')[1].rstrip("0")

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
                        decimal_pronunciation_parts.append(self.pronounce_number(
                            int(decimal_part_str), gender=gender, _fraction_digits=True))
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
        # the digits after the decimal marker keep their reading in words
        if self.vocab.MAX_SCALE_COUNT and count >= self.vocab.MAX_SCALE_COUNT \
                and not _fraction_digits:
            raise OverflowError(f"no scale word for {n}")

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
            if gender == GrammaticalGender.FEMININE and \
                    scale_val[0] in self.vocab.AGREEING_SCALES:
                count_gender = gender
            else:
                count_gender = self.vocab.SCALE_GENDERS.get(scale_val[0],
                                                            GrammaticalGender.MASCULINE)
            count_pronunciation = self.pronounce_number(count, places, scale,
                                                        gender=count_gender,
                                                        _under_higher_scale=True,
                                                        _fraction_digits=_fraction_digits)
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
        remainder_gender = gender if self.vocab.AGREE_AFTER_SCALE \
            else GrammaticalGender.MASCULINE
        remainder_str = self.pronounce_number(remainder, places, scale,
                                              gender=remainder_gender,
                                              _force_hundreds_join=remainder_force,
                                              _under_higher_scale=nested_under_higher,
                                              _fraction_digits=_fraction_digits)
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
            if n in tens_map:
                # a fused single-word spelling covers the whole 1-99 remainder:
                # teens and round tens for every language, plus the fused
                # twenties some languages write solid ("veintitrés", "vintiún")
                parts.append(gendered(n, tens_map[n]))
            elif n < 20:
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


#: re-entrancy guard for :func:`leftmost_separated_number`. The span scanner
#: calls the language extractors back, and those extractors call this helper,
#: so without the guard the first call would never return.
_LEFTMOST_SCAN = threading.local()


def leftmost_separated_number(text: str, lang: str, ordinals: bool
                              ) -> Optional[Union[int, float]]:
    """The leftmost number of a line that holds several separated numbers.

    Under ``ordinals=True`` a line can hold an ordinal and a cardinal, and
    the languages did not agree on which one answers. The rule is that the
    number written first wins, whether it is the ordinal or the cardinal.

    The rule covers numbers that other words separate, and only those.
    Whether an adjacent cardinal-then-ordinal pair reads as a fraction and
    collapses into one span is a property of the locale, not a general rule
    of :func:`ovos_number_parser.extract_number_spans`. In German
    ("zwei drittel") and Danish ("to tredje") that order is one span, so the
    rule never reaches it; the ordinal-then-cardinal order in those same
    languages stays two spans. English reads the singular pair ("two
    third", "third two") as one span in both orders, while the plural
    ("two thirds") stays two spans. Kabyle ("sin wis kṛaḍ") stays two spans
    in both orders. The rule reaches a locale's adjacent pair exactly when
    the pair is two spans.

    Args:
        text: the line to read.
        lang: BCP-47 language code.
        ordinals: the caller's flag. The rule applies under True alone.

    Returns:
        The value of the first span, or ``None`` when the rule does not
        apply: ``ordinals`` is False, the text is not a string, the line
        holds fewer than two number spans, or the call is already inside a
        span scan.
    """
    if not ordinals or not isinstance(text, str):
        return None
    if len(word_tokenize(text)) < 2:
        # extract_number_spans can answer two spans only when the line
        # itself holds two or more words; word_tokenize splits at least as
        # often as the span scanner's own word boundaries, so this can
        # never skip a line the scan would have found two spans in.
        return None
    if getattr(_LEFTMOST_SCAN, "active", False):
        return None
    _LEFTMOST_SCAN.active = True
    try:
        from ovos_number_parser import extract_number_spans
        spans = extract_number_spans(text, lang, ordinals=True)
    except Exception:
        # the rule never turns a readable line into an error; the language's
        # own extractor answers instead
        return None
    finally:
        _LEFTMOST_SCAN.active = False
    if len(spans) < 2:
        return None
    return spans[0].value
