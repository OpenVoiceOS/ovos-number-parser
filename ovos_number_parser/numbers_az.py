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
from collections import OrderedDict

from ovos_number_parser.util import (invert_dict, convert_to_mixed_fraction, tokenize, look_for_fractions,
                                     partition_list, is_numeric, Token, ReplaceableNumber)

_NUM_STRING_AZ = {
    0: 'sıfır',
    1: 'bir',
    2: 'iki',
    3: 'üç',
    4: 'dörd',
    5: 'beş',
    6: 'altı',
    7: 'yeddi',
    8: 'səkkiz',
    9: 'doqquz',
    10: 'on',
    11: 'on bir',
    12: 'on iki',
    13: 'on üç',
    14: 'on dörd',
    15: 'on beş',
    16: 'on altı',
    17: 'on yeddi',
    18: 'on səkkiz',
    19: 'on doqquz',
    20: 'iyirmi',
    30: 'otuz',
    40: 'qırx',
    50: 'əlli',
    60: 'altmış',
    70: 'yetmiş',
    80: 'səksən',
    90: 'doxsan'
}

_FRACTION_STRING_AZ = {
    2: 'ikidə',
    3: 'üçdə',
    4: 'dörddə',
    5: 'beşdə',
    6: 'altıda',
    7: 'yeddidə',
    8: 'səkkizdə',
    9: 'doqquzda',
    10: 'onda',
    11: 'on birdə',
    12: 'on ikidə',
    13: 'on üçdə',
    14: 'on dörddə',
    15: 'on beşdə',
    16: 'on altıda',
    17: 'on yeddidə',
    18: 'on səkkizdə',
    19: 'on doqquzda',
    20: 'iyirmidə',
    30: 'otuzda',
    40: 'qırxda',
    50: 'əllidə',
    60: 'altmışda',
    70: 'yetmişdə',
    80: 'səksəndə',
    90: 'doxsanda',
    1e2: 'yüzdə',
    1e3: 'mində'
}

_LONG_SCALE_AZ = OrderedDict([
    (100, 'yüz'),
    (1000, 'min'),
    (1000000, 'milyon'),
    (1e12, "milyard"),
    (1e18, 'trilyon'),
    (1e24, "kvadrilyon"),
    (1e30, "kvintilyon"),
    (1e36, "sekstilyon"),
    (1e42, "septilyon"),
    (1e48, "oktilyon"),
    (1e54, "nonilyon"),
    (1e60, "dekilyon")
])

_SHORT_SCALE_AZ = OrderedDict([
    (100, 'yüz'),
    (1000, 'min'),
    (1000000, 'milyon'),
    (1e9, "milyard"),
    (1e12, 'trilyon'),
    (1e15, "kvadrilyon"),
    (1e18, "kvintilyon"),
    (1e21, "sekstilyon"),
    (1e24, "septilyon"),
    (1e27, "oktilyon"),
    (1e30, "nonilyon"),
    (1e33, "dekilyon")
])

_ORDINAL_BASE_AZ = {
    1: 'birinci',
    2: 'ikinci',
    3: 'üçüncü',
    4: 'dördüncü',
    5: 'beşinci',
    6: 'altıncı',
    7: 'yeddinci',
    8: 'səkkizinci',
    9: 'doqquzuncu',
    10: 'onuncu',
    11: 'on birinci',
    12: 'on ikinci',
    13: 'on üçüncü',
    14: 'on dördüncü',
    15: 'on beşinci',
    16: 'on altıncı',
    17: 'on yeddinci',
    18: 'on səkkizinci',
    19: 'on doqquzuncu',
    20: 'iyirminci',
    30: 'otuzuncu',
    40: "qırxıncı",
    50: "əllinci",
    60: "altmışıncı",
    70: "yetmışinci",
    80: "səksəninci",
    90: "doxsanınçı",
    1e2: "yüzüncü",
    1e3: "mininci"
}

_SHORT_ORDINAL_AZ = {
    1e6: "milyonuncu",
    1e9: "milyardıncı",
    1e12: "trilyonuncu",
    1e15: "kvadrilyonuncu",
    1e18: "kvintilyonuncu",
    1e21: "sekstilyonuncu",
    1e24: "septilyonuncu",
    1e27: "oktilyonuncu",
    1e30: "nonilyonuncu",
    1e33: "dekilyonuncu"
    # TODO > 1e-33
}
_SHORT_ORDINAL_AZ.update(_ORDINAL_BASE_AZ)

_LONG_ORDINAL_AZ = {
    1e6: "milyonuncu",
    1e12: "milyardıncı",
    1e18: "trilyonuncu",
    1e24: "kvadrilyonuncu",
    1e30: "kvintilyonuncu",
    1e36: "sekstilyonuncu",
    1e42: "septilyonuncu",
    1e48: "oktilyonuncu",
    1e54: "nonilyonuncu",
    1e60: "dekilyonuncu"
    # TODO > 1e60
}
_LONG_ORDINAL_AZ.update(_ORDINAL_BASE_AZ)

# negate next number (-2 = 0 - 2)
_NEGATIVES_AZ = {"mənfi", "minus"}

# sum the next number (iyirmi iki = 20 + 2)
_SUMS_AZ = {'on', '10', 'iyirmi', '20', 'otuz', '30', 'qırx', '40', 'əlli', '50',
            'altmış', '60', 'yetmiş', '70', 'səksən', '80', 'doxsan', '90'}

_HARD_VOWELS = ['a', 'ı', 'o', 'u']
_SOFT_VOWELS = ['e', 'ə', 'i', 'ö', 'ü']
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
    last_vowel, is_last = _get_last_vowel(word)
    if not last_vowel:
        return ""

    if last_vowel in ["a", "ı"]:
        if is_last:
            return "ncı"
        return "ıncı"

    if last_vowel == ["e", "ə", "i"]:
        if is_last:
            return "nci"
        return "inci"

    if last_vowel in ["o", "u"]:
        if is_last:
            return "ncu"
        return "uncu"

    if last_vowel == ["ö", "ü"]:
        if is_last:
            return "ncü"
        return "üncü"


def _get_full_time_ak(hour):
    if hour in [1, 3, 4, 5, 8, 11]:
        return "ə"
    if hour in [2, 7, 12]:
        return "yə"
    if hour in [9, 10]:
        return "a"
    return "ya"


def _get_half_time_ak(hour):
    if hour in [1, 5, 8, 11]:
        return "in"
    if hour in [2, 7, 12]:
        return "nin"
    if hour in [3, 4]:
        return "ün"
    if hour in [9, 10]:
        return "un"
    return "nın"


def _get_daytime(hour):
    if hour < 6:
        return "gecə"
    if hour < 12:
        return "səhər"
    if hour < 18:
        return "gündüz"
    return "axşam"


def _generate_plurals_az(originals):
    """
    Return a new set or dict containing the plural form of the original values,

    In Azerbaijani this means appending 'lar' or 'lər' to them according to the last vowel in word.

    Args:
        originals set(str) or dict(str, any): values to pluralize

    Returns:
        set(str) or dict(str, any)

    """

    if isinstance(originals, dict):
        return {key + ('lar' if _last_vowel_type(key) else 'lər'): value for key, value in originals.items()}
    return {value + ('lar' if _last_vowel_type(value) else 'lər') for value in originals}


_MULTIPLIES_LONG_SCALE_AZ = set(_LONG_SCALE_AZ.values()) | \
                            set(_LONG_SCALE_AZ.values())

_MULTIPLIES_SHORT_SCALE_AZ = set(_SHORT_SCALE_AZ.values()) | \
                             set(_SHORT_SCALE_AZ.values())

# split sentence parse separately and sum ( 2 and a half = 2 + 0.5 )
_FRACTION_MARKER_AZ = {"və"}

# decimal marker ( 1 nöqtə 5 = 1 + 0.5)
_DECIMAL_MARKER_AZ = {"nöqtə"}

_STRING_NUM_AZ = invert_dict(_NUM_STRING_AZ)

_SPOKEN_EXTRA_NUM_AZ = {
    "yarım": 0.5,
    "üçdəbir": 1 / 3,
    "dörddəbir": 1 / 4
}

_STRING_SHORT_ORDINAL_AZ = invert_dict(_SHORT_ORDINAL_AZ)
_STRING_LONG_ORDINAL_AZ = invert_dict(_LONG_ORDINAL_AZ)


def nice_number_az(number, speech=True, denominators=range(1, 21)):
    """ Azerbaijani helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 yarım" for speech and "4 1/2" for text

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
    den_str = _FRACTION_STRING_AZ[den]
    if whole == 0:
        if den == 2:
            return 'yarım'
        return '{} {}'.format(den_str, num)
    if den == 2:
        return '{} yarım'.format(whole)
    return '{} və {} {}'.format(whole, den_str, num)


def pronounce_number_az(number, places=2, short_scale=True, scientific=False,
                        ordinals=False):
    """
    Convert a number to it's spoken equivalent

    For example, '5.2' would return 'beş nöqtə iki'

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
    num = number
    # deal with infinity
    if num == float("inf"):
        return "sonsuzluq"
    elif num == float("-inf"):
        return "mənfi sonsuzluq"
    if scientific:
        number = '%E' % num
        n, power = number.replace("+", "").split("E")
        power = int(power)
        if power != 0:
            if ordinals:
                # This handles negatives of powers separately from the normal
                # handling since each call disables the scientific flag
                return '{}{} vurulsun on üstü {}{}'.format(
                    'mənfi ' if float(n) < 0 else '',
                    pronounce_number_az(
                        abs(float(n)), places, short_scale, False, ordinals=False),
                    'mənfi ' if power < 0 else '',
                    pronounce_number_az(abs(power), places, short_scale, False, ordinals=True))
            else:
                # This handles negatives of powers separately from the normal
                # handling since each call disables the scientific flag
                return '{}{} vurulsun on üstü {}{}'.format(
                    'mənfi ' if float(n) < 0 else '',
                    pronounce_number_az(
                        abs(float(n)), places, short_scale, False),
                    'mənfi ' if power < 0 else '',
                    pronounce_number_az(abs(power), places, short_scale, False))

    if short_scale:
        number_names = _NUM_STRING_AZ.copy()
        number_names.update(_SHORT_SCALE_AZ)
    else:
        number_names = _NUM_STRING_AZ.copy()
        number_names.update(_LONG_SCALE_AZ)

    digits = [number_names[n] for n in range(0, 20)]

    tens = [number_names[n] for n in range(10, 100, 10)]

    if short_scale:
        hundreds = [_SHORT_SCALE_AZ[n] for n in _SHORT_SCALE_AZ.keys()]
    else:
        hundreds = [_LONG_SCALE_AZ[n] for n in _LONG_SCALE_AZ.keys()]

    # deal with negatives
    result = ""
    if num < 0:
        # result = "mənfi " if scientific else "minus "
        result = "mənfi "
    num = abs(num)

    # check for a direct match
    if num in number_names and not ordinals:
        if num > 1000:
            result += "bir "
        result += number_names[num]
    else:
        def _sub_thousand(n, ordinals=False):
            assert 0 <= n <= 999
            if n in _SHORT_ORDINAL_AZ and ordinals:
                return _SHORT_ORDINAL_AZ[n]
            if n <= 19:
                return digits[n]
            elif n <= 99:
                q, r = divmod(n, 10)
                return tens[q - 1] + (" " + _sub_thousand(r, ordinals) if r
                                      else "")
            else:
                q, r = divmod(n, 100)
                return (digits[q] + " " if q != 1 else "") + "yüz" + (
                    " " + _sub_thousand(r, ordinals) if r else "")

        def _short_scale(n):
            if n >= 999 * max(_SHORT_SCALE_AZ.keys()):
                return "sonsuzluq"
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

                        if i * 1000 in _SHORT_ORDINAL_AZ:
                            if z == 1:
                                number = _SHORT_ORDINAL_AZ[i * 1000]
                            else:
                                number += _SHORT_ORDINAL_AZ[i * 1000]
                        else:
                            if n not in _SHORT_SCALE_AZ:
                                num = int("1" + "0" * (len(str(n)) - 2))

                                number += _SHORT_SCALE_AZ[num] + _get_ordinal_ak(_SHORT_SCALE_AZ[num])
                            else:
                                number = _SHORT_SCALE_AZ[n] + _get_ordinal_ak(_SHORT_SCALE_AZ[n])
                    else:
                        number += hundreds[i]
                if number.startswith("bir min"):
                    number = number[4:]
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
            if n >= max(_LONG_SCALE_AZ.keys()):
                return "sonsuzluq"
            ordi = ordinals
            if int(n) != n:
                ordi = False
            n = int(n)
            assert 0 <= n
            res = []
            for i, z in enumerate(_split_by(n, 1000000)):
                if not z:
                    continue
                number = pronounce_number_az(z, places, True, scientific,
                                             ordinals=ordi and not i)
                # strip off the comma after the thousand
                if i:
                    if i >= len(hundreds):
                        return ""
                    # plus one as we skip 'thousand'
                    # (and 'hundred', but this is excluded by index value)
                    number = number.replace(',', '')

                    if ordi:
                        if i * 1000000 in _LONG_ORDINAL_AZ:
                            if z == 1:
                                number = _LONG_ORDINAL_AZ[
                                    (i + 1) * 1000000]
                            else:
                                number += _LONG_ORDINAL_AZ[
                                    (i + 1) * 1000000]
                        else:
                            if n not in _LONG_SCALE_AZ:
                                num = int("1" + "0" * (len(str(n)) - 2))

                                number += " " + _LONG_SCALE_AZ[
                                    num] + _get_ordinal_ak(_LONG_SCALE_AZ[num])
                            else:
                                number = " " + _LONG_SCALE_AZ[n] + _get_ordinal_ak(_LONG_SCALE_AZ[n])
                    else:

                        number += " " + hundreds[i + 1]
                res.append(number)
            return ", ".join(reversed(res))

        if short_scale:
            result += _short_scale(num)
        else:
            result += _long_scale(num)

    # deal with scientific notation unpronounceable as number
    if not result and "e" in str(num):
        return pronounce_number_az(num, places, short_scale, scientific=True)
    # Deal with fractional part
    elif not num == int(num) and places > 0:
        if abs(num) < 1.0 and (result == "mənfi " or not result):
            result += "sıfır"
        result += " nöqtə"
        _num_str = str(num)
        _num_str = _num_str.split(".")[1][0:places]
        for char in _num_str:
            result += " " + number_names[int(char)]
    return result


def numbers_to_digits_az(text, short_scale=True, ordinals=False):
    """
    Convert words in a string into their equivalent numbers.
    Args:
        text str:
        short_scale boolean: True if short scale numbers should be used.
        ordinals boolean: True if ordinals (e.g. birinci, ikinci, üçüncü) should
                          be parsed to their number values (1, 2, 3...)

    Returns:
        str
        The original text, with numbers subbed in where appropriate.

    """
    tokens = tokenize(text)
    numbers_to_replace = \
        _extract_numbers_with_text_az(tokens, short_scale, ordinals)

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


def _extract_numbers_with_text_az(tokens, short_scale=True,
                                  ordinals=False, fractional_numbers=True):
    """
    Extract all numbers from a list of Tokens, with the words that
    represent them.

    Args:
        [Token]: The tokens to parse.
        short_scale bool: True if short scale numbers should be used, False for
                          long scale. True by default.
        ordinals bool: True if ordinal words (birinci, ikinci, üçüncü, etc) should
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
            _extract_number_with_text_az(tokens, short_scale,
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


def _extract_number_with_text_az(tokens, short_scale=True,
                                 ordinals=False, fractional_numbers=True):
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
        _extract_number_with_text_az_helper(tokens, short_scale,
                                            ordinals, fractional_numbers)
    return ReplaceableNumber(number, tokens)


def _extract_number_with_text_az_helper(tokens,
                                        short_scale=True, ordinals=False,
                                        fractional_numbers=True):
    """
    Helper for _extract_number_with_text_az.

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
            _extract_fraction_with_text_az(tokens, short_scale, ordinals)
        if fraction:
            # print("fraction")
            return fraction, fraction_text

        decimal, decimal_text = \
            _extract_decimal_with_text_az(tokens, short_scale, ordinals)
        if decimal:
            # print("decimal")
            return decimal, decimal_text

    return _extract_whole_number_with_text_az(tokens, short_scale, ordinals)


def _extract_fraction_with_text_az(tokens, short_scale, ordinals):
    """
    Extract fraction numbers from a string.

    This function handles text such as '2 və dörddə üç'. Note that "yarım" or
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
    for c in _FRACTION_MARKER_AZ:
        partitions = partition_list(tokens, lambda t: t.word == c)

        if len(partitions) == 3:
            numbers1 = \
                _extract_numbers_with_text_az(partitions[0], short_scale,
                                              ordinals, fractional_numbers=False)
            numbers2 = \
                _extract_numbers_with_text_az(partitions[2], short_scale,
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


def _extract_decimal_with_text_az(tokens, short_scale, ordinals):
    """
    Extract decimal numbers from a string.

    This function handles text such as '2 nöqtə 5'.

    Notes:
        While this is a helper for extractnumber_az, it also depends on
        extractnumber_az, to parse out the components of the decimal.

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
    for c in _DECIMAL_MARKER_AZ:
        partitions = partition_list(tokens, lambda t: t.word == c)

        if len(partitions) == 3:
            numbers1 = \
                _extract_numbers_with_text_az(partitions[0], short_scale,
                                              ordinals, fractional_numbers=False)
            numbers2 = \
                _extract_numbers_with_text_az(partitions[2], short_scale,
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


def _extract_whole_number_with_text_az(tokens, short_scale, ordinals):
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
        _initialize_number_data_az(short_scale, speech=ordinals is not None)

    number_words = []  # type: List[Token]
    val = False
    prev_val = None
    next_val = None
    to_sum = []
    # print(tokens, ordinals)
    for idx, token in enumerate(tokens):
        current_val = None
        if next_val:
            next_val = None
            continue

        word = token.word.lower()
        if word in _NEGATIVES_AZ:
            number_words.append(token)
            continue

        prev_word = tokens[idx - 1].word.lower() if idx > 0 else ""
        next_word = tokens[idx + 1].word.lower() if idx + 1 < len(tokens) else ""
        # print(prev_word, word, next_word, number_words)
        if word not in string_num_scale and \
                word not in _STRING_NUM_AZ and \
                word not in _SUMS_AZ and \
                word not in multiplies and \
                not (ordinals and word in string_num_ordinal) and \
                not is_numeric(word) and \
                not is_fractional_az(word, short_scale=short_scale) and \
                not look_for_fractions(word.split('/')):
            # print("a1")
            words_only = [token.word for token in number_words]

            if number_words and not all([w.lower() in
                                         _NEGATIVES_AZ for w in words_only]):
                break
            else:
                number_words = []
                continue
        elif word not in multiplies \
                and word not in _SPOKEN_EXTRA_NUM_AZ \
                and prev_word not in multiplies \
                and prev_word not in _SUMS_AZ \
                and not (ordinals and prev_word in string_num_ordinal) \
                and prev_word not in _NEGATIVES_AZ:
            number_words = [token]
            # print("a2")
        elif prev_word in _SUMS_AZ and word in _SUMS_AZ:
            number_words = [token]
            # print("a3")
        elif ordinals is None and \
                (word in string_num_ordinal or word in _SPOKEN_EXTRA_NUM_AZ):
            # print("a4")
            # flagged to ignore this token
            continue
        else:
            # print("a5")
            number_words.append(token)

        # is this word already a number ?
        if is_numeric(word):
            # print("b")
            if word.isdigit():  # doesn't work with decimals
                val = int(word)
            else:
                val = float(word)
            current_val = val

        # is this word the name of a number ?
        if word in _STRING_NUM_AZ:
            val = _STRING_NUM_AZ.get(word)
            current_val = val
            # print("c1", current_val)
        elif word in string_num_scale:
            val = string_num_scale.get(word)
            current_val = val
            # print("c2")
        elif ordinals and word in string_num_ordinal:
            val = string_num_ordinal[word]
            current_val = val
            # print("c3")
        # is the prev word a number and should we sum it?
        # twenty two, fifty six
        if (prev_word in _SUMS_AZ and val and val < 10) or all([prev_word in
                                                                multiplies,
                                                                val < prev_val if prev_val else False]):
            val = prev_val + val
            # print("d")

        # is the prev word a number and should we multiply it?
        # twenty hundred, six hundred
        if word in multiplies:
            if not prev_val:
                prev_val = 1
            val = prev_val * val
            # print("e")

        # is this a spoken fraction?
        # 1 yarım fincan - yarım fincan
        if current_val is None and not (ordinals is None and word in _SPOKEN_EXTRA_NUM_AZ):
            val = is_fractional_az(word, short_scale=short_scale,
                                   spoken=ordinals is not None)
            if val:
                if prev_val:
                    val += prev_val
                current_val = val
                # print("f", current_val, prev_val)
                if word in _SPOKEN_EXTRA_NUM_AZ:
                    break

        # dörddə bir
        if ordinals is False:
            temp = prev_val
            prev_val = is_fractional_az(prev_word, short_scale=short_scale)
            if prev_val:
                if not val:
                    val = 1
                val = val * prev_val
                if idx + 1 < len(tokens):
                    number_words.append(tokens[idx + 1])
            else:
                prev_val = temp
            # print("g", prev_val)

        # is this a negative number?
        if val and prev_word and prev_word in _NEGATIVES_AZ:
            val = 0 - val
            # print("h")

        # let's make sure it isn't a fraction
        if not val:
            # look for fractions like "2/3"
            aPieces = word.split('/')
            if look_for_fractions(aPieces):
                val = float(aPieces[0]) / float(aPieces[1])
                current_val = val
            # print("i")

        else:
            if current_val and all([
                prev_word in _SUMS_AZ,
                word not in _SUMS_AZ,
                word not in multiplies,
                current_val >= 10]):
                # Backtrack - we've got numbers we can't sum.
                # print("j", number_words, prev_val)
                number_words.pop()
                val = prev_val
                break
            prev_val = val

            if word in multiplies and next_word not in multiplies:
                # handle long numbers
                # six hundred sixty six
                # two million five hundred thousand
                #
                # This logic is somewhat complex, and warrants
                # extensive documentation for the next coder's sake.
                #
                # The current word is a power of ten. `current_val` is
                # its integer value. `val` is our working sum
                # (above, when `current_val` is 1 million, `val` is
                # 2 million.)
                #
                # We have a dict `string_num_scale` containing [value, word]
                # pairs for "all" powers of ten: string_num_scale[10] == "ten.
                #
                # We need go over the rest of the tokens, looking for other
                # powers of ten. If we find one, we compare it with the current
                # value, to see if it's smaller than the current power of ten.
                #
                # Numbers which are not powers of ten will be passed over.
                #
                # If all the remaining powers of ten are smaller than our
                # current value, we can set the current value aside for later,
                # and begin extracting another portion of our final result.
                # For example, suppose we have the following string.
                # The current word is "million".`val` is 9000000.
                # `current_val` is 1000000.
                #
                #    "nine **million** nine *hundred* seven **thousand**
                #     six *hundred* fifty seven"
                #
                # Iterating over the rest of the string, the current
                # value is larger than all remaining powers of ten.
                #
                # The if statement passes, and nine million (9000000)
                # is appended to `to_sum`.
                #
                # The main variables are reset, and the main loop begins
                # assembling another number, which will also be appended
                # under the same conditions.
                #
                # By the end of the main loop, to_sum will be a list of each
                # "place" from 100 up: [9000000, 907000, 600]
                #
                # The final three digits will be added to the sum of that list
                # at the end of the main loop, to produce the extracted number:
                #
                #    sum([9000000, 907000, 600]) + 57
                # == 9,000,000 + 907,000 + 600 + 57
                # == 9,907,657
                #
                # >>> foo = "nine million nine hundred seven thousand six
                #            hundred fifty seven"
                # >>> extract_number(foo)
                # 9907657
                # print("k", tokens[idx+1:])
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
                    # print("l")
                    to_sum.append(val)
                    val = 0
                    prev_val = 0

    if val is not None and to_sum:
        # print("m", to_sum)
        val += sum(to_sum)
    # print(val, number_words, "end")
    return val, number_words


def _initialize_number_data_az(short_scale, speech=True):
    """
    Generate dictionaries of words to numbers, based on scale.

    This is a helper function for _extract_whole_number.

    Args:
        short_scale (bool):
        speech (bool): consider extra words (_SPOKEN_EXTRA_NUM_AZ) to be numbers

    Returns:
        (set(str), dict(str, number), dict(str, number))
        multiplies, string_num_ordinal, string_num_scale

    """
    multiplies = _MULTIPLIES_SHORT_SCALE_AZ if short_scale \
        else _MULTIPLIES_LONG_SCALE_AZ

    string_num_ordinal_az = _STRING_SHORT_ORDINAL_AZ if short_scale \
        else _STRING_LONG_ORDINAL_AZ

    string_num_scale_az = _SHORT_SCALE_AZ if short_scale else _LONG_SCALE_AZ
    string_num_scale_az = invert_dict(string_num_scale_az)

    return multiplies, string_num_ordinal_az, string_num_scale_az


def is_fractional_az(input_str, short_scale=True, spoken=True):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): use short scale if True, long scale if False
        spoken (bool):
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """

    fracts = {"dörddəbir": 4, "yarım": 2, "üçdəbir": 3}
    for num in _FRACTION_STRING_AZ:
        if num > 2:
            fracts[_FRACTION_STRING_AZ[num]] = num

    if input_str.lower() in fracts and spoken:
        return 1.0 / fracts[input_str.lower()]
    return False


def extract_number_az(text, short_scale=True, ordinals=False):
    """
    This function extracts a number from a text string,
    handles pronunciations in long scale and short scale

    https://en.wikipedia.org/wiki/Names_of_large_numbers

    Args:
        text (str): the string to normalize
        short_scale (bool): use short scale if True, long scale if False
        ordinals (bool): consider ordinal numbers
    Returns:
        (int) or (float) or False: The extracted number or False if no number
                                   was found

    """
    return _extract_number_with_text_az(tokenize(text.lower()),
                                        short_scale, ordinals).value
