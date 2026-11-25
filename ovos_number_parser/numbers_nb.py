"""Norwegian number parsing and pronunciation.

Covers both written standards of Norwegian:

* Bokmål (``nb``) — tables suffixed ``_NB``
* Nynorsk (``nn``) — implemented in :mod:`ovos_number_parser.numbers_nn`,
  which reuses this engine with its own tables (the two standards share
  all grammar relevant here and differ only in word forms)

Both Norwegian counting traditions are understood when parsing:

* the modern tens-first order introduced by the Storting in 1951
  ("den nye tellemåten"): ``tjueen`` = 21
* the traditional units-first order still common in speech
  ("den gamle tellemåten"): ``enogtyve`` = 21

Pronunciation always uses the modern order and the official modern forms
(``sju``, ``tjue``), per the 1951 counting reform.

Sources:
    - https://snl.no/den_nye_tellem%C3%A5ten (1951 counting reform)
    - https://snl.no/den_gamle_tellem%C3%A5ten (traditional counting)
    - ICU 78.3 spellout-ordinal (CLDR rbnf nb.xml): "én milliard ti millioner
      første", "to milliarder hundre millionte"
    - https://ordbokene.no (Språkrådet/UiB: Bokmålsordboka & Nynorskordboka;
      every pronounced form in this module is an attested entry)
"""
from decimal import Decimal
from math import floor

from ovos_number_parser.util import (convert_to_mixed_fraction, GrammaticalGender, Scale, warn_reader_removed)
from ovos_number_parser import numtag_readers

# indefinite articles are homographs of "one"
#: the numeral 1 before a feminine or neuter noun. Wiktionary "ett" (Norwegian
#: Bokmål, usage notes): the neuter numeral is "ett", and "the corresponding
#: masculine and feminine forms are én and éi"; Wiktionary "ei" gives the
#: unaccented feminine numeral "ei" ("Jeg trenger bare ei bok"). The sources
#: cover the bare 1 only, so a number that ends in 1 keeps "en".
_GENDERED_ONE_NB = {
    GrammaticalGender.FEMININE: "ei",
    GrammaticalGender.NEUTRAL: "ett",
}

_NUM_STRING_NB = {
    0: 'null',
    1: 'en',
    2: 'to',
    3: 'tre',
    4: 'fire',
    5: 'fem',
    6: 'seks',
    7: 'sju',
    8: 'åtte',
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
    20: 'tjue',
    30: 'tretti',
    40: 'førti',
    50: 'femti',
    60: 'seksti',
    70: 'sytti',
    80: 'åtti',
    90: 'nitti',
}

# words accepted when parsing: the pronounced forms above plus official
# variants (Bokmålsordboka: "syv" and "sju" are equal Bokmål forms) and the
# traditional counting words "tyve"/"tredve" documented in
# https://snl.no/den_gamle_tellem%C3%A5ten
# scale words in singular, in ascending order, for pronunciation
_SCALE_ORDER_NB = ['hundre', 'tusen', 'million', 'milliard',
                   'billion', 'billiard', 'trillion']

_ORDINAL_STRING_NB = {
    0: 'nulte',
    1: 'første',
    2: 'andre',
    3: 'tredje',
    4: 'fjerde',
    5: 'femte',
    6: 'sjette',
    7: 'sjuende',
    8: 'åttende',
    9: 'niende',
    10: 'tiende',
    11: 'ellevte',
    12: 'tolvte',
    13: 'trettende',
    14: 'fjortende',
    15: 'femtende',
    16: 'sekstende',
    17: 'syttende',
    18: 'attende',
    19: 'nittende',
    20: 'tjuende',
    30: 'trettiende',
    40: 'førtiende',
    50: 'femtiende',
    60: 'sekstiende',
    70: 'syttiende',
    80: 'åttiende',
    90: 'nittiende',
    100: 'hundrede',
    1000: 'tusende',
    1000000: 'millionte',
    10 ** 9: 'milliardte',
    10 ** 12: 'billionte',
    10 ** 15: 'billiardte',
    10 ** 18: 'trillionte',
}

# variant ordinal forms accepted when parsing (Bokmålsordboka)
_FRACTION_STRING_NB = {
    2: 'halv',
    3: 'tredjedel',
    4: 'fjerdedel',
    5: 'femtedel',
    6: 'sjettedel',
    7: 'sjuendedel',
    8: 'åttendedel',
    9: 'niendedel',
    10: 'tiendedel',
    11: 'ellevtedel',
    12: 'tolvtedel',
    13: 'trettendedel',
    14: 'fjortendedel',
    15: 'femtendedel',
    16: 'sekstendedel',
    17: 'syttendedel',
    18: 'attendedel',
    19: 'nittendedel',
    20: 'tjuendedel',
}

# variant fraction forms accepted when parsing (Bokmålsordboka)
# fraction plural suffix: "to tredjedeler"
_FRACTION_PLURAL_SUFFIX_NB = 'er'

_TABLES_NB = None  # populated at the end of the module


class _NorwegianTables:
    """Bundle of the variant-specific word tables used by the engine."""

    def __init__(self, num_string, scale_order, ordinal_string,
                 fraction_string, fraction_plural_suffix, one_word):
        self.num_string = num_string
        self.scale_order = scale_order
        self.ordinal_string = ordinal_string
        self.fraction_string = fraction_string
        self.fraction_plural_suffix = fraction_plural_suffix
        self.one_word = one_word  # "en" / "ein"


# ---------------------------------------------------------------------------
# pronunciation
# ---------------------------------------------------------------------------

def _pronounce_below_hundred(num, t):
    """21 -> 'tjueen' (modern tens-first order, written as one word)."""
    if num == 1:
        return t.one_word
    if num <= 20:
        return t.num_string[num]
    tens = (num // 10) * 10
    ones = num % 10
    result = t.num_string[tens]
    if ones > 0:
        result += t.num_string[ones] if ones != 1 else t.one_word
    return result


def _pronounce_triplet(num, t):
    """256 -> 'to hundre og femtiseks' (space-separated per Språkrådet)."""
    result = ""
    num = floor(num)
    if num > 99:
        hundreds = num // 100
        if hundreds == 1:
            result += 'hundre'
        else:
            result += t.num_string[hundreds] + ' hundre'
        num -= hundreds * 100
        if num > 0:
            result += ' og '
    if num > 0:
        result += _pronounce_below_hundred(num, t)
    return result


def _pronounce_whole_number(num, t, scale_level=0):
    if num == 0:
        return ''
    num = floor(num)
    result = ''
    last_triplet = num % 1000

    if last_triplet > 0:
        if scale_level == 0:
            result = _pronounce_triplet(last_triplet, t)
        elif scale_level == 1:
            if last_triplet == 1:
                result = 'tusen '
            else:
                result = _pronounce_triplet(last_triplet, t) + ' tusen '
        else:
            scale_word = t.scale_order[scale_level]
            if last_triplet == 1:
                result = t.one_word + ' ' + scale_word + ' '
            else:
                result = _pronounce_triplet(last_triplet, t) + ' ' + \
                    scale_word + t.fraction_plural_suffix + ' '

    higher = _pronounce_whole_number(num // 1000, t, scale_level + 1)
    if higher and scale_level == 0 and last_triplet:
        # "og" before a final part below one hundred: "to tusen og tjuetre"
        if last_triplet < 100:
            result = 'og ' + result
        return higher.rstrip() + ' ' + result
    return higher + result


def _pronounce_number(number, t, places=2):
    result = ""
    if abs(number) >= 1000000000000000000000:  # beyond named scale words
        return str(number)
    if number == 0:
        return t.num_string[0]
    if number < 0:
        return "minus " + _pronounce_number(abs(number), t, places)
    if number == int(number):
        return _pronounce_whole_number(number, t).strip()
    whole_number_part = floor(number)
    result += _pronounce_whole_number(whole_number_part, t).strip() or \
        t.num_string[0]
    if places > 0:
        result += " komma"
        for digit in f"{Decimal(str(number)):f}".split(".")[1][:places].ljust(places, "0"):
            result += " " + t.num_string[int(digit)]
    return result


def _pronounce_ordinal(number, t):
    if number < 0 or number != int(number):
        return str(number)
    number = int(number)
    if number in t.ordinal_string:
        return t.ordinal_string[number]
    if number < 100:
        tens = (number // 10) * 10
        ones = number % 10
        return t.num_string[tens] + t.ordinal_string[ones]
    # 121 -> "hundre og tjueførste": cardinal prefix + ordinal last element
    if number >= 10 ** 21:
        raise NotImplementedError(
            f"cannot pronounce {number} as a Norwegian ordinal")
    if number >= 10 ** 6 and number % 10 ** 6 == 0:
        # the lowest non-zero group of three digits names the ordinal
        # ("to milliarder hundre millionte"); the head stays cardinal
        scale = 10 ** 6
        while number % (scale * 1000) == 0:
            scale *= 1000
        group = number // scale % 1000
        head = number - group * scale
        lead = f"{_pronounce_whole_number(head, t).strip()} " if head else ''
        if group > 1:
            lead += _pronounce_whole_number(group, t).strip() + ' '
        return lead + t.ordinal_string[scale]
    for scale in (10 ** 6, 1000, 100):
        if number >= scale:
            remainder = number % scale
            if remainder == 0:
                prefix = number // scale
                lead = '' if prefix == 1 else \
                    _pronounce_whole_number(prefix, t).strip() + ' '
                return lead + t.ordinal_string[scale]
            head = number - remainder
            return _pronounce_whole_number(head, t).strip() + ' og ' + \
                _pronounce_ordinal(remainder, t)


def _nice_number(number, t, speech=True, denominators=range(1, 21)):
    result = convert_to_mixed_fraction(number, denominators)
    if not result:
        return str(round(number, 3)).replace(".", ",")
    whole, num, den = result
    if not speech:
        if num == 0:
            return str(whole)
        return '{} {}/{}'.format(whole, num, den)
    if num == 0:
        return str(whole)
    den_str = t.fraction_string[den]
    if num > 1:
        den_str += t.fraction_plural_suffix
    if whole == 0:
        return '{} {}'.format(num, den_str)
    return '{} og {} {}'.format(whole, num, den_str)


# ---------------------------------------------------------------------------
# parsing
# ---------------------------------------------------------------------------


_TABLES_NB = _NorwegianTables(
    num_string=_NUM_STRING_NB,
    scale_order=_SCALE_ORDER_NB,
    ordinal_string=_ORDINAL_STRING_NB,
    fraction_string=_FRACTION_STRING_NB,
    fraction_plural_suffix=_FRACTION_PLURAL_SUFFIX_NB,
    one_word='en',
)


# ---------------------------------------------------------------------------
# public Bokmål API
# ---------------------------------------------------------------------------

def nice_number_nb(number, speech=True, denominators=range(1, 21)):
    """Bokmål helper for nice_number: 4.5 -> "4 og 1 halv"."""
    return _nice_number(number, _TABLES_NB, speech, denominators)


def pronounce_number_nb(number, places=2, short_scale=False,
                        scientific=False, ordinals=False,
                        gender=GrammaticalGender.MASCULINE):
    """Convert a number to its spoken Bokmål equivalent.

    Uses the modern tens-first counting order ("tjueen") and the official
    modern forms "sju"/"tjue" (1951 counting reform). The number 1 takes the
    form of ``gender`` ("ei", "ett").
    """
    if ordinals:
        return pronounce_ordinal_nb(number)
    spoken = _pronounce_number(number, _TABLES_NB, places)
    if abs(number) == 1:
        *head, last = spoken.split(" ")
        spoken = " ".join(head + [_GENDERED_ONE_NB.get(gender, last)])
    return spoken


def pronounce_ordinal_nb(number):
    """Pronounce a number as a Bokmål ordinal: 21 -> "tjueførste"."""
    return _pronounce_ordinal(number, _TABLES_NB)


def is_ordinal_nb(input_str):
    """Deprecated: use ``ovos_number_parser.is_ordinal(text, "nb")``."""
    warn_reader_removed("is_ordinal_nb", 'ovos_number_parser.is_ordinal(text, "nb")')
    return numtag_readers.is_ordinal(input_str, "nb")


def numbers_to_digits_nb(text, short_scale=False, ordinals=False, fractions=True):
    """Deprecated: use ``ovos_number_parser.numbers_to_digits(text, "nb")``."""
    warn_reader_removed("numbers_to_digits_nb", 'ovos_number_parser.numbers_to_digits(text, "nb")')
    return numtag_readers.numbers_to_digits(text, "nb", Scale.SHORT if short_scale else Scale.LONG, ordinals)
