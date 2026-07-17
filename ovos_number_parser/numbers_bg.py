#
# Copyright 2017 Mycroft AI Inc.
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
"""Bulgarian number parsing and pronunciation.

Bulgarian is analytic: cardinal numerals do not decline for case, which keeps
both directions simple. The conjunction "и" is inserted before the last
element of a compound number ("двадесет и едно" = 21, "сто двадесет и три"
= 123, "сто и пет" = 105).

Spelling-variant policy: the contracted colloquial forms of the teens and
tens ("единайсет", "двайсет", "трийсет", "четирийсет", "шейсет") are accepted
when parsing, but pronunciation always produces the full standard forms
("единадесет", "двадесет", "тридесет", "четиридесет", "шестдесет").
"""
from collections import OrderedDict

from ovos_number_parser.util import convert_to_mixed_fraction, is_numeric, look_for_fractions, \
    invert_dict, ReplaceableNumber, partition_list, tokenize, Token

_NUM_STRING_BG = {
    0: 'нула',
    1: 'едно',
    2: 'две',
    3: 'три',
    4: 'четири',
    5: 'пет',
    6: 'шест',
    7: 'седем',
    8: 'осем',
    9: 'девет',
    10: 'десет',
    11: 'единадесет',
    12: 'дванадесет',
    13: 'тринадесет',
    14: 'четиринадесет',
    15: 'петнадесет',
    16: 'шестнадесет',
    17: 'седемнадесет',
    18: 'осемнадесет',
    19: 'деветнадесет',
    20: 'двадесет',
    30: 'тридесет',
    40: 'четиридесет',
    50: 'петдесет',
    60: 'шестдесет',
    70: 'седемдесет',
    80: 'осемдесет',
    90: 'деветдесет',
    100: 'сто',
    200: 'двеста',
    300: 'триста',
    400: 'четиристотин',
    500: 'петстотин',
    600: 'шестстотин',
    700: 'седемстотин',
    800: 'осемстотин',
    900: 'деветстотин'
}

# gender-marked low numerals (masculine, feminine, neuter)
_GENDERED_UNITS_BG = {
    1: {'m': 'един', 'f': 'една', 'n': 'едно'},
    2: {'m': 'два', 'f': 'две', 'n': 'две'},
}

# contracted colloquial spellings, accepted in parsing only
_VARIANT_NUM_BG = {
    'единайсет': 11,
    'дванайсет': 12,
    'тринайсет': 13,
    'четиринайсет': 14,
    'петнайсет': 15,
    'шестнайсет': 16,
    'седемнайсет': 17,
    'осемнайсет': 18,
    'деветнайсет': 19,
    'двайсет': 20,
    'трийсет': 30,
    'четирийсет': 40,
    'шейсет': 60,
}

# thousands and the international scale words with their count forms
_SCALE_BG = OrderedDict([
    (1e3, 'хиляда'),
    (1e6, 'милион'),
    (1e9, 'милиард'),
    (1e12, 'трилион'),
    (1e15, 'квадрилион'),
])

_SCALE_PLURAL_BG = {
    'хиляда': 'хиляди',
    'милион': 'милиона',
    'милиард': 'милиарда',
    'трилион': 'трилиона',
    'квадрилион': 'квадрилиона',
}

_ORDINAL_BG = {
    1: 'първи',
    2: 'втори',
    3: 'трети',
    4: 'четвърти',
    5: 'пети',
    6: 'шести',
    7: 'седми',
    8: 'осми',
    9: 'девети',
    10: 'десети',
    11: 'единадесети',
    12: 'дванадесети',
    13: 'тринадесети',
    14: 'четиринадесети',
    15: 'петнадесети',
    16: 'шестнадесети',
    17: 'седемнадесети',
    18: 'осемнадесети',
    19: 'деветнадесети',
    20: 'двадесети',
    30: 'тридесети',
    40: 'четиридесети',
    50: 'петдесети',
    60: 'шестдесети',
    70: 'седемдесети',
    80: 'осемдесети',
    90: 'деветдесети',
    100: 'стотен',
    1000: 'хиляден',
    1000000: 'милионен',
}

_VARIANT_ORDINAL_BG = {
    'единайсети': 11,
    'дванайсети': 12,
    'тринайсети': 13,
    'четиринайсети': 14,
    'петнайсети': 15,
    'шестнайсети': 16,
    'седемнайсети': 17,
    'осемнайсети': 18,
    'деветнайсети': 19,
    'двайсети': 20,
    'трийсети': 30,
    'четирийсети': 40,
    'шейсети': 60,
}

# feminine ordinal used as the fraction denominator ("една пета" = 1/5)
_FRACTION_STRING_BG = {
    2: 'половина',
    3: 'трета',
    4: 'четвърт',
    5: 'пета',
    6: 'шеста',
    7: 'седма',
    8: 'осма',
    9: 'девета',
    10: 'десета',
    11: 'единадесета',
    12: 'дванадесета',
    13: 'тринадесета',
    14: 'четиринадесета',
    15: 'петнадесета',
    16: 'шестнадесета',
    17: 'седемнадесета',
    18: 'осемнадесета',
    19: 'деветнадесета',
    20: 'двадесета',
    30: 'тридесета',
    40: 'четиридесета',
    50: 'петдесета',
    60: 'шестдесета',
    70: 'седемдесета',
    80: 'осемдесета',
    90: 'деветдесета',
    1e2: 'стотна',
    1e3: 'хилядна',
    1e6: 'милионна',
    1e9: 'милиардна',
}

# negate next number (-2 = 0 - 2)
_NEGATIVES_BG = {"минус"}

# words that a following number is summed onto (двадесет и три = 20 + 3)
_SUMS_BG = {'двадесет', 'двайсет', '20', 'тридесет', 'трийсет', '30',
            'четиридесет', 'четирийсет', '40', 'петдесет', '50',
            'шестдесет', 'шейсет', '60', 'седемдесет', '70',
            'осемдесет', '80', 'деветдесет', '90',
            'сто', '100', 'двеста', '200', 'триста', '300',
            'четиристотин', '400', 'петстотин', '500', 'шестстотин', '600',
            'седемстотин', '700', 'осемстотин', '800', 'деветстотин', '900'}

_STRING_SCALE_BG = {}
for _value, _word in _SCALE_BG.items():
    _STRING_SCALE_BG[_word] = _value
    _STRING_SCALE_BG[_SCALE_PLURAL_BG[_word]] = _value

_MULTIPLIES_BG = set(_STRING_SCALE_BG.keys())

# the conjunction joining the last element of a compound number
_JOINERS_BG = {"и"}

# split sentence, parse separately and sum (две и половина = 2 + 0.5)
_FRACTION_MARKER_BG = {"и"}

# decimal marker (пет запетая две = 5.2, пет цяло и две = 5.2)
_DECIMAL_MARKER_BG = {"запетая", "цяло"}

_STRING_NUM_BG = invert_dict(_NUM_STRING_BG)
_STRING_NUM_BG.update(_VARIANT_NUM_BG)
_STRING_NUM_BG.update({
    "един": 1,
    "една": 1,
    "два": 2,
    "чифт": 2,
    "половина": 0.5,
    "половин": 0.5,
    "четвърт": 0.25,
})

_STRING_ORDINAL_BG = invert_dict(_ORDINAL_BG)
_STRING_ORDINAL_BG.update(_VARIANT_ORDINAL_BG)


def _sub_thousand_bg(n, gender='n'):
    """Words for 1..999, with "и" before the last element."""
    assert 0 < n <= 999
    words = []
    q, r = divmod(n, 100)
    if q:
        words.append(_NUM_STRING_BG[q * 100])
    if r:
        if r < 20:
            if r in _GENDERED_UNITS_BG:
                words.append(_GENDERED_UNITS_BG[r][gender])
            else:
                words.append(_NUM_STRING_BG[r])
        else:
            t, u = divmod(r, 10)
            words.append(_NUM_STRING_BG[t * 10])
            if u:
                if u in _GENDERED_UNITS_BG:
                    words.append(_GENDERED_UNITS_BG[u][gender])
                else:
                    words.append(_NUM_STRING_BG[u])
    if len(words) > 1:
        words.insert(len(words) - 1, "и")
    return words


def _int_bg(n):
    """Words for a non-negative integer, or None if out of range."""
    if n == 0:
        return [_NUM_STRING_BG[0]]
    scale_names = list(_SCALE_BG.values())
    groups = []  # low to high, chunks of 1000
    while n:
        n, r = divmod(n, 1000)
        groups.append(r)
    word_groups = []
    for i, z in enumerate(groups):
        if not z:
            continue
        if i == 0:
            g = _sub_thousand_bg(z, 'n')
        elif i == 1:
            if z == 1:
                g = ['хиляда']
            else:
                g = _sub_thousand_bg(z, 'f') + ['хиляди']
        else:
            if i - 1 >= len(scale_names):
                return None
            scale_word = scale_names[i - 1]
            if z == 1:
                g = ['един', scale_word]
            else:
                g = _sub_thousand_bg(z, 'm') + [_SCALE_PLURAL_BG[scale_word]]
        word_groups.append(g)
    word_groups.reverse()
    # "и" before the final group when it is a single word
    # (хиляда и едно = 1001, хиляда и сто = 1100)
    if len(word_groups) > 1 and len(word_groups[-1]) == 1:
        word_groups[-1] = ["и"] + word_groups[-1]
    return [w for g in word_groups for w in g]


def _ordinal_bg(n):
    """Masculine ordinal words for a positive integer.

    Only the last element takes the ordinal form
    ("двадесет и първи" = 21st).
    """
    n = int(n)
    if n <= 0:
        raise ValueError(f"Cannot pronounce ordinal for: {n}")
    if n in _ORDINAL_BG:
        return _ORDINAL_BG[n]
    if n < 100:
        t, u = divmod(n, 10)
        return f"{_NUM_STRING_BG[t * 10]} и {_ORDINAL_BG[u]}"
    if n < 1000:
        q, r = divmod(n, 100)
        if not r:
            raise ValueError(f"Cannot pronounce ordinal for: {n}")
        rest = _ordinal_bg(r)
        joiner = " " if " " in rest else " и "
        return _NUM_STRING_BG[q * 100] + joiner + rest
    if n < 1e9:
        q, r = divmod(n, 1000)
        if not r:
            raise ValueError(f"Cannot pronounce ordinal for: {n}")
        prefix_words = _int_bg(n - r)
        if prefix_words is None:
            raise ValueError(f"Cannot pronounce ordinal for: {n}")
        rest = _ordinal_bg(r)
        joiner = " " if " " in rest else " и "
        return " ".join(prefix_words) + joiner + rest
    raise ValueError(f"Cannot pronounce ordinal for: {n}")


def nice_number_bg(number, speech=True, denominators=range(1, 21)):
    """Bulgarian helper for nice_number

    This function formats a float to a human understandable string. Like
    4.5 becomes "четири и половина" for speech and "4 1/2" for text.

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
            return str(whole)
        else:
            return '{} {}/{}'.format(whole, num, den)

    if num == 0:
        return str(whole)
    den_str = _FRACTION_STRING_BG[den]
    if num > 1:
        # plural of the fraction noun (трета -> трети, четвърт -> четвърти)
        if den_str.endswith('а'):
            den_str = den_str[:-1] + 'и'
        else:
            den_str += 'и'
    if whole == 0:
        if num == 1:
            if den == 2:
                return_string = den_str
            else:
                return_string = 'една {}'.format(den_str)
        else:
            return_string = '{} {}'.format(num, den_str)
    elif num == 1 and den == 2:
        return_string = '{} и половина'.format(whole)
    else:
        return_string = '{} и {} {}'.format(whole, num, den_str)
    return return_string


def pronounce_number_bg(number, places=2, short_scale=True, scientific=False,
                        ordinals=False):
    """
    Convert a number to it's spoken equivalent

    For example, '5.2' would return 'пет запетая две'

    Args:
        number(float or int): the number to pronounce
        places(int): maximum decimal places to speak
        short_scale (bool): Bulgarian uses a single (short) scale; the
                            argument is accepted for API parity
        scientific (bool): pronounce in scientific notation
        ordinals (bool): pronounce in ordinal form "първи" instead of "едно"
    Returns:
        (str): The pronounced number
    """
    num = number
    # deal with infinity
    if num == float("inf"):
        return "безкрайност"
    elif num == float("-inf"):
        return "минус безкрайност"
    if scientific:
        number = '%E' % num
        n, power = number.replace("+", "").split("E")
        power = int(power)
        if power != 0:
            return '{}{} по десет на степен {}{}'.format(
                'минус ' if float(n) < 0 else '',
                pronounce_number_bg(abs(float(n)), places, short_scale, False),
                'минус ' if power < 0 else '',
                pronounce_number_bg(abs(power), places, short_scale, False))

    result = ""
    if num < 0:
        result = "минус "
    num = abs(num)

    if ordinals and num == int(num):
        return result + _ordinal_bg(int(num))

    whole_words = _int_bg(int(num))
    if whole_words is None:
        return "безкрайност"
    result += " ".join(whole_words)

    # deal with fractional part
    if not num == int(num) and places > 0:
        result += " запетая"
        _num_str = str(num).split(".")[1][0:places]
        for char in _num_str:
            result += " " + _NUM_STRING_BG[int(char)]
    return result


def numbers_to_digits_bg(text, short_scale=True, ordinals=False):
    """
    Convert words in a string into their equivalent numbers.
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
        _extract_numbers_with_text_bg(tokens, short_scale, ordinals)
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


def _extract_numbers_with_text_bg(tokens, short_scale=True,
                                  ordinals=False, fractional_numbers=True):
    """
    Extract all numbers from a list of Tokens, with the words that
    represent them.

    Args:
        [Token]: The tokens to parse.
        short_scale bool: ignored, Bulgarian uses a single scale
        ordinals bool: True if ordinal words (първи, втори, ...) should
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
            _extract_number_with_text_bg(tokens, short_scale,
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


def _extract_number_with_text_bg(tokens, short_scale=True,
                                 ordinals=False, fractional_numbers=True):
    """
    This function extracts a number from a list of Tokens.

    Args:
        tokens [Token]: the tokens to parse
        short_scale (bool): ignored, Bulgarian uses a single scale
        ordinals (bool): consider ordinal numbers, трети=3 instead of 1/3
        fractional_numbers (bool): True if we should look for fractions and
                                   decimals.
    Returns:
        ReplaceableNumber

    """
    number, tokens = \
        _extract_number_with_text_bg_helper(tokens, short_scale,
                                            ordinals, fractional_numbers)
    return ReplaceableNumber(number, tokens)


def _extract_number_with_text_bg_helper(tokens,
                                        short_scale=True, ordinals=False,
                                        fractional_numbers=True):
    """
    Helper for _extract_number_with_text_bg.

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
            _extract_fraction_with_text_bg(tokens, short_scale, ordinals)
        if fraction:
            return fraction, fraction_text

        decimal, decimal_text = \
            _extract_decimal_with_text_bg(tokens, short_scale, ordinals)
        if decimal:
            return decimal, decimal_text

    return _extract_whole_number_with_text_bg(tokens, short_scale, ordinals)


def _extract_fraction_with_text_bg(tokens, short_scale, ordinals):
    """
    Extract fraction numbers from a string ("две и половина" = 2.5).

    Args:
        tokens [Token]: words and their indexes in the original string.
        short_scale boolean:
        ordinals boolean:

    Returns:
        (int or float, [Token])
        The value found, and the list of relevant tokens.
        (None, None) if no fraction value is found.

    """
    for c in _FRACTION_MARKER_BG:
        partitions = partition_list(tokens, lambda t: t.word == c)

        if len(partitions) == 3:
            numbers1 = \
                _extract_numbers_with_text_bg(partitions[0], short_scale,
                                              ordinals, fractional_numbers=False)
            numbers2 = \
                _extract_numbers_with_text_bg(partitions[2], short_scale,
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


def _extract_decimal_with_text_bg(tokens, short_scale, ordinals):
    """
    Extract decimal numbers from a string ("пет запетая две" = 5.2).

    Args:
        tokens [Token]: The text to parse.
        short_scale boolean:
        ordinals boolean:

    Returns:
        (float, [Token])
        The value found and relevant tokens.
        (None, None) if no decimal value is found.

    """
    for c in _DECIMAL_MARKER_BG:
        partitions = partition_list(tokens, lambda t: t.word == c)

        if len(partitions) == 3:
            numbers1 = \
                _extract_numbers_with_text_bg(partitions[0], short_scale,
                                              ordinals, fractional_numbers=False)
            numbers2 = \
                _extract_numbers_with_text_bg(partitions[2], short_scale,
                                              ordinals, fractional_numbers=False)

            if not numbers1 or not numbers2:
                return None, None

            number = numbers1[-1]
            decimal = numbers2[0]
            # concatenate consecutive single digits after the marker
            # ("запетая едно четири" -> .14)
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
                return (number.value - _frac if number.value < 0
                        else number.value + _frac), \
                    number.tokens + partitions[1] + _digit_tokens

            if "." not in str(decimal.text) and \
                    float(decimal.value) == int(decimal.value):
                _frac2 = float('0.' + str(int(decimal.value)))
                return (number.value - _frac2 if number.value < 0
                        else number.value + _frac2), \
                       number.tokens + partitions[1] + decimal.tokens
    return None, None


def _extract_whole_number_with_text_bg(tokens, short_scale, ordinals):
    """
    Handle numbers not handled by the decimal or fraction functions.

    Args:
        tokens [Token]:
        short_scale boolean:
        ordinals boolean:

    Returns:
        int or float, [Tokens]
        The value parsed, and tokens that it corresponds to.

    """
    # the conjunction "и" joins the last element of a compound number
    # ("двадесет и три" = 23); drop it so the summing logic sees
    # adjacent number words. Original token indices are preserved.
    tokens = [t for t in tokens if t.word not in _JOINERS_BG]

    number_words = []  # type: [Token]
    val = False
    prev_val = None
    next_val = None
    negative = False
    to_sum = []
    for idx, token in enumerate(tokens):
        current_val = None
        if next_val:
            next_val = None
            continue

        word = token.word
        if word in _NEGATIVES_BG:
            negative = True
            number_words.append(token)
            continue

        prev_word = tokens[idx - 1].word if idx > 0 else ""
        next_word = tokens[idx + 1].word if idx + 1 < len(tokens) else ""

        # explicit ordinals written as digits with a period (1., 2., ...)
        if is_numeric(word[:-1]) and word.endswith("."):
            word = word[:-1]

        if word not in _STRING_SCALE_BG and \
                word not in _STRING_NUM_BG and \
                word not in _SUMS_BG and \
                word not in _MULTIPLIES_BG and \
                not (ordinals and word in _STRING_ORDINAL_BG) and \
                not is_numeric(word) and \
                not is_fractional_bg(word, short_scale=short_scale) and \
                not look_for_fractions(word.split('/')):
            words_only = [token.word for token in number_words]
            if number_words and not all([w in _NEGATIVES_BG for w in words_only]):
                break
            else:
                number_words = []
                continue
        elif word not in _MULTIPLIES_BG \
                and prev_word not in _MULTIPLIES_BG \
                and prev_word not in _SUMS_BG \
                and not (ordinals and prev_word in _STRING_ORDINAL_BG) \
                and prev_word not in _NEGATIVES_BG:
            number_words = [token]
        elif prev_word in _SUMS_BG and word in _SUMS_BG:
            number_words = [token]
        else:
            number_words.append(token)

        # is this word already a number?
        if is_numeric(word):
            if word.isdigit():  # doesn't work with decimals
                val = int(word)
            else:
                val = float(word)
            current_val = val

        # is this word the name of a number?
        if word in _STRING_NUM_BG:
            val = _STRING_NUM_BG.get(word)
            current_val = val
        elif word in _STRING_SCALE_BG:
            val = _STRING_SCALE_BG.get(word)
            current_val = val
        elif ordinals and word in _STRING_ORDINAL_BG:
            val = _STRING_ORDINAL_BG[word]
            current_val = val

        # is the prev word a number and should we sum it?
        # двадесет [и] три, сто [и] пет
        if (prev_word in _SUMS_BG and val and val < 10) \
                or (prev_word in _SUMS_BG and val and val < 100 and prev_val >= 100) \
                or all([prev_word in _MULTIPLIES_BG, val < prev_val if prev_val else False]):
            if prev_val < 0:
                # continue a negated number: "минус четиридесет и две" = -(40+2)
                val = prev_val - val
            else:
                val = prev_val + val

        # is the prev word a number and should we multiply it?
        # две хиляди, три милиона
        if word in _MULTIPLIES_BG:
            if not prev_val:
                prev_val = 1
            val = prev_val * val

        # is this a spoken fraction? половин чаша
        if val is False:
            val = is_fractional_bg(word, short_scale=short_scale)
            current_val = val

        # две трети
        if not ordinals:
            next_val = is_fractional_bg(next_word, short_scale=short_scale)
            if next_val:
                if not val:
                    val = 1
                val = val * next_val
                number_words.append(tokens[idx + 1])

        # the sign is applied once to the whole number after parsing,
        # so no per-token negation happens here

        # let's make sure it isn't a fraction
        if not val:
            # look for fractions like "2/3"
            a_pieces = word.split('/')
            if look_for_fractions(a_pieces):
                val = float(a_pieces[0]) / float(a_pieces[1])
        else:
            if all([
                prev_word in _SUMS_BG,
                word not in _SUMS_BG,
                word not in _MULTIPLIES_BG,
                current_val >= 10,
                # teens continue a preceding hundred ("сто и десет" = 110)
                not (prev_val and prev_val >= 100 and current_val < 100)
            ]):
                # Backtrack - we've got numbers we can't sum.
                number_words.pop()
                val = prev_val
                break
            prev_val = val

            if word in _MULTIPLIES_BG and next_word not in _MULTIPLIES_BG:
                # handle long numbers, e.g.
                # две хиляди петстотин двадесет и три
                # look ahead: if all remaining scale words are smaller,
                # this chunk is complete and can be set aside to sum later
                time_to_sum = True
                for other_token in tokens[idx + 1:]:
                    if other_token.word in _MULTIPLIES_BG:
                        if _STRING_SCALE_BG[other_token.word] >= current_val:
                            time_to_sum = False
                        else:
                            continue
                    if not time_to_sum:
                        break
                if time_to_sum:
                    to_sum.append(val)
                    val = 0
                    prev_val = 0

    if val is not None and to_sum:
        val += sum(to_sum)
    if negative and val not in (None, False):
        val = -val

    return val, number_words


def extract_number_bg(text, short_scale=True, ordinals=False):
    """
    This function extracts a number from a text string

    Args:
        text (str): the string to normalize
        short_scale (bool): ignored, Bulgarian uses a single scale
        ordinals (bool): consider ordinal numbers, трети=3 instead of 1/3
    Returns:
        (int) or (float) or False: The extracted number or False if no number
                                   was found

    """
    value = _extract_number_with_text_bg(tokenize(text.lower()),
                                         short_scale, ordinals).value
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    return value


def is_fractional_bg(input_str, short_scale=True):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): ignored, Bulgarian uses a single scale
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    fractions = {"цяло": 1, "половин": 2, "третина": 3, "четвъртина": 4}
    for num, word in _FRACTION_STRING_BG.items():
        fractions[word] = num
        # plural (трета -> трети, четвърт -> четвърти)
        if word.endswith('а'):
            fractions[word[:-1] + 'и'] = num
        else:
            fractions[word + 'и'] = num

    if input_str.lower() in fractions:
        return 1.0 / fractions[input_str.lower()]
    return False
