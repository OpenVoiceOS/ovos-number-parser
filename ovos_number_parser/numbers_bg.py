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
from decimal import Decimal
from collections import OrderedDict

from ovos_number_parser.util import convert_to_mixed_fraction, invert_dict, scientific_parts
from ovos_number_parser import numtag_readers
from ovos_number_parser.util import warn_reader_removed

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
    (10 ** 3, 'хиляда'),
    (10 ** 6, 'милион'),
    (10 ** 9, 'милиард'),
    (10 ** 12, 'трилион'),
    (10 ** 15, 'квадрилион'),
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


_STRING_SCALE_BG = {}
for _value, _word in _SCALE_BG.items():
    _STRING_SCALE_BG[_word] = _value
    _STRING_SCALE_BG[_SCALE_PLURAL_BG[_word]] = _value


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
        n, power = scientific_parts(num, places)
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
        # a magnitude with no spoken name reads scientifically
        return result + pronounce_number_bg(
            num, places, short_scale, scientific=True)
    result += " ".join(whole_words)

    # deal with fractional part
    if not num == int(num) and places > 0:
        result += " запетая"
        _num_str = f"{Decimal(str(num)):f}".split(".")[1][0:places]
        for char in _num_str:
            result += " " + _NUM_STRING_BG[int(char)]
    return result


def extract_number_bg(text, short_scale=True, ordinals=False):
    """Deprecated: use ``ovos_number_parser.extract_number(text, "bg")``."""
    warn_reader_removed("extract_number_bg", 'ovos_number_parser.extract_number(text, "bg")')
    return numtag_readers.extract_number(text, "bg", short_scale, ordinals)
