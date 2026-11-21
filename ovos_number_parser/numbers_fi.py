"""Finnish number parsing and pronunciation.

Finnish writes numerals below a million as a single agglutinated word:
21 is "kaksikymmentäyksi" and 345 is "kolmesataaneljäkymmentäviisi".
Inside those compounds the ten, hundred and thousand words appear in the
partitive singular ("kymmentä", "sataa", "tuhatta") whenever the multiplier
is greater than one, while the bare forms "kymmenen", "sata" and "tuhat"
stand alone. "miljoona" and "miljardi" are independent nouns written as
separate words and take the partitive ("kaksi miljoonaa").

References:
    * Kotimaisten kielten keskus (Kotus), Kielitoimiston ohjepankki,
      "Numeraalit" / "Lukusanat"
    * https://fi.wikipedia.org/wiki/Numeraali
    * https://en.wiktionary.org/wiki/Appendix:Finnish_numbers
    * Kotus, Kielitoimiston ohjepankki, "Luvut ja numerot: järjestyslukujen
      taivuttaminen" (every part of a compound ordinal takes the ordinal
      stem); fi.wiktionary "miljardis" ("lukua miljardi vastaava
      järjestysluku"); "biljoonas" follows the same -s derivation
"""
from decimal import Decimal
from math import floor

from ovos_number_parser.util import convert_to_mixed_fraction

_NUM_STRING_FI = {
    0: 'nolla',
    1: 'yksi',
    2: 'kaksi',
    3: 'kolme',
    4: 'neljä',
    5: 'viisi',
    6: 'kuusi',
    7: 'seitsemän',
    8: 'kahdeksan',
    9: 'yhdeksän',
    10: 'kymmenen',
}

# ordinal units; the *_COMPOUND forms are the allomorphs used inside larger
# ordinals (11. "yhdestoista", 12. "kahdestoista")
_ORDINAL_UNITS_FI = {
    1: 'ensimmäinen',
    2: 'toinen',
    3: 'kolmas',
    4: 'neljäs',
    5: 'viides',
    6: 'kuudes',
    7: 'seitsemäs',
    8: 'kahdeksas',
    9: 'yhdeksäs',
    10: 'kymmenes',
}
_ORDINAL_UNITS_COMPOUND_FI = dict(_ORDINAL_UNITS_FI)
_ORDINAL_UNITS_COMPOUND_FI[1] = 'yhdes'
_ORDINAL_UNITS_COMPOUND_FI[2] = 'kahdes'

# fraction denominators: ordinal stem + "osa" is fully productive
# ("kolmasosa"); 3..9 also have the synonymous -nnes nouns ("kolmannes")
_FRACTION_STRING_FI = {
    2: 'puoli',
    3: 'kolmasosa',
    4: 'neljäsosa',
    5: 'viidesosa',
    6: 'kuudesosa',
    7: 'seitsemäsosa',
    8: 'kahdeksasosa',
    9: 'yhdeksäsosa',
    10: 'kymmenesosa',
    11: 'yhdestoistaosa',
    12: 'kahdestoistaosa',
    13: 'kolmastoistaosa',
    14: 'neljästoistaosa',
    15: 'viidestoistaosa',
    16: 'kuudestoistaosa',
    17: 'seitsemästoistaosa',
    18: 'kahdeksastoistaosa',
    19: 'yhdeksästoistaosa',
    20: 'kahdeskymmenesosa',
}

_NNES_FRACTIONS_FI = {
    'kolmannes': 3,
    'neljännes': 4,
    'viidennes': 5,
    'kuudennes': 6,
    'seitsemännes': 7,
    'kahdeksannes': 8,
    'yhdeksännes': 9,
}


def _pronounce_below_1000_fi(num):
    """Pronounce 1..999 as a single compound word."""
    result = ""
    hundreds = num // 100
    if hundreds:
        result += 'sata' if hundreds == 1 else \
            _NUM_STRING_FI[hundreds] + 'sataa'
        num -= hundreds * 100
    if num == 0:
        pass
    elif num <= 10:
        result += _NUM_STRING_FI[num]
    elif num < 20:
        result += _NUM_STRING_FI[num - 10] + 'toista'
    else:
        tens, ones = divmod(num, 10)
        result += _NUM_STRING_FI[tens] + 'kymmentä'
        if ones:
            result += _NUM_STRING_FI[ones]
    return result


def _pronounce_int_fi(num):
    """Pronounce a non-negative integer."""
    if num == 0:
        return _NUM_STRING_FI[0]
    words = []
    for value, name in ((10 ** 12, 'biljoona'), (10 ** 9, 'miljardi'),
                        (10 ** 6, 'miljoona')):
        count = num // value
        if count:
            if count == 1:
                words.append(name)
            else:
                # miljoona/miljardi are separate nouns in the partitive
                words.append(_pronounce_int_fi(count) + ' ' + name + 'a')
            num -= count * value
    compound = ""
    thousands = num // 1000
    if thousands:
        compound += 'tuhat' if thousands == 1 else \
            _pronounce_below_1000_fi(thousands) + 'tuhatta'
        num -= thousands * 1000
    if num:
        compound += _pronounce_below_1000_fi(num)
    if compound:
        words.append(compound)
    return ' '.join(words)


def pronounce_number_fi(number, places=2, short_scale=True, scientific=False,
                        ordinals=False):
    """
    Convert a number to its spoken Finnish equivalent.

    For example, 5.2 becomes "viisi pilkku kaksi". Cardinals are composed by
    the multiplication-based rule of Kotimaisten kielten keskus (Kotus),
    Kielitoimiston ohjepankki, "Luvut ja numerot: peruslukujen taivuttaminen":
    the sub-thousand part is one agglutinated word with the partitive
    allomorphs "sataa"/"tuhatta" when the multiplier exceeds one, while
    miljoona/miljardi are separate nouns in the partitive ("kaksi miljoonaa").

    Finnish uses the long scale (Wikipedia, "Long and short scales",
    https://en.wikipedia.org/wiki/Long_and_short_scales): the milliard-cognate
    "miljardi" names 10^9 and the billion-cognate "biljoona" names 10^12.

    Args:
        number(float or int): the number to pronounce
        places(int): maximum decimal places to speak
        short_scale (bool): ignored, Finnish uses its own scale words
        scientific (bool): ignored
        ordinals (bool): pronounce as an ordinal ("ensimmäinen")
    Returns:
        (str): The pronounced number
    """
    if ordinals and number == int(number) and number >= 0:
        return pronounce_ordinal_fi(number)
    if abs(number) >= 10 ** 15:  # beyond the supported scale words
        return f"{Decimal(str(number)):f}".removesuffix(".0")
    if number < 0:
        return "miinus " + pronounce_number_fi(abs(number), places,
                                                ordinals=ordinals)
    if number == int(number):
        return _pronounce_int_fi(int(number))
    result = _pronounce_int_fi(floor(number))
    if places > 0:
        # decimals are read digit by digit after "pilkku"
        fraction = f"{Decimal(str(round(number - floor(number), places))):f}"[2:]
        digits = [_NUM_STRING_FI[int(d)] for d in fraction[:places]]
        result += " pilkku " + " ".join(digits)
    return result


# round scale ordinals, largest first
_ORDINAL_SCALES_FI = ((10 ** 12, 'biljoonas'), (10 ** 9, 'miljardis'),
                      (10 ** 6, 'miljoonas'), (1000, 'tuhannes'))


def _ordinal_multiplier_fi(number):
    """Ordinal stem of a scale-word multiplier (before "tuhannes"/"miljoonas").

    A bare multiplier takes the compositive ordinal stem rather than the
    standalone form: 2000th is "kahdestuhannes", not "toinentuhannes". Kotus,
    Kielitoimiston ohjepankki, "järjestyslukujen taivuttaminen", gives the
    compound base "kahdeskymmenesyhdes" (21st), showing the compositive stems
    "yhdes"/"kahdes" carry through compounds instead of "ensimmäinen"/"toinen".
    """
    if number in _ORDINAL_UNITS_COMPOUND_FI and number < 10:
        return _ORDINAL_UNITS_COMPOUND_FI[number]
    return pronounce_ordinal_fi(number)


def pronounce_ordinal_fi(number):
    """
    Pronounce a number as a Finnish ordinal.

    1 -> "ensimmäinen", 2 -> "toinen", 21 -> "kahdeskymmenesensimmäinen",
    2000 -> "kahdestuhannes", 2000000 -> "kahdesmiljoonas"

    Compound ordinals mark every inflectable part with the compositive ordinal
    stem (Kotus, Kielitoimiston ohjepankki, "järjestyslukujen taivuttaminen").

    Args:
        number (int): the number to format
    Returns:
        (str): The pronounced ordinal string.
    """
    # only for whole positive numbers including zero
    if number < 0 or number != int(number):
        return number
    number = int(number)
    if number == 0:
        return 'nollas'
    if number in _ORDINAL_UNITS_FI:
        return _ORDINAL_UNITS_FI[number]
    if number < 20:
        return _ORDINAL_UNITS_COMPOUND_FI[number - 10] + 'toista'
    if number < 100:
        tens, ones = divmod(number, 10)
        result = _ORDINAL_UNITS_COMPOUND_FI[tens] + 'kymmenes'
        if ones:
            result += _ORDINAL_UNITS_FI[ones]
        return result
    if number < 1000 and number % 100 == 0:
        hundreds = number // 100
        return 'sadas' if hundreds == 1 else \
            _ORDINAL_UNITS_COMPOUND_FI[hundreds] + 'sadas'
    if number >= 10 ** 15:
        raise NotImplementedError(
            f"cannot pronounce {number} as a Finnish ordinal")
    for base, word in _ORDINAL_SCALES_FI:
        count, rest = divmod(number, base)
        if not rest and count < 1000:
            return word if count == 1 else \
                _ordinal_multiplier_fi(count) + word
    # compose: ordinal prefix from the largest round part + remainder.
    for base in (10 ** 12, 10 ** 9, 10 ** 6, 1000, 100):
        if number > base:
            head = (number // base) * base
            return pronounce_ordinal_fi(head) + \
                pronounce_ordinal_fi(number - head)


def nice_number_fi(number, speech=True, denominators=range(1, 21)):
    """Finnish helper for nice_number

    This function formats a float to a human understandable string. Like
    4.5 becomes "4 ja puoli" for speech and "4 1/2" for text

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
        return '{} {}/{}'.format(whole, num, den)

    if num == 0:
        return str(whole)
    den_str = _FRACTION_STRING_FI[den]
    if num > 1:
        # numerals govern the partitive: "kolme neljäsosaa"
        den_str = 'puolta' if den == 2 else den_str + 'a'
        frac = '{} {}'.format(pronounce_number_fi(num), den_str)
    else:
        frac = den_str
    if whole == 0:
        return frac
    return '{} ja {}'.format(whole, frac)


_ORDINAL_REVERSE_FI = {}


def is_ordinal_fi(input_str):
    """
    Check if the given word is a Finnish ordinal number.

    Args:
        input_str (str): the string to check if ordinal
    Returns:
        (bool) or (int): False if not an ordinal, otherwise the number
    """
    if not _ORDINAL_REVERSE_FI:
        candidates = list(range(0, 101)) + \
            [n * 100 for n in range(1, 11)] + [1000, 10 ** 6]
        for n in candidates:
            _ORDINAL_REVERSE_FI[pronounce_ordinal_fi(n)] = n
    return _ORDINAL_REVERSE_FI.get(input_str.lower().strip(), False)


def is_fractional_fi(input_str, short_scale=True):
    """
    Check if the given word is a Finnish fraction.

    Accepts both the productive ordinal + "osa" pattern ("kolmasosa") and
    the -nnes nouns ("kolmannes", "neljännes"), plus the partitive forms
    that follow numerals ("kolme neljäsosaa").

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): ignored, present for API compatibility
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction
    """
    word = input_str.lower().strip()
    if word in ('puoli', 'puolta'):
        return 0.5
    for den, den_str in _FRACTION_STRING_FI.items():
        if word in (den_str, den_str + 'a'):
            return 1.0 / den
    if word in _NNES_FRACTIONS_FI:
        return 1.0 / _NNES_FRACTIONS_FI[word]
    return False


