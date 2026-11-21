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

from ovos_number_parser.util import convert_to_mixed_fraction, invert_dict, GrammaticalGender, scientific_parts, \
    round_half_up

#: the last word of a cardinal that agrees with a feminine or neuter noun
#: (ICU RBNF ru spellout-cardinal-feminine and -neuter); the scale words
#: before it keep their own agreement ("одна тысяча")
_GENDERED_LAST_WORD_RU = {
    GrammaticalGender.FEMININE: {"один": "одна", "два": "две"},
    GrammaticalGender.NEUTRAL: {"один": "одно"},
}

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

# The scale words by the power of ten they name. The float keys above stop
# being exact powers of ten past 10^22, so a lookup goes by the exponent.
_SHORT_SCALE_POWERS_RU = {round(math.log10(k)): w for k, w in _SHORT_SCALE_RU.items()}
_LONG_SCALE_POWERS_RU = {round(math.log10(k)): w for k, w in _LONG_SCALE_RU.items()}

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


_STRING_NUM_RU = invert_dict(_NUM_STRING_RU)
_STRING_NUM_RU.update({
    "тысяч": 10 ** 3,
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
_WORDS_DAY_RU = ["днём"]


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
                        ordinals=False, gender=GrammaticalGender.MASCULINE):
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
        gender (GrammaticalGender): gender of the noun a cardinal counts
    Returns:
        (str): The pronounced number
    """
    num = number
    # deal with infinity
    if num == float("inf"):
        return "бесконечность"
    elif num == float("-inf"):
        return "минус бесконечность"
    # Round (not truncate) the value to `places` decimals: half-away-from-zero
    # per ISO 80000-1 and NIST SP 811 (2008) B.7. Rounding here also carries
    # into the integer part and collapses a value that rounds to zero to a
    # plain "ноль" (never "минус ноль").
    if not scientific and isinstance(num, float) and math.isfinite(num) \
            and num != int(num):
        num = float(round_half_up(Decimal(str(num)), places)) or 0.0
    if scientific:
        n, power = scientific_parts(num, places)
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

    # deal with negative numbers
    result = ""
    if num < 0:
        result = "минус "
    num = abs(num)

    # check for a direct match
    if num in number_names and not ordinals:
        result += number_names[num]
    elif ordinals and num == int(num) and \
            (word := _ordinal_ru(int(num), short_scale)):
        result += word
    else:
        def _sub_thousand(n):
            assert 0 <= n <= 999
            if n <= 19:
                return digits[n]
            elif n <= 99:
                q, r = divmod(n, 10)
                return tens[q - 1] + (" " + _sub_thousand(r) if r else "")
            else:
                q, r = divmod(n, 100)
                return _NUM_STRING_RU[q * 100] + (" " + _sub_thousand(r) if r else "")

        def _split_by(n, split=1000):
            assert 0 <= n
            res = []
            while n:
                n, r = divmod(n, split)
                res.append(r)
            return res

        def _scale_reading(n):
            # Every group of three digits takes the scale word of its power of
            # ten, in the plural form its count asks for. A group with no
            # scale word returns "" so the caller falls back to a scientific
            # reading; "бесконечность" is reserved for math.inf (handled above).
            names = _SHORT_SCALE_POWERS_RU if short_scale else _LONG_SCALE_POWERS_RU
            res = []
            for i, z in enumerate(_split_by(int(n), 1000)):
                if not z:
                    continue
                number = _sub_thousand(z)
                if i:
                    name = names.get(3 * i)
                    if name is None:
                        return ""
                    if i == 1:
                        # тысяча is feminine: "одна тысяча", "две тысячи"
                        if z % 10 == 1 and z % 100 != 11:
                            number = number[:-2] + "на"
                        elif z % 10 == 2 and z % 100 != 12:
                            number = number[:-1] + "е"
                        word = plural_ru(z, name, name[:-1] + "и", name[:-1])
                    else:
                        word = plural_ru(z, name, name + "а", name + "ов")
                    number = word if z == 1 else f"{number} {word}"
                res.append(number)
            return " ".join(reversed(res))

        result += _scale_reading(num)

    # deal with a magnitude that has no spoken name: read it scientifically
    # (covers floats in "e" notation and very large ints alike) so a finite
    # value never returns an empty string.
    if result in ("", "минус ") and num >= 1e6:
        return result + pronounce_number_ru(
            num, places, short_scale, scientific=True)
    # Deal with fractional part
    elif not num == int(num) and places > 0:
        if abs(num) < 1.0 and (result == "минус " or not result):
            result += "ноль"
        result += " точка"
        _num_str = f"{Decimal(str(num)):f}"
        _num_str = _num_str.split(".")[1][0:places]
        for char in _num_str:
            result += " " + number_names[int(char)]
    elif not ordinals:
        *head, last = result.split(" ")
        last = _GENDERED_LAST_WORD_RU.get(gender, {}).get(last, last)
        result = " ".join(head + [last])
    else:
        *head, last = result.split(" ")
        result = " ".join(head + [_ordinal_gender_ru(last, gender)])
    return result


# Stems that join a count to "-тысячный", "-миллионный": the words are
# written as one (ru.wikipedia "Порядковое числительное":
# "тридцативосьмимиллионный"; ru.wiktionary "двухтысячный", "стотысячный",
# "двухсоттысячный", "сорокатысячный", "девяностотысячный",
# "двадцатипятитысячный").
_ORDINAL_STEM_UNITS_RU = ["", "одно", "двух", "трёх", "четырёх", "пяти",
                          "шести", "семи", "восьми", "девяти"]
_ORDINAL_STEM_TEENS_RU = ["десяти", "одиннадцати", "двенадцати",
                          "тринадцати", "четырнадцати", "пятнадцати",
                          "шестнадцати", "семнадцати", "восемнадцати",
                          "девятнадцати"]
_ORDINAL_STEM_TENS_RU = ["", "", "двадцати", "тридцати", "сорока",
                         "пятидесяти", "шестидесяти", "семидесяти",
                         "восьмидесяти", "девяносто"]
_ORDINAL_STEM_HUNDREDS_RU = ["", "сто", "двухсот", "трёхсот", "четырёхсот",
                             "пятисот", "шестисот", "семисот", "восьмисот",
                             "девятисот"]


def _ordinal_stem_ru(n):
    hundreds, rest = divmod(n, 100)
    tens, units = divmod(rest, 10)
    if tens == 1:
        return _ORDINAL_STEM_HUNDREDS_RU[hundreds] + _ORDINAL_STEM_TEENS_RU[units]
    return _ORDINAL_STEM_HUNDREDS_RU[hundreds] + _ORDINAL_STEM_TENS_RU[tens] + \
        _ORDINAL_STEM_UNITS_RU[units]


def _ordinal_ru(n, short_scale=True):
    """Masculine ordinal of a whole number: the groups before the last
    non-zero group stay cardinal ("две тысячи пятый"). Return None when that
    group has no scale name, or when the groups before it read
    scientifically."""
    if n == 0:
        # CLDR RBNF ru spellout-ordinal-masculine: 0 "нулевой"
        return "нулевой"
    scale, group = 0, n
    while group % 1000 == 0:
        scale, group = scale + 1, group // 1000
    head = (group - group % 1000) * 1000 ** scale
    group %= 1000
    if scale:
        name = (_SHORT_SCALE_POWERS_RU if short_scale
                else _LONG_SCALE_POWERS_RU).get(3 * scale)
        if name is None:
            return None
        word = ("" if group == 1 else _ordinal_stem_ru(group)) + \
            name.removesuffix("а") + "ный"
    else:
        hundreds, rest = divmod(group, 100)
        if not rest:
            word = _ORDINAL_BASE_RU[group]
        else:
            words = [_NUM_STRING_RU[hundreds * 100]] if hundreds else []
            if rest in _ORDINAL_BASE_RU:
                words.append(_ORDINAL_BASE_RU[rest])
            else:
                words += [_NUM_STRING_RU[rest - rest % 10],
                          _ORDINAL_BASE_RU[rest % 10]]
            word = " ".join(words)
    if head:
        head_words = pronounce_number_ru(head, short_scale=short_scale)
        if head_words == pronounce_number_ru(head, short_scale=short_scale,
                                               scientific=True):
            return None
        word = f"{head_words} {word}"
    return word


def _ordinal_gender_ru(word, gender):
    """Inflect a masculine ordinal as an adjective: "первый" -> "первая",
    "первое"; "второй" -> "вторая", "второе"; the soft "третий" -> "третья",
    "третье" (ICU RBNF ru spellout-ordinal-feminine and -neuter)."""
    if gender == GrammaticalGender.FEMININE:
        if word.endswith("ий"):
            return word[:-2] + "ья"
        if word.endswith(("ый", "ой")):
            return word[:-2] + "ая"
    if gender == GrammaticalGender.NEUTRAL:
        if word.endswith("ий"):
            return word[:-2] + "ье"
        if word.endswith(("ый", "ой")):
            return word[:-2] + "ое"
    return word


def plural_ru(num: int, one: str, few: str, many: str):
    num %= 100
    if num // 10 == 1:
        return many
    if num % 10 == 1:
        return one
    if 2 <= num % 10 <= 4:
        return few
    return many


def is_fractional_ru(input_str, short_scale=True):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): use short scale if True, long scale if False
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    # Ordinal-derived fraction nouns are feminine ("пятая", 1/5). After a
    # numerator they take the plural nominative "-ые" or genitive "-ых"
    # ("две пятые", "три пятых"); normalize that ending back to the singular
    # "-тая" citation form so it matches the table.
    if input_str[-3:] in ["тые", "тых"]:
        input_str = input_str[:-3] + "тая"
    fractions = {"целая": 1}  # first four numbers have little different format

    for num in _FRACTION_STRING_RU:  # Numbers from 2 to 1 hundred, more is not usually used in common speech
        if num > 1:
            fractions[_FRACTION_STRING_RU[num]] = num

    if input_str.lower() in fractions:
        return 1.0 / fractions[input_str.lower()]
    return False


