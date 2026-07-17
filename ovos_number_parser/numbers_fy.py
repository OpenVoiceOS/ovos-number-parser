from collections import OrderedDict
from math import floor

from ovos_number_parser.util import convert_to_mixed_fraction, is_numeric, look_for_fractions, Token, \
    ReplaceableNumber, tokenize, partition_list, invert_dict

_ARTICLES_FY = {'de', 'it'}

_NUM_STRING_FY = {
    0: 'nul',
    1: 'ien',
    2: 'twa',
    3: 'trije',
    4: 'fjouwer',
    5: 'fiif',
    6: 'seis',
    7: 'sân',
    8: 'acht',
    9: 'njoggen',
    10: 'tsien',
    11: 'alve',
    12: 'tolve',
    13: 'trettjin',
    14: 'fjirtjin',
    15: 'fyftjin',
    16: 'sechstjin',
    17: 'santjin',
    18: 'achttjin',
    19: 'njoggentjin',
    20: 'tweintich',
    30: 'tritich',
    40: 'fjirtich',
    50: 'fyftich',
    60: 'sechstich',
    70: 'santich',
    80: 'tachtich',
    90: 'njoggentich',
    100: 'hûndert'
}

_FRACTION_STRING_FY = {
    2: 'heal',
    3: 'tredde',
    4: 'fjirde',
    5: 'fyfte',
    6: 'sechste',
    7: 'sânde',
    8: 'achtste',
    9: 'njoggende',
    10: 'tsiende',
    11: 'alfde',
    12: 'tolfde',
    13: 'trettjinde',
    14: 'fjirtjinde',
    15: 'fyftjinde',
    16: 'sechstjinde',
    17: 'santjinde',
    18: 'achttjinde',
    19: 'njoggentjinde',
    20: 'tweintichste'
}

# West Frisian uses the long scale, alternating -joen and -jard suffixes
_LONG_SCALE_FY = OrderedDict([
    (100, 'hûndert'),
    (1000, 'tûzen'),
    (1000000, 'miljoen'),
    (1e12, 'biljoen'),
    (1e18, 'triljoen'),
])

_SHORT_SCALE_FY = OrderedDict([
    (100, 'hûndert'),
    (1000, 'tûzen'),
    (1000000, 'miljoen'),
    (1e9, 'miljard'),
    (1e12, 'biljoen'),
    (1e15, 'biljard'),
    (1e18, 'triljoen'),
    (1e21, 'triljard'),
])

_ORDINAL_STRING_BASE_FY = {
    1: 'earste',
    2: 'twadde',
    3: 'tredde',
    4: 'fjirde',
    5: 'fyfte',
    6: 'sechste',
    7: 'sânde',
    8: 'achtste',
    9: 'njoggende',
    10: 'tsiende',
    11: 'alfde',
    12: 'tolfde',
    13: 'trettjinde',
    14: 'fjirtjinde',
    15: 'fyftjinde',
    16: 'sechstjinde',
    17: 'santjinde',
    18: 'achttjinde',
    19: 'njoggentjinde',
    20: 'tweintichste',
    30: 'tritichste',
    40: 'fjirtichste',
    50: 'fyftichste',
    60: 'sechstichste',
    70: 'santichste',
    80: 'tachtichste',
    90: 'njoggentichste',
    1e2: 'hûndertste',
    1e3: 'tûzenste'
}

_SHORT_ORDINAL_STRING_FY = {
    1e6: 'miljoenste',
    1e9: 'miljardste',
    1e12: 'biljoenste',
    1e15: 'biljardste',
    1e18: 'triljoenste',
    1e21: 'triljardste'
}
_SHORT_ORDINAL_STRING_FY.update(_ORDINAL_STRING_BASE_FY)

_LONG_ORDINAL_STRING_FY = {
    1e6: 'miljoenste',
    1e12: 'biljoenste',
    1e18: 'triljoenste'
}
_LONG_ORDINAL_STRING_FY.update(_ORDINAL_STRING_BASE_FY)

# negate next number (-2 = 0 - 2)
_NEGATIVES_FY = {"min", "minus"}

# sum the next number (twenty two = 20 + 2)
_SUMS_FY = {'tweintich', '20', 'tritich', '30', 'fjirtich', '40',
            'fyftich', '50', 'sechstich', '60', 'santich', '70',
            'tachtich', '80', 'njoggentich', '90'}

_MULTIPLIES_LONG_SCALE_FY = set(_LONG_SCALE_FY.values())

_MULTIPLIES_SHORT_SCALE_FY = set(_SHORT_SCALE_FY.values())

# split sentence parse separately and sum ( 2 and a half = 2 + 0.5 )
_FRACTION_MARKER_FY = {"en"}

# decimal marker ( 1 komma 5 = 1 + 0.5)
_DECIMAL_MARKER_FY = {"komma", "punt"}

_STRING_NUM_FY = invert_dict(_NUM_STRING_FY)
_STRING_NUM_FY.update({
    # spellings without diacritics, common in ASR output
    "san": 7,
    "hundert": 100,
    "tuzen": 1000,
    # variant teen/ten spellings without the etymological -s-
    "sechtjin": 16,
    "sechtich": 60,
    "heal": 0.5,
})

_STRING_SHORT_ORDINAL_FY = invert_dict(_SHORT_ORDINAL_STRING_FY)
_STRING_LONG_ORDINAL_FY = invert_dict(_LONG_ORDINAL_STRING_FY)

# Numbers below 1 million are written in one word in West Frisian, just as
# in Dutch: units come before the tens, joined with "en" (ienentweintich)

_NUM_POWERS_OF_TEN_FY = [
    '', 'tûzen', 'miljoen', 'miljard', 'biljoen', 'biljard', 'triljoen',
    'triljard'
]

_EXTRA_SPACE_FY = ""


def nice_number_fy(number, speech=True, denominators=range(1, 21)):
    """ West Frisian helper for nice_number

    This function formats a float to a human understandable string. Like
    4.5 becomes "4 en in heal" for speech and "4 1/2" for text

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
            return str(whole)
        else:
            return '{} {}/{}'.format(whole, num, den)
    if num == 0:
        return str(whole)
    den_str = _FRACTION_STRING_FY[den]
    if whole == 0:
        if num == 1:
            return_string = 'ien {}'.format(den_str)
        else:
            return_string = '{} {}'.format(num, den_str)
    elif num == 1:
        return_string = '{} en ien {}'.format(whole, den_str)
    else:
        return_string = '{} en {} {}'.format(whole, num, den_str)

    return return_string


def pronounce_number_fy(number, places=2, short_scale=True, scientific=False,
                        ordinals=False):
    """
    Convert a number to its spoken West Frisian equivalent

    For example, '5.2' would return 'fiif komma twa'

    Args:
        number(float or int): the number to pronounce
        places(int): maximum decimal places to speak
        short_scale (bool) : use short (True) or long scale (False)
            https://en.wikipedia.org/wiki/Names_of_large_numbers
        scientific (bool): pronounce in scientific notation
        ordinals (bool): pronounce in ordinal form "first" instead of "one"
    Returns:
        (str): The pronounced number
    """
    if ordinals:
        return pronounce_ordinal_fy(number)

    def pronounce_triplet_fy(num):
        result = ""
        num = floor(num)
        if num > 99:
            hundreds = floor(num / 100)
            if hundreds > 0:
                result += _NUM_STRING_FY[hundreds] + _EXTRA_SPACE_FY + 'hûndert' + _EXTRA_SPACE_FY
                num -= hundreds * 100
        if num == 0:
            result += ''  # do nothing
        elif num <= 20:
            result += _NUM_STRING_FY[num]
        elif num > 20:
            ones = num % 10
            tens = num - ones
            if ones > 0:
                result += _NUM_STRING_FY[ones] + _EXTRA_SPACE_FY
                if tens > 0:
                    result += 'en' + _EXTRA_SPACE_FY
            if tens > 0:
                result += _NUM_STRING_FY[tens] + _EXTRA_SPACE_FY
        return result

    def pronounce_fractional_fy(num, places):
        # fixed number of places even with trailing zeros
        result = ""
        num = round(num, places)
        place = 10
        while places > 0:
            result += " " + _NUM_STRING_FY[int(num * place) % 10]
            place *= 10
            places -= 1
        return result

    def pronounce_whole_number_fy(num, scale_level=0):
        if num == 0:
            return ''

        num = floor(num)
        result = ''
        last_triplet = num % 1000

        if last_triplet == 1:
            if scale_level == 0:
                result += "ien"
            elif scale_level == 1:
                result += 'ien' + _EXTRA_SPACE_FY + 'tûzen' + _EXTRA_SPACE_FY
            else:
                result += "ien " + _NUM_POWERS_OF_TEN_FY[scale_level] + ' '
        elif last_triplet > 1:
            result += pronounce_triplet_fy(last_triplet)
            if scale_level == 1:
                result += 'tûzen' + _EXTRA_SPACE_FY
            if scale_level >= 2:
                result += " " + _NUM_POWERS_OF_TEN_FY[scale_level] + ' '

        num = floor(num / 1000)
        scale_level += 1
        return pronounce_whole_number_fy(num, scale_level) + result

    result = ""
    if abs(number) >= 1000000000000000000000000:  # cannot do more than this
        return str(number)
    elif number == 0:
        return str(_NUM_STRING_FY[0])
    elif number < 0:
        return "min " + pronounce_number_fy(abs(number), places)
    else:
        if number == int(number):
            return pronounce_whole_number_fy(number)
        else:
            whole_number_part = floor(number)
            fractional_part = number - whole_number_part
            result += pronounce_whole_number_fy(whole_number_part) or \
                _NUM_STRING_FY[0]
            if places > 0:
                result += " komma"
                result += pronounce_fractional_fy(fractional_part, places)
            return result


def pronounce_ordinal_fy(number):
    """
    This function pronounces a West Frisian number as an ordinal

    1 -> earste
    2 -> twadde

    Args:
        number (int): the number to format
    Returns:
        (str): The pronounced number string.
    """
    # only for whole positive numbers including zero
    if number < 0 or number != int(number):
        return number
    number = int(number)
    if number in _ORDINAL_STRING_BASE_FY:
        return _ORDINAL_STRING_BASE_FY[number]
    if number in _SHORT_ORDINAL_STRING_FY:
        return _SHORT_ORDINAL_STRING_FY[number]
    # compounds: cardinal + table-driven last element, mirroring the
    # cardinal compounding ("ienentweintich" -> "ienentweintichste").
    # zero has no compound tens element, so it takes the regular suffix
    # like the sibling Dutch "nulste"
    if 0 < number < 100:
        ones = number % 10
        tens = number - ones
        return _NUM_STRING_FY[ones] + "en" + _ORDINAL_STRING_BASE_FY[tens]
    return pronounce_number_fy(number) + "ste"


def numbers_to_digits_fy(text, short_scale=True, ordinals=False):
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
    text = text.lower().replace("û", "u").replace("â", "a") \
        .replace("ú", "u").replace("á", "a").replace("ê", "e") \
        .replace("ô", "o").replace("é", "e")
    text = _expand_compound_numbers_fy(text, short_scale)
    tokens = tokenize(text)
    numbers_to_replace = \
        _extract_numbers_with_text_fy(tokens, short_scale, ordinals)
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


def _extract_numbers_with_text_fy(tokens, short_scale=True,
                                  ordinals=False, fractional_numbers=True):
    """Extract all numbers from a list of Tokens, with the representing words.

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
            _extract_number_with_text_fy(tokens, short_scale,
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


def _extract_number_with_text_fy(tokens, short_scale=True,
                                 ordinals=False, fractional_numbers=True):
    """This function extracts a number from a list of Tokens.

    Args:
        tokens str: the string to normalize
        short_scale (bool): use short scale if True, long scale if False
        ordinals (bool): consider ordinal numbers, third=3 instead of 1/3
        fractional_numbers (bool): True if we should look for fractions and
                                   decimals.
    Returns:
        ReplaceableNumber
    """
    number, tokens = \
        _extract_number_with_text_fy_helper(tokens, short_scale,
                                            ordinals, fractional_numbers)
    while tokens and tokens[0].word in _ARTICLES_FY:
        tokens.pop(0)
    return ReplaceableNumber(number, tokens)


def _extract_number_with_text_fy_helper(tokens,
                                        short_scale=True, ordinals=False,
                                        fractional_numbers=True):
    """Helper for _extract_number_with_text_fy.

    This contains the real logic for parsing, but produces
    a result that needs a little cleaning (specific, it may
    contain leading articles that can be trimmed off).

    Args:
        tokens [Token]:
        short_scale boolean:
        ordinals boolean:
        fractional_numbers boolean:

    Returns:
        int or float, [Tokens]
    """
    if fractional_numbers:
        fraction, fraction_text = \
            _extract_fraction_with_text_fy(tokens, short_scale, ordinals)
        if fraction:
            return fraction, fraction_text

        decimal, decimal_text = \
            _extract_decimal_with_text_fy(tokens, short_scale, ordinals)
        if decimal:
            return decimal, decimal_text

    return _extract_whole_number_with_text_fy(tokens, short_scale, ordinals)


def _extract_fraction_with_text_fy(tokens, short_scale, ordinals):
    """Extract fraction numbers from a string.

    This function handles text such as '2 en 3/4'. Note that "ien heal" or
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
    for c in _FRACTION_MARKER_FY:
        partitions = partition_list(tokens, lambda t: t.word == c)

        if len(partitions) == 3:
            numbers1 = \
                _extract_numbers_with_text_fy(partitions[0], short_scale,
                                              ordinals, fractional_numbers=False)
            numbers2 = \
                _extract_numbers_with_text_fy(partitions[2], short_scale,
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


def _extract_decimal_with_text_fy(tokens, short_scale, ordinals):
    """Extract decimal numbers from a string.

    This function handles text such as '2 komma 5'.

    Notes:
        While this is a helper for extract_number_fy, it also depends on
        extract_number_fy, to parse out the components of the decimal.

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
    for c in _DECIMAL_MARKER_FY:
        partitions = partition_list(tokens, lambda t: t.word == c)

        if len(partitions) == 3:
            numbers1 = \
                _extract_numbers_with_text_fy(partitions[0], short_scale,
                                              ordinals, fractional_numbers=False)
            numbers2 = \
                _extract_numbers_with_text_fy(partitions[2], short_scale,
                                              ordinals, fractional_numbers=False)

            if not numbers1 or not numbers2:
                return None, None

            number = numbers1[-1]
            decimal = numbers2[0]
            # concatenate consecutive single digits after the marker
            # ("komma ien fjouwer" -> .14)
            _digits = ""
            _digit_tokens = []
            _prev_end = None
            for _num in numbers2:
                _v = _num.value
                if _v is None or _v is False or float(_v) != int(_v) \
                        or not 0 <= _v <= 9:
                    break
                if _prev_end is not None and _num.start_index != _prev_end + 1:
                    break
                _digits += str(int(_v))
                _digit_tokens.extend(_num.tokens)
                _prev_end = _num.end_index
            if len(_digits) > 1:
                _frac = float("0." + _digits)
                return (number.value - _frac if (number.value < 0 or any(_t.word.lower() in _NEGATIVES_FY for _t in number.tokens))
                        else number.value + _frac), \
                    number.tokens + partitions[1] + _digit_tokens

            if "." not in str(decimal.text):
                _frac2 = float('0.' + str(decimal.value))
                return (number.value - _frac2 if (number.value < 0 or any(_t.word.lower() in _NEGATIVES_FY for _t in number.tokens))
                        else number.value + _frac2), \
                       number.tokens + partitions[1] + decimal.tokens
    return None, None


def _extract_whole_number_with_text_fy(tokens, short_scale, ordinals):
    """Handle numbers not handled by the decimal or fraction functions.

    This is generally whole numbers. Note that phrases such as "ien heal" will
    be handled by this function, while "ien en in heal" is handled by the
    fraction function.

    Args:
        tokens [Token]:
        short_scale boolean:
        ordinals boolean:

    Returns:
        int or float, [Tokens]
        The value parsed, and tokens that it corresponds to.
    """
    multiplies, string_num_ordinal, string_num_scale = \
        _initialize_number_data_fy(short_scale)

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
        if word in _ARTICLES_FY or word in _NEGATIVES_FY:
            number_words.append(token)
            continue

        prev_word = tokens[idx - 1].word if idx > 0 else ""
        next_word = tokens[idx + 1].word if idx + 1 < len(tokens) else ""

        if word not in string_num_scale and \
                word not in _STRING_NUM_FY and \
                word not in _SUMS_FY and \
                word not in multiplies and \
                not (ordinals and word in string_num_ordinal) and \
                not is_numeric(word) and \
                not is_fractional_fy(word, short_scale=short_scale) and \
                not look_for_fractions(word.split('/')):
            words_only = [token.word for token in number_words]
            if number_words and not all([w in _ARTICLES_FY |
                                         _NEGATIVES_FY for w in words_only]):
                break
            else:
                number_words = []
                continue
        elif word not in multiplies \
                and prev_word not in multiplies \
                and prev_word not in _SUMS_FY \
                and not (ordinals and prev_word in string_num_ordinal) \
                and prev_word not in _NEGATIVES_FY \
                and prev_word not in _ARTICLES_FY:
            number_words = [token]
        elif prev_word in _SUMS_FY and word in _SUMS_FY:
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
        if word in _STRING_NUM_FY:
            val = _STRING_NUM_FY.get(word)
            current_val = val
        elif word in string_num_scale:
            val = string_num_scale.get(word)
            current_val = val
        elif ordinals and word in string_num_ordinal:
            val = string_num_ordinal[word]
            current_val = val

        # is the prev word an ordinal number and current word is one?
        if ordinals and prev_word in string_num_ordinal and val == 1:
            val = prev_val

        # is the prev word a number and should we sum it?
        if prev_word in _SUMS_FY and val and val < 10:
            if prev_val < 0:
                val = prev_val - val
            else:
                val = prev_val + val

        # is the prev word a number and should we multiply it?
        if word in multiplies:
            if not prev_val:
                prev_val = 1
            val = prev_val * val

        # is this a spoken fraction?
        if val is False:
            val = is_fractional_fy(word, short_scale=short_scale)
            current_val = val

        # 2 fifths
        if not ordinals:
            next_val = is_fractional_fy(next_word, short_scale=short_scale)
            if next_val:
                if not val:
                    val = 1
                val = val * next_val
                number_words.append(tokens[idx + 1])

        # is this a negative number?
        if val and prev_word and prev_word in _NEGATIVES_FY:
            val = 0 - val

        # let's make sure it isn't a fraction
        if not val:
            # look for fractions like "2/3"
            aPieces = word.split('/')
            if look_for_fractions(aPieces):
                val = float(aPieces[0]) / float(aPieces[1])
                current_val = val

        else:
            if prev_word in _SUMS_FY and word not in _SUMS_FY and current_val >= 10:
                # Backtrack - we've got numbers we can't sum.
                number_words.pop()
                val = prev_val
                break
            prev_val = val

            # handle long numbers
            if word in multiplies and next_word not in multiplies:
                to_sum.append(val)
                val = 0
                prev_val = 0

    if val is not None and to_sum:
        val += sum(to_sum)

    return val, number_words


def _initialize_number_data_fy(short_scale):
    """Generate dictionaries of words to numbers, based on scale.

    This is a helper function for _extract_whole_number.

    Args:
        short_scale boolean:

    Returns:
        (set(str), dict(str, number), dict(str, number))
        multiplies, string_num_ordinal, string_num_scale
    """
    multiplies = _MULTIPLIES_SHORT_SCALE_FY if short_scale \
        else _MULTIPLIES_LONG_SCALE_FY

    string_num_ordinal_fy = _STRING_SHORT_ORDINAL_FY if short_scale \
        else _STRING_LONG_ORDINAL_FY

    string_num_scale_fy = _SHORT_SCALE_FY if short_scale else _LONG_SCALE_FY
    string_num_scale_fy = invert_dict(string_num_scale_fy)

    return multiplies, string_num_ordinal_fy, string_num_scale_fy


def _split_compound_number_fy(word):
    """
    Split a West Frisian compound number word into its component number words.

    "ienentweintich" -> ["ien", "en", "tweintich"]
    "twahûnderttrijeentweintich" -> ["twa", "hûndert", "trije", "en", "tweintich"]

    Returns None if the word is not composed purely of known number words.
    """
    if word in _STRING_NUM_FY:
        return None
    keys = sorted(set(_STRING_NUM_FY) |
                  set(_MULTIPLIES_LONG_SCALE_FY) |
                  set(_MULTIPLIES_SHORT_SCALE_FY),
                  key=len, reverse=True)
    parts, rest = [], word
    while rest:
        if rest.startswith("en") and parts and rest != "en":
            candidate = rest[2:]
            if any(candidate.startswith(k) for k in keys):
                parts.append("en")
                rest = candidate
                continue
        for k in keys:
            if rest.startswith(k):
                parts.append(k)
                rest = rest[len(k):]
                break
        else:
            return None
    return parts if len(parts) > 1 else None


def _compound_value_fy(parts, short_scale=True):
    """Evaluate the numeric value of a split compound number word."""
    scale = _SHORT_SCALE_FY if short_scale else _LONG_SCALE_FY
    string_scale = invert_dict(scale)
    total = current = 0
    for p in parts:
        if p == "en":
            continue
        v = _STRING_NUM_FY.get(p)
        if v is None:
            v = string_scale.get(p)
        if v is None:
            return None
        if v >= 1000:
            total += max(current, 1) * v
            current = 0
        elif v == 100:
            current = max(current, 1) * 100
        else:
            current += v
    return total + current


def _expand_compound_numbers_fy(text, short_scale=True):
    """Rewrite compound number words as their digit value for parsing."""
    out = []
    for w in text.split():
        parts = _split_compound_number_fy(w)
        if parts:
            value = _compound_value_fy(parts, short_scale)
            out.append(str(value) if value is not None else w)
        else:
            out.append(w)
    return " ".join(out)


def extract_number_fy(text, short_scale=True, ordinals=False):
    """Extract a number from a West Frisian text string

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
    text = text.lower().replace("û", "u").replace("â", "a") \
        .replace("ú", "u").replace("á", "a").replace("ê", "e") \
        .replace("ô", "o").replace("é", "e")
    # normalize the words carrying diacritics to their plain spellings so
    # the compound splitter sees a single canonical form
    text = _expand_compound_numbers_fy(text, short_scale)
    return _extract_number_with_text_fy(tokenize(text),
                                        short_scale, ordinals).value


def is_fractional_fy(input_str, short_scale=True):
    """This function takes the given text and checks if it is a fraction.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): use short scale if True, long scale if False
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction
    """
    fracts = {"hiel": 1, "heal": 2, "healve": 2, "kwart": 4}
    if short_scale:
        for num in _SHORT_ORDINAL_STRING_FY:
            if num > 2:
                fracts[_SHORT_ORDINAL_STRING_FY[num]] = num
    else:
        for num in _LONG_ORDINAL_STRING_FY:
            if num > 2:
                fracts[_LONG_ORDINAL_STRING_FY[num]] = num

    if input_str.lower() in fracts:
        return 1.0 / fracts[input_str.lower()]
    return False
