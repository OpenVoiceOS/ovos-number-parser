"""Kabyle (Taqbaylit, ``kab``) number tools.

Kabyle has two numeral systems in active use:

- the pan-Amazigh (Berber) numerals, universally used for 1-10:
  yiwen, sin, kṛaḍ, kuẓ, semmus, sḍis, sa, tam, tẓa, mraw
- the Algerian-Arabic borrowed numerals, which carry everyday counting
  above ten: ḥḍac (11), ɛecrin (20), mya (100), alef (1000), joined with
  the conjunction "u" ("waḥed u ɛecrin" = 21, unit before ten)

Pronunciation uses the Amazigh forms for 0-10 and the Arabic-derived
forms above ten (the system with consistent attestation for large
values). Extraction accepts both systems, including feminine forms
(yiwet, snat, ...) and additive Amazigh compounds ("mraw d yiwen" = 11).

Ordinals are formed with wis (masculine) / tis (feminine) + cardinal;
"first" is the adjective amezwaru / tamezwarut.

Sources:
- https://en.wikipedia.org/wiki/Kabyle_language (grammar & numeral notes)
- https://www.omniglot.com/language/numbers/kabyle.htm
- https://www.languagesandnumbers.com/how-to-count-in-kabyle/en/kab/
- https://fr.wikipedia.org/wiki/Num%C3%A9ration_amazighe
"""
import re
from typing import Union

from ovos_number_parser.util import GrammaticalGender

# pan-Amazigh cardinals, masculine (pronunciation defaults)
_UNITS_AMAZIGH_M = {0: "ilem", 1: "yiwen", 2: "sin", 3: "kṛaḍ", 4: "kuẓ",
                    5: "semmus", 6: "sḍis", 7: "sa", 8: "tam", 9: "tẓa",
                    10: "mraw"}
# feminine counterparts (only 1 and 2 are pronounced; all are extracted)
_UNITS_AMAZIGH_F = {1: "yiwet", 2: "snat", 3: "kṛaḍet", 4: "kuẓet",
                    5: "semmuset", 6: "sḍiset", 7: "sat", 8: "tamet",
                    9: "tẓat", 10: "mrawet"}

# Arabic-derived cardinals (everyday counting system)
_UNITS_LOAN = {1: "waḥed", 2: "tnayn", 3: "tlata", 4: "ṛebɛa", 5: "xemsa",
               6: "setta", 7: "sebɛa", 8: "tmanya", 9: "tesɛa", 10: "ɛecṛa"}
_TEENS_LOAN = {11: "ḥḍac", 12: "tnac", 13: "tleṭṭac", 14: "ṛbeɛṭac",
               15: "xemseṭṭac", 16: "seṭṭac", 17: "sebeɛṭac",
               18: "temmenṭac", 19: "tseɛṭac"}
_TENS_LOAN = {20: "ɛecrin", 30: "tlatin", 40: "ṛebɛin", 50: "xemsin",
              60: "settin", 70: "sebɛin", 80: "tmanyin", 90: "tsɛin"}
_HUNDREDS_LOAN = {100: "mya", 200: "mitin", 300: "telt-mya", 400: "ṛebɛ-mya",
                  500: "xems-mya", 600: "sett-mya", 700: "sebɛ-mya",
                  800: "temn-mya", 900: "tesɛ-mya"}
_THOUSANDS_LOAN = {1000: "alef", 2000: "juǧ alaf", 3000: "tlat-alaf",
                   4000: "ṛebɛ-alaf", 5000: "xems-alaf", 6000: "sett-alaf",
                   7000: "sebɛ-alaf", 8000: "temn-alaf", 9000: "tesɛ-alaf"}

# conjunction joining number words ("waḥed u ɛecrin" = 21,
# "mraw d yiwen" = 11)
_CONNECTORS = {"u", "d", "ed"}

_FRACTIONS = {"azgen": 0.5}  # half; other fraction nouns are not attested

_ORDINAL_FIRST = {"amezwaru": 1, "tamezwarut": 1}
_ORDINAL_MARKERS = {"wis", "tis"}


def _normalize(token: str) -> str:
    """Diacritic-tolerant lookup key (ṛ→r, ṭ→t, ḍ→d, ẓ→z, ḥ→h, ǧ→g)."""
    table = str.maketrans("ṛṭḍẓḥǧṣč", "rtdzhgsc")
    return token.lower().translate(table)


def _build_word_map():
    words = {}
    for table in (_UNITS_AMAZIGH_M, _UNITS_AMAZIGH_F, _UNITS_LOAN,
                  _TEENS_LOAN, _TENS_LOAN, _HUNDREDS_LOAN, _THOUSANDS_LOAN):
        for val, word in table.items():
            words[_normalize(word)] = val
    for word, val in _FRACTIONS.items():
        words[_normalize(word)] = val
    return words


_WORDS = _build_word_map()


def _slot(val) -> str:
    if val < 1:
        return "frac"
    if val >= 1000:
        return "thousand"
    if val >= 100:
        return "hundred"
    if 11 <= val <= 19:
        return "teen"
    if val == 10 or (val % 10 == 0 and val >= 20):
        return "ten"
    return "unit"


def pronounce_number_kab(number: Union[int, float], places: int = 3,
                         ordinals: bool = False,
                         gender: GrammaticalGender = GrammaticalGender.MASCULINE) -> str:
    """Pronounce a number in Kabyle.

    Supports integers from 0 to 9999; the minus word and decimal-separator
    word are not reliably attested, so negative and non-integer values are
    rejected rather than guessed.
    """
    if ordinals:
        return pronounce_ordinal_kab(number, gender)
    if isinstance(number, float):
        if not number.is_integer():
            raise ValueError(
                "Kabyle decimal pronunciation is not supported")
        number = int(number)
    if number < 0:
        raise ValueError("Kabyle negative pronunciation is not supported")
    if number > 9999:
        raise OverflowError(
            "Kabyle pronunciation is supported up to 9999")

    if number <= 10:
        if gender == GrammaticalGender.FEMININE and number in (1, 2):
            return _UNITS_AMAZIGH_F[number]
        return _UNITS_AMAZIGH_M[number]

    parts = []
    thousands = number // 1000 * 1000
    hundreds = number % 1000 // 100 * 100
    rest = number % 100
    if thousands:
        parts.append(_THOUSANDS_LOAN[thousands])
    if hundreds:
        parts.append(_HUNDREDS_LOAN[hundreds])
    if rest:
        if rest <= 10:
            # units keep the Amazigh form even inside compounds when they
            # stand alone; the Arabic-loan unit is used before a ten
            parts.append(_UNITS_AMAZIGH_M[rest] if not parts
                         else _UNITS_LOAN[rest])
        elif rest in _TEENS_LOAN:
            parts.append(_TEENS_LOAN[rest])
        elif rest in _TENS_LOAN:
            parts.append(_TENS_LOAN[rest])
        else:
            ten = rest // 10 * 10
            unit = rest % 10
            parts.append(f"{_UNITS_LOAN[unit]} u {_TENS_LOAN[ten]}")
    return " u ".join(parts)


def pronounce_ordinal_kab(number: Union[int, float],
                          gender: GrammaticalGender = GrammaticalGender.MASCULINE) -> str:
    """Ordinals: amezwaru "first", otherwise wis/tis + cardinal."""
    number = int(number)
    if number < 1:
        raise ValueError("Kabyle ordinals start at 1")
    if number == 1:
        return "tamezwarut" if gender == GrammaticalGender.FEMININE \
            else "amezwaru"
    marker = "tis" if gender == GrammaticalGender.FEMININE else "wis"
    return f"{marker} {pronounce_number_kab(number, gender=gender)}"


def is_fractional_kab(input_str: str, short_scale: bool = False) -> Union[bool, float]:
    """Only the well-attested "azgen" (half) is recognized."""
    return _FRACTIONS.get(_normalize(input_str.strip())) or False


def is_ordinal_kab(input_str: str) -> Union[bool, int]:
    """Detect wis/tis + cardinal ordinals and amezwaru/tamezwarut."""
    text = _normalize(input_str.strip())
    if text in {_normalize(k) for k in _ORDINAL_FIRST}:
        return 1
    tokens = text.split()
    if len(tokens) >= 2 and tokens[0] in _ORDINAL_MARKERS:
        val = extract_number_kab(" ".join(tokens[1:]))
        if val and float(val).is_integer():
            return int(val)
    return False


def _token_values(tokens):
    """Map cleaned tokens to (index, value) pairs, joining the multiword
    and hyphenated hundred/thousand forms."""
    vals = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        two = f"{tok} {tokens[i + 1]}" if i + 1 < len(tokens) else None
        two_hyphen = f"{tok}-{tokens[i + 1]}" if i + 1 < len(tokens) else None
        if two and _normalize(two) in _WORDS:
            vals.append((i, 2, _WORDS[_normalize(two)]))
            i += 2
            continue
        if two_hyphen and _normalize(two_hyphen) in _WORDS:
            vals.append((i, 2, _WORDS[_normalize(two_hyphen)]))
            i += 2
            continue
        if _normalize(tok) in _WORDS:
            vals.append((i, 1, _WORDS[_normalize(tok)]))
            i += 1
            continue
        vals.append((i, 1, None))
        i += 1
    return vals


def extract_number_kab(text: str, short_scale: bool = False,
                       ordinals: bool = False) -> Union[int, float, bool]:
    """Extract the first number from Kabyle text.

    Understands digits, both numeral systems (Amazigh and Arabic-derived),
    feminine forms, "u"/"d" joined compounds in either order
    ("waḥed u ɛecrin" = 21, "mraw d yiwen" = 11) and the fraction azgen.
    With ``ordinals=True``, wis/tis + cardinal and amezwaru return the
    ordinal value.
    """
    tokens = [t.strip(".,!?;:()\"'") for t in text.lower().split()]
    tokens = [t for t in tokens if t]

    # ordinals
    for i, tok in enumerate(tokens):
        norm = _normalize(tok)
        if ordinals:
            if norm in {_normalize(k) for k in _ORDINAL_FIRST}:
                return 1
            if norm in _ORDINAL_MARKERS and i + 1 < len(tokens):
                val = extract_number_kab(" ".join(tokens[i + 1:]))
                if val is not False:
                    return val

    parsed = _token_values(tokens)
    i = 0
    while i < len(parsed):
        idx, width, val = parsed[i]
        tok = tokens[idx]
        # digits
        m = re.fullmatch(r"-?\d+(?:[.,]\d+)?", tok)
        if m:
            num = m.group().replace(",", ".")
            return float(num) if "." in num else int(num)
        if val is None:
            i += 1
            continue
        # combine a run of number words joined directly or by u/d
        total_parts = [val]
        slots = {_slot(val)}
        j = i + 1
        while j < len(parsed):
            nidx, nwidth, nval = parsed[j]
            if nval is None:
                # connectors may join two number words
                if _normalize(tokens[nidx]) in _CONNECTORS \
                        and j + 1 < len(parsed) and parsed[j + 1][2] is not None:
                    j += 1
                    continue
                break
            nslot = _slot(nval)
            if nslot in slots:
                break
            total_parts.append(nval)
            slots.add(nslot)
            j += 1
        total = sum(total_parts)
        if isinstance(total, float) and total.is_integer():
            total = int(total)
        return total
    return False
