"""Slovak number words.

Sources for the writer rules:

* Pravidlá slovenského pravopisu (JÚĽŠ SAV, 3rd ed. 2000): "Dovedna sa píšu
  číslovky v základnom tvare, napr. pätnásť, dvadsaťsedem, stojeden,
  sedemstodvadsať, tisícpäť, sedemtisícdesať." and "Číslovky označujúce
  stovky a tisícky sa píšu spolu, napr. dvesto, sedemsto, tritisíc,
  dvadsaťsedemtisíc, stoosemdesiatdvatisíc. Spolu sa píšu aj radové číslovky
  zložené z jednotiek, stovák a tisícok, napr. stoprvý, dvetisícdruhý.
  Číslovky označujúce milióny, miliardy, bilióny sa píšu oddelene". In an
  ordinal from 21 up the tens and units stay two words ("stodvadsiaty
  štvrtý").
* Jazyková poradňa JÚĽŠ SAV, "dvatisíc, dva tisíc alebo dvetisíc?": "Číslo a
  počet 2 000 sa vyjadruje nesklonnou základnou číslovkou dvetisíc".
  Wiktionary, "dvetisíc": "two thousand".
"""
from decimal import Decimal
from collections import OrderedDict

from ovos_number_parser.util import (invert_dict, convert_to_mixed_fraction, scientific_parts)
from ovos_number_parser import numtag_readers
from ovos_number_parser.util import warn_reader_removed

_NUM_STRING_SK = {
    0: 'nula',
    1: 'jeden',
    2: 'dva',
    3: 'tri',
    4: 'štyri',
    5: 'päť',
    6: 'šesť',
    7: 'sedem',
    8: 'osem',
    9: 'deväť',
    10: 'desať',
    11: 'jedenásť',
    12: 'dvanásť',
    13: 'trinásť',
    14: 'štrnásť',
    15: 'pätnásť',
    16: 'šestnásť',
    17: 'sedemnásť',
    18: 'osemnásť',
    19: 'devätnásť',
    20: 'dvadsať',
    30: 'tridsať',
    40: 'štyridsať',
    50: 'päťdesiat',
    60: 'šesťdesiat',
    70: 'sedemdesiat',
    80: 'osemdesiat',
    90: 'deväťdesiat'
}

# multiples of one hundred are single compound words in Slovak
_HUNDREDS_SK = {
    1: 'sto',
    2: 'dvesto',
    3: 'tristo',
    4: 'štyristo',
    5: 'päťsto',
    6: 'šesťsto',
    7: 'sedemsto',
    8: 'osemsto',
    9: 'deväťsto'
}

_FRACTION_STRING_SK = {
    2: 'polovica',
    3: 'tretina',
    4: 'štvrtina',
    5: 'pätina',
    6: 'šestina',
    7: 'sedmina',
    8: 'osmina',
    9: 'devätina',
    10: 'desatina',
    11: 'jedenástina',
    12: 'dvanástina',
    13: 'trinástina',
    14: 'štrnástina',
    15: 'pätnástina',
    16: 'šestnástina',
    17: 'sedemnástina',
    18: 'osemnástina',
    19: 'devätnástina',
    20: 'dvadsatina',
    30: 'tridsatina',
    40: 'štyridsatina',
    50: 'päťdesiatina',
    60: 'šesťdesiatina',
    70: 'sedemdesiatina',
    80: 'osemdesiatina',
    90: 'deväťdesiatina',
    1e2: 'stotina',
    1e3: 'tisícina'
}

# Slovak uses the long scale (milión, miliarda, bilión, ...)
_SCALE_SK = OrderedDict([
    (100, 'sto'),
    (1000, 'tisíc'),
    (1000000, 'milión'),
    (10 ** 9, 'miliarda'),
    (10 ** 12, 'bilión'),
    (10 ** 15, 'biliarda'),
    (10 ** 18, 'trilión'),
    (10 ** 21, 'triliarda'),
    (10 ** 24, 'kvadrilión')
])

_ORDINAL_BASE_SK = {
    1: 'prvý',
    2: 'druhý',
    3: 'tretí',
    4: 'štvrtý',
    5: 'piaty',
    6: 'šiesty',
    7: 'siedmy',
    8: 'ôsmy',
    9: 'deviaty',
    10: 'desiaty',
    11: 'jedenásty',
    12: 'dvanásty',
    13: 'trinásty',
    14: 'štrnásty',
    15: 'pätnásty',
    16: 'šestnásty',
    17: 'sedemnásty',
    18: 'osemnásty',
    19: 'devätnásty',
    20: 'dvadsiaty',
    30: 'tridsiaty',
    40: 'štyridsiaty',
    50: 'päťdesiaty',
    60: 'šesťdesiaty',
    70: 'sedemdesiaty',
    80: 'osemdesiaty',
    90: 'deväťdesiaty',
    1e2: 'stý',
    1e3: 'tisíci'
}

_ORDINAL_SK = {
    1e6: 'miliónty'
}
_ORDINAL_SK.update(_ORDINAL_BASE_SK)

_ORDINAL_HUNDREDS_SK = {
    200: 'dvojstý', 300: 'trojstý', 400: 'štvorstý', 500: 'päťstý',
    600: 'šesťstý', 700: 'sedemstý', 800: 'osemstý', 900: 'deväťstý',
}


# declined forms of scale words ("dva tisíce", "tri milióny", "päť miliónov")
# and the compound hundreds, all of which multiply the preceding numeral
_SCALE_DECLENSIONS_SK = {
    "tisíce": 1000,
    "milióny": 1000000,
    "miliónov": 1000000,
    "miliardy": 10 ** 9,
    "miliárd": 10 ** 9,
    "bilióny": 10 ** 12,
    "biliónov": 10 ** 12,
    "biliardy": 10 ** 15,
    "biliárd": 10 ** 15,
    "trilióny": 10 ** 18,
    "triliónov": 10 ** 18,
    "triliardy": 10 ** 21,
    "triliárd": 10 ** 21,
    "kvadrilióny": 10 ** 24,
    "kvadriliónov": 10 ** 24,
}
_SCALE_DECLENSIONS_SK.update(
    {word: n * 100 for n, word in _HUNDREDS_SK.items() if n > 1})


_STRING_NUM_SK = invert_dict(_NUM_STRING_SK)
_STRING_NUM_SK.update({
    "jedna": 1,
    "jedno": 1,
    "dve": 2,
    "polovica": 0.5,
    "pol": 0.5,
})


def _scale_declined_sk(word, count):
    """Return the Slovak form of a scale word for a given multiplier."""
    if count == 1:
        return word
    few = 2 <= count <= 4
    if word == "tisíc":
        return "tisíce" if few else "tisíc"
    if word.endswith("ión"):
        return word + ("y" if few else "ov")
    if word.endswith("iarda"):
        return word[:-1] + "y" if few else word[:-4] + "árd"
    return word


def nice_number_sk(number, speech=True, denominators=range(1, 21)):
    """Slovak helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 a polovica" for speech and "4 1/2" for text

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
    den_str = _FRACTION_STRING_SK[den]
    # decline the fraction noun: 1 tretina, 2-4 tretiny, 5+ tretín
    if num > 4:
        if den_str == "polovica":
            den_str = "polovíc"
        elif den_str.endswith("ina"):
            den_str = den_str[:-3] + "ín"
    elif num > 1:
        if den_str == "polovica":
            den_str = "polovice"
        elif den_str.endswith("ina"):
            den_str = den_str[:-1] + "y"
    if whole == 0:
        if num == 1:
            return_string = '{}'.format(den_str)
        else:
            return_string = '{} {}'.format(num, den_str)
    elif num == 1:
        return_string = '{} a {}'.format(whole, den_str)
    else:
        return_string = '{} a {} {}'.format(whole, num, den_str)

    return return_string


def pronounce_number_sk(number, places=2, short_scale=True, scientific=False,
                        ordinals=False):
    """
    Convert a number to its spoken Slovak equivalent

    For example, '5.2' would return 'päť celá dva'

    Word forms follow the Rules of Slovak Orthography (Pravidlá slovenského
    pravopisu, Jazykovedný ústav Ľudovíta Štúra SAV, 3rd ed. 2000): million and
    milliard groups are spoken as separate words, so the output round-trips
    through extract_number_sk.

    Args:
        number(float or int): the number to pronounce
        places(int): maximum decimal places to speak
        short_scale (bool): kept for API compatibility; Slovak uses the
            long scale names regardless
        scientific (bool): pronounce in scientific notation
        ordinals (bool): pronounce in ordinal form "prvý" instead of "jeden"
    Returns:
        (str): The pronounced number
    """
    num = number
    # deal with infinity
    if num == float("inf"):
        return "nekonečno"
    elif num == float("-inf"):
        return "mínus nekonečno"
    if scientific:
        n, power = scientific_parts(num, places)
        if power != 0:
            if ordinals:
                return '{}{} krát desať na {}{} mocninu'.format(
                    'mínus ' if float(n) < 0 else '',
                    pronounce_number_sk(
                        abs(float(n)), places, short_scale, False, ordinals=False),
                    'mínus ' if power < 0 else '',
                    pronounce_number_sk(abs(power), places, short_scale, False, ordinals=True))
            else:
                return '{}{} krát desať na mocninu {}{}'.format(
                    'mínus ' if float(n) < 0 else '',
                    pronounce_number_sk(
                        abs(float(n)), places, short_scale, False),
                    'mínus ' if power < 0 else '',
                    pronounce_number_sk(abs(power), places, short_scale, False))

    number_names = _NUM_STRING_SK.copy()
    number_names.update(_SCALE_SK)

    digits = [number_names[n] for n in range(0, 20)]

    tens = [number_names[n] for n in range(10, 100, 10)]

    hundreds = list(_SCALE_SK.values())

    # deal with negative numbers
    result = ""
    if num < 0:
        result = "mínus "
    num = abs(num)

    # check for a direct match
    if num in number_names and not ordinals:
        result += number_names[num]
    else:
        def _sub_thousand(n, ordinals=False):
            assert 0 <= n <= 999
            if n in _ORDINAL_SK and ordinals:
                return _ORDINAL_SK[n]
            if n <= 19:
                return digits[n]
            elif n <= 99:
                q, r = divmod(n, 10)
                # units join the tens into a single word: dvadsaťjeden
                return tens[q - 1] + (_sub_thousand(r, ordinals) if r
                                      else "")
            else:
                q, r = divmod(n, 100)
                hundred = _HUNDREDS_SK[q]
                # hundreds, tens and units are one word; an ordinal keeps its
                # own word
                joiner = " " if ordinals else ""
                return hundred + (
                    joiner + _sub_thousand(r, ordinals) if r else "")

        def _split_by(n, split=1000):
            assert 0 <= n
            res = []
            while n:
                n, r = divmod(n, split)
                res.append(r)
            return res

        def _whole_number(n):
            if n >= max(_SCALE_SK.keys()) * 1000:
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

                if i == 1 and not ordi:
                    # tisíc is invariable and joins its count: tritisíc,
                    # dvetisíc (2 000), tisíc (1 000)
                    if z == 1:
                        number = "tisíc"
                    else:
                        number = ("dve" if z == 2 else number) + "tisíc"
                elif i:
                    if i >= len(hundreds):
                        return ""
                    number += " "
                    if ordi:
                        if i * 1000 in _ORDINAL_SK:
                            if z == 1:
                                number = _ORDINAL_SK[i * 1000]
                            else:
                                number += _ORDINAL_SK[i * 1000]
                        else:
                            number += hundreds[i] + "ty"
                    else:
                        number += _scale_declined_sk(hundreds[i], z)
                res.append((i, number))
                ordi = False

            # thousands, hundreds, tens and units below a million are one
            # word; million and larger groups stay separate words
            words = []
            for i, number in reversed(res):
                if i == 0 and words and words[-1][0] == 1 and not ordinals:
                    words[-1] = (0, words[-1][1] + number)
                else:
                    words.append((i, number))
            return " ".join(word for _, word in words)

        result += _whole_number(num)

    # a magnitude with no spoken name reads scientifically
    if result in ("", "mínus ") and num >= 1e6:
        return result + pronounce_number_sk(
            num, places, short_scale, scientific=True)
    if num != int(num) and abs(num) < 1.0 \
            and (result == "mínus " or not result):
        result += "nula"
    # Deal with fractional part
    if not num == int(num) and places > 0:
        result += " celá"
        _num_str = f"{Decimal(str(num)):f}"
        _num_str = _num_str.split(".")[1][0:places]
        for char in _num_str:
            result += " " + number_names[int(char)]
    return result


def pronounce_ordinal_sk(number):
    """
    Pronounce a number as a Slovak ordinal.

    Args:
        number (int): the number to pronounce
    Returns:
        (str): the ordinal in Slovak
    """
    number = int(number)
    if number <= 0:
        raise ValueError("Slovak ordinals start at 1")
    if number in _ORDINAL_SK:
        return _ORDINAL_SK[number]
    if number in _ORDINAL_HUNDREDS_SK:
        return _ORDINAL_HUNDREDS_SK[number]
    if number < 100:
        tens = number // 10 * 10
        unit = number % 10
        return f"{_ORDINAL_SK[tens]} {_ORDINAL_SK[unit]}"
    last = number % 100
    if last:
        prefix = number - last
        # thousands, hundreds and the tail are one word (stoprvý,
        # dvetisícdruhý); a million group stays a separate word
        joiner = " " if prefix % 1000000 == 0 else ""
        return pronounce_number_sk(prefix) + joiner + pronounce_ordinal_sk(last)
    raise NotImplementedError(f"cannot pronounce {number} as a Slovak ordinal")


def extract_number_sk(text, short_scale=True, ordinals=False):
    """Deprecated: use ``ovos_number_parser.extract_number(text, "sk")``."""
    warn_reader_removed("extract_number_sk", 'ovos_number_parser.extract_number(text, "sk")')
    return numtag_readers.extract_number(text, "sk", short_scale, ordinals)
