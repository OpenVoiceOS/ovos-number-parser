from ovos_number_parser.util import (Scale, GrammaticalGender, DigitPronunciation,
                                     NumberVocabulary, RomanceNumberExtractor)
from typing import Union
import warnings


def swap_gender_mwl(word: str, gender: GrammaticalGender) -> str:
    if word == "un" and gender == GrammaticalGender.FEMININE:
        return "ũa"
    elif word == "ũa" and gender == GrammaticalGender.MASCULINE:
        return "un"
    elif word == "dous" and gender == GrammaticalGender.FEMININE:
        return "dues"
    elif word == "dues" and gender == GrammaticalGender.MASCULINE:
        return "dous"

    # TODO - is this correct?
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


def pluralize_mwl(word: str):
    # TODO - is this accurate?
    if word.endswith("on"):
        return word + "es"
    if not word.endswith("s"):
        return word + "s"
    return word


_MWL = NumberVocabulary(
    LANG="mwl",
    swap_gender=swap_gender_mwl,  # used for female forms
    pluralize=pluralize_mwl,  # use for plural forms

    HUNDRED_PARTICLE="ciento",  # how to read "1XX"
    DENOMINATOR_PARTICLE="abos",  # for fractions  X / N {PARTICLE}
    DIVIDED_BY_ZERO="a dibidir por zero",  # how to read X/0 values
    NO_PREV_UNIT=[100, 1000],  # "mil" vs "um mil"  / "cem" vs "um cem"
    NO_PLURAL=[1000],  # "dois mil" vs "dois mils" / "dois milhões" vs "dois milhão"
    NUMBER_OVERFLOW="número exageradamente grande",
    DEFAULT_SCALE=Scale.LONG,
    JOIN_WORD=["i"],

    JOINER_ON_TWENTYS=True,  # add JOIN_WORD from 20-30 - "vinte e um"
    JOINER_ON_HUNDREDS=True,  # add JOIN_WORD from 100-1000 - "duzentos e um"
    JOINER_ON_THOUSANDS=False,  # add JOIN_WORD from 1000-10000 - "mil e duzentos"

    DECIMAL_MARKER=["ponto", "bírgula", "birgula", ".", ","],
    NEGATIVE_SIGN=["menos"],
    UNITS={
        0: 'zero',
        1: 'un',
        2: 'dous',
        3: 'trés',
        4: 'quatro',
        5: 'cinco',
        6: 'seis',
        7: 'siete',
        8: 'uito',
        9: 'nuobe'
    },
    TENS={
        10: 'dieç',
        11: 'onze',
        12: 'duoze',
        13: 'treze',
        14: 'catorze',
        15: 'quinze',
        16: 'zasseis',
        17: 'zassiete',
        18: 'zuio',
        19: 'zanuobe',
        20: 'binte',
        30: 'trinta',
        40: 'quarenta',
        50: 'cinquenta',
        60: 'sessenta',
        70: 'setenta',
        80: 'uitenta',
        90: 'nobenta'
    },
    HUNDREDS={
        100: 'cien',
        200: 'duzientos',
        300: 'trezientos',
        400: 'quatrocientos',
        500: 'quinhentos',
        600: 'seiscientos',
        700: 'sietecientos',
        800: 'uitocientos',
        900: 'nuobecientos'
    },
    FRACTION={
        2: 'meio',
        3: 'tércio',
        4: 'quarto',
        5: 'quinto',
        6: 'sesto',
        7: 'sétimo',
        8: 'uitabo',
        9: 'nono',
        10: 'décimo',
        11: 'onze abos',
        12: 'doze abos',
        13: 'treze abos',
        14: 'catorze abos',
        15: 'quinze abos',
        16: 'dezasseis abos',
        17: 'dezassete abos',
        18: 'dezoito abos',
        19: 'dezanuobe abos',
        20: 'bigésimo',
        30: 'trigésimo',
        100: 'centésimo',
        1000: 'milésimo'
    },
    FRACTION_FEMALE={
        2: "meia"  # ũa i meia -> 1.5
    },
    SHORT_SCALE={
        10 ** 21: "sextilion",
        10 ** 18: "quintilion",
        10 ** 15: "quadrilion",
        10 ** 12: "trilion",
        10 ** 9: "bilion",
        10 ** 6: "milhon",
        10 ** 3: "mil",
    },
    LONG_SCALE={
        10 ** 36: "sextilion",
        10 ** 30: "quintilion",
        10 ** 24: "quadrilion",
        10 ** 18: "trilion",
        10 ** 12: "bilion",
        10 ** 6: "milhon",
        10 ** 3: "mil",
    },
    GENDERED_SPELLINGS={
        GrammaticalGender.FEMININE: {
            1: "ũa",
            2: "dues"
        }
    },
    DIGIT_SPELLINGS={},
    ALT_SPELLINGS={
        'dezasseis': 16,
        'dezassiete': 17,
        'dezuito': 18,
        'dezanuobe': 19,
        'un ciento': 100,
        'dous cientos': 200,
        'trés cientos': 300,
        'quatro cientos': 400,
        'cinco cientos': 500,
        'seis cientos': 600,
        'siete cientos': 700,
        'uito cientos': 800,
        'nuobe cientos': 900,
        "bint": 20,
        "bint'i": 20
    },
    ORDINAL_UNITS={
        1: 'purmerio',
        2: 'segundo',
        3: 'terceiro',
        4: 'quarto',
        5: 'quinto',
        6: 'sesto',
        7: 'sétimo',
        8: 'uitabo',
        9: 'nono'
    },
    ORDINAL_TENS={
        10: 'décimo',
        20: 'bigésimo',
        30: 'trigésimo',
        40: 'quadragésimo',
        50: 'quinquagésimo',
        60: 'sessagésimo',
        70: 'setuagésimo',
        80: 'uctogésimo',
        90: 'nonagésimo'
    },
    ORDINAL_HUNDREDS={
        100: 'centésimo',
        200: 'ducentésimo',
        300: 'tricentésimo',
        400: 'quadringentésimo',
        500: 'quingentésimo',
        600: 'seiscentésimo',
        700: 'setingentésimo',
        800: 'uctingentésimo',
        900: 'noningentésimo'
    },
    ORDINAL_SHORT_SCALE={
        10 ** 21: "sextilionésimo",
        10 ** 18: "quintilionésimo",
        10 ** 15: "quadrilionésimo",
        10 ** 12: "trilionésimo",
        10 ** 9: "bilionésimo",
        10 ** 6: "milionésimo",
        10 ** 3: "milésimo"
    },
    ORDINAL_LONG_SCALE={
        10 ** 36: "sextilionésimo",
        10 ** 30: "quintilionésimo",
        10 ** 24: "quadrilionésimo",
        10 ** 18: "trilionésimo",
        10 ** 12: "bilionésimo",
        10 ** 6: "milionésimo",
        10 ** 3: "milésimo"
    }
)

MWL = RomanceNumberExtractor(_MWL)

##################################################################
# all methods below are deprecated and only for backwards compat
##################################################################

def pronounce_ordinal_mwl(
        number: Union[int, float],
        gender: GrammaticalGender = GrammaticalGender.MASCULINE,
        scale: Scale = Scale.LONG
) -> str:
    """
    DEPRECATED
    """
    warnings.warn(
        "migrate to use RomanceNumberExtractor and NumberVocabulary directly instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return MWL.pronounce_ordinal(number, gender, scale)


def is_fractional_mwl(
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
    return MWL.is_fractional(input_str)


def is_ordinal_mwl(input_str: str) -> bool:
    """
    DEPRECATED
    """
    warnings.warn(
        "migrate to use RomanceNumberExtractor and NumberVocabulary directly instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return MWL.is_ordinal(input_str)


def extract_number_mwl(
        text: str,
        ordinals: bool = False,
        scale: Scale = Scale.LONG,
) -> Union[int, float, bool]:
    """
    DEPRECATED
    """
    warnings.warn(
        "migrate to use RomanceNumberExtractor and NumberVocabulary directly instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return MWL.extract_number(text, ordinals, scale)


def pronounce_number_mwl(
        number: Union[int, float],
        places: int = 5,
        scale: Scale = Scale.LONG,
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
    return MWL.pronounce_number(number, places, scale, ordinals, digits, gender)


def numbers_to_digits_mwl(
        utterance: str,
        scale: Scale = Scale.LONG
) -> str:
    """
    DEPRECATED
    """
    warnings.warn(
        "migrate to use RomanceNumberExtractor and NumberVocabulary directly instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return MWL.numbers_to_digits(utterance, scale)



def pronounce_fraction_mwl(word: str, scale: Scale = Scale.LONG) -> str:
    """
    DEPRECATED
    """
    warnings.warn(
        "migrate to use RomanceNumberExtractor and NumberVocabulary directly instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return MWL.pronounce_fraction(word, scale)


if __name__ == "__main__":
    print("--- Testing Pronunciation (Short Scale) ---")
    print(f"1,234,567: {MWL.pronounce_number(1_234_567, scale=Scale.SHORT)}")
    print(f"1,000,000,000: {MWL.pronounce_number(1_000_000_000, scale=Scale.SHORT)}")

    print("\n--- Testing Pronunciation (Long Scale) ---")
    print(f"1,000,000: {MWL.pronounce_number(1_000_000, scale=Scale.LONG)}")
    print(f"1,000,100: {MWL.pronounce_number(1_000_100, scale=Scale.LONG)}")
    print(f"1,000,000,000: {MWL.pronounce_number(1_000_000_000, scale=Scale.LONG)}")
    print(f"1,000,000,000,000: {MWL.pronounce_number(1_000_000_000_000, scale=Scale.LONG)}")
    print(f"2,500,000,000: {MWL.pronounce_number(2_500_000_000, scale=Scale.LONG)}")
    print(f"2,500,123,456: {MWL.pronounce_number(2_500_123_456, scale=Scale.LONG)}")
    print(f"16: {MWL.pronounce_number(16)}")

    print("\n--- Testing Edge Cases ---")
    print(f"-123.45: {MWL.pronounce_number(-123.45)}")
    print(f"10.05: {MWL.pronounce_number(10.05)}")
    print(f"2000: {MWL.pronounce_number(2000)}")
    print(f"2001: {MWL.pronounce_number(2001)}")
    print(f"123.456789: {MWL.pronounce_number(123.456789)}")

    print("\n--- Testing Ordinal Pronunciation ---")
    print(f"1st (masculine): {MWL.pronounce_number(1, ordinals=True, gender=GrammaticalGender.MASCULINE)}")
    print(f"1st (feminine): {MWL.pronounce_number(1, ordinals=True, gender=GrammaticalGender.FEMININE)}")
    print(f"23rd (masculine): {MWL.pronounce_number(23, ordinals=True)}")
    print(f"23rd (feminine): {MWL.pronounce_number(23, ordinals=True, gender=GrammaticalGender.FEMININE)}")
    print(f"100th: {MWL.pronounce_number(100, ordinals=True)}")
    print(f"101st: {MWL.pronounce_number(101, ordinals=True)}")
    print(f"1000th: {MWL.pronounce_number(1000, ordinals=True)}")
    print(f"1,000,000th: {MWL.pronounce_number(1_000_000, ordinals=True)}")
    print(f"1,000,000,000,000th (long): {MWL.pronounce_number(1_000_000_000_000, ordinals=True, scale=Scale.LONG)}")

    print("\n--- Testing MWL.numbers_to_digits ---")
    print(f"'duzientos i cinquenta' -> '{MWL.numbers_to_digits('duzientos i cinquenta')}'")
    print(f"'un milhon' -> '{MWL.numbers_to_digits('un milhon')}'")
    print(f"'zasseis' -> '{MWL.numbers_to_digits('zasseis')}'")
    print(f"'hai duzientos i cinquenta carros' -> '{MWL.numbers_to_digits('hai duzientos i cinquenta carros')}'")

    print("\n--- Testing Ordinal Extraction ---")
    print(f"'l segundo carro' -> {MWL.extract_number('l segundo carro', ordinals=True)}")
    print(f"'purmerio lugar' -> {MWL.extract_number('purmerio lugar', ordinals=True)}")
    print(f"'l milésimo die' -> {MWL.extract_number('l milésimo dia', ordinals=True)}")
    print(f"'la milésima beç' -> {MWL.extract_number('la milésima beç', ordinals=True)}")
    print(f"'la purmeria beç' -> {MWL.extract_number('la purmeria beç', ordinals=True)}")
    print(f"'la sessagésima quarta beç' -> {MWL.extract_number('la sessagésima quarta beç', ordinals=True)}")

    print("\n--- Testing Cardinal Extraction ---")
    print(f"'un' -> {MWL.extract_number('un')}")
    print(f"'ũa' -> {MWL.extract_number('ũa')}")
    print(f"'bint'i un' ->", MWL.extract_number("bint'i un"))
    print(f"'bint'i ũa' ->", MWL.extract_number("bint'i ũa"))
    print(f"'bint'i dous' ->", MWL.extract_number("bint'i dous"))
    print(f"'bint'i dues' ->", MWL.extract_number("bint'i dues"))
    print(f"'un milhon' -> {MWL.extract_number('un milhon')}")
    print(f"'dous milhones e quinhentos' -> {MWL.extract_number('dous milhones i quinhentos')}")
    print(f"'mil i binte i trés' -> {MWL.extract_number('mil i binte i trés')}")
    print(f"'trinta i cinco bírgula quatro' -> {MWL.extract_number('trinta i cinco bírgula quatro')}")

    print("\n--- Testing Fractions ---")
    print(f"1/2: {MWL.pronounce_fraction('1/2')}")
    print(f"2/2: {MWL.pronounce_fraction('2/2')}")
    print(f"5/2: {MWL.pronounce_fraction('5/2')}")
    print(f"5/3: {MWL.pronounce_fraction('5/3')}")
    print(f"5/4: {MWL.pronounce_fraction('5/4')}")
    print(f"7/5: {MWL.pronounce_fraction('7/5')}")
    print(f"0/20: {MWL.pronounce_fraction('0/20')}")
