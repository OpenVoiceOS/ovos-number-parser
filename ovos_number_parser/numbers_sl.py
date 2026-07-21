from math import isfinite
from collections import OrderedDict

from ovos_number_parser.util import (convert_to_mixed_fraction)

_NUM_STRING_SL = {
    0: 'nič',
    1: 'ena',
    2: 'dve',
    3: 'tri',
    4: 'štiri',
    5: 'pet',
    6: 'šest',
    7: 'sedem',
    8: 'osem',
    9: 'devet',
    10: 'deset',
    11: 'enajst',
    12: 'dvanajst',
    13: 'trinajst',
    14: 'štirinajst',
    15: 'petnajst',
    16: 'šestnajst',
    17: 'sedemnajst',
    18: 'osemnajst',
    19: 'devetnajst',
    20: 'dvajset',
    30: 'trideset',
    40: 'štirideset',
    50: 'petdeset',
    60: 'šestdeset',
    70: 'sedemdeset',
    80: 'osemdeset',
    90: 'devetdeset'
}

_FRACTION_STRING_SL = {
    2: 'polovica',
    3: 'tretjina',
    4: 'četrtina',
    5: 'petina',
    6: 'šestina',
    7: 'sedmina',
    8: 'osmina',
    9: 'devetina',
    10: 'desetina',
    11: 'enajstina',
    12: 'dvanajstina',
    13: 'trinajstina',
    14: 'štirinajstina',
    15: 'petnajstina',
    16: 'šestnajstina',
    17: 'sedemnajstina',
    18: 'osemnajstina',
    19: 'devetnajstina',
    20: 'dvajsetina'
}

_LONG_SCALE_SL = OrderedDict([
    (100, 'sto'),
    (1000, 'tisoč'),
    (1000000, 'milijon'),
    (1e12, 'bilijon'),
    (1e18, 'trilijon'),
    (1e24, 'kvadrilijon'),
    (1e30, 'kvintilijon'),
    (1e36, 'sekstilijon'),
    (1e42, 'septilijon'),
    (1e48, 'oktilijon'),
    (1e54, 'nonilijon'),
    (1e60, 'decilijon')
    # TODO > 1e63
])

_SHORT_SCALE_SL = OrderedDict([
    (100, 'sto'),
    (1000, 'tisoč'),
    (1000000, 'milijon'),
    (1e9, 'bilijon'),
    (1e12, 'trilijon'),
    (1e15, 'kvadrilijon'),
    (1e18, 'kvintilijon'),
    (1e21, 'sekstilijon'),
    (1e24, 'septilijon'),
    (1e27, 'oktilijon'),
    (1e30, 'nonilijon'),
    (1e33, 'decilijon')
    # TODO > 1e33
])

_ORDINAL_BASE_SL = {
    1: 'prvi',
    2: 'drugi',
    3: 'tretji',
    4: 'četrti',
    5: 'peti',
    6: 'šesti',
    7: 'sedmi',
    8: 'osmi',
    9: 'deveti',
    10: 'deseti',
    11: 'enajsti',
    12: 'dvanajsti',
    13: 'trinajsti',
    14: 'štirinajsti',
    15: 'petnajsti',
    16: 'šestnajsti',
    17: 'sedemnajsti',
    18: 'osemnajsti',
    19: 'devetnajsti',
    20: 'dvajseti',
    30: 'trideseti',
    40: 'štirideseti',
    50: 'petdeseti',
    60: 'šestdeseti',
    70: 'sedemdeseti',
    80: 'osemdeseti',
    90: 'devetdeseti',
    1e2: 'stoti',
    1e3: 'tisoči'
}

_LONG_ORDINAL_SL = {
    1e6: 'milijonti',
    1e12: 'bilijonti',
    1e18: 'trilijonti',
    1e24: 'kvadrilijonti',
    1e30: 'kvintiljonti',
    1e36: 'sekstilijonti',
    1e42: 'septilijonti',
    1e48: 'oktilijonti',
    1e54: 'nonilijonti',
    1e60: 'decilijonti'
    # TODO > 1e60
}
_LONG_ORDINAL_SL.update(_ORDINAL_BASE_SL)

_SHORT_ORDINAL_SL = {
    1e6: 'milijonti',
    1e9: 'bilijonti',
    1e12: 'trilijonti',
    1e15: 'kvadrilijonti',
    1e18: 'kvintiljonti',
    1e21: 'sekstilijonti',
    1e24: 'septilijonti',
    1e27: 'oktilijonti',
    1e30: 'nonilijonti',
    1e33: 'decilijonti'
    # TODO > 1e33
}
_SHORT_ORDINAL_SL.update(_ORDINAL_BASE_SL)


def nice_number_sl(number, speech=True, denominators=None):
    """ Slovenian helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "2 in polovica" for speech and "4 1/2" for text

    Args:
        number (int or float): the float to format
        speech (bool): format for speech (True) or display (False)
        denominators (iter of ints): denominators to use, default [1 .. 20]
    Returns:
        (str): The formatted string.
    """
    if denominators is None:
        denominators = range(1, 21)
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
    den_str = _FRACTION_STRING_SL[den]
    if whole == 0:
        return_string = '{} {}'.format(num, den_str)
    else:
        return_string = '{} in {} {}'.format(whole, num, den_str)

    if num % 100 == 1:
        pass
    elif num % 100 == 2:
        return_string = return_string[:-1] + 'i'
    elif num % 100 == 3 or num % 100 == 4:
        return_string = return_string[:-1] + 'e'
    else:
        return_string = return_string[:-1]

    return return_string


def pronounce_number_sl(num, places=2, short_scale=True, scientific=False,
                        ordinals=False):
    """
    Convert a number to it's spoken equivalent

    For example, '5.2' would return 'pet celih dve'

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
        return "neskončno"
    elif num == float("-inf"):
        return "minus neskončno"
    if scientific:
        number = '%E' % num
        n, power = number.replace("+", "").split("E")
        power = int(power)
        if power != 0:
            if ordinals:
                # This handles negatives of powers separately from the normal
                # handling since each call disables the scientific flag
                return '{}{} krat deset na {}{}'.format(
                    'minus ' if float(n) < 0 else '',
                    pronounce_number_sl(
                        abs(float(n)), places, short_scale, False, ordinals=False),
                    'minus ' if power < 0 else '',
                    pronounce_number_sl(abs(power), places, short_scale, False, ordinals=True))
            else:
                # This handles negatives of powers separately from the normal
                # handling since each call disables the scientific flag
                return '{}{} krat deset na {}{}'.format(
                    'minus ' if float(n) < 0 else '',
                    pronounce_number_sl(
                        abs(float(n)), places, short_scale, False),
                    'minus ' if power < 0 else '',
                    pronounce_number_sl(abs(power), places, short_scale, False))

    if short_scale:
        number_names = _NUM_STRING_SL.copy()
        number_names.update(_SHORT_SCALE_SL)
    else:
        number_names = _NUM_STRING_SL.copy()
        number_names.update(_LONG_SCALE_SL)

    digits = [number_names[n] for n in range(0, 20)]

    tens = [number_names[n] for n in range(10, 100, 10)]

    if short_scale:
        hundreds = [_SHORT_SCALE_SL[n] for n in _SHORT_SCALE_SL.keys()]
    else:
        hundreds = [_LONG_SCALE_SL[n] for n in _LONG_SCALE_SL.keys()]

    # deal with negatives
    result = ""
    if num < 0:
        result = "minus "
    num = abs(num)

    # check for a direct match
    if num in number_names and not ordinals:
        result += number_names[num]
    else:
        def _sub_thousand(n, ordinals=False, is_male=False):
            assert 0 <= n <= 999
            if n in _SHORT_ORDINAL_SL and ordinals:
                return _SHORT_ORDINAL_SL[n]
            if n <= 19:
                if is_male and n == 2:
                    return digits[n][:-1] + "a"
                return digits[n]
            elif n <= 99:
                q, r = divmod(n, 10)
                sub = _sub_thousand(r, False)
                if r == 2:
                    sub = sub[:-1] + "a"
                return ((sub + "in") if r else "") + (
                    tens[q - 1]) + ("i" if ordinals else "")
            else:
                q, r = divmod(n, 100)
                if q == 1:
                    qstr = ""
                else:
                    qstr = digits[q]
                return (qstr + "sto" + (
                    " " + _sub_thousand(r, ordinals) if r else ""))

        def _plural_hundreds(n, hundred, ordi=True):
            if hundred[-3:] != "jon":
                if ordi:
                    return hundred + "i"

                return hundred

            if n < 1000 or short_scale:
                if ordi:
                    return hundred + "ti"

                if n % 100 == 1:
                    return hundred
                elif n % 100 == 2:
                    return hundred + "a"
                elif n % 100 == 3 or n % 100 == 4:
                    return hundred + "i"
                else:
                    return hundred + "ov"
            else:
                n //= 1000

                if ordi:
                    return hundred[:-3] + "jardti"

                if n % 100 == 1:
                    return hundred[:-3] + "jarda"
                elif n % 100 == 2:
                    return hundred[:-3] + "jardi"
                elif n % 100 == 3 or n % 100 == 4:
                    return hundred[:-3] + "jarde"
                else:
                    return hundred[:-3] + "jard"

        def _short_scale(n):
            if n >= max(_SHORT_SCALE_SL.keys()):
                return "neskončno"
            ordi = ordinals

            if int(n) != n:
                ordi = False
            n = int(n)
            assert 0 <= n
            res = []

            split = _split_by(n, 1000)
            if ordinals and len([a for a in split if a > 0]) == 1:
                ordi_force = True
            else:
                ordi_force = False

            for i, z in enumerate(split):
                if not z:
                    continue

                if z == 1 and i == 1:
                    number = ""
                elif z > 100 and z % 100 == 2 and not ordi:
                    number = _sub_thousand(z, not i and ordi, is_male=True)
                elif z > 100 and z % 100 == 3 and not ordi:
                    number = _sub_thousand(z, not i and ordi) + "je"
                elif z > 1 or i == 0 or ordi:
                    number = _sub_thousand(z, not i and ordi)
                else:
                    number = ""

                if i:
                    if i >= len(hundreds):
                        return ""
                    if z > 1:
                        number += " "
                    number += _plural_hundreds(
                        z, hundreds[i], True if ordi_force else not i and ordi)
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

        def _long_scale(n):
            if n >= max(_LONG_SCALE_SL.keys()):
                return "neskončno"
            ordi = ordinals
            if int(n) != n:
                ordi = False
            n = int(n)
            assert 0 <= n
            res = []

            split = _split_by(n, 1000000)
            if ordinals and len([a for a in split if a > 0]) == 1:
                ordi_force = True
            else:
                ordi_force = False

            def _long_numeral(count, masculine, ordi=False):
                # spoken numeral preceding a long-scale word, in the gender the
                # word requires: "-jon" words (milijon) are masculine and take
                # dva/trije, "-jarda" words (milijarda) are feminine and keep
                # dve/tri from the plain cardinal.
                spoken = pronounce_number_sl(count, places, True, scientific,
                                             ordinals=ordi)
                if masculine and not ordi:
                    prefix = spoken.split()[0] + " " if count > 100 else ""
                    if count % 100 == 2:
                        spoken = prefix + digits[2][:-1] + "a"
                    elif count % 100 == 3:
                        spoken = prefix + digits[3] + "je"
                return spoken

            for i, z in enumerate(split):
                if not z:
                    continue

                if i == 0:
                    # units group: a plain sub-million number
                    res.append(pronounce_number_sl(z, places, True, scientific))
                    continue

                if i + 1 >= len(hundreds):
                    return ""

                # a million-group value 0..999999 carries two magnitudes: the
                # "-jarda" tier (z // 1000, e.g. milijarda) and the "-jon" tier
                # (z % 1000, e.g. milijon). Both must be emitted, larger first.
                word = hundreds[i + 1]
                high, low = divmod(z, 1000)
                group = []

                if high:
                    hundred = _plural_hundreds(high * 1000, word, ordi_force)
                    if high == 1:
                        group.append(hundred)
                    else:
                        group.append(
                            _long_numeral(high, masculine=False,
                                          ordi=ordi_force) + " " + hundred)

                if low:
                    hundred = _plural_hundreds(low, word, ordi_force)
                    if low == 1:
                        group.append(hundred)
                    else:
                        group.append(
                            _long_numeral(low, masculine=True) + " " + hundred)

                res.append(" ".join(group))
            return " ".join(reversed(res))

        if short_scale:
            result += _short_scale(num)
        else:
            result += _long_scale(num)

    if ordinals:
        result = result.replace(" ", "")

    # deal with scientific notation unpronounceable as number
    if (not result or result == "neskončno") and "e" in str(num):
        return pronounce_number_sl(num, places, short_scale, scientific=True)
    # Deal with fractional part
    elif not num == int(num) and places > 0:
        if abs(num) < 1.0 and (result == "minus " or not result):
            result += "nič"

        if int(abs(num)) % 100 == 1:
            result += " cela"
        elif int(abs(num)) % 100 == 2:
            result += " celi"
        elif int(abs(num)) % 100 == 3 or int(abs(num)) % 100 == 4:
            result += " cele"
        else:
            result += " celih"

        _num_str = str(num)
        _num_str = _num_str.split(".")[1][0:places]
        for char in _num_str:
            result += " " + number_names[int(char)]
    return result


_MINUS_SL = ("minus",)

_DECIMAL_MARKERS_SL = ("cela", "celi", "cele", "celih")

# unit word → value map, including the allomorphs used inside compounds
_STRING_NUM_SL = {word: val for val, word in _NUM_STRING_SL.items()}
_STRING_NUM_SL["en"] = 1
_STRING_NUM_SL["eno"] = 1
_STRING_NUM_SL["dva"] = 2
_STRING_NUM_SL["trije"] = 3

# scale stems match declined forms too ("milijona", "milijonov", ...)
_SCALE_STEMS_SHORT_SL = {
    'tisoč': 1000,
    'milijon': 1000000,
    'bilijon': 1000000000,
    'trilijon': 1000000000000,
    'kvadrilijon': 1000000000000000,
    'kvintilijon': 1000000000000000000,
}

_SCALE_STEMS_LONG_SL = {
    'tisoč': 1000,
    'milijon': 1000000,
    'milijard': 1000000000,
    'bilijon': 1000000000000,
    'bilijard': 1000000000000000,
    'trilijon': 1000000000000000000,
}

_TENS_WORDS_SL = {word: val for val, word in _NUM_STRING_SL.items()
                  if 20 <= val <= 90 and val % 10 == 0}


def _parse_number_word_sl(word):
    """Parse a single Slovenian number word into its value, or None.

    Handles simple words ("pet"), in-compounds ("enaindvajset" = 21) and
    hundred compounds ("dvesto" = 200, "sto" = 100).
    """
    word = word.lower().strip()
    if not word:
        return None
    if word in _STRING_NUM_SL:
        return _STRING_NUM_SL[word]
    if word == "sto":
        return 100
    # "enaindvajset" → ena + in + dvajset
    for tens_word, tens_val in _TENS_WORDS_SL.items():
        if word.endswith(tens_word):
            prefix = word[:-len(tens_word)]
            if prefix.endswith("in"):
                unit = prefix[:-2]
                if unit in _STRING_NUM_SL and _STRING_NUM_SL[unit] < 10:
                    return tens_val + _STRING_NUM_SL[unit]
    # "dvesto", "tristo", "sto petdeset" (remainder is a separate token)
    if word.endswith("sto"):
        prefix = word[:-3]
        if not prefix:
            return 100
        if prefix in _STRING_NUM_SL and _STRING_NUM_SL[prefix] < 10:
            return _STRING_NUM_SL[prefix] * 100
    return None


def _parse_scale_word_sl(word, short_scale=True):
    """Return the scale value for a (possibly declined) Slovenian scale word."""
    word = word.lower().strip()
    stems = _SCALE_STEMS_SHORT_SL if short_scale else _SCALE_STEMS_LONG_SL
    # "milijarda" is unambiguous and only exists in the long scale
    if word.startswith("milijard") and len(word) - len("milijard") <= 2:
        return 1000000000
    for stem, val in stems.items():
        if word == stem or (word.startswith(stem) and
                            len(word) - len(stem) <= 2):
            return val
    return None


def is_fractional_sl(input_str, short_scale=True):
    """
    Check if the given word is a Slovenian fraction.

    Accepts the inflected forms used after numerals ("dve tretjini",
    "pet tretjin") as well as the base form.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): ignored, present for API compatibility
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction
    """
    word = input_str.lower().strip()
    for den, base in _FRACTION_STRING_SL.items():
        forms = {base, base[:-1], base[:-1] + 'i', base[:-1] + 'e'}
        if word in forms:
            return 1.0 / den
    return False


_ORDINAL_REVERSE_SL = {}


def is_ordinal_sl(input_str):
    """
    Check if the given word is a Slovenian ordinal number.

    Args:
        input_str (str): the string to check if ordinal
    Returns:
        (bool) or (int): False if not an ordinal, otherwise the number
    """
    if not _ORDINAL_REVERSE_SL:
        candidates = list(range(1, 1000)) + [1000, 1000000]
        for n in candidates:
            _ORDINAL_REVERSE_SL[pronounce_number_sl(n, ordinals=True)] = n
    return _ORDINAL_REVERSE_SL.get(input_str.lower().strip(), False)


def extract_number_sl(text, short_scale=True, ordinals=False):
    """
    Extract the first number from Slovenian text.

    Args:
        text (str): the string to extract a number from
        short_scale (bool): use short (True) or long (False) scale
        ordinals (bool): consider ordinal numbers ("drugi" → 2)
    Returns:
        (int, float or False): the extracted number or False if no number
                               was found
    """
    tokens = [t.strip('.,!?;:').lower() for t in text.split()]
    tokens = [t for t in tokens if t]

    for idx, token in enumerate(tokens):
        negative = idx > 0 and tokens[idx - 1] in _MINUS_SL

        # digits, including comma decimals
        cleaned = token.replace(',', '.')
        try:
            val = float(cleaned)
            if isfinite(val):
                if val == int(val) and '.' not in cleaned:
                    val = int(val)
                return -val if negative else val
        except ValueError:
            pass

        if ordinals:
            val = is_ordinal_sl(token)
            if val is not False:
                return -val if negative else val

        if _parse_number_word_sl(token) is None and \
                _parse_scale_word_sl(token, short_scale) is None:
            frac = is_fractional_sl(token)
            if frac:
                return -frac if negative else frac
            continue

        # accumulate a run of number/scale words starting here
        total = 0
        current = 0
        j = idx
        while j < len(tokens):
            tok = tokens[j]
            scale = _parse_scale_word_sl(tok, short_scale)
            if scale is not None:
                total += (current or 1) * scale
                current = 0
                j += 1
                continue
            v = _parse_number_word_sl(tok)
            if v is None:
                try:
                    v = int(tok)
                except ValueError:
                    v = None
            if v is None:
                break
            if v == 100 or (v % 100 == 0 and v < 1000 and current == 0):
                # "sto" after a unit multiplies implicitly only in compounds,
                # standalone "sto"/"dvesto" tokens are additive values
                current += v
            else:
                current += v
            j += 1
        val = total + current

        # decimals: "pet celih dve tri" → 5.23
        if j < len(tokens) and tokens[j] in _DECIMAL_MARKERS_SL:
            digits = ""
            k = j + 1
            while k < len(tokens):
                d = _parse_number_word_sl(tokens[k])
                if d is None or d > 9:
                    break
                digits += str(d)
                k += 1
            if digits:
                val = float(f"{val}.{digits}")

        # fractions: "dve tretjini" → 2/3
        elif j < len(tokens):
            frac = is_fractional_sl(tokens[j])
            if frac:
                val = val * frac

        return -val if negative else val
    return False
