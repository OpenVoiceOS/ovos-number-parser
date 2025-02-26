from collections import OrderedDict
from typing import List

from ovos_number_parser.util import (convert_to_mixed_fraction, look_for_fractions,
                                     is_numeric, tokenize, Token)

_NUM_STRING_GL = {
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
}

_STRING_NUM_GL = {
    "cero": 0,
    "un": 1,
    "unha": 1,
    "dous": 2,
    "tres": 3,
    "catro": 4,
    "cinco": 5,
    "seis": 6,
    "sete": 7,
    "oito": 8,
    "nove": 9,
    "dez": 10,
    "once": 11,
    "doce": 12,
    "trece": 13,
    "catorce": 14,
    "quince": 15,
    "dezaseis": 16,
    "dezasete": 17,
    "dezaoito": 18,
    "dezanove": 19,
    "vinte": 20,
    "vinte e un": 21,
    "vinte e dous": 22,
    "vinte e tres": 23,
    "vinte e catro": 24,
    "vinte e cinco": 25,
    "vinte e seis": 26,
    "vinte e sete": 27,
    "vinte e oito": 28,
    "vinte e nove": 29,
    "trinta": 30,
    "corenta": 40,
    "cincuenta": 50,
    "sesenta": 60,
    "setenta": 70,
    "oitenta": 80,
    "noventa": 90,
    "cen": 100,
    "cento": 100,
    "douscentos": 200,
    "duascentas": 200,
    "trescentos": 300,
    "trescentas": 300,
    "catrocentos": 400,
    "catrocentas": 400,
    "cincocentos": 500,
    "cincocentas": 500,
    "seiscentos": 600,
    "seiscentas": 600,
    "setecentos": 700,
    "setecentas": 700,
    "oitocentos": 800,
    "oitocentas": 800,
    "novecentos": 900,
    "novecentas": 900,
    "mil": 1000}

_FRACTION_STRING_GL = {
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
    20: 'vinteavo'
}

# https://www.grobauer.at/gl_eur/zahlnamen.php
_LONG_SCALE_GL = OrderedDict([
    (100, 'centena'),
    (1000, 'millar'),
    (1000000, 'millón'),
    (1e9, "millardo"),
    (1e12, "billón"),
    (1e18, 'trillón'),
    (1e24, "cuatrillón"),
    (1e30, "quintillón"),
    (1e36, "sextillón"),
    (1e42, "septillón"),
    (1e48, "octillón"),
    (1e54, "nonillón"),
    (1e60, "decillón"),
    (1e66, "undecillón"),
    (1e72, "duodecillón"),
    (1e78, "tredecillón"),
    (1e84, "cuatrodecillón"),
    (1e90, "quindecillón"),
    (1e96, "sexdecillón"),
    (1e102, "septendecillón"),
    (1e108, "octodecillón"),
    (1e114, "novendecillón"),
    (1e120, "vigintillón"),
    (1e306, "unquinquagintillón"),
    (1e312, "duoquinquagintillón"),
    (1e336, "sexquinquagintillón"),
    (1e366, "unsexagintillón")
])

_SHORT_SCALE_GL = OrderedDict([
    (100, 'centena'),
    (1000, 'millar'),
    (1000000, 'millón'),
    (1e9, "billón"),
    (1e12, 'trillón'),
    (1e15, "cuatrillón"),
    (1e18, "quintillón"),
    (1e21, "sextillón"),
    (1e24, "septillón"),
    (1e27, "octillón"),
    (1e30, "nonillón"),
    (1e33, "decillón"),
    (1e36, "undecillón"),
    (1e39, "duodecillón"),
    (1e42, "tredecillón"),
    (1e45, "cuatrodecillón"),
    (1e48, "quindecillón"),
    (1e51, "sexdecillón"),
    (1e54, "septendecillón"),
    (1e57, "octodecillón"),
    (1e60, "novendecillón"),
    (1e63, "vigintillón"),
    (1e66, "unvigintillón"),
    (1e69, "unovigintillón"),
    (1e72, "tresvigintillón"),
    (1e75, "quattuorvigintillón"),
    (1e78, "quinquavigintillón"),
    (1e81, "qesvigintillón"),
    (1e84, "septemvigintillón"),
    (1e87, "octovigintillón"),
    (1e90, "novemvigintillón"),
    (1e93, "trigintillón"),
    (1e96, "untrigintillón"),
    (1e99, "duotrigintillón"),
    (1e102, "trestrigintillón"),
    (1e105, "quattuortrigintillón"),
    (1e108, "quinquatrigintillón"),
    (1e111, "sestrigintillón"),
    (1e114, "septentrigintillón"),
    (1e117, "octotrigintillón"),
    (1e120, "noventrigintillón"),
    (1e123, "quadragintillón"),
    (1e153, "quinquagintillón"),
    (1e183, "sexagintillón"),
    (1e213, "septuagintillón"),
    (1e243, "octogintillón"),
    (1e273, "nonagintillón"),
    (1e303, "centillón"),
    (1e306, "uncentillón"),
    (1e309, "duocentillón"),
    (1e312, "trescentillón"),
    (1e333, "decicentillón"),
    (1e336, "undecicentillón"),
    (1e363, "viginticentillón"),
    (1e366, "unviginticentillón"),
    (1e393, "trigintacentillón"),
    (1e423, "quadragintacentillón"),
    (1e453, "quinquagintacentillón"),
    (1e483, "sexagintacentillón"),
    (1e513, "septuagintacentillón"),
    (1e543, "octogintacentillón"),
    (1e573, "nonagintacentillón"),
    (1e603, "ducentillón"),
    (1e903, "trecentillón"),
    (1e1203, "quadringentillón"),
    (1e1503, "quingentillón"),
    (1e1803, "sexcentillón"),
    (1e2103, "septingentillón"),
    (1e2403, "octingentillón"),
    (1e2703, "nongentillón"),
    (1e3003, "millinillón")
])

# TODO: female forms.
_ORDINAL_STRING_BASE_GL = {
    1: 'primeiro',
    2: 'segundo',
    3: 'terceiro',
    4: 'cuarto',
    5: 'quinto',
    6: 'sexto',
    7: 'séptimo',
    8: 'oitavo',
    9: 'noveno',
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
    90: "nonaxésimo",
    10e3: "centésimo",
    1e3: "milésimo"
}

_SHORT_ORDINAL_STRING_GL = {
    1e6: "millonésimo",
    1e9: "milmillonésimo",
    1e12: "billonésimo",
    1e15: "milbillonésimo",
    1e18: "trillonésimo",
    1e21: "miltrillonésimo",
    1e24: "cuatrillonésimo",
    1e27: "milcuatrillonésimo",
    1e30: "quintillonésimo",
    1e33: "milquintillonésimo"
    # TODO > 1e-33
}
_SHORT_ORDINAL_STRING_GL.update(_ORDINAL_STRING_BASE_GL)

_LONG_ORDINAL_STRING_GL = {
    1e6: "millonésimo",
    1e12: "billonésimo",
    1e18: "trillonésimo",
    1e24: "cuatrillonésimo",
    1e30: "quintillonésimo",
    1e36: "sextillonésimo",
    1e42: "septillonésimo",
    1e48: "octillonésimo",
    1e54: "nonillonésimo",
    1e60: "decillonésimo"
    # TODO > 1e60
}
_LONG_ORDINAL_STRING_GL.update(_ORDINAL_STRING_BASE_GL)


def is_fractional_gl(input_str, short_scale=True):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        text (str): the string to check if fractional

        short_scale (bool): use short scale if True, long scale if False
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    if input_str.endswith('s', -1):
        input_str = input_str[:len(input_str) - 1]  # e.g. "fifths"

    aFrac = {"medio": 2, "media": 2, "terzo": 3, "cuarto": 4,
             "cuarta": 4, "quinto": 5, "quinta": 5, "sexto": 6, "sexta": 6,
             "séptimo": 7, "séptima": 7, "oitavo": 8, "oitava": 8,
             "noveno": 9, "novena": 9, "décimo": 10, "décima": 10,
             "onceavo": 11, "onceava": 11, "doceavo": 12, "doceava": 12}

    if input_str.lower() in aFrac:
        return 1.0 / aFrac[input_str]
    if (input_str == "vixésimo" or input_str == "vixésima"):
        return 1.0 / 20
    if (input_str == "trixésimo" or input_str == "trixésima"):
        return 1.0 / 30
    if (input_str == "centésimo" or input_str == "centésima"):
        return 1.0 / 100
    if (input_str == "milésimo" or input_str == "milésima"):
        return 1.0 / 1000
    return False


def extract_number_gl(text, short_scale=True, ordinals=False):
    """
    This function prepares the given text for parsing by making
    numbers consistent, getting rid of contractions, etc.
    Args:
        text (str): the string to normalize
    Returns:
        (int) or (float): The value of extracted number

    """
    # TODO: short_scale and ordinals don't do anything here.
    # The parameters are present in the function signature for API compatibility
    # reasons.
    #
    # Returns incorrect output on certain fractional phrases like, "cuarto de dous"
    #  TODO: numbers greater than 999999
    aWords = text.lower().split()
    count = 0
    result = None
    while count < len(aWords):
        val = 0
        word = aWords[count]
        next_next_word = None
        if count + 1 < len(aWords):
            next_word = aWords[count + 1]
            if count + 2 < len(aWords):
                next_next_word = aWords[count + 2]
        else:
            next_word = None

        # is current word a number?
        if word in _STRING_NUM_GL:
            val = _STRING_NUM_GL[word]
        elif word.isdigit():  # doesn't work with decimals
            val = int(word)
        elif is_numeric(word):
            val = float(word)
        elif is_fractional_gl(word):
            if not result:
                result = 1
            result = result * is_fractional_gl(word)
            count += 1
            continue

        if not val:
            # look for fractions like "2/3"
            aPieces = word.split('/')
            # if (len(aPieces) == 2 and is_numeric(aPieces[0])
            #   and is_numeric(aPieces[1])):
            if look_for_fractions(aPieces):
                val = float(aPieces[0]) / float(aPieces[1])

        if val:
            if result is None:
                result = 0
            # handle fractions
            if next_word != "avos":
                result = val
            else:
                result = float(result) / float(val)

        if next_word is None:
            break

        # number word and fraction
        ands = ["e"]
        if next_word in ands:
            zeros = 0
            if result is None:
                count += 1
                continue
            newWords = aWords[count + 2:]
            newText = ""
            for word in newWords:
                newText += word + " "

            afterAndVal = extract_number_gl(newText[:-1])
            if afterAndVal:
                if result < afterAndVal or result < 20:
                    while afterAndVal > 1:
                        afterAndVal = afterAndVal / 10.0
                    for word in newWords:
                        if word == "cero" or word == "0":
                            zeros += 1
                        else:
                            break
                for _ in range(0, zeros):
                    afterAndVal = afterAndVal / 10.0
                result += afterAndVal
                break
        elif next_next_word is not None:
            if next_next_word in ands:
                newWords = aWords[count + 3:]
                newText = ""
                for word in newWords:
                    newText += word + " "
                afterAndVal = extract_number_gl(newText[:-1])
                if afterAndVal:
                    if result is None:
                        result = 0
                    result += afterAndVal
                    break

        decimals = ["punto", "coma", ".", ","]
        if next_word in decimals:
            zeros = 0
            newWords = aWords[count + 2:]
            newText = ""
            for word in newWords:
                newText += word + " "
            for word in newWords:
                if word == "cero" or word == "0":
                    zeros += 1
                else:
                    break
            afterDotVal = str(extract_number_gl(newText[:-1]))
            afterDotVal = zeros * "0" + afterDotVal
            result = float(str(result) + "." + afterDotVal)
            break
        count += 1

    # Return the $str with the number related words removed
    # (now empty strings, so strlen == 0)
    # aWords = [word for word in aWords if len(word) > 0]
    # text = ' '.join(aWords)
    if "." in str(result):
        integer, dec = str(result).split(".")
        # cast float to int
        if dec == "0":
            result = int(integer)

    return result or False


def _gl_number_parse(words, i):
    # TODO Not parsing 'cero'

    def gl_cte(i, s):
        if i < len(words) and s == words[i]:
            return s, i + 1
        return None

    def gl_number_word(i, mi, ma):
        if i < len(words):
            v = _STRING_NUM_GL.get(words[i])
            if v and v >= mi and v <= ma:
                return v, i + 1
        return None

    def gl_number_1_99(i):
        r1 = gl_number_word(i, 1, 29)
        if r1:
            return r1

        r1 = gl_number_word(i, 30, 90)
        if r1:
            v1, i1 = r1
            r2 = gl_cte(i1, "y")
            if r2:
                i2 = r2[1]
                r3 = gl_number_word(i2, 1, 9)
                if r3:
                    v3, i3 = r3
                    return v1 + v3, i3
            return r1
        return None

    def gl_number_1_999(i):
        # [2-9]centos [1-99]?
        r1 = gl_number_word(i, 100, 900)
        if r1:
            v1, i1 = r1
            r2 = gl_number_1_99(i1)
            if r2:
                v2, i2 = r2
                return v1 + v2, i2
            else:
                return r1

        # [1-99]
        r1 = gl_number_1_99(i)
        if r1:
            return r1

        return None

    def gl_number(i):
        # check for cero
        r1 = gl_number_word(i, 0, 0)
        if r1:
            return r1

        # check for [1-999] (mil [0-999])?
        r1 = gl_number_1_999(i)
        if r1:
            v1, i1 = r1
            r2 = gl_cte(i1, "mil")
            if r2:
                i2 = r2[1]
                r3 = gl_number_1_999(i2)
                if r3:
                    v3, i3 = r3
                    return v1 * 1000 + v3, i3
                else:
                    return v1 * 1000, i2
            else:
                return r1
        return None

    return gl_number(i)


def nice_number_gl(number, speech=True, denominators=range(1, 21)):
    """ Galician helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 e medio" for speech and "4 1/2" for text

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
        den_str = _FRACTION_STRING_GL[den]
        # if it is not an integer
        if whole == 0:
            # if there is no whole number
            if num == 1:
                # if numerator is 1, return "un medio", for example
                strNumber = 'un {}'.format(den_str)
            else:
                # else return "catro terzos", for example
                strNumber = '{} {}'.format(num, den_str)
        elif num == 1:
            # if there is a whole number and numerator is 1
            if den == 2:
                # if denominator is 2, return "1 e medio", for example
                strNumber = '{} y {}'.format(whole, den_str)
            else:
                # else return "1 e 1 terzo", for example
                strNumber = '{} y 1 {}'.format(whole, den_str)
        else:
            # else return "2 e 3 cuarto", for example
            strNumber = '{} y {} {}'.format(whole, num, den_str)
        if num > 1 and den != 3:
            # if the numerator is greater than 1 and the denominator
            # is not 3 ("terzo"), add an s for plural
            strNumber += 's'

    return strNumber


def pronounce_number_gl(number, places=2):
    """
    Convert a number to it's spoken equivalent

    For example, '5.2' would return 'cinco coma dous'

    Args:
        num(float or int): the number to pronounce (under 100)
        places(int): maximum decimal places to speak
    Returns:
        (str): The pronounced number
    """
    if abs(number) >= 100:
        # TODO: Soporta a números por encima de 100
        return str(number)

    result = ""
    if number < 0:
        result = "menos "
        number = abs(number)
    elif number >= 30:  # de 30 en adelante
        tens = int(number - int(number) % 10)
        ones = int(number - tens)
        result += _NUM_STRING_GL[tens]
        if ones > 0:
            result += " y " + _NUM_STRING_GL[ones]
    else:
        result += _NUM_STRING_GL[int(number)]

    # Deal with decimal part, in galician is commonly used the comma
    # instead dot. Decimal part can be written both with comma
    # and dot, but when pronounced, its pronounced "coma"
    if not number == int(number) and places > 0:
        if abs(number) < 1.0 and (result == "menos " or not result):
            result += "cero"
        result += " coma"
        _num_str = str(number)
        _num_str = _num_str.split(".")[1][0:places]
        for char in _num_str:
            result += " " + _NUM_STRING_GL[int(char)]
    return result


def numbers_to_digits_gl(utterance: str) -> str:
    """
    Replace written numbers in a Galician text with their digit equivalents.

       "un dous catro" -> "1 2 4"

    Args:
        utterance (str): Input string possibly containing written numbers.

    Returns:
        str: Text with written numbers replaced by digits.
    """
    # TODO - above twenty it's ambiguous, "twenty one" is 2 words but only 1 number
    mapping = {_NUM_STRING_GL[i + 1]: str(i + 1) for i in range(20)}
    words: List[Token] = tokenize(utterance)
    for idx, tok in enumerate(words):
        if tok.word in mapping:
            words[idx] = mapping[tok.word]
        else:
            words[idx] = tok.word
    return " ".join(words)
