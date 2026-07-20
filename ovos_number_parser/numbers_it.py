import collections

import re
from typing import Optional, Union

from ovos_number_parser.util import (convert_to_mixed_fraction, Scale,
                                     GrammaticalGender, NumberVocabulary,
                                     RomanceNumberExtractor)

_SHORT_ORDINAL_STRING_IT = {
    1: 'primo',
    2: 'secondo',
    3: 'terzo',
    4: 'quarto',
    5: 'quinto',
    6: 'sesto',
    7: 'settimo',
    8: 'ottavo',
    9: 'nono',
    10: 'decimo',
    11: 'undicesimo',
    12: 'dodicesimo',
    13: 'tredicesimo',
    14: 'quattordicesimo',
    15: 'quindicesimo',
    16: 'sedicesimo',
    17: 'diciassettesimo',
    18: 'diciottesimo',
    19: 'diciannovesimo',
    20: 'ventesimo',
    30: 'trentesimo',
    40: 'quarantesimo',
    50: 'cinquantesimo',
    60: 'sessantesimo',
    70: 'settantesimo',
    80: 'ottantesimo',
    90: 'novantesimo',
    1e2: 'centesimo',
    1e3: 'millesimo',
    1e6: 'milionesimo',
    1e9: 'miliardesimo',
    1e12: 'trilionesimo',
    1e15: 'quadrilionesimo',
    1e18: 'quintilionesim',
    1e21: 'sestilionesimo',
    1e24: 'settilionesimo',
    1e27: 'ottilionesimo',
    1e30: 'nonilionesimo',
    1e33: 'decilionesimo'
    # TODO > 1e-33
}

#  per i > 10e12 modificata solo la desinenza: da sistemare a fine debug
_LONG_ORDINAL_STRING_IT = {
    1: 'primo',
    2: 'secondo',
    3: 'terzo',
    4: 'quarto',
    5: 'quinto',
    6: 'sesto',
    7: 'settimo',
    8: 'ottavo',
    9: 'nono',
    10: 'decimo',
    11: 'undicesimo',
    12: 'dodicesimo',
    13: 'tredicesimo',
    14: 'quattordicesimo',
    15: 'quindicesimo',
    16: 'sedicesimo',
    17: 'diciassettesimo',
    18: 'diciottesimo',
    19: 'diciannovesimo',
    20: 'ventesimo',
    30: 'trentesimo',
    40: 'quarantesimo',
    50: 'cinquantesimo',
    60: 'sessantesimo',
    70: 'settantesimo',
    80: 'ottantesimo',
    90: 'novantesimo',
    1e2: 'centesimo',
    1e3: 'millesimo',
    1e6: 'milionesimo',
    1e12: 'bilionesimo',
    1e18: 'trilionesimo',
    1e24: 'quadrilionesimo',
    1e30: 'quintilionesimo',
    1e36: 'sestilionesimo',
    1e42: 'settilionesimo',
    1e48: 'ottilionesimo',
    1e54: 'nonilionesimo',
    1e60: 'decilionesimo'
    # TODO > 1e60
}

# Undefined articles ['un', 'una', 'un\''] can not be supressed,
# in Italian, 'un cavallo' means 'a horse' or 'one horse'.
_ARTICLES_IT = ['il', 'lo', 'la', 'i', 'gli', 'le']

_STRING_NUM_IT = {
    'zero': 0,
    'un': 1,
    'uno': 1,
    'una': 1,
    'un\'': 1,
    'due': 2,
    'tre': 3,
    'quattro': 4,
    'cinque': 5,
    'sei': 6,
    'sette': 7,
    'otto': 8,
    'nove': 9,
    'dieci': 10,
    'undici': 11,
    'dodici': 12,
    'tredici': 13,
    'quattordici': 14,
    'quindici': 15,
    'sedici': 16,
    'diciassette': 17,
    'diciotto': 18,
    'diciannove': 19,
    'venti': 20,
    'vent': 20,
    'trenta': 30,
    'trent': 30,
    'quaranta': 40,
    'quarant': 40,
    'cinquanta': 50,
    'cinquant': 50,
    'sessanta': 60,
    'sessant': 60,
    'settanta': 70,
    'settant': 70,
    'ottanta': 80,
    'ottant': 80,
    'novanta': 90,
    'novant': 90,
    'cento': 100,
    'duecento': 200,
    'trecento': 300,
    'quattrocento': 400,
    'cinquecento': 500,
    'seicento': 600,
    'settecento': 700,
    'ottocento': 800,
    'novecento': 900,
    'mille': 1000,
    'mila': 1000,
    'centomila': 100000,
    'milione': 1000000,
    'miliardo': 1000000000,
    'primo': 1,
    'secondo': 2,
    'mezzo': 0.5,
    'mezza': 0.5,
    'paio': 2,
    'decina': 10,
    'decine': 10,
    'dozzina': 12,
    'dozzine': 12,
    'centinaio': 100,
    'centinaia': 100,
    'migliaio': 1000,
    'migliaia': 1000
}

_NUM_STRING_IT = {
    0: 'zero',
    1: 'uno',
    2: 'due',
    3: 'tre',
    4: 'quattro',
    5: 'cinque',
    6: 'sei',
    7: 'sette',
    8: 'otto',
    9: 'nove',
    10: 'dieci',
    11: 'undici',
    12: 'dodici',
    13: 'tredici',
    14: 'quattordici',
    15: 'quindici',
    16: 'sedici',
    17: 'diciassette',
    18: 'diciotto',
    19: 'diciannove',
    20: 'venti',
    30: 'trenta',
    40: 'quaranta',
    50: 'cinquanta',
    60: 'sessanta',
    70: 'settanta',
    80: 'ottanta',
    90: 'novanta'
}

_FRACTION_STRING_IT = {
    2: 'mezz',
    3: 'terz',
    4: 'quart',
    5: 'quint',
    6: 'sest',
    7: 'settim',
    8: 'ottav',
    9: 'non',
    10: 'decim',
    11: 'undicesim',
    12: 'dodicesim',
    13: 'tredicesim',
    14: 'quattordicesim',
    15: 'quindicesim',
    16: 'sedicesim',
    17: 'diciassettesim',
    18: 'diciottesim',
    19: 'diciannovesim',
    20: 'ventesim'
}

# fonte: http://tulengua.es/numeros-texto/default.aspx
_LONG_SCALE_IT = collections.OrderedDict([
    (100, 'cento'),
    (1000, 'mila'),
    (1000000, 'milioni'),
    (1e9, "miliardi"),
    (1e12, "bilioni"),
    (1e18, 'trilioni'),
    (1e24, "quadrilioni"),
    (1e30, "quintilioni"),
    (1e36, "sestilioni"),
    (1e42, "settilioni"),
    (1e48, "ottillioni"),
    (1e54, "nonillioni"),
    (1e60, "decemillioni"),
    (1e66, "undicilione"),
    (1e72, "dodicilione"),
    (1e78, "tredicilione"),
    (1e84, "quattordicilione"),
    (1e90, "quindicilione"),
    (1e96, "sedicilione"),
    (1e102, "diciasettilione"),
    (1e108, "diciottilione"),
    (1e114, "dicianovilione"),
    (1e120, "vintilione"),
    (1e306, "unquinquagintilione"),
    (1e312, "duoquinquagintilione"),
    (1e336, "sesquinquagintilione"),
    (1e366, "unsexagintilione")
])

#: singular form of the large scale words, used when the count is exactly one
#: ("un milione", "un miliardo"). The scale tables hold the plurals; most go
#: -i -> -e, but miliardi -> miliardo is irregular.
_LONG_SCALE_SINGULAR_IT = {
    'milioni': 'milione',
    'miliardi': 'miliardo',
    'bilioni': 'bilione',
    'triliardi': 'triliardo',
}

_SHORT_SCALE_IT = collections.OrderedDict([
    (100, 'cento'),
    (1000, 'mila'),
    (1000000, 'milioni'),
    (1e9, "miliardi"),
    (1e12, 'bilioni'),
    (1e15, "biliardi"),
    (1e18, "trilioni"),
    (1e21, "triliardi"),
    (1e24, "quadrilioni"),
    (1e27, "quadriliardi"),
    (1e30, "quintilioni"),
    (1e33, "quintiliardi"),
    (1e36, "sestilioni"),
    (1e39, "sestiliardi"),
    (1e42, "settilioni"),
    (1e45, "settiliardi"),
    (1e48, "ottilioni"),
    (1e51, "ottiliardi"),
    (1e54, "nonilioni"),
    (1e57, "noniliardi"),
    (1e60, "decilioni"),
    (1e63, "deciliardi"),
    (1e66, "undicilioni"),
    (1e69, "undiciliardi"),
    (1e72, "dodicilioni"),
    (1e75, "dodiciliardi"),
    (1e78, "tredicilioni"),
    (1e81, "trediciliardi"),
    (1e84, "quattordicilioni"),
    (1e87, "quattordiciliardi"),
    (1e90, "quindicilioni"),
    (1e93, "quindiciliardi"),
    (1e96, "sedicilioni"),
    (1e99, "sediciliardi"),
    (1e102, "diciassettilioni"),
    (1e105, "diciassettiliardi"),
    (1e108, "diciottilioni"),
    (1e111, "diciottiliardi"),
    (1e114, "dicianovilioni"),
    (1e117, "dicianoviliardi"),
    (1e120, "vintilioni"),
    (1e123, "vintiliardi"),
    (1e153, "quinquagintillion"),
    (1e183, "sexagintillion"),
    (1e213, "septuagintillion"),
    (1e243, "ottogintilioni"),
    (1e273, "nonigintillioni"),
    (1e303, "centilioni"),
    (1e306, "uncentilioni"),
    (1e309, "duocentilioni"),
    (1e312, "trecentilioni"),
    (1e333, "decicentilioni"),
    (1e336, "undicicentilioni"),
    (1e363, "viginticentilioni"),
    (1e366, "unviginticentilioni"),
    (1e393, "trigintacentilioni"),
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


def is_fractional_it(input_str, short_scale=False):
    """
    This function takes the given text and checks if it is a fraction.
    Updated to italian from en version 18.8.9

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): use short scale if True, long scale if False
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    input_str = input_str.lower()
    if input_str.endswith('i', -1) and len(input_str) > 2:
        input_str = input_str[:-1] + "o"  # normalizza plurali

    fracts_it = {"intero": 1, "mezza": 2, "mezzo": 2}

    if short_scale:
        for num in _SHORT_ORDINAL_STRING_IT:
            if num > 2:
                fracts_it[_SHORT_ORDINAL_STRING_IT[num]] = num
    else:
        for num in _LONG_ORDINAL_STRING_IT:
            if num > 2:
                fracts_it[_LONG_ORDINAL_STRING_IT[num]] = num

    if input_str in fracts_it:
        return 1.0 / fracts_it[input_str]
    return False


# ---------------------------------------------------------------------------
# Vocabulary-driven extraction on the shared RomanceNumberExtractor engine.
#
# Italian writes cardinals as a single fused word ("ventitré", "milleduecento-
# trentaquattro"), joining the parts with vowel elisions and the accented -tré
# ending. The rules encoded here follow the Accademia della Crusca consulenza
# "Quarantaquattro gatti in fila per sei col resto di due, o di quando e come
# scrivere i numeri in lettere"
# (https://accademiadellacrusca.it/it/consulenza/quarantaquattro-gatti-in-fila-
# per-sei-col-resto-di-due-o-di-quando-e-come-scrivere-i-numeri-in-lettere/1077):
# the tens elide their final vowel before "uno" and "otto" (venti->ventuno,
# venti->ventotto, trenta->trentuno/trentotto ...); "tre" carries a written
# accent in every compound (ventitré, trentatré, centotré); "cento" is
# invariable and "mille" pluralises to "mila" (duemila).
# ---------------------------------------------------------------------------


def swap_gender_it(word: str, gender: GrammaticalGender) -> str:
    """Only "uno" and the fraction noun "mezzo" inflect for gender in Italian."""
    if gender == GrammaticalGender.FEMININE:
        if word == "uno":
            return "una"
        if word == "mezzo":
            return "mezza"
    return word


def pluralize_it(word: str) -> str:
    """Regular Italian plural for the scale and fraction words used here."""
    if word == "mille":
        return "mila"                      # duemila, tremila
    if word.endswith(("e", "o")):
        return word[:-1] + "i"             # milione->milioni, quarto->quarti
    return word


_UNITS_IT = {0: 'zero', 1: 'uno', 2: 'due', 3: 'tre', 4: 'quattro',
             5: 'cinque', 6: 'sei', 7: 'sette', 8: 'otto', 9: 'nove'}

_TENS_IT = {10: 'dieci', 11: 'undici', 12: 'dodici', 13: 'tredici',
            14: 'quattordici', 15: 'quindici', 16: 'sedici', 17: 'diciassette',
            18: 'diciotto', 19: 'diciannove', 20: 'venti', 30: 'trenta',
            40: 'quaranta', 50: 'cinquanta', 60: 'sessanta', 70: 'settanta',
            80: 'ottanta', 90: 'novanta'}

_IT = NumberVocabulary(
    LANG="it",
    swap_gender=swap_gender_it,
    pluralize=pluralize_it,

    HUNDRED_PARTICLE="cento",          # cento is invariable
    DENOMINATOR_PARTICLE="",
    DIVIDED_BY_ZERO="diviso zero",
    NO_PREV_UNIT=[1000],               # "mille", never "un mille"
    NO_PLURAL=[1000],                  # "duemila", pluralised as "mila"

    NUMBER_OVERFLOW="numero davvero enorme",
    # Italy follows the long scale: milione 10^6, miliardo 10^9, bilione 10^12
    DEFAULT_SCALE=Scale.LONG,
    JOIN_WORD=["e"],
    JOINER_ON_TWENTYS=False,           # fused forms carry no spoken joiner
    JOINER_ON_HUNDREDS=False,
    JOINER_ON_THOUSANDS=False,
    JOINER_ON_SCALE_REMAINDER=False,
    MULTIPLY_HUNDREDS=True,            # "duecento" split to "due cento" = 200
    FRACTIONS_ALWAYS_MULTIPLY=True,    # "un quarto" = 1/4, "tre quarti" = 3/4

    DECIMAL_MARKER=["virgola", "punto"],
    NEGATIVE_SIGN=["meno"],
    UNITS=_UNITS_IT,
    TENS=_TENS_IT,
    HUNDREDS={},                       # the hundreds multiply the units instead
    FRACTION={2: 'mezzo', 3: 'terzo', 4: 'quarto', 5: 'quinto', 6: 'sesto',
              7: 'settimo', 8: 'ottavo', 9: 'nono', 10: 'decimo',
              11: 'undicesimo', 12: 'dodicesimo', 13: 'tredicesimo',
              14: 'quattordicesimo', 15: 'quindicesimo', 16: 'sedicesimo',
              17: 'diciassettesimo', 18: 'diciottesimo', 19: 'diciannovesimo',
              20: 'ventesimo', 100: 'centesimo', 1000: 'millesimo'},
    FRACTION_FEMALE={2: 'mezza'},
    SHORT_SCALE={1000: 'mille', 10 ** 6: 'milione', 10 ** 9: 'miliardo',
                 10 ** 12: 'bilione', 10 ** 15: 'biliardo', 10 ** 18: 'trilione',
                 10 ** 21: 'triliardo', 10 ** 24: 'quadrilione'},
    LONG_SCALE={1000: 'mille', 10 ** 6: 'milione', 10 ** 9: 'miliardo',
                10 ** 12: 'bilione', 10 ** 18: 'trilione', 10 ** 24: 'quadrilione',
                10 ** 30: 'quintilione', 10 ** 36: 'sestilione'},

    GENDERED_SPELLINGS={GrammaticalGender.FEMININE: {1: 'una'}},
    DIGIT_SPELLINGS={},
    ALT_SPELLINGS={
        'un': 1,                       # "un milione"
        'mila': 1000,                  # plural of mille inside compounds
        'milioni': 10 ** 6,
        'miliardi': 10 ** 9,
    },
    ORDINAL_UNITS={1: 'primo', 2: 'secondo', 3: 'terzo', 4: 'quarto',
                   5: 'quinto', 6: 'sesto', 7: 'settimo', 8: 'ottavo', 9: 'nono'},
    ORDINAL_TENS={10: 'decimo', 20: 'ventesimo', 30: 'trentesimo',
                  40: 'quarantesimo', 50: 'cinquantesimo', 60: 'sessantesimo',
                  70: 'settantesimo', 80: 'ottantesimo', 90: 'novantesimo'},
    ORDINAL_HUNDREDS={100: 'centesimo'},
    ORDINAL_SHORT_SCALE={1000: 'millesimo', 10 ** 6: 'milionesimo'},
    ORDINAL_LONG_SCALE={1000: 'millesimo', 10 ** 6: 'milionesimo'},
)


# --- fused-compound splitter ----------------------------------------------
# Italian glues a whole numeral into one word ("milleduecentotrentaquattro").
# The shared engine tokenises on spaces, so a per-language hook first breaks the
# fused word back into the space-separated numeral morphemes the vocabulary
# knows, restoring the vowel elided at each join.

_MORPHEMES_IT = {}
for _d in (_UNITS_IT, _TENS_IT):
    for _v in _d.values():
        _MORPHEMES_IT[_v] = _v
_MORPHEMES_IT['cento'] = 'cento'
for _s in ('mille', 'mila', 'milione', 'milioni', 'miliardo', 'miliardi',
           'bilione', 'bilioni'):
    _MORPHEMES_IT[_s] = _s
# elided tens ("vent-", "trent-", ... appear only before "uno"/"otto"): the
# full tens word above is matched first, so these only fire on an elision.
for _full in ('venti', 'trenta', 'quaranta', 'cinquanta', 'sessanta',
              'settanta', 'ottanta', 'novanta'):
    _MORPHEMES_IT[_full[:-1]] = _full
# longest surface first, so "trenta" wins over "trent" and "sette" over "sei"
_MORPHEME_SURFACES_IT = sorted(_MORPHEMES_IT, key=len, reverse=True)


def _split_fused_it(word: str) -> str:
    """Break a fused Italian numeral into space-separated morphemes.

    Restores the accent (ventitré -> ventitre) and the vowel elided before
    "uno"/"otto" in the tens and hundreds (ventuno -> venti uno, centotto ->
    cento otto). A word that does not decompose cleanly into numeral morphemes
    is returned unchanged, so non-numbers ("trentini") stay non-numbers.
    """
    w = word.lower().replace('é', 'e').replace('è', 'e')
    # cento elides its final -o before uno and before any o-word (otto,
    # ottanta...): "centuno", "centottanta", "trecentottantotto". Restore the
    # dropped vowel so the morpheme splitter sees "cento" + remainder.
    w = w.replace('centuno', 'centouno').replace('centott', 'centoott')
    out = []
    i = 0
    while i < len(w):
        for surf in _MORPHEME_SURFACES_IT:
            if w.startswith(surf, i):
                out.append(_MORPHEMES_IT[surf])
                i += len(surf)
                break
        else:
            return word
    return ' '.join(out)


class ItalianNumberExtractor(RomanceNumberExtractor):
    """Italian number engine.

    Adds the one Italian-specific surface convention the shared engine does not
    model: cardinals are written as a single fused word. The extractor splits
    each fused token back into numeral morphemes before delegating to the shared
    vocabulary-driven parser.
    """

    def _presplit(self, text: str) -> str:
        # a comma glued to a word is a group separator ("duemila, ventitre"),
        # not part of the number
        text = re.sub(r"(?<=[^\W\d]),", " ", text)
        return " ".join(_split_fused_it(tok) for tok in text.split())

    def extract_number(self,
                       text: str,
                       ordinals: bool = False,
                       scale: Optional[Scale] = None
                       ) -> Union[int, float, bool]:
        if isinstance(text, str):
            text = self._presplit(text)
        return super().extract_number(text, ordinals=ordinals, scale=scale)

    def numbers_to_digits(self,
                          utterance: str,
                          scale: Optional[Scale] = None) -> str:
        return super().numbers_to_digits(self._presplit(utterance), scale=scale)


IT = ItalianNumberExtractor(_IT)


def extract_number_it(text, short_scale=False, ordinals=False):
    """Extract a number from Italian text.

    Delegates to the shared :class:`RomanceNumberExtractor`. Italian writes each
    cardinal as a single fused word, so a per-language splitter first tokenises
    the fused form back into numeral morphemes, restoring the vowel elided
    before "uno"/"otto" (ventuno -> venti uno, centotto -> cento otto) and the
    accented -tré ending (ventitré -> venti tre). These fusion, elision and
    accent rules follow the Accademia della Crusca consulenza "Quarantaquattro
    gatti in fila per sei col resto di due, o di quando e come scrivere i numeri
    in lettere"
    (https://accademiadellacrusca.it/it/consulenza/quarantaquattro-gatti-in-
    fila-per-sei-col-resto-di-due-o-di-quando-e-come-scrivere-i-numeri-in-
    lettere/1077): the tens drop their final vowel before "uno" and "otto"
    (ventuno, ventotto, trentuno, quarantotto), "tre" is written "-tré" in every
    compound, "cento" is invariable and "mille" pluralises to "mila" (duemila).
    The ``scale`` defaults to the long scale used in Italy (miliardo 10^9,
    bilione 10^12).

    Args:
        text (str): the string to extract a number from
        short_scale (bool): use the short scale instead of the default long scale
        ordinals (bool): also recognise ordinal words
    Returns:
        (int, float) or False: the extracted number, or False if none is found
    """
    scale = Scale.SHORT if short_scale else _IT.DEFAULT_SCALE
    return IT.extract_number(text, ordinals=ordinals, scale=scale)


def nice_number_it(number, speech=True, denominators=range(1, 21)):
    """ Italian helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 e un mezz" for speech and "4 1/2" for text

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
    # denominatore
    den_str = _FRACTION_STRING_IT[den]
    # frazione
    if whole == 0:
        if num == 1:
            # un decimo
            return_string = 'un {}'.format(den_str)
        else:
            # tre mezzi
            return_string = '{} {}'.format(num, den_str)
    # interi  >10
    elif num == 1:
        # trenta e un
        return_string = '{} e un {}'.format(whole, den_str)
    # interi >10 con frazioni
    else:
        # venti e 3 decimi
        return_string = '{} e {} {}'.format(whole, num, den_str)

    # gestisce il plurale del denominatore
    if num > 1:
        return_string += 'i'
    else:
        return_string += 'o'

    return return_string


def pronounce_number_it(number, places=2, short_scale=False, scientific=False):
    """
    Convert a number to it's spoken equivalent
    adapted to italian fron en version

    For example, '5.2' would return 'cinque virgola due'

    Args:
        num(float or int): the number to pronounce (under 100)
        places(int): maximum decimal places to speak
        short_scale (bool) : use short (True) or long scale (False)
            https://en.wikipedia.org/wiki/Names_of_large_numbers
        scientific (bool): pronounce in scientific notation
    Returns:
        (str): The pronounced number
    """
    num = number
    # gestione infinito
    if num == float("inf"):
        return "infinito"
    elif num == float("-inf"):
        return "meno infinito"

    if scientific:
        number = '%E' % num
        n, power = number.replace("+", "").split("E")
        power = int(power)
        if power != 0:
            return '{}{} per dieci elevato alla {}{}'.format(
                'meno ' if float(n) < 0 else '',
                pronounce_number_it(abs(float(n)), places, short_scale, False),
                'meno ' if power < 0 else '',
                pronounce_number_it(abs(power), places, short_scale, False))

    if short_scale:
        number_names = _NUM_STRING_IT.copy()
        number_names.update(_SHORT_SCALE_IT)
    else:
        number_names = _NUM_STRING_IT.copy()
        number_names.update(_LONG_SCALE_IT)

    digits = [number_names[n] for n in range(0, 20)]

    tens = [number_names[n] for n in range(10, 100, 10)]

    if short_scale:
        hundreds = [_SHORT_SCALE_IT[n] for n in _SHORT_SCALE_IT.keys()]
    else:
        hundreds = [_LONG_SCALE_IT[n] for n in _LONG_SCALE_IT.keys()]

    # deal with negatives
    result = ""
    if num < 0:
        result = "meno "
    num = abs(num)

    # check for a direct match
    if num in number_names:
        if num > 90:
            result += ""  # inizio stringa
        result += number_names[num]
    else:
        def _sub_thousand(n):
            assert 0 <= n <= 999
            if n <= 19:
                return digits[n]
            elif n <= 99:
                q, r = divmod(n, 10)
                _deci = tens[q - 1]
                _unit = r
                _partial = _deci
                if _unit > 0:
                    if _unit == 1 or _unit == 8:
                        _partial = _partial[:-1]  # ventuno  ventotto
                    _partial += number_names[_unit]
                return _partial
            else:
                q, r = divmod(n, 100)
                if q == 1:
                    _partial = "cento"
                else:
                    _partial = digits[q] + "cento"
                # Crusca (consulenza 1077): "la grafia prevista è, tranne rare
                # eccezioni, senza spazi: duecentodiecimila". Cardinals below a
                # million are one fused word, so the hundreds join directly.
                rest = _sub_thousand(r) if r else ""
                # "cento" drops its final -o before a word beginning with o
                # (otto, ottanta...): "centottanta", "trecentottantotto", not
                # "centoottanta". Both ICU and num2words agree.
                if rest.startswith("o"):
                    _partial = _partial[:-1]
                _partial += rest
                return _partial

        def _short_scale(n):
            if n >= max(_SHORT_SCALE_IT.keys()):
                return "numero davvero enorme"
            n = int(n)
            assert 0 <= n
            res = []
            for i, z in enumerate(_split_by(n, 1000)):
                if not z:
                    continue
                number = _sub_thousand(z)
                if i:
                    # a scale word joins onto a single Italian word, so the
                    # digit group it multiplies must collapse to one token
                    # first: "cento uno" + "mila" -> "centounomila", never
                    # "cento unomila" (which reads back as 100 + 1000)
                    number = number.replace(" ", "") + hundreds[i]
                res.append(number)

            # one fused word below a million ("millecentoventidue")
            return "".join(reversed(res))

        def _split_by(n, split=1000):
            assert 0 <= n
            res = []
            while n:
                n, r = divmod(n, split)
                res.append(r)
            return res

        def _long_scale(n):
            if n >= max(_LONG_SCALE_IT.keys()):
                return "numero davvero enorme"
            n = int(n)
            assert 0 <= n
            res = []
            for i, z in enumerate(_split_by(n, 1000000)):
                if not z:
                    continue
                if not i:
                    # the sub-million group is one fused word
                    number = pronounce_number_it(z, places, True, scientific)
                    res.append(number)
                    continue
                # milione/miliardo are separate words, unlike the fused "mila":
                # "un milione", "due milioni", "un miliardo" (Crusca allows the
                # spaced form for these large scale words). The plural table
                # holds "milioni"/"miliardi"; 1 takes the apocopated "un" and
                # the singular.
                plural = hundreds[i + 1]
                singular = _LONG_SCALE_SINGULAR_IT.get(
                    plural, plural[:-1] + "e")
                if z == 1:
                    number = "un " + singular
                else:
                    count = pronounce_number_it(z, places, True, scientific)
                    number = count + " " + plural
                res.append(number)
            # scale groups are separated by a space ("un milione duecentomila")
            return " ".join(reversed(res))

        if short_scale:
            result += _short_scale(num)
        else:
            result += _long_scale(num)

    # normalizza unità misura singole e 'ragionevoli' ed ad inizio stringa
    if result == 'mila':
        result = 'mille'
    if result == 'milioni':
        result = 'un milione'
    if result == 'miliardi':
        result = 'un miliardo'
    if result[0:7] == 'unomila':
        result = result.replace('unomila', 'mille', 1)
    if result[0:10] == 'unomilioni':
        result = result.replace('unomilioni', 'un milione', 1)
    # if result[0:11] == 'unomiliardi':
    # result = result.replace('unomiliardi', 'un miliardo', 1)

    # Every compound of "tre" carries a written acute accent on the final
    # syllable: ventitré, trentatré, centotré, duemilatré. Accademia della
    # Crusca, consulenza 1077 "Quarantaquattro gatti ...": "I composti di tre
    # si scrivono più correttamente con l'accento". The standalone "tre" (3)
    # takes none, so only a "tre" that ends a longer word is accented.
    result = re.sub(r"(?<=[a-zàèéìòù])tre\b", "tré", result)

    # Deal with fractional part
    if not num == int(num) and places > 0:
        if abs(num) < 1.0 and (result == "meno " or not result):
            result += "zero"
        result += " virgola"
        _num_str = str(num)
        _num_str = _num_str.split(".")[1][0:places]
        for char in _num_str:
            result += " " + number_names[int(char)]
    return result
