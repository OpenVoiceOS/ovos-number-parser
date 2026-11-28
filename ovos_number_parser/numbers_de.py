import re
from collections import OrderedDict
from decimal import Decimal
from math import floor

from ovos_number_parser.util import (invert_dict, convert_to_mixed_fraction, GrammaticalGender, numeric_value, Scale,
                                     warn_reader_removed)
from ovos_number_parser import numtag_readers

#: the final 1 of a whole number before a feminine or neuter noun (ICU RBNF de
#: spellout-cardinal-feminine and -neuter: "eine", "einhunderteine", "ein").
#: The masculine keeps the counting form "eins": it is the default gender, so
#: it also serves a caller that names no noun.
_GENDERED_ONE_DE = {
    GrammaticalGender.FEMININE: "eine",
    GrammaticalGender.NEUTRAL: "ein",
}


#: German groups the digits of a whole number by threes with ".", and marks
#: the decimal with "," (CLDR de): "12.000" is 12000, "12.000,5" is 12000.5
_DIGIT_GROUP_MARK_DE = "."
_GROUPED_DIGITS_DE = re.compile(
    rf"-?[1-9]\d{{0,2}}(?:{re.escape(_DIGIT_GROUP_MARK_DE)}\d{{3}})+(?:,\d+)?")

# _SPOKEN_NUMBER
_NUM_STRING = {
    0: 'null',
    1: 'eins',
    2: 'zwei',
    3: 'drei',
    4: 'vier',
    5: 'fünf',
    6: 'sechs',
    7: 'sieben',
    8: 'acht',
    9: 'neun',
    10: 'zehn',
    11: 'elf',
    12: 'zwölf',
    13: 'dreizehn',
    14: 'vierzehn',
    15: 'fünfzehn',
    16: 'sechzehn',
    17: 'siebzehn',
    18: 'achtzehn',
    19: 'neunzehn',
    20: 'zwanzig',
    30: 'dreißig',
    40: 'vierzig',
    50: 'fünfzig',
    60: 'sechzig',
    70: 'siebzig',
    80: 'achtzig',
    90: 'neunzig',
    100: 'hundert',
    200: 'zweihundert',
    300: 'dreihundert',
    400: 'vierhundert',
    500: 'fünfhundert',
    600: 'sechshundert',
    700: 'siebenhundert',
    800: 'achthundert',
    900: 'neunhundert',
    1000: 'tausend',
    1000000: 'million'
}

_STRING_NUM = invert_dict(_NUM_STRING)
_STRING_NUM.update({
    'ein': 1,
    'eine': 1,
    'einer': 1,
    'eines': 1,
    'einem': 1,
    'einen': 1
})

_MONTHS = ['januar', 'februar', 'märz', 'april', 'mai', 'juni',
           'juli', 'august', 'september', 'oktober', 'november',
           'dezember']

# German uses "long scale" https://en.wikipedia.org/wiki/Long_and_short_scales
# Currently, numbers are limited to 1000000000000000000000000,
# but _NUM_POWERS_OF_TEN can be extended to include additional number words


_NUM_POWERS_OF_TEN = [
    '', 'tausend', 'Million', 'Milliarde', 'Billion', 'Billiarde', 'Trillion',
    'Trilliarde'
]

_FRACTION_STRING = {
    2: 'halb',
    3: 'drittel',
    4: 'viertel',
    5: 'fünftel',
    6: 'sechstel',
    7: 'siebtel',
    8: 'achtel',
    9: 'neuntel',
    10: 'zehntel',
    11: 'elftel',
    12: 'zwölftel',
    13: 'dreizehntel',
    14: 'vierzehntel',
    15: 'fünfzehntel',
    16: 'sechzehntel',
    17: 'siebzehntel',
    18: 'achtzehntel',
    19: 'neunzehntel',
    20: 'zwanzigstel'
}

_STRING_FRACTION = invert_dict(_FRACTION_STRING)
_STRING_FRACTION.update({
    'halb': 2,
    'halbe': 2,
    'halben': 2,
    'halbes': 2,
    'halber': 2,
    'halbem': 2
})

# Numbers below 1 million are written in one word in German, yielding very
# long words
# In some circumstances it may better to seperate individual words
# Set _EXTRA_SPACE_DA=" " for separating numbers below 1 million (
# orthographically incorrect)
# Set _EXTRA_SPACE_DA="" for correct spelling, this is standard

# _EXTRA_SPACE_DA = " "
_EXTRA_SPACE = ""

_ORDINAL_BASE = {
    "1.": "erst",
    "2.": "zweit",
    "3.": "dritt",
    "4.": "viert",
    "5.": "fünft",
    "6.": "sechst",
    "7.": "siebt",
    "8.": "acht",
    "9.": "neunt",
    "10.": "zehnt",
    "11.": "elft",
    "12.": "zwölft",
    "13.": "dreizehnt",
    "14.": "vierzehnt",
    "15.": "fünfzehnt",
    "16.": "sechzehnt",
    "17.": "siebzehnt",
    "18.": "achtzehnt",
    "19.": "neunzehnt",
    "20.": "zwanzigst",
    "21.": "einundzwanzigst",
    "22.": "zweiundzwanzigst",
    "23.": "dreiundzwanzigst",
    "24.": "vierundzwanzigst",
    "25.": "fünfundzwanzigst",
    "26.": "sechsundzwanzigst",
    "27.": "siebenundzwanzigst",
    "28.": "achtundzwanzigst",
    "29.": "neunundzwanzigst",
    "30.": "dreißigst",
    "31.": "einunddreißigst",
    "32.": "zweiunddreißigst",
    "33.": "dreiunddreißigst",
    "34.": "vierunddreißigst",
    "35.": "fünfunddreißigst",
    "36.": "sechsunddreißigst",
    "37.": "siebenunddreißigst",
    "38.": "achtunddreißigst",
    "39.": "neununddreißigst",
    "40.": "vierzigst",
    "41.": "einundvierzigst",
    "42.": "zweiundvierzigst",
    "43.": "dreiundvierzigst",
    "44.": "vierundvierzigst",
    "45.": "fünfundvierzigst",
    "46.": "sechsundvierzigst",
    "47.": "siebenundvierzigst",
    "48.": "achtundvierzigst",
    "49.": "neunundvierzigst",
    "50.": "fünfzigst",
    "51.": "einundfünfzigst",
    "52.": "zweiundfünfzigst",
    "53.": "dreiundfünfzigst",
    "60.": "sechzigst",
    "70.": "siebzigst",
    "80.": "achtzigst",
    "90.": "neunzigst",
    "100.": "einhundertst",
    "1000.": "eintausendst",
    "1000000.": "millionst"
}

_LONG_SCALE = OrderedDict([
    (100, 'hundert'),
    (1000, 'tausend'),
    (1000000, 'million'),
    (10 ** 9, "milliarde"),
    (10 ** 12, 'billion'),
    (10 ** 15, "billiarde"),
    (10 ** 18, "trillion"),
    (10 ** 21, "trilliarde"),
    (10 ** 24, "quadrillion"),
    (10 ** 27, "quadrilliarde")
])

_MULTIPLIER = set(_LONG_SCALE.values())

_STRING_LONG_SCALE = invert_dict(_LONG_SCALE)

# ending manipulation
for number, item in _LONG_SCALE.items():
    if int(number) > 1000:
        if item.endswith('e'):
            name = item + 'n'
            _MULTIPLIER.add(name)
            _STRING_LONG_SCALE[name] = number
        else:
            name = item + 'en'
            _MULTIPLIER.add(name)
            _STRING_LONG_SCALE[name] = number

_LONG_ORDINAL = {
    1e6: "millionst",
    1e9: "milliardst",
    1e12: "billionst",
    1e15: "billiardst",
    1e18: "trillionst",
    1e21: "trilliardst",
    1e24: "quadrillionst",
    1e27: "quadrilliardst"
}

_LONG_ORDINAL.update(_ORDINAL_BASE)


def nice_number_de(number, speech=True, denominators=range(1, 21)):
    """ German helper for nice_number
    This function formats a float to human understandable functions. Like
    4.5 becomes "4 einhalb" for speech and "4 1/2" for text
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
        return str(round(number, 3)).replace(".", ",")
    whole, num, den = result
    if not speech:
        if num == 0:
            # TODO: Number grouping?  E.g. "1,000,000"
            return str(whole)
        else:
            return '{} {}/{}'.format(whole, num, den)
    if num == 0:
        return str(whole)
    den_str = _FRACTION_STRING[den]
    if whole == 0:
        if num == 1:
            return_string = 'ein {}'.format(den_str)
        else:
            return_string = '{} {}'.format(num, den_str)
    elif num == 1:
        return_string = '{} und ein {}'.format(whole, den_str)
    else:
        return_string = '{} und {} {}'.format(whole, num, den_str)

    return return_string


def pronounce_number_de(number, places=2, short_scale=True, scientific=False,
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
        gender (GrammaticalGender): gender of the noun a whole number counts
    Returns:
        (str): The pronounced number
    """

    # TODO short_scale, scientific and ordinals
    # currently ignored

    # a decimal keeps "eins" ("eins Komma fünf")
    one = _GENDERED_ONE_DE.get(gender, "eins") if number % 1 == 0 else "eins"

    def pronounce_triplet_de(num, one="eins"):
        result = ""
        num = floor(num)
        if num > 99:
            hundreds = floor(num / 100)
            if hundreds > 0:
                number = _NUM_STRING[hundreds] if hundreds > 1 else "ein"
                result += number + 'hundert' + _EXTRA_SPACE
                num -= hundreds * 100
        if num == 0:
            result += ''  # do nothing
        elif num == 1:
            result += one  # need the s for the last digit
        elif num <= 20:
            result += _NUM_STRING[num]  # + _EXTRA_SPACE_DA
        elif num > 20:
            ones = num % 10
            tens = num - ones
            if ones > 0:
                number = _NUM_STRING[ones]
                if ones == 1 and tens > 0:  # eins > ein
                    number = number[:-1]
                result += number + _EXTRA_SPACE
                if tens > 0:
                    result += 'und' + _EXTRA_SPACE
            if tens > 0:
                result += _NUM_STRING[tens] + _EXTRA_SPACE
        return result

    def pronounce_fractional_de(num,
                                places):  # fixed number of places even with
        # trailing zeros
        result = ""
        for digit in f"{Decimal(str(num)):f}".split(".")[1][:places].ljust(places, "0"):
            word = _NUM_STRING[int(digit)]
            if digit == "1" and not word.endswith("s"):
                word += "s"  # "1" is pronounced "eins" after the decimal point
            result += " " + word
        return result

    def pronounce_whole_number_de(num, scale_level=0):
        if num == 0:
            return ''

        num = floor(num)
        result = ''
        last_triplet = num % 1000

        if last_triplet == 1:
            if scale_level == 0:
                if result != '':
                    result += '' + one
                else:
                    result += one
            elif scale_level == 1:
                result += 'ein' + _EXTRA_SPACE + 'tausend' + _EXTRA_SPACE
            else:
                result += "eine " + _NUM_POWERS_OF_TEN[scale_level] + ' '
        elif last_triplet > 1:
            # Before "tausend" the cardinal is "ein", not "eins":
            # "einhunderteintausend" (not "einhunderteinstausend").
            one_for_scale = one if scale_level == 0 else (
                "ein" if scale_level == 1 else "eins")
            result += pronounce_triplet_de(last_triplet, one_for_scale)
            if scale_level == 1:
                # result += _EXTRA_SPACE_DA
                result += 'tausend' + _EXTRA_SPACE
            if scale_level >= 2:
                # if _EXTRA_SPACE_DA == '':
                #    result += " "
                result += " " + _NUM_POWERS_OF_TEN[scale_level]
            if scale_level >= 2:
                if scale_level % 2 == 0:
                    result += "e"  # MillionE
                result += "n "  # MilliardeN, MillioneN

        num //= 1000
        scale_level += 1
        return pronounce_whole_number_de(num,
                                         scale_level) + result  # + _EXTRA_SPACE_DA

    result = ""
    if abs(number) >= 1000000000000000000000000:  # cannot do more than this
        return str(number)
    elif number == 0:
        return str(_NUM_STRING[0])
    elif number < 0:
        return "minus " + pronounce_number_de(abs(number), places, gender=gender)
    else:
        # a scale word ends in the space that joins it to the lower
        # triplets, so a number with no lower triplets ends in that space
        if number == int(number):
            return pronounce_whole_number_de(number).rstrip()
        else:
            whole_number_part = floor(number)
            result += pronounce_whole_number_de(whole_number_part).rstrip() \
                or _NUM_STRING[0]
            if places > 0:
                result += " Komma"
                result += pronounce_fractional_de(number, places)
            return result


def pronounce_ordinal_de(number):
    """
      This function pronounces a number as an ordinal

      1 -> first
      2 -> second

      Args:
          number (int): the number to format
      Returns:
          (str): The pronounced number string.
      """
    # ordinals for 1, 3, 7 and 8 are irregular
    # this produces the base form, it will have to be adapted for genus,
    # casus, numerus

    # only for whole positive numbers including zero
    if number < 0 or number != int(number):
        return number
    elif number >= 10 ** 24:
        raise NotImplementedError(
            f"cannot pronounce {number} as a German ordinal")
    number = int(number)
    last = number % 100
    if 0 < last < 20:
        # the ending follows the last word: "einhunderterste",
        # "hundertneunzehnte", "eine Million dritte"
        tail = _NUM_STRING[last]
        return pronounce_number_de(number)[:-len(tail)] + \
            _ORDINAL_BASE[f"{last}."] + "e"
    if number == 0:
        return "nullte"
    return pronounce_number_de(number) + "ste"


def _get_ordinal_index(input_str: str, type_: type = str):
    warn_reader_removed("_get_ordinal_index", 'ovos_number_parser.is_ordinal(text, "de")')
    if input_str.endswith(".") and is_numeric_de(input_str[:-1]):
        return type_(input_str.replace(".", ""))
    value = numtag_readers.is_ordinal(input_str, "de")
    return type_(value) if value else value


def _ungroup_digits_de(word: str) -> str:
    if _GROUPED_DIGITS_DE.fullmatch(word):
        return word.replace(_DIGIT_GROUP_MARK_DE, "").replace(",", ".")
    return word


def is_number_de(word: str):
    if is_numeric_de(word):
        return numeric_value(_ungroup_digits_de(word))
    elif word in _STRING_NUM:
        return _STRING_NUM.get(word)
    elif word in _STRING_LONG_SCALE:
        return _STRING_LONG_SCALE.get(word)

    return None


def is_numeric_de(input_str):
    """
    Takes in a string and tests to see if it is a number.

    Args:
        text (str): string to test if a number
    Returns:
        (bool): True if a number, else False
    """
    # da float("1.") = 1.0
    if input_str.endswith('.'):
        return False
    try:
        numeric_value(_ungroup_digits_de(input_str))
        return True
    except ValueError:
        return False


def numbers_to_digits_de(text, short_scale=False, ordinals=False, fractions=True):
    """Deprecated: use ``ovos_number_parser.numbers_to_digits(text, "de")``."""
    warn_reader_removed("numbers_to_digits_de", 'ovos_number_parser.numbers_to_digits(text, "de")')
    return numtag_readers.numbers_to_digits(text, "de", Scale.SHORT if short_scale else Scale.LONG, ordinals)
