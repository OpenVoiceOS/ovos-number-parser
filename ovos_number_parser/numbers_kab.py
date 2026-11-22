"""Kabyle (Taqbaylit, ``kab``) number tools.

Kabyle has two numeral systems in active use:

- the pan-Amazigh (Berber) numerals, universally used for 1-10:
  yiwen, sin, kṛaḍ, kuẓ, semmus, sḍis, sa, tam, tẓa, mraw
- the Algerian-Arabic borrowed numerals, which carry everyday counting
  above ten: ḥḍac (11), ɛecrin (20), mya (100), alef (1000), joined with
  the conjunction "u" ("waḥed u ɛecrin" = 21, unit before ten)

A formalized pan-Amazigh numeral proposal is also supported for extraction. 
This system uses invariable tens ("snan", "kraḍan") and descending magnitudes 
without connectors ("sin igiman tam imda" = 2800). 

Pronunciation uses the Amazigh forms for 0-10 and the Arabic-derived
forms above ten (the conversational standard). Extraction accepts both systems, 
including feminine forms (yiwet, snat, ...) and additive Amazigh compounds.

Ordinals are formed with wis (masculine) / tis (feminine) + cardinal;
"first" is the adjective amezwaru / tamezwarut.

Sources:
- https://en.wikipedia.org/wiki/Kabyle_language (grammar & numeral notes)
- https://www.omniglot.com/language/numbers/kabyle.htm
- https://anzart.github.io/kab-new-num-system/ (formal Amazigh numeral proposal)
"""
from typing import Union

from ovos_number_parser import numtag_readers
from ovos_number_parser.util import GrammaticalGender, warn_reader_removed

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
_TEENS_LOAN = {11: "ḥḍac", 12: "tnac", 13: "telṭac", 14: "ṛbeɛṭac",
               15: "xemseṭṭac", 16: "seṭṭac", 17: "sbeɛṭac",
               18: "tmenṭac", 19: "tseɛṭac"}
_TENS_LOAN = {20: "ɛecrin", 30: "tlatin", 40: "ṛebɛin", 50: "xemsin",
              60: "settin", 70: "sebɛin", 80: "tmanyin", 90: "tesɛin"}
_HUNDREDS_LOAN = {100: "mya", 200: "mitin", 300: "telt-mya", 400: "ṛebɛ-mya",
                  500: "xems-mya", 600: "sett-mya", 700: "sebɛ-mya",
                  800: "temn-mya", 900: "tesɛ-mya"}
_THOUSANDS_LOAN = {1000: "alef", 2000: "juǧ alaf", 3000: "telt-alaf",
                   4000: "ṛebɛ-alaf", 5000: "xems-alaf", 6000: "sett-alaf",
                   7000: "sebɛ-alaf", 8000: "temn-alaf", 9000: "tesɛ-alaf"}


def _normalize(token: str) -> str:
    """Diacritic-tolerant lookup key (ṛ→r, ṭ→t, ḍ→d, ẓ→z, ḥ→h, ǧ→g)."""
    table = str.maketrans("ṛṭḍẓḥǧṣč", "rtdzhgsc")
    return token.lower().translate(table)


def pronounce_number_kab(number: Union[int, float], places: int = 3,
                         ordinals: bool = False,
                         gender: GrammaticalGender = GrammaticalGender.MASCULINE) -> str:
    """Pronounce a number in Kabyle (everyday counting system).

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


def extract_number_kab(text: str, short_scale: bool = False,
                       ordinals: bool = False) -> Union[int, float, bool]:
    """Deprecated: use ``ovos_number_parser.extract_number(text, "kab")``."""
    warn_reader_removed("extract_number_kab", 'ovos_number_parser.extract_number(text, "kab")')
    return numtag_readers.extract_number(text, "kab", short_scale, ordinals)


