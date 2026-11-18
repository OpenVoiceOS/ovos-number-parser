"""Read numbers in text through numtag, for the languages in ``NUMTAG_LANGS``.

numtag finds every number in a text with its exact value as a digit string
("1002", "-2.5", "1/3") and its character span. The readers here convert
each value once, at this boundary, to the ``int`` or ``float`` that the
public API returns. A value that ``str`` cannot write as an ``int`` is no
number, as ``extract_number`` rules for the other languages.
"""
import math
import re
import sys
from fractions import Fraction
from typing import List, Optional, Union

from numtag import Form, Kind, NumberMention, tag_numbers
from numtag import Scale as NumtagScale

from ovos_number_parser.util import Scale

#: languages whose readers are numtag: every language numtag reads. Every
#: other language keeps its numbers_xx.py reader
NUMTAG_LANGS = frozenset({
    "an", "ar", "ast", "az", "bg", "ca", "cs", "da",
    "de", "el", "en", "es", "et", "eu", "fa", "fi",
    "fr", "fy", "gl", "he", "hr", "hu", "id", "it",
    "kab", "mwl", "nb", "nl", "nn", "oc", "pl", "pt",
    "ro", "ru", "sk", "sl", "sv", "tr", "uk"})

#: languages whose numbers_to_digits writes the cardinal words of a fraction
#: in digits and keeps the fraction words ("dois e meio" is "2 e meio"); the
#: other languages write the value as a decimal ("one third" is
#: "0.3333333333333333")
_FRACTION_WORDS_KEPT = frozenset({"pt"})


#: language codes that name the language of another code ("no" is Norwegian
#: Bokmål, "azj" North Azerbaijani)
_ALIASES = {"no": "nb", "azj": "az", "ekk": "et", "pes": "fa"}


def routed(lang: str) -> bool:
    """Whether numtag reads the numbers of ``lang``."""
    return isinstance(lang, str) and _base(lang) in NUMTAG_LANGS


def _base(lang: str) -> str:
    base = lang.lower().replace("_", "-").split("-")[0]
    return _ALIASES.get(base, base)


def _numtag_lang(lang: str) -> str:
    """The tag numtag reads: "pt-BR" stays, "no" is "nb"."""
    base = lang.lower().replace("_", "-").split("-")[0]
    return _ALIASES[base] if base in _ALIASES else lang


def _scale(scale: Optional[Scale], short_scale: Optional[bool]) -> Optional[NumtagScale]:
    """The scale the caller asked for; None leaves the language's own."""
    if scale is not None:
        return NumtagScale(Scale(scale).value)
    if short_scale is not None:
        return NumtagScale.SHORT if short_scale else NumtagScale.LONG
    return None


#: digits of other scripts, read as the digits they write ("١" is 1)
_WESTERN_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "0123456789" * 2)
#: an underscore between two letters, which spells a space ("twenty_one")
_UNDERSCORE = re.compile(r"(?<=[^\W\d_])_(?=[^\W\d_])")


def _prepare(text: str) -> str:
    """``text`` with each character numtag does not read replaced by one it
    reads, so every offset stays the same."""
    return _UNDERSCORE.sub(" ", text.translate(_WESTERN_DIGITS))


def number(value: str) -> Optional[Union[int, float]]:
    """The ``int`` or ``float`` of a numtag value, or None when the value
    is an integer with more digits than ``str`` can write.

    A value that is no whole number is a ``float``. When the ``float`` has
    no room left for the part after the point, or none for the value at all,
    the value rounds half up to an ``int``, so the whole part keeps its digits.
    """
    whole = value.lstrip("-").split(".")[0].split("/")[0]
    if len(whole) > sys.get_int_max_str_digits() > 0:
        return None
    if "/" not in value and "." not in value:
        return int(value)
    exact = Fraction(value)
    try:
        approx = float(exact)
    except OverflowError:
        approx = math.inf
    if approx.is_integer() or math.isinf(approx):
        rounded = (2 * abs(exact.numerator) + exact.denominator) // (2 * exact.denominator)
        return -rounded if exact < 0 else rounded
    return approx


def mentions(text: str, lang: str, short_scale: Optional[bool] = None,
             ordinals: bool = False, scale: Optional[Scale] = None) -> List[NumberMention]:
    """The numbers in ``text`` that the API reads: no ordinal unless asked
    for, and no value that ``str`` cannot write."""
    if not isinstance(text, str):
        return []
    return [m for m in tag_numbers(_prepare(text), _numtag_lang(lang), scale=_scale(scale, short_scale))
            if (ordinals or m.kind is not Kind.ORDINAL) and number(m.value) is not None]


def extract_number(text: str, lang: str, short_scale: Optional[bool] = None,
                   ordinals: bool = False,
                   scale: Optional[Scale] = None) -> Union[int, float, bool]:
    """The value of the first number in ``text``, or False."""
    found = mentions(text, lang, short_scale, ordinals, scale)
    return number(found[0].value) if found else False


def _one(text: str, lang: str, scale: Optional[Scale], kind: Kind) -> Optional[NumberMention]:
    """The number ``text`` is, when all of it is one number of ``kind``."""
    found = tag_numbers(_prepare(text), _numtag_lang(lang), scale=_scale(scale, None))
    if len(found) == 1 and found[0].char_span == (0, len(text)) and found[0].kind is kind:
        return found[0]
    return None


def _fraction_words(text: str, lang: str, scale: Optional[Scale]) -> str:
    """The words of a fraction with each count in digits and each fraction
    word kept: "dois e meio" is "2 e meio", "dois milhões e um quarto" is
    "2000000 e 1 quarto", "doze vinte e cinco avos" is "12 25 avos"."""
    head, joiner, tail = text.rpartition(" e ")
    if joiner and _one(tail, lang, scale, Kind.FRACTION):
        return numbers_to_digits(head, lang, scale) + joiner + _fraction_words(tail, lang, scale)
    words, out, at = text.split(" "), [], 0
    while at < len(words):
        for end in range(len(words), at, -1):
            count = _one(" ".join(words[at:end]), lang, scale, Kind.CARDINAL)
            if count:
                out.append(count.value)
                at = end
                break
        else:
            out.append(words[at])
            at += 1
    return " ".join(out)


def _digits(mention: NumberMention, words: str, lang: str, scale: Optional[Scale]) -> str:
    """How numbers_to_digits writes one number, written as ``words``."""
    if mention.kind is Kind.FRACTION and _base(lang) in _FRACTION_WORDS_KEPT \
            and Fraction(mention.value).denominator != 1:
        return _fraction_words(words, lang, scale)
    return str(number(mention.value))


def numbers_to_digits(utterance: str, lang: str, scale: Optional[Scale] = None,
                      ordinals: bool = False) -> str:
    """``utterance`` with each number written in words put in digits.

    A number already in digits stays as written ("Version 2.0"). An ordinal
    ("the sixth sense") stays as written too, unless ``ordinals`` is true:
    then it is the digits of its value ("the twenty-first of march" is "the
    21 of march").
    """
    out, at = [], 0
    for mention in mentions(utterance, lang, ordinals=True, scale=scale):
        if mention.form is Form.DIGITS or (mention.kind is Kind.ORDINAL and not ordinals):
            continue
        start, end = mention.char_span
        out += [utterance[at:start], _digits(mention, utterance[start:end], lang, scale)]
        at = end
    out.append(utterance[at:])
    return "".join(out)
