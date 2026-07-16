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
from ovos_number_parser.util import invert_dict

from ovos_number_parser.numbers_nb import (
    _NorwegianTables, _nice_number, _pronounce_number, _pronounce_ordinal,
    _is_ordinal, _is_fractional, _extract_number, _numbers_to_digits,
    _NUM_STRING_NB, _SCALE_ORDER_NB)

_ARTICLES_NN = {'ein', 'ei', 'eit', 'eitt'}

_NUM_STRING_NN = dict(_NUM_STRING_NB)
_NUM_STRING_NN[1] = 'ein'

_STRING_NUM_NN = invert_dict(_NUM_STRING_NN)
_STRING_NUM_NN.update({
    'ei': 1,
    'eitt': 1,
})

_SCALE_NN = {
    'hundre': 100,
    'tusen': 1000,
    'million': 1000000,
    'millionar': 1000000,
    'milliard': 1000000000,
    'milliardar': 1000000000,
    'billion': 1000000000000,
    'billionar': 1000000000000,
    'billiard': 1000000000000000,
    'billiardar': 1000000000000000,
    'trillion': 1000000000000000000,
    'trillionar': 1000000000000000000,
}

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
}

_STRING_ORDINAL_NN = invert_dict(_ORDINAL_STRING_NN)
_STRING_ORDINAL_NN.update({
    'fyrste': 1,  # equal Nynorsk form of "første"
    'tusende': 1000,
})

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

_STRING_FRACTION_NN = invert_dict(_FRACTION_STRING_NN)
_STRING_FRACTION_NN.update({
    'halvdel': 2,
    'tredel': 3,
    'kvart': 4,
    'firedel': 4,
    'femdel': 5,
    'seksdel': 6,
    'sjudel': 7,
    'åttedel': 8,
    'nidel': 9,
    'tidel': 10,
})

_TABLES_NN = _NorwegianTables(
    num_string=_NUM_STRING_NN,
    string_num=_STRING_NUM_NN,
    scale=_SCALE_NN,
    scale_order=_SCALE_ORDER_NB,
    ordinal_string=_ORDINAL_STRING_NN,
    string_ordinal=_STRING_ORDINAL_NN,
    fraction_string=_FRACTION_STRING_NN,
    string_fraction=_STRING_FRACTION_NN,
    articles=_ARTICLES_NN,
    negatives={'minus'},
    connectors={'og'},
    comma={'komma'},
    fraction_plural_suffix='ar',
    one_word='ein',
    one_neuter_word='eitt',
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
    """Return the value of a Nynorsk ordinal word, or False."""
    return _is_ordinal(input_str, _TABLES_NN)


def is_fractional_nn(input_str, short_scale=False):
    """Return the value of a Nynorsk fraction word, or False."""
    return _is_fractional(input_str, _TABLES_NN)


def extract_number_nn(text, short_scale=False, ordinals=False):
    """Extract a number from Nynorsk text, both counting traditions."""
    return _extract_number(text, _TABLES_NN, ordinals)


def numbers_to_digits_nn(text, short_scale=False, ordinals=False,
                         fractions=True):
    """Replace spoken Nynorsk numbers in a text with digits."""
    return _numbers_to_digits(text, _TABLES_NN, ordinals, fractions)
