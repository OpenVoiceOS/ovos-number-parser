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
from collections import OrderedDict

from ovos_number_parser.util import convert_to_mixed_fraction, is_numeric, look_for_fractions, \
    invert_dict, ReplaceableNumber, partition_list, tokenize, Token

_NUM_STRING_RU = {
    0: 'ноль',
    1: 'один',
    2: 'два',
    3: 'три',
    4: 'четыре',
    5: 'пять',
    6: 'шесть',
    7: 'семь',
    8: 'восемь',
    9: 'девять',
    10: 'десять',
    11: 'одиннадцать',
    12: 'двенадцать',
    13: 'тринадцать',
    14: 'четырнадцать',
    15: 'пятнадцать',
    16: 'шестнадцать',
    17: 'семнадцать',
    18: 'восемнадцать',
    19: 'девятнадцать',
    20: 'двадцать',
    30: 'тридцать',
    40: 'сорок',
    50: 'пятьдесят',
    60: 'шестьдесят',
    70: 'семьдесят',
    80: 'восемьдесят',
    90: 'девяносто',
    100: 'сто',
    200: 'двести',
    300: 'триста',
    400: 'четыреста',
    500: 'пятьсот',
    600: 'шестьсот',
    700: 'семьсот',
    800: 'восемьсот',
    900: 'девятьсот'
}

_FRACTION_STRING_RU = {
    2: 'половина',
    3: 'треть',
    4: 'четверть',
    5: 'пятая',
    6: 'шестая',
    7: 'седьмая',
    8: 'восьмая',
    9: 'девятая',
    10: 'десятая',
    11: 'одиннадцатая',
    12: 'двенадцатая',
    13: 'тринадцатая',
    14: 'четырнадцатая',
    15: 'пятнадцатая',
    16: 'шестнадцатая',
    17: 'семнадцатая',
    18: 'восемнадцатая',
    19: 'девятнадцатая',
    20: 'двадцатая',
    30: 'тридцатая',
    40: 'сороковая',
    50: 'пятидесятая',
    60: 'шестидесятая',
    70: 'семидесятая',
    80: 'восьмидесятая',
    90: 'девяностая',
    1e2: 'сотая',
    1e3: 'тысячная',
    1e6: 'миллионная',
    1e9: 'миллиардная'
}

_SHORT_SCALE_RU = OrderedDict([
    (1e3, 'тысяча'),
    (1e6, "миллион"),
    (1e9, "миллиард"),
    (1e12, "триллион"),
    (1e15, "квадриллион"),
    (1e18, "квинтиллион"),
    (1e21, "секстиллион"),
    (1e24, "септиллион"),
    (1e27, "октиллион"),
    (1e30, "нониллион"),
    (1e33, "дециллион"),
    (1e36, "ундециллион"),
    (1e39, "дуодециллион"),
    (1e42, "тредециллион"),
    (1e45, "кваттордециллион"),
    (1e48, "квиндециллион"),
    (1e51, "сексдециллион"),
    (1e54, "септендециллион"),
    (1e57, "октодециллион"),
    (1e60, "новемдециллион"),
    (1e63, "вигинтиллион"),
    (1e66, "унвигинтиллион"),
    (1e69, "дуовигинтиллион"),
    (1e72, "тревигинтиллион"),
    (1e75, "кватторвигинтиллион"),
    (1e78, "квинвигинтиллион"),
    (1e81, "секснвигинтиллион"),
    (1e84, "септенвигинтиллион"),
    (1e87, "октовигинтиллион"),
    (1e90, "новемвигинтиллион"),
    (1e93, "тригинтиллион"),
])

_LONG_SCALE_RU = OrderedDict([
    (1e3, 'тысяча'),
    (1e6, "миллион"),
    (1e9, "миллиард"),
    (1e12, "биллион"),
    (1e15, "биллиард"),
    (1e18, "триллион"),
    (1e21, "триллиард"),
    (1e24, "квадриллион"),
    (1e27, "квадриллиард"),
    (1e30, "квинтиллион"),
    (1e33, "квинтиллиард"),
    (1e36, "секстиллион"),
    (1e39, "секстиллиард"),
    (1e42, "септиллион"),
    (1e45, "септиллиард"),
    (1e48, "октиллион"),
    (1e51, "октиллиард"),
    (1e54, "нониллион"),
    (1e57, "нониллиард"),
    (1e60, "дециллион"),
    (1e63, "дециллиард"),
    (1e66, "ундециллион"),
    (1e72, "дуодециллион"),
    (1e78, "тредециллион"),
    (1e84, "кваттордециллион"),
    (1e90, "квиндециллион"),
    (1e96, "сексдециллион"),
    (1e102, "септендециллион"),
    (1e108, "октодециллион"),
    (1e114, "новемдециллион"),
    (1e120, "вигинтиллион"),
])

_ORDINAL_BASE_RU = {
    1: 'первый',
    2: 'второй',
    3: 'третий',
    4: 'четвёртый',
    5: 'пятый',
    6: 'шестой',
    7: 'седьмой',
    8: 'восьмой',
    9: 'девятый',
    10: 'десятый',
    11: 'одиннадцатый',
    12: 'двенадцатый',
    13: 'тринадцатый',
    14: 'четырнадцатый',
    15: 'пятнадцатый',
    16: 'шестнадцатый',
    17: 'семнадцатый',
    18: 'восемнадцатый',
    19: 'девятнадцатый',
    20: 'двадцатый',
    30: 'тридцатый',
    40: "сороковой",
    50: "пятидесятый",
    60: "шестидесятый",
    70: "семидесятый",
    80: "восьмидесятый",
    90: "девяностый",
    1e2: "сотый",
    2e2: "двухсотый",
    3e2: "трёхсотый",
    4e2: "четырёхсотый",
    5e2: "пятисотый",
    6e2: "шестисотый",
    7e2: "семисотый",
    8e2: "восьмисотый",
    9e2: "девятисотый",
    1e3: "тысячный"
}

_SHORT_ORDINAL_RU = {
    1e6: "миллион",
    1e9: "миллиард",
    1e12: "триллион",
    1e15: "квадриллион",
    1e18: "квинтиллион",
    1e21: "секстиллион",
    1e24: "септиллион",
    1e27: "октиллион",
    1e30: "нониллион",
    1e33: "дециллион",
    1e36: "ундециллион",
    1e39: "дуодециллион",
    1e42: "тредециллион",
    1e45: "кваттордециллион",
    1e48: "квиндециллион",
    1e51: "сексдециллион",
    1e54: "септендециллион",
    1e57: "октодециллион",
    1e60: "новемдециллион",
    1e63: "вигинтиллион"
}
_SHORT_ORDINAL_RU.update(_ORDINAL_BASE_RU)

_LONG_ORDINAL_RU = {
    1e6: "миллион",
    1e9: "миллиард",
    1e12: "биллион",
    1e15: "биллиард",
    1e18: "триллион",
    1e21: "триллиард",
    1e24: "квадриллион",
    1e27: "квадриллиард",
    1e30: "квинтиллион",
    1e33: "квинтиллиард",
    1e36: "секстиллион",
    1e39: "секстиллиард",
    1e42: "септиллион",
    1e45: "септиллиард",
    1e48: "октиллион",
    1e51: "октиллиард",
    1e54: "нониллион",
    1e57: "нониллиард",
    1e60: "дециллион",
    1e63: "дециллиард",
    1e66: "ундециллион",
    1e72: "дуодециллион",
    1e78: "тредециллион",
    1e84: "кваттордециллион",
    1e90: "квиндециллион",
    1e96: "сексдециллион",
    1e102: "септендециллион",
    1e108: "октодециллион",
    1e114: "новемдециллион",
    1e120: "вигинтиллион"
}
_LONG_ORDINAL_RU.update(_ORDINAL_BASE_RU)


def generate_plurals_ru(originals):
    """
    Return a new set or dict containing the plural form of the original values,

    In English this means all with 's' appended to them.

    Args:
        originals set(str) or dict(str, any): values to pluralize

    Returns:
        set(str) or dict(str, any)

    """
    suffixes = ["а", "ах", "ам", "ами", "ные", "ный", "ов", "ом", "ы"]
    if isinstance(originals, dict):
        return {key + suffix: value for key, value in originals.items() for suffix in suffixes}
    return {value + suffix for value in originals for suffix in suffixes}


# negate next number (-2 = 0 - 2)
_NEGATIVES = {"минус"}

# sum the next number (twenty two = 20 + 2)
_SUMS = {'двадцать', '20', 'тридцать', '30', 'сорок', '40', 'пятьдесят', '50',
         'шестьдесят', '60', 'семьдесят', '70', 'восемьдесят', '80', 'девяносто', '90',
         'сто', '100', 'двести', '200', 'триста', '300', 'четыреста', '400',
         'пятьсот', '500', 'шестьсот', '600', 'семьсот', '700', 'восемьсот', '800',
         'девятьсот', '900'}

_MULTIPLIES_LONG_SCALE_RU = set(_LONG_SCALE_RU.values()) | \
                            generate_plurals_ru(_LONG_SCALE_RU.values())

_MULTIPLIES_SHORT_SCALE_RU = set(_SHORT_SCALE_RU.values()) | \
                             generate_plurals_ru(_SHORT_SCALE_RU.values())

# split sentence parse separately and sum ( 2 and a half = 2 + 0.5 )
_FRACTION_MARKER = {"и", "с", " "}

# decimal marker ( 1 point 5 = 1 + 0.5)
_DECIMAL_MARKER = {"целая", "целых", "точка", "запятая"}

_STRING_NUM_RU = invert_dict(_NUM_STRING_RU)
_STRING_NUM_RU.update({
    "тысяч": 1e3,
})
_STRING_NUM_RU.update(generate_plurals_ru(_STRING_NUM_RU))
_STRING_NUM_RU.update({
    "четверти": 0.25,
    "четвёртая": 0.25,
    "четвёртых": 0.25,
    "третья": 1 / 3,
    "третяя": 1 / 3,
    "вторая": 0.5,
    "вторых": 0.5,
    "половина": 0.5,
    "половиной": 0.5,
    "пол": 0.5,
    "одна": 1,
    "двойка": 2,
    "двое": 2,
    "пара": 2,
    "сот": 100,
    "сотен": 100,
    "сотни": 100,
    "сотня": 100,
})

_WORDS_NEXT_RU = [
    "будущая", "будущее", "будущей", "будущий", "будущим", "будущую",
    "новая", "новое", "новой", "новый", "новым",
    "следующая", "следующее", "следующей", "следующем", "следующий", "следующую",
]
_WORDS_PREV_RU = [
    "предыдущая", "предыдущем", "предыдущей", "предыдущий", "предыдущим", "предыдущую",
    "прошедшая", "прошедшем", "прошедшей", "прошедший", "прошедшим", "прошедшую",
    "прошлая", "прошлой", "прошлом", "прошлую", "прошлый", "прошлым",
    "том", "тот",
]
_WORDS_CURRENT_RU = [
    "данная", "данное", "данном", "данный",
    "настойщая", "настоящее", "настойщем", "настойщем", "настойщий",
    "нынешняя", "нынешнее", "нынешней", "нынешнем", "нынешний",
    "текущая", "текущее", "текущей", "текущем", "текущий",
    "это", "этим", "этой", "этом", "этот", "эту",
]
_WORDS_NOW_RU = [
    "теперь",
    "сейчас",
]
_WORDS_MORNING_RU = ["утро", "утром"]
_WORDS_DAY_RU = ["днём"]
_WORDS_EVENING_RU = ["вечер", "вечером"]
_WORDS_NIGHT_RU = ["ночь", "ночью"]

_STRING_SHORT_ORDINAL_RU = invert_dict(_SHORT_ORDINAL_RU)
_STRING_LONG_ORDINAL_RU = invert_dict(_LONG_ORDINAL_RU)


def nice_number_ru(number, speech=True, denominators=range(1, 21)):
    """ English helper for nice_number

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
            # TODO: Number grouping?  E.g. "1,000,000"
            return str(whole)
        else:
            return '{} {}/{}'.format(whole, num, den)

    if num == 0:
        return str(whole)
    den_str = _FRACTION_STRING_RU[den]
    if whole == 0:
        if num == 1 and den <= 4:
            return_string = '{}'.format(den_str)
        else:
            return_string = '{} {}'.format(num, den_str)
    elif num == 1 and den == 2:
        return_string = '{} с половиной'.format(whole)
    else:
        return_string = '{} и {} {}'.format(whole, num, den_str)
    if 2 <= den <= 4:
        if 2 <= num <= 4:
            return_string = return_string[:-1] + 'и'
        elif num > 4:
            return_string = return_string[:-1] + 'ей'
    elif den >= 5:
        if 2 <= num <= 4:
            return_string = return_string[:-2] + 'ые'
        elif num > 4:
            return_string = return_string[:-2] + 'ых'

    return return_string


def pronounce_number_ru(number, places=2, short_scale=True, scientific=False,
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
        return "бесконечность"
    elif num == float("-inf"):
        return "минус бесконечность"
    if scientific:
        number = '%E' % num
        n, power = number.replace("+", "").split("E")
        power = int(power)
        if power != 0:
            if ordinals:
                # This handles negative powers separately from the normal
                # handling since each call disables the scientific flag
                return '{}{} на десять в {}{} степени'.format(
                    'минус ' if float(n) < 0 else '',
                    pronounce_number_ru(
                        abs(float(n)), places, short_scale, False, ordinals=True),
                    'минус ' if power < 0 else '',
                    pronounce_number_ru(abs(power), places, short_scale, False, ordinals=True))
            else:
                # This handles negative powers separately from the normal
                # handling since each call disables the scientific flag
                return '{}{} на десять в степени {}{}'.format(
                    'минус ' if float(n) < 0 else '',
                    pronounce_number_ru(
                        abs(float(n)), places, short_scale, False, ordinals=False),
                    'минус ' if power < 0 else '',
                    pronounce_number_ru(abs(power), places, short_scale, False, ordinals=False))

    if short_scale:
        number_names = _NUM_STRING_RU.copy()
        number_names.update(_SHORT_SCALE_RU)
    else:
        number_names = _NUM_STRING_RU.copy()
        number_names.update(_LONG_SCALE_RU)

    digits = [number_names[n] for n in range(0, 20)]

    tens = [number_names[n] for n in range(10, 100, 10)]

    if short_scale:
        hundreds = [_SHORT_SCALE_RU[n] for n in _SHORT_SCALE_RU.keys()]
    else:
        hundreds = [_LONG_SCALE_RU[n] for n in _LONG_SCALE_RU.keys()]

    # deal with negative numbers
    result = ""
    if num < 0:
        result = "минус "
    num = abs(num)

    # check for a direct match
    if num in number_names and not ordinals:
        result += number_names[num]
    else:
        def _sub_thousand(n, ordinals=False):
            assert 0 <= n <= 999
            if n in _SHORT_ORDINAL_RU and ordinals:
                return _SHORT_ORDINAL_RU[n]
            if n <= 19:
                return digits[n]
            elif n <= 99:
                q, r = divmod(n, 10)
                return tens[q - 1] + (" " + _sub_thousand(r, ordinals) if r
                                      else "")
            else:
                q, r = divmod(n, 100)
                return _NUM_STRING_RU[q * 100] + (" " + _sub_thousand(r, ordinals) if r else "")

        def _short_scale(n):
            if n > max(_SHORT_SCALE_RU.keys()):
                return "бесконечность"
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
                        if i * 1000 in _SHORT_ORDINAL_RU:
                            if z == 1:
                                number = _SHORT_ORDINAL_RU[i * 1000]
                            else:
                                if z > 5:
                                    number = number[:-1] + "и"
                                number += _SHORT_ORDINAL_RU[i * 1000]
                        else:
                            if n not in _SHORT_SCALE_RU:
                                num = int("1" + "0" * (len(str(n)) // 3 * 3))

                                if number[-3:] == "два":
                                    number = number[:-1] + "ух"
                                elif number[-2:] == "ри" or number[-2:] == "ре":
                                    number = number[:-1] + "ёх"
                                elif number[-1:] == "ь":
                                    number = number[:-1] + "и"

                                number += _SHORT_SCALE_RU[num] + "ный"
                            else:
                                number = _SHORT_SCALE_RU[n] + "ный"
                    elif z == 1:
                        number = hundreds[i - 1]
                    else:
                        if i == 1:
                            if z % 10 == 1 and z % 100 // 10 != 1:
                                number = number[:-2] + "на"
                            elif z % 10 == 2 and z % 100 // 10 != 1:
                                number = number[:-1] + "е"
                            number += " " + plural_ru(z, "тысяча", "тысячи", "тысяч")
                        elif 1 <= z % 10 <= 4 and z % 100 // 10 != 1:
                            number += " " + hundreds[i - 1] + "а"
                        else:
                            number += " " + hundreds[i - 1] + "ов"

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
            if n >= max(_LONG_SCALE_RU.keys()):
                return "бесконечность"
            ordi = ordinals
            if int(n) != n:
                ordi = False
            n = int(n)
            assert 0 <= n
            res = []
            for i, z in enumerate(_split_by(n, 1000000)):
                if not z:
                    continue
                number = pronounce_number_ru(z, places, True, scientific,
                                             ordinals=ordi and not i)
                # strip off the comma after the thousand
                if i:
                    if i >= len(hundreds):
                        return ""
                    # plus one as we skip 'thousand'
                    # (and 'hundred', but this is excluded by index value)
                    number = number.replace(',', '')

                    if ordi:
                        if (i + 1) * 1000000 in _LONG_ORDINAL_RU:
                            if z == 1:
                                number = _LONG_ORDINAL_RU[
                                    (i + 1) * 1000000]
                            else:
                                number += _LONG_ORDINAL_RU[
                                    (i + 1) * 1000000]
                        else:
                            if n not in _LONG_SCALE_RU:
                                num = int("1" + "0" * (len(str(n)) // 3 * 3))

                                if number[-3:] == "два":
                                    number = number[:-1] + "ух"
                                elif number[-2:] == "ри" or number[-2:] == "ре":
                                    number = number[:-1] + "ёх"
                                elif number[-1:] == "ь":
                                    number = number[:-1] + "и"

                                number += _LONG_SCALE_RU[num] + "ный"
                            else:
                                number = " " + _LONG_SCALE_RU[n] + "ный"
                    elif z == 1:
                        number = hundreds[i]
                    elif z <= 4:
                        number += " " + hundreds[i] + "а"
                    else:
                        number += " " + hundreds[i] + "ов"

                res.append(number)
            return " ".join(reversed(res))

        if short_scale:
            result += _short_scale(num)
        else:
            result += _long_scale(num)

    # deal with scientific notation unpronounceable as number
    if not result and "e" in str(num):
        return pronounce_number_ru(num, places, short_scale, scientific=True)
    # Deal with fractional part
    elif not num == int(num) and places > 0:
        if abs(num) < 1.0 and (result == "минус " or not result):
            result += "ноль"
        result += " точка"
        _num_str = str(num)
        _num_str = _num_str.split(".")[1][0:places]
        for char in _num_str:
            result += " " + number_names[int(char)]
    return result


def plural_ru(num: int, one: str, few: str, many: str):
    num %= 100
    if num // 10 == 1:
        return many
    if num % 10 == 1:
        return one
    if 2 <= num % 10 <= 4:
        return few
    return many


def numbers_to_digits_ru(text, short_scale=True, ordinals=False):
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
        _extract_numbers_with_text_ru(tokens, short_scale, ordinals)
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


def _extract_numbers_with_text_ru(tokens, short_scale=True,
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
            _extract_number_with_text_ru(tokens, short_scale,
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


def _extract_number_with_text_ru(tokens, short_scale=True,
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
        _extract_number_with_text_ru_helper(tokens, short_scale,
                                            ordinals, fractional_numbers)
    return ReplaceableNumber(number, tokens)


def _extract_number_with_text_ru_helper(tokens,
                                        short_scale=True, ordinals=False,
                                        fractional_numbers=True):
    """
    Helper for _extract_number_with_text_en.

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
            _extract_fraction_with_text_ru(tokens, short_scale, ordinals)
        if fraction:
            return fraction, fraction_text

        decimal, decimal_text = \
            _extract_decimal_with_text_ru(tokens, short_scale, ordinals)
        if decimal:
            return decimal, decimal_text

    return _extract_whole_number_with_text_ru(tokens, short_scale, ordinals)


def _extract_fraction_with_text_ru(tokens, short_scale, ordinals):
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
                _extract_numbers_with_text_ru(partitions[0], short_scale,
                                              ordinals, fractional_numbers=False)
            numbers2 = \
                _extract_numbers_with_text_ru(partitions[2], short_scale,
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


def _extract_decimal_with_text_ru(tokens, short_scale, ordinals):
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
                _extract_numbers_with_text_ru(partitions[0], short_scale,
                                              ordinals, fractional_numbers=False)
            numbers2 = \
                _extract_numbers_with_text_ru(partitions[2], short_scale,
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


def _extract_whole_number_with_text_ru(tokens, short_scale, ordinals):
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
        next_word = tokens[idx + 1].word if idx + 1 < len(tokens) else ""

        # In Russian (?) we do no use suffix (1st,2nd,..) but use point instead (1.,2.,..)
        if is_numeric(word[:-1]) and \
                (word.endswith(".")):
            # explicit ordinals, 1st, 2nd, 3rd, 4th.... Nth
            word = word[:-1]

            # handle nth one
        #    if next_word == "one":
        # would return 1 instead otherwise
        #        tokens[idx + 1] = Token("", idx)
        #        next_word = ""

        # Normalize Russian inflection of numbers (один, одна, одно,...)
        if not ordinals:
            word = _text_ru_inflection_normalize(word, 1)

        if word not in string_num_scale and \
                word not in _STRING_NUM_RU and \
                word not in _SUMS and \
                word not in multiplies and \
                not (ordinals and word in string_num_ordinal) and \
                not is_numeric(word) and \
                not is_fractional_ru(word, short_scale=short_scale) and \
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
        if word in _STRING_NUM_RU:
            val = _STRING_NUM_RU.get(word)
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
        # twenty hundred, six hundred
        if word in multiplies:
            if not prev_val:
                prev_val = 1
            val = prev_val * val

        # is this a spoken fraction?
        # half cup
        if val is False:
            val = is_fractional_ru(word, short_scale=short_scale)
            current_val = val

        # 2 fifths
        if not ordinals:
            next_val = is_fractional_ru(next_word, short_scale=short_scale)
            if next_val:
                if not val:
                    val = 1
                val = val * next_val
                number_words.append(tokens[idx + 1])

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
            if all([
                prev_word in _SUMS,
                word not in _SUMS,
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
    multiplies = _MULTIPLIES_SHORT_SCALE_RU if short_scale \
        else _MULTIPLIES_LONG_SCALE_RU

    string_num_ordinal_ru = _STRING_SHORT_ORDINAL_RU if short_scale \
        else _STRING_LONG_ORDINAL_RU

    string_num_scale_ru = _SHORT_SCALE_RU if short_scale else _LONG_SCALE_RU
    string_num_scale_ru = invert_dict(string_num_scale_ru)
    string_num_scale_ru.update(generate_plurals_ru(string_num_scale_ru))
    return multiplies, string_num_ordinal_ru, string_num_scale_ru


def extract_number_ru(text, short_scale=True, ordinals=False):
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
    return _extract_number_with_text_ru(tokenize(text.lower()),
                                        short_scale, ordinals).value


def is_fractional_ru(input_str, short_scale=True):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): use short scale if True, long scale if False
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    if input_str[-3:] in ["тые", "тых"]:  # leading number is bigger than one (две четвёртые, три пятых)
        input_str = input_str[-3:] + "тая"
    fractions = {"целая": 1}  # first four numbers have little different format

    for num in _FRACTION_STRING_RU:  # Numbers from 2 to 1 hundred, more is not usually used in common speech
        if num > 1:
            fractions[_FRACTION_STRING_RU[num]] = num

    if input_str.lower() in fractions:
        return 1.0 / fractions[input_str.lower()]
    return False


def _text_ru_inflection_normalize(word, arg):
    """
    Russian Inflection normalizer.

    This try to normalize known inflection. This function is called
    from multiple places, each one is defined with arg.

    Args:
        word [Word]
        arg [Int]

    Returns:
        word [Word]

    """
    if word in ["тысяч", "тысячи"]:
        return "тысяча"

    if arg == 1:  # _extract_whole_number_with_text_ru
        if word in ["одна", "одним", "одно", "одной"]:
            return "один"
        if word == "две":
            return "два"
        if word == "пару":
            return "пара"

    elif arg == 2:  # extract_datetime_ru
        if word in ["часа", "часам", "часами", "часов", "часу"]:
            return "час"
        if word in ["минут", "минутам", "минутами", "минуту", "минуты"]:
            return "минута"
        if word in ["секунд", "секундам", "секундами", "секунду", "секунды"]:
            return "секунда"
        if word in ["дней", "дни"]:
            return "день"
        if word in ["неделе", "недели", "недель"]:
            return "неделя"
        if word in ["месяца", "месяцев"]:
            return "месяц"
        if word in ["года", "лет"]:
            return "год"
        if word in _WORDS_MORNING_RU:
            return "утром"
        if word in ["полудне", "полудня"]:
            return "полдень"
        if word in _WORDS_EVENING_RU:
            return "вечером"
        if word in _WORDS_NIGHT_RU:
            return "ночь"
        if word in ["викенд", "выходным", "выходных"]:
            return "выходные"
        if word in ["столетие", "столетий", "столетия"]:
            return "век"

        # Week days
        if word in ["среду", "среды"]:
            return "среда"
        if word in ["пятницу", "пятницы"]:
            return "пятница"
        if word in ["субботу", "субботы"]:
            return "суббота"

        # Months
        if word in ["марта", "марте"]:
            return "март"
        if word in ["мае", "мая"]:
            return "май"
        if word in ["августа", "августе"]:
            return "август"
    return word
