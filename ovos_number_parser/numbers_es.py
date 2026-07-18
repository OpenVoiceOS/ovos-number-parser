from typing import List, Optional, Union

from ovos_number_parser.util import (convert_to_mixed_fraction, tokenize, Token,
                                     Scale, GrammaticalGender, DigitPronunciation,
                                     NumberVocabulary, RomanceNumberExtractor)


def swap_gender_es(word: str, gender: GrammaticalGender) -> str:
    """Swap a Castilian number word to the requested grammatical gender.

    Only the words that actually inflect change: "uno"/"veintiuno" and the
    hundreds series ("doscientos".."novecientos", "quinientos"). Everything
    else - and the apocopated NEUTRAL forms used before scale nouns - is
    returned unchanged.
    """
    if gender == GrammaticalGender.FEMININE:
        if word.endswith("ientos"):  # doscientas ... quinientas ... novecientas
            return word[:-2] + "as"
        if word == "uno":
            return "una"
        if word.endswith("uno"):  # veintiuno -> veintiuna
            return word[:-1] + "a"
    return word


def pluralize_es(word: str) -> str:
    if word.endswith("ón"):  # millón -> millones, billón -> billones
        return word[:-2] + "ones"
    if not word.endswith("s"):
        return word + "s"
    return word


# https://blocs.xtec.cat/elruidodelalluvia/files/2013/12/nueva_ortografia_lengua_espanola.pdf
# RAE, Ortografía de la lengua española (2010): the series of ten and twenty are
# written as a single word ("dieciséis", "veintiuno"); from thirty on they are
# written apart ("treinta y uno"), with "y" joining only tens to units.
_ES = NumberVocabulary(
    LANG="es-ES",
    swap_gender=swap_gender_es,  # used for feminine forms
    pluralize=pluralize_es,  # used for plural forms

    HUNDRED_PARTICLE="ciento",  # "ciento uno" - "cien" only stands alone
    DENOMINATOR_PARTICLE="avos",  # for fractions  X / N {PARTICLE}
    DIVIDED_BY_ZERO="dividido por cero",  # how to read X/0 values
    NO_PREV_UNIT=[100, 1000],  # "cien"/"mil", never "un cien"/"un mil"
    NO_PLURAL=[1000],  # "dos mil", never "dos miles"

    NUMBER_OVERFLOW="número exageradamente grande",
    # Spain follows the long scale: millón 10^6, millardo 10^9, billón 10^12
    DEFAULT_SCALE=Scale.LONG,
    JOIN_WORD=["y"],

    JOINER_ON_TWENTYS=True,  # "treinta y uno"; 21-29 are fused, joiner kept for extraction
    JOINER_ON_HUNDREDS=False,  # "ciento cuatro", never "ciento y cuatro"
    JOINER_ON_THOUSANDS=False,  # "mil doscientos"
    JOINER_ON_SCALE_REMAINDER=False,  # "dos mil veintitrés", never "dos mil y..."

    # "uno" apocopates to "un" ("veintiuno" to "veintiún") before a scale noun;
    # NEUTRAL carries that pre-scale spelling so the standalone masculine stays "uno"
    SCALE_GENDERS={
        1000: GrammaticalGender.NEUTRAL,
        10 ** 6: GrammaticalGender.NEUTRAL,
        10 ** 9: GrammaticalGender.NEUTRAL,
        10 ** 12: GrammaticalGender.NEUTRAL,
        10 ** 18: GrammaticalGender.NEUTRAL,
        10 ** 24: GrammaticalGender.NEUTRAL,
        10 ** 30: GrammaticalGender.NEUTRAL,
        10 ** 36: GrammaticalGender.NEUTRAL,
    },
    SCALE_ONE={
        10 ** 6: "un millón",
        10 ** 9: "un millardo",
        10 ** 12: "un billón",
        10 ** 18: "un trillón",
        10 ** 24: "un cuatrillón",
        10 ** 30: "un quintillón",
        10 ** 36: "un sextillón",
    },

    DECIMAL_MARKER=["coma", "punto", ".", ","],
    NEGATIVE_SIGN=["menos"],
    UNITS={
        0: 'cero',
        1: 'uno',
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
        20: 'veinte',
        # the twenties are written solid (RAE Ort. 2010, p. 671)
        21: 'veintiuno',
        22: 'veintidós',
        23: 'veintitrés',
        24: 'veinticuatro',
        25: 'veinticinco',
        26: 'veintiséis',
        27: 'veintisiete',
        28: 'veintiocho',
        29: 'veintinueve',
        30: 'treinta',
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
        2: 'medio',
        3: 'tercio',
        4: 'cuarto',
        5: 'quinto',
        6: 'sexto',
        7: 'séptimo',
        8: 'octavo',
        9: 'noveno',
        10: 'décimo',
        11: 'onceavo',
        12: 'doceavo',
        13: 'treceavo',
        14: 'catorceavo',
        15: 'quinceavo',
        16: 'dieciseisavo',
        17: 'diecisieteavo',
        18: 'dieciochoavo',
        19: 'diecinueveavo',
        20: 'veinteavo',
        100: 'centésimo',
        1000: 'milésimo'
    },
    FRACTION_FEMALE={
        2: "media",
        4: "cuarta",
        100: "centésima",
        1000: "milésima"
    },
    SHORT_SCALE={
        10 ** 3: "mil",
        10 ** 6: "millón",
        10 ** 9: "billón",
        10 ** 12: "trillón",
        10 ** 15: "cuatrillón",
        10 ** 18: "quintillón",
        10 ** 21: "sextillón"
    },
    LONG_SCALE={
        10 ** 3: "mil",
        10 ** 6: "millón",
        10 ** 9: "millardo",
        10 ** 12: "billón",
        10 ** 18: "trillón",
        10 ** 24: "cuatrillón",
        10 ** 30: "quintillón",
        10 ** 36: "sextillón"
    },

    GENDERED_SPELLINGS={
        GrammaticalGender.FEMININE: {
            1: "una",
        },
        # apocopated masculine used before a scale noun ("un millón",
        # "veintiún mil", "treinta y un mil")
        GrammaticalGender.NEUTRAL: {
            1: "un",
            21: "veintiún",
        },
    },
    DIGIT_SPELLINGS={},
    ALT_SPELLINGS={
        # apocopated forms and accent-free variants, accepted for extraction
        "un": 1,
        "trés": 3,
        "dieciseis": 16,
        "veintiún": 21,
        "veintidos": 22,
        "veintitres": 23,
        "veintiseis": 26,
        "ciento": 100,
        "millon": 10 ** 6,
        # "millardo" (10^9) is RAE-accepted alongside "mil millones"
        "millardo": 10 ** 9,
        "millardos": 10 ** 9,
    },
    ORDINAL_UNITS={
        1: 'primero',
        2: 'segundo',
        3: 'tercero',
        4: 'cuarto',
        5: 'quinto',
        6: 'sexto',
        7: 'séptimo',
        8: 'octavo',
        9: 'noveno'
    },
    ORDINAL_TENS={
        10: 'décimo',
        20: 'vigésimo',
        30: 'trigésimo',
        40: 'cuadragésimo',
        50: 'quincuagésimo',
        60: 'sexagésimo',
        70: 'septuagésimo',
        80: 'octogésimo',
        90: 'nonagésimo'
    },
    ORDINAL_HUNDREDS={
        100: 'centésimo',
        200: 'ducentésimo',
        300: 'tricentésimo',
        400: 'cuadringentésimo',
        500: 'quingentésimo',
        600: 'sexcentésimo',
        700: 'septingentésimo',
        800: 'octingentésimo',
        900: 'noningentésimo'
    },
    ORDINAL_SHORT_SCALE={
        10 ** 3: "milésimo",
        10 ** 6: "millonésimo",
        10 ** 9: "billonésimo",
        10 ** 12: "trillonésimo"
    },
    ORDINAL_LONG_SCALE={
        10 ** 3: "milésimo",
        10 ** 6: "millonésimo",
        10 ** 12: "billonésimo",
        10 ** 18: "trillonésimo"
    }
)

ES = RomanceNumberExtractor(_ES)

# fraction denominator spellings kept for nice_number_es
_FRACTION_STRING_ES = {
    2: 'medio',
    3: 'tercio',
    4: 'cuarto',
    5: 'quinto',
    6: 'sexto',
    7: 'séptimo',
    8: 'octavo',
    9: 'noveno',
    10: 'décimo',
    11: 'onceavo',
    12: 'doceavo',
    13: 'treceavo',
    14: 'catorceavo',
    15: 'quinceavo',
    16: 'dieciseisavo',
    17: 'diecisieteavo',
    18: 'dieciochoavo',
    19: 'diecinueveavo',
    20: 'veinteavo'
}


def extract_number_es(text, short_scale=True, ordinals=False):
    """Extract a number from Castilian Spanish text.

    Delegates to the shared :class:`RomanceNumberExtractor`. The Spanish
    vocabulary follows RAE, *Ortografía de la lengua española* (2010, p. 671):
    the twenties are written solid ("veintiuno".."veintinueve") while from
    thirty on the parts stand apart ("treinta y uno"), "y" joins only tens to
    units, and "cien" apocopates to "ciento" inside compounds.

    This low-level entry point defaults ``short_scale`` to ``True``. The public
    :func:`ovos_number_parser.extract_number` wrapper instead resolves the scale
    from the language configuration, applying the long scale used in Spain
    (millón 10^6, billón 10^12) that Castilian Spanish speakers expect.

    Args:
        text (str): the string to extract a number from
        short_scale (bool): use the short scale (default) instead of the long scale
        ordinals (bool): also recognise ordinal words
    Returns:
        (int, float) or False: the extracted number, or False if none is found
    """
    scale = Scale.SHORT if short_scale else _ES.DEFAULT_SCALE
    return ES.extract_number(text, ordinals=ordinals, scale=scale)


def is_fractional_es(input_str, short_scale=True):
    """Return the fractional value of a Spanish fraction word, else False."""
    return ES.is_fractional(input_str)


def pronounce_number_es(number, places=2, short_scale=False):
    """Convert a number to its spoken Castilian Spanish form.

    Decimals are read digit by digit ("tres coma uno cuatro").

    Args:
        number (float or int): the number to pronounce
        places (int): maximum decimal places to speak
        short_scale (bool): use the short scale instead of the default long scale
    Returns:
        (str): the pronounced number
    """
    scale = Scale.SHORT if short_scale else _ES.DEFAULT_SCALE
    return ES.pronounce_number(number, places=places, scale=scale,
                               digits=DigitPronunciation.DIGIT_BY_DIGIT)


def numbers_to_digits_es(utterance: str) -> str:
    """Replace written numbers in Spanish text with their digit equivalents."""
    return ES.numbers_to_digits(utterance)


def nice_number_es(number, speech=True, denominators=range(1, 21)):
    """ Spanish helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 y medio" for speech and "4 1/2" for text

    Args:
        number (int or float): the float to format
        speech (bool): format for speech (True) or display (False)
        denominators (iter of ints): denominators to use, default [1 .. 20]
    Returns:
        (str): The formatted string.
    """
    strNumber = ""
    whole = 0
    num = 0
    den = 0

    result = convert_to_mixed_fraction(number, denominators)

    if not result:
        # Give up, just represent as a 3 decimal number
        whole = round(number, 3)
    else:
        whole, num, den = result

    if not speech:
        if num == 0:
            strNumber = '{:,}'.format(whole)
            strNumber = strNumber.replace(",", " ")
            strNumber = strNumber.replace(".", ",")
            return strNumber
        else:
            return '{} {}/{}'.format(whole, num, den)
    else:
        if num == 0:
            # if the number is not a fraction, nothing to do
            strNumber = str(whole)
            strNumber = strNumber.replace(".", ",")
            return strNumber
        den_str = _FRACTION_STRING_ES[den]
        # if it is not an integer
        if whole == 0:
            # if there is no whole number
            if num == 1:
                # if numerator is 1, return "un medio", for example
                strNumber = 'un {}'.format(den_str)
            else:
                # else return "cuatro tercios", for example
                strNumber = '{} {}'.format(num, den_str)
        elif num == 1:
            # if there is a whole number and numerator is 1
            if den == 2:
                # if denominator is 2, return "1 y medio", for example
                strNumber = '{} y {}'.format(whole, den_str)
            else:
                # else return "1 y 1 tercio", for example
                strNumber = '{} y 1 {}'.format(whole, den_str)
        else:
            # else return "2 y 3 cuarto", for example
            strNumber = '{} y {} {}'.format(whole, num, den_str)
        if num > 1:
            # pluralize the denominator ("dos tercios", "tres cuartos")
            strNumber += 's'

    return strNumber
