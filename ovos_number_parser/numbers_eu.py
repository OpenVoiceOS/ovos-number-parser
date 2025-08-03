from ovos_number_parser.util import (convert_to_mixed_fraction, look_for_fractions,
                                     is_numeric)

_NUM_STRING_EU = {
    "zero": 0,
    "bat": 1,
    "bi": 2,
    "hiru": 3,
    "lau": 4,
    "bost": 5,
    "sei": 6,
    "zazpi": 7,
    "zortzi": 8,
    "bederatzi": 9,
    "hamar": 10,
    "hamaika": 11,
    "hamabi": 12,
    "hamahiru": 13,
    "hamalau": 14,
    "hamabost": 15,
    "hamasei": 16,
    "hamazazpi": 17,
    "hemezortzi": 18,
    "hemeretzi": 19,
    "hogei": 20,
    "hogeita hamar": 30,
    "hogeita hamaika": 31,
    "berrogei": 40,
    "berrogeita hamar": 50,
    "hirurogei": 60,
    "hirurogeita hamar": 70,
    "laurogei": 80,
    "laurogeita hamar": 90,
    "ehun": 100,
    "berrehun": 200,
    "hirurehun": 300,
    "laurehun": 400,
    "bostehun": 500,
    "seirehun": 600,
    "zazpirehun": 700,
    "zortzirehun": 800,
    "bederatzirehun": 900,
    "mila": 1000}

NUM_STRING_EU = {
    0: 'zero',
    1: 'bat',
    2: 'bi',
    3: 'hiru',
    4: 'lau',
    5: 'bost',
    6: 'sei',
    7: 'zazpi',
    8: 'zortzi',
    9: 'bederatzi',
    10: 'hamar',
    11: 'hamaika',
    12: 'hamabi',
    13: 'hamahiru',
    14: 'hamalau',
    15: 'hamabost',
    16: 'hamasei',
    17: 'hamazazpi',
    18: 'hemezortzi',
    19: 'hemeretzi',
    20: 'hogei',
    30: 'hogeita hamar',
    40: 'berrogei',
    50: 'berrogeita hamar',
    60: 'hirurogei',
    70: 'hirurogehita hamar',
    80: 'laurogei',
    90: 'laurogeita hamar',
    100: 'ehun',
    200: 'berrehun',
    300: 'hirurehun',
    400: 'laurehun',
    500: 'bostehun',
    600: 'seirehun',
    700: 'zazpirehun',
    800: 'zortzirehun',
    900: 'bederatzirehun',
    1000: 'mila'
}

FRACTION_STRING_EU = {
    2: 'erdi',
    3: 'heren',
    4: 'laurden',
    5: 'bosten',
    6: 'seiren',
    7: 'zazpiren',
    8: 'zortziren',
    9: 'bederatziren',
    10: 'hamarren',
    11: 'hamaikaren',
    12: 'hamabiren',
    13: 'hamahiruren',
    14: 'hamalauren',
    15: 'hamabosten',
    16: 'hamaseiren',
    17: 'hamazazpiren',
    18: 'hemezortziren',
    19: 'hemeretziren',
    20: 'hogeiren'
}


def nice_number_eu(number, speech=True, denominators=range(1, 21)):
    """ Euskara helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 eta erdi" for speech and "4 1/2" for text

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
        den_str = FRACTION_STRING_EU[den]
        # if it is not an integer
        if whole == 0:
            # if there is no whole number
            if num == 1:
                # if numerator is 1, return "un medio", for example
                strNumber = '{} bat'.format(den_str)
            else:
                # else return "cuatro tercios", for example
                strNumber = '{} {}'.format(num, den_str)
        elif num == 1:
            # if there is a whole number and numerator is 1
            if den == 2:
                # if denominator is 2, return "1 y medio", for example
                strNumber = '{} eta {}'.format(whole, den_str)
            else:
                # else return "1 y 1 tercio", for example
                strNumber = '{} eta {} bat'.format(whole, den_str)
        else:
            # else return "2 y 3 cuarto", for example
            strNumber = '{} eta {} {}'.format(whole, num, den_str)

    return strNumber


def pronounce_number_eu(num, places=2):
    """
    Convert a number to it's spoken equivalent

    For example, '5.2' would return 'bost koma bi'

    Args:
        num(float or int): the number to pronounce (under 100)
        places(int): maximum decimal places to speak
    Returns:
        (str): The pronounced number
    """
    if abs(num) >= 10000:
        # TODO: Soporta a números por encima de 1000
        return str(num)

    result = ""
    if num < 0:
        result = "minus "
    num = abs(num)

    thousands = int(num - int(num) % 1000)
    _num = num - thousands
    hundreds = int(_num - int(_num) % 100)
    _num = _num - hundreds
    tens = int(_num - _num % 10)
    ones = int(_num - tens)

    if thousands > 0:
        if thousands > 1000:
            result += NUM_STRING_EU[int(thousands / 1000)] + ' '
        result += NUM_STRING_EU[1000]
        if hundreds > 0 and tens == 0 and ones == 0:
            result += ' eta '
        elif hundreds > 0 or tens > 0 or ones > 0:
            result += ' '
    if hundreds > 0:
        result += NUM_STRING_EU[hundreds]
        if tens > 0 or ones > 0:
            result += ' eta '
    if tens or ones:
        if tens == 0 or tens == 10 or ones == 0:
            result += NUM_STRING_EU[int(_num)]
        else:
            if (tens % 20) == 10:
                ones = ones + 10
            result += NUM_STRING_EU[int(tens)].split(' ')[0].replace("ta", "") + str("ta ") + NUM_STRING_EU[int(ones)]
    if abs(num) < 1.0:
        result += NUM_STRING_EU[0]
    # Deal with decimal part, in basque is commonly used the comma
    # instead the dot. Decimal part can be written both with comma
    # and dot, but when pronounced, its pronounced "koma"
    if not num == int(num) and places > 0:
        if abs(num) < 1.0 and (result == "minus " or not result):
            result += NUM_STRING_EU[0]
        result += " koma"
        _num_str = str(num)
        _num_str = _num_str.split(".")[1][0:places]
        for char in _num_str:
            result += " " + NUM_STRING_EU[int(char)]

    return result


def is_fractional_eu(input_str):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        text (str): the string to check if fractional
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    if input_str.endswith('s', -1):
        input_str = input_str[:len(input_str) - 1]  # e.g. "fifths"

    aFrac = {"erdia": 2, "erdi": 2, "heren": 3, "laurden": 4,
             "laurdena": 4, "bosten": 5, "bostena": 5, "seiren": 6, "seirena": 6,
             "zazpiren": 7, "zapirena": 7, "zortziren": 8, "zortzirena": 8,
             "bederatziren": 9, "bederatzirena": 9, "hamarren": 10, "hamarrena": 10,
             "hamaikaren": 11, "hamaikarena": 11, "hamabiren": 12, "hamabirena": 12}

    if input_str.lower() in aFrac:
        return 1.0 / aFrac[input_str]
    if (input_str == "hogeiren" or input_str == "hogeirena"):
        return 1.0 / 20
    if (input_str == "hogeita hamarren" or input_str == "hogeita hamarrena"):
        return 1.0 / 30
    if (input_str == "ehunen" or input_str == "ehunena"):
        return 1.0 / 100
    if (input_str == "milaren" or input_str == "milarena"):
        return 1.0 / 1000
    return False


# TODO: short_scale and ordinals don't do anything here.
# The parameters are present in the function signature for API compatibility
# reasons.
#
# Returns incorrect output on certain fractional phrases like, "cuarto de dos"
def extract_number_eu(text, short_scale=True, ordinals=False):
    """
    This function prepares the given text for parsing by making
    numbers consistent, getting rid of contractions, etc.
    Args:
        text (str): the string to normalize
    Returns:
        (int) or (float): The value of extracted number

    """
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
        if word in _NUM_STRING_EU:
            val = _NUM_STRING_EU[word]
        elif word.isdigit():  # doesn't work with decimals
            val = int(word)
        elif is_numeric(word):
            val = float(word)
        elif is_fractional_eu(word):
            if next_word in _NUM_STRING_EU:
                # erdi bat, heren bat, etab
                result = _NUM_STRING_EU[next_word]
                # hurrengo hitza (bat, bi, ...) salto egin
                next_word = None
                count += 2
            elif not result:
                result = 1
                count += 1
            result = result * is_fractional_eu(word)
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
            if next_word == "en" or next_word == "ren":
                result = float(result) / float(val)
            else:
                result = val

        if next_word is None:
            break

        # number word and fraction
        ands = ["eta"]
        if next_word in ands:
            zeros = 0
            if result is None:
                count += 1
                continue
            newWords = aWords[count + 2:]
            newText = ""
            for word in newWords:
                newText += word + " "

            afterAndVal = extract_number_eu(newText[:-1])
            if afterAndVal:
                if result < afterAndVal or result < 20:
                    while afterAndVal > 1:
                        afterAndVal = afterAndVal / 10.0
                    for word in newWords:
                        if word == "zero" or word == "0":
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
                afterAndVal = extract_number_eu(newText[:-1])
                if afterAndVal:
                    if result is None:
                        result = 0
                    result += afterAndVal
                    break

        decimals = ["puntu", "koma", ".", ","]
        if next_word in decimals:
            zeros = 0
            newWords = aWords[count + 2:]
            newText = ""
            for word in newWords:
                newText += word + " "
            for word in newWords:
                if word == "zero" or word == "0":
                    zeros += 1
                else:
                    break
            afterDotVal = str(extract_number_eu(newText[:-1]))
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


# TODO Not parsing 'cero'
def eu_number_parse(words, i):
    def eu_cte(i, s):
        if i < len(words) and s == words[i]:
            return s, i + 1
        return None

    def eu_number_word(i, mi, ma):
        if i < len(words):
            v = _NUM_STRING_EU.get(words[i])
            if v and v >= mi and v <= ma:
                return v, i + 1
        return None

    def eu_number_1_99(i):
        if i >= len(words):
            return None
        r1 = eu_number_word(i, 1, 29)
        if r1:
            return r1

        composed = False
        if words[i] != "eta" and words[i][-2:] == "ta":
            composed = True
            words[i] = words[i][:-2]

        r1 = eu_number_word(i, 20, 90)

        if r1:
            v1, i1 = r1

            if composed:
                # i2 = r2[1]
                r3 = eu_number_word(i1, 1, 19)
                if r3:
                    v3, i3 = r3
                    return v1 + v3, i3
            return r1
        return None

    def eu_number_1_999(i):
        r1 = eu_number_word(i, 100, 900)
        if r1:
            v1, i1 = r1
            r2 = eu_cte(i1, "eta")
            if r2:
                i2 = r2[1]
                r3 = eu_number_1_99(i2)
                if r3:
                    v3, i3 = r3
                    return v1 + v3, i3
            else:
                return r1

        # [1-99]
        r1 = eu_number_1_99(i)
        if r1:
            return r1

        return None

    def eu_number(i):
        # check for cero
        r1 = eu_number_word(i, 0, 0)
        if r1:
            return r1

        # check for [1-999] (mil [0-999])?
        r1 = eu_number_1_999(i)
        if r1:
            v1, i1 = r1
            r2 = eu_cte(i1, "mila")
            if r2:
                i2 = r2[1]
                r3 = eu_number_1_999(i2)
                if r3:
                    v3, i3 = r3
                    return v1 * 1000 + v3, i3
                else:
                    return v1 * 1000, i2
            else:
                return r1
        return None

    return eu_number(i)
