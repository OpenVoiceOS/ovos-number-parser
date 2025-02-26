from typing import List

from ovos_number_parser.util import (convert_to_mixed_fraction, look_for_fractions,
                                     is_numeric, tokenize, Token)

_NUMBERS_CA = {
    "zero": 0,
    "u": 1,
    "un": 1,
    "una": 1,
    "uns": 1,
    "unes": 1,
    "primer": 1,
    "primera": 1,
    "segon": 2,
    "segona": 2,
    "tercer": 3,
    "tercera": 3,
    "dos": 2,
    "dues": 2,
    "tres": 3,
    "quatre": 4,
    "cinc": 5,
    "sis": 6,
    "set": 7,
    "vuit": 8,
    "huit": 8,
    "nou": 9,
    "deu": 10,
    "onze": 11,
    "dotze": 12,
    "tretze": 13,
    "catorze": 14,
    "quinze": 15,
    "setze": 16,
    "disset": 17,
    "divuit": 18,
    "dinou": 19,
    "vint": 20,
    "trenta": 30,
    "quaranta": 40,
    "cinquanta": 50,
    "seixanta": 60,
    "setanta": 70,
    "vuitanta": 80,
    "noranta": 90,
    "cent": 100,
    "cents": 100,
    "dos-cents": 200,
    "dues-centes": 200,
    "tres-cents": 300,
    "tres-centes": 300,
    "quatre-cents": 400,
    "quatre-centes": 400,
    "cinc-cents": 500,
    "cinc-centes": 500,
    "sis-cents": 600,
    "sis-centes": 600,
    "set--cents": 700,
    "set-centes": 700,
    "vuit-cents": 800,
    "vuit-centes": 800,
    "nou-cents": 900,
    "nou-centes": 900,
    "mil": 1000,
    "milió": 1000000
}

_FRACTION_STRING_CA = {
    2: 'mig',
    3: 'terç',
    4: 'quart',
    5: 'cinquè',
    6: 'sisè',
    7: 'setè',
    8: 'vuitè',
    9: 'novè',
    10: 'desè',
    11: 'onzè',
    12: 'dotzè',
    13: 'tretzè',
    14: 'catorzè',
    15: 'quinzè',
    16: 'setzè',
    17: 'dissetè',
    18: 'divuitè',
    19: 'dinovè',
    20: 'vintè',
    30: 'trentè',
    100: 'centè',
    1000: 'milè'
}

_NUM_STRING_CA = {
    0: 'zero',
    1: 'un',
    2: 'dos',
    3: 'tres',
    4: 'quatre',
    5: 'cinc',
    6: 'sis',
    7: 'set',
    8: 'vuit',
    9: 'nou',
    10: 'deu',
    11: 'onze',
    12: 'dotze',
    13: 'tretze',
    14: 'catorze',
    15: 'quinze',
    16: 'setze',
    17: 'disset',
    18: 'divuit',
    19: 'dinou',
    20: 'vint',
    30: 'trenta',
    40: 'quaranta',
    50: 'cinquanta',
    60: 'seixanta',
    70: 'setanta',
    80: 'vuitanta',
    90: 'noranta'
}

_TENS_CA = {
    "vint": 20,
    "trenta": 30,
    "quaranta": 40,
    "cinquanta": 50,
    "seixanta": 60,
    "setanta": 70,
    "vuitanta": 80,
    "huitanta": 80,
    "noranta": 90
}

_AFTER_TENS_CA = {
    "u": 1,
    "un": 1,
    "dos": 2,
    "dues": 2,
    "tres": 3,
    "quatre": 4,
    "cinc": 5,
    "sis": 6,
    "set": 7,
    "vuit": 8,
    "huit": 8,
    "nou": 9
}

_BEFORE_HUNDREDS_CA = {
    "dos": 2,
    "dues": 2,
    "tres": 3,
    "quatre": 4,
    "cinc": 5,
    "sis": 6,
    "set": 7,
    "vuit": 8,
    "huit": 8,
    "nou": 9,
}

_HUNDREDS_CA = {
    "cent": 100,
    "cents": 100,
    "centes": 100
}


def nice_number_ca(number, speech, denominators=range(1, 21)):
    """ Catalan helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 i mig" for speech and "4 1/2" for text

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
        return str(round(number, 3))

    whole, num, den = result

    if not speech:
        if num == 0:
            # TODO: Number grouping?  E.g. "1,000,000"
            return str(whole)
        else:
            return '{} {}/{}'.format(whole, num, den)

    if num == 0:
        return str(whole)
    # denominador
    den_str = _FRACTION_STRING_CA[den]
    # fraccions
    if whole == 0:
        if num == 1:
            # un desè
            return_string = 'un {}'.format(den_str)
        else:
            # tres mig
            return_string = '{} {}'.format(num, den_str)
    # inteiros >10
    elif num == 1:
        # trenta-un
        return_string = '{}-{}'.format(whole, den_str)
    # inteiros >10 com fracções
    else:
        # vint i 3 desens
        return_string = '{} i {} {}'.format(whole, num, den_str)
    # plural
    if num > 1:
        return_string += 's'
    return return_string


def pronounce_number_ca(number, places=2):
    """
    Convert a number to it's spoken equivalent
     For example, '5.2' would return 'cinc coma dos'
     Args:
        number(float or int): the number to pronounce (under 100)
        places(int): maximum decimal places to speak
    Returns:
        (str): The pronounced number
    """
    if abs(number) >= 100:
        # TODO: Support n > 100
        return str(number)

    result = ""
    if number < 0:
        result = "menys "
    number = abs(number)

    if number >= 20:
        tens = int(number - int(number) % 10)
        ones = int(number - tens)
        result += _NUM_STRING_CA[tens]
        if ones > 0:
            if tens == 20:
                result += "-i-" + _NUM_STRING_CA[ones]
            else:
                result += "-" + _NUM_STRING_CA[ones]
    else:
        result += _NUM_STRING_CA[int(number)]

    # Deal with decimal part, in Catalan is commonly used the comma
    # instead the dot. Decimal part can be written both with comma
    # and dot, but when pronounced, its pronounced "coma"
    if not number == int(number) and places > 0:
        if abs(number) < 1.0 and (result == "menys " or not result):
            result += "zero"
        result += " coma"
        _num_str = str(number)
        _num_str = _num_str.split(".")[1][0:places]
        for char in _num_str:
            result += " " + _NUM_STRING_CA[int(char)]
    return result


def is_fractional_ca(input_str, short_scale=True):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): use short scale if True, long scale if False
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    if input_str.endswith('é', -1):
        input_str = input_str[:len(input_str) - 1] + "è"  # e.g. "cinqué -> cinquè"
    elif input_str.endswith('ena', -3):
        input_str = input_str[:len(input_str) - 3] + "è"  # e.g. "cinquena -> cinquè"
    elif input_str.endswith('ens', -3):
        input_str = input_str[:len(input_str) - 3] + "è"  # e.g. "cinquens -> cinquè"
    elif input_str.endswith('enes', -4):
        input_str = input_str[:len(input_str) - 4] + "è"  # e.g. "cinquenes -> cinquè"
    elif input_str.endswith('os', -2):
        input_str = input_str[:len(input_str) - 2]  # e.g. "terços -> terç"
    elif (input_str == 'terceres' or input_str == 'tercera'):
        input_str = "terç"  # e.g. "tercer -> terç"
    elif (input_str == 'mitges' or input_str == 'mitja'):
        input_str = "mig"  # e.g. "mitges -> mig"
    elif (input_str == 'meitat' or input_str == 'meitats'):
        input_str = "mig"  # e.g. "mitges -> mig"
    elif input_str.endswith('a', -1):
        input_str = input_str[:len(input_str) - 1]  # e.g. "quarta -> quart"
    elif input_str.endswith('es', -2):
        input_str = input_str[:len(input_str) - 2]  # e.g. "quartes -> quartes"
    elif input_str.endswith('s', -1):
        input_str = input_str[:len(input_str) - 1]  # e.g. "quarts -> quart"

    aFrac = ["mig", "terç", "quart", "cinquè", "sisè", "sètè", "vuitè", "novè",
             "desè", "onzè", "dotzè", "tretzè", "catorzè", "quinzè", "setzè",
             "dissetè", "divuitè", "dinovè"]

    if input_str.lower() in aFrac:
        return 1.0 / (aFrac.index(input_str) + 2)
    if input_str == "vintè":
        return 1.0 / 20
    if input_str == "trentè":
        return 1.0 / 30
    if input_str == "centè":
        return 1.0 / 100
    if input_str == "milè":
        return 1.0 / 1000
    if (input_str == "vuitè" or input_str == "huitè"):
        return 1.0 / 8
    if (input_str == "divuitè" or input_str == "dihuitè"):
        return 1.0 / 18

    return False


def extract_number_ca(text, short_scale=True, ordinals=False):
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
    text = text.lower()
    aWords = text.split()
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
        if word in _NUMBERS_CA:
            val = _NUMBERS_CA[word]
        elif '-' in word:
            wordparts = word.split('-')
            # trenta-cinc > 35
            if len(wordparts) == 2 and (wordparts[0] in _TENS_CA and wordparts[1] in _AFTER_TENS_CA):
                val = _TENS_CA[wordparts[0]] + _AFTER_TENS_CA[wordparts[1]]
            # vint-i-dues > 22
            elif len(wordparts) == 3 and wordparts[1] == 'i' and (
                    wordparts[0] in _TENS_CA and wordparts[2] in _AFTER_TENS_CA):
                val = _TENS_CA[wordparts[0]] + _AFTER_TENS_CA[wordparts[2]]
            # quatre-centes > 400
            elif len(wordparts) == 2 and (wordparts[0] in _BEFORE_HUNDREDS_CA and wordparts[1] in _HUNDREDS_CA):
                val = _BEFORE_HUNDREDS_CA[wordparts[0]] * 100

        elif word.isdigit():  # doesn't work with decimals
            val = int(word)
        elif is_numeric(word):
            val = float(word)
        elif is_fractional_ca(word):
            if not result:
                result = 1
            result = result * is_fractional_ca(word)
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
            # TODO: caution, review use of "ens" word
            if next_word != "ens":
                result += val
            else:
                result = float(result) / float(val)

        if next_word is None:
            break

        # number word and fraction
        ands = ["i"]
        if next_word in ands:
            zeros = 0
            if result is None:
                count += 1
                continue
            newWords = aWords[count + 2:]
            newText = ""
            for word in newWords:
                newText += word + " "

            afterAndVal = extract_number_ca(newText[:-1])
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
                afterAndVal = extract_number_ca(newText[:-1])
                if afterAndVal:
                    if result is None:
                        result = 0
                    result += afterAndVal
                    break

        decimals = ["coma", "amb", "punt", ".", ","]
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
            afterDotVal = str(extract_number_ca(newText[:-1]))
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


def numbers_to_digits_ca(utterance: str) -> str:
    """
    Substitueix els números escrits en un text en català per les seves equivalents en xifres.

    Args:
        utterance (str): Cadena d'entrada que possiblement conté números escrits.

    Returns:
        str: Text amb els números escrits substituïts per xifres.
    """
    # TODO - above twenty it's ambiguous, "twenty one" is 2 words but only 1 number
    number_replacements = {
        "un": "1", "dos": "2", "tres": "3", "quatre": "4",
        "cinc": "5", "sis": "6", "set": "7", "vuit": "8", "nou": "9",
        "deu": "10", "onze": "11", "dotze": "12", "tretze": "13", "catorze": "14",
        "quinze": "15", "setze": "16", "disset": "17", "divuit": "18",
        "dinou": "19", "vint": "20"
        # Amplieu aquest diccionari per a números més alts si és necessari
    }
    words: List[Token] = tokenize(utterance)
    for idx, tok in enumerate(words):
        if tok.word in number_replacements:
            words[idx] = number_replacements[tok.word]
        else:
            words[idx] = tok.word
    return " ".join(words)
