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
from decimal import Decimal
from collections import OrderedDict

from ovos_number_parser.util import (convert_to_mixed_fraction, scientific_parts)

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

    Word forms follow the Türk Dil Kurumu spelling rules ("Sayıların
    Yazılışı"): each numeral group (yüz, bin, milyon) is spoken as separate
    words, so the output round-trips through extract_number_tr.

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
        n, power = scientific_parts(num, places)
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

    # a magnitude with no spoken name reads scientifically
    if result in ("", "eksi ") and num >= 1e6:
        return result + pronounce_number_tr(
            num, places, short_scale, scientific=True)
    if num != int(num) and abs(num) < 1.0 \
            and (result == "eksi " or not result):
        result += "sıfır"
    # Deal with fractional part
    if not num == int(num) and places > 0:
        result += " virgül"
        _num_str = f"{Decimal(str(num)):f}"
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


