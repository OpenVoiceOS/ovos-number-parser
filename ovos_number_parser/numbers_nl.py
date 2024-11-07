#
# Copyright 2019 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from collections import OrderedDict
from math import floor

from ovos_number_parser.util import convert_to_mixed_fraction, is_numeric, look_for_fractions, Token, \
    ReplaceableNumber, tokenize, partition_list, invert_dict

_ARTICLES_NL = {'de', 'het'}

_NUM_STRING_NL = {
    0: 'nul',
    1: 'een',
    2: 'twee',
    3: 'drie',
    4: 'vier',
    5: 'vijf',
    6: 'zes',
    7: 'zeven',
    8: 'acht',
    9: 'negen',
    10: 'tien',
    11: 'elf',
    12: 'twaalf',
    13: 'dertien',
    14: 'veertien',
    15: 'vijftien',
    16: 'zestien',
    17: 'zeventien',
    18: 'achttien',
    19: 'negentien',
    20: 'twintig',
    30: 'dertig',
    40: 'veertig',
    50: 'vijftig',
    60: 'zestig',
    70: 'zeventig',
    80: 'tachtig',
    90: 'negentig'
}

_FRACTION_STRING_NL = {
    2: 'half',
    3: 'derde',
    4: 'vierde',
    5: 'vijfde',
    6: 'zesde',
    7: 'zevende',
    8: 'achtste',
    9: 'negende',
    10: 'tiende',
    11: 'elfde',
    12: 'twaalfde',
    13: 'dertiende',
    14: 'veertiende',
    15: 'vijftiende',
    16: 'zestiende',
    17: 'zeventiende',
    18: 'achttiende',
    19: 'negentiende',
    20: 'twintigste'
}

_LONG_SCALE_NL = OrderedDict([
    (100, 'honderd'),
    (1000, 'duizend'),
    (1000000, 'miljoen'),
    (1e12, "biljoen"),
    (1e18, 'triljoen'),
    (1e24, "quadriljoen"),
    (1e30, "quintillion"),
    (1e36, "sextillion"),
    (1e42, "septillion"),
    (1e48, "octillion"),
    (1e54, "nonillion"),
    (1e60, "decillion"),
    (1e66, "undecillion"),
    (1e72, "duodecillion"),
    (1e78, "tredecillion"),
    (1e84, "quattuordecillion"),
    (1e90, "quinquadecillion"),
    (1e96, "sedecillion"),
    (1e102, "septendecillion"),
    (1e108, "octodecillion"),
    (1e114, "novendecillion"),
    (1e120, "vigintillion"),
    (1e306, "unquinquagintillion"),
    (1e312, "duoquinquagintillion"),
    (1e336, "sesquinquagintillion"),
    (1e366, "unsexagintillion")
])

_SHORT_SCALE_NL = OrderedDict([
    (100, 'honderd'),
    (1000, 'duizend'),
    (1000000, 'miljoen'),
    (1e9, "miljard"),
    (1e12, 'biljoen'),
    (1e15, "quadrillion"),
    (1e18, "quintiljoen"),
    (1e21, "sextiljoen"),
    (1e24, "septiljoen"),
    (1e27, "octiljoen"),
    (1e30, "noniljoen"),
    (1e33, "deciljoen"),
    (1e36, "undeciljoen"),
    (1e39, "duodeciljoen"),
    (1e42, "tredeciljoen"),
    (1e45, "quattuordeciljoen"),
    (1e48, "quinquadeciljoen"),
    (1e51, "sedeciljoen"),
    (1e54, "septendeciljoen"),
    (1e57, "octodeciljoen"),
    (1e60, "novendeciljoen"),
    (1e63, "vigintiljoen"),
    (1e66, "unvigintiljoen"),
    (1e69, "uuovigintiljoen"),
    (1e72, "tresvigintiljoen"),
    (1e75, "quattuorvigintiljoen"),
    (1e78, "quinquavigintiljoen"),
    (1e81, "qesvigintiljoen"),
    (1e84, "septemvigintiljoen"),
    (1e87, "octovigintiljoen"),
    (1e90, "novemvigintiljoen"),
    (1e93, "trigintiljoen"),
    (1e96, "untrigintiljoen"),
    (1e99, "duotrigintiljoen"),
    (1e102, "trestrigintiljoen"),
    (1e105, "quattuortrigintiljoen"),
    (1e108, "quinquatrigintiljoen"),
    (1e111, "sestrigintiljoen"),
    (1e114, "septentrigintiljoen"),
    (1e117, "octotrigintiljoen"),
    (1e120, "noventrigintiljoen"),
    (1e123, "quadragintiljoen"),
    (1e153, "quinquagintiljoen"),
    (1e183, "sexagintiljoen"),
    (1e213, "septuagintiljoen"),
    (1e243, "octogintiljoen"),
    (1e273, "nonagintiljoen"),
    (1e303, "centiljoen"),
    (1e306, "uncentiljoen"),
    (1e309, "duocentiljoen"),
    (1e312, "trescentiljoen"),
    (1e333, "decicentiljoen"),
    (1e336, "undecicentiljoen"),
    (1e363, "viginticentiljoen"),
    (1e366, "unviginticentiljoen"),
    (1e393, "trigintacentiljoen"),
    (1e423, "quadragintacentiljoen"),
    (1e453, "quinquagintacentiljoen"),
    (1e483, "sexagintacentiljoen"),
    (1e513, "septuagintacentiljoen"),
    (1e543, "ctogintacentiljoen"),
    (1e573, "nonagintacentiljoen"),
    (1e603, "ducentiljoen"),
    (1e903, "trecentiljoen"),
    (1e1203, "quadringentiljoen"),
    (1e1503, "quingentiljoen"),
    (1e1803, "sescentiljoen"),
    (1e2103, "septingentiljoen"),
    (1e2403, "octingentiljoen"),
    (1e2703, "nongentiljoen"),
    (1e3003, "milliniljoen")
])

_ORDINAL_STRING_BASE_NL = {
    1: 'eerste',
    2: 'tweede',
    3: 'derde',
    4: 'vierde',
    5: 'vijfde',
    6: 'zesde',
    7: 'zevende',
    8: 'achtste',
    9: 'negende',
    10: 'tiende',
    11: 'elfde',
    12: 'twaalfde',
    13: 'dertiende',
    14: 'veertiende',
    15: 'vijftiende',
    16: 'zestiende',
    17: 'zeventiende',
    18: 'achttiende',
    19: 'negentiende',
    20: 'twintigste',
    30: 'dertigste',
    40: "veertigste",
    50: "vijftigste",
    60: "zestigste",
    70: "zeventigste",
    80: "tachtigste",
    90: "negentigste",
    10e3: "honderdste",
    1e3: "duizendste"
}

_SHORT_ORDINAL_STRING_NL = {
    1e6: "miloenste",
    1e9: "miljardste",
    1e12: "biljoenste",
    1e15: "biljardste",
    1e18: "triljoenste",
    1e21: "trijardste",
    1e24: "quadriljoenste",
    1e27: "quadriljardste",
    1e30: "quintiljoenste",
    1e33: "quintiljardste"
    # TODO > 1e-33
}
_SHORT_ORDINAL_STRING_NL.update(_ORDINAL_STRING_BASE_NL)

_LONG_ORDINAL_STRING_NL = {
    1e6: "miloenste",
    1e9: "miljardste",
    1e12: "biljoenste",
    1e15: "biljardste",
    1e18: "triljoenste",
    1e21: "trijardste",
    1e24: "quadriljoenste",
    1e27: "quadriljardste",
    1e30: "quintiljoenste",
    1e33: "quintiljardste"
    # TODO > 1e60
}
_LONG_ORDINAL_STRING_NL.update(_ORDINAL_STRING_BASE_NL)

# negate next number (-2 = 0 - 2)
_NEGATIVES_NL = {"min", "minus"}

# sum the next number (twenty two = 20 + 2)
_SUMS_NL = {'twintig', '20', 'dertig', '30', 'veertig', '40', 'vijftig', '50',
            'zestig', '60', 'zeventig', '70', 'techtig', '80', 'negentig',
            '90'}

_MULTIPLIES_LONG_SCALE_NL = set(_LONG_SCALE_NL.values())

_MULTIPLIES_SHORT_SCALE_NL = set(_SHORT_SCALE_NL.values())

# split sentence parse separately and sum ( 2 and a half = 2 + 0.5 )
_FRACTION_MARKER_NL = {"en"}

# decimal marker ( 1 point 5 = 1 + 0.5)
_DECIMAL_MARKER_NL = {"komma", "punt"}

_STRING_NUM_NL = invert_dict(_NUM_STRING_NL)
_STRING_NUM_NL.update({
    "half": 0.5,
    "driekwart": 0.75,
    "anderhalf": 1.5,
    "paar": 2
})

_STRING_SHORT_ORDINAL_NL = invert_dict(_SHORT_ORDINAL_STRING_NL)
_STRING_LONG_ORDINAL_NL = invert_dict(_LONG_ORDINAL_STRING_NL)

_MONTHS_NL = ['januari', 'februari', 'maart', 'april', 'mei', 'juni',
              'juli', 'augustus', 'september', 'oktober', 'november',
              'december']

_NUM_STRING_NL = {
    0: 'nul',
    1: 'één',
    2: 'twee',
    3: 'drie',
    4: 'vier',
    5: 'vijf',
    6: 'zes',
    7: 'zeven',
    8: 'acht',
    9: 'negen',
    10: 'tien',
    11: 'elf',
    12: 'twaalf',
    13: 'dertien',
    14: 'veertien',
    15: 'vijftien',
    16: 'zestien',
    17: 'zeventien',
    18: 'achttien',
    19: 'negentien',
    20: 'twintig',
    30: 'dertig',
    40: 'veertig',
    50: 'vijftig',
    60: 'zestig',
    70: 'zeventig',
    80: 'tachtig',
    90: 'negentig',
    100: 'honderd'
}

# Dutch uses "long scale" https://en.wikipedia.org/wiki/Long_and_short_scales
# Currently, numbers are limited to 1000000000000000000000000,
# but _NUM_POWERS_OF_TEN can be extended to include additional number words


_NUM_POWERS_OF_TEN = [
    '', 'duizend', 'miljoen', 'miljard', 'biljoen', 'biljard', 'triljoen',
    'triljard'
]

# Numbers below 1 million are written in one word in dutch, yielding very
# long words
# In some circumstances it may better to seperate individual words
# Set _EXTRA_SPACE_NL=" " for separating numbers below 1 million (
# orthographically incorrect)
# Set _EXTRA_SPACE_NL="" for correct spelling, this is standard

# _EXTRA_SPACE_NL = " "
_EXTRA_SPACE_NL = ""


def nice_number_nl(number, speech=True, denominators=range(1, 21)):
    """ Dutch helper for nice_number
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
    den_str = _FRACTION_STRING_NL[den]
    if whole == 0:
        if num == 1:
            return_string = 'één {}'.format(den_str)
        else:
            return_string = '{} {}'.format(num, den_str)
    elif num == 1:
        return_string = '{} en één {}'.format(whole, den_str)
    else:
        return_string = '{} en {} {}'.format(whole, num, den_str)

    return return_string


def pronounce_number_nl(number, places=2, short_scale=True, scientific=False,
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

    def pronounce_triplet_nl(num):
        result = ""
        num = floor(num)
        if num > 99:
            hundreds = floor(num / 100)
            if hundreds > 0:
                result += _NUM_STRING_NL[
                              hundreds] + _EXTRA_SPACE_NL + 'honderd' + _EXTRA_SPACE_NL
                num -= hundreds * 100
        if num == 0:
            result += ''  # do nothing
        elif num <= 20:
            result += _NUM_STRING_NL[num]  # + _EXTRA_SPACE_DA
        elif num > 20:
            ones = num % 10
            tens = num - ones
            if ones > 0:
                result += _NUM_STRING_NL[ones] + _EXTRA_SPACE_NL
                if tens > 0:
                    result += 'en' + _EXTRA_SPACE_NL
            if tens > 0:
                result += _NUM_STRING_NL[tens] + _EXTRA_SPACE_NL
        return result

    def pronounce_fractional_nl(num,
                                places):  # fixed number of places even with
        # trailing zeros
        result = ""
        place = 10
        while places > 0:  # doesn't work with 1.0001 and places = 2: int(
            # number*place) % 10 > 0 and places > 0:
            result += " " + _NUM_STRING_NL[int(num * place) % 10]
            if int(num * place) % 10 == 1:
                result += ''  # "1" is pronounced "eins" after the decimal
                # point
            place *= 10
            places -= 1
        return result

    def pronounce_whole_number_nl(num, scale_level=0):
        if num == 0:
            return ''

        num = floor(num)
        result = ''
        last_triplet = num % 1000

        if last_triplet == 1:
            if scale_level == 0:
                if result != '':
                    result += '' + 'één'
                else:
                    result += "één"
            elif scale_level == 1:
                result += 'één' + _EXTRA_SPACE_NL + 'duizend' + _EXTRA_SPACE_NL
            else:
                result += "één " + _NUM_POWERS_OF_TEN[scale_level] + ' '
        elif last_triplet > 1:
            result += pronounce_triplet_nl(last_triplet)
            if scale_level == 1:
                # result += _EXTRA_SPACE_DA
                result += 'duizend' + _EXTRA_SPACE_NL
            if scale_level >= 2:
                # if _EXTRA_SPACE_DA == '':
                #    result += " "
                result += " " + _NUM_POWERS_OF_TEN[scale_level] + ' '
            if scale_level >= 2:
                if scale_level % 2 == 0:
                    result += ""  # Miljioen
                result += ""  # Miljard, Miljoen

        num = floor(num / 1000)
        scale_level += 1
        return pronounce_whole_number_nl(num,
                                         scale_level) + result + ''

    result = ""
    if abs(number) >= 1000000000000000000000000:  # cannot do more than this
        return str(number)
    elif number == 0:
        return str(_NUM_STRING_NL[0])
    elif number < 0:
        return "min " + pronounce_number_nl(abs(number), places)
    else:
        if number == int(number):
            return pronounce_whole_number_nl(number)
        else:
            whole_number_part = floor(number)
            fractional_part = number - whole_number_part
            result += pronounce_whole_number_nl(whole_number_part)
            if places > 0:
                result += " komma"
                result += pronounce_fractional_nl(fractional_part, places)
            return result


def pronounce_ordinal_nl(number):
    """
    This function pronounces a number as an ordinal

    1 -> first
    2 -> second

    Args:
        number (int): the number to format
    Returns:
        (str): The pronounced number string.
    """
    ordinals = ["nulste", "eerste", "tweede", "derde", "vierde", "vijfde",
                "zesde", "zevende", "achtste"]
    # only for whole positive numbers including zero
    if number < 0 or number != int(number):
        return number
    if number < 4:
        return ordinals[number]
    if number < 8:
        return pronounce_number_nl(number) + "de"
    if number < 9:
        return pronounce_number_nl(number) + "ste"
    if number < 20:
        return pronounce_number_nl(number) + "de"
    return pronounce_number_nl(number) + "ste"


def numbers_to_digits_nl(text, short_scale=True, ordinals=False):
    """Convert words in a string into their equivalent numbers.
    Args:
        text str:
        short_scale boolean: True if short scale numbers should be used.
        ordinals boolean: True if ordinals (e.g. first, second, third) should
                          be parsed to their number values (1, 2, 3...)

    Returns:
        str
        The original text, with numbers subbed in where appropriate.
    """
    text = text.lower()
    tokens = tokenize(text)
    numbers_to_replace = \
        _extract_numbers_with_text_nl(tokens, short_scale, ordinals)
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


def _extract_numbers_with_text_nl(tokens, short_scale=True,
                                  ordinals=False, fractional_numbers=True):
    """Extract all numbers from a list of _Tokens, with the representing words.

    Args:
        [Token]: The tokens to parse.
        short_scale bool: True if short scale numbers should be used, False for
                          long scale. True by default.
        ordinals bool: True if ordinal words (first, second, third, etc) should
                       be parsed.
        fractional_numbers bool: True if we should look for fractions and
                                 decimals.

    Returns:
        [_ReplaceableNumber]: A list of tuples, each containing a number and a
                         string.
    """
    placeholder = "<placeholder>"  # inserted to maintain correct indices
    results = []
    while True:
        to_replace = \
            _extract_number_with_text_nl(tokens, short_scale,
                                         ordinals, fractional_numbers)

        if not to_replace:
            break

        results.append(to_replace)

        tokens = [
            t if not
            to_replace.start_index <= t.index <= to_replace.end_index
            else
            Token(placeholder, t.index) for t in tokens
        ]
    results.sort(key=lambda n: n.start_index)
    return results


def _extract_number_with_text_nl(tokens, short_scale=True,
                                 ordinals=False, fractional_numbers=True):
    """This function extracts a number from a list of _Tokens.

    Args:
        tokens str: the string to normalize
        short_scale (bool): use short scale if True, long scale if False
        ordinals (bool): consider ordinal numbers, third=3 instead of 1/3
        fractional_numbers (bool): True if we should look for fractions and
                                   decimals.
    Returns:
        _ReplaceableNumber
    """
    number, tokens = \
        _extract_number_with_text_nl_helper(tokens, short_scale,
                                            ordinals, fractional_numbers)
    while tokens and tokens[0].word in _ARTICLES_NL:
        tokens.pop(0)
    return ReplaceableNumber(number, tokens)


def _extract_number_with_text_nl_helper(tokens,
                                        short_scale=True, ordinals=False,
                                        fractional_numbers=True):
    """Helper for _extract_number_with_text_nl.

    This contains the real logic for parsing, but produces
    a result that needs a little cleaning (specific, it may
    contain leading articles that can be trimmed off).

    Args:
        tokens [Token]:
        short_scale boolean:
        ordinals boolean:
        fractional_numbers boolean:

    Returns:
        int or float, [_Tokens]
    """
    if fractional_numbers:
        fraction, fraction_text = \
            _extract_fraction_with_text_nl(tokens, short_scale, ordinals)
        if fraction:
            return fraction, fraction_text

        decimal, decimal_text = \
            _extract_decimal_with_text_nl(tokens, short_scale, ordinals)
        if decimal:
            return decimal, decimal_text

    return _extract_whole_number_with_text_nl(tokens, short_scale, ordinals)


def _extract_fraction_with_text_nl(tokens, short_scale, ordinals):
    """Extract fraction numbers from a string.

    This function handles text such as '2 and 3/4'. Note that "one half" or
    similar will be parsed by the whole number function.

    Args:
        tokens [Token]: words and their indexes in the original string.
        short_scale boolean:
        ordinals boolean:

    Returns:
        (int or float, [Token])
        The value found, and the list of relevant tokens.
        (None, None) if no fraction value is found.
    """
    for c in _FRACTION_MARKER_NL:
        partitions = partition_list(tokens, lambda t: t.word == c)

        if len(partitions) == 3:
            numbers1 = \
                _extract_numbers_with_text_nl(partitions[0], short_scale,
                                              ordinals, fractional_numbers=False)
            numbers2 = \
                _extract_numbers_with_text_nl(partitions[2], short_scale,
                                              ordinals, fractional_numbers=True)

            if not numbers1 or not numbers2:
                return None, None

            # ensure first is not a fraction and second is a fraction
            num1 = numbers1[-1]
            num2 = numbers2[0]
            if num1.value >= 1 and 0 < num2.value < 1:
                return num1.value + num2.value, \
                       num1.tokens + partitions[1] + num2.tokens

    return None, None


def _extract_decimal_with_text_nl(tokens, short_scale, ordinals):
    """Extract decimal numbers from a string.

    This function handles text such as '2 point 5'.

    Notes:
        While this is a helper for extractnumber_nl, it also depends on
        extractnumber_nl, to parse out the components of the decimal.

        This does not currently handle things like:
            number dot number number number

    Args:
        tokens [Token]: The text to parse.
        short_scale boolean:
        ordinals boolean:

    Returns:
        (float, [Token])
        The value found and relevant tokens.
        (None, None) if no decimal value is found.
    """
    for c in _DECIMAL_MARKER_NL:
        partitions = partition_list(tokens, lambda t: t.word == c)

        if len(partitions) == 3:
            numbers1 = \
                _extract_numbers_with_text_nl(partitions[0], short_scale,
                                              ordinals, fractional_numbers=False)
            numbers2 = \
                _extract_numbers_with_text_nl(partitions[2], short_scale,
                                              ordinals, fractional_numbers=False)

            if not numbers1 or not numbers2:
                return None, None

            number = numbers1[-1]
            decimal = numbers2[0]

            # TODO handle number dot number number number
            if "." not in str(decimal.text):
                return number.value + float('0.' + str(decimal.value)), \
                       number.tokens + partitions[1] + decimal.tokens
    return None, None


def _extract_whole_number_with_text_nl(tokens, short_scale, ordinals):
    """Handle numbers not handled by the decimal or fraction functions.

    This is generally whole numbers. Note that phrases such as "one half" will
    be handled by this function, while "one and a half" are handled by the
    fraction function.

    Args:
        tokens [Token]:
        short_scale boolean:
        ordinals boolean:

    Returns:
        int or float, [_Tokens]
        The value parsed, and tokens that it corresponds to.
    """
    multiplies, string_num_ordinal, string_num_scale = \
        _initialize_number_data_nl(short_scale)

    number_words = []  # type: [Token]
    val = False
    prev_val = None
    next_val = None
    to_sum = []
    for idx, token in enumerate(tokens):
        current_val = None
        if next_val:
            next_val = None
            continue

        word = token.word
        if word in _ARTICLES_NL or word in _NEGATIVES_NL:
            number_words.append(token)
            continue

        prev_word = tokens[idx - 1].word if idx > 0 else ""
        next_word = tokens[idx + 1].word if idx + 1 < len(tokens) else ""

        if word not in string_num_scale and \
                word not in _STRING_NUM_NL and \
                word not in _SUMS_NL and \
                word not in multiplies and \
                not (ordinals and word in string_num_ordinal) and \
                not is_numeric(word) and \
                not is_fractional_nl(word, short_scale=short_scale) and \
                not look_for_fractions(word.split('/')):
            words_only = [token.word for token in number_words]
            if number_words and not all([w in _ARTICLES_NL |
                                         _NEGATIVES_NL for w in words_only]):
                break
            else:
                number_words = []
                continue
        elif word not in multiplies \
                and prev_word not in multiplies \
                and prev_word not in _SUMS_NL \
                and not (ordinals and prev_word in string_num_ordinal) \
                and prev_word not in _NEGATIVES_NL \
                and prev_word not in _ARTICLES_NL:
            number_words = [token]
        elif prev_word in _SUMS_NL and word in _SUMS_NL:
            number_words = [token]
        else:
            number_words.append(token)

        # is this word already a number ?
        if is_numeric(word):
            if word.isdigit():  # doesn't work with decimals
                val = int(word)
            else:
                val = float(word)
            current_val = val

        # is this word the name of a number ?
        if word in _STRING_NUM_NL:
            val = _STRING_NUM_NL.get(word)
            current_val = val
        elif word in string_num_scale:
            val = string_num_scale.get(word)
            current_val = val
        elif ordinals and word in string_num_ordinal:
            val = string_num_ordinal[word]
            current_val = val

        # is the prev word an ordinal number and current word is one?
        # second one, third one
        if ordinals and prev_word in string_num_ordinal and val == 1:
            val = prev_val

        # is the prev word a number and should we sum it?
        # twenty two, fifty six
        if prev_word in _SUMS_NL and val and val < 10:
            val = prev_val + val

        # is the prev word a number and should we multiply it?
        # twenty hundred, six hundred
        if word in multiplies:
            if not prev_val:
                prev_val = 1
            val = prev_val * val

        # is this a spoken fraction?
        # half cup
        if val is False:
            val = is_fractional_nl(word, short_scale=short_scale)
            current_val = val

        # 2 fifths
        if not ordinals:
            next_val = is_fractional_nl(next_word, short_scale=short_scale)
            if next_val:
                if not val:
                    val = 1
                val = val * next_val
                number_words.append(tokens[idx + 1])

        # is this a negative number?
        if val and prev_word and prev_word in _NEGATIVES_NL:
            val = 0 - val

        # let's make sure it isn't a fraction
        if not val:
            # look for fractions like "2/3"
            aPieces = word.split('/')
            if look_for_fractions(aPieces):
                val = float(aPieces[0]) / float(aPieces[1])
                current_val = val

        else:
            if prev_word in _SUMS_NL and word not in _SUMS_NL and current_val >= 10:
                # Backtrack - we've got numbers we can't sum.
                number_words.pop()
                val = prev_val
                break
            prev_val = val

            # handle long numbers
            # six hundred sixty six
            # two million five hundred thousand
            if word in multiplies and next_word not in multiplies:
                to_sum.append(val)
                val = 0
                prev_val = 0

    if val is not None and to_sum:
        val += sum(to_sum)

    return val, number_words


def _initialize_number_data_nl(short_scale):
    """Generate dictionaries of words to numbers, based on scale.

    This is a helper function for _extract_whole_number.

    Args:
        short_scale boolean:

    Returns:
        (set(str), dict(str, number), dict(str, number))
        multiplies, string_num_ordinal, string_num_scale
    """
    multiplies = _MULTIPLIES_SHORT_SCALE_NL if short_scale \
        else _MULTIPLIES_LONG_SCALE_NL

    string_num_ordinal_nl = _STRING_SHORT_ORDINAL_NL if short_scale \
        else _STRING_LONG_ORDINAL_NL

    string_num_scale_nl = _SHORT_SCALE_NL if short_scale else _LONG_SCALE_NL
    string_num_scale_nl = invert_dict(string_num_scale_nl)

    return multiplies, string_num_ordinal_nl, string_num_scale_nl


def extract_number_nl(text, short_scale=True, ordinals=False):
    """Extract a number from a text string

    The function handles pronunciations in long scale and short scale

    https://en.wikipedia.org/wiki/Names_of_large_numbers

    Args:
        text (str): the string to normalize
        short_scale (bool): use short scale if True, long scale if False
        ordinals (bool): consider ordinal numbers, third=3 instead of 1/3
    Returns:
        (int) or (float) or False: The extracted number or False if no number
                                   was found
    """
    return _extract_number_with_text_nl(tokenize(text.lower()),
                                        short_scale, ordinals).value


def is_fractional_nl(input_str, short_scale=True):
    """This function takes the given text and checks if it is a fraction.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): use short scale if True, long scale if False
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction
    """
    fracts = {"heel": 1, "half": 2, "halve": 2, "kwart": 4}
    if short_scale:
        for num in _SHORT_ORDINAL_STRING_NL:
            if num > 2:
                fracts[_SHORT_ORDINAL_STRING_NL[num]] = num
    else:
        for num in _LONG_ORDINAL_STRING_NL:
            if num > 2:
                fracts[_LONG_ORDINAL_STRING_NL[num]] = num

    if input_str.lower() in fracts:
        return 1.0 / fracts[input_str.lower()]
    return False
