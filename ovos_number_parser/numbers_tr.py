#
# Copyright 2021 Mycroft AI Inc.
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
"""Turkish number parsing and formatting.

Turkish numerals compound with spaces ("yirmi bir" = 21), omit "bir"
before "yüz" and "bin" ("yüz" = 100, "bin" = 1000) and only use the
short scale ("milyar" = 1e9). The decimal separator is spoken "virgül"
(comma). Fractions use the locative denominator ("üçte bir" = 1/3) plus
the special words "yarım" (a standalone half), "buçuk" (a half after a
number: "bir buçuk" = 1.5) and "çeyrek" (a quarter).
"""
import re
from collections import OrderedDict

from ovos_number_parser.util import (invert_dict, convert_to_mixed_fraction, tokenize, look_for_fractions,
                                     partition_list, is_numeric, Token, ReplaceableNumber)

_NUM_STRING_TR = {
    0: 'sıfır',
    1: 'bir',
    2: 'iki',
    3: 'üç',
    4: 'dört',
    5: 'beş',
    6: 'altı',
    7: 'yedi',
    8: 'sekiz',
    9: 'dokuz',
    10: 'on',
    11: 'on bir',
    12: 'on iki',
    13: 'on üç',
    14: 'on dört',
    15: 'on beş',
    16: 'on altı',
    17: 'on yedi',
    18: 'on sekiz',
    19: 'on dokuz',
    20: 'yirmi',
    30: 'otuz',
    40: 'kırk',
    50: 'elli',
    60: 'altmış',
    70: 'yetmiş',
    80: 'seksen',
    90: 'doksan'
}

# locative denominators: "üçte bir" = 1/3, "dörtte üç" = 3/4
_FRACTION_STRING_TR = {
    2: 'ikide',
    3: 'üçte',
    4: 'dörtte',
    5: 'beşte',
    6: 'altıda',
    7: 'yedide',
    8: 'sekizde',
    9: 'dokuzda',
    10: 'onda',
    11: 'on birde',
    12: 'on ikide',
    13: 'on üçte',
    14: 'on dörtte',
    15: 'on beşte',
    16: 'on altıda',
    17: 'on yedide',
    18: 'on sekizde',
    19: 'on dokuzda',
    20: 'yirmide',
    30: 'otuzda',
    40: 'kırkta',
    50: 'ellide',
    60: 'altmışta',
    70: 'yetmişte',
    80: 'seksende',
    90: 'doksanda',
    1e2: 'yüzde',
    1e3: 'binde'
}

# Turkish only uses the short scale (TDK: milyar = 10^9); the long-scale
# table mirrors it so both Scale values behave identically.
_SHORT_SCALE_TR = OrderedDict([
    (100, 'yüz'),
    (1000, 'bin'),
    (1000000, 'milyon'),
    (1e9, "milyar"),
    (1e12, 'trilyon'),
    (1e15, "katrilyon"),
    (1e18, "kentilyon"),
    (1e21, "sekstilyon"),
    (1e24, "septilyon"),
    (1e27, "oktilyon"),
    (1e30, "nonilyon"),
    (1e33, "desilyon")
])

_LONG_SCALE_TR = _SHORT_SCALE_TR

_ORDINAL_BASE_TR = {
    1: 'birinci',
    2: 'ikinci',
    3: 'üçüncü',
    4: 'dördüncü',
    5: 'beşinci',
    6: 'altıncı',
    7: 'yedinci',
    8: 'sekizinci',
    9: 'dokuzuncu',
    10: 'onuncu',
    11: 'on birinci',
    12: 'on ikinci',
    13: 'on üçüncü',
    14: 'on dördüncü',
    15: 'on beşinci',
    16: 'on altıncı',
    17: 'on yedinci',
    18: 'on sekizinci',
    19: 'on dokuzuncu',
    20: 'yirminci',
    30: 'otuzuncu',
    40: "kırkıncı",
    50: "ellinci",
    60: "altmışıncı",
    70: "yetmişinci",
    80: "sekseninci",
    90: "doksanıncı",
    1e2: "yüzüncü",
    1e3: "bininci"
}

_SHORT_ORDINAL_TR = {
    1e6: "milyonuncu",
    1e9: "milyarıncı",
    1e12: "trilyonuncu",
    1e15: "katrilyonuncu",
    1e18: "kentilyonuncu",
    1e21: "sekstilyonuncu",
    1e24: "septilyonuncu",
    1e27: "oktilyonuncu",
    1e30: "nonilyonuncu",
    1e33: "desilyonuncu"
}
_SHORT_ORDINAL_TR.update(_ORDINAL_BASE_TR)

_LONG_ORDINAL_TR = _SHORT_ORDINAL_TR

# negate next number (-2 = 0 - 2)
_NEGATIVES_TR = {"eksi", "negatif"}

# sum the next number (yirmi bir = 20 + 1)
_SUMS_TR = {'on', '10', 'yirmi', '20', 'otuz', '30', 'kırk', '40', 'elli', '50',
            'altmış', '60', 'yetmiş', '70', 'seksen', '80', 'doksan', '90'}

_HARD_VOWELS = ['a', 'ı', 'o', 'u']
_SOFT_VOWELS = ['e', 'i', 'ö', 'ü']
_VOWELS = _HARD_VOWELS + _SOFT_VOWELS


def _get_last_vowel(word):
    is_last = True
    for char in word[::-1]:
        if char in _VOWELS:
            return char, is_last
        is_last = False

    return "", is_last


def _last_vowel_type(word):
    return _get_last_vowel(word)[0] in _HARD_VOWELS


def _get_ordinal_ak(word):
    """Ordinal suffix (-ıncı/-inci/-uncu/-üncü) by vowel harmony."""
    last_vowel, is_last = _get_last_vowel(word)
    if not last_vowel:
        return ""

    if last_vowel in ["a", "ı"]:
        if is_last:
            return "ncı"
        return "ıncı"

    if last_vowel in ["e", "i"]:
        if is_last:
            return "nci"
        return "inci"

    if last_vowel in ["o", "u"]:
        if is_last:
            return "ncu"
        return "uncu"

    if last_vowel in ["ö", "ü"]:
        if is_last:
            return "ncü"
        return "üncü"


def _generate_plurals_tr(originals):
    """
    Return a new set or dict containing the plural form of the original values,

    In Turkish this means appending 'lar' or 'ler' to them according to the last vowel in word.

    Args:
        originals set(str) or dict(str, any): values to pluralize

    Returns:
        set(str) or dict(str, any)

    """

    if isinstance(originals, dict):
        return {key + ('lar' if _last_vowel_type(key) else 'ler'): value for key, value in originals.items()}
    return {value + ('lar' if _last_vowel_type(value) else 'ler') for value in originals}


_MULTIPLIES_SHORT_SCALE_TR = set(_SHORT_SCALE_TR.values())

_MULTIPLIES_LONG_SCALE_TR = _MULTIPLIES_SHORT_SCALE_TR

# split sentence parse separately and sum ( 2 and a half = 2 + 0.5 )
_FRACTION_MARKER_TR = {"ve"}

# decimal marker ( 1 virgül 5 = 1 + 0.5 )
_DECIMAL_MARKER_TR = {"virgül", "nokta"}

_STRING_NUM_TR = invert_dict(_NUM_STRING_TR)

_SPOKEN_EXTRA_NUM_TR = {
    "yarım": 0.5,
    "buçuk": 0.5,
    "çeyrek": 0.25
}

_STRING_SHORT_ORDINAL_TR = invert_dict(_SHORT_ORDINAL_TR)
_STRING_LONG_ORDINAL_TR = invert_dict(_LONG_ORDINAL_TR)


def nice_number_tr(number, speech=True, denominators=range(1, 21)):
    """ Turkish helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 buçuk" for speech and "4 1/2" for text

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
    den_str = _FRACTION_STRING_TR[den]
    if whole == 0:
        if den == 2:
            return 'yarım'
        if den == 4 and num == 1:
            return 'çeyrek'
        return '{} {}'.format(den_str, num)
    if den == 2:
        # "bir buçuk" = 1.5
        return '{} buçuk'.format(whole)
    return '{} ve {} {}'.format(whole, den_str, num)


def pronounce_number_tr(number, places=2, short_scale=True, scientific=False,
                        ordinals=False):
    """
    Convert a number to it's spoken equivalent

    For example, '5.2' would return 'beş virgül iki'

    Args:
        num(float or int): the number to pronounce (under 100)
        places(int): maximum decimal places to speak
        short_scale (bool) : ignored — Turkish only uses the short scale
        scientific (bool): pronounce in scientific notation
        ordinals (bool): pronounce in ordinal form "first" instead of "one"
    Returns:
        (str): The pronounced number
    """
    num = number
    # deal with infinity
    if num == float("inf"):
        return "sonsuzluk"
    elif num == float("-inf"):
        return "eksi sonsuzluk"
    if scientific:
        number = '%E' % num
        n, power = number.replace("+", "").split("E")
        power = int(power)
        if power != 0:
            # This handles negatives of powers separately from the normal
            # handling since each call disables the scientific flag
            return '{}{} çarpı on üzeri {}{}'.format(
                'eksi ' if float(n) < 0 else '',
                pronounce_number_tr(
                    abs(float(n)), places, short_scale, False, ordinals=False),
                'eksi ' if power < 0 else '',
                pronounce_number_tr(abs(power), places, short_scale, False,
                                    ordinals=ordinals))

    number_names = _NUM_STRING_TR.copy()
    number_names.update(_SHORT_SCALE_TR)

    digits = [number_names[n] for n in range(0, 20)]

    tens = [number_names[n] for n in range(10, 100, 10)]

    hundreds = [_SHORT_SCALE_TR[n] for n in _SHORT_SCALE_TR.keys()]

    # deal with negatives
    result = ""
    if num < 0:
        result = "eksi "
    num = abs(num)

    # check for a direct match
    if num in number_names and not ordinals:
        # "bin" (not "bir bin") but "bir milyon"
        if num > 1000:
            result += "bir "
        result += number_names[num]
    else:
        def _sub_thousand(n, ordinals=False):
            assert 0 <= n <= 999
            if n in _SHORT_ORDINAL_TR and ordinals:
                return _SHORT_ORDINAL_TR[n]
            if n <= 19:
                return digits[n]
            elif n <= 99:
                q, r = divmod(n, 10)
                return tens[q - 1] + (" " + _sub_thousand(r, ordinals) if r
                                      else "")
            else:
                q, r = divmod(n, 100)
                # "yüz" (not "bir yüz") but "iki yüz"
                return (digits[q] + " " if q != 1 else "") + "yüz" + (
                    " " + _sub_thousand(r, ordinals) if r else "")

        def _short_scale(n):
            if n >= 999 * max(_SHORT_SCALE_TR.keys()):
                return "sonsuzluk"
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
                        if i * 1000 in _SHORT_ORDINAL_TR:
                            if z == 1:
                                number = _SHORT_ORDINAL_TR[i * 1000]
                            else:
                                number += _SHORT_ORDINAL_TR[i * 1000]
                        else:
                            if n not in _SHORT_SCALE_TR:
                                num = int("1" + "0" * (len(str(n)) - 2))

                                number += _SHORT_SCALE_TR[num] + _get_ordinal_ak(_SHORT_SCALE_TR[num])
                            else:
                                number = _SHORT_SCALE_TR[n] + _get_ordinal_ak(_SHORT_SCALE_TR[n])
                    else:
                        number += hundreds[i]
                # "bin" (not "bir bin")
                if number.startswith("bir bin"):
                    number = number[4:]
                res.append(number)
                ordi = False

            return " ".join(reversed(res))

        def _split_by(n, split=1000):
            assert 0 <= n
            res = []
            while n:
                n, r = divmod(n, split)
                res.append(r)
            return res

        result += _short_scale(num)

    # deal with scientific notation unpronounceable as number
    if not result and "e" in str(num):
        return pronounce_number_tr(num, places, short_scale, scientific=True)
    # Deal with fractional part
    elif not num == int(num) and places > 0:
        if abs(num) < 1.0 and (result == "eksi " or not result):
            result += "sıfır"
        result += " virgül"
        _num_str = str(num)
        _num_str = _num_str.split(".")[1][0:places]
        for char in _num_str:
            result += " " + number_names[int(char)]
    return result


def pronounce_ordinal_tr(number):
    """
    Pronounce an ordinal number in Turkish, e.g. 1 -> "birinci".
    """
    if number != int(number) or number < 1:
        raise ValueError("ordinals must be positive integers")
    return pronounce_number_tr(int(number), ordinals=True)


def numbers_to_digits_tr(text, short_scale=True, ordinals=False):
    """
    Convert words in a string into their equivalent numbers.
    Args:
        text str:
        short_scale boolean: ignored — Turkish only uses the short scale
        ordinals boolean: True if ordinals (e.g. birinci, ikinci, üçüncü) should
                          be parsed to their number values (1, 2, 3...)

    Returns:
        str
        The original text, with numbers subbed in where appropriate.

    """
    tokens = tokenize(text)
    numbers_to_replace = \
        _extract_numbers_with_text_tr(tokens, short_scale, ordinals)

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


def _extract_numbers_with_text_tr(tokens, short_scale=True,
                                  ordinals=False, fractional_numbers=True):
    """
    Extract all numbers from a list of Tokens, with the words that
    represent them.

    Args:
        [Token]: The tokens to parse.
        short_scale bool: ignored — Turkish only uses the short scale
        ordinals bool: True if ordinal words (birinci, ikinci, üçüncü, etc)
                       should be parsed.
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
            _extract_number_with_text_tr(tokens, short_scale,
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


def _extract_number_with_text_tr(tokens, short_scale=True,
                                 ordinals=False, fractional_numbers=True):
    """
    This function extracts a number from a list of Tokens.

    Args:
        tokens str: the string to normalize
        short_scale (bool): ignored — Turkish only uses the short scale
        ordinals (bool): consider ordinal numbers
        fractional_numbers (bool): True if we should look for fractions and
                                   decimals.
    Returns:
        ReplaceableNumber

    """
    number, tokens = \
        _extract_number_with_text_tr_helper(tokens, short_scale,
                                            ordinals, fractional_numbers)
    return ReplaceableNumber(number, tokens)


def _extract_number_with_text_tr_helper(tokens,
                                        short_scale=True, ordinals=False,
                                        fractional_numbers=True):
    """
    Helper for _extract_number_with_text_tr.

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
            _extract_fraction_with_text_tr(tokens, short_scale, ordinals)
        if fraction:
            return fraction, fraction_text

        decimal, decimal_text = \
            _extract_decimal_with_text_tr(tokens, short_scale, ordinals)
        if decimal:
            return decimal, decimal_text

    return _extract_whole_number_with_text_tr(tokens, short_scale, ordinals)


def _extract_fraction_with_text_tr(tokens, short_scale, ordinals):
    """
    Extract fraction numbers from a string.

    This function handles text such as '2 ve dörtte üç'. Note that "yarım" or
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
    for c in _FRACTION_MARKER_TR:
        partitions = partition_list(tokens, lambda t: t.word == c)

        if len(partitions) == 3:
            numbers1 = \
                _extract_numbers_with_text_tr(partitions[0], short_scale,
                                              ordinals, fractional_numbers=False)
            numbers2 = \
                _extract_numbers_with_text_tr(partitions[2], short_scale,
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


def _extract_decimal_with_text_tr(tokens, short_scale, ordinals):
    """
    Extract decimal numbers from a string.

    This function handles text such as '2 virgül 5'.

    Notes:
        While this is a helper for extract_number_tr, it also depends on
        extract_number_tr, to parse out the components of the decimal.

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
    for c in _DECIMAL_MARKER_TR:
        partitions = partition_list(tokens, lambda t: t.word == c)

        if len(partitions) == 3:
            numbers1 = \
                _extract_numbers_with_text_tr(partitions[0], short_scale,
                                              ordinals, fractional_numbers=False)
            numbers2 = \
                _extract_numbers_with_text_tr(partitions[2], short_scale,
                                              ordinals, fractional_numbers=False)
            if not numbers1 or not numbers2:
                return None, None

            number = numbers1[-1]
            decimal = numbers2[0]
            # concatenate consecutive single digits after the marker
            # ("virgül bir dört" -> .14)
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

            # TODO handle number dot number number number
            if "." not in str(decimal.text):
                _frac2 = float('0.' + str(decimal.value))
                return (number.value - _frac2 if number.value < 0
                        else number.value + _frac2), \
                       number.tokens + partitions[1] + decimal.tokens
    return None, None


def _extract_whole_number_with_text_tr(tokens, short_scale, ordinals):
    """
    Handle numbers not handled by the decimal or fraction functions. This is
    generally whole numbers. Note that phrases such as "yarım" will be
    handled by this function.

    Args:
        tokens [Token]:
        short_scale boolean:
        ordinals boolean:

    Returns:
        int or float, [Tokens]
        The value parsed, and tokens that it corresponds to.

    """
    multiplies, string_num_ordinal, string_num_scale = \
        _initialize_number_data_tr(short_scale, speech=ordinals is not None)

    number_words = []  # type: List[Token]
    val = False
    prev_val = None
    next_val = None
    to_sum = []
    for idx, token in enumerate(tokens):
        current_val = None
        if next_val:
            next_val = None
            continue

        word = token.word.lower()
        if word in _NEGATIVES_TR:
            number_words.append(token)
            continue

        prev_word = tokens[idx - 1].word.lower() if idx > 0 else ""
        next_word = tokens[idx + 1].word.lower() if idx + 1 < len(tokens) else ""
        if word not in string_num_scale and \
                word not in _STRING_NUM_TR and \
                word not in _SUMS_TR and \
                word not in multiplies and \
                not (ordinals and word in string_num_ordinal) and \
                not is_numeric(word) and \
                not is_fractional_tr(word, short_scale=short_scale) and \
                not look_for_fractions(word.split('/')):
            words_only = [token.word for token in number_words]

            if number_words and not all([w.lower() in
                                         _NEGATIVES_TR for w in words_only]):
                break
            else:
                number_words = []
                continue
        elif word not in multiplies \
                and word not in _SPOKEN_EXTRA_NUM_TR \
                and prev_word not in multiplies \
                and prev_word not in _SUMS_TR \
                and not (ordinals and prev_word in string_num_ordinal) \
                and prev_word not in _NEGATIVES_TR:
            number_words = [token]
        elif prev_word in _SUMS_TR and word in _SUMS_TR:
            number_words = [token]
        elif ordinals is None and \
                (word in string_num_ordinal or word in _SPOKEN_EXTRA_NUM_TR):
            # flagged to ignore this token
            continue
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
        if word in _STRING_NUM_TR:
            val = _STRING_NUM_TR.get(word)
            current_val = val
        elif word in string_num_scale:
            val = string_num_scale.get(word)
            current_val = val
        elif ordinals and word in string_num_ordinal:
            val = string_num_ordinal[word]
            current_val = val
        # is the prev word a number and should we sum it?
        # yirmi iki, elli altı
        if (prev_word in _SUMS_TR and val and val < 10) or all([prev_word in
                                                                multiplies,
                                                                val < prev_val if prev_val else False]):
            if prev_val < 0:
                # continue a negated number: "eksi kırk iki" = -(40+2)
                val = prev_val - val
            else:
                val = prev_val + val

        # is the prev word a number and should we multiply it?
        # yirmi bin, altı yüz
        if word in multiplies:
            if not prev_val:
                prev_val = 1
            if current_val is None or prev_val < current_val:
                val = prev_val * val
            # else: the scale word is smaller than what came before it, so it
            # opens a new addend ("bin yüz" = 1000 + 100) already accumulated
            # by the summing branch above rather than a multiplier

        # is this a spoken fraction?
        # bir buçuk fincan - yarım fincan
        if current_val is None and not (ordinals is None and word in _SPOKEN_EXTRA_NUM_TR):
            val = is_fractional_tr(word, short_scale=short_scale,
                                   spoken=ordinals is not None)
            if val:
                if prev_val:
                    val += prev_val
                current_val = val
                if word in _SPOKEN_EXTRA_NUM_TR:
                    break

        # dörtte bir
        if ordinals is False:
            temp = prev_val
            prev_val = is_fractional_tr(prev_word, short_scale=short_scale)
            if prev_val:
                if not val:
                    val = 1
                val = val * prev_val
                if idx + 1 < len(tokens):
                    number_words.append(tokens[idx + 1])
            else:
                prev_val = temp

        # is this a negative number?
        if val and prev_word and prev_word in _NEGATIVES_TR:
            val = 0 - val

        # let's make sure it isn't a fraction
        if not val:
            # look for fractions like "2/3"
            aPieces = word.split('/')
            if look_for_fractions(aPieces):
                val = float(aPieces[0]) / float(aPieces[1])
                current_val = val

        else:
            if current_val and all([
                prev_word in _SUMS_TR,
                word not in _SUMS_TR,
                word not in multiplies,
                current_val >= 10]):
                # Backtrack - we've got numbers we can't sum.
                number_words.pop()
                val = prev_val
                break
            prev_val = val

            if word in multiplies and next_word not in multiplies:
                # handle long numbers
                # altı yüz altmış altı
                # iki milyon beş yüz bin
                #
                # if all the remaining scale words are smaller than the
                # current one, the current group is complete and is set
                # aside in to_sum (see the English parser for the full
                # walkthrough of this logic)
                time_to_sum = True
                for other_token in tokens[idx + 1:]:
                    if other_token.word.lower() in multiplies:
                        if string_num_scale[other_token.word.lower()] >= current_val:
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
    return val, number_words


def _initialize_number_data_tr(short_scale, speech=True):
    """
    Generate dictionaries of words to numbers, based on scale.

    This is a helper function for _extract_whole_number.

    Args:
        short_scale (bool):
        speech (bool): consider extra words (_SPOKEN_EXTRA_NUM_TR) to be numbers

    Returns:
        (set(str), dict(str, number), dict(str, number))
        multiplies, string_num_ordinal, string_num_scale

    """
    multiplies = _MULTIPLIES_SHORT_SCALE_TR if short_scale \
        else _MULTIPLIES_LONG_SCALE_TR

    string_num_ordinal_tr = _STRING_SHORT_ORDINAL_TR if short_scale \
        else _STRING_LONG_ORDINAL_TR

    string_num_scale_tr = _SHORT_SCALE_TR if short_scale else _LONG_SCALE_TR
    string_num_scale_tr = invert_dict(string_num_scale_tr)

    return multiplies, string_num_ordinal_tr, string_num_scale_tr


def is_fractional_tr(input_str, short_scale=True, spoken=True):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): ignored — Turkish only uses the short scale
        spoken (bool):
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """

    fracts = {"yarım": 2, "buçuk": 2, "çeyrek": 4}
    for num in _FRACTION_STRING_TR:
        if num > 2:
            fracts[_FRACTION_STRING_TR[num]] = num

    if input_str.lower() in fracts and spoken:
        return 1.0 / fracts[input_str.lower()]
    return False


def extract_number_tr(text, short_scale=True, ordinals=False):
    """
    This function extracts a number from a text string

    Args:
        text (str): the string to normalize
        short_scale (bool): ignored — Turkish only uses the short scale
        ordinals (bool): consider ordinal numbers
    Returns:
        (int) or (float) or False: The extracted number or False if no number
                                   was found

    """
    text = re.sub(r"(?<=[^\W\d]),", " ", text)
    return _extract_number_with_text_tr(tokenize(text.lower()),
                                        short_scale, ordinals).value
