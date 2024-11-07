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

_NUM_STRING_PL = {
    0: 'zero',
    1: 'jeden',
    2: 'dwa',
    3: 'trzy',
    4: 'cztery',
    5: 'pięć',
    6: 'sześć',
    7: 'siedem',
    8: 'osiem',
    9: 'dziewięć',
    10: 'dziesięć',
    11: 'jedenaście',
    12: 'dwanaście',
    13: 'trzynaście',
    14: 'czternaście',
    15: 'piętnaście',
    16: 'szesnaście',
    17: 'siedemnaście',
    18: 'osiemnaście',
    19: 'dziewiętnaście',
    20: 'dwadzieścia',
    30: 'trzydzieści',
    40: 'czterdzieści',
    50: 'pięćdziesiąt',
    60: 'sześćdziesiąt',
    70: 'siedemdziesiąt',
    80: 'osiemdziesiąt',
    90: 'dziewięćdziesiąt',
    100: 'sto',
    200: 'dwieście',
    300: 'trzysta',
    400: 'czterysta',
    500: 'pięćset',
    600: 'sześćset',
    700: 'siedemset',
    800: 'osiemset',
    900: 'dziewięćset',
}

_FRACTION_STRING_PL = {
    1: 'jedna',
    2: 'druga',
    3: 'trzecia',
    4: 'czwarta',
    5: 'piąta',
    6: 'szósta',
    7: 'siódma',
    8: 'ósma',
    9: 'dziewiąta',
    10: 'dziesiąta',
    11: 'jedenasta',
    12: 'dwunasta',
    13: 'trzynasta',
    14: 'czternasta',
    15: 'piętnasta',
    16: 'szesnasta',
    17: 'siedemnasta',
    18: 'osiemnasta',
    19: 'dziewiętnasta',
    20: 'dwudziesta',
    30: 'trzydziesta',
    40: 'czterdziesta',
    50: 'pięćdziesiąta',
    60: 'sześćdziesiąta',
    70: 'siedemdziesiąta',
    80: 'osiemdziesiąta',
    90: 'dziewięćdziesiąta',
    100: 'setna',
    200: 'dwusetna',
    300: 'trzysetna',
    400: 'czterysetna',
    500: 'pięćsetna',
    600: 'sześćsetna',
    700: 'siedemsetna',
    800: 'osiemsetna',
    900: 'dziewięćsetna',
    1000: 'tysięczna',
}

_SHORT_SCALE_PL = OrderedDict([
    (100, 'sto'),
    (200, 'dwieście'),
    (300, 'trzysta'),
    (400, 'czterysta'),
    (500, 'pięćset'),
    (600, 'sześćset'),
    (700, 'siedemset'),
    (800, 'osiemset'),
    (900, 'dziewięćset'),
    (1000, 'tysiąc'),
    (1000000, 'milion'),
    (1e9, "miliard"),
    (1e12, 'bilion'),
    (1e15, "biliard"),
    (1e18, "trylion"),
    (1e21, "sekstilion"),
    (1e24, "kwadrylion"),
    (1e27, "kwadryliard"),
    (1e30, "kwintylion"),
    (1e33, "kwintyliard"),
    (1e36, "sekstylion"),
    (1e39, "sekstyliard"),
    (1e42, "septylion"),
    (1e45, "septyliard"),
    (1e48, "oktylion"),
    (1e51, "oktyliard"),
    (1e54, "nonilion"),
    (1e57, "noniliard"),
    (1e60, "decylion"),
    (1e63, "decyliard"),
    (1e66, "undecylion"),
    (1e69, "undecyliard"),
    (1e72, "duodecylion"),
    (1e75, "duodecyliard"),
    (1e78, "tredecylion"),
    (1e81, "tredecyliard"),
    (1e84, "kwartyduodecylion"),
    (1e87, "kwartyduodecyliard"),
    (1e90, "kwintyduodecylion"),
    (1e93, "kwintyduodecyliard"),
    (1e96, "seksdecylion"),
    (1e99, "seksdecyliard"),
    (1e102, "septydecylion"),
    (1e105, "septydecyliard"),
    (1e108, "oktodecylion"),
    (1e111, "oktodecyliard"),
    (1e114, "nondecylion"),
    (1e117, "nondecyliard"),
    (1e120, "wigintylion"),
    (1e123, "wigintyliard"),
    (1e153, "quinquagintylion"),
    (1e183, "trycyliard"),
    (1e213, "septuagintylion"),
    (1e243, "kwadragiliard"),
    (1e273, "nonagintylion"),
    (1e303, "centezylion"),
    (1e306, "uncentylion"),
    (1e309, "duocentylion"),
    (1e312, "trescentylion"),
    (1e333, "decicentylion"),
    (1e336, "undecicentylion"),
    (1e363, "viginticentylion"),
    (1e366, "unviginticentylion"),
    (1e393, "trigintacentylion"),
    (1e423, "quadragintacentylion"),
    (1e453, "quinquagintacentylion"),
    (1e483, "sexagintacentylion"),
    (1e513, "septuagintacentylion"),
    (1e543, "ctogintacentylion"),
    (1e573, "nonagintacentylion"),
    (1e603, "centyliard"),
    (1e903, "trecentylion"),
    (1e1203, "quadringentylion"),
    (1e1503, "quingentylion"),
    (1e1803, "sescentylion"),
    (1e2103, "septingentylion"),
    (1e2403, "octingentylion"),
    (1e2703, "nongentylion"),
    (1e3003, "milinylion")
])

_ORDINAL_BASE_PL = {
    1: 'pierwszy',
    2: 'drugi',
    3: 'trzeci',
    4: 'czwarty',
    5: 'piąty',
    6: 'szósty',
    7: 'siódmy',
    8: 'ósmy',
    9: 'dziewiąty',
    10: 'dziesiąty',
    11: 'jedenasty',
    12: 'dwunasty',
    13: 'trzynasty',
    14: 'czternasty',
    15: 'piętnasty',
    16: 'szesnasty',
    17: 'siedemnasty',
    18: 'osiemnasty',
    19: 'dziewiętnasty',
    20: 'dwudziesty',
    30: 'trzydziesty',
    40: "czterdziesty",
    50: "pięćdziesiąty",
    60: "sześćdziesiąty",
    70: "siedemdziesiąty",
    80: "osiemdziesiąty",
    90: "dziewięćdziesiąty",
    1e2: "setny",
    1e3: "tysięczny"
}

_SHORT_ORDINAL_PL = {
    1e6: "milionowy",
    1e9: "miliardowy",
    1e12: "bilionowy",
    1e15: "biliardowy",
    1e18: "trylionowy",
    1e21: "tryliardowy",
    1e24: "kwadrylionowy",
    1e27: "kwadryliardowy",
    1e30: "kwintylionowy",
    1e33: "kwintyliardowy",
    1e36: "sektylionowy",
    1e42: "septylionowy",
    1e48: "oktylionowy",
    1e54: "nonylionowy",
    1e60: "decylionowy"
    # TODO > 1e-33
}
_SHORT_ORDINAL_PL.update(_ORDINAL_BASE_PL)

_ALT_ORDINALS_PL = {
    1: 'pierwszej',
    2: 'drugiej',
    3: 'trzeciej',
    4: 'czwartej',
    5: 'piątej',
    6: 'szóstej',
    7: 'siódmej',
    8: 'ósmej',
    9: 'dziewiątej',
    10: 'dziesięcio',
    11: 'jedenasto',
    12: 'dwunasto',
    13: 'trzynasto',
    14: 'czternasto',
    15: 'piętnasto',
    16: 'szesnasto',
    17: 'siedemnasto',
    18: 'osiemnasto',
    19: 'dziewiętnasto',
    20: 'dwudziesto',
    30: 'trzydziesto',
    40: 'czterdziesto',
    50: 'pięćdziesiecio',
    60: 'sześćdziesięcio',
    70: 'siedemdziesięcio',
    80: 'osiemdziesięcio',
    90: 'dziewięćdziesięcio',
}


def nice_number_pl(number, speech=True, denominators=range(1, 21)):
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
    den_str = _FRACTION_STRING_PL[den]
    if whole == 0:
        return_string = '{} {}'.format(num, den_str)
    else:
        return_string = '{} i {} {}'.format(whole, num, den_str)
    if num > 1:
        return_string = return_string[:-1] + 'e'
    return return_string


def pronounce_number_pl(num, places=2, short_scale=True, scientific=False,
                        ordinals=False, scientific_run=False):
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
    # deal with infinity
    if num == float("inf"):
        return "nieskończoność"
    elif num == float("-inf"):
        return "minus nieskończoność"
    if scientific:
        number = '%E' % num
        n, power = number.replace("+", "").split("E")
        power = int(power)
        if power != 0:
            if ordinals:
                # This handles negatives of powers separately from the normal
                # handling since each call disables the scientific flag
                return '{}{} razy dziesięć do {}{} potęgi'.format(
                    'minus ' if float(n) < 0 else '',
                    pronounce_number_pl(
                        abs(float(n)), places, short_scale, False, ordinals=False, scientific_run=True),
                    'minus ' if power < 0 else '',
                    pronounce_number_pl(abs(power), places, short_scale, False, ordinals=True, scientific_run=True))
            else:
                # This handles negatives of powers separately from the normal
                # handling since each call disables the scientific flag
                return '{}{} razy dziesięć do potęgi {}{}'.format(
                    'minus ' if float(n) < 0 else '',
                    pronounce_number_pl(
                        abs(float(n)), places, short_scale, False),
                    'minus ' if power < 0 else '',
                    pronounce_number_pl(abs(power), places, short_scale, False))

    number_names = _NUM_STRING_PL.copy()
    number_names.update(_SHORT_SCALE_PL)

    digits = [number_names[n] for n in range(0, 20)]
    if ordinals:
        tens = [_SHORT_ORDINAL_PL[n] for n in range(10, 100, 10)]
    else:
        tens = [number_names[n] for n in range(10, 100, 10)]
    hundreds = [_SHORT_SCALE_PL[n] for n in _SHORT_SCALE_PL.keys()]

    # deal with negatives
    result = ""
    if num < 0:
        result = "minus "
    num = abs(num)

    # check for a direct match
    if num in number_names and not ordinals:
        result += number_names[num]
    else:
        def _sub_thousand(n, ordinals=False, iteration=0):
            assert 0 <= n <= 999

            _, n_mod = divmod(n, 10)
            if iteration > 0 and n in _ALT_ORDINALS_PL and ordinals:
                return _ALT_ORDINALS_PL[n]
            elif n in _SHORT_ORDINAL_PL and ordinals:
                return _SHORT_ORDINAL_PL[n] if not scientific_run \
                    else _ALT_ORDINALS_PL[n]
            if n <= 19:
                return digits[n] if not scientific_run or not ordinals \
                    else digits[n][:-1] + "ej"
            elif n <= 99:
                q, r = divmod(n, 10)
                tens_text = tens[q - 1]
                if scientific_run:
                    tens_text = tens_text[:-1] + "ej"
                return tens_text + (" " + _sub_thousand(r, ordinals) if r
                                    else "")
            else:
                q, r = divmod(n, 100)
                digit_name = digits[q]
                if q * 100 in _NUM_STRING_PL:
                    digit_name = _NUM_STRING_PL[q * 100]

                return digit_name + (
                    " " + _sub_thousand(r, ordinals) if r else "")

        def _short_scale(n):
            if n >= max(_SHORT_SCALE_PL.keys()):
                return "nieskończoność"
            ordi = ordinals

            if int(n) != n:
                ordi = False
            n = int(n)
            assert 0 <= n
            res = []
            for i, z in enumerate(_split_by(n, 1000)):
                if not z:
                    continue
                number = _sub_thousand(z, ordi, iteration=i)

                if i:
                    if i >= len(hundreds):
                        return ""
                    number += " "
                    if ordi:
                        if i * 1000 in _SHORT_ORDINAL_PL:
                            if z == 1:
                                number = _SHORT_ORDINAL_PL[i * 1000]
                            else:
                                number += _SHORT_ORDINAL_PL[i * 1000]
                        else:
                            if n not in _SHORT_SCALE_PL:
                                num = int("1" + "0" * (len(str(n)) - 2))

                                number += _SHORT_SCALE_PL[num] + "owa"
                            else:
                                number = _SHORT_SCALE_PL[n] + "ty"
                    else:
                        hundreds_text = _SHORT_SCALE_PL[float(pow(1000, i))]
                        if z != 1:
                            _, z_mod = divmod(z, 10)
                            _, z_mod_tens = divmod(z, 100)
                            n_main, _ = divmod(z_mod_tens, 10)
                            if i == 1:
                                if n_main != 1 and 5 > z_mod > 0:
                                    hundreds_text += "e"
                                else:
                                    hundreds_text = "tysięcy"
                            elif i > 1:
                                hundreds_text += "y" if 5 > z_mod > 0 else "ów"

                        number += hundreds_text
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

        result += _short_scale(num)

    # deal with scientific notation unpronounceable as number
    if not result and "e" in str(num):
        return pronounce_number_pl(num, places, short_scale, scientific=True)
    # Deal with fractional part
    elif not num == int(num) and places > 0:
        if abs(num) < 1.0 and (result == "minus " or not result):
            result += "zero"
        result += " przecinek"
        _num_str = str(num)
        _num_str = _num_str.split(".")[1][0:places]
        for char in _num_str:
            result += " " + number_names[int(char)]
    return result


def generate_plurals_pl(originals):
    """
    Return a new set or dict containing the plural form of the original values,

    In English this means all with 's' appended to them.

    Args:
        originals set(str) or dict(str, any): values to pluralize

    Returns:
        set(str) or dict(str, any)

    """
    if isinstance(originals, dict):
        result = {key + 'y': value for key, value in originals.items()}
        result = {**result, **{key + 'ów': value for key, value in originals.items()}}
        result = {**result, **{'tysiące': 1000, 'tysięcy': 1000}}

        return result

    result = {value + "y" for value in originals}
    result = result.union({value + "ów" for value in originals})
    result = result.union({'tysiące', 'tysięcy'})

    return result


def generate_fractions_pl(fractions):
    '''Returns a list of all fraction combinations. E.g.:
    trzecia, trzecich, trzecie
    czwarta, czwarte, czwartych

    :param fractions: Existing fractions
    :return: Fractions with add suffixes
    '''

    result = {**fractions}
    for k, v in fractions.items():
        k_no_last = k[:-1]
        result[k_no_last + 'e'] = v
        if k_no_last[-1:] == 'i':
            result[k_no_last + 'ch'] = v
        else:
            result[k_no_last + 'ych'] = v

    for k, v in _SHORT_ORDINAL_PL.items():
        result[v[:-1] + 'a'] = k

    result['jedno'] = 1
    result['czwartego'] = 4

    return result


# negate next number (-2 = 0 - 2)
_NEGATIVES = {"ujemne", "minus"}

# sum the next number (twenty two = 20 + 2)
_SUMS = {'dwadzieścia', '20', 'trzydzieści', '30', 'czterdzieści', '40', 'pięćdziesiąt', '50',
         'sześćdziesiąt', '60', 'siedemdziesiąt', '70', 'osiemdziesiąt', '80', 'dziewięćdziesiąt', '90'}

_MULTIPLIES_SHORT_SCALE_PL = generate_plurals_pl(_SHORT_SCALE_PL.values())

# split sentence parse separately and sum ( 2 and a half = 2 + 0.5 )
_FRACTION_MARKER = {'i'}

# decimal marker ( 1 point 5 = 1 + 0.5)
_DECIMAL_MARKER = {'kropka', 'przecinek'}

_STRING_NUM_PL = invert_dict(_NUM_STRING_PL)
_STRING_NUM_PL.update(generate_plurals_pl(_STRING_NUM_PL))
_STRING_NUM_PL.update({
    'pół': 0.5,
    'połówka': 0.5,
    'połowa': 0.5,
})

_STRING_SHORT_ORDINAL_PL = invert_dict(_SHORT_ORDINAL_PL)

_REV_FRACTITONS = generate_fractions_pl(invert_dict(_FRACTION_STRING_PL))


def numbers_to_digits_pl(text, short_scale=True, ordinals=False):
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
        _extract_numbers_with_text_pl(tokens, short_scale, ordinals)
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


def _extract_numbers_with_text_pl(tokens, short_scale=True,
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
            _extract_number_with_text_pl(tokens, short_scale,
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


def _extract_number_with_text_pl(tokens, short_scale=True,
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
        _extract_number_with_text_pl_helper(tokens, short_scale,
                                            ordinals, fractional_numbers)
    return ReplaceableNumber(number, tokens)


def _extract_number_with_text_pl_helper(tokens,
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
            _extract_fraction_with_text_pl(tokens, short_scale, ordinals)
        if fraction:
            return fraction, fraction_text

        decimal, decimal_text = \
            _extract_decimal_with_text_pl(tokens, short_scale, ordinals)
        if decimal:
            return decimal, decimal_text

    return _extract_whole_number_with_text_pl(tokens, short_scale, ordinals)


def _extract_fraction_with_text_pl(tokens, short_scale, ordinals):
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
                _extract_numbers_with_text_pl(partitions[0], short_scale,
                                              ordinals, fractional_numbers=False)
            numbers2 = \
                _extract_numbers_with_text_pl(partitions[2], short_scale,
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


def _extract_decimal_with_text_pl(tokens, short_scale, ordinals):
    """
    Extract decimal numbers from a string.

    This function handles text such as '2 point 5'.

    Notes:
        While this is a helper for extractnumber_en, it also depends on
        extractnumber_en, to parse out the components of the decimal.

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
                _extract_numbers_with_text_pl(partitions[0], short_scale,
                                              ordinals, fractional_numbers=False)
            numbers2 = \
                _extract_numbers_with_text_pl(partitions[2], short_scale,
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


def _extract_whole_number_with_text_pl(tokens, short_scale, ordinals):
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

        prev_word = tokens[idx - 1].word if idx > 0 else ""
        next_word = tokens[idx + 1].word if idx + 1 < len(tokens) else ""

        if is_numeric(word[:-1]) and word.endswith('.'):
            # explicit ordinals, 1., 2., 3., 4.... N.
            word = word[:-1]

        word = normalize_word_pl(word)

        if word not in string_num_scale and \
                word not in _STRING_NUM_PL and \
                word not in _SUMS and \
                word not in multiplies and \
                not (ordinals and word in string_num_ordinal) and \
                not is_numeric(word) and \
                not is_fractional_pl(word) and \
                not look_for_fractions(word.split('/')):
            words_only = [token.word for token in number_words]
            if number_words and not all([w in _NEGATIVES for w in words_only]):
                break
            else:
                number_words = []
                continue
        elif word not in multiplies \
                and prev_word not in multiplies \
                and prev_word not in _SHORT_SCALE_PL.values() \
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
        if word in _STRING_NUM_PL:
            val = _STRING_NUM_PL.get(word)
            current_val = val
        elif word in string_num_scale:
            val = string_num_scale.get(word)
            current_val = val
        elif ordinals and word in string_num_ordinal:
            val = string_num_ordinal[word]
            current_val = val

        if word in multiplies:
            if not prev_val:
                prev_val = 1
            val = prev_val * val
            prev_val = None

        # is the prev word a number and should we sum it?
        # twenty two, fifty six
        if prev_val:
            if (prev_word in string_num_ordinal and val and val < prev_val) or \
                    (prev_word in _STRING_NUM_PL and val and val < prev_val and val // 10 != prev_val // 10) or \
                    all([prev_word in multiplies, val < prev_val if prev_val else False]):
                val += prev_val

        if next_word in multiplies:
            prev_val = val
            continue

        # is this a spoken fraction?
        # half cup
        if val is False:
            val = is_fractional_pl(word)
            current_val = val

        # 2 fifths
        if not ordinals:
            next_val = is_fractional_pl(next_word)
            if next_val:
                if not val:
                    val = 1
                val *= next_val
                number_words.append(tokens[idx + 1])

        # is this a negative number?
        if val and prev_word and prev_word in _NEGATIVES:
            val = 0 - val

        if next_word in _STRING_NUM_PL:
            prev_val = val

        # let's make sure it isn't a fraction
        if not val:
            # look for fractions like "2/3"
            aPieces = word.split('/')
            if look_for_fractions(aPieces):
                val = float(aPieces[0]) / float(aPieces[1])
                number_words.append(tokens[idx + 1])
        else:
            if all([
                prev_word in _SUMS,
                word not in _SUMS,
                word not in multiplies,
                current_val >= 10]):
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
    multiplies = _MULTIPLIES_SHORT_SCALE_PL

    string_num_scale = invert_dict(_SHORT_SCALE_PL)
    string_num_scale.update(generate_plurals_pl(string_num_scale))
    return multiplies, _STRING_SHORT_ORDINAL_PL, string_num_scale


def extract_number_pl(text, short_scale=True, ordinals=False):
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
    return _extract_number_with_text_pl(tokenize(text.lower()),
                                        True, ordinals).value


def is_fractional_pl(input_str, short_scale=True):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): use short scale if True, long scale if False
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    lower_input = input_str.lower()
    if lower_input in _REV_FRACTITONS:
        return 1.0 / _REV_FRACTITONS[lower_input]

    return False


def normalize_word_pl(word):
    if word.startswith('jedn'):
        suffix = 'ą', 'ej', 'ym'
        if word.endswith(suffix):
            return 'jedna'
    if word == 'dwie':
        return 'dwa'

    return word
