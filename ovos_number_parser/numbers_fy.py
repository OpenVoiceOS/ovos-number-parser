from decimal import Decimal
from math import floor

from ovos_number_parser.util import convert_to_mixed_fraction, invert_dict


_NUM_STRING_FY = {
    0: 'nul',
    1: 'ien',
    2: 'twa',
    3: 'trije',
    4: 'fjouwer',
    5: 'fiif',
    6: 'seis',
    7: 'sân',
    8: 'acht',
    9: 'njoggen',
    10: 'tsien',
    11: 'alve',
    12: 'tolve',
    13: 'trettjin',
    14: 'fjirtjin',
    15: 'fyftjin',
    16: 'sechstjin',
    17: 'santjin',
    18: 'achttjin',
    19: 'njoggentjin',
    20: 'tweintich',
    30: 'tritich',
    40: 'fjirtich',
    50: 'fyftich',
    60: 'sechstich',
    70: 'santich',
    80: 'tachtich',
    90: 'njoggentich',
    100: 'hûndert'
}

_FRACTION_STRING_FY = {
    2: 'heal',
    3: 'tredde',
    4: 'fjirde',
    5: 'fyfte',
    6: 'sechste',
    7: 'sânde',
    8: 'achtste',
    9: 'njoggende',
    10: 'tsiende',
    11: 'alfde',
    12: 'tolfde',
    13: 'trettjinde',
    14: 'fjirtjinde',
    15: 'fyftjinde',
    16: 'sechstjinde',
    17: 'santjinde',
    18: 'achttjinde',
    19: 'njoggentjinde',
    20: 'tweintichste'
}


_ORDINAL_STRING_BASE_FY = {
    1: 'earste',
    2: 'twadde',
    3: 'tredde',
    4: 'fjirde',
    5: 'fyfte',
    6: 'sechste',
    7: 'sânde',
    8: 'achtste',
    9: 'njoggende',
    10: 'tsiende',
    11: 'alfde',
    12: 'tolfde',
    13: 'trettjinde',
    14: 'fjirtjinde',
    15: 'fyftjinde',
    16: 'sechstjinde',
    17: 'santjinde',
    18: 'achttjinde',
    19: 'njoggentjinde',
    20: 'tweintichste',
    30: 'tritichste',
    40: 'fjirtichste',
    50: 'fyftichste',
    60: 'sechstichste',
    70: 'santichste',
    80: 'tachtichste',
    90: 'njoggentichste',
    1e2: 'hûndertste',
    1e3: 'tûzenste'
}

_SHORT_ORDINAL_STRING_FY = {
    1e6: 'miljoenste',
    1e9: 'miljardste',
    1e12: 'biljoenste',
    1e15: 'biljardste',
    1e18: 'triljoenste',
    1e21: 'triljardste'
}
_SHORT_ORDINAL_STRING_FY.update(_ORDINAL_STRING_BASE_FY)

_LONG_ORDINAL_STRING_FY = {
    1e6: 'miljoenste',
    1e12: 'biljoenste',
    1e18: 'triljoenste'
}
_LONG_ORDINAL_STRING_FY.update(_ORDINAL_STRING_BASE_FY)


_STRING_NUM_FY = invert_dict(_NUM_STRING_FY)
_STRING_NUM_FY.update({
    # spellings without diacritics, common in ASR output
    "san": 7,
    "hundert": 100,
    "tuzen": 1000,
    # variant teen/ten spellings without the etymological -s-
    "sechtjin": 16,
    "sechtich": 60,
    "heal": 0.5,
})


# Numbers below 1 million are written in one word in West Frisian, just as
# in Dutch: units come before the tens, joined with "en" (ienentweintich)

_NUM_POWERS_OF_TEN_FY = [
    '', 'tûzen', 'miljoen', 'miljard', 'biljoen', 'biljard', 'triljoen',
    'triljard'
]

_EXTRA_SPACE_FY = ""


def nice_number_fy(number, speech=True, denominators=range(1, 21)):
    """ West Frisian helper for nice_number

    This function formats a float to a human understandable string. Like
    4.5 becomes "4 en in heal" for speech and "4 1/2" for text

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
            return str(whole)
        else:
            return '{} {}/{}'.format(whole, num, den)
    if num == 0:
        return str(whole)
    den_str = _FRACTION_STRING_FY[den]
    if whole == 0:
        if num == 1:
            return_string = 'ien {}'.format(den_str)
        else:
            return_string = '{} {}'.format(num, den_str)
    elif num == 1:
        return_string = '{} en ien {}'.format(whole, den_str)
    else:
        return_string = '{} en {} {}'.format(whole, num, den_str)

    return return_string


def pronounce_number_fy(number, places=2, short_scale=True, scientific=False,
                        ordinals=False):
    """
    Convert a number to its spoken West Frisian equivalent

    For example, '5.2' would return 'fiif komma twa'

    Args:
        number(float or int): the number to pronounce
        places(int): maximum decimal places to speak
        short_scale (bool) : use short (True) or long scale (False)
            https://en.wikipedia.org/wiki/Names_of_large_numbers
        scientific (bool): pronounce in scientific notation
        ordinals (bool): pronounce in ordinal form "first" instead of "one"
    Returns:
        (str): The pronounced number
    """
    if ordinals and number == int(number) and number >= 0:
        return pronounce_ordinal_fy(number)

    def pronounce_triplet_fy(num):
        result = ""
        num = floor(num)
        if num > 99:
            hundreds = floor(num / 100)
            if hundreds > 0:
                result += _NUM_STRING_FY[hundreds] + _EXTRA_SPACE_FY + 'hûndert' + _EXTRA_SPACE_FY
                num -= hundreds * 100
        if num == 0:
            result += ''  # do nothing
        elif num <= 20:
            result += _NUM_STRING_FY[num]
        elif num > 20:
            ones = num % 10
            tens = num - ones
            if ones > 0:
                result += _NUM_STRING_FY[ones] + _EXTRA_SPACE_FY
                if tens > 0:
                    result += 'en' + _EXTRA_SPACE_FY
            if tens > 0:
                result += _NUM_STRING_FY[tens] + _EXTRA_SPACE_FY
        return result

    def pronounce_fractional_fy(num, places):
        # fixed number of places even with trailing zeros
        result = ""
        for digit in f"{Decimal(str(num)):f}".split(".")[1][:places].ljust(places, "0"):
            result += " " + _NUM_STRING_FY[int(digit)]
        return result

    def pronounce_whole_number_fy(num, scale_level=0):
        if num == 0:
            return ''

        num = floor(num)
        result = ''
        last_triplet = num % 1000

        if last_triplet == 1:
            if scale_level == 0:
                result += "ien"
            elif scale_level == 1:
                result += 'ien' + _EXTRA_SPACE_FY + 'tûzen' + _EXTRA_SPACE_FY
            else:
                result += "ien " + _NUM_POWERS_OF_TEN_FY[scale_level] + ' '
        elif last_triplet > 1:
            result += pronounce_triplet_fy(last_triplet)
            if scale_level == 1:
                result += 'tûzen' + _EXTRA_SPACE_FY
            if scale_level >= 2:
                result += " " + _NUM_POWERS_OF_TEN_FY[scale_level] + ' '

        num //= 1000
        scale_level += 1
        return pronounce_whole_number_fy(num, scale_level) + result

    result = ""
    if abs(number) >= 1000000000000000000000000:  # cannot do more than this
        return str(number)
    elif number == 0:
        return str(_NUM_STRING_FY[0])
    elif number < 0:
        return "min " + pronounce_number_fy(abs(number), places,
                                            ordinals=ordinals)
    else:
        if number == int(number):
            return pronounce_whole_number_fy(number)
        else:
            whole_number_part = floor(number)
            result += pronounce_whole_number_fy(whole_number_part) or \
                _NUM_STRING_FY[0]
            if places > 0:
                result += " komma"
                result += pronounce_fractional_fy(number, places)
            return result


def pronounce_ordinal_fy(number):
    """
    This function pronounces a West Frisian number as an ordinal

    1 -> earste
    2 -> twadde

    Args:
        number (int): the number to format
    Returns:
        (str): The pronounced number string.
    """
    # only for whole positive numbers including zero
    if number < 0 or number != int(number):
        return number
    number = int(number)
    if number >= 10 ** 24:
        raise NotImplementedError(
            f"cannot pronounce {number} as a West Frisian ordinal")
    if number in _ORDINAL_STRING_BASE_FY:
        return _ORDINAL_STRING_BASE_FY[number]
    if number in _SHORT_ORDINAL_STRING_FY:
        return _SHORT_ORDINAL_STRING_FY[number]
    # compounds: cardinal + table-driven last element, mirroring the
    # cardinal compounding ("ienentweintich" -> "ienentweintichste").
    # zero has no compound tens element, so it takes the regular suffix
    # like the sibling Dutch "nulste"
    if 0 < number < 100:
        ones = number % 10
        tens = number - ones
        return _NUM_STRING_FY[ones] + "en" + _ORDINAL_STRING_BASE_FY[tens]
    return pronounce_number_fy(number) + "ste"


def is_fractional_fy(input_str, short_scale=True):
    """This function takes the given text and checks if it is a fraction.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): use short scale if True, long scale if False
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction
    """
    fracts = {"hiel": 1, "heal": 2, "healve": 2, "kwart": 4}
    if short_scale:
        for num in _SHORT_ORDINAL_STRING_FY:
            if num > 2:
                fracts[_SHORT_ORDINAL_STRING_FY[num]] = num
    else:
        for num in _LONG_ORDINAL_STRING_FY:
            if num > 2:
                fracts[_LONG_ORDINAL_STRING_FY[num]] = num

    if input_str.lower() in fracts:
        return 1.0 / fracts[input_str.lower()]
    return False
