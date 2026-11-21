from decimal import Decimal
from collections import OrderedDict

from ovos_number_parser.util import (invert_dict, convert_to_mixed_fraction, GrammaticalGender, scientific_parts)
from ovos_number_parser import numtag_readers
from ovos_number_parser.util import warn_reader_removed
from ovos_number_parser.util import Scale

#: the last word of a cardinal that agrees with a feminine or neuter noun
#: (ICU RBNF cs spellout-cardinal-feminine and -neuter). The masculine keeps
#: the counting form "jedna": it is the default gender, so it also serves a
#: caller that names no noun.
_GENDERED_LAST_WORD_CS = {
    GrammaticalGender.FEMININE: {"dva": "dvě"},
    GrammaticalGender.NEUTRAL: {"jedna": "jedno", "dva": "dvě"},
}


_NUM_STRING_CS = {
    0: 'nula',
    1: 'jedna',
    2: 'dva',
    3: 'tři',
    4: 'čtyři',
    5: 'pět',
    6: 'šest',
    7: 'sedm',
    8: 'osm',
    9: 'devět',
    10: 'deset',
    11: 'jedenáct',
    12: 'dvanáct',
    13: 'třináct',
    14: 'čtrnáct',
    15: 'patnáct',
    16: 'šestnáct',
    17: 'sedmnáct',
    18: 'osmnáct',
    19: 'devatenáct',
    20: 'dvacet',
    30: 'třicet',
    40: 'čtyřicet',
    50: 'padesát',
    60: 'šedesát',
    70: 'sedmdesát',
    80: 'osmdesát',
    90: 'devadesát'
}

_FRACTION_STRING_CS = {
    2: 'polovina',
    3: 'třetina',
    4: 'čtvrtina',
    5: 'pětina',
    6: 'šestina',
    7: 'sedmina',
    8: 'osmina',
    9: 'devítina',
    10: 'desetina',
    11: 'jedenáctina',
    12: 'dvanáctina',
    13: 'třináctina',
    14: 'čtrnáctina',
    15: 'patnáctina',
    16: 'šestnáctina',
    17: 'sedmnáctina',
    18: 'osmnáctina',
    19: 'devatenáctina',
    20: 'dvacetina',
    30: 'třicetina',
    40: 'čtyřicetina',
    50: 'padesátina',
    60: 'šedesátina',
    70: 'sedmdesátina',
    80: 'osmdesátina',
    90: 'devadesátina',
    1e2: 'setina',
    1e3: 'tisícina'
}

_LONG_SCALE_CS = OrderedDict([
    (100, 'sto'),
    (1000, 'tisíc'),
    (10 ** 6, 'milion'),
    (10 ** 9, "miliarda"),
    (10 ** 12, "bilion"),
    (10 ** 15, "biliarda"),
    (10 ** 18, "trilion"),
    (10 ** 21, "triliarda"),
    (10 ** 24, "kvadrilion"),
    (10 ** 27, "kvadriliarda"),
    (10 ** 30, "kvintilion"),
    (10 ** 33, "kvintiliarda"),
    (10 ** 36, "sextilion"),
    (10 ** 39, "sextiliarda"),
    (10 ** 42, "septilion"),
    (10 ** 45, "septiliarda"),
    (10 ** 48, "oktilion"),
    (10 ** 51, "oktiliarda"),
    (10 ** 54, "nonilion"),
    (10 ** 57, "noniliarda"),
    (10 ** 60, "decilion"),
    (10 ** 63, "deciliarda"),
    (10 ** 66, "undecilion"),
    (10 ** 69, "undeciliarda"),
    (10 ** 72, "duodecilion"),
    (10 ** 75, "duodeciliarda"),
    (10 ** 78, "tredecilion"),
    (10 ** 81, "tredeciliarda"),
    (10 ** 84, "kvadrodecilion"),
    (10 ** 87, "kvadrodeciliarda"),
    (10 ** 90, "kvindecilion"),
    (10 ** 93, "kvindeciliarda"),
    (10 ** 96, "sexdecilion"),
    (10 ** 99, "sexdeciliarda"),
    (10 ** 120, "vigintilion"),
    (10 ** 180, "trigintilion"),
    (10 ** 303, "kvingintiliarda"),
    (10 ** 600, "centilion"),
    (10 ** 603, "centiliarda")
])

_SHORT_SCALE_CS = OrderedDict([
    (100, 'sto'),
    (1000, 'tisíc'),
    (1000000, 'million'),
    (1e9, "billion"),
    (1e12, 'trillion'),
    (1e15, "quadrillion"),
    (1e18, "quintillion"),
    (1e21, "sextillion"),
    (1e24, "septillion"),
    (1e27, "octillion"),
    (1e30, "nonillion"),
    (1e33, "decillion"),
    (1e36, "undecillion"),
    (1e39, "duodecillion"),
    (1e42, "tredecillion"),
    (1e45, "quadrdecillion"),
    (1e48, "quindecillion"),
    (1e51, "sexdecillion"),
    (1e54, "septendecillion"),
    (1e57, "octodecillion"),
    (1e60, "novemdecillion"),
    (1e63, "vigintillion"),
    (1e66, "unvigintillion"),
    (1e69, "uuovigintillion"),
    (1e72, "tresvigintillion"),
    (1e75, "quattuorvigintillion"),
    (1e78, "quinquavigintillion"),
    (1e81, "qesvigintillion"),
    (1e84, "septemvigintillion"),
    (1e87, "octovigintillion"),
    (1e90, "novemvigintillion"),
    (1e93, "trigintillion"),
    (1e96, "untrigintillion"),
    (1e99, "duotrigintillion"),
    (1e102, "trestrigintillion"),
    (1e105, "quattuortrigintillion"),
    (1e108, "quinquatrigintillion"),
    (1e111, "sestrigintillion"),
    (1e114, "septentrigintillion"),
    (1e117, "octotrigintillion"),
    (1e120, "noventrigintillion"),
    (1e123, "quadragintillion"),
    (1e153, "quinquagintillion"),
    (1e183, "sexagintillion"),
    (1e213, "septuagintillion"),
    (1e243, "octogintillion"),
    (1e273, "nonagintillion"),
    (1e303, "centillion"),
    (1e306, "uncentillion"),
    (1e309, "duocentillion"),
    (1e312, "trescentillion"),
    (1e333, "decicentillion"),
    (1e336, "undecicentillion"),
    (1e363, "viginticentillion"),
    (1e366, "unviginticentillion"),
    (1e393, "trigintacentillion"),
    (1e423, "quadragintacentillion"),
    (1e453, "quinquagintacentillion"),
    (1e483, "sexagintacentillion"),
    (1e513, "septuagintacentillion"),
    (1e543, "ctogintacentillion"),
    (1e573, "nonagintacentillion"),
    (1e603, "ducentillion"),
    (1e903, "trecentillion"),
    (1e1203, "quadringentillion"),
    (1e1503, "quingentillion"),
    (1e1803, "sescentillion"),
    (1e2103, "septingentillion"),
    (1e2403, "octingentillion"),
    (1e2703, "nongentillion"),
    (1e3003, "millinillion")
])

_ORDINAL_BASE_CS = {
    1: 'první',
    2: 'druhý',
    3: 'třetí',
    4: 'čtvrtý',
    5: 'pátý',
    6: 'šestý',
    7: 'sedmý',
    8: 'osmý',
    9: 'devátý',
    10: 'desátý',
    11: 'jedenáctý',
    12: 'dvanáctý',
    13: 'třináctý',
    14: 'čtrnáctý',
    15: 'patnáctý',
    16: 'šestnáctý',
    17: 'sedmnáctý',
    18: 'osmnáctý',
    19: 'devatenáctý',
    20: 'dvacátý',
    30: 'třicátý',
    40: "čtyřicátý",
    50: "padesátý",
    60: "šedesátý",
    70: "sedmdesátý",
    80: "osmdesátý",
    90: "devadesátý",
    1e2: "stý",
    1e3: "tisící"
}

_SHORT_ORDINAL_CS = {
    1e6: "miliontý",
    1e9: "billiontý",
    1e12: "trilliontý",
    1e15: "quadrilliontý",
    1e18: "quintilliontý",
    1e21: "sextilliontý",
    1e24: "septilliontý",
    1e27: "oktiliontý",
    1e30: "nonilliontý",
    1e33: "decilliontý"
    # TODO > 1e-33
}
_SHORT_ORDINAL_CS.update(_ORDINAL_BASE_CS)

_LONG_ORDINAL_CS = {
    1e6: "miliontý",
    1e9: "miliardtý",
    1e12: "biliontý",
    1e15: "biliardtý",
    1e18: "triliontý",
    1e21: "triliardtý",
    1e24: "kvadriliontý",
    1e27: "kvadriliardtý",
    1e30: "kvintiliontý",
    1e33: "kvintiliardtý",
    1e36: "sextiliontý",
    1e39: "sextiliardtý",
    1e42: "septiliontý",
    1e45: "septiliardtý",
    1e48: "oktilion",
    1e51: "oktiliardtý",
    1e54: "noniliontý",
    1e57: "noniliardtý",
    1e60: "deciliontý"
    # TODO > 1e60
}
_LONG_ORDINAL_CS.update(_ORDINAL_BASE_CS)


def generate_plurals_cs(originals):
    """
    Return a new set or dict containing the plural form of the original values,

    In English this means all with 's' appended to them.

    Args:
        originals set(str) or dict(str, any): values to pluralize

    Returns:
        set(str) or dict(str, any)

    """
    if isinstance(originals, dict):
        return {key + 'ý': value for key, value in originals.items()}
    return {value + "ý" for value in originals}


_STRING_NUM_CS = invert_dict(_NUM_STRING_CS)
_STRING_NUM_CS.update(generate_plurals_cs(_STRING_NUM_CS))
_STRING_NUM_CS.update({
    "polovina": 0.5,
    "půlka": 0.5,
    "půl": 0.5,
    "jeden": 1,
    "dvojice": 2,
    "dvoje": 2
})


def is_fractional_cs(input_str, short_scale=True):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): use short scale if True, long scale if False
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    if input_str.endswith('iny', -3):  # leading number is bigger than one ( one třetina, two třetiny)
        # Normalize to format of one (třetiny > třetina)
        input_str = input_str[:len(input_str) - 1] + "a"

    fracts = {"celá": 1}  # first four numbers have little different format

    for num in _FRACTION_STRING_CS:  # Numbers from 2 to 1 hundret, more is not usualy used in common speech
        if num > 1:
            fracts[_FRACTION_STRING_CS[num]] = num

    if input_str.lower() in fracts:
        return 1.0 / fracts[input_str.lower()]
    return False


def nice_number_cs(number, speech=True, denominators=range(1, 21)):
    """ English helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 and a half" for speech and "4 1/2" for text

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
            # TODO: Number grouping?  E.g. "1,000,000"
            return str(whole)
        else:
            return '{} {}/{}'.format(whole, num, den)

    if num == 0:
        return str(whole)
    den_str = _FRACTION_STRING_CS[den]
    if whole == 0:
        if num == 1:
            return_string = '{}'.format(den_str)
        else:
            return_string = '{} {}'.format(num, den_str)
    elif num == 1:
        return_string = '{} a {}'.format(whole, den_str)
    else:
        return_string = '{} a {} {}'.format(whole, num, den_str)
    if num > 4:
        return_string = return_string[:-1]
    elif num > 1:
        return_string = return_string[:-1] + 'y'

    return return_string


def pronounce_number_cs(number, places=2, short_scale=True, scientific=False,
                        ordinals=False, gender=GrammaticalGender.MASCULINE):
    """
    Convert a number to it's spoken equivalent

    For example, '5.2' would return 'five point two'

    Word forms follow the Internetová jazyková příručka of the Ústav pro jazyk
    český AV ČR (§791): each numeral group is spoken as separate words, so the
    output round-trips through extract_number_cs.

    Args:
        num(float or int): the number to pronounce (under 100)
        places(int): maximum decimal places to speak
        short_scale (bool) : use short (True) or long scale (False)
            https://en.wikipedia.org/wiki/Names_of_large_numbers
        scientific (bool): pronounce in scientific notation
        ordinals (bool): pronounce in ordinal form "first" instead of "one"
        gender (GrammaticalGender): gender of the noun a cardinal counts
    Returns:
        (str): The pronounced number
    """
    num = number
    # deal with infinity
    if num == float("inf"):
        return "nekonečno"
    elif num == float("-inf"):
        return "záporné nekonečno"
    if scientific:
        n, power = scientific_parts(num, places)
        if power != 0:
            if ordinals:
                # This handles zápornés of powers separately from the normal
                # handling since each call disables the scientific flag
                return '{}{} krát deset k {}{} mocnině'.format(
                    'záporné ' if float(n) < 0 else '',
                    pronounce_number_cs(
                        abs(float(n)), places, short_scale, False, ordinals=False),
                    'záporné ' if power < 0 else '',
                    pronounce_number_cs(abs(power), places, short_scale, False, ordinals=True))
            else:
                # This handles zápornés of powers separately from the normal
                # handling since each call disables the scientific flag
                return '{}{} krát deset na mocninu {}{}'.format(
                    'záporné ' if float(n) < 0 else '',
                    pronounce_number_cs(
                        abs(float(n)), places, short_scale, False),
                    'záporné ' if power < 0 else '',
                    pronounce_number_cs(abs(power), places, short_scale, False))

    if short_scale:
        number_names = _NUM_STRING_CS.copy()
        number_names.update(_SHORT_SCALE_CS)
    else:
        number_names = _NUM_STRING_CS.copy()
        number_names.update(_LONG_SCALE_CS)

    digits = [number_names[n] for n in range(0, 20)]

    tens = [number_names[n] for n in range(10, 100, 10)]

    if short_scale:
        hundreds = [_SHORT_SCALE_CS[n] for n in _SHORT_SCALE_CS.keys()]
    else:
        hundreds = [_LONG_SCALE_CS[n] for n in _LONG_SCALE_CS.keys()]

    # deal with zápornés
    result = ""
    if num < 0:
        result = "záporné " if scientific else "mínus "
    num = abs(num)

    # Czech does not group years into digit pairs the way English does
    # ("nineteen seventy two"); numbers are spoken with full scale words
    # ("tisíc devět set sedmdesát dva"), handled by the routine below.

    # check for a direct match
    if num in number_names and not ordinals:
        result += number_names[num]
    elif ordinals and num == int(num) and \
            (word := _ordinal_cs(int(num), short_scale)):
        result += word
    else:
        def _sub_thousand(n, ordinals=False):
            assert 0 <= n <= 999
            if n in _SHORT_ORDINAL_CS and ordinals:
                return _SHORT_ORDINAL_CS[n]
            if n <= 19:
                return digits[n]
            elif n <= 99:
                q, r = divmod(n, 10)
                return tens[q - 1] + (" " + _sub_thousand(r, ordinals) if r
                                      else "")
            else:
                q, r = divmod(n, 100)
                if q == 1:
                    hundred = "sto"
                elif q == 2:
                    hundred = "dvě stě"
                elif q in (3, 4):
                    hundred = digits[q] + " sta"
                else:
                    hundred = digits[q] + " set"
                return hundred + (
                    " " + _sub_thousand(r, ordinals) if r else "")

        def _short_scale(n):
            if n >= max(_SHORT_SCALE_CS.keys()):
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
                    if i >= len(hundreds):
                        return ""
                    number += " "
                    if ordi:

                        if i * 1000 in _SHORT_ORDINAL_CS:
                            if z == 1:
                                number = _SHORT_ORDINAL_CS[i * 1000]
                            else:
                                number += _SHORT_ORDINAL_CS[i * 1000]
                        else:
                            if n not in _SHORT_SCALE_CS:
                                num = int("1" + "0" * (len(str(n)) - 2))

                                number += _SHORT_SCALE_CS[num] + "tý"
                            else:
                                number = _SHORT_SCALE_CS[n] + "tý"
                    elif i == 1:
                        number = _counted(z, "tisíc")
                    else:
                        number += hundreds[i]
                res.append(number)
                ordi = False

            return ", ".join(reversed(res))

        def _split_by(n, split=1000):
            assert 0 <= n
            res = []
            while n:
                n, r = divmod(n, split)
                res.append(r)
            return res

        def _counted(z, name):
            """``z`` of the scale noun ``name``, in the form the count takes:
            jeden/jedna, then the nominative plural after 2-4 and after a
            compound ending in 2-4, else the genitive plural"""
            feminine = name.endswith("a")
            if z == 1:
                if name == "tisíc":
                    return name
                return ("jedna " if feminine else "jeden ") + name
            count = _sub_thousand(z)
            if z % 10 in (2, 3, 4) and z % 100 // 10 != 1:
                if feminine:
                    *head, last = count.split(" ")
                    count = " ".join(head + [_GENDERED_LAST_WORD_CS[
                        GrammaticalGender.FEMININE].get(last, last)])
                    return count + " " + name[:-1] + "y"
                return count + " " + ("tisíce" if name == "tisíc"
                                      else name + "y")
            if feminine:
                return count + " " + name[:-1]
            return count + " " + (name if name == "tisíc" else name + "ů")

        def _long_scale(n):
            if n >= max(_LONG_SCALE_CS.keys()):
                return ""
            ordi = ordinals and int(n) == n
            n = int(n)
            assert 0 <= n
            res = []
            for i, z in enumerate(_split_by(n, 1000)):
                if not z:
                    continue
                if not i:
                    res.append(_sub_thousand(z))
                    continue
                if ordi:
                    # _ordinal_cs found no ordinal name for this group
                    raise OverflowError(f"no Czech ordinal for {n}")
                name = _LONG_SCALE_CS.get(1000 ** i)
                if name is None:
                    return ""
                res.append(_counted(z, name))
            return ", ".join(reversed(res))

        if short_scale:
            result += _short_scale(num)
        else:
            result += _long_scale(num)

    # a magnitude with no spoken name reads scientifically
    if result in ("", "mínus ") and num >= 1e6:
        # the scientific reading speaks its own sign word
        return pronounce_number_cs(
            -num if result else num, places, short_scale, scientific=True)
    if num != int(num) and abs(num) < 1.0 \
            and (result == "mínus " or not result):
        result += "nula"
    # Deal with fractional part
    if not num == int(num) and places > 0:
        result += " tečka"
        _num_str = f"{Decimal(str(num)):f}"
        _num_str = _num_str.split(".")[1][0:places]
        for char in _num_str:
            result += " " + number_names[int(char)]
    elif not ordinals:
        *head, last = result.split(" ")
        last = _GENDERED_LAST_WORD_CS.get(gender, {}).get(last, last)
        result = " ".join(head + [last])
    else:
        result = " ".join(_ordinal_gender_cs(word, gender)
                          for word in result.split(" "))
    return result


_ORDINAL_HUNDREDS_CS = {
    200: "dvoustý", 300: "třístý", 400: "čtyřstý", 500: "pětistý",
    600: "šestistý", 700: "sedmistý", 800: "osmistý", 900: "devítistý",
}


# Stems that join a count to "-tisící", "-miliontý", written as one word
# (IJP ÚJČ "třítisící", "stotisící"; SSČ "dvou~ v slož.").
_ORDINAL_STEM_UNITS_CS = ["", "jedna", "dvou", "tří", "čtyř", "pěti", "šesti",
                          "sedmi", "osmi", "devíti"]
_ORDINAL_STEM_TEENS_CS = ["deseti", "jedenácti", "dvanácti", "třinácti",
                          "čtrnácti", "patnácti", "šestnácti", "sedmnácti",
                          "osmnácti", "devatenácti"]
_ORDINAL_STEM_TENS_CS = ["", "", "dvaceti", "třiceti", "čtyřiceti", "padesáti",
                         "šedesáti", "sedmdesáti", "osmdesáti", "devadesáti"]
_ORDINAL_STEM_HUNDREDS_CS = ["", "sto", "dvouset", "tříset", "čtyřset",
                             "pětiset", "šestiset", "sedmiset", "osmiset",
                             "devítiset"]


def _ordinal_stem_cs(n):
    hundreds, rest = divmod(n, 100)
    tens, units = divmod(rest, 10)
    if tens == 1:
        return _ORDINAL_STEM_HUNDREDS_CS[hundreds] + _ORDINAL_STEM_TEENS_CS[units]
    return _ORDINAL_STEM_HUNDREDS_CS[hundreds] + _ORDINAL_STEM_TENS_CS[tens] + \
        _ORDINAL_STEM_UNITS_CS[units]


def _ordinal_cs(n, short_scale=True):
    """Masculine ordinal of a whole number. Every part is ordinal (IJP ÚJČ
    "tisící dvoustý padesátý druhý" = 1252., "třítisící dvoustý padesátý
    první" = 3251.). Return None for 0 or when a group has no scale name."""
    if n < 1:
        return None
    ordinals = _SHORT_ORDINAL_CS if short_scale else _LONG_ORDINAL_CS
    words = []
    for scale in reversed(range(len(str(n)) // 3 + 1)):
        group = n // 1000 ** scale % 1000
        if not group:
            continue
        if scale:
            name = ordinals.get(1000 ** scale)
            if name is None:
                return None
            words.append(("" if group == 1 else _ordinal_stem_cs(group)) + name)
            continue
        hundreds, rest = divmod(group, 100)
        if hundreds:
            words.append(_ORDINAL_HUNDREDS_CS.get(group - rest) or
                         _ORDINAL_BASE_CS[100])
        if rest in _ORDINAL_BASE_CS:
            words.append(_ORDINAL_BASE_CS[rest])
        elif rest:
            words += [_ORDINAL_BASE_CS[rest - rest % 10],
                      _ORDINAL_BASE_CS[rest % 10]]
    return " ".join(words)


def _ordinal_gender_cs(word, gender):
    """Inflect a masculine ordinal as an adjective: the hard "druhý" ->
    "druhá", "druhé"; a soft ordinal ("první", "třetí") has one form."""
    if word.endswith("ý"):
        if gender == GrammaticalGender.FEMININE:
            return word[:-1] + "á"
        if gender == GrammaticalGender.NEUTRAL:
            return word[:-1] + "é"
    return word


def pronounce_ordinal_cs(number, gender=GrammaticalGender.MASCULINE,
                         short_scale=False):
    """
    Pronounce a number as a Czech ordinal in the nominative.

    Args:
        number (int): the number to pronounce
        gender (GrammaticalGender): gender of the noun the ordinal agrees with
        short_scale (bool): use the short scale; Czech uses the long scale,
            where 10^9 is "miliarda"
    Returns:
        (str): the ordinal in Czech
    """
    number = int(number)
    if number <= 0:
        raise ValueError("Czech ordinals start at 1")
    return pronounce_number_cs(number, short_scale=short_scale, ordinals=True,
                               gender=gender)


def extract_number_cs(text, short_scale=True, ordinals=False):
    """Deprecated: use ``ovos_number_parser.extract_number(text, "cs")``."""
    warn_reader_removed("extract_number_cs", 'ovos_number_parser.extract_number(text, "cs")')
    return numtag_readers.extract_number(text, "cs", short_scale, ordinals)


def numbers_to_digits_cs(text, short_scale=True, ordinals=False):
    """Deprecated: use ``ovos_number_parser.numbers_to_digits(text, "cs")``."""
    warn_reader_removed("numbers_to_digits_cs", 'ovos_number_parser.numbers_to_digits(text, "cs")')
    return numtag_readers.numbers_to_digits(text, "cs", Scale.SHORT if short_scale else Scale.LONG, ordinals)
