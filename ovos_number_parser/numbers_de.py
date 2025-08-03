from collections import OrderedDict
from math import floor

from ovos_number_parser.util import (invert_dict, convert_to_mixed_fraction, tokenize, ReplaceableNumber, Token,
                                     look_for_fractions)

_ARTICLES = {'der', 'das', 'die', 'dem', 'den'}

# _SPOKEN_NUMBER
_NUM_STRING = {
    0: 'null',
    1: 'eins',
    2: 'zwei',
    3: 'drei',
    4: 'vier',
    5: 'fünf',
    6: 'sechs',
    7: 'sieben',
    8: 'acht',
    9: 'neun',
    10: 'zehn',
    11: 'elf',
    12: 'zwölf',
    13: 'dreizehn',
    14: 'vierzehn',
    15: 'fünfzehn',
    16: 'sechzehn',
    17: 'siebzehn',
    18: 'achtzehn',
    19: 'neunzehn',
    20: 'zwanzig',
    30: 'dreißig',
    40: 'vierzig',
    50: 'fünfzig',
    60: 'sechzig',
    70: 'siebzig',
    80: 'achtzig',
    90: 'neunzig',
    100: 'hundert',
    200: 'zweihundert',
    300: 'dreihundert',
    400: 'vierhundert',
    500: 'fünfhundert',
    600: 'sechshundert',
    700: 'siebenhundert',
    800: 'achthundert',
    900: 'neunhundert',
    1000: 'tausend',
    1000000: 'million'
}

_STRING_NUM = invert_dict(_NUM_STRING)
_STRING_NUM.update({
    'ein': 1,
    'eine': 1,
    'einer': 1,
    'eines': 1,
    'einem': 1,
    'einen': 1
})

_MONTHS = ['januar', 'februar', 'märz', 'april', 'mai', 'juni',
           'juli', 'august', 'september', 'oktober', 'november',
           'dezember']

# German uses "long scale" https://en.wikipedia.org/wiki/Long_and_short_scales
# Currently, numbers are limited to 1000000000000000000000000,
# but _NUM_POWERS_OF_TEN can be extended to include additional number words


_NUM_POWERS_OF_TEN = [
    '', 'tausend', 'Million', 'Milliarde', 'Billion', 'Billiarde', 'Trillion',
    'Trilliarde'
]

_FRACTION_STRING = {
    2: 'halb',
    3: 'drittel',
    4: 'viertel',
    5: 'fünftel',
    6: 'sechstel',
    7: 'siebtel',
    8: 'achtel',
    9: 'neuntel',
    10: 'zehntel',
    11: 'elftel',
    12: 'zwölftel',
    13: 'dreizehntel',
    14: 'vierzehntel',
    15: 'fünfzehntel',
    16: 'sechzehntel',
    17: 'siebzehntel',
    18: 'achtzehntel',
    19: 'neunzehntel',
    20: 'zwanzigstel'
}

_STRING_FRACTION = invert_dict(_FRACTION_STRING)
_STRING_FRACTION.update({
    'halb': 2,
    'halbe': 2,
    'halben': 2,
    'halbes': 2,
    'halber': 2,
    'halbem': 2
})

# Numbers below 1 million are written in one word in German, yielding very
# long words
# In some circumstances it may better to seperate individual words
# Set _EXTRA_SPACE_DA=" " for separating numbers below 1 million (
# orthographically incorrect)
# Set _EXTRA_SPACE_DA="" for correct spelling, this is standard

# _EXTRA_SPACE_DA = " "
_EXTRA_SPACE = ""

_ORDINAL_BASE = {
    "1.": "erst",
    "2.": "zweit",
    "3.": "dritt",
    "4.": "viert",
    "5.": "fünft",
    "6.": "sechst",
    "7.": "siebt",
    "8.": "acht",
    "9.": "neunt",
    "10.": "zehnt",
    "11.": "elft",
    "12.": "zwölft",
    "13.": "dreizehnt",
    "14.": "vierzehnt",
    "15.": "fünfzehnt",
    "16.": "sechzehnt",
    "17.": "siebzehnt",
    "18.": "achtzehnt",
    "19.": "neunzehnt",
    "20.": "zwanzigst",
    "21.": "einundzwanzigst",
    "22.": "zweiundzwanzigst",
    "23.": "dreiundzwanzigst",
    "24.": "vierundzwanzigst",
    "25.": "fünfundzwanzigst",
    "26.": "sechsundzwanzigst",
    "27.": "siebenundzwanzigst",
    "28.": "achtundzwanzigst",
    "29.": "neunundzwanzigst",
    "30.": "dreißigst",
    "31.": "einunddreißigst",
    "32.": "zweiunddreißigst",
    "33.": "dreiunddreißigst",
    "34.": "vierunddreißigst",
    "35.": "fünfunddreißigst",
    "36.": "sechsunddreißigst",
    "37.": "siebenunddreißigst",
    "38.": "achtunddreißigst",
    "39.": "neununddreißigst",
    "40.": "vierzigst",
    "41.": "einundvierzigst",
    "42.": "zweiundvierzigst",
    "43.": "dreiundvierzigst",
    "44.": "vierundvierzigst",
    "45.": "fünfundvierzigst",
    "46.": "sechsundvierzigst",
    "47.": "siebenundvierzigst",
    "48.": "achtundvierzigst",
    "49.": "neunundvierzigst",
    "50.": "fünfzigst",
    "51.": "einundfünfzigst",
    "52.": "zweiundfünfzigst",
    "53.": "dreiundfünfzigst",
    "60.": "sechzigst",
    "70.": "siebzigst",
    "80.": "achtzigst",
    "90.": "neunzigst",
    "100.": "einhundertst",
    "1000.": "eintausendst",
    "1000000.": "millionst"
}

_LONG_SCALE = OrderedDict([
    (100, 'hundert'),
    (1000, 'tausend'),
    (1000000, 'million'),
    (1e9, "milliarde"),
    (1e12, 'billion'),
    (1e15, "billiarde"),
    (1e18, "trillion"),
    (1e21, "trilliarde"),
    (1e24, "quadrillion"),
    (1e27, "quadrilliarde")
])

_MULTIPLIER = set(_LONG_SCALE.values())

_STRING_LONG_SCALE = invert_dict(_LONG_SCALE)

# ending manipulation
for number, item in _LONG_SCALE.items():
    if int(number) > 1000:
        if item.endswith('e'):
            name = item + 'n'
            _MULTIPLIER.add(name)
            _STRING_LONG_SCALE[name] = number
        else:
            name = item + 'en'
            _MULTIPLIER.add(name)
            _STRING_LONG_SCALE[name] = number

_LONG_ORDINAL = {
    1e6: "millionst",
    1e9: "milliardst",
    1e12: "billionst",
    1e15: "billiardst",
    1e18: "trillionst",
    1e21: "trilliardst",
    1e24: "quadrillionst",
    1e27: "quadrilliardst"
}

_LONG_ORDINAL.update(_ORDINAL_BASE)

# dict für erste, drittem, millionstes ...
_STRING_LONG_ORDINAL = {ord + ending: num for ord, num in invert_dict(_LONG_ORDINAL).items()
                        for ending in ("en", "em", "es", "er", "e")}

_FRACTION_MARKER = set()

_NEGATIVES = {"minus"}

_NUMBER_CONNECTORS = {"und"}

_COMMA = {"komma", "comma", "punkt"}


def nice_number_de(number, speech=True, denominators=range(1, 21)):
    """ German helper for nice_number
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
    den_str = _FRACTION_STRING[den]
    if whole == 0:
        if num == 1:
            return_string = 'ein {}'.format(den_str)
        else:
            return_string = '{} {}'.format(num, den_str)
    elif num == 1:
        return_string = '{} und ein {}'.format(whole, den_str)
    else:
        return_string = '{} und {} {}'.format(whole, num, den_str)

    return return_string


def pronounce_number_de(number, places=2, short_scale=True, scientific=False,
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

    def pronounce_triplet_de(num):
        result = ""
        num = floor(num)
        if num > 99:
            hundreds = floor(num / 100)
            if hundreds > 0:
                number = _NUM_STRING[hundreds] if hundreds > 1 else "ein"
                result += number + 'hundert' + _EXTRA_SPACE
                num -= hundreds * 100
        if num == 0:
            result += ''  # do nothing
        elif num == 1:
            result += 'eins'  # need the s for the last digit
        elif num <= 20:
            result += _NUM_STRING[num]  # + _EXTRA_SPACE_DA
        elif num > 20:
            ones = num % 10
            tens = num - ones
            if ones > 0:
                number = _NUM_STRING[ones]
                if ones == 1 and tens > 0:  # eins > ein
                    number = number[:-1]
                result += number + _EXTRA_SPACE
                if tens > 0:
                    result += 'und' + _EXTRA_SPACE
            if tens > 0:
                result += _NUM_STRING[tens] + _EXTRA_SPACE
        return result

    def pronounce_fractional_de(num,
                                places):  # fixed number of places even with
        # trailing zeros
        result = ""
        place = 10
        while places > 0:  # doesn't work with 1.0001 and places = 2: int(
            # number*place) % 10 > 0 and places > 0:
            result += " " + _NUM_STRING[int(num * place) % 10]
            if int(num * place) % 10 == 1:
                result += 's'  # "1" is pronounced "eins" after the decimal
                # point
            place *= 10
            places -= 1
        return result

    def pronounce_whole_number_de(num, scale_level=0):
        if num == 0:
            return ''

        num = floor(num)
        result = ''
        last_triplet = num % 1000

        if last_triplet == 1:
            if scale_level == 0:
                if result != '':
                    result += '' + 'eins'
                else:
                    result += "eins"
            elif scale_level == 1:
                result += 'ein' + _EXTRA_SPACE + 'tausend' + _EXTRA_SPACE
            else:
                result += "eine " + _NUM_POWERS_OF_TEN[scale_level] + ' '
        elif last_triplet > 1:
            result += pronounce_triplet_de(last_triplet)
            if scale_level == 1:
                # result += _EXTRA_SPACE_DA
                result += 'tausend' + _EXTRA_SPACE
            if scale_level >= 2:
                # if _EXTRA_SPACE_DA == '':
                #    result += " "
                result += " " + _NUM_POWERS_OF_TEN[scale_level]
            if scale_level >= 2:
                if scale_level % 2 == 0:
                    result += "e"  # MillionE
                result += "n "  # MilliardeN, MillioneN

        num = floor(num / 1000)
        scale_level += 1
        return pronounce_whole_number_de(num,
                                         scale_level) + result  # + _EXTRA_SPACE_DA

    result = ""
    if abs(number) >= 1000000000000000000000000:  # cannot do more than this
        return str(number)
    elif number == 0:
        return str(_NUM_STRING[0])
    elif number < 0:
        return "minus " + pronounce_number_de(abs(number), places)
    else:
        if number == int(number):
            return pronounce_whole_number_de(number)
        else:
            whole_number_part = floor(number)
            fractional_part = number - whole_number_part
            result += pronounce_whole_number_de(whole_number_part)
            if places > 0:
                result += " Komma"
                result += pronounce_fractional_de(fractional_part, places)
            return result


def pronounce_ordinal_de(number):
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

    ordinals = ["nullte", "erste", "zweite", "dritte", "vierte", "fünfte",
                "sechste", "siebte", "achte"]

    # only for whole positive numbers including zero
    if number < 0 or number != int(number):
        return number
    elif number < 9:
        return ordinals[number]
    elif number < 20:
        return pronounce_number_de(number) + "te"
    else:
        return pronounce_number_de(number) + "ste"


def numbers_to_digits_de(text, short_scale=False,
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
        _extract_numbers_with_text_de(tokens, short_scale, ordinals, fractions)
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


def _extract_numbers_with_text_de(tokens, short_scale=True,
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
        to_replace = \
            _extract_number_with_text_de(tokens, short_scale,
                                         ordinals)

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


def _extract_number_with_text_de(tokens, short_scale=True,
                                 ordinals=False):
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
    number, tokens = \
        _extract_number_with_text_de_helper(tokens, short_scale,
                                            ordinals)
    return ReplaceableNumber(number, tokens)


def _extract_number_with_text_de_helper(tokens,
                                        short_scale, ordinals):
    """
    Helper for _extract_number_with_text_de.

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
            ordinal = is_ordinal_de(token.word)
            if ordinal:
                return ordinal, [token]

    return _extract_real_number_with_text_de(tokens, short_scale)


def _extract_real_number_with_text_de(tokens, short_scale):
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
                word not in _STRING_NUM and \
                word not in _MULTIPLIER and \
                not is_numeric_de(word) and \
                not is_fractional_de(word):
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
                and prev_word not in _STRING_NUM \
                and not is_ordinal_de(word) \
                and not is_numeric_de(prev_word) \
                and not is_fractional_de(prev_word):
            number_words = [token]
        else:
            number_words.append(token)

        # is this word already a number or a word of a number?
        _val = _current_val = is_number_de(word)

        # is this a negative number?
        if _current_val is not None and prev_word in _NEGATIVES:
            _val = 0 - _current_val

        # is the prev word a number and should we multiply it?
        if _prev_val is not None and (word in _MULTIPLIER or \
                                      word in ("einer", "eines", "einem")):
            to_sum.append(_prev_val * _current_val or _current_val)
            _val = _current_val = None

        # fraction handling
        _fraction_val = is_fractional_de(word, short_scale=short_scale)
        if _fraction_val:
            if _prev_val is not None and prev_word != "eine" and \
                    word not in _STRING_FRACTION:  # zusammengesetzter Bruch
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
        if (is_numeric_de(prev_word) or prev_word in _STRING_NUM) \
                and not _fraction_val and not is_fractional_de(next_word) and not to_sum:
            val = _prev_val
            number_words.pop(-1)
            break

        # is this a spoken time ("drei viertel acht")
        if isinstance(_prev_val, float) and is_number_de(word) and not to_sum:
            if idx + 1 < len(tokens):
                _, number = _extract_real_number_with_text_de([tokens[idx + 1]],
                                                              short_scale=short_scale)
            if not next_word or not number:
                val = f"{_val - 1}:{int(60 * _prev_val)}"
                break

        # correct time format (whisper "13.30 Uhr")
        if all([isinstance(_current_val, float),
                next_word.lower() in ["uhr", "pm", "a.m.", "p.m."]]):
            components = word.split(".")
            if len(components) == 2 and \
                    all(map(str.isdigit, components)) and \
                    int(components[0]) < 25 and int(components[1]) < 60:
                _hstr, _mstr = components
                _mstr = _mstr.ljust(2, "0")
                tokens[idx] = Token(f"{_hstr}:{_mstr}", idx)
                number_words.clear()
                _val = _prev_val = None
                continue

                # spoken decimals
        if _current_val is not None and _comma:
            # to_sum = [ 1, 0.2, 0.04,...]
            to_sum.append(_current_val if _current_val >= 10 else (
                                                                      _current_val) / (
                                                                          10 ** (token.index - _comma.index)))
            _val = _current_val = None

        if _current_val is not None and next_word in (_NUMBER_CONNECTORS | _COMMA | {""}):
            to_sum.append(_val or _current_val)
            _val = _current_val = None

        if not next_word and number_words:
            val = sum(to_sum) or _val

    return val, number_words


def is_fractional_de(input_str, short_scale=False):
    """
    This function takes the given text and checks if it is a fraction.
    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): use short scale if True, long scale if False
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction
    """
    # account for different numerators, e.g. zweidrittel

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
        for fraction in sorted(_STRING_FRACTION.keys(),
                               key=lambda x: len(x),
                               reverse=True):
            if fraction in input_str and not denominator:
                denominator = _STRING_FRACTION.get(fraction)
                remainder = input_str.replace(fraction, "")
                break

        if remainder:
            if not _STRING_NUM.get(remainder, False):
                # acount for eineindrittel
                for numstring, number in _STRING_NUM.items():
                    if remainder.endswith(numstring):
                        prev_number = _STRING_NUM.get(
                            remainder.replace(numstring, "", 1), 0)
                        numerator = number
                        break
                else:
                    return False
            else:
                numerator = _STRING_NUM.get(remainder)

    if denominator:
        return prev_number + (numerator / denominator)
    else:
        return False


def is_ordinal_de(input_str):
    """
    This function takes the given text and checks if it is an ordinal number.
    Args:
        input_str (str): the string to check if ordinal
    Returns:
        (bool) or (float): False if not an ordinal, otherwise the number
        corresponding to the ordinal
    ordinals for 1, 3, 7 and 8 are irregular
    only works for ordinals corresponding to the numbers in _STRING_NUM
    """
    val = _STRING_LONG_ORDINAL.get(input_str.lower(), False)
    # account for numbered ordinals
    if not val and input_str.endswith('.') and is_numeric_de(input_str[:-1]):
        val = input_str
    return val


def _get_ordinal_index(input_str: str, type_: type = str):
    ord = is_ordinal_de(input_str)
    return type_(ord.replace(".", "")) if ord else ord


def is_number_de(word: str):
    if is_numeric_de(word):
        if word.isdigit():
            return int(word)
        else:
            return float(word)
    elif word in _STRING_NUM:
        return _STRING_NUM.get(word)
    elif word in _STRING_LONG_SCALE:
        return _STRING_LONG_SCALE.get(word)

    return None


def is_numeric_de(input_str):
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


def extract_number_de(text, short_scale=True, ordinals=False):
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
    numbers = _extract_numbers_with_text_de(tokenize(text.lower()),
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
