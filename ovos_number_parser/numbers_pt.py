import re

from ovos_number_parser.util import convert_to_mixed_fraction, is_numeric, look_for_fractions

_NUMBERS_PT = {
    "zero": 0,
    "um": 1,
    "uma": 1,
    "uns": 1,
    "umas": 1,
    "primeiro": 1,
    "segundo": 2,
    "terceiro": 3,
    "dois": 2,
    "duas": 2,
    "tres": 3,
    "três": 3,
    "quatro": 4,
    "cinco": 5,
    "seis": 6,
    "sete": 7,
    "oito": 8,
    "nove": 9,
    "dez": 10,
    "onze": 11,
    "doze": 12,
    "treze": 13,
    "catorze": 14,
    "quinze": 15,
    "dezasseis": 16,
    "dezassete": 17,
    "dezoito": 18,
    "dezanove": 19,
    "vinte": 20,
    "trinta": 30,
    "quarenta": 40,
    "cinquenta": 50,
    "sessenta": 60,
    "setenta": 70,
    "oitenta": 80,
    "noventa": 90,
    "cem": 100,
    "cento": 100,
    "duzentos": 200,
    "duzentas": 200,
    "trezentos": 300,
    "trezentas": 300,
    "quatrocentos": 400,
    "quatrocentas": 400,
    "quinhentos": 500,
    "quinhentas": 500,
    "seiscentos": 600,
    "seiscentas": 600,
    "setecentos": 700,
    "setecentas": 700,
    "oitocentos": 800,
    "oitocentas": 800,
    "novecentos": 900,
    "novecentas": 900,
    "mil": 1000,
    "milhão": 1000000}

_FRACTION_STRING_PT = {
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
}

_NUM_STRING_PT = {
    0: 'zero',
    1: 'um',
    2: 'dois',
    3: 'três',
    4: 'quatro',
    5: 'cinco',
    6: 'seis',
    7: 'sete',
    8: 'oito',
    9: 'nove',
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
}


def nice_number_pt(number, speech, denominators=range(1, 21)):
    """ Portuguese helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 e meio" for speech and "4 1/2" for text

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
    den_str = _FRACTION_STRING_PT[den]
    # fracções
    if whole == 0:
        if num == 1:
            # um décimo
            return_string = 'um {}'.format(den_str)
        else:
            # três meio
            return_string = '{} {}'.format(num, den_str)
    # inteiros >10
    elif num == 1:
        # trinta e um
        return_string = '{} e {}'.format(whole, den_str)
    # inteiros >10 com fracções
    else:
        # vinte e 3 décimo
        return_string = '{} e {} {}'.format(whole, num, den_str)
    # plural
    if num > 1:
        return_string += 's'
    return return_string


def pronounce_number_pt(number, places=2):
    """
    Convert a number to it's spoken equivalent
     For example, '5.2' would return 'cinco virgula dois'
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
        result = "menos "
    number = abs(number)

    if number >= 20:
        tens = int(number - int(number) % 10)
        ones = int(number - tens)
        result += _NUM_STRING_PT[tens]
        if ones > 0:
            result += " e " + _NUM_STRING_PT[ones]
    else:
        result += _NUM_STRING_PT[int(number)]

    # Deal with decimal part, in portuguese is commonly used the comma
    # instead the dot. Decimal part can be written both with comma
    # and dot, but when pronounced, its pronounced "virgula"
    if not number == int(number) and places > 0:
        if abs(number) < 1.0 and (result == "menos " or not result):
            result += "zero"
        result += " vírgula"
        _num_str = str(number)
        _num_str = _num_str.split(".")[1][0:places]
        for char in _num_str:
            result += " " + _NUM_STRING_PT[int(char)]
    return result


def is_fractional_pt(input_str, short_scale=True):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): use short scale if True, long scale if False
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    if input_str.endswith('s', -1):
        input_str = input_str[:len(input_str) - 1]  # e.g. "fifths"

    aFrac = ["meio", "terço", "quarto", "quinto", "sexto",
             "setimo", "oitavo", "nono", "décimo"]

    if input_str.lower() in aFrac:
        return 1.0 / (aFrac.index(input_str) + 2)
    if input_str == "vigésimo":
        return 1.0 / 20
    if input_str == "trigésimo":
        return 1.0 / 30
    if input_str == "centésimo":
        return 1.0 / 100
    if input_str == "milésimo":
        return 1.0 / 1000
    if (input_str == "sétimo" or input_str == "septimo" or
            input_str == "séptimo"):
        return 1.0 / 7

    return False


def extract_number_pt(text, short_scale=True, ordinals=False):
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
        if word in _NUMBERS_PT:
            val = _NUMBERS_PT[word]
        elif word.isdigit():  # doesn't work with decimals
            val = int(word)
        elif is_numeric(word):
            val = float(word)
        elif is_fractional_pt(word):
            if not result:
                result = 1
            result = result * is_fractional_pt(word)
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
                result += val
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

            afterAndVal = extract_number_pt(newText[:-1])
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
                afterAndVal = extract_number_pt(newText[:-1])
                if afterAndVal:
                    if result is None:
                        result = 0
                    result += afterAndVal
                    break

        decimals = ["ponto", "virgula", "vírgula", ".", ","]
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
            afterDotVal = str(extract_number_pt(newText[:-1]))
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


def numbers_to_digits_pt(utterance: str) -> str:
    """
    Replace written numbers in text with their digit equivalents.

    Args:
        utterance (str): Input string possibly containing written numbers.

    Returns:
        str: Text with written numbers replaced by digits.
    """
    number_replacements = {
        "catorze": "14",
        "cem": "100",
        "cento": "100",
        "cinco": "5",
        "cinquenta": "50",
        "dez": "10",
        "dezanove": "19",
        "dezasseis": "16",
        "dezassete": "17",
        "dezoito": "18",
        "dois": "2",
        "doze": "12",
        "duas": "2",
        "duzentas": "200",
        "duzentos": "200",
        "mil": "1000",
        "milhão": "1000000",
        "nove": "9",
        "novecentas": "900",
        "novecentos": "900",
        "noventa": "90",
        "oitenta": "80",
        "oito": "8",
        "oitocentas": "800",
        "oitocentos": "800",
        "onze": "11",
        "primeiro": "1",
        "quarenta": "40",
        "quatro": "4",
        "quatrocentas": "400",
        "quatrocentos": "400",
        "quinhentas": "500",
        "quinhentos": "500",
        "quinze": "15",
        "segundo": "2",
        "seis": "6",
        "seiscentas": "600",
        "seiscentos": "600",
        "sessenta": "60",
        "sete": "7",
        "setecentas": "700",
        "setecentos": "700",
        "setenta": "70",
        "terceiro": "3",
        "tres": "3",
        "treze": "13",
        "trezentas": "300",
        "trezentos": "300",
        "trinta": "30",
        "três": "3",
        "um": "1",
        "uma": "1",
        "vinte": "20",
        "zero": "0"
    }
    words = tokenize(utterance)
    for idx, word in enumerate(words):
        if word in number_replacements:
            words[idx] = number_replacements[word]
    return " ".join(words)


def tokenize(utterance):
    # Split things like 12%
    utterance = re.sub(r"([0-9]+)([\%])", r"\1 \2", utterance)
    # Split things like #1
    utterance = re.sub(r"(\#)([0-9]+\b)", r"\1 \2", utterance)
    # Split things like amo-te
    utterance = re.sub(r"([a-zA-Z]+)(-)([a-zA-Z]+\b)", r"\1 \2 \3",
                       utterance)
    tokens = utterance.split()
    if tokens[-1] == '-':
        tokens = tokens[:-1]

    return tokens


def _pt_pruning(text, symbols=True, accents=True, agressive=True):
    # agressive pt word pruning
    words = ["a", "o", "os", "as", "de", "dos", "das",
             "lhe", "lhes", "me", "e", "no", "nas", "na", "nos", "em", "para",
             "este",
             "esta", "deste", "desta", "neste", "nesta", "nesse",
             "nessa", "foi", "que"]
    if symbols:
        symbols = [".", ",", ";", ":", "!", "?", "º", "ª"]
        for symbol in symbols:
            text = text.replace(symbol, "")
        text = text.replace("-", " ").replace("_", " ")
    if accents:
        accents = {"a": ["á", "à", "ã", "â"],
                   "e": ["ê", "è", "é"],
                   "i": ["í", "ì"],
                   "o": ["ò", "ó"],
                   "u": ["ú", "ù"],
                   "c": ["ç"]}
        for char in accents:
            for acc in accents[char]:
                text = text.replace(acc, char)
    if agressive:
        text_words = text.split(" ")
        for idx, word in enumerate(text_words):
            if word in words:
                text_words[idx] = ""
        text = " ".join(text_words)
        text = ' '.join(text.split())
    return text
