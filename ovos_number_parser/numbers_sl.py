from collections import OrderedDict

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



def pronounce_number_sl(num, places=2, short_scale=True, scientific=False,
                        ordinals=False):
    """
                        Convert a number to its spoken Slovenian equivalent.
                        
                        Supports pronunciation of integers, decimals, large numbers (using short or long scale), scientific notation, and ordinal forms. Handles special cases such as infinity and negative numbers, and applies Slovenian grammatical rules for number words and fractions.
                        
                        Parameters:
                            num (float or int): The number to pronounce.
                            places (int, optional): Maximum number of decimal places to pronounce (default is 2).
                            short_scale (bool, optional): If True, use short scale for large numbers; if False, use long scale.
                            scientific (bool, optional): If True, pronounce the number in scientific notation.
                            ordinals (bool, optional): If True, pronounce the number as an ordinal (e.g., "first" instead of "one").
                        
                        Returns:
                            str: The Slovenian spoken form of the number.
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
                elif z > 100 and z % 100 == 2:
                    number = _sub_thousand(z, not i and ordi, is_male=True)
                elif z > 100 and z % 100 == 3:
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

            for i, z in enumerate(split):
                if not z:
                    continue

                number = pronounce_number_sl(z, places, True, scientific)
                if z > 100:
                    add = number.split()[0] + " "
                else:
                    add = ""
                if z % 100 == 2 and i >= 1:
                    number = add + digits[2][:-1] + "a"
                if z % 100 == 3 and i >= 1:
                    number = add + digits[3] + "je"

                # strip off the comma after the thousand
                if i:
                    if i >= len(hundreds):
                        return ""
                    # plus one as we skip 'thousand'
                    # (and 'hundred', but this is excluded by index value)
                    hundred = _plural_hundreds(
                        z, hundreds[i + 1], True if ordi_force else ordi and not i)

                    if z >= 1000:
                        z //= 1000
                        number = pronounce_number_sl(z, places, True, scientific,
                                                     ordinals=True if ordi_force else ordi and not i)

                    if z == 1:
                        number = hundred
                    else:
                        number += " " + hundred
                res.append(number)
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
