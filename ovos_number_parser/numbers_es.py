from collections import OrderedDict
from typing import List

from ovos_number_parser.util import (convert_to_mixed_fraction, look_for_fractions,
                                     is_numeric, tokenize, Token)

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
    17: 'diecisiete',
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
    (100, 'cien'),
    (1000, 'mil'),
    (1000000, 'millones'),
    (1e9, "millardos"),
    (1e12, "billones"),
    (1e18, 'trillones'),
    (1e24, "cuatrillones"),
    (1e30, "quintillones"),
    (1e36, "sextillones"),
    (1e42, "septillones"),
    (1e48, "octillones"),
    (1e54, "nonillones"),
    (1e60, "decillones"),
    (1e66, "undecillones"),
    (1e72, "duodecillones"),
    (1e78, "tredecillones"),
    (1e84, "cuatrodecillones"),
    (1e90, "quindecillones"),
    (1e96, "sexdecillones"),
    (1e102, "septendecillones"),
    (1e108, "octodecillones"),
    (1e114, "novendecillones"),
    (1e120, "vigintillones"),
    (1e306, "unquinquagintillones"),
    (1e312, "duoquinquagintillones"),
    (1e336, "sexquinquagintillones"),
    (1e366, "unsexagintillones")
])

_SHORT_SCALE_ES = OrderedDict([
    (100, 'cien'),
    (1000, 'mil'),
    (1000000, 'millones'),
    (1e9, "billones"),
    (1e12, 'trillones'),
    (1e15, "cuatrillones"),
    (1e18, "quintillones"),
    (1e21, "sextillones"),
    (1e24, "septillones"),
    (1e27, "octillones"),
    (1e30, "nonillones"),
    (1e33, "decillones"),
    (1e36, "undecillones"),
    (1e39, "duodecillones"),
    (1e42, "tredecillones"),
    (1e45, "cuatrodecillones"),
    (1e48, "quindecillones"),
    (1e51, "sexdecillones"),
    (1e54, "septendecillones"),
    (1e57, "octodecillones"),
    (1e60, "novendecillones"),
    (1e63, "vigintillones"),
    (1e66, "unvigintillones"),
    (1e69, "uuovigintillones"),
    (1e72, "tresvigintillones"),
    (1e75, "quattuorvigintillones"),
    (1e78, "quinquavigintillones"),
    (1e81, "qesvigintillones"),
    (1e84, "septemvigintillones"),
    (1e87, "octovigintillones"),
    (1e90, "novemvigintillones"),
    (1e93, "trigintillones"),
    (1e96, "untrigintillones"),
    (1e99, "duotrigintillones"),
    (1e102, "trestrigintillones"),
    (1e105, "quattuortrigintillones"),
    (1e108, "quinquatrigintillones"),
    (1e111, "sestrigintillones"),
    (1e114, "septentrigintillones"),
    (1e117, "octotrigintillones"),
    (1e120, "noventrigintillones"),
    (1e123, "quadragintillones"),
    (1e153, "quinquagintillones"),
    (1e183, "sexagintillones"),
    (1e213, "septuagintillones"),
    (1e243, "octogintillones"),
    (1e273, "nonagintillones"),
    (1e303, "centillones"),
    (1e306, "uncentillones"),
    (1e309, "duocentillones"),
    (1e312, "trescentillones"),
    (1e333, "decicentillones"),
    (1e336, "undecicentillones"),
    (1e363, "viginticentillones"),
    (1e366, "unviginticentillones"),
    (1e393, "trigintacentillones"),
    (1e423, "quadragintacentillones"),
    (1e453, "quinquagintacentillones"),
    (1e483, "sexagintacentillones"),
    (1e513, "septuagintacentillones"),
    (1e543, "octogintacentillones"),
    (1e573, "nonagintacentillones"),
    (1e603, "ducentillones"),
    (1e903, "trecentillones"),
    (1e1203, "quadringentillones"),
    (1e1503, "quingentillones"),
    (1e1803, "sexcentillones"),
    (1e2103, "septingentillones"),
    (1e2403, "octingentillones"),
    (1e2703, "nongentillones"),
    (1e3003, "millinillones")
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


def pronounce_number_es(number, places=2, short_scale=False):
    """
    Convert a number to it's spoken equivalent

    For example, '5.2' would return 'cinco coma dos'

    Args:
        num(float or int): the number to pronounce 
        places(int): maximum decimal places to speak
    Returns:
        (str): The pronounced number
    """
    
    result = ""
    if number < 0:
        result = "menos "
    number = abs(number)

    number_names = _NUM_STRING_ES.copy()

    if short_scale:
        number_names.update(_SHORT_SCALE_ES)
    else:
        number_names.update(_LONG_SCALE_ES)      

    digits = [number_names[n] for n in range(0, 20)]

    tens = [number_names[n] for n in range(10, 100, 10)]

    if short_scale==True:
        hundreds = [_SHORT_SCALE_ES[n] for n in _SHORT_SCALE_ES.keys()]
    else:
        hundreds = [_LONG_SCALE_ES[n] for n in _LONG_SCALE_ES.keys()]
    
        
    
    if number in number_names: # check for a direct match 
        result += number_names[number]
    else:
        def _sub_thousand(n):
            assert 0 <= n <= 999
            if n <= 19:
                return digits[n]
            elif n <= 99:
                q, r = divmod(n, 10)
                _deci = tens[q - 1]
                _unit = r
                _partial = _deci
                if _unit > 0:
                    if q == 2:
                        _partial = _partial[:-1]
                        if r == 2:
                            _partial += "idós"
                        elif r == 3:
                            _partial += "itrés"
                        elif r == 6:
                            _partial += "iséis"
                        else:
                            _partial += "i" + number_names[_unit]
                    else:
                        _partial = _partial + " y " + number_names[_unit]
                return _partial
            else:
                q, r = divmod(n, 100)
                if q == 1:
                    _partial = "ciento"
                elif q == 5:
                    _partial = "quinientos"
                elif q == 7:
                    _partial = "setecientos"
                elif q == 9:
                    _partial = "novecientos"
                else:    
                    _partial = digits[q] + "cientos"
                _partial += (
                    " " + _sub_thousand(r) if r else "")  # separa centenars
        
                return _partial
            
        def _un_uno(number):
            if number[-9:] == "veintiuno":
                number = number.replace("veintiuno", "veintiún")
            elif number[-3:] == "uno":
                number = number[:-1]
            return number

        def _short_scale(n):
            if n >= max(_SHORT_SCALE_ES.keys()):
                return "número exageradamente grande"
            n = int(n)
            assert 0 <= n
            res = []
            for i, z in enumerate(_split_by(n, 1000)):
                if not z:
                    continue
                number = _sub_thousand(z)
                if i > 0: 
                    number = _un_uno(number)
                if i:
                    number += " "  # separa ordres de magnitud
                    number += hundreds[i]
                    if number == "un mil":
                        number = "mil"
                res.append(number)
            return " ".join(reversed(res))

        def _split_by(n, split=1000):
            assert 0 <= n
            res = []
            while n:
                n, r = divmod(n, split)
                res.append(r)
            return res

        def _long_scale(n):
            if n >= max(_LONG_SCALE_ES.keys()):
                return "número exageradamente grande"
            n = int(n)
            assert 0 <= n
            res = []
            for i, z in enumerate(_split_by(n, 1000000)):
                if not z:
                    continue
                number = pronounce_number_es(z, places, True)
                
                
                # strip off the comma after the thousand
                if i:
                    # plus one as we skip 'thousand'
                    # (and 'hundred', but this is excluded by index value)
                    number = number.replace(',', '')
                    number = _un_uno(number)
                    number += " " + hundreds[i + 1]
                res.append(number)
            return " ".join(reversed(res))

        if short_scale:
            result += _short_scale(number)
        else:
            result += _long_scale(number)

    big_nums = [_LONG_SCALE_ES[a] for a in _LONG_SCALE_ES]
    if result in big_nums:
        
        if result[-4:] == "rdos" or result[-4:] == "ones":
            result = "un " + result[:-1]

    if len(result.split(" ")) > 1 and result.split(" ")[0] in ["un", "uno"]:
        big_num = result.split(" ")[1]
        if big_num in big_nums:
            new_big_num = big_num
            if big_num[-4:] == "rdos":
                new_big_num = big_num[:-1]

            elif big_num[-4:] == "ones":
                new_big_num = big_num[:-4] + "ón"             
            result = result.replace(big_num, new_big_num)


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
    # TODO - above twenty it's ambiguous, "twenty one" is 2 words but only 1 number
    number_replacements = {
        "uno": "1", "dos": "2", "tres": "3", "cuatro": "4",
        "cinco": "5", "seis": "6", "siete": "7", "ocho": "8", "nueve": "9",
        "diez": "10", "once": "11", "doce": "12", "trece": "13", "catorce": "14",
        "quince": "15", "dieciséis": "16", "diecisiete": "17", "dieciocho": "18",
        "diecinueve": "19", "veinte": "20"
        # Extend this dictionary for higher numbers as needed
    }
    words: List[Token] = tokenize(utterance)
    for idx, tok in enumerate(words):
        if tok.word in number_replacements:
            words[idx] = number_replacements[tok.word]
        else:
            words[idx] = tok.word
    return " ".join(words)
