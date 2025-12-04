from ovos_number_parser.util import (Scale, GrammaticalGender, DigitPronunciation,
                                     NumberVocabulary, RomanceNumberExtractor)
from typing import Union


def swap_gender_ast(word: str, gender: GrammaticalGender) -> str:
    """Swap ordinal/adjective endings between masculine and feminine where applicable.

    For Asturian, ordinals typically end in -u (masc.) and -a (fem.).
    """
    if gender == GrammaticalGender.FEMININE:
        if word.endswith('u'):
            return word[:-1] + 'a'
        if word.endswith('imu'):
            return word[:-1] + 'a'
    else:
        if word.endswith('a'):
            return word[:-1] + 'u'
    return word


def pluralize_ast(word: str):
    # TODO - is this accurate?
    if word.endswith("ón"):
        return word[:-2] + "ones"
    if not word.endswith("u"):
        return word[:-1] + "os"
    if not word.endswith("s"):
        return word + "s"
    return word


AST = NumberVocabulary(
    LANG="ast",
    swap_gender=swap_gender_ast,  # used for female forms
    pluralize=pluralize_ast,  # use for plural forms

    HUNDRED_PARTICLE="ciento",  # how to read "1XX"
    DENOMINATOR_PARTICLE="avos",  # for fractions  X / N {PARTICLE}
    DIVIDED_BY_ZERO="a dividir por zero",  # how to read X/0 values
    NO_PREV_UNIT=[100, 1000],  # "mil" vs "um mil"  / "cem" vs "um cem"
    NO_PLURAL=[1000],  # "dois mil" vs "dois mils" / "dois milhões" vs "dois milhão"

    NUMBER_OVERFLOW="número exageradamente grande",
    DEFAULT_SCALE=Scale.LONG,
    JOIN_WORD=["y"],

    JOINER_ON_TWENTYS=True,  # add JOIN_WORD from 20-30 - "vinte e um"
    JOINER_ON_HUNDREDS=False,  # add JOIN_WORD from 100-1000 - "duzentos e um"
    JOINER_ON_THOUSANDS=False,  # add JOIN_WORD from 1000-10000 - "mil e duzentos"


    DECIMAL_MARKER=["punto", "coma", ".", ","],
    NEGATIVE_SIGN=["menos"],
    UNITS={
        0: 'cero',
        1: 'un',
        2: 'dos',
        3: 'tres',
        4: 'cuatro',
        5: 'cinco',
        6: 'seis',
        7: 'siete',
        8: 'ocho',
        9: 'nueve'
    },
    TENS={
        10: 'diez',
        11: 'once',
        12: 'doce',
        13: 'trece',
        14: 'catorce',
        15: 'quince',
        16: 'dieciséis',
        17: 'diecisiete',
        18: 'dieciocho',
        19: 'diecinueve',
        20: 'venti',
        21: 'ventiuno',
        22: 'ventidós',
        23: 'ventitrés',
        24: 'venticuatro',
        25: 'venticinco',
        26: 'ventiséis',
        27: 'ventisiete',
        28: 'ventiocho',
        29: 'ventinueve',
        30: 'trenta',
        40: 'cuarenta',
        50: 'cincuenta',
        60: 'sesenta',
        70: 'setenta',
        80: 'ochenta',
        90: 'noventa'
    },
    HUNDREDS={
        100: 'cien',
        200: 'doscientos',
        300: 'trescientos',
        400: 'cuatrocientos',
        500: 'quinientos',
        600: 'seiscientos',
        700: 'setecientos',
        800: 'ochocientos',
        900: 'novecientos'
    },
    FRACTION={
        2: 'mediu',
        3: 'terciu',
        4: 'cuartu',
        5: 'quintu',
        6: 'sestu',
        7: 'séptimu',
        8: 'octavu',
        9: 'novenu',
        10: 'décimu',
        11: 'onceavos',
        12: 'doceavos'
    },
    FRACTION_FEMALE={
        2: "media"  # una y media -> 1.5
    },
    SHORT_SCALE={
        10 ** 6: "millón",
        10 ** 3: "mil"
    },
    LONG_SCALE={
        10 ** 6: "millón",
        10 ** 3: "mil"
    },

    GENDERED_SPELLINGS={
        GrammaticalGender.FEMININE: {
            1: "una"
        }
    },
    DIGIT_SPELLINGS={},
    ALT_SPELLINGS={

    },
    ORDINAL_UNITS={
        1: 'primeru',
        2: 'segundu',
        3: 'terceru',
        4: 'cuartu',
        5: 'quintu',
        6: 'sestu',
        7: 'séptimu',
        8: 'octavu',
        9: 'novenu'
    },
    ORDINAL_TENS={
        10: 'décimu',
        20: 'ventésimu',
        30: 'trentésimu',
        40: 'cuarentenu',
        50: 'cincuentenu',
        60: 'sesentenu',
        70: 'setentenu',
        80: 'ochentenu',
        90: 'noventenu'
    },
    ORDINAL_HUNDREDS={
        # TODO - up to 900
        100: 'centésimu'
    },
    ORDINAL_SHORT_SCALE={
        # TODO - at least up to 10 ** 21
        10 ** 6: "millonésimu",
        10 ** 3: "milésimu"
    },
    ORDINAL_LONG_SCALE={
        # TODO - at least up to 10 ** 36
        10 ** 6: "millonésimu",
        10 ** 3: "milésimu"
    }
)

AST = RomanceNumberExtractor(AST)



def pronounce_ordinal_ast(
        number: Union[int, float],
        gender: GrammaticalGender = GrammaticalGender.MASCULINE,
        scale: Scale = Scale.LONG
) -> str:
    """
    Return the ordinal pronunciation of a number in Portuguese, supporting grammatical gender, scale (short or long), and language variant (Brazilian or European Portuguese).

    Parameters:
        number (int or float): The number to pronounce as an ordinal.
        gender (GrammaticalGender, optional): The grammatical gender for the ordinal form (masculine or feminine).
        scale (Scale, optional): The numerical scale to use (short or long).

    Returns:
        str: The ordinal pronunciation of the number in Portuguese.

    Raises:
        TypeError: If `number` is not an int or float.
    """
    return AST.pronounce_ordinal(number, gender, scale)


def is_fractional_ast(
        input_str: str
) -> Union[float, bool]:
    """
    Checks if the input string corresponds to a recognized Portuguese fractional word.

    Returns:
        The fractional value as a float if recognized (e.g., 0.5 for "meio" or "meia"); otherwise, False.
    """
    return AST.is_fractional(input_str)


def is_ordinal_ast(input_str: str) -> bool:
    """
    Determine if a string is a Portuguese ordinal word.

    Returns:
        bool: True if the input string is recognized as a Portuguese ordinal, otherwise False.
    """
    return AST.is_ordinal(input_str)


def extract_number_ast(
        text: str,
        ordinals: bool = False,
        scale: Scale = Scale.LONG,
) -> Union[int, float, bool]:
    """
    Extracts a numeric value from a Portuguese text phrase, supporting cardinals, ordinals, fractions, and large scales.

    Parameters:
        text (str): The input phrase potentially containing a number.
        ordinals (bool): If True, recognizes ordinal words as numbers.
        scale (Scale): Specifies whether to use the short or long numerical scale.

    Returns:
        int or float: The extracted number if found; otherwise, False.
    """
    return AST.extract_number(text, ordinals, scale)


def pronounce_number_ast(
        number: Union[int, float],
        places: int = 5,
        scale: Scale = Scale.LONG,
        ordinals: bool = False,
        digits: DigitPronunciation = DigitPronunciation.FULL_NUMBER,
        gender: GrammaticalGender = GrammaticalGender.MASCULINE
) -> str:
    """
    Return the full Portuguese pronunciation of a number, supporting cardinal and ordinal forms, decimals, large scales, grammatical gender, and both Brazilian and European Portuguese variants.

    Parameters:
        number (int or float): The number to pronounce.
        places (int): Number of decimal places to include for floats.
        scale (Scale): Numerical scale to use (short or long).
        ordinals (bool): If True, pronounce as an ordinal number.
        gender (GrammaticalGender): Grammatical gender for ordinal numbers.

    Returns:
        str: The number expressed as a Portuguese phrase.
    """
    return AST.pronounce_number(number, places, scale, ordinals, digits, gender)


def numbers_to_digits_ast(
        utterance: str,
        scale: Scale = Scale.LONG
) -> str:
    """
    Converts written Portuguese numbers in a text string to their digit equivalents, preserving all other text.

    Identifies spans of number words (including the joiner "y"), extracts their numeric values, and replaces them with digit strings. Non-number words and context are left unchanged.

    Parameters:
        utterance (str): Input text possibly containing written Portuguese numbers.
        scale (Scale, optional): Numerical scale (short or long) to interpret large numbers. Defaults to Scale.LONG.

    Returns:
        str: The input text with written numbers replaced by their digit representations.
    """
    return AST.numbers_to_digits(utterance, scale)



def pronounce_fraction_ast(word: str, scale: Scale = Scale.LONG) -> str:
    """
    Return the Portuguese pronunciation of a fraction given as a string (e.g., "1/2").

    The numerator is pronounced as a cardinal number, and the denominator as an ordinal or fraction name, pluralized if appropriate. For denominators not in the known fraction list, the denominator is pronounced as a cardinal number followed by "avos" if plural.

    Parameters:
        word (str): Fraction in the form "numerator/denominator" (e.g., "3/4").

    Returns:
        str: The Portuguese pronunciation of the fraction.
    """
    return AST.pronounce_fraction(word, scale)



if __name__ == '__main__':
    print('--- Asturian number tests ---')
    print('16 ->', pronounce_number_ast(16))
    print('21 ->', pronounce_number_ast(21))
    print('35 ->', pronounce_number_ast(35))
    print('101 ->', pronounce_number_ast(101))
    print('1,234 ->', pronounce_number_ast(1234))
    print('1,000,000 ->', pronounce_number_ast(1_000_000))

    print('\n--- Ordinals ---')
    print('1st (m):', pronounce_ordinal_ast(1))
    print('1st (f):', pronounce_ordinal_ast(1, GrammaticalGender.FEMININE))
    print('23rd (m):', pronounce_ordinal_ast(23))
    print('100th:', pronounce_ordinal_ast(100))

    print('\n--- Extraction ---')
    print("'un millón' ->", extract_number_ast('un millón'))
    print("'dos millones trescientos' ->", extract_number_ast('dos millones trescientos'))
    print("'ventiuno' ->", extract_number_ast('ventiuno'))
    print("'tres cuartos' (fraction word) ->", extract_number_ast('tres cuartos'))

    print('\n--- numbers_to_digits_ast ---')
    print(numbers_to_digits_ast('hai dos millones cincuenta persoas'))
    print(numbers_to_digits_ast('merquei ventiuno panes'))
