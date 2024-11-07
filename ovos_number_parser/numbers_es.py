from collections import OrderedDict

from ovos_number_parser.util import (convert_to_mixed_fraction, look_for_fractions,
                                     is_numeric, tokenize)

_ARTICLES_ES = {'el', 'la', 'los', 'las'}

_NUM_STRING_ES = {
    0: 'cero',
    1: 'uno',
    2: 'dos',
    3: 'tres',
    4: 'cuatro',
    5: 'cinco',
    6: 'seis',
    7: 'siete',
    8: 'ocho',
    9: 'nueve',
    10: 'diez',
    11: 'once',
    12: 'doce',
    13: 'trece',
    14: 'catorce',
    15: 'quince',
    16: 'dieciséis',
    17: 'diecisete',
    18: 'dieciocho',
    19: 'diecinueve',
    20: 'veinte',
    30: 'treinta',
    40: 'cuarenta',
    50: 'cincuenta',
    60: 'sesenta',
    70: 'setenta',
    80: 'ochenta',
    90: 'noventa'
}

_STRING_NUM_ES = {
    "cero": 0,
    "un": 1,
    "uno": 1,
    "una": 1,
    "dos": 2,
    "tres": 3,
    "trés": 3,
    "cuatro": 4,
    "cinco": 5,
    "seis": 6,
    "siete": 7,
    "ocho": 8,
    "nueve": 9,
    "diez": 10,
    "once": 11,
    "doce": 12,
    "trece": 13,
    "catorce": 14,
    "quince": 15,
    "dieciseis": 16,
    "dieciséis": 16,
    "diecisiete": 17,
    "dieciocho": 18,
    "diecinueve": 19,
    "veinte": 20,
    "veintiuno": 21,
    "veintidos": 22,
    "veintitres": 23,
    "veintidós": 22,
    "veintitrés": 23,
    "veinticuatro": 24,
    "veinticinco": 25,
    "veintiséis": 26,
    "veintiseis": 26,
    "veintisiete": 27,
    "veintiocho": 28,
    "veintinueve": 29,
    "treinta": 30,
    "cuarenta": 40,
    "cincuenta": 50,
    "sesenta": 60,
    "setenta": 70,
    "ochenta": 80,
    "noventa": 90,
    "cien": 100,
    "ciento": 100,
    "doscientos": 200,
    "doscientas": 200,
    "trescientos": 300,
    "trescientas": 300,
    "cuatrocientos": 400,
    "cuatrocientas": 400,
    "quinientos": 500,
    "quinientas": 500,
    "seiscientos": 600,
    "seiscientas": 600,
    "setecientos": 700,
    "setecientas": 700,
    "ochocientos": 800,
    "ochocientas": 800,
    "novecientos": 900,
    "novecientas": 900,
    "mil": 1000}

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

# https://www.grobauer.at/es_eur/zahlnamen.php
_LONG_SCALE_ES = OrderedDict([
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

_SHORT_SCALE_ES = OrderedDict([
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
    (1e69, "uuovigintillón"),
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
    (1e543, "ctogintacentillón"),
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
_ORDINAL_STRING_BASE_ES = {
    1: 'primero',
    2: 'segundo',
    3: 'tercero',
    4: 'cuarto',
    5: 'quinto',
    6: 'sexto',
    7: 'séptimo',
    8: 'octavo',
    9: 'noveno',
    10: 'décimo',
    11: 'undécimo',
    12: 'duodécimo',
    13: 'decimotercero',
    14: 'decimocuarto',
    15: 'decimoquinto',
    16: 'decimosexto',
    17: 'decimoséptimo',
    18: 'decimoctavo',
    19: 'decimonoveno',
    20: 'vigésimo',
    30: 'trigésimo',
    40: "cuadragésimo",
    50: "quincuagésimo",
    60: "sexagésimo",
    70: "septuagésimo",
    80: "octogésimo",
    90: "nonagésimo",
    10e3: "centésimó",
    1e3: "milésimo"
}

_SHORT_ORDINAL_STRING_ES = {
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
_SHORT_ORDINAL_STRING_ES.update(_ORDINAL_STRING_BASE_ES)

_LONG_ORDINAL_STRING_ES = {
    1e6: "millonésimo",
    1e12: "billionth",
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
_LONG_ORDINAL_STRING_ES.update(_ORDINAL_STRING_BASE_ES)


def is_fractional_es(input_str, short_scale=True):
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

    aFrac = {"medio": 2, "media": 2, "tercio": 3, "cuarto": 4,
             "cuarta": 4, "quinto": 5, "quinta": 5, "sexto": 6, "sexta": 6,
             "séptimo": 7, "séptima": 7, "octavo": 8, "octava": 8,
             "noveno": 9, "novena": 9, "décimo": 10, "décima": 10,
             "onceavo": 11, "onceava": 11, "doceavo": 12, "doceava": 12}

    if input_str.lower() in aFrac:
        return 1.0 / aFrac[input_str]
    if (input_str == "vigésimo" or input_str == "vigésima"):
        return 1.0 / 20
    if (input_str == "trigésimo" or input_str == "trigésima"):
        return 1.0 / 30
    if (input_str == "centésimo" or input_str == "centésima"):
        return 1.0 / 100
    if (input_str == "milésimo" or input_str == "milésima"):
        return 1.0 / 1000
    return False


def extract_number_es(text, short_scale=True, ordinals=False):
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
    # Returns incorrect output on certain fractional phrases like, "cuarto de dos"
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
        if word in _STRING_NUM_ES:
            val = _STRING_NUM_ES[word]
        elif word.isdigit():  # doesn't work with decimals
            val = int(word)
        elif is_numeric(word):
            val = float(word)
        elif is_fractional_es(word):
            if not result:
                result = 1
            result = result * is_fractional_es(word)
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
        ands = ["y"]
        if next_word in ands:
            zeros = 0
            if result is None:
                count += 1
                continue
            newWords = aWords[count + 2:]
            newText = ""
            for word in newWords:
                newText += word + " "

            afterAndVal = extract_number_es(newText[:-1])
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
                afterAndVal = extract_number_es(newText[:-1])
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
            afterDotVal = str(extract_number_es(newText[:-1]))
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


def _es_number_parse(words, i):
    # TODO Not parsing 'cero'

    def es_cte(i, s):
        if i < len(words) and s == words[i]:
            return s, i + 1
        return None

    def es_number_word(i, mi, ma):
        if i < len(words):
            v = _STRING_NUM_ES.get(words[i])
            if v and v >= mi and v <= ma:
                return v, i + 1
        return None

    def es_number_1_99(i):
        r1 = es_number_word(i, 1, 29)
        if r1:
            return r1

        r1 = es_number_word(i, 30, 90)
        if r1:
            v1, i1 = r1
            r2 = es_cte(i1, "y")
            if r2:
                i2 = r2[1]
                r3 = es_number_word(i2, 1, 9)
                if r3:
                    v3, i3 = r3
                    return v1 + v3, i3
            return r1
        return None

    def es_number_1_999(i):
        # [2-9]cientos [1-99]?
        r1 = es_number_word(i, 100, 900)
        if r1:
            v1, i1 = r1
            r2 = es_number_1_99(i1)
            if r2:
                v2, i2 = r2
                return v1 + v2, i2
            else:
                return r1

        # [1-99]
        r1 = es_number_1_99(i)
        if r1:
            return r1

        return None

    def es_number(i):
        # check for cero
        r1 = es_number_word(i, 0, 0)
        if r1:
            return r1

        # check for [1-999] (mil [0-999])?
        r1 = es_number_1_999(i)
        if r1:
            v1, i1 = r1
            r2 = es_cte(i1, "mil")
            if r2:
                i2 = r2[1]
                r3 = es_number_1_999(i2)
                if r3:
                    v3, i3 = r3
                    return v1 * 1000 + v3, i3
                else:
                    return v1 * 1000, i2
            else:
                return r1
        return None

    return es_number(i)


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
            strNumber = strNumber.replace(",", " ")
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
        if num > 1 and den != 3:
            # if the numerator is greater than 1 and the denominator
            # is not 3 ("tercio"), add an s for plural
            strNumber += 's'

    return strNumber


def pronounce_number_es(number, places=2):
    """
    Convert a number to it's spoken equivalent

    For example, '5.2' would return 'cinco coma dos'

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

    # del 21 al 29 tienen una pronunciación especial
    if 20 <= number <= 29:
        tens = int(number - int(number) % 10)
        ones = int(number - tens)
        result += _NUM_STRING_ES[tens]
        if ones > 0:
            result = result[:-1]
            # a veinte le quitamos la "e" final para construir los
            # números del 21 - 29. Pero primero tenemos en cuenta
            # las excepciones: 22, 23 y 26, que llevan tilde.
            if ones == 2:
                result += "idós"
            elif ones == 3:
                result += "itrés"
            elif ones == 6:
                result += "iséis"
            else:
                result += "i" + _NUM_STRING_ES[ones]
    elif number >= 30:  # de 30 en adelante
        tens = int(number - int(number) % 10)
        ones = int(number - tens)
        result += _NUM_STRING_ES[tens]
        if ones > 0:
            result += " y " + _NUM_STRING_ES[ones]
    else:
        result += _NUM_STRING_ES[int(number)]

    # Deal with decimal part, in spanish is commonly used the comma
    # instead the dot. Decimal part can be written both with comma
    # and dot, but when pronounced, its pronounced "coma"
    if not number == int(number) and places > 0:
        if abs(number) < 1.0 and (result == "menos " or not result):
            result += "cero"
        result += " coma"
        _num_str = str(number)
        _num_str = _num_str.split(".")[1][0:places]
        for char in _num_str:
            result += " " + _NUM_STRING_ES[int(char)]
    return result

def numbers_to_digits_es(utterance: str) -> str:
    """
    Replace written numbers in a Spanish text with their digit equivalents.

    Args:
        utterance (str): Input string possibly containing written numbers.

    Returns:
        str: Text with written numbers replaced by digits.
    """
    number_replacements = {
        "uno": "1", "dos": "2", "tres": "3", "cuatro": "4",
        "cinco": "5", "seis": "6", "siete": "7", "ocho": "8", "nueve": "9",
        "diez": "10", "once": "11", "doce": "12", "trece": "13", "catorce": "14",
        "quince": "15", "dieciséis": "16", "diecisiete": "17", "dieciocho": "18",
        "diecinueve": "19", "veinte": "20"
        # Extend this dictionary for higher numbers as needed
    }
    words = tokenize(utterance)
    for idx, word in enumerate(words):
        if word in number_replacements:
            words[idx] = number_replacements[word]
    return " ".join(words)