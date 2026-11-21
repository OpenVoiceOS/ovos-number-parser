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
from decimal import Decimal
from collections import OrderedDict

from ovos_number_parser.util import convert_to_mixed_fraction, invert_dict, GrammaticalGender, scientific_parts
from ovos_number_parser import numtag_readers
from ovos_number_parser.util import warn_reader_removed
from ovos_number_parser.util import Scale

#: the last word of a cardinal that agrees with a feminine or neuter noun
#: (ICU RBNF pl spellout-cardinal-feminine and -neuter); a compound ending in
#: 1 keeps "jeden" ("dwadzieścia jeden"), so only the bare 1 inflects
_GENDERED_LAST_WORD_PL = {
    GrammaticalGender.FEMININE: {"dwa": "dwie"},
}
_GENDERED_ONE_PL = {
    GrammaticalGender.FEMININE: "jedna",
    GrammaticalGender.NEUTRAL: "jedno",
}

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
                        ordinals=False, scientific_run=False,
                        gender=GrammaticalGender.MASCULINE):
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
        gender (GrammaticalGender): gender of the noun a cardinal counts
    Returns:
        (str): The pronounced number
    """
    # deal with infinity
    if num == float("inf"):
        return "nieskończoność"
    elif num == float("-inf"):
        return "minus nieskończoność"
    if scientific:
        n, power = scientific_parts(num, places)
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
    elif ordinals and num == int(num) and (word := _ordinal_pl(int(num))):
        result += word
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
                number = _sub_thousand(z, ordi, iteration=i)

                if i:
                    if i >= len(hundreds) or \
                            float(pow(1000, i)) not in _SHORT_SCALE_PL:
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
                            z_mod = z % 10
                            z_tens = (z % 100) // 10
                            # Polish agreement: a quantity ending in 2, 3 or 4
                            # -- but NOT 12, 13, 14 -- takes the nominative
                            # plural ("dwa tysiące", "dwadzieścia dwa
                            # tysiące"). Everything else takes the genitive
                            # plural ("pięć tysięcy", and crucially anything
                            # ending in 1 above one: "dwadzieścia jeden
                            # tysięcy", not "... tysiące"). Standard grammar
                            # (zpe.gov.pl "Odmiana liczebnika i zaimka").
                            nominative_plural = z_tens != 1 and 2 <= z_mod <= 4
                            if i == 1:
                                hundreds_text = hundreds_text + "e" \
                                    if nominative_plural else "tysięcy"
                            elif i > 1:
                                hundreds_text += "y" if nominative_plural \
                                    else "ów"
                        else:
                            # "one thousand" is just "tysiąc", never
                            # "jeden tysiąc" -- the count word is dropped for a
                            # single scale unit
                            number = ""
                        number += hundreds_text
                res.append(number)
                ordi = False

            # groups are spoken with a space, not a comma ("tysiąc sto")
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
    if result in ("", "minus ") and num >= 1e6:
        return result + pronounce_number_pl(
            num, places, short_scale, scientific=True)
    if num != int(num) and abs(num) < 1.0 \
            and (result == "minus " or not result):
        result += "zero"
    # Deal with fractional part
    if not num == int(num) and places > 0:
        result += " przecinek"
        _num_str = f"{Decimal(str(num)):f}"
        _num_str = _num_str.split(".")[1][0:places]
        for char in _num_str:
            result += " " + number_names[int(char)]
    elif not ordinals:
        *head, last = result.split(" ")
        if abs(num) == 1:
            last = _GENDERED_ONE_PL.get(gender, last)
        last = _GENDERED_LAST_WORD_PL.get(gender, {}).get(last, last)
        result = " ".join(head + [last])
    else:
        # every ordinal word agrees ("dwudziesta pierwsza"); a cardinal
        # hundreds word stays ("sto dwudziesta pierwsza")
        ordinal_words = set(_SHORT_ORDINAL_PL.values()) | set(_ORDINAL_HUNDREDS_PL.values())
        *head, last = result.split(" ")
        head = [_ordinal_gender_pl(w, gender) if w in ordinal_words else w
                for w in head]
        if last.endswith(("y", "i")) and last not in _NUM_STRING_PL.values():
            last = _ordinal_gender_pl(last, gender)
        result = " ".join(head + [last])
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


_STRING_NUM_PL = invert_dict(_NUM_STRING_PL)
_STRING_NUM_PL.update(generate_plurals_pl(_STRING_NUM_PL))
_STRING_NUM_PL.update({
    'pół': 0.5,
    'połówka': 0.5,
    'połowa': 0.5,
})


_REV_FRACTITONS = generate_fractions_pl(invert_dict(_FRACTION_STRING_PL))


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


_ORDINAL_HUNDREDS_PL = {
    200: "dwusetny", 300: "trzechsetny", 400: "czterechsetny",
    500: "pięćsetny", 600: "sześćsetny", 700: "siedemsetny",
    800: "osiemsetny", 900: "dziewięćsetny",
}


# Stems that join a count to "-tysięczny", "-milionowy", written as one word
# (en.wiktionary "trzytysięczny", "pięciotysięczny", "dziesięciotysięczny",
# "jedenastotysięczny", "dwudziestotysięczny", "stutysięczny",
# "pięćsettysięczny"; M. Jagodziński, "Liczebniki": "2000. – dwutysięczny",
# "1 500 000. – milion pięćsettysięczny").
_ORDINAL_STEM_UNITS_PL = ["", "jedno", "dwu", "trzy", "cztero", "pięcio",
                          "sześcio", "siedmio", "ośmio", "dziewięcio"]
_ORDINAL_STEM_TEENS_PL = ["dziesięcio", "jedenasto", "dwunasto", "trzynasto",
                          "czternasto", "piętnasto", "szesnasto",
                          "siedemnasto", "osiemnasto", "dziewiętnasto"]
_ORDINAL_STEM_TENS_PL = ["", "", "dwudziesto", "trzydziesto", "czterdziesto",
                         "pięćdziesięcio", "sześćdziesięcio",
                         "siedemdziesięcio", "osiemdziesięcio",
                         "dziewięćdziesięcio"]
_ORDINAL_STEM_HUNDREDS_PL = ["", "stu", "dwustu", "trzystu", "czterystu",
                             "pięćset", "sześćset", "siedemset", "osiemset",
                             "dziewięćset"]


def _ordinal_stem_pl(n):
    hundreds, rest = divmod(n, 100)
    tens, units = divmod(rest, 10)
    if tens == 1:
        return _ORDINAL_STEM_HUNDREDS_PL[hundreds] + _ORDINAL_STEM_TEENS_PL[units]
    return _ORDINAL_STEM_HUNDREDS_PL[hundreds] + _ORDINAL_STEM_TENS_PL[tens] + \
        _ORDINAL_STEM_UNITS_PL[units]


def _ordinal_pl(n):
    """Masculine ordinal of a whole number. Tens and units are ordinal
    ("dwudziesty pierwszy"); the hundreds and the groups before them stay
    cardinal, and only the last word is ordinal when tens and units are
    absent ("dwa tysiące setny", Jagodziński). Return None for 0 or when the
    last non-zero group has no scale name."""
    if n < 1:
        return None
    scale, group = 0, n
    while group % 1000 == 0:
        scale, group = scale + 1, group // 1000
    head = (group - group % 1000) * 1000 ** scale
    group %= 1000
    if scale:
        name = "tysięczny" if scale == 1 else _SHORT_ORDINAL_PL.get(1000 ** scale)
        if name is None:
            return None
        word = ("" if group == 1 else _ordinal_stem_pl(group)) + name
    else:
        hundreds, rest = divmod(group, 100)
        if not rest:
            word = _ORDINAL_HUNDREDS_PL.get(group) or _ORDINAL_BASE_PL[group]
        else:
            words = [_NUM_STRING_PL[hundreds * 100]] if hundreds else []
            if rest in _ORDINAL_BASE_PL:
                words.append(_ORDINAL_BASE_PL[rest])
            else:
                words += [_ORDINAL_BASE_PL[rest - rest % 10],
                          _ORDINAL_BASE_PL[rest % 10]]
            word = " ".join(words)
    if head:
        word = f"{pronounce_number_pl(head)} {word}"
    return word


def _ordinal_gender_pl(word, gender):
    """Inflect a masculine ordinal as an adjective: "pierwszy" -> "pierwsza",
    "pierwsze"; "drugi" -> "druga", "drugie"; "trzeci" -> "trzecia",
    "trzecie"."""
    if gender == GrammaticalGender.FEMININE:
        if word.endswith("y") or word.endswith("gi"):
            return word[:-1] + "a"
        return word + "a"
    if gender == GrammaticalGender.NEUTRAL:
        return word[:-1] + "e" if word.endswith("y") else word + "e"
    return word


def pronounce_ordinal_pl(number, gender=GrammaticalGender.MASCULINE):
    """
    Pronounce a number as a Polish ordinal in the nominative.

    Args:
        number (int): the number to pronounce
        gender (GrammaticalGender): gender of the noun the ordinal agrees with
    Returns:
        (str): the ordinal in Polish
    """
    number = int(number)
    if number <= 0:
        raise ValueError("Polish ordinals start at 1")
    return pronounce_number_pl(number, ordinals=True, gender=gender)


def extract_number_pl(text, short_scale=True, ordinals=False):
    """Deprecated: use ``ovos_number_parser.extract_number(text, "pl")``."""
    warn_reader_removed("extract_number_pl", 'ovos_number_parser.extract_number(text, "pl")')
    return numtag_readers.extract_number(text, "pl", short_scale, ordinals)


def numbers_to_digits_pl(text, short_scale=True, ordinals=False):
    """Deprecated: use ``ovos_number_parser.numbers_to_digits(text, "pl")``."""
    warn_reader_removed("numbers_to_digits_pl", 'ovos_number_parser.numbers_to_digits(text, "pl")')
    return numtag_readers.numbers_to_digits(text, "pl", Scale.SHORT if short_scale else Scale.LONG, ordinals)
