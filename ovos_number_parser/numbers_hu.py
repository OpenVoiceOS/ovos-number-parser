from math import floor
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
    """
    Determine the vowel harmony type of a Hungarian word.
    
    Returns:
        int: 0 if the word contains only low vowels, 1 if only high vowels, 2 if both (mixed).
    """
    vowels_high = len([char for char in word if char in 'eéiíöőüű'])
    vowels_low = len([char for char in word if char in 'aáoóuú'])
    if vowels_high != 0 and vowels_low != 0:
        return 2                                   # 2: type is mixed
    return 0 if vowels_high == 0 else 1            # 0: type is low, 1: is high


def pronounce_number_hu(number, places=2, short_scale=True, scientific=False,
                        ordinals=False):
    """
                        Convert a number to its spoken Hungarian equivalent as a cardinal number.
                        
                        Handles integers and floats, including negative numbers and zero. For floats, pronounces the whole part, inserts "egész" (whole), and then pronounces the fractional part with the appropriate Hungarian fractional suffix (e.g., 'tized' for tenths, 'század' for hundredths). For very large numbers (≥ 10^24), returns the number as a string. Ignores the `short_scale`, `scientific`, and `ordinals` parameters.
                        
                        Parameters:
                            number (int or float): The number to pronounce.
                            places (int): Maximum number of decimal places to pronounce (default is 2).
                        
                        Returns:
                            str: The pronounced Hungarian representation of the number.
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

        if last_triplet == 1:
            if scale_level == 0:
                if result != '':
                    result += '' + "egy"
                else:
                    result += "egy"
            elif scale_level == 1:
                result += _EXTRA_SPACE_HU + \
                          _NUM_POWERS_OF_TEN[1] + _EXTRA_SPACE_HU
            else:
                result += "egy" + _NUM_POWERS_OF_TEN[scale_level]
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

        num = floor(num / 1000)
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
            fractional_part = number - whole_number_part
            if whole_number_part == 0:
                result += _NUM_STRING_HU[0]
            result += pronounce_whole_number_hu(whole_number_part)
            if places > 0:
                result += " egész "
                fraction = pronounce_whole_number_hu(
                    round(fractional_part * 10 ** places))
                result += fraction.replace(_NUM_STRING_HU[2], 'két')
                fraction_suffixes = [
                    'tized', 'század', 'ezred', 'tízezred', 'százezred']
                if places <= len(fraction_suffixes):
                    result += ' ' + fraction_suffixes[places - 1]
            return result


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
    big_ordinals = ["", "ezredik", "milliomodik"]

    # only for whole positive numbers including zero
    if number < 0 or number != int(number):
        return number
    elif number < 11:
        return ordinals[number]
    else:
        # concatenate parts and inflect them accordingly
        root = pronounce_number_hu(number)
        vtype = _get_vocal_type_hu(root)
        last_digit = number - floor(number / 10) * 10
        if root == "húsz":
            root = "husz"
        if number % 1000000 == 0:
            return root.replace(_NUM_POWERS_OF_TEN[2], big_ordinals[2])
        if number % 1000 == 0:
            return root.replace(_NUM_POWERS_OF_TEN[1], big_ordinals[1])
        if last_digit == 1:
            return root + "edik"
        elif root[-1] == 'ő':
            return root[:-1] + 'edik'
        elif last_digit != 0:
            return ordinals[last_digit].join(
                root.rsplit(_NUM_STRING_HU[last_digit], 1))
        return root + "edik" if vtype == 1 else root + "adik"
