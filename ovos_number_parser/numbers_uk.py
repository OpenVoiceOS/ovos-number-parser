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
from collections import OrderedDict

from ovos_number_parser.util import (convert_to_mixed_fraction, invert_dict, GrammaticalGender, scientific_parts)

#: the last word of a cardinal that agrees with a feminine or neuter noun
#: (ICU RBNF uk spellout-cardinal-feminine and -neuter); the scale words
#: before it keep their own agreement ("одна тисяча")
_GENDERED_LAST_WORD_UK = {
    GrammaticalGender.FEMININE: {"один": "одна", "два": "дві"},
    GrammaticalGender.NEUTRAL: {"один": "одне"},
}

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
    (10 ** 3, "тисяча"),
    (10 ** 6, "мільйон"),
    (10 ** 9, "мільярд"),
    (10 ** 12, "трильйон"),
    (10 ** 15, "квадрильйон"),
    (10 ** 18, "квінтильйон"),
    (10 ** 21, "секстильйон"),
    (10 ** 24, "септильйон"),
    (10 ** 27, "октильйон"),
    (10 ** 30, "нонільйон"),
    (10 ** 33, "децильйон"),
    (10 ** 36, "ундецильйон"),
    (10 ** 39, "додецильйон"),
    (10 ** 42, "тредецильйон"),
    (10 ** 45, "кватордецильйон"),
    (10 ** 48, "квіндецильйон"),
    (10 ** 51, "сексдецильйон"),
    (10 ** 54, "септендецильйон"),
    (10 ** 57, "октодецильйон"),
    (10 ** 60, "новемдецильйон"),
    (10 ** 63, "вігінтильйон"),
    (10 ** 66, "анвігінтильйон"),
    (10 ** 69, "дуовігінтильйон"),
    (10 ** 72, "тревігінтильйон"),
    (10 ** 75, "кватторвігінтильйон"),
    (10 ** 78, "квінвігінтильйон"),
    (10 ** 81, "сексвігінтильйон"),
    (10 ** 84, "септемвігінтильйон"),
    (10 ** 87, "октовігінтильйон"),
    (10 ** 90, "новемвігінтильйон"),
    (10 ** 93, "трігінтильйон"),
])

_LONG_SCALE_UK = OrderedDict([
    (10 ** 3, "тисяча"),
    (10 ** 6, "мільйон"),
    (10 ** 9, "мільярд"),
    (10 ** 12, "більйон"),
    (10 ** 15, "більярд"),
    (10 ** 18, "трильйон"),
    (10 ** 21, "трильярд"),
    (10 ** 24, "квадрильйон"),
    (10 ** 27, "квадрильярд"),
    (10 ** 30, "квінтильйон"),
    (10 ** 33, "квінтильярд"),
    (10 ** 36, "секстильйон"),
    (10 ** 39, "секстильярд"),
    (10 ** 42, "септильйон"),
    (10 ** 45, "септильярд"),
    (10 ** 48, "октильйон"),
    (10 ** 51, "октильярд"),
    (10 ** 54, "нонільйон"),
    (10 ** 57, "нонільярд"),
    (10 ** 60, "децильйон"),
    (10 ** 63, "децильярд"),
    (10 ** 66, "ундецильйон"),
    (10 ** 69, "ундецильярд"),
    (10 ** 72, "додецильйон"),
    (10 ** 75, "додецильярд"),
    (10 ** 78, "тредецильйон"),
    (10 ** 81, "тредецильярд"),
    (10 ** 84, "кватордецильйон"),
    (10 ** 87, "кватордецильярд"),
    (10 ** 90, "квіндецильйон"),
    (10 ** 93, "квіндецильярд"),
    (10 ** 96, "сексдецильйон"),
    (10 ** 99, "сексдецильярд"),
    (10 ** 102, "септендецильйон"),
    (10 ** 105, "септендецильярд"),
    (10 ** 108, "октодецильйон"),
    (10 ** 111, "октодецильярд"),
    (10 ** 114, "новемдецильйон"),
    (10 ** 117, "новемдецильярд"),
    (10 ** 120, "вігінтильйон"),
    (10 ** 123, "вігінтильярд"),
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
    4e2: "чотирьохсотий",
    5e2: "п'ятисотий",
    6e2: "шестисотий",
    7e2: "семисотий",
    8e2: "восьмисотий",
    9e2: "дев'ятисотий",
    1e3: "тисячний"
}

_SHORT_ORDINAL_UK = {n: word for n, word in _SHORT_SCALE_UK.items()
                     if n >= 10 ** 6}
_SHORT_ORDINAL_UK.update(_ORDINAL_BASE_UK)

_LONG_ORDINAL_UK = {n: word for n, word in _LONG_SCALE_UK.items()
                    if n >= 10 ** 6}
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


_STRING_NUM_UK = invert_dict(_NUM_STRING_UK)

_STRING_NUM_UK.update(generate_plurals_uk(_STRING_NUM_UK))
_STRING_NUM_UK.update(_PLURALS)
_STRING_NUM_UK.update({
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
_WORDS_DAY_UK = ["вдень", "опівдні"]


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
        return "нескінченність"
    elif num == float("-inf"):
        return "мінус нескінченність"
    if scientific:
        n, power = scientific_parts(num, places)
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
    elif ordinals and num == int(num) and \
            (word := _ordinal_uk(int(num), short_scale)):
        result += word
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
            if n > max(_LONG_SCALE_UK.keys()):
                return ""
            n = int(n)
            assert 0 <= n
            high, low = divmod(n, 1000000)
            res = [pronounce_number_uk(low, places, True)] if low else []
            for i, z in enumerate(_split_by(high, 1000), start=2):
                if not z:
                    continue
                name = _LONG_SCALE_UK.get(1000 ** i)
                if name is None:
                    return ""
                if z == 1:
                    number = name
                elif z <= 4:
                    number = pronounce_number_uk(z, places, True) + " " + \
                        name + "а"
                else:
                    number = pronounce_number_uk(z, places, True) + " " + \
                        name + "ів"
                res.append(number)
            return " ".join(reversed(res))

        if short_scale:
            result += _short_scale(num)
        else:
            result += _long_scale(num)

    # a magnitude with no spoken name reads scientifically
    if result in ("", "мінус ") and num >= 1e6:
        return result + pronounce_number_uk(
            num, places, short_scale, scientific=True)
    if num != int(num) and abs(num) < 1.0 \
            and (result == "мінус " or not result):
        result += "нуль"
    # Deal with fractional part
    if not num == int(num) and places > 0:
        result += " крапка"
        _num_str = f"{Decimal(str(num)):f}"
        _num_str = _num_str.split(".")[1][0:places]
        for char in _num_str:
            result += " " + number_names[int(char)]
    elif not ordinals:
        *head, last = result.split(" ")
        last = _GENDERED_LAST_WORD_UK.get(gender, {}).get(last, last)
        result = " ".join(head + [last])
    elif result.endswith(("ий", "ій")):
        *head, last = result.split(" ")
        result = " ".join(head + [_ordinal_gender_uk(last, gender)])
    return result


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


def plural_uk(num: int, one: str, few: str, many: str):
    num %= 100
    if num // 10 == 1:
        return many
    if num % 10 == 1:
        return one
    if 2 <= num % 10 <= 4:
        return few
    return many


def _ordinal_gender_uk(word, gender):
    """Inflect a masculine ordinal as an adjective: "перший" -> "перша",
    "перше"; the soft "третій" -> "третя", "третє"."""
    if gender == GrammaticalGender.FEMININE:
        return word[:-2] + "я" if word.endswith("ій") else word[:-2] + "а"
    if gender == GrammaticalGender.NEUTRAL:
        return word[:-2] + "є" if word.endswith("ій") else word[:-2] + "е"
    return word


# Stems that join a count to "-тисячний", "-мільйонний", written as one
# word (en.wiktionary "двохтисячний", "трьохтисячний", "чотирьохтисячний",
# "п'ятитисячний", "десятитисячний", "двадцятитисячний", "сорокатисячний",
# "дев'яностотисячний", "стотисячний", "двохсоттисячний").
_ORDINAL_STEM_UNITS_UK = ["", "одно", "двох", "трьох", "чотирьох", "п'яти",
                          "шести", "семи", "восьми", "дев'яти"]
_ORDINAL_STEM_TEENS_UK = ["десяти", "одинадцяти", "дванадцяти", "тринадцяти",
                          "чотирнадцяти", "п'ятнадцяти", "шістнадцяти",
                          "сімнадцяти", "вісімнадцяти", "дев'ятнадцяти"]
_ORDINAL_STEM_TENS_UK = ["", "", "двадцяти", "тридцяти", "сорока",
                         "п'ятдесяти", "шістдесяти", "сімдесяти",
                         "вісімдесяти", "дев'яносто"]
_ORDINAL_STEM_HUNDREDS_UK = ["", "сто", "двохсот", "трьохсот", "чотирьохсот",
                             "п'ятисот", "шестисот", "семисот", "восьмисот",
                             "дев'ятисот"]


def _ordinal_stem_uk(n):
    hundreds, rest = divmod(n, 100)
    tens, units = divmod(rest, 10)
    if tens == 1:
        return _ORDINAL_STEM_HUNDREDS_UK[hundreds] + _ORDINAL_STEM_TEENS_UK[units]
    return _ORDINAL_STEM_HUNDREDS_UK[hundreds] + _ORDINAL_STEM_TENS_UK[tens] + \
        _ORDINAL_STEM_UNITS_UK[units]


def _ordinal_uk(n, short_scale=True):
    """Masculine ordinal of a whole number: the groups before the last
    non-zero group stay cardinal ("дві тисячі п'ятий"). Return None for 0,
    when that group has no scale name, or when the groups before it read
    scientifically."""
    if n < 1:
        return None
    scale, group = 0, n
    while group % 1000 == 0:
        scale, group = scale + 1, group // 1000
    head = (group - group % 1000) * 1000 ** scale
    group %= 1000
    if scale:
        name = (_SHORT_SCALE_UK if short_scale else _LONG_SCALE_UK).get(1000 ** scale)
        if name is None:
            return None
        word = ("" if group == 1 else _ordinal_stem_uk(group)) + \
            name.removesuffix("а") + "ний"
    else:
        hundreds, rest = divmod(group, 100)
        if not rest:
            word = _ORDINAL_BASE_UK[group]
        else:
            words = [_NUM_STRING_UK[hundreds * 100]] if hundreds else []
            if rest in _ORDINAL_BASE_UK:
                words.append(_ORDINAL_BASE_UK[rest])
            else:
                words += [_NUM_STRING_UK[rest - rest % 10],
                          _ORDINAL_BASE_UK[rest % 10]]
            word = " ".join(words)
    if head:
        head_words = pronounce_number_uk(head, short_scale=short_scale)
        if head_words == pronounce_number_uk(head, short_scale=short_scale,
                                               scientific=True):
            return None
        word = f"{head_words} {word}"
    return word


def pronounce_ordinal_uk(number, gender=GrammaticalGender.MASCULINE):
    """
    Pronounce a number as a Ukrainian ordinal in the nominative.

    Only the final word is ordinal, preceding groups stay cardinal.

    Args:
        number (int): the number to pronounce
        gender (GrammaticalGender): gender of the noun the ordinal agrees with
    Returns:
        (str): the ordinal in Ukrainian
    """
    number = int(number)
    if number <= 0:
        raise ValueError("Ukrainian ordinals start at 1")
    return pronounce_number_uk(number, ordinals=True, gender=gender)
