"""Danish number words.

Sources for the writer rules:

* Dansk Sprognævn, svarbase SV00017853 (sproget.dk): "Man vil altså udtale
  tallene: et hundrede og en, et tusinde og en, en million og en." A final
  group below 100 follows a hundred, thousand or million after "og", and a
  final 1 is the counting form "en"; "et" is for a neuter noun
  ("101 gram udtales et hundrede og et gram"). Wiktionary, Appendix:Danish
  numerals: "tre tusinde to hundrede og fireoghalvtreds" (3254).
* Den Danske Ordbog, "tusinde" and "tusind": "tusinde 1 eller tusind talord
  (mængdetal)". The writer keeps "tusind" for 1000 and "tusinde" after a
  count ("to tusinde"). The same entries list "hundrede" and "tusinde" as the
  ordinals of 100 and 1000, and "millionte", "milliardte" and "billionte"
  are ordinals, so a larger scale word takes -te.
* Politikens sprogklumme on sproget.dk, "Den 101. dalmatiner møder den 101.
  stryger": the ordinal of 100 is "hundrede"; "hundred(e) (og) syttende"
  shows that "og" before the last ordinal is optional.
* Dansk Sprognævn, svarbase SV00000084: "fyrrende, halvtredsende, tressende,
  halvfjerdsende, firsende og halvfemsende" are correct next to the long
  forms on -indstyvende. The writer uses the short series for 40 to 90, so
  the 60th is "tressende" (da.wikipedia, "Talord", gives the long forms as
  frequent in ordinals).
"""
import re
from decimal import Decimal
from math import floor

from ovos_number_parser.util import (invert_dict, convert_to_mixed_fraction, GrammaticalGender, Scale, warn_reader_removed)
from ovos_number_parser import numtag_readers

#: the last word of a whole number before a common-gender (FEMININE) or neuter
#: noun (ICU RBNF da spellout-cardinal-common and -neuter: "hundrede og en",
#: "hundrede og et"). The masculine is the default gender and keeps its output.
_GENDERED_LAST_WORD_DA = {
    GrammaticalGender.FEMININE: {"et": "en"},
    GrammaticalGender.NEUTRAL: {"en": "et"},
}


_MONTHS_DA = ['januar', 'februar', 'marts', 'april', 'maj', 'juni',
              'juli', 'august', 'september', 'oktober', 'november',
              'december']

_NUM_STRING_DA = {
    0: 'nul',
    1: 'en',
    2: 'to',
    3: 'tre',
    4: 'fire',
    5: 'fem',
    6: 'seks',
    7: 'syv',
    8: 'otte',
    9: 'ni',
    10: 'ti',
    11: 'elleve',
    12: 'tolv',
    13: 'tretten',
    14: 'fjorten',
    15: 'femten',
    16: 'seksten',
    17: 'sytten',
    18: 'atten',
    19: 'nitten',
    20: 'tyve',
    30: 'tredive',
    40: 'fyrre',
    50: 'halvtreds',
    60: 'tres',
    70: 'halvfjerds',
    80: 'firs',
    90: 'halvfems',
    100: 'hundrede',
    200: 'tohundrede',
    300: 'trehundrede',
    400: 'firehundrede',
    500: 'femhundrede',
    600: 'sekshundrede',
    700: 'syvhundrede',
    800: 'ottehundrede',
    900: 'nihundrede',
    1000: 'tusinde',
    1000000: 'million'
}

_NUM_POWERS_OF_TEN = [
    'hundred',
    'tusind',
    'million',
    'milliard',
    'billion',
    'billiard',
    'trillion',
    'trilliard'
]

_FRACTION_STRING_DA = {
    2: 'halv',
    3: 'trediedel',
    4: 'fjerdedel',
    5: 'femtedel',
    6: 'sjettedel',
    7: 'syvendedel',
    8: 'ottendedel',
    9: 'niendedel',
    10: 'tiendedel',
    11: 'elftedel',
    12: 'tolvtedel',
    13: 'trettendedel',
    14: 'fjortendedel',
    15: 'femtendedel',
    16: 'sejstendedel',
    17: 'syttendedel',
    18: 'attendedel',
    19: 'nittendedel',
    20: 'tyvendedel'
}

_STRING_FRACTION_DA = invert_dict(_FRACTION_STRING_DA)
_STRING_FRACTION_DA.update({
    'halvdel': 2,
    'kvart': 4
})

_LONG_SCALE = {
    100: 'hundrede',
    1000: 'tusinde',
    1000000: 'million',
    10 ** 9: "milliard",
    10 ** 12: 'billion',
    10 ** 15: "billiard",
    10 ** 18: "trillion",
    10 ** 21: "trilliard",
    10 ** 24: "quadrillion",
    10 ** 27: "quadrilliard"
}

_MULTIPLIER = set(_LONG_SCALE.values())

_STRING_LONG_SCALE = invert_dict(_LONG_SCALE)
# "tusind" is the count word for 1000 (Retskrivningsordbogen); "tusinde" also
# occurs. Both must parse, so register the bare form alongside the inverted map.
_STRING_LONG_SCALE['tusind'] = 1000
_MULTIPLIER.add('tusind')

# ending manipulation
for number, item in _LONG_SCALE.items():
    if int(number) > 1000:
        name = item + 'er'
        _MULTIPLIER.add(name)
        _STRING_LONG_SCALE[name] = number

# The vigesimal-derived tens (halvtreds = 50, tres = 60, halvfjerds = 70,
# firs = 80, halvfems = 90) are atoms in their own right; the ones digit is
# spoken first and joined with "og" ("fireogtyve" = 4 og 20 = 24).
_DA_SCALE_VALUES = {'hundrede': 100, 'hunderede': 100,
                    'tusinde': 1000, 'tusind': 1000}
for _scale_number, _scale_word in _LONG_SCALE.items():
    if int(_scale_number) >= 1000000:
        _DA_SCALE_VALUES[_scale_word] = _scale_number
        _DA_SCALE_VALUES[_scale_word + 'er'] = _scale_number


# Numbers below 1 million are written in one word in Danish, yielding very
# long words
# In some circumstances it may better to seperate individual words
# Set _EXTRA_SPACE_DA=" " for separating numbers below 1 million (
# orthographically incorrect)
# Set _EXTRA_SPACE_DA="" for correct spelling, this is standard

# _EXTRA_SPACE_DA = " "
_EXTRA_SPACE_DA = ""


def is_ordinal_da(input_str):
    """Deprecated: use ``ovos_number_parser.is_ordinal(text, "da")``."""
    warn_reader_removed("is_ordinal_da", 'ovos_number_parser.is_ordinal(text, "da")')
    return numtag_readers.is_ordinal(input_str, "da")


def nice_number_da(number, speech=True, denominators=range(1, 21)):
    """ Danish helper for nice_number
    This function formats a float to human understandable functions. Like
    4.5 becomes "4 en halv" for speech and "4 1/2" for text
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
            # TODO: Number grouping?  E.g. "1,000,000"
            return str(whole)
        else:
            return '{} {}/{}'.format(whole, num, den)
    if num == 0:
        return str(whole)
    den_str = _FRACTION_STRING_DA[den]
    if whole == 0:
        if num == 1:
            return_string = '{} {}'.format(num, den_str)
        else:
            return_string = '{} {}e'.format(num, den_str)
    else:
        if num == 1:
            return_string = '{} og {} {}'.format(whole, num, den_str)
        else:
            return_string = '{} og {} {}e'.format(whole, num, den_str)

    return return_string


def pronounce_number_da(number, places=2, short_scale=True, scientific=False,
                        ordinals=False, gender=GrammaticalGender.MASCULINE):
    """
    Convert a number to it's spoken equivalent

    For example, '5.2' would return 'five point two'

    Danish writes a whole number below a million as a single spaceless word and
    uses the vigesimal-derived tens prescribed by Dansk Sprognævn, svarbase
    SV00000047 "De danske tal; halvtreds"
    (https://sproget.dk/raad-og-regler/artikler-mv/svarbase/sv00000047/):
    halvtreds (50), tres (60), halvfjerds (70), firs (80), halvfems (90), each a
    shortened -sindstyve ("times twenty") form. The ones digit precedes the tens
    and is joined with "og" ("fireogtyve" = 24).

    Args:
        number(float or int): the number to pronounce (under 100)
        places(int): maximum decimal places to speak
        short_scale (bool) : use short (True) or long scale (False)
            https://en.wikipedia.org/wiki/Names_of_large_numbers
        scientific (bool): pronounce in scientific notation
        ordinals (bool): pronounce in ordinal form "first" instead of "one"
    Returns:
        (str): The pronounced number
    """

    # TODO short_scale, scientific and ordinals
    # currently ignored

    def pronounce_triplet_da(num, one="en"):
        result = ""
        num = floor(num)
        if num > 99:
            hundreds = floor(num / 100)
            if hundreds > 0:
                # 100 is "hundrede", never "et hundrede": Retskrivningsordbogen
                # gives "hundrede" as the correct form (sproget.dk, Politikens
                # sprogklumme "Den 101. dalmatiner moeder den 101. stryger":
                # "en helt fjerde form, hundrede, er den korrekte form ifoelge
                # Retskrivningsordbogen"). Numerals above 100 are also written
                # as separate words -- "talord over 100 [...] deles op i
                # modsaetning til talord under 100" -- so the hundreds group is
                # spaced ("fem tusinde ni hundrede og treoghalvtreds"), while
                # everything below 100 stays a single fused word.
                if hundreds > 1:
                    result += _NUM_STRING_DA[hundreds] + ' '
                result += 'hundrede'
                num -= hundreds * 100
                if num > 0:
                    # "og" links the hundreds to the remainder; the same source
                    # marks it optional ("hundred(e) (og) syttende"), and it is
                    # the conventional written form
                    result += ' og '
        if num == 0:
            result += ''  # do nothing
        elif num == 1:
            result += one
        elif num <= 20:
            result += _NUM_STRING_DA[num] + _EXTRA_SPACE_DA
        elif num > 20:
            ones = num % 10
            tens = num - ones
            if ones > 0:
                result += _NUM_STRING_DA[ones] + _EXTRA_SPACE_DA
                if tens > 0:
                    result += 'og' + _EXTRA_SPACE_DA
            if tens > 0:
                result += _NUM_STRING_DA[tens] + _EXTRA_SPACE_DA

        return result

    def pronounce_fractional_da(num, places):
        # fixed number of places even with trailing zeros
        result = ""
        for digit in f"{Decimal(str(num)):f}".split(".")[1][:places].ljust(places, "0"):
            result += " " + _NUM_STRING_DA[int(digit)]
        return result

    def pronounce_whole_number_da(num, scale_level=0):
        if num == 0:
            return ''

        num = floor(num)
        result = ''
        last_triplet = num % 1000
        if scale_level == 0 and num > 1000 and 0 < last_triplet < 100:
            # "og" links a final group below 100 to the thousands or millions
            # before it ("tusind og en", "to tusind og fireogtyve")
            result += 'og '

        if last_triplet == 1:
            if scale_level == 0:
                result += "en"
            elif scale_level == 1:
                # 1000 is "tusind", not "et tusinde": Retskrivningsordbogen
                # gives "tusind" as the count word (a bare "tusinde" also
                # occurs, but the "et" prefix is not written)
                result += 'tusind '
            else:
                result += "en " + _NUM_POWERS_OF_TEN[scale_level] + ' '
        elif last_triplet > 1:
            # a final 1 is "en" (common gender); before "tusind", a neuter
            # noun, it is "et" ("hundrede og et tusind")
            result += pronounce_triplet_da(
                last_triplet, "et" if scale_level == 1 else "en")
            if scale_level == 1:
                # a space so the thousands stay a separate word from the
                # hundreds below them ("fem tusinde ni hundrede ...")
                result += ' tusinde '
            if scale_level >= 2:
                result += ' ' + _NUM_POWERS_OF_TEN[scale_level]
            if scale_level >= 2:
                result += "er "  # MilliardER, MillioneER

        num //= 1000
        scale_level += 1
        return pronounce_whole_number_da(num,
                                         scale_level) + result + _EXTRA_SPACE_DA

    result = ""
    if abs(number) >= 1000000000000000000000000:  # cannot do more than this
        return str(number)
    elif number == 0:
        return str(_NUM_STRING_DA[0])
    elif number < 0:
        return "minus " + pronounce_number_da(abs(number), places, gender=gender)
    else:
        if number == int(number):
            spoken = re.sub(r'\s+', ' ', pronounce_whole_number_da(number)).strip()
            *head, last = spoken.split(" ")
            last = _GENDERED_LAST_WORD_DA.get(gender, {}).get(last, last)
            return " ".join(head + [last])
        else:
            whole_number_part = floor(number)
            result += pronounce_whole_number_da(whole_number_part) or _NUM_STRING_DA[0]
            if places > 0:
                result += " komma"
                result += pronounce_fractional_da(number, places)
            return re.sub(r'\s+', ' ', result).strip() or _NUM_STRING_DA[0]


def pronounce_ordinal_da(number, gender=GrammaticalGender.MASCULINE):
    """
    This function pronounces a number as an ordinal

    1 -> first
    2 -> second

    Args:
        number (int): the number to format
        gender (GrammaticalGender): NEUTRAL gives the neuter "andet" for 2
            (ICU RBNF da spellout-ordinal-neuter); the other ordinals have
            one form
    Returns:
        (str): The pronounced number string.
    """

    # ordinals 0-19 are irregular (11/12 use a -te suffix on a truncated
    # stem, 13-19 use -de not -ende since the cardinal already ends "-en")
    # this produces the base form, it will have to be adapted for genus,
    # casus, numerus

    # ellevte, tolvte, trettende, fjortende, femtende, sekstende,
    # syttende, attende, nittende

    ordinals = ["nulte", "første", "anden", "tredje", "fjerde", "femte",
                "sjette", "syvende", "ottende", "niende", "tiende",
                "ellevte", "tolvte", "trettende", "fjortende", "femtende",
                "sekstende", "syttende", "attende", "nittende"]

    # only for whole positive numbers including zero
    if number < 0 or number != int(number):
        return number
    number = int(number)
    if number >= 10 ** 24:
        raise NotImplementedError(
            f"cannot pronounce {number} as a Danish ordinal")
    if number < 20:
        if number == 2 and gender == GrammaticalGender.NEUTRAL:
            return "andet"
        return ordinals[number]
    if number >= 100:
        last = number % 100
        if last:
            # the cardinal head is unchanged and "og" links the ordinal of
            # the last group below 100 ("hundrede og første")
            return pronounce_number_da(number - last) + " og " + \
                pronounce_ordinal_da(last, gender)
        # the last word of a round number is a scale word: hundrede and
        # tusinde are the ordinals of 100 and 1000, larger ones take -te
        # ("millionte", "milliardte")
        head, _, scale = pronounce_number_da(number).rpartition(" ")
        if scale in ("tusind", "tusinde"):
            scale = "tusinde"
        elif scale != "hundrede":
            scale = scale.removesuffix("er") + "te"
        return scale if head in ("", "en") else f"{head} {scale}"
    if 30 <= number < 40:
        # tredive -> tredivte, enogtredive -> enogtredivte: drop the
        # trailing unstressed -e and add -te (distinct from the plain
        # +ende suffix used everywhere else)
        return pronounce_number_da(number)[:-1] + "te"
    cardinal = pronounce_number_da(number)
    if cardinal.endswith("tres"):
        # tres + sende, as halvtreds + ende: the short series of
        # Retskrivningsordbogen ("tressende")
        return cardinal + "sende"
    # 20-29 and 40+ both just append the cardinal's usual +nde/+ende
    return cardinal + ("nde" if cardinal[-1:] == 'e' else "ende")


def numbers_to_digits_da(text, short_scale=False, ordinals=False, fractions=True):
    """Deprecated: use ``ovos_number_parser.numbers_to_digits(text, "da")``."""
    warn_reader_removed("numbers_to_digits_da", 'ovos_number_parser.numbers_to_digits(text, "da")')
    return numtag_readers.numbers_to_digits(text, "da", Scale.SHORT if short_scale else Scale.LONG, ordinals)
