from math import floor

from ovos_number_parser.util import (convert_to_mixed_fraction, look_for_fractions, is_numeric)

_DA_NUMBERS = {
    'nul': 0,
    'en': 1,
    'et': 1,
    'to': 2,
    'tre': 3,
    'fire': 4,
    'fem': 5,
    'seks': 6,
    'syv': 7,
    'otte': 8,
    'ni': 9,
    'ti': 10,
    'elve': 11,
    'tolv': 12,
    'tretten': 13,
    'fjorten': 14,
    'femten': 15,
    'seksten': 16,
    'sytten': 17,
    'atten': 18,
    'nitten': 19,
    'tyve': 20,
    'enogtyve': 21,
    'toogtyve': 22,
    'treogtyve': 23,
    'fireogtyve': 24,
    'femogtyve': 25,
    'seksogtyve': 26,
    'syvogtyve': 27,
    'otteogtyve': 28,
    'niogtyve': 29,
    'tredive': 30,
    'enogtredive': 31,
    'fyrrre': 40,
    'halvtres': 50,
    'tres': 60,
    'halvfjers': 70,
    'firs': 80,
    'halvfems': 90,
    'hunderede': 100,
    'tohundrede': 200,
    'trehundrede': 300,
    'firehundrede': 400,
    'femhundrede': 500,
    'sekshundrede': 600,
    'syvhundrede': 700,
    'ottehundrede': 800,
    'nihundrede': 900,
    'tusinde': 1000,
    'million': 1000000
}

_MONTHS_DA = ['januar', 'februar', 'märz', 'april', 'mai', 'juni',
              'juli', 'august', 'september', 'oktober', 'november',
              'dezember']

_NUM_STRING_DA = {
    0: 'nul',
    1: 'en',
    2: 'to',
    3: 'tre',
    4: 'fire',
    5: 'fem',
    6: 'seks',
    7: 'syv',
    8: 'otte',
    9: 'ni',
    10: 'ti',
    11: 'elve',
    12: 'tolv',
    13: 'tretten',
    14: 'fjorten',
    15: 'femten',
    16: 'seksten',
    17: 'sytten',
    18: 'atten',
    19: 'nitten',
    20: 'tyve',
    30: 'tredive',
    40: 'fyrre',
    50: 'halvtres',
    60: 'tres',
    70: 'halvfjers',
    80: 'firs',
    90: 'halvfems',
    100: 'hundrede'
}

_NUM_POWERS_OF_TEN = [
    'hundred',
    'tusind',
    'million',
    'milliard',
    'billion',
    'billiard',
    'trillion',
    'trilliard'
]

_FRACTION_STRING_DA = {
    2: 'halv',
    3: 'trediedel',
    4: 'fjerdedel',
    5: 'femtedel',
    6: 'sjettedel',
    7: 'syvendedel',
    8: 'ottendedel',
    9: 'niendedel',
    10: 'tiendedel',
    11: 'elftedel',
    12: 'tolvtedel',
    13: 'trettendedel',
    14: 'fjortendedel',
    15: 'femtendedel',
    16: 'sejstendedel',
    17: 'syttendedel',
    18: 'attendedel',
    19: 'nittendedel',
    20: 'tyvendedel'
}

# Numbers below 1 million are written in one word in Danish, yielding very
# long words
# In some circumstances it may better to seperate individual words
# Set _EXTRA_SPACE_DA=" " for separating numbers below 1 million (
# orthographically incorrect)
# Set _EXTRA_SPACE_DA="" for correct spelling, this is standard

# _EXTRA_SPACE_DA = " "
_EXTRA_SPACE_DA = ""


def extract_number_da(text, short_scale=True, ordinals=False):
    """
    This function prepares the given text for parsing by making
    numbers consistent, getting rid of contractions, etc.
    Args:
        text (str): the string to normalize
    Returns:
        (int) or (float): The value of extracted number


    undefined articles cannot be suppressed in German:
    'ein Pferd' means 'one horse' and 'a horse'

    """
    # TODO: short_scale and ordinals don't do anything here.
    # The parameters are present in the function signature for API compatibility
    # reasons.

    text = text.lower()
    aWords = text.split()
    aWords = [word for word in aWords if
              word not in ["den", "det"]]
    and_pass = False
    valPreAnd = False
    val = False
    count = 0
    while count < len(aWords):
        word = aWords[count]
        if is_numeric(word):
            if word.isdigit():  # doesn't work with decimals
                val = float(word)
        elif is_fractional_da(word):
            val = is_fractional_da(word)
        elif is_ordinal_da(word):
            val = is_ordinal_da(word)
        else:
            if word in _DA_NUMBERS:
                val = _DA_NUMBERS[word]
                if count < (len(aWords) - 1):
                    wordNext = aWords[count + 1]
                else:
                    wordNext = ""
                valNext = is_fractional_da(wordNext)

                if valNext:
                    val = val * valNext
                    aWords[count + 1] = ""

        if not val:
            # look for fractions like "2/3"
            aPieces = word.split('/')
            # if (len(aPieces) == 2 and is_numeric(aPieces[0])
            #   and is_numeric(aPieces[1])):
            if look_for_fractions(aPieces):
                val = float(aPieces[0]) / float(aPieces[1])
            elif and_pass:
                # added to value, quit here
                val = valPreAnd
                break
            else:
                count += 1
                continue

        aWords[count] = ""

        if and_pass:
            aWords[count - 1] = ''  # remove "og"
            val += valPreAnd
        elif count + 1 < len(aWords) and aWords[count + 1] == 'og':
            and_pass = True
            valPreAnd = val
            val = False
            count += 2
            continue
        elif count + 2 < len(aWords) and aWords[count + 2] == 'og':
            and_pass = True
            valPreAnd = val
            val = False
            count += 3
            continue

        break

    return val or False


def is_fractional_da(input_str, short_scale=True):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        input_str (str): the string to check if fractional
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    if input_str.lower().startswith("halv"):
        return 0.5

    if input_str.lower() == "trediedel":
        return 1.0 / 3
    elif input_str.endswith('del'):
        input_str = input_str[:len(input_str) - 3]  # e.g. "fünftel"
        if input_str.lower() in _DA_NUMBERS:
            return 1.0 / (_DA_NUMBERS[input_str.lower()])

    return False


def is_ordinal_da(input_str):
    """
    This function takes the given text and checks if it is an ordinal number.

    Args:
        input_str (str): the string to check if ordinal
    Returns:
        (bool) or (float): False if not an ordinal, otherwise the number
        corresponding to the ordinal

    ordinals for 1, 3, 7 and 8 are irregular

    only works for ordinals corresponding to the numbers in _DA_NUMBERS

    """

    lowerstr = input_str.lower()

    if lowerstr.startswith("første"):
        return 1
    if lowerstr.startswith("anden"):
        return 2
    if lowerstr.startswith("tredie"):
        return 3
    if lowerstr.startswith("fjerde"):
        return 4
    if lowerstr.startswith("femte"):
        return 5
    if lowerstr.startswith("sjette"):
        return 6
    if lowerstr.startswith("elfte"):
        return 1
    if lowerstr.startswith("tolvfte"):
        return 12

    if lowerstr[-3:] == "nde":
        # from 20 suffix is -ste*
        lowerstr = lowerstr[:-3]
        if lowerstr in _DA_NUMBERS:
            return _DA_NUMBERS[lowerstr]

    if lowerstr[-4:] in ["ende"]:
        lowerstr = lowerstr[:-4]
        if lowerstr in _DA_NUMBERS:
            return _DA_NUMBERS[lowerstr]

    if lowerstr[-2:] == "te":  # below 20 suffix is -te*
        lowerstr = lowerstr[:-2]
        if lowerstr in _DA_NUMBERS:
            return _DA_NUMBERS[lowerstr]

    return False


def nice_number_da(number, speech=True, denominators=range(1, 21)):
    """ Danish helper for nice_number
    This function formats a float to human understandable functions. Like
    4.5 becomes "4 einhalb" for speech and "4 1/2" for text
    Args:
        number (int or float): the float to format
        speech (bool): format for speech (True) or display (False)
        denominators (iter of ints): denominators to use, default [1 .. 20]
    Returns:
        (str): The formatted string.
    """
    result = convert_to_mixed_fraction(number, denominators)
    if not result:
        # Give up, just represent as a 3 decimal number
        return str(round(number, 3)).replace(".", ",")
    whole, num, den = result
    if not speech:
        if num == 0:
            # TODO: Number grouping?  E.g. "1,000,000"
            return str(whole)
        else:
            return '{} {}/{}'.format(whole, num, den)
    if num == 0:
        return str(whole)
    den_str = _FRACTION_STRING_DA[den]
    if whole == 0:
        if num == 1:
            return_string = '{} {}'.format(num, den_str)
        else:
            return_string = '{} {}e'.format(num, den_str)
    else:
        if num == 1:
            return_string = '{} og {} {}'.format(whole, num, den_str)
        else:
            return_string = '{} og {} {}e'.format(whole, num, den_str)

    return return_string


def pronounce_number_da(number, places=2, short_scale=True, scientific=False,
                        ordinals=False):
    """
    Convert a number to it's spoken equivalent

    For example, '5.2' would return 'five point two'

    Args:
        number(float or int): the number to pronounce (under 100)
        places(int): maximum decimal places to speak
        short_scale (bool) : use short (True) or long scale (False)
            https://en.wikipedia.org/wiki/Names_of_large_numbers
        scientific (bool): pronounce in scientific notation
        ordinals (bool): pronounce in ordinal form "first" instead of "one"
    Returns:
        (str): The pronounced number
    """

    # TODO short_scale, scientific and ordinals
    # currently ignored

    def pronounce_triplet_da(num):
        result = ""
        num = floor(num)
        if num > 99:
            hundreds = floor(num / 100)
            if hundreds > 0:
                if hundreds == 1:
                    result += 'et' + 'hundrede' + _EXTRA_SPACE_DA
                else:
                    result += _NUM_STRING_DA[hundreds] + \
                              'hundrede' + _EXTRA_SPACE_DA
                    num -= hundreds * 100
        if num == 0:
            result += ''  # do nothing
        elif num == 1:
            result += 'et'
        elif num <= 20:
            result += _NUM_STRING_DA[num] + _EXTRA_SPACE_DA
        elif num > 20:
            ones = num % 10
            tens = num - ones
            if ones > 0:
                result += _NUM_STRING_DA[ones] + _EXTRA_SPACE_DA
                if tens > 0:
                    result += 'og' + _EXTRA_SPACE_DA
            if tens > 0:
                result += _NUM_STRING_DA[tens] + _EXTRA_SPACE_DA

        return result

    def pronounce_fractional_da(num, places):
        # fixed number of places even with trailing zeros
        result = ""
        place = 10
        while places > 0:
            # doesn't work with 1.0001 and places = 2: int(
            # number*place) % 10 > 0 and places > 0:
            result += " " + _NUM_STRING_DA[int(num * place) % 10]
            place *= 10
            places -= 1
        return result

    def pronounce_whole_number_da(num, scale_level=0):
        if num == 0:
            return ''

        num = floor(num)
        result = ''
        last_triplet = num % 1000

        if last_triplet == 1:
            if scale_level == 0:
                if result != '':
                    result += '' + 'et'
                else:
                    result += "en"
            elif scale_level == 1:
                result += 'et' + _EXTRA_SPACE_DA + 'tusinde' + _EXTRA_SPACE_DA
            else:
                result += "en " + _NUM_POWERS_OF_TEN[scale_level] + ' '
        elif last_triplet > 1:
            result += pronounce_triplet_da(last_triplet)
            if scale_level == 1:
                result += 'tusinde' + _EXTRA_SPACE_DA
            if scale_level >= 2:
                result += "og" + _NUM_POWERS_OF_TEN[scale_level]
            if scale_level >= 2:
                if scale_level % 2 == 0:
                    result += "er"  # MillionER
                result += "er "  # MilliardER, MillioneER

        num = floor(num / 1000)
        scale_level += 1
        return pronounce_whole_number_da(num,
                                         scale_level) + result + _EXTRA_SPACE_DA

    result = ""
    if abs(number) >= 1000000000000000000000000:  # cannot do more than this
        return str(number)
    elif number == 0:
        return str(_NUM_STRING_DA[0])
    elif number < 0:
        return "minus " + pronounce_number_da(abs(number), places)
    else:
        if number == int(number):
            return pronounce_whole_number_da(number)
        else:
            whole_number_part = floor(number)
            fractional_part = number - whole_number_part
            result += pronounce_whole_number_da(whole_number_part)
            if places > 0:
                result += " komma"
                result += pronounce_fractional_da(fractional_part, places)
            return result


def pronounce_ordinal_da(number):
    """
    This function pronounces a number as an ordinal

    1 -> first
    2 -> second

    Args:
        number (int): the number to format
    Returns:
        (str): The pronounced number string.
    """

    # ordinals for 1, 3, 7 and 8 are irregular
    # this produces the base form, it will have to be adapted for genus,
    # casus, numerus

    ordinals = ["nulte", "første", "anden", "tredie", "fjerde", "femte",
                "sjette", "syvende", "ottende", "niende", "tiende"]

    # only for whole positive numbers including zero
    if number < 0 or number != int(number):
        return number
    if number < 10:
        return ordinals[number]
    if number < 30:
        if pronounce_number_da(number)[-1:] == 'e':
            return pronounce_number_da(number) + "nde"
        else:
            return pronounce_number_da(number) + "ende"
    if number < 40:
        return pronounce_number_da(number) + "fte"
    else:
        if pronounce_number_da(number)[-1:] == 'e':
            return pronounce_number_da(number) + "nde"
        else:
            return pronounce_number_da(number) + "ende"
