"""Norwegian Nynorsk number parsing and pronunciation.

Nynorsk shares its number grammar with Bokmål, so this module reuses the
engine in :mod:`ovos_number_parser.numbers_nb` with Nynorsk word tables.

Divergences from Bokmål (all verified against Nynorskordboka via
https://ordbokene.no):

* 1 is ``ein``/``ei``/``eitt`` (Bokmål ``en``/``ei``/``ett``)
* only ``sju`` and ``tjue`` exist (no ``syv``/``tyve`` variants)
* ordinals 7th-20th and the tens use ``-ande`` (``sjuande``, ``attande``,
  ``tjuande``) where Bokmål has ``-ende``
* fraction words follow the ordinals (``sjuandedel``) and pluralize in
  ``-ar`` (``tredjedelar``) where Bokmål has ``-er``
* scale-word plurals use ``-ar``: ``millionar``, ``milliardar``

Only the modern tens-first counting order is pronounced; the traditional
units-first order ("einogtjue") is still accepted when parsing.
"""

from ovos_number_parser.numbers_nb import (
    _NorwegianTables, _nice_number, _pronounce_number, _pronounce_ordinal,
    _NUM_STRING_NB, _SCALE_ORDER_NB)
from ovos_number_parser import numtag_readers
from ovos_number_parser.util import Scale, warn_reader_removed

_NUM_STRING_NN = dict(_NUM_STRING_NB)
_NUM_STRING_NN[1] = 'ein'

_ORDINAL_STRING_NN = {
    0: 'nulte',
    1: 'første',
    2: 'andre',
    3: 'tredje',
    4: 'fjerde',
    5: 'femte',
    6: 'sjette',
    7: 'sjuande',
    8: 'åttande',
    9: 'niande',
    10: 'tiande',
    11: 'ellevte',
    12: 'tolvte',
    13: 'trettande',
    14: 'fjortande',
    15: 'femtande',
    16: 'sekstande',
    17: 'syttande',
    18: 'attande',
    19: 'nittande',
    20: 'tjuande',
    30: 'trettiande',
    40: 'førtiande',
    50: 'femtiande',
    60: 'sekstiande',
    70: 'syttiande',
    80: 'åttiande',
    90: 'nittiande',
    100: 'hundrede',
    1000: 'tusande',
    1000000: 'millionte',
    10 ** 9: 'milliardte',
    10 ** 12: 'billionte',
    10 ** 15: 'billiardte',
    10 ** 18: 'trillionte',
}

_FRACTION_STRING_NN = {
    2: 'halv',
    3: 'tredjedel',
    4: 'fjerdedel',
    5: 'femtedel',
    6: 'sjettedel',
    7: 'sjuandedel',
    8: 'åttandedel',
    9: 'niandedel',
    10: 'tiandedel',
    11: 'ellevtedel',
    12: 'tolvtedel',
    13: 'trettandedel',
    14: 'fjortandedel',
    15: 'femtandedel',
    16: 'sekstandedel',
    17: 'syttandedel',
    18: 'attandedel',
    19: 'nittandedel',
    20: 'tjuandedel',
}

_TABLES_NN = _NorwegianTables(
    num_string=_NUM_STRING_NN,
    scale_order=_SCALE_ORDER_NB,
    ordinal_string=_ORDINAL_STRING_NN,
    fraction_string=_FRACTION_STRING_NN,
    fraction_plural_suffix='ar',
    one_word='ein',
)


def nice_number_nn(number, speech=True, denominators=range(1, 21)):
    """Nynorsk helper for nice_number: 4.5 -> "4 og 1 halv"."""
    return _nice_number(number, _TABLES_NN, speech, denominators)


def pronounce_number_nn(number, places=2, short_scale=False,
                        scientific=False, ordinals=False):
    """Convert a number to its spoken Nynorsk equivalent ("tjueein")."""
    if ordinals:
        return pronounce_ordinal_nn(number)
    return _pronounce_number(number, _TABLES_NN, places)


def pronounce_ordinal_nn(number):
    """Pronounce a number as a Nynorsk ordinal: 21 -> "tjueførste"."""
    return _pronounce_ordinal(number, _TABLES_NN)


def is_ordinal_nn(input_str):
    """Deprecated: use ``ovos_number_parser.is_ordinal(text, "nn")``."""
    warn_reader_removed("is_ordinal_nn", 'ovos_number_parser.is_ordinal(text, "nn")')
    return numtag_readers.is_ordinal(input_str, "nn")


def numbers_to_digits_nn(text, short_scale=False, ordinals=False, fractions=True):
    """Deprecated: use ``ovos_number_parser.numbers_to_digits(text, "nn")``."""
    warn_reader_removed("numbers_to_digits_nn", 'ovos_number_parser.numbers_to_digits(text, "nn")')
    return numtag_readers.numbers_to_digits(text, "nn", Scale.SHORT if short_scale else Scale.LONG, ordinals)
