from enum import Enum
from typing import Union

from ovos_number_parser.util import (Scale, GrammaticalGender,
                                     DigitPronunciation,
                                     NumberVocabulary, RomanceNumberExtractor)


class PortugueseVariant(str, Enum):
    """
    Defines the Portuguese variant for spelling.
    - BR: Brazilian Portuguese (e.g., bilhão, dezesseis).
    - PT: European Portuguese (e.g., bilião, dezasseis).
    """
    BR = "br"
    PT = "pt"


def swap_gender_pt(word: str, gender: GrammaticalGender) -> str:
    """
    Convert a Portuguese word between masculine and feminine grammatical gender by adjusting its ending.

    Parameters:
        word (str): The word to convert.
        gender (GrammaticalGender): The target grammatical gender.

    Returns:
        str: The word with its ending swapped to match the specified gender, if applicable; otherwise, the original word.
    """
    if word == "dois" and gender == GrammaticalGender.FEMININE:
        return "duas"
    elif word == "duas" and gender == GrammaticalGender.MASCULINE:
        return "dois"

    elif gender == GrammaticalGender.FEMININE and word.endswith('o'):
        return word[:-1] + 'a'
    elif gender == GrammaticalGender.MASCULINE and word.endswith('ma'):
        return word[:-1]
    elif gender == GrammaticalGender.MASCULINE and word.endswith('a'):
        return word[:-1] + 'o'
    elif gender == GrammaticalGender.FEMININE and word.endswith('os'):
        return word[:-2] + 'as'
    elif gender == GrammaticalGender.MASCULINE and word.endswith('as'):
        return word[:-2] + 'os'
    elif gender == GrammaticalGender.FEMININE and word.endswith('m'):
        return word + 'a'
    return word


def pluralize_pt(word: str):
    if word.endswith("ão"):
        return word[:-2] + "ões"
    if not word.endswith("s"):
        return word + "s"
    return word


_PT_PT = NumberVocabulary(
    LANG="pt-PT",

    swap_gender=swap_gender_pt, # used for female forms
    pluralize=pluralize_pt, # use for plural forms

    HUNDRED_PARTICLE="cento", # how to read "1XX"
    DENOMINATOR_PARTICLE="avos",   # for fractions  X / N {PARTICLE}
    NUMBER_OVERFLOW="número exageradamente grande",
    DIVIDED_BY_ZERO="a dividir por zero", # how to read X/0 values
    NO_PREV_UNIT=[100, 1000], # "mil" vs "um mil"  / "cem" vs "um cem"
    NO_PLURAL=[1000], # "dois mil" vs "dois mils" / "dois milhões" vs "dois milhão"

    DEFAULT_SCALE=Scale.LONG,
    JOIN_WORD=["e"],
    JOINER_ON_TWENTYS = True,  # add JOIN_WORD from 20-30 - "vinte e um"
    JOINER_ON_HUNDREDS = True,   # add JOIN_WORD from 100-1000 - "duzentos e um"
    JOINER_ON_THOUSANDS = False,  # add JOIN_WORD from 1000-10000 - "mil e duzentos"

    DECIMAL_MARKER=["vírgula", "virgula", "ponto", ".", ","],
    NEGATIVE_SIGN=["menos"],
    UNITS={
        0: 'zero',
        1: 'um',
        2: 'dois',
        3: 'três',
        4: 'quatro',
        5: 'cinco',
        6: 'seis',
        7: 'sete',
        8: 'oito',
        9: 'nove'
    },
    TENS={
        10: 'dez',
        11: 'onze',
        12: 'doze',
        13: 'treze',
        14: 'catorze',
        15: 'quinze',
        16: 'dezasseis',
        17: 'dezassete',
        18: 'dezoito',
        19: 'dezanove',
        20: 'vinte',
        30: 'trinta',
        40: 'quarenta',
        50: 'cinquenta',
        60: 'sessenta',
        70: 'setenta',
        80: 'oitenta',
        90: 'noventa'
    },
    HUNDREDS={
        100: 'cem',
        200: 'duzentos',
        300: 'trezentos',
        400: 'quatrocentos',
        500: 'quinhentos',
        600: 'seiscentos',
        700: 'setecentos',
        800: 'oitocentos',
        900: 'novecentos'
    },
    FRACTION={
        2: 'meio',
        3: 'terço',
        4: 'quarto',
        5: 'quinto',
        6: 'sexto',
        7: 'sétimo',
        8: 'oitavo',
        9: 'nono',
        10: 'décimo',
        11: 'onze avos',
        12: 'doze avos',
        13: 'treze avos',
        14: 'catorze avos',
        15: 'quinze avos',
        16: 'dezasseis avos',
        17: 'dezassete avos',
        18: 'dezoito avos',
        19: 'dezanove avos',
        20: 'vigésimo',
        30: 'trigésimo',
        100: 'centésimo',
        1000: 'milésimo'
    },
    FRACTION_FEMALE={2: "meia"},
    SHORT_SCALE={
        10 ** 21: "sextilião",
        10 ** 18: "quintilião",
        10 ** 15: "quatrilião",
        10 ** 12: "trilião",
        10 ** 9: "bilião",
        10 ** 6: "milhão",
        10 ** 3: "mil"
    },
    LONG_SCALE={
        10 ** 36: "sextilião",
        10 ** 30: "quintilião",
        10 ** 24: "quatrilião",
        10 ** 18: "trilião",
        10 ** 12: "bilião",
        10 ** 6: "milhão",
        10 ** 3: "mil"
    },
    # defaults to male, use swap_gender/self.GENDERED_SPELLINGS if needed
    GENDERED_SPELLINGS={
        GrammaticalGender.FEMININE: {1: "uma", 2: "duas"}
    },
    DIGIT_SPELLINGS={},
    ALT_SPELLINGS={
        # pt-BR regionalisms
        'dezesseis': 16,
        'dezessete': 17,
        'dezenove': 19
    },
    ORDINAL_UNITS={
        1: 'primeiro',
        2: 'segundo',
        3: 'terceiro',
        4: 'quarto',
        5: 'quinto',
        6: 'sexto',
        7: 'sétimo',
        8: 'oitavo',
        9: 'nono'
    },
    ORDINAL_TENS={
        10: 'décimo',
        20: 'vigésimo',
        30: 'trigésimo',
        40: 'quadragésimo',
        50: 'quinquagésimo',
        60: 'sexagésimo',
        70: 'septuagésimo',
        80: 'octogésimo',
        90: 'nonagésimo'
    },
    ORDINAL_HUNDREDS={
        100: 'centésimo',
        200: 'ducentésimo',
        300: 'trecentésimo',
        400: 'quadrigentésimo',
        500: 'quingentésimo',
        600: 'sexcentésimo',
        700: 'septingentésimo',
        800: 'octingentésimo',
        900: 'noningentésimo'
    },
    ORDINAL_SHORT_SCALE={
        10 ** 21: "sextilionésimo",
        10 ** 18: "quintilionésimo",
        10 ** 15: "quatrilionésimo",
        10 ** 12: "trilionésimo",
        10 ** 9: "bilionésimo",
        10 ** 6: "milionésimo",
        10 ** 3: "milésimo"
    },
    ORDINAL_LONG_SCALE={
        10 ** 36: "sextilionésimo",
        10 ** 30: "quintilionésimo",
        10 ** 24: "quatrilionésimo",
        10 ** 18: "trilionésimo",
        10 ** 12: "bilionésimo",
        10 ** 6: "milionésimo",
        10 ** 3: "milésimo"
    }
)

_PT_BR = NumberVocabulary(
    LANG="pt-BR",
    swap_gender=swap_gender_pt,  # used for female forms
    pluralize=pluralize_pt,  # use for plural forms
    DEFAULT_SCALE=Scale.SHORT,
    DIVIDED_BY_ZERO=_PT_PT.DIVIDED_BY_ZERO,
    DENOMINATOR_PARTICLE=_PT_PT.DENOMINATOR_PARTICLE,
    HUNDRED_PARTICLE=_PT_PT.HUNDRED_PARTICLE,
    NO_PREV_UNIT=_PT_PT.NO_PREV_UNIT,
    NO_PLURAL=_PT_PT.NO_PLURAL,
    NUMBER_OVERFLOW=_PT_PT.NUMBER_OVERFLOW,
    JOIN_WORD=_PT_PT.JOIN_WORD,
    JOINER_ON_TWENTYS=True,  # add JOIN_WORD from 20-30 - "vinte e um"
    JOINER_ON_HUNDREDS=True,  # add JOIN_WORD from 100-1000 - "duzentos e um"
    JOINER_ON_THOUSANDS=False,  # add JOIN_WORD from 1000-10000 - "mil e duzentos"
    DECIMAL_MARKER=_PT_PT.DECIMAL_MARKER,
    NEGATIVE_SIGN=_PT_PT.NEGATIVE_SIGN,
    UNITS=_PT_PT.UNITS,
    TENS={
        **_PT_PT.TENS,
        16: 'dezesseis',
        17: 'dezessete',
        19: 'dezenove'
    },
    HUNDREDS=_PT_PT.HUNDREDS,
    FRACTION=_PT_PT.FRACTION,
    FRACTION_FEMALE=_PT_PT.FRACTION_FEMALE,
    SHORT_SCALE={
        10 ** 21: "sextilhão",
        10 ** 18: "quintilhão",
        10 ** 15: "quatrilhão",
        10 ** 12: "trilhão",
        10 ** 9: "bilhão",
        10 ** 6: "milhão",
        10 ** 3: "mil"
    },
    LONG_SCALE={
        10 ** 36: "sextilhão",
        10 ** 30: "quintilhão",
        10 ** 24: "quatrilhão",
        10 ** 18: "trilhão",
        10 ** 12: "bilhão",
        10 ** 6: "milhão",
        10 ** 3: "mil"
    },
    GENDERED_SPELLINGS=_PT_PT.GENDERED_SPELLINGS,
    DIGIT_SPELLINGS={
        6: "meia" # coloquialism
    },
    ALT_SPELLINGS={
        # pt-PT regionalisms
        'dezasseis': 16,
        'dezassete': 17,
        'dezanove': 19
    },
    ORDINAL_UNITS=_PT_PT.ORDINAL_UNITS,
    ORDINAL_TENS=_PT_PT.ORDINAL_TENS,
    ORDINAL_HUNDREDS=_PT_PT.ORDINAL_HUNDREDS,
    ORDINAL_SHORT_SCALE=_PT_PT.ORDINAL_SHORT_SCALE,
    ORDINAL_LONG_SCALE=_PT_PT.ORDINAL_LONG_SCALE
)

PT_PT = RomanceNumberExtractor(_PT_PT)
PT_BR = RomanceNumberExtractor(_PT_BR)


def pronounce_ordinal_pt(
        number: Union[int, float],
        gender: GrammaticalGender = GrammaticalGender.MASCULINE,
        scale: Scale = Scale.LONG,
        variant: PortugueseVariant = PortugueseVariant.PT
) -> str:
    """
    Return the ordinal pronunciation of a number in Portuguese, supporting grammatical gender, scale (short or long), and language variant (Brazilian or European Portuguese).

    Parameters:
        number (int or float): The number to pronounce as an ordinal.
        gender (GrammaticalGender, optional): The grammatical gender for the ordinal form (masculine or feminine).
        scale (Scale, optional): The numerical scale to use (short or long).
        variant (PortugueseVariant, optional): The Portuguese variant (Brazilian or European).

    Returns:
        str: The ordinal pronunciation of the number in Portuguese.

    Raises:
        TypeError: If `number` is not an int or float.
    """
    if variant == PortugueseVariant.PT:
        return PT_PT.pronounce_ordinal(number, gender, scale)
    return PT_BR.pronounce_ordinal(number, gender, scale)


def is_fractional_pt(
        input_str: str
) -> Union[float, bool]:
    """
    Checks if the input string corresponds to a recognized Portuguese fractional word.

    Returns:
        The fractional value as a float if recognized (e.g., 0.5 for "meio" or "meia"); otherwise, False.
    """
    return PT_PT.is_fractional(input_str)


def is_ordinal_pt(input_str: str) -> bool:
    """
    Determine if a string is a Portuguese ordinal word.

    Returns:
        bool: True if the input string is recognized as a Portuguese ordinal, otherwise False.
    """
    return PT_PT.is_ordinal(input_str)


def extract_number_pt(
        text: str,
        ordinals: bool = False,
        scale: Scale = Scale.LONG,
        variant: PortugueseVariant = PortugueseVariant.PT
) -> Union[int, float, bool]:
    """
    Extracts a numeric value from a Portuguese text phrase, supporting cardinals, ordinals, fractions, and large scales.

    Parameters:
        text (str): The input phrase potentially containing a number.
        ordinals (bool): If True, recognizes ordinal words as numbers.
        scale (Scale): Specifies whether to use the short or long numerical scale.
        variant (PortugueseVariant): Specifies the Portuguese language variant (BR or PT).

    Returns:
        int or float: The extracted number if found; otherwise, False.
    """
    if variant == PortugueseVariant.PT:
        return PT_PT.extract_number(text, ordinals, scale)
    return PT_BR.extract_number(text, ordinals, scale)


def pronounce_number_pt(
        number: Union[int, float],
        places: int = 5,
        scale: Scale = Scale.LONG,
        variant: PortugueseVariant = PortugueseVariant.PT,
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
        variant (PortugueseVariant): Portuguese language variant for pronunciation.
        ordinals (bool): If True, pronounce as an ordinal number.
        gender (GrammaticalGender): Grammatical gender for ordinal numbers.

    Returns:
        str: The number expressed as a Portuguese phrase.
    """
    if variant == PortugueseVariant.PT:
        return PT_PT.pronounce_number(number, places, scale, ordinals, digits, gender)
    return PT_BR.pronounce_number(number, places, scale, ordinals, digits, gender)


def numbers_to_digits_pt(
        utterance: str,
        scale: Scale = Scale.LONG,
        variant: PortugueseVariant = PortugueseVariant.PT
) -> str:
    """
    Converts written Portuguese numbers in a text string to their digit equivalents, preserving all other text.

    Identifies spans of number words (including the joiner "e"), extracts their numeric values, and replaces them with digit strings. Non-number words and context are left unchanged.

    Parameters:
        utterance (str): Input text possibly containing written Portuguese numbers.
        scale (Scale, optional): Numerical scale (short or long) to interpret large numbers. Defaults to Scale.LONG.
        variant (PortugueseVariant, optional): Portuguese language variant (BR or PT). Defaults to PortugueseVariant.PT.

    Returns:
        str: The input text with written numbers replaced by their digit representations.
    """
    if variant == PortugueseVariant.PT:
        return PT_PT.numbers_to_digits(utterance, scale)
    return PT_BR.numbers_to_digits(utterance, scale)



def pronounce_fraction_pt(word: str,
                          scale: Scale = Scale.LONG,
                          variant: PortugueseVariant = PortugueseVariant.PT) -> str:
    """
    Return the Portuguese pronunciation of a fraction given as a string (e.g., "1/2").

    The numerator is pronounced as a cardinal number, and the denominator as an ordinal or fraction name, pluralized if appropriate. For denominators not in the known fraction list, the denominator is pronounced as a cardinal number followed by "avos" if plural.

    Parameters:
        word (str): Fraction in the form "numerator/denominator" (e.g., "3/4").

    Returns:
        str: The Portuguese pronunciation of the fraction.
    """
    if variant == PortugueseVariant.PT:
        return PT_PT.pronounce_fraction(word, scale)
    return PT_BR.pronounce_fraction(word, scale)


if __name__ == "__main__":
    print("--- Testing Pronunciation (Short Scale, BR Variant) ---")
    print(f"1,234,567: {pronounce_number_pt(1_234_567, scale=Scale.SHORT, variant=PortugueseVariant.BR)}")
    print(f"1,000,000,000: {pronounce_number_pt(1_000_000_000, scale=Scale.SHORT, variant=PortugueseVariant.BR)}")
    print(f"16: {pronounce_number_pt(16, variant=PortugueseVariant.BR)}")

    print("\n--- Testing Pronunciation (Long Scale, PT Variant) ---")
    print(f"1,000,000: {pronounce_number_pt(1_000_000, scale=Scale.LONG, variant=PortugueseVariant.PT)}")
    print(f"1,000,100: {pronounce_number_pt(1_000_100, scale=Scale.LONG, variant=PortugueseVariant.PT)}")
    print(f"1,000,000,000: {pronounce_number_pt(1_000_000_000, scale=Scale.LONG, variant=PortugueseVariant.PT)}")
    print(
        f"1,000,000,000,000: {pronounce_number_pt(1_000_000_000_000, scale=Scale.LONG, variant=PortugueseVariant.PT)}")
    print(f"2,500,000,000: {pronounce_number_pt(2_500_000_000, scale=Scale.LONG, variant=PortugueseVariant.PT)}")
    print(f"2,500,123,456: {pronounce_number_pt(2_500_123_456, scale=Scale.LONG, variant=PortugueseVariant.PT)}")
    print(f"16: {pronounce_number_pt(16, variant=PortugueseVariant.PT)}")
    print(f"-16: {pronounce_number_pt(-16, variant=PortugueseVariant.PT)}")

    print("\n--- Testing Edge Cases ---")
    print(f"-123.45: {pronounce_number_pt(-123.45)}")
    print(f"10.05: {pronounce_number_pt(10.05)}")
    print(f"2000: {pronounce_number_pt(2000)}")
    print(f"2001: {pronounce_number_pt(2001)}")
    print(f"123.456789: {pronounce_number_pt(123.456789)}")

    print("\n--- Testing Ordinal Pronunciation ---")
    print(f"1st (masculine): {pronounce_number_pt(1, ordinals=True, gender=GrammaticalGender.MASCULINE)}")
    print(f"1st (feminine): {pronounce_number_pt(1, ordinals=True, gender=GrammaticalGender.FEMININE)}")
    print(f"23rd (masculine): {pronounce_number_pt(23, ordinals=True)}")
    print(f"23rd (feminine): {pronounce_number_pt(23, ordinals=True, gender=GrammaticalGender.FEMININE)}")
    print(f"100th: {pronounce_number_pt(100, ordinals=True)}")
    print(f"101st: {pronounce_number_pt(101, ordinals=True)}")
    print(f"1000th: {pronounce_number_pt(1000, ordinals=True)}")
    print(f"1,000,000th: {pronounce_number_pt(1_000_000, ordinals=True)}")
    print(
        f"1,000,000,000,000th (PT, long): {pronounce_number_pt(1_000_000_000_000, ordinals=True, variant=PortugueseVariant.PT, scale=Scale.LONG)}")

    print("\n--- Testing numbers_to_digits_pt (BR) ---")
    print(f"'quinhentos e cinquenta' -> '{numbers_to_digits_pt('quinhentos e cinquenta')}'")
    print(f"'um milhão' -> '{numbers_to_digits_pt('um milhão')}'")
    print(f"'dezesseis' -> '{numbers_to_digits_pt('dezesseis')}'")
    print(f"'há duzentos e cinquenta carros' -> '{numbers_to_digits_pt('há duzentos e cinquenta carros')}'")

    print("\n--- Testing numbers_to_digits_pt (PT) ---")
    print(
        f"'quinhentos e cinquenta' -> '{numbers_to_digits_pt('quinhentos e cinquenta', variant=PortugueseVariant.PT)}'")
    print(f"'um milhão' -> '{numbers_to_digits_pt('um milhão', variant=PortugueseVariant.PT)}'")
    print(f"'dezasseis' -> '{numbers_to_digits_pt('dezasseis', variant=PortugueseVariant.PT)}'")

    print("\n--- Testing Ordinal Extraction ---")
    print(f"'o segundo carro' -> {extract_number_pt('o segundo carro', ordinals=True)}")
    print(f"'primeiro lugar' -> {extract_number_pt('primeiro lugar', ordinals=True)}")
    print(f"'o milésimo dia' -> {extract_number_pt('o milésimo dia', ordinals=True)}")
    print(f"'a milésima vez' -> {extract_number_pt('a milésima vez', ordinals=True)}")
    print(f"'a primeira vez' -> {extract_number_pt('a primeira vez', ordinals=True)}")
    print(f"'a sexagésima quarta vez' -> {extract_number_pt('a sexagésima quarta vez', ordinals=True)}")

    print("\n--- Testing Cardinal Extraction ---")
    print(f"'um' -> {extract_number_pt('um')}")
    print(f"'uma' -> {extract_number_pt('uma')}")
    print(f"'vinte e um' -> {extract_number_pt('vinte e um')}")
    print(f"'um milhão' -> {extract_number_pt('um milhão')}")
    print(f"'dois milhões e quinhentos' -> {extract_number_pt('dois milhões e quinhentos')}")
    print(f"'mil e vinte e três' -> {extract_number_pt('mil e vinte e três')}")
    print(f"'trinta e cinco vírgula quatro' -> {extract_number_pt('trinta e cinco vírgula quatro')}")

    print("\n--- Testing Fractions ---")
    print(f"1/2: {pronounce_fraction_pt('1/2')}")
    print(f"2/2: {pronounce_fraction_pt('2/2')}")
    print(f"5/2: {pronounce_fraction_pt('5/2')}")
    print(f"5/3: {pronounce_fraction_pt('5/3')}")
    print(f"5/4: {pronounce_fraction_pt('5/4')}")
    print(f"7/5: {pronounce_fraction_pt('7/5')}")
    print(f"0/20: {pronounce_fraction_pt('0/20')}")
    print(f"1/0: {pronounce_fraction_pt('1/0')}")
    print(f"0/0: {pronounce_fraction_pt('0/0')}")
