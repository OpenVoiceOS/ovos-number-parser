# -*- coding: utf-8 -*-
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
import math
from collections import OrderedDict
from decimal import Decimal

from ovos_number_parser.util import (invert_dict, scientific_parts,
                                     round_half_up, Scale, warn_reader_removed)
from ovos_number_parser import numtag_readers


_NUM_STRING_EN = {
    0: 'zero',
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five',
    6: 'six',
    7: 'seven',
    8: 'eight',
    9: 'nine',
    10: 'ten',
    11: 'eleven',
    12: 'twelve',
    13: 'thirteen',
    14: 'fourteen',
    15: 'fifteen',
    16: 'sixteen',
    17: 'seventeen',
    18: 'eighteen',
    19: 'nineteen',
    20: 'twenty',
    30: 'thirty',
    40: 'forty',
    50: 'fifty',
    60: 'sixty',
    70: 'seventy',
    80: 'eighty',
    90: 'ninety'
}

_FRACTION_STRING_EN = {
    2: 'half',
    3: 'third',
    4: 'forth',
    5: 'fifth',
    6: 'sixth',
    7: 'seventh',
    8: 'eigth',
    9: 'ninth',
    10: 'tenth',
    11: 'eleventh',
    12: 'twelveth',
    13: 'thirteenth',
    14: 'fourteenth',
    15: 'fifteenth',
    16: 'sixteenth',
    17: 'seventeenth',
    18: 'eighteenth',
    19: 'nineteenth',
    20: 'twentyith'
}

_LONG_SCALE_EN = OrderedDict([
    (100, 'hundred'),
    (1000, 'thousand'),
    (1000000, 'million'),
    (1e12, "billion"),
    (1e18, 'trillion'),
    (1e24, "quadrillion"),
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

_SHORT_SCALE_EN = OrderedDict([
    (100, 'hundred'),
    (1000, 'thousand'),
    (1000000, 'million'),
    (1e9, "billion"),
    (1e12, 'trillion'),
    (1e15, "quadrillion"),
    (1e18, "quintillion"),
    (1e21, "sextillion"),
    (1e24, "septillion"),
    (1e27, "octillion"),
    (1e30, "nonillion"),
    (1e33, "decillion"),
    (1e36, "undecillion"),
    (1e39, "duodecillion"),
    (1e42, "tredecillion"),
    (1e45, "quattuordecillion"),
    (1e48, "quinquadecillion"),
    (1e51, "sedecillion"),
    (1e54, "septendecillion"),
    (1e57, "octodecillion"),
    (1e60, "novendecillion"),
    (1e63, "vigintillion"),
    (1e66, "unvigintillion"),
    (1e69, "uuovigintillion"),
    (1e72, "tresvigintillion"),
    (1e75, "quattuorvigintillion"),
    (1e78, "quinquavigintillion"),
    (1e81, "qesvigintillion"),
    (1e84, "septemvigintillion"),
    (1e87, "octovigintillion"),
    (1e90, "novemvigintillion"),
    (1e93, "trigintillion"),
    (1e96, "untrigintillion"),
    (1e99, "duotrigintillion"),
    (1e102, "trestrigintillion"),
    (1e105, "quattuortrigintillion"),
    (1e108, "quinquatrigintillion"),
    (1e111, "sestrigintillion"),
    (1e114, "septentrigintillion"),
    (1e117, "octotrigintillion"),
    (1e120, "noventrigintillion"),
    # Names from 10^123 to 10^303 follow the Conway-Wechsler system for the
    # short-scale "-illion" series, cross-checked against Wikipedia's "Names of
    # large numbers". The table is kept contiguous (one entry per 10^3 step) so
    # every finite magnitude a float can hold composes to a spoken name.
    (1e123, "quadragintillion"),
    (1e126, "unquadragintillion"),
    (1e129, "duoquadragintillion"),
    (1e132, "tresquadragintillion"),
    (1e135, "quattuorquadragintillion"),
    (1e138, "quinquadragintillion"),
    (1e141, "sesquadragintillion"),
    (1e144, "septenquadragintillion"),
    (1e147, "octoquadragintillion"),
    (1e150, "novenquadragintillion"),
    (1e153, "quinquagintillion"),
    (1e156, "unquinquagintillion"),
    (1e159, "duoquinquagintillion"),
    (1e162, "tresquinquagintillion"),
    (1e165, "quattuorquinquagintillion"),
    (1e168, "quinquinquagintillion"),
    (1e171, "sesquinquagintillion"),
    (1e174, "septenquinquagintillion"),
    (1e177, "octoquinquagintillion"),
    (1e180, "novenquinquagintillion"),
    (1e183, "sexagintillion"),
    (1e186, "unsexagintillion"),
    (1e189, "duosexagintillion"),
    (1e192, "tresexagintillion"),
    (1e195, "quattuorsexagintillion"),
    (1e198, "quinsexagintillion"),
    (1e201, "sesexagintillion"),
    (1e204, "septensexagintillion"),
    (1e207, "octosexagintillion"),
    (1e210, "novensexagintillion"),
    (1e213, "septuagintillion"),
    (1e216, "unseptuagintillion"),
    (1e219, "duoseptuagintillion"),
    (1e222, "treseptuagintillion"),
    (1e225, "quattuorseptuagintillion"),
    (1e228, "quinseptuagintillion"),
    (1e231, "seseptuagintillion"),
    (1e234, "septenseptuagintillion"),
    (1e237, "octoseptuagintillion"),
    (1e240, "novenseptuagintillion"),
    (1e243, "octogintillion"),
    (1e246, "unoctogintillion"),
    (1e249, "duooctogintillion"),
    (1e252, "treoctogintillion"),
    (1e255, "quattuoroctogintillion"),
    (1e258, "quinoctogintillion"),
    (1e261, "sexoctogintillion"),
    (1e264, "septemoctogintillion"),
    (1e267, "octooctogintillion"),
    (1e270, "novemoctogintillion"),
    (1e273, "nonagintillion"),
    (1e276, "unnonagintillion"),
    (1e279, "duononagintillion"),
    (1e282, "trenonagintillion"),
    (1e285, "quattuornonagintillion"),
    (1e288, "quinnonagintillion"),
    (1e291, "senonagintillion"),
    (1e294, "septenonagintillion"),
    (1e297, "octononagintillion"),
    (1e300, "novenonagintillion"),
    (1e303, "centillion"),
    (1e306, "uncentillion"),
    (1e309, "duocentillion"),
    (1e312, "trescentillion"),
    (1e333, "decicentillion"),
    (1e336, "undecicentillion"),
    (1e363, "viginticentillion"),
    (1e366, "unviginticentillion"),
    (1e393, "trigintacentillion"),
    (1e423, "quadragintacentillion"),
    (1e453, "quinquagintacentillion"),
    (1e483, "sexagintacentillion"),
    (1e513, "septuagintacentillion"),
    (1e543, "ctogintacentillion"),
    (1e573, "nonagintacentillion"),
    (1e603, "ducentillion"),
    (1e903, "trecentillion"),
    (1e1203, "quadringentillion"),
    (1e1503, "quingentillion"),
    (1e1803, "sescentillion"),
    (1e2103, "septingentillion"),
    (1e2403, "octingentillion"),
    (1e2703, "nongentillion"),
    (1e3003, "millinillion")
])

_ORDINAL_BASE_EN = {
    1: 'first',
    2: 'second',
    3: 'third',
    4: 'fourth',
    5: 'fifth',
    6: 'sixth',
    7: 'seventh',
    8: 'eighth',
    9: 'ninth',
    10: 'tenth',
    11: 'eleventh',
    12: 'twelfth',
    13: 'thirteenth',
    14: 'fourteenth',
    15: 'fifteenth',
    16: 'sixteenth',
    17: 'seventeenth',
    18: 'eighteenth',
    19: 'nineteenth',
    20: 'twentieth',
    30: 'thirtieth',
    40: "fortieth",
    50: "fiftieth",
    60: "sixtieth",
    70: "seventieth",
    80: "eightieth",
    90: "ninetieth",
    1e2: "hundredth",
    1e3: "thousandth"
}

_SHORT_ORDINAL_EN = {
    1e6: "millionth",
    1e9: "billionth",
    1e12: "trillionth",
    1e15: "quadrillionth",
    1e18: "quintillionth",
    1e21: "sextillionth",
    1e24: "septillionth",
    1e27: "octillionth",
    1e30: "nonillionth",
    1e33: "decillionth"
    # TODO > 1e-33
}
_SHORT_ORDINAL_EN.update(_ORDINAL_BASE_EN)

_LONG_ORDINAL_EN = {
    1e6: "millionth",
    1e12: "billionth",
    1e18: "trillionth",
    1e24: "quadrillionth",
    1e30: "quintillionth",
    1e36: "sextillionth",
    1e42: "septillionth",
    1e48: "octillionth",
    1e54: "nonillionth",
    1e60: "decillionth"
    # TODO > 1e60
}
_LONG_ORDINAL_EN.update(_ORDINAL_BASE_EN)


def _generate_plurals_en(originals):
    """
    Return a new set or dict containing the plural form of the original values,

    In English this means all with 's' appended to them.

    Args:
        originals set(str) or dict(str, any): values to pluralize

    Returns:
        set(str) or dict(str, any)

    """
    # TODO migrate to https://github.com/MycroftAI/lingua-franca/pull/36
    if isinstance(originals, dict):
        return {key + 's': value for key, value in originals.items()}
    return {value + "s" for value in originals}


_STRING_NUM_EN = invert_dict(_NUM_STRING_EN)
_STRING_NUM_EN.update(_generate_plurals_en(_STRING_NUM_EN))

_STRING_SHORT_ORDINAL_EN = invert_dict(_SHORT_ORDINAL_EN)
_STRING_LONG_ORDINAL_EN = invert_dict(_LONG_ORDINAL_EN)


def is_ordinal_en(input_str: str):
    """
    Check if the given text is an ordinal word.

    Returns:
        (bool) or (int/float): False if not an ordinal, otherwise the number
        corresponding to the ordinal
    """
    input_str = input_str.lower()
    if input_str in _STRING_LONG_ORDINAL_EN:
        return _STRING_LONG_ORDINAL_EN[input_str]
    if input_str in _STRING_SHORT_ORDINAL_EN:
        return _STRING_SHORT_ORDINAL_EN[input_str]
    return False


def pronounce_number_en(number, places=2, short_scale=True, scientific=False,
                        ordinals=False, year=False):
    """
    Convert a number to it's spoken equivalent

    For example, '5.2' would return 'five point two'

    Args:
        num(float or int): the number to pronounce (under 100)
        places(int): maximum decimal places to speak
        short_scale (bool) : use short (True) or long scale (False)
            https://en.wikipedia.org/wiki/Names_of_large_numbers
        scientific (bool): pronounce in scientific notation
        ordinals (bool): pronounce in ordinal form "first" instead of "one"
        year (bool): pronounce a 4-digit number in date style, e.g.
            1972 => "nineteen seventy two". Off by default so the spoken
            form of a plain number round-trips back to the same value.
    Returns:
        (str): The pronounced number
    """
    num = number
    # deal with infinity
    if num == float("inf"):
        return "infinity"
    elif num == float("-inf"):
        return "negative infinity"
    # Round (not truncate) the value to `places` decimals so the spoken form
    # matches the rounded number: half-away-from-zero per ISO 80000-1 and
    # NIST SP 811 (2008) B.7. Rounding here also carries into the integer part
    # ("zero point nine nine nine nine nine nine" at 2 places becomes "one")
    # and collapses a value that rounds to zero to a plain "zero".
    if not scientific and isinstance(num, float) and math.isfinite(num) \
            and num != int(num):
        num = float(round_half_up(Decimal(str(num)), places)) or 0.0
    if scientific:
        n, power = scientific_parts(num, places)
        if power != 0:
            if ordinals:
                # This handles negatives of powers separately from the normal
                # handling since each call disables the scientific flag
                return '{}{} times ten to the {}{} power'.format(
                    'negative ' if float(n) < 0 else '',
                    pronounce_number_en(
                        abs(float(n)), places, short_scale, False, ordinals=False),
                    'negative ' if power < 0 else '',
                    pronounce_number_en(abs(power), places, short_scale, False, ordinals=True))
            else:
                # This handles negatives of powers separately from the normal
                # handling since each call disables the scientific flag
                return '{}{} times ten to the power of {}{}'.format(
                    'negative ' if float(n) < 0 else '',
                    pronounce_number_en(
                        abs(float(n)), places, short_scale, False),
                    'negative ' if power < 0 else '',
                    pronounce_number_en(abs(power), places, short_scale, False))

    if short_scale:
        number_names = _NUM_STRING_EN.copy()
        number_names.update(_SHORT_SCALE_EN)
    else:
        number_names = _NUM_STRING_EN.copy()
        number_names.update(_LONG_SCALE_EN)

    digits = [number_names[n] for n in range(0, 20)]

    tens = [number_names[n] for n in range(10, 100, 10)]

    if short_scale:
        hundreds = [_SHORT_SCALE_EN[n] for n in _SHORT_SCALE_EN.keys()]
    else:
        hundreds = [_LONG_SCALE_EN[n] for n in _LONG_SCALE_EN.keys()]

    # deal with negatives
    result = ""
    if num < 0:
        result = "negative " if scientific else "minus "
    num = abs(num)

    if year and not ordinals:
        try:
            # deal with 4 digits
            # when explicitly asked for, say it like a date
            # i.e. 1972 => nineteen seventy two
            if len(str(num)) == 4 and isinstance(num, int):
                _num = str(num)
                # deal with 1000, 2000, 2001, 2100, 3123, etc
                # is skipped as the rest of the
                # functin deals with this already
                if _num[1:4] == '000' or _num[1:3] == '00' or int(_num[0:2]) >= 20:
                    pass
                # deal with 1900, 1300, etc
                # i.e. 1900 => nineteen hundred
                elif _num[2:4] == '00':
                    first = number_names[int(_num[0:2])]
                    last = number_names[100]
                    return first + " " + last
                # deal with 1960, 1961, etc
                # i.e. 1960 => nineteen sixty
                #      1961 => nineteen sixty one
                else:
                    first = number_names[int(_num[0:2])]
                    if _num[3:4] == '0':
                        last = number_names[int(_num[2:4])]
                    else:
                        second = number_names[int(_num[2:3]) * 10]
                        last = second + " " + number_names[int(_num[3:4])]
                    return first + " " + last
        # exception used to catch any unforseen edge cases
        # will default back to normal subroutine
        except Exception as e:
            # TODO this probably shouldn't go to stdout
            print('ERROR: Exception in pronounce_number_en: {}' + repr(e))

    # check for a direct match
    if ordinals and num == 0:
        result += "zeroth"
    elif ordinals and num == 100:
        # a round unit alone takes no "one", as "thousandth" and "millionth"
        result += _SHORT_ORDINAL_EN[100]
    elif num in number_names and not ordinals:
        if num > 90:
            result += "one "
        result += number_names[num]
    else:
        def _sub_thousand(n, ordinals=False):
            assert 0 <= n <= 999
            if n < 100 and n in _SHORT_ORDINAL_EN and ordinals:
                return _SHORT_ORDINAL_EN[n]
            if n <= 19:
                return digits[n]
            elif n <= 99:
                q, r = divmod(n, 10)
                return tens[q - 1] + (" " + _sub_thousand(r, ordinals) if r
                                      else "")
            else:
                q, r = divmod(n, 100)
                if r:
                    return digits[q] + " hundred and " + _sub_thousand(r, ordinals)
                return digits[q] + (" hundredth" if ordinals else " hundred")

        def _short_scale(n):
            # A finite value above the largest named scale returns "" so the
            # caller reads it scientifically; "infinity" is reserved for the
            # actual math.inf case handled at the top of pronounce_number_en.
            if n >= max(_SHORT_SCALE_EN.keys()):
                return ""
            ordi = ordinals

            if int(n) != n:
                ordi = False
            n = int(n)
            assert 0 <= n
            res = []
            for i, z in enumerate(_split_by(n, 1000)):
                if not z:
                    continue
                number = _sub_thousand(z, not i and ordi)

                if i:
                    if i >= len(hundreds):
                        return ""
                    number += " "
                    if ordi:

                        if 1000 ** i in _SHORT_ORDINAL_EN:
                            if z == 1 and n == 1000 ** i:
                                number = _SHORT_ORDINAL_EN[1000 ** i]
                            else:
                                number += _SHORT_ORDINAL_EN[1000 ** i]
                        else:
                            if n not in _SHORT_SCALE_EN:
                                num = int("1" + "0" * (len(str(n)) - 2))

                                number += _SHORT_SCALE_EN[num] + "th"
                            else:
                                number = _SHORT_SCALE_EN[n] + "th"
                    else:
                        number += hundreds[i]
                res.append(number)
                ordi = False

            return ", ".join(reversed(res))

        def _split_by(n, split=1000):
            assert 0 <= n
            res = []
            while n:
                n, r = divmod(n, split)
                res.append(r)
            return res

        def _long_scale(n):
            # See _short_scale: a finite value beyond the largest named scale
            # returns "" for a scientific fallback, never the infinity word.
            if n >= max(_LONG_SCALE_EN.keys()):
                return ""
            ordi = ordinals
            if int(n) != n:
                ordi = False
            n = int(n)
            assert 0 <= n
            res = []
            for i, z in enumerate(_split_by(n, 1000000)):
                if not z:
                    continue
                number = pronounce_number_en(z, places, True, scientific,
                                             ordinals=ordi and not i)
                if ordi and not i and z != n \
                        and number in ("hundredth", "thousandth"):
                    # the bare form is for the round unit alone
                    number = "one " + number
                # strip off the comma after the thousand
                if i:
                    if i >= len(hundreds):
                        return ""
                    # plus one as we skip 'thousand'
                    # (and 'hundred', but this is excluded by index value)
                    number = number.replace(',', '')

                    if ordi:
                        if 1000000 ** i in _LONG_ORDINAL_EN:
                            if z == 1 and n == 1000000 ** i:
                                number = _LONG_ORDINAL_EN[1000000 ** i]
                            else:
                                number += " " + _LONG_ORDINAL_EN[1000000 ** i]
                        else:
                            if n not in _LONG_SCALE_EN:
                                num = int("1" + "0" * (len(str(n)) - 2))

                                number += " " + _LONG_SCALE_EN[
                                    num] + "th"
                            else:
                                number = " " + _LONG_SCALE_EN[n] + "th"
                    else:

                        number += " " + hundreds[i + 1]
                res.append(number)
                ordi = False
            return ", ".join(reversed(res))

        if short_scale:
            result += _short_scale(num)
        else:
            result += _long_scale(num)

    # deal with a magnitude that has no spoken name: read it scientifically
    # (covers floats in "e" notation and very large ints alike) so a finite
    # value never returns an empty string.
    if result in ("", "minus ") and num >= 1e6:
        # the scientific reading speaks its own sign word
        return pronounce_number_en(
            -num if result else num, places, short_scale, scientific=True)
    # Deal with fractional part
    elif not num == int(num) and places > 0:
        if abs(num) < 1.0 and (result == "minus " or not result):
            result += "zero"
        result += " point"
        _num_str = f"{Decimal(str(num)):f}"
        _num_str = _num_str.split(".")[1][0:places]
        for char in _num_str:
            result += " " + number_names[int(char)]
    return result


def is_fractional_en(input_str, short_scale=True, spoken=True):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): use short scale if True, long scale if False
        spoken (bool): consider "half", "quarter", "whole" a fraction
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    if input_str.endswith('s', -1):
        input_str = input_str[:len(input_str) - 1]  # e.g. "fifths"

    fracts = {"whole": 1, "half": 2, "halve": 2, "quarter": 4}
    if short_scale:
        for num in _SHORT_ORDINAL_EN:
            if num > 2:
                fracts[_SHORT_ORDINAL_EN[num]] = num
    else:
        for num in _LONG_ORDINAL_EN:
            if num > 2:
                fracts[_LONG_ORDINAL_EN[num]] = num

    if input_str.lower() in fracts and spoken:
        return 1.0 / fracts[input_str.lower()]
    return False


def numbers_to_digits_en(text, short_scale=True, ordinals=False):
    """Deprecated: use ``ovos_number_parser.numbers_to_digits(text, "en")``."""
    warn_reader_removed("numbers_to_digits_en", 'ovos_number_parser.numbers_to_digits(text, "en")')
    return numtag_readers.numbers_to_digits(text, "en", Scale.SHORT if short_scale else Scale.LONG, ordinals)
