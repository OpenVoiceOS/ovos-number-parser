"""Hungarian number parsing and pronunciation.

The ordinal of a scale word: hu.wikipedia, article "Richard és Maurice
McDonald": "az ötven milliárdodik (50 000 000 000)". The billió and trillió
pairs follow the "milliomodik" and "milliárdodik" pattern.
"""
from decimal import Decimal, ROUND_HALF_UP
from math import floor

from ovos_number_parser import numtag_readers
from ovos_number_parser.util import convert_to_mixed_fraction, scientific_parts, warn_reader_removed

_NUM_STRING_HU = {
    0: 'nulla',
    1: 'egy',
    2: 'kettő',
    3: 'három',
    4: 'négy',
    5: 'öt',
    6: 'hat',
    7: 'hét',
    8: 'nyolc',
    9: 'kilenc',
    10: 'tíz',
    11: 'tizenegy',
    12: 'tizenkettő',
    13: 'tizenhárom',
    14: 'tizennégy',
    15: 'tizenöt',
    16: 'tizenhat',
    17: 'tizenhét',
    18: 'tizennyolc',
    19: 'tizenkilenc',
    20: 'húsz',
    30: 'harminc',
    40: 'negyven',
    50: 'ötven',
    60: 'hatvan',
    70: 'hetven',
    80: 'nyolcvan',
    90: 'kilencven',
    100: 'száz'
}

# Hungarian uses "long scale"
#    https://en.wikipedia.org/wiki/Long_and_short_scales
# Currently, numbers are limited to 1000000000000000000000000,
# but _NUM_POWERS_OF_TEN can be extended to include additional number words

_NUM_POWERS_OF_TEN = [
    '', 'ezer', 'millió', 'milliárd', 'billió', 'billiárd', 'trillió',
    'trilliárd'
]

_FRACTION_STRING_HU = {
    2: 'fél',
    3: 'harmad',
    4: 'negyed',
    5: 'ötöd',
    6: 'hatod',
    7: 'heted',
    8: 'nyolcad',
    9: 'kilenced',
    10: 'tized',
    11: 'tizenegyed',
    12: 'tizenketted',
    13: 'tizenharmad',
    14: 'tizennegyed',
    15: 'tizenötöd',
    16: 'tizenhatod',
    17: 'tizenheted',
    18: 'tizennyolcad',
    19: 'tizenkilenced',
    20: 'huszad'
}

# Numbers below 2 thousand are written in one word in Hungarian
# Numbers above 2 thousand are separated by hyphens
# In some circumstances it may better to seperate individual words
# Set _EXTRA_SPACE_HU=" " for separating numbers below 2 thousand (
# orthographically incorrect)
# Set _EXTRA_SPACE_HU="" for correct spelling, this is standard

# _EXTRA_SPACE_HU = " "
_EXTRA_SPACE_HU = ""


def _get_vocal_type_hu(word):
    # checks the vocal attributes of a word
    vowels_high = len([char for char in word if char in 'eéiíöőüű'])
    vowels_low = len([char for char in word if char in 'aáoóuú'])
    if vowels_high != 0 and vowels_low != 0:
        return 2                                   # 2: type is mixed
    return 0 if vowels_high == 0 else 1            # 0: type is low, 1: is high


def nice_number_hu(number, speech=True, denominators=range(1, 21)):
    """ Hungarian helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 és fél" for speech and "4 1/2" for text

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
    den_str = _FRACTION_STRING_HU[den]
    if whole == 0:
        if num == 1:
            one = 'egy ' if den != 2 else ''
            return_string = '{}{}'.format(one, den_str)
        else:
            return_string = '{} {}'.format(num, den_str)
    elif num == 1:
        pointOne = 'egész egy' if den != 2 else 'és'
        return_string = '{} {} {}'.format(whole, pointOne, den_str)
    else:
        return_string = '{} egész {} {}'.format(whole, num, den_str)
    return return_string


#: the fraction word of 10 ** n for n = 1 to 24: "tíz" or "száz" before the
#: fraction word of a power of 1000 fills the places between them. 24 places
#: is the most whose numerator the scale words of _NUM_POWERS_OF_TEN can read.
_FRACTION_SUFFIXES_HU = ['tized', 'század'] + [
    prefix + scale
    for scale in ('ezred', 'milliomod', 'milliárdod', 'billiomod',
                  'billiárdod', 'trilliomod', 'trilliárdod')
    for prefix in ('', 'tíz', 'száz')] + ['kvadrilliomod']

#: the multiplicative adverb of each digit, the "-szor" form that reads
#: "times" (Wiktionary "Module:number list/data/hu")
_ADVERBIAL_HU = {1: 'egyszer', 2: 'kétszer', 3: 'háromszor', 4: 'négyszer',
                 5: 'ötször', 6: 'hatszor', 7: 'hétszer', 8: 'nyolcszor',
                 9: 'kilencszer'}


def pronounce_scientific_hu(mantissa, exponent):
    """
    Read a mantissa times a negative power of ten

    The mantissa reads as the multiplicative adverb of a whole number: its
    digits move into a whole number and the exponent shifts with them, so
    1.5 and -25 read as fifteen times ten to the minus twenty-sixth. The
    suffix "-szor" goes on a cardinal numeral (Wiktionary "-szor"); on a
    fraction word such as "tized" it reads "for the tenth time". The adverb
    of a compound replaces its last unit word with that unit's adverb
    ("tizenkétszer", Wiktionary "Module:number list/data/hu").

    The power reads as "tíz a b-ediken": the base, the article and the
    exponent ordinal in the superessive, which takes "-on" after "-adik"
    and "-odik" and "-en" after "-edik" and "-ödik".

    Args:
        mantissa (int or float): from 1 to below 10, with its sign
        exponent (int): a negative power of ten
    Returns:
        (str): the reading, e.g. "hétszer tíz a mínusz harmincadikon" for
            7 and -30
    """
    digits = Decimal(str(abs(mantissa))).normalize()
    shift = digits.as_tuple().exponent
    whole = int(digits.scaleb(-shift))
    exponent += shift
    ordinal = pronounce_ordinal_hu(-exponent)
    ordinal += 'on' if ordinal.endswith(('adik', 'odik')) else 'en'
    sign = 'mínusz ' if mantissa < 0 else ''
    words = pronounce_number_hu(whole)
    times = words[:-len(_NUM_STRING_HU[whole % 10])] + \
        _ADVERBIAL_HU[whole % 10]
    return f"{sign}{times} tíz a mínusz {ordinal}"


def pronounce_number_hu(number, places=2, short_scale=True, scientific=False,
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

    # TODO short_scale, scientific and ordinals
    # currently ignored

    def pronounce_triplet_hu(num):
        result = ""
        num = floor(num)
        if num > 99:
            hundreds = floor(num / 100)
            if hundreds > 0:
                hundredConst = _EXTRA_SPACE_HU + 'száz' + _EXTRA_SPACE_HU
                if hundreds == 1:
                    result += hundredConst
                elif hundreds == 2:
                    result += 'két' + hundredConst
                else:
                    result += _NUM_STRING_HU[hundreds] + hundredConst
                num -= hundreds * 100
        if num == 0:
            result += ''  # do nothing
        elif num <= 20:
            result += _NUM_STRING_HU[num]  # + _EXTRA_SPACE_DA
        elif num > 20:
            ones = num % 10
            tens = num - ones
            if tens > 0:
                if tens != 20:
                    result += _NUM_STRING_HU[tens] + _EXTRA_SPACE_HU
                else:
                    result += "huszon" + _EXTRA_SPACE_HU
            if ones > 0:
                result += _NUM_STRING_HU[ones] + _EXTRA_SPACE_HU
        return result

    def pronounce_whole_number_hu(num, scale_level=0):
        if num == 0:
            return ''

        num = floor(num)
        result = ''
        last_triplet = num % 1000

        higher_groups = floor(num / 1000) > 0

        if last_triplet == 1:
            if scale_level == 0:
                if result != '':
                    result += '' + "egy"
                else:
                    result += "egy"
            elif scale_level == 1:
                # a lone thousands group is "ezer" on its own, but "egyezer"
                # once a higher (million+) group precedes it, and then the
                # group boundary takes a hyphen like any other above 2000
                if higher_groups:
                    result += "egy" + _NUM_POWERS_OF_TEN[1] + '-'
                else:
                    result += _EXTRA_SPACE_HU + \
                        _NUM_POWERS_OF_TEN[1] + _EXTRA_SPACE_HU
            else:
                result += "egy" + _NUM_POWERS_OF_TEN[scale_level] + '-'
        elif last_triplet > 1:
            result += pronounce_triplet_hu(last_triplet)
            if scale_level != 0:
                result = result.replace(_NUM_STRING_HU[2], 'két')
            if scale_level == 1:
                result += _NUM_POWERS_OF_TEN[1] + _EXTRA_SPACE_HU
            if scale_level >= 2:
                result += _NUM_POWERS_OF_TEN[scale_level]
            if scale_level > 0:
                result += '-'

        num //= 1000
        scale_level += 1
        return pronounce_whole_number_hu(num,
                                         scale_level) + result

    result = ""
    if abs(number) >= 1000000000000000000000000:  # cannot do more than this
        return str(number)
    elif number == 0:
        return str(_NUM_STRING_HU[0])
    elif number < 0:
        return "mínusz " + pronounce_number_hu(abs(number), places)
    else:
        if number == int(number):
            return pronounce_whole_number_hu(number).strip('-')
        else:
            whole_number_part = floor(number)
            if whole_number_part == 0:
                result += _NUM_STRING_HU[0]
            result += pronounce_whole_number_hu(whole_number_part).strip('-')
            if places > len(_FRACTION_SUFFIXES_HU) and \
                    number < 10 ** -len(_FRACTION_SUFFIXES_HU):
                # finer than the smallest denominator: the mantissa keeps
                # the digits ``places`` reads, as many as a whole number
                # below 10 ** 24 holds
                kept = places + Decimal(str(number)).adjusted()
                return pronounce_scientific_hu(*scientific_parts(
                    number, min(max(kept, 0), len(_FRACTION_SUFFIXES_HU) - 1)))
            if places > 0:
                places = min(places, len(_FRACTION_SUFFIXES_HU))
                result += " egész "
                numerator = int(((Decimal(str(number)) - whole_number_part)
                                 * 10 ** places).to_integral_value(ROUND_HALF_UP))
                fraction = pronounce_whole_number_hu(numerator).strip('-')
                result += fraction.replace(_NUM_STRING_HU[2], 'két') \
                    or _NUM_STRING_HU[0]
                result += ' ' + _FRACTION_SUFFIXES_HU[places - 1]
            return result


#: ordinal of each scale word
_SCALE_ORDINALS_HU = (
    ("ezer", "ezredik"),
    ("millió", "milliomodik"),
    ("milliárd", "milliárdodik"),
    ("billió", "billiomodik"),
    ("billiárd", "billiárdodik"),
    ("trillió", "trilliomodik"),
    ("trilliárd", "trilliárdodik"),
)


def pronounce_ordinal_hu(number):
    """
    This function pronounces a number as an ordinal

    1 -> first
    2 -> second

    Args:
        number (int): the number to format
    Returns:
        (str): The pronounced number string.
    """
    ordinals = ["nulladik", "első", "második", "harmadik", "negyedik",
                "ötödik", "hatodik", "hetedik", "nyolcadik", "kilencedik",
                "tizedik"]

    # only for whole positive numbers including zero
    if number < 0 or number != int(number):
        return number
    elif number < 11:
        return ordinals[number]
    elif number >= 10 ** 24:
        raise NotImplementedError(
            f"cannot pronounce {number} as a Hungarian ordinal")
    else:
        # concatenate parts and inflect them accordingly
        root = pronounce_number_hu(number)
        last_digit = number % 10
        if root == "húsz":
            root = "husz"
        for scale_word, scale_ordinal in _SCALE_ORDINALS_HU:
            if root.endswith(scale_word):
                return root[:-len(scale_word)] + scale_ordinal
        if last_digit == 1:
            return root + "edik"
        elif root[-1] == 'ő':
            return root[:-1] + 'edik'
        elif last_digit != 0:
            return ordinals[last_digit].join(
                root.rsplit(_NUM_STRING_HU[last_digit], 1))
        vtype = _get_vocal_type_hu(root)
        return root + "edik" if vtype == 1 else root + "adik"


# word → value map used to split compound numbers, including the allomorphs
# that only appear inside compounds ("két", "huszon")
_STRING_NUM_HU = {word: val for val, word in _NUM_STRING_HU.items()}
_STRING_NUM_HU["két"] = 2
_STRING_NUM_HU["huszon"] = 20


_STRING_FRACTION_HU = {word: val for val, word in _FRACTION_STRING_HU.items()}


_ORDINAL_REVERSE_HU = {}


def is_ordinal_hu(input_str):
    """
    Check if the given word is a Hungarian ordinal number.

    Args:
        input_str (str): the string to check if ordinal
    Returns:
        (bool) or (int): False if not an ordinal, otherwise the number
    """
    if not _ORDINAL_REVERSE_HU:
        candidates = list(range(0, 101)) + \
            [n * 100 for n in range(1, 11)] + [1000, 1000000]
        for n in candidates:
            _ORDINAL_REVERSE_HU[pronounce_ordinal_hu(n)] = n
    return _ORDINAL_REVERSE_HU.get(input_str.lower().strip(), False)


def is_fractional_hu(input_str, short_scale=True):
    """
    Check if the given word is a Hungarian fraction.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): ignored, present for API compatibility
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction
    """
    word = input_str.lower().strip()
    if word in _STRING_FRACTION_HU:
        return 1.0 / _STRING_FRACTION_HU[word]
    return False


def extract_number_hu(text, short_scale=True, ordinals=False):
    """Deprecated: use ``ovos_number_parser.extract_number(text, "hu")``."""
    warn_reader_removed("extract_number_hu", 'ovos_number_parser.extract_number(text, "hu")')
    return numtag_readers.extract_number(text, "hu", short_scale, ordinals)
