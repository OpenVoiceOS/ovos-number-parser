from ovos_number_parser.util import (convert_to_mixed_fraction)


NUM_STRING_EU = {
    0: 'zero',
    1: 'bat',
    2: 'bi',
    3: 'hiru',
    4: 'lau',
    5: 'bost',
    6: 'sei',
    7: 'zazpi',
    8: 'zortzi',
    9: 'bederatzi',
    10: 'hamar',
    11: 'hamaika',
    12: 'hamabi',
    13: 'hamahiru',
    14: 'hamalau',
    15: 'hamabost',
    16: 'hamasei',
    17: 'hamazazpi',
    18: 'hemezortzi',
    19: 'hemeretzi',
    20: 'hogei',
    30: 'hogeita hamar',
    40: 'berrogei',
    50: 'berrogeita hamar',
    60: 'hirurogei',
    70: 'hirurogeita hamar',
    80: 'laurogei',
    90: 'laurogeita hamar',
    100: 'ehun',
    200: 'berrehun',
    300: 'hirurehun',
    400: 'laurehun',
    500: 'bostehun',
    600: 'seiehun',
    700: 'zazpiehun',
    800: 'zortziehun',
    900: 'bederatziehun',
    1000: 'mila'
}

FRACTION_STRING_EU = {
    2: 'erdi',
    3: 'heren',
    4: 'laurden',
    5: 'bosten',
    6: 'seiren',
    7: 'zazpiren',
    8: 'zortziren',
    9: 'bederatziren',
    10: 'hamarren',
    11: 'hamaikaren',
    12: 'hamabiren',
    13: 'hamahiruren',
    14: 'hamalauren',
    15: 'hamabosten',
    16: 'hamaseiren',
    17: 'hamazazpiren',
    18: 'hemezortziren',
    19: 'hemeretziren',
    20: 'hogeiren'
}


def nice_number_eu(number, speech=True, denominators=range(1, 21)):
    """ Euskara helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 eta erdi" for speech and "4 1/2" for text

    Args:
        number (int or float): the float to format
        speech (bool): format for speech (True) or display (False)
        denominators (iter of ints): denominators to use, default [1 .. 20]
    Returns:
        (str): The formatted string.
    """
    strNumber = ""
    whole = 0
    num = 0
    den = 0

    result = convert_to_mixed_fraction(number, denominators)

    if not result:
        # Give up, just represent as a 3 decimal number
        whole = round(number, 3)
    else:
        whole, num, den = result

    if not speech:
        if num == 0:
            strNumber = '{:,}'.format(whole)
            strNumber = strNumber.replace(",", " ")
            strNumber = strNumber.replace(".", ",")
            return strNumber
        else:
            return '{} {}/{}'.format(whole, num, den)
    else:
        if num == 0:
            # if the number is not a fraction, nothing to do
            strNumber = str(whole)
            strNumber = strNumber.replace(".", ",")
            return strNumber
        den_str = FRACTION_STRING_EU[den]
        # if it is not an integer
        if whole == 0:
            # if there is no whole number
            if num == 1:
                # if numerator is 1, return "un medio", for example
                strNumber = '{} bat'.format(den_str)
            else:
                # else return "cuatro tercios", for example
                strNumber = '{} {}'.format(num, den_str)
        elif num == 1:
            # if there is a whole number and numerator is 1
            if den == 2:
                # if denominator is 2, return "1 y medio", for example
                strNumber = '{} eta {}'.format(whole, den_str)
            else:
                # else return "1 y 1 tercio", for example
                strNumber = '{} eta {} bat'.format(whole, den_str)
        else:
            # else return "2 y 3 cuarto", for example
            strNumber = '{} eta {} {}'.format(whole, num, den_str)

    return strNumber


# Vigesimal (base-20) cardinal composer.
#
# Basque tens are built on ``hogei`` (20), ``berrogei`` (40 = 2x20),
# ``hirurogei`` (60 = 3x20) and ``laurogei`` (80 = 4x20); 30/50/70/90 are the
# preceding twenty *plus ten* (``hogeita hamar`` = 20-and-10 = 30). The
# copulative ``eta`` ("and") joins groups and contracts to ``-ta`` on the
# twenties (``hogeita hamaika`` = 31). Spelled verbatim / composed from the
# rules in Euskaltzaindia Araua 7 ("Zenbakien idazkeraz", 1994).
_AND_EU = "eta"

_TWENTIES_EU = {1: "hogei", 2: "berrogei", 3: "hirurogei", 4: "laurogei"}


def _under_100_eu(n):
    if n < 20:
        return NUM_STRING_EU[n]
    twenties, rem = divmod(n, 20)
    head = _TWENTIES_EU[twenties]
    if rem == 0:
        return head
    # ``eta`` contracts to ``-ta`` on the twenty head (hogei+eta -> hogeita),
    # but the "ten" stays a separate word (Araua 7: hogeita hamar, never
    # *hogeitamar).
    return f"{head}ta {NUM_STRING_EU[rem]}"


def _under_1000_eu(n):
    if n < 100:
        return _under_100_eu(n)
    hundreds, rem = divmod(n, 100)
    head = NUM_STRING_EU[100] if hundreds == 1 else NUM_STRING_EU[hundreds * 100]
    if rem == 0:
        return head
    return f"{head} {_AND_EU} {_under_100_eu(rem)}"


def _join_rem_eu(rem):
    # Araua 7 ("Oharrak"): ``eta`` links the last two chunks but drops when a
    # lower remainder follows the hundreds -- ``mila eta berrehun`` (1200) vs
    # ``mila berrehun eta bi`` (1202). ``eta`` is inserted only when the
    # remainder is a single terminal chunk (below 100, or a bare hundreds
    # multiple); a remainder carrying its own internal ``eta`` is juxtaposed.
    if rem < 100 or rem % 100 == 0:
        return f"{_AND_EU} {_spell_cardinal_eu(rem)}"
    return _spell_cardinal_eu(rem)


def _spell_cardinal_eu(n):
    """Spell a non-negative integer as a Basque cardinal (vigesimal)."""
    if n == 0:
        return NUM_STRING_EU[0]
    if n < 1000:
        return _under_1000_eu(n)
    # Long scale (Araua 7): milioi 10^6, bilioi 10^12, trilioi 10^18. 10^9 has
    # no distinct word -- it falls out of the milioi branch as a count of one
    # thousand, spelled "mila milioi".
    for divisor, word in ((10 ** 18, "trilioi"), (10 ** 12, "bilioi"),
                          (10 ** 6, "milioi")):
        if n >= divisor:
            count, rem = divmod(n, divisor)
            # "a million" is "milioi bat"; N million is "<N> milioi", where the
            # count is composed recursively so 1000 million reads "mila milioi".
            head = f"{word} {NUM_STRING_EU[1]}" if count == 1 \
                else f"{_spell_cardinal_eu(count)} {word}"
            return head if rem == 0 else f"{head} {_join_rem_eu(rem)}"
    # thousands
    thousands, rem = divmod(n, 1000)
    # 1000 is bare "mila", not "*bat mila"
    head = NUM_STRING_EU[1000] if thousands == 1 \
        else f"{_under_1000_eu(thousands)} {NUM_STRING_EU[1000]}"
    return head if rem == 0 else f"{head} {_join_rem_eu(rem)}"


def pronounce_number_eu(num, places=2):
    """
    Convert a number to its spoken Basque equivalent.

    For example, '5.2' would return 'bost koma bi'. Integers are composed with
    the vigesimal ``eta`` rule of Euskaltzaindia Araua 7 ("Zenbakien
    idazkeraz", 1994), which defines Basque as a long-scale system: ``milioi``
    is 10^6, ``bilioi`` is 10^12 and ``trilioi`` is 10^18, while 10^9 has no
    distinct word and is spoken ``mila milioi`` (thousand-million). The
    fractional part is read digit by digit after ``koma``; magnitudes small
    enough to round away at ``places`` decimals and integer-valued floats
    (including scientific-notation values) are rendered without the koma tail.

    Args:
        num(float or int): the number to pronounce
        places(int): maximum decimal places to speak
    Returns:
        (str): The pronounced number
    """
    result = ""
    if num < 0:
        result = "minus "
    num = abs(num)

    whole = int(num)
    result += _spell_cardinal_eu(whole)

    # Deal with decimal part; in Basque the comma is commonly used instead of
    # the dot, and when pronounced it is read as "koma".
    if not num == int(num) and places > 0:
        # Fixed-point formatting avoids scientific notation (e.g. ``1e-09``),
        # which has no fractional part to split and would otherwise crash;
        # trailing zeros left by rounding are dropped so tiny magnitudes that
        # round to the whole part carry no empty ``koma`` tail.
        _num_str = f"{num:.{places}f}".split(".")[1].rstrip("0")
        if _num_str:
            result += " koma"
            for char in _num_str:
                result += " " + NUM_STRING_EU[int(char)]

    return result


# Ordinals: the suffix is ``-garren``; 1st is suppletive (``lehenengo`` /
# ``lehen``) and ``bost`` drops its ``t`` before the suffix (``bosgarren``, not
# *bostgarren). Spelled / ruled in Euskaltzaindia Araua 18 ("Ordinalen eta
# banatzaileen idazkera", 1994).
_ORDINAL_SUFFIX_EU = "garren"

ORDINAL_BASE_EU = {
    1: "lehenengo",
    2: "bigarren",
    3: "hirugarren",
    4: "laugarren",
    5: "bosgarren",
    6: "seigarren",
    7: "zazpigarren",
    8: "zortzigarren",
    9: "bederatzigarren",
    10: "hamargarren",
}


def _ordinalize_word_eu(word):
    if word.endswith("bost"):
        word = word[:-1]  # bost -> bos (bosgarren)
    return f"{word}{_ORDINAL_SUFFIX_EU}"


def pronounce_ordinal_eu(num):
    """
    Convert an integer to its spoken Basque ordinal (``-garren``).

    1-10 use the attested table (1st suppletive ``lehenengo``). Above ten the
    suffix attaches to the cardinal's final element, with the euphonic
    ``bost`` -> ``bos`` drop (``hamabost`` -> ``hamabosgarren``).

    Raises:
        ValueError: for negative numbers, which have no ordinal form.
    """
    num = int(num)
    if num < 0:
        raise ValueError(f"Basque ordinals are not defined for {num}")
    if num in ORDINAL_BASE_EU:
        return ORDINAL_BASE_EU[num]
    words = _spell_cardinal_eu(num).split()
    words[-1] = _ordinalize_word_eu(words[-1])
    return " ".join(words)


