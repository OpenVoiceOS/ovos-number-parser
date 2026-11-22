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
from decimal import Decimal
from math import floor

from ovos_number_parser import numtag_readers
from ovos_number_parser.util import (convert_to_mixed_fraction, Token, GrammaticalGender, warn_reader_removed)

_NUM_STRING_SV = {
    0: 'noll',
    1: 'en',
    2: 'två',
    3: 'tre',
    4: 'fyra',
    5: 'fem',
    6: 'sex',
    7: 'sju',
    8: 'åtta',
    9: 'nio',
    10: 'tio',
    11: 'elva',
    12: 'tolv',
    13: 'tretton',
    14: 'fjorton',
    15: 'femton',
    16: 'sexton',
    17: 'sjutton',
    18: 'arton',
    19: 'nitton',
    20: 'tjugo',
    30: 'trettio',
    40: 'fyrtio',
    50: 'femtio',
    60: 'sextio',
    70: 'sjuttio',
    80: 'åttio',
    90: 'nittio',
    100: 'hundra'
}

_NUM_POWERS_OF_TEN_SV = [
    'hundra',
    'tusen',
    'miljon',
    'miljard',
    'biljon',
    'biljard',
    'triljon',
    'triljard'
]

_FRACTION_STRING_SV = {
    2: 'halv',
    3: 'tredjedel',
    4: 'fjärdedel',
    5: 'femtedel',
    6: 'sjättedel',
    7: 'sjundedel',
    8: 'åttondel',
    9: 'niondel',
    10: 'tiondel',
    11: 'elftedel',
    12: 'tolftedel',
    13: 'trettondel',
    14: 'fjortondel',
    15: 'femtondel',
    16: 'sextondel',
    17: 'sjuttondel',
    18: 'artondel',
    19: 'nittondel',
    20: 'tjugondel'
}

_ORDINAL_STRING_SV = {
    0: 'nollte',
    1: 'första',
    2: 'andra',
    3: 'tredje',
    4: 'fjärde',
    5: 'femte',
    6: 'sjätte',
    7: 'sjunde',
    8: 'åttonde',
    9: 'nionde',
    10: 'tionde',
    11: 'elfte',
    12: 'tolfte',
    13: 'trettonde',
    14: 'fjortonde',
    15: 'femtonde',
    16: 'sextonde',
    17: 'sjuttonde',
    18: 'artonde',
    19: 'nittonde',
    20: 'tjugonde',
    30: 'trettionde',
    40: 'fyrtionde',
    50: 'femtionde',
    60: 'sextionde',
    70: 'sjuttionde',
    80: 'åttionde',
    90: 'nittionde',
    100: 'hundrade',
    1000: 'tusende',
    1000000: 'miljonte',
    1000000000: 'miljardte'
}

_EXTRA_SPACE_SV = " "


def nice_number_sv(number, speech=True, denominators=range(1, 21)):
    """ Swedish helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 och en halv" for speech and "4 1/2" for text

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
    den_str = _FRACTION_STRING_SV[den]
    if whole == 0:
        if num == 1:
            return_string = 'en {}'.format(den_str)
        else:
            return_string = '{} {}'.format(num, den_str)
    elif num == 1:
        return_string = '{} och en {}'.format(whole, den_str)
    else:
        return_string = '{} och {} {}'.format(whole, num, den_str)
    if num > 1:
        return_string += 'ar'
    return return_string


def pronounce_number_sv(number, places=2, short_scale=True, scientific=False,
                        ordinals=False, gender=GrammaticalGender.MASCULINE):
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
    Returns:
        (str): The pronounced number
    """

    # TODO short_scale, scientific and ordinals
    # currently ignored

    def pronounce_triplet_sv(num):
        result = ""
        num = floor(num)

        if num > 99:
            hundreds = floor(num / 100)
            if hundreds > 0:
                if hundreds == 1:
                    result += 'ett' + 'hundra'
                else:
                    result += _NUM_STRING_SV[hundreds] + 'hundra'

                num -= hundreds * 100

        if num == 0:
            result += ''  # do nothing
        elif num == 1:
            result += 'ett'
        elif num <= 20:
            result += _NUM_STRING_SV[num]
        elif num > 20:
            tens = num % 10
            ones = num - tens

            if ones > 0:
                result += _NUM_STRING_SV[ones]
            if tens > 0:
                # a bare cardinal ends in the neuter counting form: 21 is
                # "tjugoett", not "tjugoen" ("en" is the common-gender
                # attributive form, used only before a noun)
                result += 'ett' if tens == 1 else _NUM_STRING_SV[tens]

        return result

    def pronounce_fractional_sv(num, places):
        # fixed number of places even with trailing zeros
        result = ""
        for digit in f"{Decimal(str(num)):f}".split(".")[1][:places].ljust(places, "0"):
            result += " " + _NUM_STRING_SV[int(digit)]
        return result

    def pronounce_whole_number_sv(num, scale_level=0):
        if num == 0:
            return ''

        num = floor(num)
        result = ''
        last_triplet = num % 1000

        if last_triplet == 1:
            if scale_level == 0:
                # the counting form of 1 is "ett" (räkna: ett, två, tre),
                # not the common-gender "en"
                result += 'ett'
            elif scale_level == 1:
                result += 'ettusen' + _EXTRA_SPACE_SV
            else:
                result += 'en ' + \
                          _NUM_POWERS_OF_TEN_SV[scale_level] + _EXTRA_SPACE_SV
        elif last_triplet > 1:
            result += pronounce_triplet_sv(last_triplet)
            if scale_level == 1:
                result += 'tusen' + _EXTRA_SPACE_SV
            if scale_level >= 2:
                # miljon/miljard are separate words ("två miljoner"), unlike
                # the glued "tusen" ("tvåtusen")
                result += ' ' + _NUM_POWERS_OF_TEN_SV[scale_level]
                result += 'er' + _EXTRA_SPACE_SV  # MiljonER

        num //= 1000
        scale_level += 1
        return pronounce_whole_number_sv(num, scale_level) + result

    result = ""
    if abs(number) >= 1000000000000000000000000:  # cannot do more than this
        return str(number)
    elif number == 0:
        return str(_NUM_STRING_SV[0])
    elif number < 0:
        return "minus " + pronounce_number_sv(abs(number), places, gender=gender)
    else:
        if number == int(number):
            spoken = pronounce_whole_number_sv(number)
            # Swedish has one common gender, "en" (ICU RBNF sv
            # spellout-cardinal-reale and -feminine: "tjugoen", "ettusen en").
            # FEMININE selects it; MASCULINE is the default gender and keeps
            # the counting form "ett", as NEUTRAL does.
            if gender == GrammaticalGender.FEMININE and spoken.endswith("ett"):
                spoken = spoken[:-3] + "en"
            return spoken
        else:
            whole_number_part = floor(number)
            result += pronounce_whole_number_sv(whole_number_part) or \
                _NUM_STRING_SV[0]
            if places > 0:
                result += " komma"
                result += pronounce_fractional_sv(number, places)
            return result


def pronounce_ordinal_sv(number):
    """
    This function pronounces a number as an ordinal

    1 -> first
    2 -> second

    Args:
        number (int): the number to format
    Returns:
        (str): The pronounced number string.
    """

    # In Swedish only the final element of a compound is inflected as an
    # ordinal; the preceding magnitude words stay in their cardinal form
    # (121 -> "hundratjugoförsta"). This produces the base (uter) form, which
    # may need adaption for genus, kasus and numerus.

    if number < 0 or number != int(number):
        return number
    number = int(number)

    if number in _ORDINAL_STRING_SV:
        return _ORDINAL_STRING_SV[number]

    if number < 100:
        tens = number // 10 * 10
        ones = number % 10
        return _NUM_STRING_SV[tens] + _ORDINAL_STRING_SV[ones]

    if number < 1000:
        hundreds = number // 100
        rem = number % 100
        prefix = 'hundra' if hundreds == 1 \
            else _NUM_STRING_SV[hundreds] + 'hundra'
        if rem == 0:
            return prefix + 'de'
        return prefix + pronounce_ordinal_sv(rem)

    if number < 1000000:
        thousands = number // 1000
        rem = number % 1000
        prefix = 'tusen' if thousands == 1 \
            else pronounce_number_sv(thousands).replace(' ', '') + 'tusen'
        if rem == 0:
            return prefix + 'de'
        return prefix + pronounce_ordinal_sv(rem)

    if number >= 10 ** 24:
        raise NotImplementedError(
            f"cannot pronounce {number} as a Swedish ordinal")
    # the scale words come in pairs: miljon/miljard, biljon/biljard,
    # triljon/triljard
    scale_level = (len(str(number)) - 1) // 3
    scale = 10 ** (3 * scale_level)
    word = _NUM_POWERS_OF_TEN_SV[scale_level]
    count = number // scale
    rem = number % scale
    if rem == 0:
        prefix = word if count == 1 \
            else pronounce_number_sv(count).replace(' ', '') + word
        return prefix + 'te'
    # magnitude word stays cardinal; only the remainder is the ordinal
    return pronounce_number_sv(number - rem).strip() + ' ' \
        + pronounce_ordinal_sv(rem)


def _find_numbers_in_text(tokens):
    """Finds duration related numbers in texts and makes a list of mappings.

    The mapping will be for number to token that created it, if no number was
    created from the token the mapping will be from None to the token.

    The function is optimized to generate data that can be parsed to a duration
    so it returns the list in reverse order to make the "size" (minutes/hours/
    etc.) come first and the related numbers afterwards.

    Args:
        tokens: Tokens to parse

    Returns:
        list of (number, token) tuples
    """
    warn_reader_removed("_find_numbers_in_text", 'ovos_number_parser.extract_number_spans(text, "sv")')
    parts = []
    for tok in tokens:
        res = numtag_readers.extract_number(tok.word, "sv")
        if res:
            parts.insert(0, (res, tok))
            # Special case for quarter of an hour
            if tok.word == 'kvart':
                parts.insert(0, (None, Token('timmar', index=-1)))
        elif tok.word in ['halvtimme', 'halvtimma']:
            parts.insert(0, (30, tok))
            parts.insert(0, (None, Token('minuter', index=-1)))
        else:
            parts.insert(0, (None, tok))
    return parts


def _combine_adjacent_numbers(number_map):
    """Combine adjacent numbers through multiplication.

    Walks through a number map and joins adjasent numbers to handle cases
    such as "en halvtimme" (one half hour).

    Returns:
        (list): simplified number_map
    """
    simplified = []
    skip = False
    for i in range(len(number_map) - 1):
        if skip:
            skip = False
            continue
        if number_map[i][0] and number_map[i + 1][0]:
            combined_number = number_map[i][0] * number_map[i + 1][0]
            combined_tokens = (number_map[i][1], number_map[i + 1][1])
            simplified.append((combined_number, combined_tokens))
            skip = True
        else:
            simplified.append((number_map[i][0], (number_map[i][1],)))

    if not skip:
        simplified.append((number_map[-1][0], (number_map[-1][1],)))
    return simplified


