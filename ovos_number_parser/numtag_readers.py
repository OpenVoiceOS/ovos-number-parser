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
from functools import lru_cache
from typing import List, Optional, Union

from linguatag import closest_lang, is_arabic_variety, standardize_lang
from numtag import Form, Kind, NumberMention, tag_numbers
from numtag import Scale as NumtagScale

from ovos_number_parser.util import Scale

#: languages whose readers are numtag: every language numtag reads. The
#: numbers_xx.py modules hold the writers only
NUMTAG_LANGS = frozenset({
    "an", "ar", "ast", "az", "bg", "ca", "cs", "da",
    "de", "el", "en", "es", "et", "eu", "fa", "fi",
    "fr", "fy", "gl", "he", "hr", "hu", "id", "it",
    "kab", "ms", "mwl", "nb", "nl", "nn", "oc", "pl", "pt",
    "ro", "ru", "sk", "sl", "sv", "tr", "uk"})

#: languages whose numbers_to_digits writes the cardinal words of a fraction
#: in digits and keeps the fraction words ("dois e meio" is "2 e meio"); the
#: other languages write the value as a decimal ("one third" is
#: "0.3333333333333333")
_FRACTION_WORDS_KEPT = frozenset({"pt"})


def routed(lang: str) -> bool:
    """Whether numtag reads the numbers of ``lang``."""
    return isinstance(lang, str) and _base(lang) is not None


@lru_cache(maxsize=4096)
def _base(lang: str) -> Optional[str]:
    """The numtag language that ``lang`` names, or None."""
    lang = lang.strip()
    if is_arabic_variety(lang):
        return "ar"
    return closest_lang(standardize_lang(lang).partition("-")[0], sorted(NUMTAG_LANGS))


def _numtag_lang(lang: str) -> str:
    """The tag numtag reads: "pt-BR" stays, "no" is "nb"."""
    if is_arabic_variety(lang.strip()):
        return "ar"
    tag = standardize_lang(lang.strip())
    return tag if tag.partition("-")[0] in NUMTAG_LANGS else _base(lang)


def _scale(scale: Optional[Scale], short_scale: Optional[bool]) -> Optional[NumtagScale]:
    """The scale the caller asked for; None leaves the language's own."""
    if scale is not None:
        return NumtagScale(Scale(scale).value)
    if short_scale is not None:
        return NumtagScale.SHORT if short_scale else NumtagScale.LONG
    return None


#: digits of other scripts, read as the digits they write ("١" is 1)
_WESTERN_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "0123456789" * 2)
#: the same digits and the Arabic decimal separator, as numbers_to_digits
#: writes them ("١٢٫٥" is "12.5")
_WRITTEN_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹٫", "0123456789" * 2 + ".")
#: a German clock time written with a point, as speech to text writes it
#: ("13.30 Uhr"); numbers_to_digits writes it with a colon
_DE_CLOCK = re.compile(r"\b([01]?[0-9]|2[0-4])\.([0-5][0-9]?)(?=\s+(?:uhr|pm|a\.m\.|p\.m\.)(?!\w))",
                       re.IGNORECASE)
#: an underscore between two letters, which spells a space ("twenty_one")
_UNDERSCORE = re.compile(r"(?<=[^\W\d_])_(?=[^\W\d_])")


def _prepare(text: str) -> str:
    """``text`` with each character numtag does not read replaced by one it
    reads, so every offset stays the same."""
    return _UNDERSCORE.sub(" ", text.translate(_WESTERN_DIGITS))


def number(value: str, kind: Kind = Kind.DECIMAL) -> Optional[Union[int, float]]:
    """The ``int`` or ``float`` of a numtag value of ``kind``, or None when
    the value is an integer with more digits than ``str`` can write.

    A value that is no whole number is a ``float``. When the ``float`` has
    no room for the part after the point, or none for the value at all, a
    decimal rounds half up to an ``int``, and a mixed number within the
    range of a ``float`` ("9007199254740993 1/2") is its whole part, so the
    whole part keeps every digit.
    """
    whole = value.lstrip("-").split(".")[0].split("/")[0]
    if len(whole) > sys.get_int_max_str_digits() > 0:
        return None
    if "/" not in value and "." not in value:
        return int(value)
    try:
        exact = Fraction(value)
        approx = float(exact)
    except ValueError:
        return None
    except OverflowError:
        approx = math.inf
    if exact.denominator == 1 or (kind is Kind.FRACTION and approx.is_integer() and abs(exact) >= 1):
        return int(exact)
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
    return number(found[0].value, found[0].kind) if found else False


def _one(text: str, lang: str, scale: Optional[Scale], kind: Kind,
         short_scale: Optional[bool] = None) -> Optional[NumberMention]:
    """The number ``text`` is, when all of it is one number of ``kind``."""
    found = tag_numbers(_prepare(text), _numtag_lang(lang), scale=_scale(scale, short_scale))
    if len(found) == 1 and found[0].char_span == (0, len(text)) and found[0].kind is kind:
        return found[0]
    return None


def _answer(mention: Optional[NumberMention]) -> Union[int, float, bool]:
    """The value of ``mention``, or False."""
    value = number(mention.value, mention.kind) if mention else None
    return False if value is None else value


def is_fractional(text: str, lang: str, short_scale: Optional[bool] = None,
                  scale: Optional[Scale] = None) -> Union[float, bool]:
    """The value of ``text`` when all of it is one fraction, or False."""
    if not isinstance(text, str):
        return False
    return _answer(_one(text.strip(), lang, scale, Kind.FRACTION, short_scale))


def is_ordinal(text: str, lang: str) -> Union[int, bool]:
    """The value of ``text`` when all of it is one ordinal, or False."""
    if not isinstance(text, str):
        return False
    return _answer(_one(text.strip(), lang, None, Kind.ORDINAL))


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
    value = number(mention.value, mention.kind)
    if mention.kind is Kind.FRACTION and _base(lang) in _FRACTION_WORDS_KEPT \
            and Fraction(mention.value).denominator != 1:
        return _fraction_words(words, lang, scale)
    return str(value)


def numbers_to_digits(utterance: str, lang: str, scale: Optional[Scale] = None,
                      ordinals: bool = False) -> str:
    """``utterance`` with each number written in words put in digits.

    A number already in digits stays as written ("Version 2.0", "5 1/2",
    "007"), in Western digits ("٠٠٧" is "007"); with a sign word it is the
    digits of its value ("minus 5" is "-5"). An ordinal ("the sixth
    sense") stays as written too, unless ``ordinals`` is true: then it is the
    digits of its value ("the twenty-first of march" is "the 21 of march").
    In German a clock time written with a point is written with a colon
    ("um 13.30 Uhr" is "um 13:30 Uhr").
    """
    out, at = [], 0
    for mention in mentions(utterance, lang, ordinals=True, scale=scale):
        start, end = mention.char_span
        words = utterance[start:end]
        if mention.form is Form.DIGITS and not any(char.isalpha() for char in words):
            written = words.translate(_WRITTEN_DIGITS)
        elif mention.kind is Kind.ORDINAL and not ordinals:
            continue
        else:
            written = _digits(mention, words, lang, scale)
        out += [utterance[at:start], written]
        at = end
    out.append(utterance[at:])
    text = "".join(out)
    if _base(lang) == "de":
        text = _DE_CLOCK.sub(lambda m: f"{m[1]}:{m[2].ljust(2, '0')}", text)
    return text
