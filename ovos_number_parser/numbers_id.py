"""Indonesian and Malay number parsing and formatting.

The two standards share the same numeral system — the ``se-`` prefix
("sepuluh" = 10, "seratus" = 100, "seribu" = 1000), teens in "belas"
("dua belas" = 12) and multipliers "puluh"/"ratus"/"ribu"/"juta" — and
only diverge in a handful of forms:

======  ==================  ==================
value   Indonesian (id)     Malay (ms)
======  ==================  ==================
0       nol                 sifar
8       delapan             lapan
1e9     miliar              bilion
1e12    triliun             trilion
======  ==================  ==================

The decimal separator is spoken "koma" in both. Fractions use the
``per-`` denominator ("dua pertiga" = 2/3, "seperempat" = 1/4) plus
"setengah"/"separuh" (half) and, in Malay, "suku" (quarter). Ordinals
take the ``ke-`` prefix ("kedua" = 2nd) with the irregular "pertama"
(1st).
"""
import re
from decimal import Decimal
from dataclasses import dataclass, field
from typing import Dict, Union

from ovos_number_parser.util import scientific_parts

_UNITS_COMMON = {
    "satu": 1, "dua": 2, "tiga": 3, "empat": 4, "lima": 5,
    "enam": 6, "tujuh": 7, "sembilan": 9,
}

# se- fused forms (se- = "one")
_SE_FORMS = {
    "sepuluh": 10, "sebelas": 11, "seratus": 100, "seribu": 1000,
    "sejuta": 1000000,
}

# multipliers applying to the preceding group
_GROUP_MULTIPLIERS_COMMON = {
    "ribu": 1000, "juta": 1000000,
}


_HALF_WORDS = {"setengah": 0.5, "separuh": 0.5}


@dataclass
class _LangDef:
    code: str
    zero: str
    eight: str
    billion: str      # 1e9
    trillion: str     # 1e12
    group_mark: str   # groups the thousands of a digit string
    quarter_words: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self):
        self.units = dict(_UNITS_COMMON)
        self.units[self.eight] = 8
        self.group_multipliers = dict(_GROUP_MULTIPLIERS_COMMON)
        self.group_multipliers[self.billion] = 10 ** 9
        self.group_multipliers[self.trillion] = 10 ** 12
        # every token the parser understands
        self.vocab = set(self.units) | set(_SE_FORMS) | \
            set(self.group_multipliers) | {self.zero, "puluh", "belas",
                                           "ratus"}
        self.num_string = {0: self.zero}
        self.num_string.update({v: k for k, v in self.units.items()})
        group = re.escape(self.group_mark)
        decimal = re.escape("," if self.group_mark == "." else ".")
        # a group number never starts with 0 ("0.500" is a decimal)
        self.grouped_digits = re.compile(
            rf"-?[1-9]\d{{0,2}}(?:{group}\d{{3}})+(?:{decimal}\d+)?")

    def fraction_words(self) -> Dict[str, float]:
        words = dict(_HALF_WORDS)
        words.update(self.quarter_words)
        return words


_ID = _LangDef(code="id", zero="nol", eight="delapan",
               billion="miliar", trillion="triliun", group_mark=".")
_MS = _LangDef(code="ms", zero="sifar", eight="lapan",
               billion="bilion", trillion="trilion", group_mark=",",
               quarter_words={"suku": 0.25})


def _pronounce_group(n: int, lang: _LangDef) -> str:
    """Spell 1 <= n <= 999."""
    assert 1 <= n <= 999
    parts = []
    hundreds, rest = divmod(n, 100)
    if hundreds == 1:
        parts.append("seratus")
    elif hundreds:
        parts.append(lang.num_string[hundreds] + " ratus")
    if 10 <= rest <= 11:
        parts.append("sepuluh" if rest == 10 else "sebelas")
    elif 12 <= rest <= 19:
        parts.append(lang.num_string[rest - 10] + " belas")
    else:
        tens, units = divmod(rest, 10)
        if tens:
            parts.append(lang.num_string[tens] + " puluh")
        if units:
            parts.append(lang.num_string[units])
    return " ".join(parts)


def _pronounce_int(n: int, lang: _LangDef) -> str:
    if n == 0:
        return lang.zero
    scales = [(10 ** 12, lang.trillion), (10 ** 9, lang.billion),
              (10 ** 6, "juta"), (1000, "ribu")]
    parts = []
    for value, word in scales:
        count, n = divmod(n, value)
        if not count:
            continue
        if count == 1 and word == "ribu":
            parts.append("seribu")
        else:
            parts.append(f"{_pronounce_int(count, lang)} {word}")
    if n:
        parts.append(_pronounce_group(n, lang))
    return " ".join(parts)


def _pronounce_number(number: Union[int, float], lang: _LangDef,
                      places: int = 2, scientific: bool = False,
                      ordinals: bool = False) -> str:
    if number == float("inf"):
        return "tak terhingga"
    if number == float("-inf"):
        return "minus tak terhingga"
    if scientific:
        n, power = scientific_parts(number, places)
        if power != 0:
            return '{}{} kali sepuluh pangkat {}{}'.format(
                'minus ' if n < 0 else '',
                _pronounce_number(abs(n), lang, places),
                'minus ' if power < 0 else '',
                _pronounce_number(abs(power), lang, places))

    if ordinals:
        return _pronounce_ordinal(number, lang)

    result = ""
    if number < 0:
        result = "minus "
    number = abs(number)

    result += _pronounce_int(int(number), lang)

    if number != int(number) and places > 0:
        result += " koma"
        _num_str = f"{Decimal(str(number)):f}".split(".")[1][0:places]
        for char in _num_str:
            result += " " + lang.num_string[int(char)]
    return result


def _pronounce_ordinal(number: Union[int, float], lang: _LangDef) -> str:
    if number != int(number) or number < 1:
        raise ValueError("ordinals must be positive integers")
    number = int(number)
    if number == 1:
        return "pertama"
    return "ke" + _pronounce_int(number, lang)


def _nice_number(number, lang: _LangDef, speech=True,
                 denominators=range(1, 21)):
    from ovos_number_parser.util import convert_to_mixed_fraction
    result = convert_to_mixed_fraction(number, denominators)
    if not result:
        return str(round(number, 3))
    whole, num, den = result
    if not speech:
        if num == 0:
            return str(whole)
        return '{} {}/{}'.format(whole, num, den)
    if num == 0:
        return str(whole)
    if den == 2:
        # convert_to_mixed_fraction keeps num < den, so num == 1 here
        return "setengah" if whole == 0 else f"{whole} setengah"
    den_str = "per" + _pronounce_int(den, lang)
    if num == 1 and whole == 0:
        # "seperempat" = 1/4
        return "se" + den_str
    if whole == 0:
        return '{} {}'.format(num, den_str)
    return '{} {} {}'.format(whole, num, den_str)


# --- public per-language API ------------------------------------------------

def pronounce_number_id(number, places=2, short_scale=True, scientific=False,
                        ordinals=False):
    """Convert a number to its spoken Indonesian equivalent."""
    return _pronounce_number(number, _ID, places, scientific, ordinals)


def pronounce_number_ms(number, places=2, short_scale=True, scientific=False,
                        ordinals=False):
    """Convert a number to its spoken Malay equivalent."""
    return _pronounce_number(number, _MS, places, scientific, ordinals)


def pronounce_ordinal_id(number):
    """Spoken Indonesian ordinal, e.g. 2 -> "kedua"."""
    return _pronounce_ordinal(number, _ID)


def pronounce_ordinal_ms(number):
    """Spoken Malay ordinal, e.g. 2 -> "kedua"."""
    return _pronounce_ordinal(number, _MS)


def nice_number_id(number, speech=True, denominators=range(1, 21)):
    """Indonesian helper for nice_number: 4.5 becomes "4 setengah"."""
    return _nice_number(number, _ID, speech, denominators)


def nice_number_ms(number, speech=True, denominators=range(1, 21)):
    """Malay helper for nice_number: 4.5 becomes "4 setengah"."""
    return _nice_number(number, _MS, speech, denominators)


