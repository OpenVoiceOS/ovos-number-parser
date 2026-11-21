"""Croatian number parsing and pronunciation.

Croatian writes compound numerals as separate words ("dvadeset jedan" = 21),
optionally joined with "i" ("dvadeset i jedan"). Scale words decline with
the count: "tisuću" (1000), "dvije tisuće" (2000), "pet tisuća" (5000),
"milijun" / "dva milijuna", "milijarda" / "dvije milijarde" / "pet milijardi".
Croatian uses the long scale (milijun = 1e6, milijarda = 1e9, bilijun = 1e12).
"""
from decimal import Decimal
from collections import OrderedDict

from ovos_number_parser.util import convert_to_mixed_fraction, invert_dict, scientific_parts

_NUM_STRING_HR = {
    0: 'nula',
    1: 'jedan',
    2: 'dva',
    3: 'tri',
    4: 'četiri',
    5: 'pet',
    6: 'šest',
    7: 'sedam',
    8: 'osam',
    9: 'devet',
    10: 'deset',
    11: 'jedanaest',
    12: 'dvanaest',
    13: 'trinaest',
    14: 'četrnaest',
    15: 'petnaest',
    16: 'šesnaest',
    17: 'sedamnaest',
    18: 'osamnaest',
    19: 'devetnaest',
    20: 'dvadeset',
    30: 'trideset',
    40: 'četrdeset',
    50: 'pedeset',
    60: 'šezdeset',
    70: 'sedamdeset',
    80: 'osamdeset',
    90: 'devedeset',
    100: 'sto',
    200: 'dvjesto',
    300: 'tristo',
    400: 'četiristo',
    500: 'petsto',
    600: 'šesto',
    700: 'sedamsto',
    800: 'osamsto',
    900: 'devetsto'
}

_FRACTION_STRING_HR = {
    2: 'polovina',
    3: 'trećina',
    4: 'četvrtina',
    5: 'petina',
    6: 'šestina',
    7: 'sedmina',
    8: 'osmina',
    9: 'devetina',
    10: 'desetina',
    11: 'jedanaestina',
    12: 'dvanaestina',
    13: 'trinaestina',
    14: 'četrnaestina',
    15: 'petnaestina',
    16: 'šesnaestina',
    17: 'sedamnaestina',
    18: 'osamnaestina',
    19: 'devetnaestina',
    20: 'dvadesetina',
    1e2: 'stotinka',
    1e3: 'tisućinka'
}

# Croatian scale words (long scale: each power of 1000 alternates
# -ijun / -ijarda). The same names apply regardless of the short_scale
# flag, since Croatian only uses the long scale.
_SCALE_HR = OrderedDict([
    (1e3, 'tisuća'),
    (1e6, 'milijun'),
    (1e9, 'milijarda'),
    (1e12, 'bilijun'),
    (1e15, 'bilijarda'),
    (1e18, 'trilijun'),
    (1e21, 'trilijarda'),
    (1e24, 'kvadrilijun'),
])

_ORDINAL_BASE_HR = {
    1: 'prvi',
    2: 'drugi',
    3: 'treći',
    4: 'četvrti',
    5: 'peti',
    6: 'šesti',
    7: 'sedmi',
    8: 'osmi',
    9: 'deveti',
    10: 'deseti',
    11: 'jedanaesti',
    12: 'dvanaesti',
    13: 'trinaesti',
    14: 'četrnaesti',
    15: 'petnaesti',
    16: 'šesnaesti',
    17: 'sedamnaesti',
    18: 'osamnaesti',
    19: 'devetnaesti',
    20: 'dvadeseti',
    30: 'trideseti',
    40: 'četrdeseti',
    50: 'pedeseti',
    60: 'šezdeseti',
    70: 'sedamdeseti',
    80: 'osamdeseti',
    90: 'devedeseti',
    1e2: 'stoti',
    1e3: 'tisući'
}

_ORDINAL_HUNDREDS_HR = {
    200: 'dvjestoti', 300: 'tristoti', 400: 'četiristoti',
    500: 'petstoti', 600: 'šeststoti', 700: 'sedamstoti',
    800: 'osamstoti', 900: 'devetstoti',
}

_SHORT_ORDINAL_HR = {
    1e6: 'milijunti',
}
_SHORT_ORDINAL_HR.update(_ORDINAL_BASE_HR)


_STRING_NUM_HR = invert_dict(_NUM_STRING_HR)
_STRING_NUM_HR.update({
    "dvjesta": 200,
    "šeststo": 600,
    "polovina": 0.5,
    "polovica": 0.5,
    "pola": 0.5,
    "pol": 0.5,
})


def plural_hr(num: int, one: str, few: str, many: str):
    """Pick the Croatian noun form that follows the number ``num``."""
    num %= 100
    if num // 10 == 1:
        return many
    if num % 10 == 1:
        return one
    if 2 <= num % 10 <= 4:
        return few
    return many


def _feminine_hr(spoken: str) -> str:
    """Turn a trailing masculine numeral into its feminine form."""
    if spoken.endswith("jedan"):
        return spoken[:-len("jedan")] + "jedna"
    if spoken.endswith("dva"):
        return spoken[:-len("dva")] + "dvije"
    return spoken


def nice_number_hr(number, speech=True, denominators=range(1, 21)):
    """Croatian helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 i pol" for speech and "4 1/2" for text

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
    den_str = plural_hr(num, _FRACTION_STRING_HR[den],
                        _FRACTION_STRING_HR[den][:-1] + 'e',
                        _FRACTION_STRING_HR[den])
    if whole == 0:
        if num == 1:
            return_string = '{}'.format(den_str)
        else:
            return_string = '{} {}'.format(num, den_str)
    elif num == 1 and den == 2:
        return_string = '{} i pol'.format(whole)
    else:
        return_string = '{} i {} {}'.format(whole, num, den_str)

    return return_string


def pronounce_number_hr(number, places=2, short_scale=True, scientific=False,
                        ordinals=False):
    """
    Convert a number to it's spoken equivalent

    For example, '5.2' would return 'pet zarez dva'

    Args:
        number(float or int): the number to pronounce
        places(int): maximum decimal places to speak
        short_scale (bool): ignored, Croatian only uses the long scale
        scientific (bool): pronounce in scientific notation
        ordinals (bool): pronounce in ordinal form "first" instead of "one"
    Returns:
        (str): The pronounced number
    """
    num = number
    # deal with infinity
    if num == float("inf"):
        return "beskonačnost"
    elif num == float("-inf"):
        return "minus beskonačnost"
    if scientific:
        n, power = scientific_parts(num, places)
        if power != 0:
            return '{}{} puta deset na {}{}'.format(
                'minus ' if float(n) < 0 else '',
                pronounce_number_hr(
                    abs(float(n)), places, short_scale, False, ordinals=False),
                'minus ' if power < 0 else '',
                pronounce_number_hr(abs(power), places, short_scale, False,
                                    ordinals=False))

    number_names = _NUM_STRING_HR.copy()
    number_names.update(_SCALE_HR)

    digits = [number_names[n] for n in range(0, 20)]

    tens = [number_names[n] for n in range(10, 100, 10)]

    hundreds = list(_SCALE_HR.values())

    # deal with negative numbers
    result = ""
    if num < 0:
        result = "minus "
    num = abs(num)

    # check for a direct match
    if num in number_names and not ordinals:
        result += number_names[num]
    else:
        def _sub_thousand(n, ordinals=False):
            assert 0 <= n <= 999
            if n in _SHORT_ORDINAL_HR and ordinals:
                return _SHORT_ORDINAL_HR[n]
            if n in _ORDINAL_HUNDREDS_HR and ordinals:
                return _ORDINAL_HUNDREDS_HR[n]
            if n <= 19:
                return digits[n]
            elif n <= 99:
                q, r = divmod(n, 10)
                return tens[q - 1] + (" " + _sub_thousand(r, ordinals) if r
                                      else "")
            else:
                q, r = divmod(n, 100)
                return _NUM_STRING_HR[q * 100] + \
                    (" " + _sub_thousand(r, ordinals) if r else "")

        def _scale_hr(n):
            if n > max(_SCALE_HR.keys()):
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
                    if i > len(hundreds):
                        return ""
                    scale_word = hundreds[i - 1]
                    if ordi:
                        if i * 1000 in _SHORT_ORDINAL_HR:
                            if z == 1:
                                number = _SHORT_ORDINAL_HR[i * 1000]
                            else:
                                number += " " + _SHORT_ORDINAL_HR[i * 1000]
                        else:
                            number += " " + scale_word + "ti"
                    elif scale_word.endswith("a"):
                        # feminine scale nouns (tisuća, milijarda, ...)
                        if i == 1:
                            # 1000 is spoken "tisuću"
                            one = "tisuću"
                        else:
                            one = scale_word
                        if z == 1:
                            number = one
                        else:
                            # genitive plural: "tisuća" but "milijardi"
                            many = scale_word if i == 1 \
                                else scale_word[:-1] + "i"
                            number = _feminine_hr(number) + " " + plural_hr(
                                z, scale_word, scale_word[:-1] + "e", many)
                    else:
                        # masculine scale nouns (milijun, bilijun, ...)
                        if z == 1:
                            number = scale_word
                        else:
                            number += " " + plural_hr(
                                z, scale_word, scale_word + "a",
                                scale_word + "a")

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

        result += _scale_hr(num)

    # a magnitude with no spoken name reads scientifically
    if result in ("", "minus ") and num >= 1e6:
        return result + pronounce_number_hr(
            num, places, short_scale, scientific=True)
    if num != int(num) and abs(num) < 1.0 \
            and (result == "minus " or not result):
        result += "nula"
    # Deal with fractional part
    if not num == int(num) and places > 0:
        result += " zarez"
        _num_str = f"{Decimal(str(num)):f}"
        _num_str = _num_str.split(".")[1][0:places]
        for char in _num_str:
            result += " " + number_names[int(char)]
    return result


def pronounce_ordinal_hr(number):
    """
    Pronounce a number as a Croatian ordinal.

    Only the last element of a compound numeral takes the ordinal form:
    21st is "dvadeset prvi".

    Args:
        number (int): the number to pronounce
    Returns:
        (str): the ordinal in Croatian
    """
    number = int(number)
    if number <= 0:
        raise ValueError("Croatian ordinals start at 1")
    if number in _SHORT_ORDINAL_HR:
        return _SHORT_ORDINAL_HR[number]
    if number in _ORDINAL_HUNDREDS_HR:
        return _ORDINAL_HUNDREDS_HR[number]
    if number < 100:
        tens = number // 10 * 10
        unit = number % 10
        return f"{_NUM_STRING_HR[tens]} {_SHORT_ORDINAL_HR[unit]}"
    last = number % 100
    if last:
        prefix = number - last
        return f"{pronounce_number_hr(prefix)} {pronounce_ordinal_hr(last)}"
    raise NotImplementedError(f"cannot pronounce {number} as a Croatian ordinal")


def is_fractional_hr(input_str, short_scale=True):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): ignored, Croatian only uses the long scale
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    input_str = input_str.lower()
    # normalize plural forms (dvije trećine -> trećina)
    if input_str.endswith("ine"):
        input_str = input_str[:-1] + "a"

    fractions = {"pola": 2, "pol": 2, "polovica": 2, "polovice": 2}

    for num, name in _FRACTION_STRING_HR.items():
        fractions[name] = num

    if input_str in fractions:
        return 1.0 / fractions[input_str]
    return False


