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
from dataclasses import dataclass, field
from math import isfinite
from typing import Dict, List, Optional, Union

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

_NEGATIVES = {"minus", "negatif"}
_DECIMAL_MARKERS = {"koma"}

_HALF_WORDS = {"setengah": 0.5, "separuh": 0.5}


@dataclass
class _LangDef:
    code: str
    zero: str
    eight: str
    billion: str      # 1e9
    trillion: str     # 1e12
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

    def fraction_words(self) -> Dict[str, float]:
        words = dict(_HALF_WORDS)
        words.update(self.quarter_words)
        return words


_ID = _LangDef(code="id", zero="nol", eight="delapan",
               billion="miliar", trillion="triliun")
_MS = _LangDef(code="ms", zero="sifar", eight="lapan",
               billion="bilion", trillion="trilion",
               quarter_words={"suku": 0.25})

_LANGS = {"id": _ID, "ms": _MS}

# spellings accepted on input but never produced (loanword variants and
# the sibling standard's forms are mutually intelligible)
_EXTRA_INPUT = {
    "id": {"kosong": 0},   # colloquial zero
    "ms": {"kosong": 0},
}
_EXTRA_SCALES = {
    "id": {"milyar": 10 ** 9, "trilyun": 10 ** 12},
    "ms": {},
}


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
        n, power = ('%E' % number).replace("+", "").split("E")
        power = int(power)
        if power != 0:
            return '{}{} kali sepuluh pangkat {}{}'.format(
                'minus ' if float(n) < 0 else '',
                _pronounce_number(abs(float(n)), lang, places),
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
        _num_str = str(number).split(".")[1][0:places]
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


def _is_fractional(input_str: str, lang: _LangDef, spoken=True):
    if not spoken:
        return False
    word = input_str.lower().strip()
    fractions = lang.fraction_words()
    if word in fractions:
        return fractions[word]
    # "seper<den>" = 1/den, "per<den>" = the denominator after a numerator
    for prefix, numerator in (("seper", 1), ("per", 1)):
        if word.startswith(prefix) and len(word) > len(prefix):
            den = _parse_tokens(word[len(prefix):].split(), lang)
            if den and den >= 2 and den == int(den):
                return numerator / den
    return False


def _parse_tokens(tokens: List[str], lang: _LangDef) -> Optional[float]:
    """Parse a run of number words; None if the run is not a number.

    Group logic: units accumulate into ``small``; "puluh" multiplies the
    pending unit by ten; "belas" adds ten; "ratus" moves the pending
    value into the hundreds slot; "ribu"/"juta"/... close the group.
    """
    extra = _EXTRA_INPUT.get(lang.code, {})
    extra_scales = _EXTRA_SCALES.get(lang.code, {})
    total = 0.0
    hundreds = 0
    small = 0
    seen = False
    seen_group = False
    for tok in tokens:
        if tok in lang.units or tok in extra:
            value = lang.units.get(tok, extra.get(tok))
            if tok in extra and value == 0:
                if seen:
                    return None
                seen = True
                continue
            small += value
            seen = True
        elif tok == lang.zero:
            if seen:
                return None
            seen = True
        elif tok in _SE_FORMS:
            value = _SE_FORMS[tok]
            if value >= 1000:
                total += value
                seen_group = True
            elif value == 100:
                hundreds += 100
            else:
                small += value
            seen = True
        elif tok == "puluh":
            if not small or small > 9:
                return None
            small *= 10
        elif tok == "belas":
            if not 1 <= small <= 9:
                return None
            small += 10
        elif tok == "ratus":
            if not small or small > 9:
                return None
            hundreds += small * 100
            small = 0
        elif tok in lang.group_multipliers or tok in extra_scales:
            mult = lang.group_multipliers.get(tok, extra_scales.get(tok))
            group = hundreds + small
            if not group:
                return None
            total += group * mult
            hundreds = small = 0
            seen_group = True
        else:
            return None
    if not seen and not seen_group:
        return None
    result = total + hundreds + small
    return int(result) if result == int(result) else result


def _tokenize(text: str) -> List[str]:
    return text.lower().replace(",", " ").split()


def _is_number_token(tok: str, lang: _LangDef) -> bool:
    extra = _EXTRA_INPUT.get(lang.code, {})
    extra_scales = _EXTRA_SCALES.get(lang.code, {})
    return tok in lang.vocab or tok in extra or tok in extra_scales


def _extract_number(text: str, lang: _LangDef,
                    ordinals: bool = False) -> Union[int, float, bool]:
    tokens = _tokenize(text)
    fractions = lang.fraction_words()

    i = 0
    while i < len(tokens):
        tok = tokens[i]

        # digits (also "8,5")
        clean = tok.strip(".!?;:")
        if re.fullmatch(r"-?\d+(?:[.,]\d+)?", clean):
            val = float(clean.replace(",", "."))
            if not isfinite(val):
                return False
            # "2 setengah" = 2.5
            if i + 1 < len(tokens) and tokens[i + 1] in fractions:
                val += fractions[tokens[i + 1]]
            return int(val) if val == int(val) else val
        pieces = clean.split("/")
        if len(pieces) == 2 and all(p.lstrip("-").isdigit() for p in pieces) \
                and float(pieces[1]) != 0:
            return float(pieces[0]) / float(pieces[1])

        # ordinals: "pertama", "kedua", "kedua puluh satu"
        if ordinals:
            if tok == "pertama":
                return 1
            if tok.startswith("ke") and _is_number_token(tok[2:], lang):
                run = [tok[2:]]
                j = i + 1
                while j < len(tokens) and _is_number_token(tokens[j], lang):
                    run.append(tokens[j])
                    j += 1
                val = _longest_parse(run, lang)
                if val is not None:
                    return val

        # standalone fraction words ("setengah", "suku", "sepertiga")
        frac = _is_fractional(tok, lang)
        if frac and tok not in lang.vocab:
            return frac

        if _is_number_token(tok, lang):
            negative = i > 0 and tokens[i - 1] in _NEGATIVES
            run = [tok]
            j = i + 1
            while j < len(tokens) and _is_number_token(tokens[j], lang):
                run.append(tokens[j])
                j += 1
            val = _longest_parse(run, lang)
            if val is None:
                i += 1
                continue
            rest = tokens[j:]
            # "dua koma lima" = 2.5
            if len(rest) >= 2 and rest[0] in _DECIMAL_MARKERS:
                digits = ""
                for d in rest[1:]:
                    dv = _parse_tokens([d], lang)
                    if dv is None or dv > 9:
                        break
                    digits += str(int(dv))
                if digits:
                    val = float(f"{val}.{digits}")
            # "dua pertiga" = 2/3
            elif rest and _is_fractional(rest[0], lang) \
                    and rest[0].startswith("per"):
                val = val * _is_fractional(rest[0], lang)
            # "dua setengah" = 2.5, "tiga suku" = 3.25
            elif rest and rest[0] in fractions:
                val = val + fractions[rest[0]]
            if negative:
                val = -val
            return int(val) if val == int(val) else val

        i += 1
    return False


def _longest_parse(run: List[str], lang: _LangDef) -> Optional[float]:
    """Parse the longest prefix of ``run`` that is a valid number."""
    for end in range(len(run), 0, -1):
        val = _parse_tokens(run[:end], lang)
        if val is not None:
            return val
    return None


def _numbers_to_digits(utterance: str, lang: _LangDef) -> str:
    tokens = utterance.split()
    fractions = lang.fraction_words()
    out = []
    i = 0
    while i < len(tokens):
        clean = tokens[i].lower().strip(".,!?;:")
        if not _is_number_token(clean, lang):
            out.append(tokens[i])
            i += 1
            continue
        run = [clean]
        j = i + 1
        while j < len(tokens):
            nxt = tokens[j].lower().strip(".,!?;:")
            if _is_number_token(nxt, lang):
                run.append(nxt)
                j += 1
            else:
                break
        # longest prefix of the run that parses as one number
        best = None
        for end in range(len(run), 0, -1):
            val = _parse_tokens(run[:end], lang)
            if val is not None:
                best = (val, end)
                break
        if best is None:
            out.append(tokens[i])
            i += 1
            continue
        val, end = best
        last = tokens[i + end - 1]
        stripped = last.rstrip(".,!?;:")
        trail = last[len(stripped):]
        if isinstance(val, float) and val.is_integer():
            val = int(val)
        out.append(f"{val}{trail}")
        i += end
    return " ".join(out)


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


def extract_number_id(text, short_scale=True, ordinals=False):
    """Extract a number from Indonesian text; False if none found."""
    return _extract_number(text, _ID, ordinals)


def extract_number_ms(text, short_scale=True, ordinals=False):
    """Extract a number from Malay text; False if none found."""
    return _extract_number(text, _MS, ordinals)


def is_fractional_id(input_str, short_scale=True, spoken=True):
    """Check if Indonesian text is a fraction word; the fraction or False."""
    return _is_fractional(input_str, _ID, spoken)


def is_fractional_ms(input_str, short_scale=True, spoken=True):
    """Check if Malay text is a fraction word; the fraction or False."""
    return _is_fractional(input_str, _MS, spoken)


def numbers_to_digits_id(utterance, short_scale=True, ordinals=False):
    """Replace spoken Indonesian numbers in a string with digits."""
    return _numbers_to_digits(utterance, _ID)


def numbers_to_digits_ms(utterance, short_scale=True, ordinals=False):
    """Replace spoken Malay numbers in a string with digits."""
    return _numbers_to_digits(utterance, _MS)
