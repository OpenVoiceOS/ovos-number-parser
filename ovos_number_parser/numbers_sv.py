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
from math import floor

from ovos_number_parser.util import (convert_to_mixed_fraction, is_numeric, look_for_fractions, Token)

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
                        ordinals=False):
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
                result += _NUM_STRING_SV[tens]

        return result

    def pronounce_fractional_sv(num, places):
        # fixed number of places even with trailing zeros
        result = ""
        place = 10
        while places > 0:
            # doesn't work with 1.0001 and places = 2: int(
            # num*place) % 10 > 0 and places > 0:
            result += " " + _NUM_STRING_SV[int(num * place) % 10]
            place *= 10
            places -= 1
        return result

    def pronounce_whole_number_sv(num, scale_level=0):
        if num == 0:
            return ''

        num = floor(num)
        result = ''
        last_triplet = num % 1000

        if last_triplet == 1:
            if scale_level == 0:
                if result != '':
                    result += '' + 'ett'
                else:
                    result += 'en'
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
                result += _NUM_POWERS_OF_TEN_SV[scale_level]
            if scale_level >= 2:
                result += 'er' + _EXTRA_SPACE_SV  # MiljonER

        num = floor(num / 1000)
        scale_level += 1
        return pronounce_whole_number_sv(num, scale_level) + result

    result = ""
    if abs(number) >= 1000000000000000000000000:  # cannot do more than this
        return str(number)
    elif number == 0:
        return str(_NUM_STRING_SV[0])
    elif number < 0:
        return "minus " + pronounce_number_sv(abs(number), places)
    else:
        if number == int(number):
            return pronounce_whole_number_sv(number)
        else:
            whole_number_part = floor(number)
            fractional_part = number - whole_number_part
            result += pronounce_whole_number_sv(whole_number_part)
            if places > 0:
                result += " komma"
                result += pronounce_fractional_sv(fractional_part, places)
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

    # ordinals for 1, 3, 7 and 8 are irregular
    # this produces the base form, it will have to be adapted for genus,
    # casus, numerus

    ordinals = ["noll", "första", "andra", "tredje", "fjärde", "femte",
                "sjätte", "sjunde", "åttonde", "nionde", "tionde"]

    tens = int(floor(number / 10.0)) * 10
    ones = number % 10

    if number < 0 or number != int(number):
        return number
    if number == 0:
        return ordinals[number]

    result = ""
    if number > 10:
        result += pronounce_number_sv(tens).rstrip()

    if ones > 0:
        result += ordinals[ones]
    else:
        result += 'de'

    return result


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
    parts = []
    for tok in tokens:
        res = extract_number_sv(tok.word)
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


_STRING_NUM_SV = {v: k for k, v in _NUM_STRING_SV.items()}
_STRING_NUM_SV["ett"] = 1

_STRING_SCALE_SV = {
    "hundra": 100,
    "tusen": 1000,
    "miljon": 1000000,
    "miljoner": 1000000,
    "miljard": 1000000000,
    "miljarder": 1000000000,
    "biljon": 1000000000000,
    "biljoner": 1000000000000,
}

_ORDINAL_NUM_SV = {
    "första": 1, "andra": 2, "tredje": 3, "fjärde": 4, "femte": 5,
    "sjätte": 6, "sjunde": 7, "åttonde": 8, "nionde": 9, "tionde": 10,
    "elfte": 11, "tolfte": 12, "trettonde": 13, "fjortonde": 14,
    "femtonde": 15, "sextonde": 16, "sjuttonde": 17, "artonde": 18,
    "nittonde": 19, "tjugonde": 20, "trettionde": 30, "fyrtionde": 40,
    "femtionde": 50, "sextionde": 60, "sjuttionde": 70, "åttionde": 80,
    "nittionde": 90, "hundrade": 100, "tusende": 1000
}


def _split_compound_number_sv(word):
    """
    Split a Swedish compound number word into its component number words.

    "tjugoen" -> ["tjugo", "en"]
    "etthundratjugotre" -> ["ett", "hundra", "tjugo", "tre"]

    Returns None if the word is not composed purely of known number words.
    """
    if word in _STRING_NUM_SV or word in _STRING_SCALE_SV:
        return None
    keys = sorted(set(_STRING_NUM_SV) | set(_STRING_SCALE_SV),
                  key=len, reverse=True)
    parts, rest = [], word
    while rest:
        for k in keys:
            if rest.startswith(k):
                parts.append(k)
                rest = rest[len(k):]
                break
        else:
            return None
    return parts if len(parts) > 1 else None


def _compound_value_sv(parts):
    """Evaluate the numeric value of a split compound number word."""
    total = current = 0
    for p in parts:
        v = _STRING_NUM_SV.get(p)
        if v is None:
            v = _STRING_SCALE_SV.get(p)
            if v is None:
                return None
            if v >= 1000:
                total += max(current, 1) * v
                current = 0
            else:  # hundra
                current = max(current, 1) * 100
        elif v == 100:
            current = max(current, 1) * 100
        else:
            current += v
    return total + current


def _word_value_sv(word):
    """Value of a single (possibly compound) Swedish number word."""
    if word in _STRING_NUM_SV:
        return _STRING_NUM_SV[word]
    if word in _STRING_SCALE_SV:
        return _STRING_SCALE_SV[word]
    parts = _split_compound_number_sv(word)
    if parts:
        return _compound_value_sv(parts)
    return None


def _merge_values_sv(prev, nxt):
    """True if nxt is a lower-magnitude continuation of prev
    ("tvåtusen tjugotre" -> 2000 + 23)."""
    power = 10
    while power <= prev:
        if prev % power == 0 and nxt < power:
            return True
        power *= 10
    return False


def extract_number_sv(text, short_scale=True, ordinals=False):
    """
    This function prepares the given text for parsing by making
    numbers consistent, getting rid of contractions, etc.
    Args:
        text (str): the string to normalize
    Returns:
        (int) or (float): The value of extracted number
    """
    # TODO: short_scale and ordinals don't do anything here.
    # The parameters are present in the function signature for API
    # compatibility reasons.
    text = text.lower().replace("ettusen", "ett tusen")
    expanded = []
    for w in text.split():
        v = _word_value_sv(w)
        if v is not None:
            expanded.append(str(v))
        else:
            expanded.append(w)
    # merge lower-magnitude continuations ("2000 23" -> 2023)
    scales = {100, 1000, 1000000, 1000000000, 1000000000000}
    merged = []
    for w in expanded:
        if merged and w.isdigit() and merged[-1].isdigit():
            prev, nxt = int(merged[-1]), int(w)
            if nxt in scales and prev < nxt:
                # "två miljoner" -> 2 * 1000000
                merged[-1] = str(prev * nxt)
                continue
            if _merge_values_sv(prev, nxt):
                # "tvåtusen tjugotre" -> 2000 + 23
                merged[-1] = str(prev + nxt)
                continue
        merged.append(w)
    aWords = merged
    and_pass = False
    valPreAnd = False
    val = False
    count = 0
    while count < len(aWords):
        word = aWords[count]
        if is_numeric(word):
            val = float(word)
            if count + 1 < len(aWords):
                valNext = is_fractional_sv(aWords[count + 1])
                if valNext:
                    # "två och en halv" -> the "1" multiplies the fraction
                    val = val * valNext
                    aWords[count + 1] = ""
        elif word == "första":
            val = 1
        elif word == "andra":
            val = 2
        elif word == "tredje":
            val = 3
        elif word == "fjärde":
            val = 4
        elif word == "femte":
            val = 5
        elif word == "sjätte":
            val = 6
        elif is_fractional_sv(word):
            val = is_fractional_sv(word)
        else:
            if word == "en":
                val = 1
            if word == "ett":
                val = 1
            elif word == "två":
                val = 2
            elif word == "tre":
                val = 3
            elif word == "fyra":
                val = 4
            elif word == "fem":
                val = 5
            elif word == "sex":
                val = 6
            elif word == "sju":
                val = 7
            elif word == "åtta":
                val = 8
            elif word == "nio":
                val = 9
            elif word == "tio":
                val = 10
            if val:
                if count < (len(aWords) - 1):
                    wordNext = aWords[count + 1]
                else:
                    wordNext = ""
                valNext = is_fractional_sv(wordNext)

                if valNext:
                    val = val * valNext
                    aWords[count + 1] = ""

        if not val:
            # look for fractions like "2/3"
            aPieces = word.split('/')
            if look_for_fractions(aPieces):
                val = float(aPieces[0]) / float(aPieces[1])
            elif and_pass:
                # added to value, quit here
                val = valPreAnd
                break
            else:
                count += 1
                continue

        aWords[count] = ""

        if and_pass:
            aWords[count - 1] = ''  # remove "och"
            val += valPreAnd
        elif count + 1 < len(aWords) and aWords[count + 1] == 'och':
            and_pass = True
            valPreAnd = val
            val = False
            count += 2
            continue
        elif count + 2 < len(aWords) and aWords[count + 2] == 'och':
            and_pass = True
            valPreAnd = val
            val = False
            count += 3
            continue

        break

    return val or False


def is_fractional_sv(input_str, short_scale=True):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): use short scale if True, long scale if False
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    if input_str.endswith('ars', -3):
        input_str = input_str[:len(input_str) - 3]  # e.g. "femtedelar"
    if input_str.endswith('ar', -2):
        input_str = input_str[:len(input_str) - 2]  # e.g. "femtedelar"
    if input_str.endswith('a', -1):
        input_str = input_str[:len(input_str) - 1]  # e.g. "halva"
    if input_str.endswith('s', -1):
        input_str = input_str[:len(input_str) - 1]  # e.g. "halva"

    aFrac = ["hel", "halv", "tredjedel", "fjärdedel", "femtedel", "sjättedel",
             "sjundedel", "åttondel", "niondel", "tiondel", "elftedel",
             "tolftedel"]
    if input_str.lower() in aFrac:
        return 1.0 / (aFrac.index(input_str) + 1)
    if input_str == "kvart":
        return 1.0 / 4
    if input_str == "trekvart":
        return 3.0 / 4

    return False


def normalize_sv(text, remove_articles=True):
    words = text.split()  # this also removed extra spaces
    normalized = ''
    for word in words:
        # Convert numbers into digits, e.g. "two" -> "2"
        if word == 'en':
            word = 'ett'
        textNumbers = ["noll", "ett", "två", "tre", "fyra", "fem", "sex",
                       "sju", "åtta", "nio", "tio", "elva", "tolv",
                       "tretton", "fjorton", "femton", "sexton",
                       "sjutton", "arton", "nitton", "tjugo"]
        if word in textNumbers:
            word = str(textNumbers.index(word))

        normalized += " " + word

    return normalized[1:]  # strip the initial space
