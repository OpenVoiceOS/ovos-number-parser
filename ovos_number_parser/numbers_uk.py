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
import re
from collections import OrderedDict

from ovos_number_parser.util import (convert_to_mixed_fraction, look_for_fractions, invert_dict,
                                     is_numeric, tokenize, partition_list, Token, ReplaceableNumber)

_NUM_STRING_UK = {
    0: "нуль",
    1: "один",
    2: "два",
    3: "три",
    4: "чотири",
    5: "п'ять",
    6: "шість",
    7: "сім",
    8: "вісім",
    9: "дев'ять",
    10: "десять",
    11: "одинадцять",
    12: "дванадцять",
    13: "тринадцять",
    14: "чотирнадцять",
    15: "п'ятнадцять",
    16: "шістнадцять",
    17: "сімнадцять",
    18: "вісімнадцять",
    19: "дев'ятнадцять",
    20: "двадцять",
    30: "тридцять",
    40: "сорок",
    50: "п'ятдесят",
    60: "шістдесят",
    70: "сімдесят",
    80: "вісімдесят",
    90: "дев'яносто",
    100: "сто",
    200: "двісті",
    300: "триста",
    400: "чотириста",
    500: "п'ятсот",
    600: "шістсот",
    700: "сімсот",
    800: "вісімсот",
    900: "дев'ятсот"
}

_PLURALS = {
    'двох': 2, 'двум': 2, 'двома': 2, 'дві': 2, "двоє": 2, "двійка": 2,
    'обидва': 2, 'обидвох': 2, 'обидві': 2, 'обох': 2, 'обома': 2, 'обом': 2,
    'пара': 2, 'пари': 2, 'парою': 2, 'парами': 2, 'парі': 2, 'парах': 2, 'пару': 2,
    'трьох': 3, 'трьома': 3, 'трьом': 3,
    'чотирьох': 4, 'чотирьом': 4, 'чотирма': 4,
    "п'ятьох": 5, "п'ятьом": 5, "п'ятьома": 5,
    "шістьом": 6, "шести": 6, "шістьох": 6, "шістьма": 6, "шістьома": 6,
    "семи": 7, "сімом": 7, "сімох": 7, "сімома": 7, "сьома": 7,
    "восьми": 8, "вісьмох": 8, "вісьмом": 8, "вісьма": 8, "вісьмома": 8,
    "дев'яти": 9, "дев'ятьох": 9, "дев'ятьом": 9, "дев'ятьма": 9,
    "десяти": 10, "десятьох": 10, "десятьма": 10, "десятьома": 10,
    "сорока": 40,
    "сот": 100, "сотень": 100, "сотні": 100, "сотня": 100,
    "двохсот": 200, "двомстам": 200, "двомастами": 200, "двохстах": 200,
    "тисяч": 1000, "тисячі": 1000, "тисячу": 1000, "тисячах": 1000,
    "тисячами": 1000, "тисячею": 1000
}

_FRACTION_STRING_UK = {
    2: "друга",
    3: "третя",
    4: "четверта",
    5: "п'ята",
    6: "шоста",
    7: "сьома",
    8: "восьма",
    9: "дев'ята",
    10: "десята",
    11: "одинадцята",
    12: "дванадцята",
    13: "тринадцята",
    14: "чотирнадцята",
    15: "п'ятнадцята",
    16: "шістнадцята",
    17: "сімнадцята",
    18: "вісімнадцята",
    19: "дев'ятнадцята",
    20: "двадцята",
    30: "тридцята",
    40: "сорокова",
    50: "п'ятдесята",
    60: "шістдесята",
    70: "сімдесята",
    80: "вісімдесята",
    90: "дев'яноста",
    1e2: "сота",
    1e3: "тисячна",
    1e6: "мільйонна",
    1e9: "мільярдна",
    1e-12: "більйонна",
}

_SHORT_SCALE_UK = OrderedDict([
    (1e3, "тисяча"),
    (1e6, "мільйон"),
    (1e9, "мільярд"),
    (1e18, "трильйон"),
    (1e12, "більйон"),
    (1e15, "квадрилліон"),
    (1e18, "квінтиліон"),
    (1e21, "секстильйон"),
    (1e24, "септилліон"),
    (1e27, "октиліон"),
    (1e30, "нонільйон"),
    (1e33, "дециліон"),
    (1e36, "ундеціліон"),
    (1e39, "дуодециліон"),
    (1e42, "тредециліон"),
    (1e45, "кваттордециліон"),
    (1e48, "квіндециліон"),
    (1e51, "сексдециліон"),
    (1e54, "септендециліон"),
    (1e57, "октодециліон"),
    (1e60, "новемдециліон"),
    (1e63, "вігінтильйон"),
    (1e66, "унвігінтільйон"),
    (1e69, "дуовігінтильйон"),
    (1e72, "тревігінтильйон"),
    (1e75, "кватторвігінтільйон"),
    (1e78, "квінвігінтильйон"),
    (1e81, "секснвігінтіліон"),
    (1e84, "септенвігінтильйон"),
    (1e87, "октовігінтиліон"),
    (1e90, "новемвігінтільйон"),
    (1e93, "тригінтильйон"),
])

_LONG_SCALE_UK = OrderedDict([
    (1e3, "тисяча"),
    (1e6, "мільйон"),
    (1e9, "мільярд"),
    (1e12, "більйон"),
    (1e15, "біліард"),
    (1e18, "трильйон"),
    (1e21, "трильярд"),
    (1e24, "квадрилліон"),
    (1e27, "квадрільярд"),
    (1e30, "квінтиліон"),
    (1e33, "квінтільярд"),
    (1e36, "секстильйон"),
    (1e39, "секстильярд"),
    (1e42, "септилліон"),
    (1e45, "септільярд"),
    (1e48, "октиліон"),
    (1e51, "октільярд"),
    (1e54, "нонільйон"),
    (1e57, "нонільярд"),
    (1e60, "дециліон"),
    (1e63, "дециліард"),
    (1e66, "ундеціліон"),
    (1e72, "дуодециліон"),
    (1e78, "тредециліон"),
    (1e84, "кваттордециліон"),
    (1e90, "квіндециліон"),
    (1e96, "сексдециліон"),
    (1e102, "септендециліон"),
    (1e108, "октодециліон"),
    (1e114, "новемдециліон"),
    (1e120, "вігінтильйон"),
])

_ORDINAL_BASE_UK = {
    1: "перший",
    2: "другий",
    3: "третій",
    4: "четвертий",
    5: "п'ятий",
    6: "шостий",
    7: "сьомий",
    8: "восьмий",
    9: "дев'ятий",
    10: "десятий",
    11: "одинадцятий",
    12: "дванадцятий",
    13: "тринадцятий",
    14: "чотирнадцятий",
    15: "п'ятнадцятий",
    16: "шістнадцятий",
    17: "сімнадцятий",
    18: "вісімнадцятий",
    19: "дев'ятнадцятий",
    20: "двадцятий",
    30: "тридцятий",
    40: "сороковий",
    50: "п'ятдесятий",
    60: "шістдесятий",
    70: "сімдесятий",
    80: "вісімдесятий",
    90: "дев'яностий",
    1e2: "сотий",
    2e2: "двохсотий",
    3e2: "трьохсотий",
    4e2: "чотирисотий",
    5e2: "п'ятисотий",
    6e2: "шістсотий",
    7e2: "семисотий",
    8e2: "восьмисотий",
    9e2: "дев'ятисотий",
    1e3: "тисячний"
}

_SHORT_ORDINAL_UK = {
    1e6: "мільйон",
    1e9: "мільярд",
    1e18: "трильйон",
    1e15: "квадрилліон",
    1e18: "квінтильйон",
    1e21: "секстильйон",
    1e24: "септилліон",
    1e27: "октиліон",
    1e30: "нонільйон",
    1e33: "дециліон",
    1e36: "ундеціліон",
    1e39: "дуодециліон",
    1e42: "тредециліон",
    1e45: "кваттордециліон",
    1e48: "квіндециліон",
    1e51: "сексдециліон",
    1e54: "септендециліон",
    1e57: "октодециліон",
    1e60: "новемдециліон",
    1e63: "вігінтильйон"
}
_SHORT_ORDINAL_UK.update(_ORDINAL_BASE_UK)

_LONG_ORDINAL_UK = {
    1e6: "мільйон",
    1e9: "мільярд",
    1e12: "більйон",
    1e15: "біліард",
    1e18: "трильйон",
    1e21: "трильярд",
    1e24: "квадрилліон",
    1e27: "квадрильярд",
    1e30: "квінтиліон",
    1e33: "квінтільярд",
    1e36: "секстильйон",
    1e39: "секстильярд",
    1e42: "септилліон",
    1e45: "септільярд",
    1e48: "октиліон",
    1e51: "октільярд",
    1e54: "нонільйон",
    1e57: "нонільярд",
    1e60: "дециліон",
    1e63: "дециліард",
    1e66: "ундеціліон",
    1e72: "дуодециліон",
    1e78: "тредециліон",
    1e84: "кваттордециліон",
    1e90: "квіндециліон",
    1e96: "сексдециліон",
    1e102: "септендециліон",
    1e108: "октодециліон",
    1e114: "новемдециліон",
    1e120: "вігінтильйон"
}
_LONG_ORDINAL_UK.update(_ORDINAL_BASE_UK)


def generate_plurals_uk(originals):
    """
    Return a new set or dict containing the plural form of the original values,
    Generate different cases of values

    In English this means all with 's' appended to them.

    Args:
        originals set(str) or dict(str, any): values to pluralize

    Returns:
        set(str) or dict(str, any)

    """
    suffixes = ["а", "ах", "их", "ам", "ами", "ів",
                "ям", "ох", "и", "на", "ни", "і", "ні",
                "ий", "ний", 'ьох', 'ьома', 'ьом', 'ох',
                'ум', 'ма', 'ом']
    if isinstance(originals, dict):
        thousand = {"тисяч": 1000, "тисячі": 1000, "тисячу": 1000, "тисячах": 1000}
        hundred = {"сотня": 100, "сотні": 100, "сотень": 100}
        result_dict = {key + suffix: value for key, value in originals.items() for suffix in suffixes}
        result_dict.update(thousand)
        result_dict.update(hundred)
        return result_dict
    thousand = ["тисяч", "тисячі", "тисячу", "тисячах"]
    result_dict = {value + suffix for value in originals for suffix in suffixes}
    result_dict.update(thousand)
    return {value + suffix for value in originals for suffix in suffixes}


# negate next number (-2 = 0 - 2)
_NEGATIVES = {"мінус"}

# sum the next number (twenty two = 20 + 2)
_SUMS = {"двадцять", "20", "тридцять", "30", "сорок", "40", "п'ятдесят", "50",
         "шістдесят", "60", "сімдесят", "70", "вісімдесят", "80", "дев'яносто", "90",
         "сто", "100", "двісті", "200", "триста", "300", "чотириста", "400",
         "п'ятсот", "500", "шістсот", "600", "сімсот", "700", "вісімсот", "800",
         "дев'ятсот", "900"}

_MULTIPLIES_LONG_SCALE_UK = set(_LONG_SCALE_UK.values()) | \
                            generate_plurals_uk(_LONG_SCALE_UK.values())

_MULTIPLIES_SHORT_SCALE_UK = set(_SHORT_SCALE_UK.values()) | \
                             generate_plurals_uk(_SHORT_SCALE_UK.values())

# split sentence parse separately and sum ( 2 and a half = 2 + 0.5 )
_FRACTION_MARKER = {"і", "та", "з", " "}

# decimal marker ( 1 point 5 = 1 + 0.5)
_DECIMAL_MARKER = {"ціла", "цілих", "точка", "крапка", "кома"}

_STRING_NUM_UK = invert_dict(_NUM_STRING_UK)

_STRING_NUM_UK.update(generate_plurals_uk(_STRING_NUM_UK))
_STRING_NUM_UK.update(_PLURALS)
_STRING_NUM_UK.update({
    "трильйон": 1e18,
    "половина": 0.5, "половиною": 0.5, "половини": 0.5, "половин": 0.5, "половинами": 0.5, "пів": 0.5,
    "одна": 1, "одної": 1, "одній": 1, "одну": 1
})

_WORDS_NEXT_UK = [
    "майбутня", "майбутнє", "майбутній", "майбутньому", "майбутнім", "майбутньої", "майбутнього",
    "нова", "нове", "новий", "нового", "нової", "новим", "новою", "через",
    "наступна", "наступне", "наступний", "наступній", "наступному", "наступним", "наступною",
]
_WORDS_PREV_UK = [
    "попередня", "попередній", "попереднім", "попередньої",
    "попередню", "попереднього", "попередне", "тому",
    "минула", "минулий", "минуле", "минулу", "минулого", "минулій", "минулому",
    "минулої", "минулою", "минулим",
    "та", "той", "ті", "те", "того",
]
_WORDS_CURRENT_UK = [
    "теперішній", "теперішня", "теперішні", "теперішній", "теперішньому",
    "теперішньою", "теперішнім", "теперішнього", "теперішньої",
    "дана", "даний", "дане", "даним", "даною", "даного", "даної", "даному", "даній",
    "поточний", "поточна", "поточні", "поточне", "поточного", "поточної",
    "поточному", "поточній", "поточним", "поточною",
    "нинішній", "нинішня", "нинішнє", "нинішньому", "нинішній",
    "нинішнього", "нинішньої", "нинішнім", "нинішньою",
    "цей", "ця", "це", "цим", "цією", "цьому", "цій"
]
_WORDS_NOW_UK = [
    "тепер",
    "зараз",
]
_WORDS_MORNING_UK = ["ранок", "зранку", "вранці", "ранку"]
_WORDS_DAY_UK = ["вдень", "опівдні"]
_WORDS_EVENING_UK = ["вечер", "ввечері", "увечері", "вечором"]
_WORDS_NIGHT_UK = ["ніч", "вночі"]

_STRING_SHORT_ORDINAL_UK = invert_dict(_SHORT_ORDINAL_UK)
_STRING_LONG_ORDINAL_UK = invert_dict(_LONG_ORDINAL_UK)


def nice_number_uk(number, speech=True, denominators=range(1, 21)):
    """ Ukrainian helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 and a half" for speech and "4 1/2" for text

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
    den_str = _FRACTION_STRING_UK[den]

    if whole == 0:
        return_string = '{} {}'.format(num, den_str)
    elif num == 1 and den == 2:
        return_string = '{} з половиною'.format(whole)
    else:
        return_string = '{} і {} {}'.format(whole, num, den_str)
    if 2 <= den <= 4:
        if 2 <= num <= 4:
            return_string = return_string[:-1] + 'і'
        elif num > 4:
            return_string = return_string[:-1] + 'ій'
    elif den >= 5:
        if 2 <= num <= 4:
            return_string = return_string[:-1] + 'і'
        elif num > 4:
            return_string = return_string[:-1] + 'их'

    return return_string


def pronounce_number_uk(number, places=2, short_scale=True, scientific=False,
                        ordinals=False):
    """
    Convert a number to it's spoken equivalent

    For example, '5.2' would return 'five point two'

    Args:
        number(float or int): the number to pronounce (under 100)
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
        return "нескінченність"
    elif num == float("-inf"):
        return "мінус нескінченність"
    if scientific:
        number = '%E' % num
        n, power = number.replace("+", "").split("E")
        power = int(power)
        if power != 0:
            if ordinals:
                # This handles negative powers separately from the normal
                # handling since each call disables the scientific flag
                if float(n) < 0:
                    first_part = 'мінус ' + pronounce_number_uk(
                        abs(float(n)), places, short_scale, False, ordinals=True)
                else:
                    first_part = pronounce_number_uk(
                        abs(float(n)), places, short_scale, False, ordinals=True)

                if power < 0:
                    second_part = 'мінус ' + pronounce_number_uk(
                        abs(power), places, short_scale, False, ordinals=True)
                else:
                    second_part = pronounce_number_uk(
                        abs(power), places, short_scale, False, ordinals=True)
                if second_part.endswith('ий'):
                    second_part = second_part[:-2] + 'ому'

                return '{} на десять у {} ступені'.format(
                    first_part, second_part)
            else:
                # This handles negative powers separately from the normal
                # handling since each call disables the scientific flag
                return '{}{} на десять у ступені {}{}'.format(
                    'мінус ' if float(n) < 0 else '',
                    pronounce_number_uk(
                        abs(float(n)), places, short_scale, False, ordinals=False),
                    'мінус ' if power < 0 else '',
                    pronounce_number_uk(abs(power), places, short_scale, False, ordinals=False))

    if short_scale:
        number_names = _NUM_STRING_UK.copy()
        number_names.update(_SHORT_SCALE_UK)
    else:
        number_names = _NUM_STRING_UK.copy()
        number_names.update(_LONG_SCALE_UK)

    digits = [number_names[n] for n in range(0, 20)]

    tens = [number_names[n] for n in range(10, 100, 10)]

    if short_scale:
        hundreds = [_SHORT_SCALE_UK[n] for n in _SHORT_SCALE_UK.keys()]
    else:
        hundreds = [_LONG_SCALE_UK[n] for n in _LONG_SCALE_UK.keys()]

    # deal with negative numbers
    result = ""
    if num < 0:
        result = "мінус "
    num = abs(num)

    # check for a direct match
    if num in number_names and not ordinals:
        result += number_names[num]
    else:
        def _sub_thousand(n, ordinals=False):
            assert 0 <= n <= 999
            if n in _SHORT_ORDINAL_UK and ordinals:
                return _SHORT_ORDINAL_UK[n]
            if n <= 19:
                return digits[n]
            elif n <= 99:
                q, r = divmod(n, 10)
                return tens[q - 1] + (" " + _sub_thousand(r, ordinals) if r
                                      else "")
            else:
                q, r = divmod(n, 100)
                return _NUM_STRING_UK[q * 100] + (" " + _sub_thousand(r, ordinals) if r else "")

        def _short_scale(n):
            if n > max(_SHORT_SCALE_UK.keys()):
                return "нескінченність"
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
                    if ordi:
                        if i * 1000 in _SHORT_ORDINAL_UK:
                            if z == 1:
                                number = _SHORT_ORDINAL_UK[i * 1000]
                            else:
                                if z > 5:
                                    number = number[:-1] + "и"
                                number += _SHORT_ORDINAL_UK[i * 1000]
                        else:
                            if n not in _SHORT_SCALE_UK:
                                num = int("1" + "0" * (len(str(n)) // 3 * 3))

                                if number[-3:] == "два":
                                    number = number[:-1] + "ох"
                                elif number[-2:] == "ри" or number[-2:] == "ре":
                                    number = number[:-1] + "ьох"
                                elif number[-1:] == "ь":
                                    number = number[:-1] + "и"

                                if _SHORT_SCALE_UK[num].endswith('н'):
                                    number += _SHORT_SCALE_UK[num] + "ний"
                                else:
                                    number += _SHORT_SCALE_UK[num] + "ий"
                            else:
                                if _SHORT_SCALE_UK[n].endswith('н'):
                                    number = _SHORT_SCALE_UK[n] + "ний"
                                else:
                                    number = _SHORT_SCALE_UK[n] + "ий"
                    elif z == 1:
                        number = hundreds[i - 1]
                    else:
                        if i == 1:
                            if z % 10 == 1 and z % 100 // 10 != 1:
                                number = number[:-2] + "на"
                            elif z % 10 == 2 and z % 100 // 10 != 1:
                                number = number[:-1] + "і"
                            number += " " + plural_uk(z, "тисяча", "тисячі", "тисяч")
                        elif 1 <= z % 10 <= 4 and z % 100 // 10 != 1:
                            number += " " + hundreds[i - 1] + "а"
                        else:
                            number += " " + hundreds[i - 1] + "ів"

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

        def _long_scale(n):
            if n >= max(_LONG_SCALE_UK.keys()):
                return "нескінченність"
            ordi = ordinals
            if int(n) != n:
                ordi = False
            n = int(n)
            assert 0 <= n
            res = []
            for i, z in enumerate(_split_by(n, 1000000)):
                if not z:
                    continue
                number = pronounce_number_uk(z, places, True, scientific,
                                             ordinals=ordi and not i)
                # strip off the comma after the thousand
                if i:
                    if i >= len(hundreds):
                        return ""
                    # plus one as we skip 'thousand'
                    # (and 'hundred', but this is excluded by index value)
                    number = number.replace(',', '')

                    if ordi:
                        if (i + 1) * 1000000 in _LONG_ORDINAL_UK:
                            if z == 1:
                                number = _LONG_ORDINAL_UK[
                                    (i + 1) * 1000000]
                            else:
                                number += _LONG_ORDINAL_UK[
                                    (i + 1) * 1000000]
                        else:
                            if n not in _LONG_SCALE_UK:
                                num = int("1" + "0" * (len(str(n)) // 3 * 3))

                                if number[-3:] == "два":
                                    number = number[:-1] + "ох"
                                elif number[-2:] == "ри" or number[-2:] == "ре":
                                    number = number[:-1] + "ьох"
                                elif number[-1:] == "ь":
                                    number = number[:-1] + "и"

                                number += _LONG_SCALE_UK[num] + "ний"
                            else:
                                number = " " + _LONG_SCALE_UK[n] + "ний"
                    elif z == 1:
                        number = hundreds[i]
                    elif z <= 4:
                        number += " " + hundreds[i] + "а"
                    else:
                        number += " " + hundreds[i] + "ів"

                res.append(number)
            return " ".join(reversed(res))

        if short_scale:
            result += _short_scale(num)
        else:
            result += _long_scale(num)

    # deal with scientific notation unpronounceable as number
    if not result and "e" in str(num):
        return pronounce_number_uk(num, places, short_scale, scientific=True)
    # Deal with fractional part
    elif not num == int(num) and places > 0:
        if abs(num) < 1.0 and (result == "мінус " or not result):
            result += "нуль"
        result += " крапка"
        _num_str = str(num)
        _num_str = _num_str.split(".")[1][0:places]
        for char in _num_str:
            result += " " + number_names[int(char)]
    return result


def numbers_to_digits_uk(text, short_scale=True, ordinals=False):
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
        _extract_numbers_with_text_uk(tokens, short_scale, ordinals)
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


def _extract_numbers_with_text_uk(tokens, short_scale=True,
                                  ordinals=False, fractional_numbers=True):
    """
    Extract all numbers from a list of Tokens, with the words that
    represent them.

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
            _extract_number_with_text_uk(tokens, short_scale,
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


def _extract_number_with_text_uk(tokens, short_scale=True,
                                 ordinals=False, fractional_numbers=True):
    """
    This function extracts a number from a list of Tokens.

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
        _extract_number_with_text_uk_helper(tokens, short_scale,
                                            ordinals, fractional_numbers)
    return ReplaceableNumber(number, tokens)


def _extract_number_with_text_uk_helper(tokens,
                                        short_scale=True, ordinals=False,
                                        fractional_numbers=True):
    """
    Helper for _extract_number_with_text_uk.

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
            _extract_fraction_with_text_uk(tokens, short_scale, ordinals)
        if fraction:
            return fraction, fraction_text

        decimal, decimal_text = \
            _extract_decimal_with_text_uk(tokens, short_scale, ordinals)
        if decimal:
            return decimal, decimal_text
    # special_number = [word for word in tokens if word ]
    # short_scale == False
    return _extract_whole_number_with_text_uk(tokens, short_scale, ordinals)


def _extract_fraction_with_text_uk(tokens, short_scale, ordinals):
    """
    Extract fraction numbers from a string.

    This function handles text such as '2 and 3/4'. Note that "one half" or
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
    for c in _FRACTION_MARKER:
        partitions = partition_list(tokens, lambda t: t.word == c)

        if len(partitions) == 3:
            numbers1 = \
                _extract_numbers_with_text_uk(partitions[0], short_scale,
                                              ordinals, fractional_numbers=False)
            numbers2 = \
                _extract_numbers_with_text_uk(partitions[2], short_scale,
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


def _extract_decimal_with_text_uk(tokens, short_scale, ordinals):
    """
    Extract decimal numbers from a string.

    This function handles text such as '2 point 5'.

    Notes:
        While this is a helper for extract_number_xx, it also depends on
        extract_number_xx, to parse out the components of the decimal.

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
    for c in _DECIMAL_MARKER:
        partitions = partition_list(tokens, lambda t: t.word == c)

        if len(partitions) == 3:
            numbers1 = \
                _extract_numbers_with_text_uk(partitions[0], short_scale,
                                              ordinals, fractional_numbers=False)
            numbers2 = \
                _extract_numbers_with_text_uk(partitions[2], short_scale,
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


def _extract_whole_number_with_text_uk(tokens, short_scale, ordinals):
    """
    Handle numbers not handled by the decimal or fraction functions. This is
    generally whole numbers. Note that phrases such as "one half" will be
    handled by this function, while "one and a half" are handled by the
    fraction function.

    Args:
        tokens [Token]:
        short_scale boolean:
        ordinals boolean:

    Returns:
        int or float, [Tokens]
        The value parsed, and tokens that it corresponds to.

    """
    number_token = [token for token in tokens if token.word.lower() in _MULTIPLIES_LONG_SCALE_UK]
    if number_token:
        short_scale = False
    multiplies, string_num_ordinal, string_num_scale = \
        _initialize_number_data(short_scale)
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
        if word in word in _NEGATIVES:
            number_words.append(token)
            continue

        prev_word = tokens[idx - 1].word if idx > 0 else ""
        prev_word = _text_uk_inflection_normalize(prev_word, 1)
        next_word = tokens[idx + 1].word if idx + 1 < len(tokens) else ""
        next_word = _text_uk_inflection_normalize(next_word, 1)

        # In Ukrainian (?) we do not use suffix (1st,2nd,..) but use point instead (1.,2.,..)
        if is_numeric(word[:-1]) and \
                (word.endswith(".")):
            # explicit ordinals, 1st, 2nd, 3rd, 4th.... Nth
            word = word[:-1]

        # Normalize Ukrainian inflection of numbers (один, одна, одно,...)
        if not ordinals:
            if word not in _STRING_NUM_UK:
                word = _text_uk_inflection_normalize(word, 1)

        if word not in string_num_scale and \
                word not in _STRING_NUM_UK and \
                word not in _SUMS and \
                word not in multiplies and \
                not (ordinals and word in string_num_ordinal) and \
                not is_numeric(word) and \
                not is_fractional_uk(word, word, short_scale=short_scale) and \
                not look_for_fractions(word.split('/')):
            words_only = [token.word for token in number_words]
            if number_words and not all([w in _NEGATIVES for w in words_only]):
                break
            else:
                number_words = []
                continue
        elif word not in multiplies \
                and prev_word not in multiplies \
                and prev_word not in _SUMS \
                and not (ordinals and prev_word in string_num_ordinal) \
                and prev_word not in _NEGATIVES:

            number_words = [token]
        elif prev_word in _SUMS and word in _SUMS:
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
        if word in _STRING_NUM_UK:
            val = _STRING_NUM_UK.get(word)
            current_val = val
        elif word in string_num_scale:
            val = string_num_scale.get(word)
            current_val = val
        elif ordinals and word in string_num_ordinal:
            val = string_num_ordinal[word]
            current_val = val
        # is the prev word an ordinal number and current word is one?
        # second one, third one
        if ordinals and prev_word in string_num_ordinal and val == 1:
            val = prev_val
        # is the prev word a number and should we sum it?
        # twenty two, fifty six
        if (prev_word in _SUMS and val and val < 10) \
                or (prev_word in _SUMS and val and val < 100 and prev_val >= 100) \
                or all([prev_word in multiplies, val < prev_val if prev_val else False]):
            val = prev_val + val

        # is the prev word a number and should we multiply it?
        multiplies.update({"тисячa", "тисячі", "тисячу", "тисячах", "тисячaми", "тисячею", "тисяч"})
        if word in multiplies:
            if not prev_val:
                prev_val = 1
            val = prev_val * val

        # пара сотень, три пари пива
        if prev_word in ['пара', 'пари', 'парою', 'парами'] and current_val != 1000.0:
            val = val * 2
        if prev_val in _STRING_NUM_UK.values() and current_val == 100:
            val = prev_val * current_val

        # half cup
        if val is False:
            val = is_fractional_uk(word, word, short_scale=short_scale)
            current_val = val

        # 2 fifths
        if not ordinals:
            next_val = is_fractional_uk(next_word, word, short_scale=short_scale)
            if next_val:
                if not val:
                    val = 1
                val = val * next_val
                number_words.append(tokens[idx + 1])
        if word in ['пара', 'пари', 'парою', 'парами']:
            if prev_val:
                val = val * prev_val
            else:
                val = 2
        # is this a negative number?
        if val and prev_word and prev_word in _NEGATIVES:
            val = 0 - val

        # let's make sure it isn't a fraction
        if not val:
            # look for fractions like "2/3"
            a_pieces = word.split('/')
            if look_for_fractions(a_pieces):
                val = float(a_pieces[0]) / float(a_pieces[1])
        else:
            # checking if word is digit in order not to substitute
            # existing calculated value
            new_word = re.sub(r'\.', '', word)
            if all([
                prev_word in _SUMS,
                word not in _SUMS,
                new_word.isdigit() is False,
                word not in multiplies,
                current_val >= 10
            ]):
                # Backtrack - we've got numbers we can't sum.
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
                time_to_sum = True
                for other_token in tokens[idx + 1:]:
                    if other_token.word in multiplies:
                        if string_num_scale[other_token.word] >= current_val:
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


def _initialize_number_data(short_scale):
    """
    Generate dictionaries of words to numbers, based on scale.

    This is a helper function for _extract_whole_number.

    Args:
        short_scale boolean:

    Returns:
        (set(str), dict(str, number), dict(str, number))
        multiplies, string_num_ordinal, string_num_scale

    """
    multiplies = _MULTIPLIES_SHORT_SCALE_UK if short_scale \
        else _MULTIPLIES_LONG_SCALE_UK

    string_num_ordinal_uk = _STRING_SHORT_ORDINAL_UK if short_scale \
        else _STRING_LONG_ORDINAL_UK

    string_num_scale_uk = _SHORT_SCALE_UK if short_scale else _LONG_SCALE_UK
    string_num_scale_uk = invert_dict(string_num_scale_uk)
    string_num_scale_uk.update(generate_plurals_uk(string_num_scale_uk))
    return multiplies, string_num_ordinal_uk, string_num_scale_uk


def extract_number_uk(text, short_scale=True, ordinals=False):
    """
    This function extracts a number from a text string,
    handles pronunciations in long scale and short scale

    https://en.wikipedia.org/wiki/Names_of_large_numbers

    Args:
        text (str): the string to normalize
        short_scale (bool): use short scale if True, long scale if False
        ordinals (bool): consider ordinal numbers, third=3 instead of 1/3
    Returns:
        (int) or (float) or False: The extracted number or False if no number
                                   was found

    """
    return _extract_number_with_text_uk(tokenize(text.lower()),
                                        short_scale, ordinals).value


def is_fractional_uk(input_str, word, short_scale=True):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): use short scale if True, long scale if False
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    fractions = {"ціла": 1}
    # endings for creation different cases and plurals in different cases
    ending = ['ої', 'е', 'их', 'ою', 'і', 'ими', 'ій']
    for num in _FRACTION_STRING_UK.keys():  # Numbers from 2 to 1 hundred, more is not usually used in common speech
        if num > 1:
            fractions[str(_FRACTION_STRING_UK[num])] = num
            for end in ending:
                new_fraction_number = _FRACTION_STRING_UK[num][:-1] + end
                fractions[new_fraction_number] = num
    fractions.update({
        "половина": 2, "половиною": 2, "половини": 2, "половин": 2, "половинами": 2, "пів": 2,
        "шоста": 6,
        "третина": 1 / 3, "треть": 1 / 3, "треті": 3, "третьої": 3,
        "чверті": 4, "чверть": 0.25, "чвертю": 0.25
    })
    if input_str.lower() in fractions.keys():
        if word == input_str:
            return fractions[input_str.lower()]
        elif word not in _STRING_NUM_UK:
            return fractions[input_str.lower()]
        else:
            return 1.0 / fractions[input_str.lower()]
    return False


def _text_uk_inflection_normalize(word, arg):
    """
    Ukrainian Inflection normalizer.

    This try to normalize known inflection. This function is called
    from multiple places, each one is defined with arg.

    Args:
        word [Word]
        arg [Int]

    Returns:
        word [Word]

    """

    if arg == 1:  # _extract_whole_number_with_text_uk
        if word in ["одна", "одним", "одно", "одною", "одного", "одної", "одному", "одній", "одного", "одну"]:
            return "один"
        return _plurals_normalizer(word)

    elif arg == 2:  # extract_datetime_uk
        if word in ["година", "години", "годин", "годину", "годин", "годинами"]:
            return "година"
        if word in ["хвилина", "хвилини", "хвилину", "хвилин", "хвилька"]:
            return "хвилина"
        if word in ["секунд", "секунди", "секундами", "секунду", "секунд", "сек"]:
            return "секунда"
        if word in ["днів", "дні", "днями", "дню", "днем", "днями"]:
            return "день"
        if word in ["тижні", "тижнів", "тижнями", "тиждень", "тижня"]:
            return "тиждень"
        if word in ["місяцем", "місяці", "місяця", "місяцях", "місяцем", "місяцями", "місяців"]:
            return "місяць"
        if word in ["року", "роки", "році", "роках", "роком", "роками", "років"]:
            return "рік"
        if word in _WORDS_MORNING_UK:
            return "вранці"
        if word in ["опівдні", "півдня"]:
            return "південь"
        if word in _WORDS_EVENING_UK:
            return "ввечері"
        if word in _WORDS_NIGHT_UK:
            return "ніч"
        if word in ["вікенд", "вихідних", "вихідними"]:
            return "вихідні"
        if word in ["столітті", "століттях", "століть"]:
            return "століття"
        if word in ["десятиліття", "десятиліть", "десятиліттях"]:
            return "десятиліття"
        if word in ["столітті", "століттях", "століть"]:
            return "століття"

        # Week days
        if word in ["понеділка", "понеділки"]:
            return "понеділок"
        if word in ["вівторка", "вівторки"]:
            return "вівторок"
        if word in ["середу", "середи"]:
            return "среда"
        if word in ["четверга"]:
            return "четвер"
        if word in ["п'ятницю", "п'ятниці"]:
            return "п'ятниця"
        if word in ["суботу", "суботи"]:
            return "субота"
        if word in ["неділю", "неділі"]:
            return "неділя"

        # Months
        if word in ["лютому", "лютого", "лютим"]:
            return "лютий"
        if word in ["листопада", "листопаді", "листопадом"]:
            return "листопад"
        tmp = ''
        if word[-3:] in ["ого", "ому"]:
            tmp = word[:-3] + "ень"
        elif word[-2:] in ["ні", "ня"]:
            tmp = word[:-2] + "ень"
    return word


def _plurals_normalizer(word):
    """
    Ukrainian Plurals normalizer.

    This function normalizes plural endings of numerals
    including different case variations.
    Uses _PLURALS dictionary with exceptions that can not
    be covered by rules.
    Args:
        word [Word]

    Returns:
        word [Word]

    """
    if word not in _STRING_NUM_UK:
        # checking for plurals 2-10
        for key, value in _PLURALS.items():
            if word == key:
                return _NUM_STRING_UK[value]

        # checking for plurals 11-19
        case_endings = ['надцяти', 'надцятим', 'надцятими',
                        'надцятьох', 'надцятьма', 'надцятьома', 'надцятьом']
        plural_case = ''.join([case for case in case_endings if case in word])
        if plural_case:
            if 'один' in word:
                return "одинадцять"
            word = word.replace(plural_case, '') + 'надцять'
            return word

        # checking for plurals 20,30
        case_endings = ['дцяти', 'дцятим', 'дцятими',
                        'дцятьох', 'дцятьма', 'дцятьома', 'дцятьом']
        plural_case = ''.join([case for case in case_endings if case in word])
        if plural_case:
            word = word.replace(plural_case, '') + 'дцять'
            return word

        # checking for plurals 50, 60, 70, 80
        case_endings = ['десятьох', 'десяти', 'десятьом',
                        'десятьма', 'десятьома']
        plural_case = ''.join([case for case in case_endings if case in word])
        if plural_case:
            word = word.replace(plural_case, '') + 'десят'
            return word

        # checking for plurals 90, 100
        case_endings = ['стам', 'стами', 'стах',
                        'стами', 'ста', 'сот']
        plural_case = ''.join([case for case in case_endings if case in word])
        if plural_case:
            word = word.replace(plural_case, '')
            for key, value in _PLURALS.items():
                if word == key:
                    firs_part = _NUM_STRING_UK[value]
                    if value in [3, 4]:
                        word = firs_part + 'ста'
                    elif value in [5, 6, 9]:
                        word = firs_part[:-1] + 'сот'
                    elif value in [7, 8]:
                        word = firs_part + 'сот'
                    return word
            return word
    return word


def plural_uk(num: int, one: str, few: str, many: str):
    num %= 100
    if num // 10 == 1:
        return many
    if num % 10 == 1:
        return one
    if 2 <= num % 10 <= 4:
        return few
    return many
