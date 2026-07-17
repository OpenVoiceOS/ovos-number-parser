from collections import OrderedDict
from typing import List, Optional, Union
import warnings
from ovos_number_parser.util import (convert_to_mixed_fraction, look_for_fractions, DigitPronunciation,
                                     is_numeric, tokenize, Token)

from ovos_number_parser.util import (Scale, GrammaticalGender, NumberVocabulary, RomanceNumberExtractor)



def swap_gender_gl(word: str, gender: GrammaticalGender) -> str:
    """
    Convert a Galician word between masculine and feminine grammatical gender by adjusting its ending.

    Parameters:
        word (str): The word to convert.
        gender (GrammaticalGender): The target grammatical gender.

    Returns:
        str: The word with its ending swapped to match the specified gender, if applicable; otherwise, the original word.
    """
    if word == "dous" and gender == GrammaticalGender.FEMININE:
        return "dúas"
    elif word == "dúas" and gender == GrammaticalGender.MASCULINE:
        return "dous"

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


def pluralize_gl(word: str):
    if word.endswith("ão"):
        return word[:-2] + "ões"
    if not word.endswith("s"):
        return word + "s"
    return word



_GL = NumberVocabulary(
    LANG="gl-ES",
    swap_gender=swap_gender_gl,  # used for female forms
    pluralize=pluralize_gl,  # use for plural forms

    HUNDRED_PARTICLE="cento",  # how to read "1XX"
    DENOMINATOR_PARTICLE="abos",  # for fractions  X / N {PARTICLE}
    DIVIDED_BY_ZERO="a dividir por cero",  # how to read X/0 values
    NO_PREV_UNIT=[100, 1000],  # "mil" vs "um mil"  / "cem" vs "um cem"
    NO_PLURAL=[1000],  # "dois mil" vs "dois mils" / "dois milhões" vs "dois milhão"

    NUMBER_OVERFLOW="número exageradamente grande",
    DEFAULT_SCALE=Scale.LONG,
    JOIN_WORD=["e"],

    JOINER_ON_TWENTYS=True,  # add JOIN_WORD from 20-30 - "vinte e un"
    JOINER_ON_HUNDREDS=False,  # Galician omits the conjunction after hundreds - "douscentos trinta e catro"
    JOINER_ON_HUNDRED_PARTICLE=True,  # but keeps it after the particle - "cento e vinte e tres"
    JOINER_ON_THOUSANDS=False,  # add JOIN_WORD from 1000-10000 - "mil e duzentos"

    DECIMAL_MARKER=["coma", "punto", ".", ","],
    NEGATIVE_SIGN=["menos"],
    UNITS={
        0: 'cero',
        1: 'un',
        2: 'dous',
        3: 'tres',
        4: 'catro',
        5: 'cinco',
        6: 'seis',
        7: 'sete',
        8: 'oito',
        9: 'nove',
    },
    TENS={
        10: 'dez',
        11: 'once',
        12: 'doce',
        13: 'trece',
        14: 'catorce',
        15: 'quince',
        16: 'dezaseis',
        17: 'dezasete',
        18: 'dezaoito',
        19: 'dezanove',
        20: 'vinte',
        30: 'trinta',
        40: 'corenta',
        50: 'cincuenta',
        60: 'sesenta',
        70: 'setenta',
        80: 'oitenta',
        90: 'noventa'
    },
    HUNDREDS={
        100: 'cen',
        200: 'douscentos',
        300: 'trescentos',
        400: 'catrocentos',
        500: 'cincocentos',
        600: 'seiscentos',
        700: 'setecentos',
        800: 'oitocentos',
        900: 'novecentos'
    },
    FRACTION={
        2: 'medio',
        3: 'terzo',
        4: 'cuarto',
        5: 'quinto',
        6: 'sexto',
        7: 'séptimo',
        8: 'oitavo',
        9: 'noveno',
        10: 'décimo',
        11: 'onceavo',
        12: 'doceavo',
        13: 'treceavo',
        14: 'catorceavo',
        15: 'quinceavo',
        16: 'dezaseisavo',
        17: 'dezaseteavo',
        18: 'dezaoitoavo',
        19: 'dezanoveavo',
        20: 'vinteavo',
        100: "centésimo",
        1000: "milésimo"
    },
    FRACTION_FEMALE={
        2: "media"  # una y media -> 1.5
    },
    SHORT_SCALE={
        1000: 'mil',
        10 ** 6: 'millón',
        10 ** 9: "billón",
        10 ** 12: 'trillón',
        10 ** 15: "cuatrillón",
        10 ** 18: "quintillón",
        10 ** 21: "sextillón",
        10 ** 24: "septillón",
        10 ** 27: "octillón",
        10 ** 30: "nonillón",
        10 ** 33: "decillón",
        10 ** 36: "undecillón",
        10 ** 39: "duodecillón",
        10 ** 42: "tredecillón",
        10 ** 45: "cuatrodecillón",
        10 ** 48: "quindecillón",
        10 ** 51: "sexdecillón",
        10 ** 54: "septendecillón",
        10 ** 57: "octodecillón",
        10 ** 60: "novendecillón",
        10 ** 63: "vigintillón",
        10 ** 66: "unvigintillón",
        10 ** 69: "unovigintillón",
        10 ** 72: "tresvigintillón",
        10 ** 75: "quattuorvigintillón",
        10 ** 78: "quinquavigintillón",
        10 ** 81: "qesvigintillón",
        10 ** 84: "septemvigintillón",
        10 ** 87: "octovigintillón",
        10 ** 90: "novemvigintillón",
        10 ** 93: "trigintillón",
        10 ** 96: "untrigintillón",
        10 ** 99: "duotrigintillón",
        10 ** 102: "trestrigintillón",
        10 ** 105: "quattuortrigintillón",
        10 ** 108: "quinquatrigintillón",
        10 ** 111: "sestrigintillón",
        10 ** 114: "septentrigintillón",
        10 ** 117: "octotrigintillón",
        10 ** 120: "noventrigintillón",
        10 ** 123: "quadragintillón",
        10 ** 153: "quinquagintillón",
        10 ** 183: "sexagintillón",
        10 ** 213: "septuagintillón",
        10 ** 243: "octogintillón",
        10 ** 273: "nonagintillón",
        10 ** 303: "centillón",
        10 ** 306: "uncentillón",
        10 ** 309: "duocentillón",
        10 ** 312: "trescentillón",
        10 ** 333: "decicentillón",
        10 ** 336: "undecicentillón",
        10 ** 363: "viginticentillón",
        10 ** 366: "unviginticentillón",
        10 ** 393: "trigintacentillón",
        10 ** 423: "quadragintacentillón",
        10 ** 453: "quinquagintacentillón",
        10 ** 483: "sexagintacentillón",
        10 ** 513: "septuagintacentillón",
        10 ** 543: "octogintacentillón",
        10 ** 573: "nonagintacentillón",
        10 ** 603: "ducentillón",
        10 ** 903: "trecentillón",
        10 ** 1203: "quadringentillón",
        10 ** 1503: "quingentillón",
        10 ** 1803: "sexcentillón",
        10 ** 2103: "septingentillón",
        10 ** 2403: "octingentillón",
        10 ** 2703: "nongentillón",
        10 ** 3003: "millinillón",
    },
    LONG_SCALE={
        1000: 'mil',
        10 ** 6: 'millón',
        10 ** 12: "billón",
        10 ** 18: 'trillón',
        10 ** 24: "cuatrillón",
        10 ** 30: "quintillón",
        10 ** 36: "sextillón",
        10 ** 42: "septillón",
        10 ** 48: "octillón",
        10 ** 54: "nonillón",
        10 ** 60: "decillón",
        10 ** 66: "undecillón",
        10 ** 72: "duodecillón",
        10 ** 78: "tredecillón",
        10 ** 84: "cuatrodecillón",
        10 ** 90: "quindecillón",
        10 ** 96: "sexdecillón",
        10 ** 102: "septendecillón",
        10 ** 108: "octodecillón",
        10 ** 114: "novendecillón",
        10 ** 120: "vigintillón",
        10 ** 306: "unquinquagintillón",
        10 ** 312: "duoquinquagintillón",
        10 ** 336: "sexquinquagintillón",
        10 ** 366: "unsexagintillón"
    },

    GENDERED_SPELLINGS={
        GrammaticalGender.FEMININE: {
            1: "unha",
            2: "dúas"
        }
    },
    DIGIT_SPELLINGS={},
    ALT_SPELLINGS={

    },
    ORDINAL_UNITS={
        1: 'primeiro',
        2: 'segundo',
        3: 'terceiro',
        4: 'cuarto',
        5: 'quinto',
        6: 'sexto',
        7: 'séptimo',
        8: 'oitavo',
        9: 'noveno',

    },
    ORDINAL_TENS={
        10: 'décimo',
        11: 'undécimo',
        12: 'duodécimo',
        13: 'decimoterceiro',
        14: 'decimocuarto',
        15: 'decimoquinto',
        16: 'decimosexto',
        17: 'decimoséptimo',
        18: 'decimoitavo',
        19: 'decimonoveno',
        20: 'vixésimo',
        30: 'trixésimo',
        40: "cuadraxésimo",
        50: "quincuaxésimo",
        60: "sexaxésimo",
        70: "septuaxésimo",
        80: "octoxésimo",
        90: "nonaxésimo"
    },
    ORDINAL_HUNDREDS={
        100: "centésimo",
    },
    ORDINAL_SHORT_SCALE={
        10 ** 3: "milésimo",
        10 ** 6: "millonésimo",
        10 ** 9: "milmillonésimo",
        10 ** 12: "billonésimo",
        10 ** 15: "milbillonésimo",
        10 ** 18: "trillonésimo",
        10 ** 21: "miltrillonésimo",
        10 ** 24: "cuatrillonésimo",
        10 ** 27: "milcuatrillonésimo",
        10 ** 30: "quintillonésimo",
        10 ** 33: "milquintillonésimo"
    },
    ORDINAL_LONG_SCALE={
        10 ** 3: "milésimo",
        10 ** 6: "millonésimo",
        10 ** 12: "billonésimo",
        10 ** 18: "trillonésimo",
        10 ** 24: "cuatrillonésimo",
        10 ** 30: "quintillonésimo",
        10 ** 36: "sextillonésimo",
        10 ** 42: "septillonésimo",
        10 ** 48: "octillonésimo",
        10 ** 54: "nonillonésimo",
        10 ** 60: "decillonésimo"
    }
)

GL = RomanceNumberExtractor(_GL)


##################################################################
# all methods below are deprecated and only for backwards compat
##################################################################

def pronounce_ordinal_gl(
        number: Union[int, float],
        gender: GrammaticalGender = GrammaticalGender.MASCULINE,
        scale: Optional[Scale] = None
) -> str:
    """
    DEPRECATED
    """
    warnings.warn(
        "migrate to use RomanceNumberExtractor and NumberVocabulary directly instead",
        DeprecationWarning,
        stacklevel=2,
    )
    scale = scale or GL.vocab.DEFAULT_SCALE
    return GL.pronounce_ordinal(number, gender, scale)


def is_fractional_gl(
        input_str: str
) -> Union[float, bool]:
    """
    DEPRECATED
    """
    warnings.warn(
        "migrate to use RomanceNumberExtractor and NumberVocabulary directly instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return GL.is_fractional(input_str)


def is_ordinal_gl(input_str: str) -> bool:
    """
    DEPRECATED
    """
    warnings.warn(
        "migrate to use RomanceNumberExtractor and NumberVocabulary directly instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return GL.is_ordinal(input_str)


def extract_number_gl(
        text: str,
        ordinals: bool = False,
        scale: Optional[Scale] = None
) -> Union[int, float, bool]:
    """
    DEPRECATED
    """
    warnings.warn(
        "migrate to use RomanceNumberExtractor and NumberVocabulary directly instead",
        DeprecationWarning,
        stacklevel=2,
    )
    scale = scale or GL.vocab.DEFAULT_SCALE
    return GL.extract_number(text, ordinals, scale)


def pronounce_number_gl(
        number: Union[int, float],
        places: int = 5,
        scale: Optional[Scale] = None,
        ordinals: bool = False,
        digits: DigitPronunciation = DigitPronunciation.FULL_NUMBER,
        gender: GrammaticalGender = GrammaticalGender.MASCULINE
) -> str:
    """
    DEPRECATED
    """
    warnings.warn(
        "migrate to use RomanceNumberExtractor and NumberVocabulary directly instead",
        DeprecationWarning,
        stacklevel=2,
    )
    scale = scale or GL.vocab.DEFAULT_SCALE
    return GL.pronounce_number(number, places, scale, ordinals, digits, gender)


def numbers_to_digits_gl(
        utterance: str,
        scale: Optional[Scale] = None
) -> str:
    """
    DEPRECATED
    """
    warnings.warn(
        "migrate to use RomanceNumberExtractor and NumberVocabulary directly instead",
        DeprecationWarning,
        stacklevel=2,
    )
    scale = scale or GL.vocab.DEFAULT_SCALE
    return GL.numbers_to_digits(utterance, scale)



def pronounce_fraction_gl(word: str, scale: Optional[Scale] = None) -> str:
    """
    DEPRECATED
    """
    warnings.warn(
        "migrate to use RomanceNumberExtractor and NumberVocabulary directly instead",
        DeprecationWarning,
        stacklevel=2,
    )
    scale = scale or GL.vocab.DEFAULT_SCALE
    return GL.pronounce_fraction(word, scale)


if __name__ == "__main__":
    print("--- Testing Pronunciation (Galician - Long Scale) ---")
    # Galician only uses the Long Scale. Short Scale tests are irrelevant or would yield the same result for the first million.
    # $1,234,567$: un millón douscentos trinta e catro mil cincocentos sesenta e sete
    print(f"1,234,567: {GL.pronounce_number(1_234_567)}")

    # $1,000,000,000$: mil millóns (Long Scale)
    print(f"1,000,000,000: {GL.pronounce_number(1_000_000_000)}")

    # $1,000,000,000,000$: un billón (Long Scale)
    print(f"1,000,000,000,000: {GL.pronounce_number(1_000_000_000_000)}")

    # $2,500,123,456$: dous mil cincocentos millóns cento vinte e tres mil catrocentos cincuenta e seis
    print(f"2,500,123,456: {GL.pronounce_number(2_500_123_456)}")

    # $16$: dezaseis
    print(f"16: {GL.pronounce_number(16)}")

    print("\n--- Testing Edge Cases ---")
    # $-123.45$: menos cento vinte e tres coma corenta e cinco
    print(f"-123.45: {GL.pronounce_number(-123.45)}")
    # $10.05$: dez coma cero cinco
    print(f"10.05: {GL.pronounce_number(10.05)}")
    # $2000$: dous mil
    print(f"2000: {GL.pronounce_number(2000)}")
    # $2001$: dous mil un
    print(f"2001: {GL.pronounce_number(2001)}")
    # $123.456789$: cento vinte e tres coma catrocentos cincuenta e seis mil setecentos oitenta e nove
    print(f"123.456789: {GL.pronounce_number(123.456789)}")

    print("\n--- Testing Ordinal Pronunciation ---")
    # $1^{st}$ (masculine): primeiro
    print(f"1st (masculine): {GL.pronounce_number(1, ordinals=True, gender=GrammaticalGender.MASCULINE)}")
    # $1^{st}$ (feminine): primeira
    print(f"1st (feminine): {GL.pronounce_number(1, ordinals=True, gender=GrammaticalGender.FEMININE)}")
    # $23^{rd}$ (masculine): vixésimo terceiro
    print(f"23rd (masculine): {GL.pronounce_number(23, ordinals=True, gender=GrammaticalGender.MASCULINE)}")
    # $23^{rd}$ (feminine): vixésima terceira
    print(f"23rd (feminine): {GL.pronounce_number(23, ordinals=True, gender=GrammaticalGender.FEMININE)}")
    # $100^{th}$: centésimo
    print(f"100th: {GL.pronounce_number(100, ordinals=True)}")
    # $101^{st}$: centésimo primeiro
    print(f"101st: {GL.pronounce_number(101, ordinals=True)}")
    # $1000^{th}$: milésimo
    print(f"1000th: {GL.pronounce_number(1000, ordinals=True)}")
    # $1,000,000^{th}$: millonésimo
    print(f"1,000,000th: {GL.pronounce_number(1_000_000, ordinals=True)}")
    # $1,000,000,000,000^{th}$: billonésimo
    print(f"1,000,000,000,000th: {GL.pronounce_number(1_000_000_000_000, ordinals=True)}")

    print("\n--- Testing GL.numbers_to_digits ---")
    # duzentos e cinquenta -> 250 (Using correct Galician: douscentos cincuenta)
    print(f"'douscentos cincuenta' -> '{GL.numbers_to_digits('douscentos cincuenta')}'")
    # un milhon -> 1000000 (Using correct Galician: un millón)
    print(f"'un millón' -> '{GL.numbers_to_digits('un millón')}'")
    # zasseis -> 16 (Using correct Galician: dezaseis)
    print(f"'dezaseis' -> '{GL.numbers_to_digits('dezaseis')}'")
    # hai duzientos e cinquenta carros -> hai 250 carros (Using correct Galician)
    print(f"'hai douscentos cincuenta carros' -> '{GL.numbers_to_digits('hai douscentos cincuenta carros')}'")

    print("\n--- Testing Ordinal Extraction ---")
    # o segundo carro -> 2 (Galician: o segundo carro)
    print(f"'o segundo carro' -> {GL.extract_number('o segundo carro', ordinals=True)}")
    # primeiro lugar -> 1 (Galician: primeiro lugar)
    print(f"'primeiro lugar' -> {GL.extract_number('primeiro lugar', ordinals=True)}")
    # o milésimo dia -> 1000 (Galician: o milésimo día)
    print(f"'o milésimo día' -> {GL.extract_number('o milésimo día', ordinals=True)}")
    # a milésima vez -> 1000 (Galician: a milésima vez)
    print(f"'a milésima vez' -> {GL.extract_number('a milésima vez', ordinals=True)}")
    # a primeira vez -> 1 (Galician: a primeira vez)
    print(f"'a primeira vez' -> {GL.extract_number('a primeira vez', ordinals=True)}")
    # a sexagésima cuarta vez -> 64 (Galician: a sexagésima cuarta vez)
    print(f"'a sexagésima cuarta vez' -> {GL.extract_number('a sexagésima cuarta vez', ordinals=True)}")

    print("\n--- Testing Cardinal Extraction ---")
    # un -> 1
    print(f"'un' -> {GL.extract_number('un')}")
    # unha -> 1
    print(f"'unha' -> {GL.extract_number('unha')}")
    # vinte e un -> 21
    print(f"'vinte e un' -> {GL.extract_number('vinte e un')}")
    # vinte e unha -> 21
    print(f"'vinte e unha' -> {GL.extract_number('vinte e unha')}")
    # vinte e dous -> 22
    print(f"'vinte e dous' -> {GL.extract_number('vinte e dous')}")
    # vinte e dúas -> 22
    print(f"'vinte e dúas' -> {GL.extract_number('vinte e dúas')}")
    # un millón -> 1000000
    print(f"'un millón' -> {GL.extract_number('un millón')}")
    # dous millóns e cincocentos -> 2500500 (Galician: dous millóns cincocentos)
    print(f"'dous millóns cincocentos' -> {GL.extract_number('dous millóns cincocentos')}")
    # mil vinte e tres -> 1023 (Galician: mil vinte e tres)
    print(f"'mil vinte e tres' -> {GL.extract_number('mil vinte e tres')}")
    # trinta e cinco coma catro -> 35.4 (Galician: trinta e cinco coma catro)
    print(f"'trinta e cinco coma catro' -> {GL.extract_number('trinta e cinco coma catro')}")

    print("\n--- Testing Fractions ---")
    # $1/2$: un medio
    print(f"1/2: {GL.pronounce_fraction('1/2')}")
    # $2/2$: dous medios / dous medios, ou dous medios (or dous sobre dous)
    print(f"2/2: {GL.pronounce_fraction('2/2')}")
    # $5/2$: cinco medios
    print(f"5/2: {GL.pronounce_fraction('5/2')}")
    # $5/3$: cinco terzos
    print(f"5/3: {GL.pronounce_fraction('5/3')}")
    # $5/4$: cinco cuartos
    print(f"5/4: {GL.pronounce_fraction('5/4')}")
    # $7/5$: sete quintos
    print(f"7/5: {GL.pronounce_fraction('7/5')}")
    # $0/20$: cero vinteavos
    print(f"0/20: {GL.pronounce_fraction('0/20')}")