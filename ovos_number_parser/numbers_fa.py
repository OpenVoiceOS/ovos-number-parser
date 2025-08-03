import math
from enum import IntEnum

_FRACTION_STRING_FA = {
    2: 'دوم',
    3: 'سوم',
    4: 'چهارم',
    5: 'پنجم',
    6: 'ششم',
    7: 'هفتم',
    8: 'هشتم',
    9: 'نهم',
    10: 'دهم',
    11: 'یازدهم',
    12: 'دوازدهم',
    13: 'سیزدهم',
    14: 'چهاردهم',
    15: 'پونزدهم',
    16: 'شونزدهم',
    17: 'هیفدهم',
    18: 'هیجدهم',
    19: 'نوزدهم',
    20: 'بیستم'
}

_FARSI_ONES = [
    "",
    "یک",
    "دو",
    "سه",
    "چهار",
    "پنج",
    "شش",
    "هفت",
    "هشت",
    "نه",
    "ده",
    "یازده",
    "دوازده",
    "سیزده",
    "چهارده",
    "پونزده",
    "شونزده",
    "هیفده",
    "هیجده",
    "نوزده",
]

_FARSI_TENS = [
    "",
    "ده",
    "بیست",
    "سی",
    "چهل",
    "پنجاه",
    "شصت",
    "هفتاد",
    "هشتاد",
    "نود",
]

_FARSI_HUNDREDS = [
    "",
    "صد",
    "دویست",
    "سیصد",
    "چهارصد",
    "پانصد",
    "ششصد",
    "هفتصد",
    "هشتصد",
    "نهصد",
]

_FARSI_BIG = [
    '',
    'هزار',
    'میلیون',
    "میلیارد",
    'تریلیون',
    "تریلیارد",
]

_FORMAL_VARIANT = {
    'هفده': 'هیفده',
    'هجده': 'هیجده',
    'شانزده': 'شونزده',
    'پانزده': 'پونزده',
}

_FARSI_FRAC = ["", "ده", "صد"]
_FARSI_FRAC_BIG = ["", "هزار", "میلیونی", "میلیاردی"]
_FARSI_SEPERATOR = ' و '


class NumberVariantFA(IntEnum):
    CONVERSATIONAL = 0
    FORMAL = 1


def _is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def _parse_sentence(text):
    for key, value in _FORMAL_VARIANT.items():
        text = text.replace(key, value)
    ar = text.split()
    result = []
    current_number = 0
    current_words = []
    s = 0
    mode = 'init'

    def finish_num():
        nonlocal current_number
        nonlocal s
        nonlocal result
        nonlocal mode
        nonlocal current_words
        current_number += s
        if current_number != 0:
            result.append((current_number, current_words))
        s = 0
        current_number = 0
        current_words = []
        mode = 'init'

    for x in ar:
        if x == "و":
            if mode == 'num_ten' or mode == 'num_hundred' or mode == 'num_one':
                mode += '_va'
                current_words.append(x)
            elif mode == 'num':
                current_words.append(x)
            else:
                finish_num()
                result.append(x)
        elif x == "نیم":
            current_words.append(x)
            current_number += 0.5
            finish_num()
        elif x in _FARSI_ONES:
            t = _FARSI_ONES.index(x)
            if mode != 'init' and mode != 'num_hundred_va' and mode != 'num':
                if not (t < 10 and mode == 'num_ten_va'):
                    finish_num()
            current_words.append(x)
            s += t
            mode = 'num_one'
        elif x in _FARSI_TENS:
            if mode != 'init' and mode != 'num_hundred_va' and mode != 'num':
                finish_num()
            current_words.append(x)
            s += _FARSI_TENS.index(x) * 10
            mode = 'num_ten'
        elif x in _FARSI_HUNDREDS:
            if mode != 'init' and mode != 'num':
                finish_num()
            current_words.append(x)
            s += _FARSI_HUNDREDS.index(x) * 100
            mode = 'num_hundred'
        elif x in _FARSI_BIG:
            current_words.append(x)
            d = _FARSI_BIG.index(x)
            if mode == 'init' and d == 1:
                s = 1
            s *= 10 ** (3 * d)
            current_number += s
            s = 0
            mode = 'num'
        elif _is_number(x):
            current_words.append(x)
            current_number = float(x)
            finish_num()
        else:
            finish_num()
            result.append(x)
    if mode[:3] == 'num':
        finish_num()
    return result


def extract_numbers_fa(text, short_scale=True, ordinals=False):
    """
        Takes in a string and extracts a list of numbers.

    Args:
        text (str): the string to extract a number from
        short_scale (bool): Use "short scale" or "long scale" for large
            numbers -- over a million.  The default is short scale, which
            is now common in most English speaking countries.
            See https://en.wikipedia.org/wiki/Names_of_large_numbers
        ordinals (bool): consider ordinal numbers, e.g. third=3 instead of 1/3
    Returns:
        list: list of extracted numbers as floats
    """

    ar = _parse_sentence(text)
    result = []
    for x in ar:
        if type(x) == tuple:
            result.append(x[0])
    return result


def extract_number_fa(text, ordinals=False):
    """
    Extracts the first number found in a Persian text string.
    
    Parameters:
        text (str): Input text to search for a number.
        ordinals (bool): If True, extracts ordinal numbers as integers (e.g., "third" as 3).
    
    Returns:
        int or float or bool: The first extracted number as int or float, or False if no number is found.
    """
    x = extract_numbers_fa(text, ordinals=ordinals)
    if (len(x) == 0):
        return False
    return x[0]


def _float2tuple(value, _precision):
    """
    Split a float into its integer part, fractional part as an integer, and the effective precision.
    
    Parameters:
        value (float): The number to split.
        _precision (int): The number of decimal places to consider for the fractional part.
    
    Returns:
        tuple: A tuple containing the integer part, the fractional part as an integer, and the adjusted precision after trimming trailing zeros.
    """
    pre = int(value)

    post = abs(value - pre) * 10 ** _precision
    if abs(round(post) - post) < 0.01:
        # We generally floor all values beyond our precision (rather than
        # rounding), but in cases where we have something like 1.239999999,
        # which is probably due to python's handling of floats, we actually
        # want to consider it as 1.24 instead of 1.23
        post = int(round(post))
    else:
        post = int(math.floor(post))

    while post != 0:
        x, y = divmod(post, 10)
        if y != 0:
            break
        post = x
        _precision -= 1

    return pre, post, _precision


def _cardinal3(number):
    if (number < 19):
        return _FARSI_ONES[number]
    if (number < 100):
        x, y = divmod(number, 10)
        if y == 0:
            return _FARSI_TENS[x]
        return _FARSI_TENS[x] + _FARSI_SEPERATOR + _FARSI_ONES[y]
    x, y = divmod(number, 100)
    if y == 0:
        return _FARSI_HUNDREDS[x]
    return _FARSI_HUNDREDS[x] + _FARSI_SEPERATOR + _cardinal3(y)


def _cardinalPos(number):
    x = number
    res = ''
    for b in _FARSI_BIG:
        x, y = divmod(x, 1000)
        if (y == 0):
            continue
        yx = _cardinal3(y)
        if y == 1 and b == 'هزار':
            yx = b
        elif b != '':
            yx += ' ' + b
        if (res == ''):
            res = yx
        else:
            res = yx + _FARSI_SEPERATOR + res
    return res


def _fractional(number, l):
    if (number / 10 ** l == 0.5):
        return "نیم"
    x = _cardinalPos(number)
    ld3, lm3 = divmod(l, 3)
    ltext = (_FARSI_FRAC[lm3] + " " + _FARSI_FRAC_BIG[ld3]).strip() + 'م'
    return x + " " + ltext


def _to_ordinal(number):
    r = _to_cardinal(number, 0)
    if (r[-1] == 'ه' and r[-2] == 'س'):
        return r[:-1] + 'وم'
    return r + 'م'


def _to_ordinal_num(value):
    return str(value) + "م"


def _to_cardinal(number, places):
    if number < 0:
        return "منفی " + _to_cardinal(-number, places)
    if (number == 0):
        return "صفر"
    x, y, l = _float2tuple(number, places)
    if y == 0:
        return _cardinalPos(x)
    if x == 0:
        return _fractional(y, l)
    return _cardinalPos(x) + _FARSI_SEPERATOR + _fractional(y, l)


def pronounce_number_fa(number, places=2, scientific=False,
                        ordinals=False,
                        variant: NumberVariantFA = NumberVariantFA.CONVERSATIONAL):
    """
    Convert a number to it's spoken equivalent

    For example, '5.2' would return 'five point two'

    Args:
        num(float or int): the number to pronounce (under 100)
        places(int): maximum decimal places to speak
        scientific (bool): pronounce in scientific notation
        ordinals (bool): pronounce in ordinal form "first" instead of "one"
    Returns:
        (str): The pronounced number
    """
    num = number
    # deal with infinity
    if num == float("inf"):
        return "بینهایت"
    elif num == float("-inf"):
        return "منفی بینهایت"
    if scientific:
        if number == 0:
            return "صفر"
        number = '%E' % num
        n, power = number.replace("+", "").split("E")
        power = int(power)
        if power != 0:
            return '{}{} ضرب در ده به توان {}{}'.format(
                'منفی ' if float(n) < 0 else '',
                pronounce_number_fa(
                    abs(float(n)), places, False, ordinals=False),
                'منفی ' if power < 0 else '',
                pronounce_number_fa(abs(power), places, False, ordinals=False))
    if ordinals:
        return _to_ordinal(number)
    return _to_cardinal(number, places)
