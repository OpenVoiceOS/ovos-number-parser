from math import floor

from ovos_number_parser.util import (invert_dict, convert_to_mixed_fraction, tokenize,
                                     ReplaceableNumber, Token, look_for_fractions)


_ARTICLES = {'en', 'et'}

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
    'fyrre': 40,
    'halvtres': 50,
    'tres': 60,
    'halvfjers': 70,
    'firs': 80,
    'halvfems': 90,
    'hunderede': 100,
    'ethunderede': 100,
    'tohundrede': 200,
    'trehundrede': 300,
    'firehundrede': 400,
    'femhundrede': 500,
    'sekshundrede': 600,
    'syvhundrede': 700,
    'ottehundrede': 800,
    'nihundrede': 900,
    'tusinde': 1000,
    'ettusinde': 1000,
    'totusinde': 2000,
    'tretusinde': 3000,
    'firetusinde': 4000,
    'femtusinde': 5000,
    'sekstusinde': 6000,
    'syvtusinde': 7000,
    'ottetusinde': 8000,
    'nitusinde': 9000,
    'titusinde': 10000,
    'million': 1000000
}

_MONTHS_DA = ['januar', 'februar', 'marts', 'april', 'maj', 'juni',
              'juli', 'august', 'september', 'oktober', 'november',
              'december']

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
    100: 'hundrede',
    200: 'tohundrede',
    300: 'trehundrede',
    400: 'firehundrede',
    500: 'femhundrede',
    600: 'sekshundrede',
    700: 'syvhundrede',
    800: 'ottehundrede',
    900: 'nihundrede',
    1000: 'tusinde',
    1000000: 'million'
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

_STRING_FRACTION_DA = invert_dict(_FRACTION_STRING_DA)
_STRING_FRACTION_DA.update({
    'halvdel': 2,
    'kvart': 4
})

_LONG_SCALE = {
    100: 'hundrede',
    1000: 'tusinde',
    1000000: 'million',
    1e9: "milliard",
    1e12: 'billion',
    1e15: "billiard",
    1e18: "trillion",
    1e21: "trilliard",
    1e24: "quadrillion",
    1e27: "quadrilliard"
}

_MULTIPLIER = set(_LONG_SCALE.values())

_STRING_LONG_SCALE = invert_dict(_LONG_SCALE)

# ending manipulation
for number, item in _LONG_SCALE.items():
    if int(number) > 1000:
        name = item + 'er'
        _MULTIPLIER.add(name)
        _STRING_LONG_SCALE[name] = number

_FRACTION_MARKER = set()

_NEGATIVES = {"minus"}

_NUMBER_CONNECTORS = {"og"}

_COMMA = {"komma"}

# Numbers below 1 million are written in one word in Danish, yielding very
# long words
# In some circumstances it may better to seperate individual words
# Set _EXTRA_SPACE_DA=" " for separating numbers below 1 million (
# orthographically incorrect)
# Set _EXTRA_SPACE_DA="" for correct spelling, this is standard

# _EXTRA_SPACE_DA = " "
_EXTRA_SPACE_DA = ""


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
    4.5 becomes "4 en halv" for speech and "4 1/2" for text
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
                result += ' ' + _NUM_POWERS_OF_TEN[scale_level]
            if scale_level >= 2:
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


def numbers_to_digits_da(text, short_scale=False,
                               ordinals=False, fractions=True):
    """
    Convert words in a string into their equivalent numbers.
    Args:
        text str:
        short_scale boolean: True if short scale numberres should be used.
        ordinals boolean: True if ordinals (e.g. first, second, third) should
                          be parsed to their number values (1, 2, 3...)
    Returns:
        str
        The original text, with numbers subbed in where appropriate.
    """
    tokens = tokenize(text)
    numbers_to_replace = \
        _extract_numbers_with_text_da(tokens, short_scale, ordinals, fractions)
    numbers_to_replace.sort(key=lambda number: number.start_index)

    results = []
    for token in tokens:
        if not numbers_to_replace or \
                token.index < numbers_to_replace[0].start_index:
            results.append(token.word)
        else:
            if numbers_to_replace and \
                    token.index == numbers_to_replace[0].start_index:
                results.append(str(numbers_to_replace[0].value))
            if numbers_to_replace and \
                    token.index == numbers_to_replace[0].end_index:
                numbers_to_replace.pop(0)

    return ' '.join(results)


def _extract_numbers_with_text_da(tokens, short_scale=False,
                                  ordinals=False, fractions=True):
    """
    Extract all numbers from a list of Tokens, with the words that
    represent them.

    Args:
        [Token]: The tokens to parse.
        short_scale bool: True if short scale numbers should be used, False for
                          long scale. True by default.
        ordinals bool: True if ordinal words (first, second, third, etc) should
                       be parsed.
        fractional_numbers bool: True if we should look for fractions and
                                 decimals.

    Returns:
        [ReplaceableNumber]: A list of tuples, each containing a number and a
                         string.

    """
    placeholder = "<placeholder>"  # inserted to maintain correct indices
    results = []
    while True:
        to_replace = _extract_number_with_text_da(tokens, short_scale, ordinals)

        if not to_replace:
            break

        if isinstance(to_replace.value, float) and not fractions:
            pass
        else:
            results.append(to_replace)

        tokens = [
            t if not
            to_replace.start_index <= t.index <= to_replace.end_index
            else
            Token(placeholder, t.index) for t in tokens
        ]
    results.sort(key=lambda n: n.start_index)
    return results


def _extract_number_with_text_da(tokens, short_scale=False, ordinals=False):
    """
    This function extracts a number from a list of Tokens.

    Args:
        tokens str: the string to normalize
        short_scale (bool): use short scale if True, long scale if False
        ordinals (bool): consider ordinal numbers
        fractional_numbers (bool): True if we should look for fractions and
                                   decimals.
    Returns:
        ReplaceableNumber

    """
    number, tokens = _extract_number_with_text_da_helper(tokens, short_scale, ordinals)
    return ReplaceableNumber(number, tokens)


def _extract_number_with_text_da_helper(tokens, short_scale, ordinals):
    """
    Helper for _extract_number_with_text_da.

    Args:
        tokens [Token]:
        short_scale boolean:
        ordinals boolean:
        fractional_numbers boolean:
    Returns:
        int or float, [Tokens]
    """
    if ordinals:
        for token in tokens:
            ordinal = is_ordinal_da(token.word)
            if ordinal:
                return ordinal, [token]

    return _extract_real_number_with_text_da(tokens, short_scale)


def _extract_real_number_with_text_da(tokens, short_scale):
    """
    This is handling real numbers.

    Args:
        tokens [Token]:
        short_scale boolean:
    Returns:
        int or float, [Tokens]
        The value parsed, and tokens that it corresponds to.
    """
    number_words = []
    val = _val = _current_val = None
    _comma = False
    to_sum = []

    for idx, token in enumerate(tokens):

        _prev_val = _current_val
        _current_val = None

        word = token.word

        if word in _NUMBER_CONNECTORS and not number_words:
            continue
        if word in (_NEGATIVES | _NUMBER_CONNECTORS | _COMMA):
            number_words.append(token)
            if word in _COMMA:
                _comma = token
                _current_val = _val or _prev_val
            continue

        prev_word = tokens[idx - 1].word if idx > 0 else ""
        next_word = tokens[idx + 1].word if idx + 1 < len(tokens) else ""

        if word not in _STRING_LONG_SCALE and \
                word not in _DA_NUMBERS and \
                word not in _MULTIPLIER and \
                not is_numeric_da(word) and \
                not is_fractional_da(word):
            words_only = [token.word for token in number_words]
            if _val is not None:
                to_sum.append(_val)
            if to_sum:
                val = sum(to_sum)

            if number_words and (not all([w in _ARTICLES | _NEGATIVES
                                          | _NUMBER_CONNECTORS for w in words_only])
                                 or str(val) == number_words[-1].word):
                break
            else:
                number_words.clear()
                to_sum.clear()
                val = _val = _prev_val = None
            continue
        elif word not in _MULTIPLIER \
                and prev_word not in _MULTIPLIER \
                and prev_word not in _NUMBER_CONNECTORS \
                and prev_word not in _NEGATIVES \
                and prev_word not in _COMMA \
                and prev_word not in _STRING_LONG_SCALE \
                and prev_word not in _DA_NUMBERS \
                and not is_ordinal_da(word) \
                and not is_numeric_da(prev_word) \
                and not is_fractional_da(prev_word):
            number_words = [token]
        else:
            number_words.append(token)

        # is this word already a number or a word of a number?
        _val = _current_val = is_number_da(word)

        # is this a negative number?
        if _current_val is not None and prev_word in _NEGATIVES:
            _val = 0 - _current_val

        # is the prev word a number and should we multiply it?
        if _prev_val is not None and (word in _MULTIPLIER or \
                                      word in _ARTICLES):
            to_sum.append(_prev_val * _current_val or _current_val)
            _val = _current_val = None

        # fraction handling
        _fraction_val = is_fractional_da(word, short_scale=short_scale)
        if _fraction_val:
            if _prev_val is not None and prev_word not in _ARTICLES and \
                    word not in _STRING_FRACTION_DA:  # sammensat brøk
                _val = _prev_val + _fraction_val
                if prev_word not in _NUMBER_CONNECTORS and tokens[idx - 1] not in number_words:
                    number_words.append(tokens[idx - 1])
            elif _prev_val is not None:
                _val = _prev_val * _fraction_val
                if tokens[idx - 1] not in number_words:
                    number_words.append(tokens[idx - 1])
            else:
                _val = _fraction_val
            _current_val = _val

        # directly following numbers without relation
        if (is_numeric_da(prev_word) or prev_word in _DA_NUMBERS) \
                and not _fraction_val and not is_fractional_da(next_word) and not to_sum:
            val = _prev_val
            number_words.pop(-1)
            break

        # TODO: handle spoken time, eg. "kvart over otte" ("quarter past eight"), "fem i ni"...

        # spoken decimals
        if _current_val is not None and _comma:
            # to_sum = [ 1, 0.2, 0.04,...]
            to_sum.append(_current_val if _current_val >= 10 else (_current_val) / (
                                                                          10 ** (token.index - _comma.index)))
            _val = _current_val = None

        if _current_val is not None and next_word in (_NUMBER_CONNECTORS | _COMMA | {""}):
            to_sum.append(_val or _current_val)
            _val = _current_val = None

        if not next_word and number_words:
            val = sum(to_sum) or _val

    return val, number_words


def is_fractional_da(input_str, short_scale=False):
    """
    This function takes the given text and checks if it is a fraction.
    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): use short scale if True, long scale if False
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction
    """
    # account for different numerators, e.g. totrediedele

    input_str = input_str.lower()
    numerator = 1
    prev_number = 0
    denominator = False
    remainder = ""

    # first check if is a fraction containing a char (eg "2/3")
    _bucket = input_str.split('/')
    if look_for_fractions(_bucket):
        numerator = float(_bucket[0])
        denominator = float(_bucket[1])

    if not denominator:
        for fraction in sorted(_STRING_FRACTION_DA.keys(),
                               key=lambda x: len(x),
                               reverse=True):
            if fraction in input_str and not denominator:
                denominator = _STRING_FRACTION_DA.get(fraction)
                remainder = input_str.replace(fraction, "")
                break

        if remainder:
            if not _DA_NUMBERS.get(remainder, False):
                # acount for eineindrittel
                for numstring, number in _DA_NUMBERS.items():
                    if remainder.endswith(numstring):
                        prev_number = _DA_NUMBERS.get(
                            remainder.replace(numstring, "", 1), 0)
                        numerator = number
                        break
                else:
                    return False
            else:
                numerator = _DA_NUMBERS.get(remainder)

    if denominator:
        return prev_number + (numerator / denominator)
    else:
        return False


def is_number_da(word: str):
    if is_numeric_da(word):
        if word.isdigit():
            return int(word)
        else:
            return float(word)
    elif word in _DA_NUMBERS:
        return _DA_NUMBERS.get(word)
    elif word in _STRING_LONG_SCALE:
        return _STRING_LONG_SCALE.get(word)

    return None


def is_numeric_da(input_str):
    """
    Takes in a string and tests to see if it is a number.

    Args:
        text (str): string to test if a number
    Returns:
        (bool): True if a number, else False
    """
    # da float("1.") = 1.0
    if input_str.endswith('.'):
        return False
    try:
        float(input_str)
        return True
    except ValueError:
        return False


def extract_number_da(text, short_scale=False, ordinals=False):
    """
    This function extracts a number from a text string

    Args:
        text (str): the string to normalize
        short_scale (bool): use short scale if True, long scale if False
        ordinals (bool): consider ordinal numbers
    Returns:
        (int) or (float) or False: The extracted number or False if no number
                                   was found
    """
    numbers = _extract_numbers_with_text_da(tokenize(text.lower()),
                                            short_scale, ordinals)
    # if query ordinals only consider ordinals
    if ordinals:
        numbers = list(filter(lambda x: isinstance(x.value, str)
                                        and x.value.endswith("."),
                              numbers))

    number = numbers[0].value if numbers else None

    if number:
        number = float(number)
        if number.is_integer():
            number = int(number)

    return number
