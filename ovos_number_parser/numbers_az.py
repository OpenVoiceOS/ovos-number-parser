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
from decimal import Decimal
from collections import OrderedDict

from ovos_number_parser.util import (convert_to_mixed_fraction, scientific_parts)

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
    70: "yetmişinci",
    80: "səksəninci",
    90: "doxsanıncı",
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

    if last_vowel in ["e", "ə", "i"]:
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

    Word forms follow standard Azerbaijani cardinal structure (yüz, min,
    milyon spoken as separate words; see "Say (dilçilik)", az.wikipedia), so
    the output round-trips through extract_number_az.

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
        n, power = scientific_parts(num, places)
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
    if num == 0 and ordinals:
        result += "sıfır" + _get_ordinal_ak("sıfır")
    elif num in number_names and not ordinals:
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
                if r:
                    tail = " " + _sub_thousand(r, ordinals)
                else:
                    tail = _get_ordinal_ak("yüz") if ordinals else ""
                return (digits[q] + " " if q != 1 else "") + "yüz" + tail

        def _short_scale(n):
            if n >= 999 * max(_SHORT_SCALE_AZ.keys()):
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

                        if 1000 ** i in _SHORT_ORDINAL_AZ:
                            # "min" is said without "bir"; a larger scale
                            # word drops it only when it stands alone
                            if z == 1 and (i == 1 or n == 1000 ** i):
                                number = _SHORT_ORDINAL_AZ[1000 ** i]
                            else:
                                number += _SHORT_ORDINAL_AZ[1000 ** i]
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
                        if 1000000 ** i in _LONG_ORDINAL_AZ:
                            if z == 1 and n == 1000000 ** i:
                                number = _LONG_ORDINAL_AZ[1000000 ** i]
                            else:
                                number += " " + _LONG_ORDINAL_AZ[1000000 ** i]
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
                ordi = False
            return ", ".join(reversed(res))

        if short_scale:
            result += _short_scale(num)
        else:
            result += _long_scale(num)

    # a magnitude with no spoken name reads scientifically
    if result in ("", "mənfi ") and num >= 1e6:
        return result + pronounce_number_az(
            num, places, short_scale, scientific=True)
    if num != int(num) and abs(num) < 1.0 \
            and (result == "mənfi " or not result):
        result += "sıfır"
    # Deal with fractional part
    if not num == int(num) and places > 0:
        result += " nöqtə"
        _num_str = f"{Decimal(str(num)):f}"
        _num_str = _num_str.split(".")[1][0:places]
        for char in _num_str:
            result += " " + number_names[int(char)]
    return result


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


