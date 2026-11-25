import math
import re
import sys
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from fractions import Fraction
from numbers import Real
from os.path import commonprefix
from functools import lru_cache
from typing import List
from typing import Optional
from typing import Union

from linguatag import closest_lang, default_region, is_arabic_variety, standardize_lang
from unicode_rbnf import RbnfEngine, FormatPurpose

from ovos_number_parser.numbers_ast import AST
from ovos_number_parser.numbers_an import AN
from ovos_number_parser.numbers_ar import (pronounce_number_ar, pronounce_ordinal_ar, nice_number_ar, resolve_ar_lang, resolve_ar_lect)
from ovos_number_parser.numbers_az import pronounce_number_az
from ovos_number_parser.numbers_bg import pronounce_number_bg, nice_number_bg
from ovos_number_parser.numbers_ca import pronounce_number_ca, CA
from ovos_number_parser.numbers_cs import pronounce_number_cs, pronounce_ordinal_cs
from ovos_number_parser.numbers_da import pronounce_number_da, pronounce_ordinal_da
from ovos_number_parser.numbers_de import pronounce_number_de, pronounce_ordinal_de
from ovos_number_parser.numbers_en import pronounce_number_en
from ovos_number_parser.numbers_el import pronounce_number_el, pronounce_ordinal_el
from ovos_number_parser.numbers_es import pronounce_number_es, fraction_noun_es, ES
from ovos_number_parser.numbers_eu import pronounce_number_eu, pronounce_ordinal_eu
from ovos_number_parser.numbers_et import pronounce_number_et, pronounce_ordinal_et, nice_number_et
from ovos_number_parser.numbers_fa import pronounce_number_fa, pronounce_ordinal_fa
from ovos_number_parser.numbers_fi import pronounce_number_fi, pronounce_ordinal_fi, nice_number_fi
from ovos_number_parser.numbers_fr import FR, FR_BE, FR_CH
from ovos_number_parser.numbers_fy import pronounce_number_fy, pronounce_ordinal_fy, nice_number_fy
from ovos_number_parser.numbers_gl import GL, pronounce_number_gl, pronounce_ordinal_gl, pronounce_fraction_gl
from ovos_number_parser.numbers_hr import pronounce_number_hr, pronounce_ordinal_hr, nice_number_hr
from ovos_number_parser.numbers_he import pronounce_number_he, pronounce_ordinal_he, nice_number_he
from ovos_number_parser.numbers_hu import (pronounce_number_hu, pronounce_ordinal_hu, nice_number_hu, pronounce_scientific_hu)
from ovos_number_parser.numbers_id import (pronounce_number_id, pronounce_number_ms, pronounce_ordinal_id, pronounce_ordinal_ms, nice_number_id, nice_number_ms)
from ovos_number_parser.numbers_it import pronounce_number_it, pronounce_ordinal_it, IT
from ovos_number_parser.numbers_kab import pronounce_number_kab, pronounce_ordinal_kab
from ovos_number_parser.numbers_mwl import MWL
from ovos_number_parser.numbers_oc import OC
from ovos_number_parser.numbers_nb import nice_number_nb, pronounce_number_nb, pronounce_ordinal_nb
from ovos_number_parser.numbers_nn import nice_number_nn, pronounce_number_nn, pronounce_ordinal_nn
from ovos_number_parser.numbers_nl import pronounce_number_nl, pronounce_ordinal_nl
from ovos_number_parser.numbers_pl import pronounce_number_pl, pronounce_ordinal_pl
from ovos_number_parser.numbers_pt import PortugueseVariant, PT_PT, PT_BR
from ovos_number_parser.numbers_ro import RO
from ovos_number_parser.numbers_ru import pronounce_number_ru, _ordinal_ru
from ovos_number_parser.numbers_sk import pronounce_number_sk, pronounce_ordinal_sk, nice_number_sk
from ovos_number_parser.numbers_sl import pronounce_number_sl, nice_number_sl
from ovos_number_parser.numbers_sv import pronounce_number_sv, pronounce_ordinal_sv
from ovos_number_parser.numbers_tr import pronounce_number_tr, pronounce_ordinal_tr, nice_number_tr
from ovos_number_parser.numbers_uk import pronounce_number_uk, pronounce_ordinal_uk
from ovos_number_parser.numbers_az import nice_number_az
from ovos_number_parser.numbers_ca import nice_number_ca
from ovos_number_parser.numbers_cs import nice_number_cs
from ovos_number_parser.numbers_da import nice_number_da
from ovos_number_parser.numbers_de import nice_number_de
from ovos_number_parser.numbers_el import nice_number_el
from ovos_number_parser.numbers_es import nice_number_es
from ovos_number_parser.numbers_eu import nice_number_eu
from ovos_number_parser.numbers_fa import nice_number_fa
from ovos_number_parser.numbers_fr import nice_number_fr
from ovos_number_parser.numbers_it import nice_number_it
from ovos_number_parser.numbers_nl import nice_number_nl
from ovos_number_parser.numbers_pl import nice_number_pl
from ovos_number_parser.numbers_ru import nice_number_ru
from ovos_number_parser.numbers_sv import nice_number_sv
from ovos_number_parser.numbers_uk import nice_number_uk
from ovos_number_parser.util import Scale, GrammaticalGender, DigitPronunciation, \
    scientific_parts, round_half_up
from ovos_number_parser import numtag_readers


# --- canonical short/long scale convention per language --------------------
#
# Short scale: 10^9 = "billion", 10^12 = "trillion".
# Long scale:  10^9 = "thousand million / milliard", 10^12 = "billion".
# Getting the default wrong mis-scales every number >= 10^9 by 1000x.
#
# The convention each language uses is a fixed property of that language, not a
# caller preference, so a caller that passes no ``scale=`` must get the
# language's canonical convention. Sources: Wikipedia "Long and short scales"
# (https://en.wikipedia.org/wiki/Long_and_short_scales), which tabulates the
# convention per country/language and cites the national language academies,
# cross-referenced with those academies where they legislate cardinal-numeral
# spelling (e.g. Euskaltzaindia Araua 7 for Basque, which makes Basque long
# scale: 10^9 = "mila milioi", "bilioi" = 10^12).
#
# Languages absent from this set default to the short scale (en, ru, uk, bg,
# el, tr, id, ms, az, ...), matching their modern standard usage.
_LONG_SCALE_LANGS = {
    "de", "fr", "es", "it", "nl", "pl", "sv", "da", "nb", "nn",
    "gl", "ca", "eu", "cs", "sl", "sk", "hr", "hu", "fi", "et", "ro",
    "ast", "oc", "an", "mwl", "fy",
}


def _resolve_scale(lang: str,
                   scale: Optional[Scale],
                   short_scale: Optional[bool] = None) -> Scale:
    """An explicit ``scale`` wins, then the deprecated ``short_scale`` flag,
    then the language's convention. European Portuguese is long scale and
    Brazilian Portuguese short scale, so ``pt`` is resolved by region."""
    if scale is not None:
        return scale
    if short_scale is not None:
        return Scale.SHORT if short_scale else Scale.LONG
    lang2 = _base_lang(lang)
    if lang2 == "pt":
        return Scale.SHORT if _is_brazilian(lang) else Scale.LONG
    return Scale.LONG if lang2 in _LONG_SCALE_LANGS else Scale.SHORT


# --- generic language fallbacks -------------------------------------------

_NICE_NUMBER_FNS = {
    "ar": nice_number_ar, "az": nice_number_az, "bg": nice_number_bg,
    "ca": nice_number_ca, "cs": nice_number_cs,
    "da": nice_number_da, "de": nice_number_de, "el": nice_number_el,
    "es": nice_number_es,
    "et": nice_number_et, "eu": nice_number_eu, "fa": nice_number_fa,
    "fi": nice_number_fi, "fr": nice_number_fr, "fy": nice_number_fy,
    "he": nice_number_he, "hr": nice_number_hr,
    "hu": nice_number_hu, "id": nice_number_id, "it": nice_number_it,
    "ms": nice_number_ms, "nb": nice_number_nb, "nl": nice_number_nl,
    "nn": nice_number_nn,
    "pl": nice_number_pl, "ru": nice_number_ru, "sk": nice_number_sk, "sl": nice_number_sl,
    "sv": nice_number_sv, "tr": nice_number_tr,
    "uk": nice_number_uk,
}

# fraction nouns take feminine numerals in the Slavic languages and the
# "két" allomorph in Hungarian
_FRACTION_NUMERATOR_OVERRIDES = {
    "bg": {1: "една", 2: "две"},
    "ru": {1: "одна", 2: "две"},
    "uk": {1: "одна", 2: "дві"},
    "cs": {1: "jedna", 2: "dvě"},
    "hr": {2: "dvije"},
    "sk": {1: "jedna", 2: "dve"},
    "pl": {1: "jedna", 2: "dwie"},
    "hu": {2: "két"},
}


def _pronounce_fraction_generic(fraction_word: str, lang: str) -> str:
    """Fallback pronunciation of a "n/m" fraction string.

    Uses the language's nice_number fraction wording where available (which
    carries the language's own plural/declension logic), spelling out any
    digits it leaves behind. Denominators outside the language's fraction
    vocabulary fall back to "<cardinal numerator> <ordinal denominator>".
    """
    n1_str, n2_str = fraction_word.split("/")
    n1, n2 = int(n1_str), int(n2_str)
    if n2 == 0:
        raise ZeroDivisionError(f"denominator is zero: {fraction_word}")
    negative = (n1 < 0) ^ (n2 < 0)
    n1, n2 = abs(n1), abs(n2)
    lang2 = _base_lang(lang)

    result = None
    if lang2 == "en":
        if n2 == 2:
            denom = "half" if n1 == 1 else "halves"
        elif n2 == 4:
            denom = "quarter" if n1 == 1 else "quarters"
        else:
            denom = pronounce_ordinal(n2, lang)
            if n1 != 1:
                denom += "s"
        result = f"{pronounce_number(n1, lang)} {denom}"
    else:
        nice_fn = _NICE_NUMBER_FNS.get(lang2) or \
            (nice_number_ar if _is_arabic(lang) else None)
        if nice_fn and 2 <= n2 <= 20:
            spoken = nice_fn(n1 / n2, speech=True, denominators=[n2])
            tokens = spoken.split()
            if "/" not in spoken and \
                    not all(t.replace(",", "").replace(".", "").isdecimal() for t in tokens):
                overrides = _FRACTION_NUMERATOR_OVERRIDES.get(lang2, {})
                result = " ".join(
                    overrides.get(int(t), pronounce_number(int(t), lang))
                    if t.isdecimal() else t
                    for t in tokens)

    if result is None and lang2 == "es" and n2 > 1:
        try:
            noun = fraction_noun_es(n2, plural=n1 != 1)
        except OverflowError:  # no reading for the denominator
            noun = None
        if noun:
            # the noun is masculine: "un veintiunavo", "veintiún cincuentavos"
            count = pronounce_number(n1, lang, gender=GrammaticalGender.NEUTRAL)
            result = f"{count} {noun}"
    if result is None:
        # approximate: cardinal numerator + ordinal denominator
        result = f"{pronounce_number(n1, lang)} {pronounce_ordinal(n2, lang)}"
    if negative:
        spoken = pronounce_number(-1, lang)
        minus = spoken.split()[0] if " " in spoken else ""
        result = f"{minus} {result}" if minus else f"-{result}"
    return result


_ORDINAL_REVERSE_CACHE = {}


def _ordinal_reverse_table(lang: str) -> dict:
    """Spoken ordinal -> value for ``lang``, built from pronounce_ordinal.

    A tag with a region or script subtag also knows the forms of its bare
    language, so "fr-BE" reads "soixante-dixième" as well as the
    "septantième" it speaks.
    """
    if lang not in _ORDINAL_REVERSE_CACHE:
        table = {}
        candidates = list(range(1, 101)) + \
            [n * 100 for n in range(2, 11)] + [1000, 1000000]
        for n in candidates:
            try:
                word = pronounce_ordinal(n, lang).lower()
            except Exception:
                break
            table[word] = n
            # register the opposite grammatical gender for languages that
            # mark it with a final -o/-a vowel
            if word.endswith("a"):
                table.setdefault(word[:-1] + "o", n)
            elif word.endswith("o"):
                table.setdefault(word[:-1] + "a", n)
        base = _base_lang(lang)
        if base == "fr":
            # French speaks its own ordinals and still reads the CLDR RBNF
            # forms ("quatre-vingt-et-unième" beside "quatre-vingt-unième")
            for n in candidates:
                word = _pronounce_rbnf(n, lang, True, GrammaticalGender.MASCULINE)
                table.setdefault(word.lower(), n)
        if base != lang:
            for word, n in _ordinal_reverse_table(base).items():
                table.setdefault(word, n)
        _ORDINAL_REVERSE_CACHE[lang] = table
    return _ORDINAL_REVERSE_CACHE[lang]


def numbers_to_digits(utterance: str, lang: str, scale: Optional[Scale] = None) -> str:
    """Replace the written numbers in ``utterance`` with digits. A language numtag does not read returns the text unchanged."""
    if numtag_readers.routed(lang):
        return numtag_readers.numbers_to_digits(utterance, lang, scale)
    return utterance


# Connectives for the a+bi complex form, per language, English as the default.
# The imaginary unit is spoken "i" following ISO 80000-2 (item 2-13.1), which
# fixes i as the symbol for sqrt(-1) in the rectangular form a + bi.
_COMPLEX_CONNECTIVES = {
    "en": ("plus", "minus", "i"),
    "ru": ("плюс", "минус", "и"),
    "de": ("plus", "minus", "i"),
}


def _pronounce_complex(number: complex, lang: str, places: int,
                       scale: Optional[Scale], digits, gender) -> str:
    """Speak a complex number in rectangular a+bi form (ISO 80000-2).

    Composed from the real pronunciation so it works in every language; only
    the "plus"/"minus"/"i" connectives are language-specific (English default).
    """
    plus_w, minus_w, i_w = _COMPLEX_CONNECTIVES.get(
        _base_lang(lang), _COMPLEX_CONNECTIVES["en"])

    def _speak(value):
        # collapse an integer-valued float ("3.0" -> "three") and -0.0 -> 0
        v = int(value) if value == int(value) else value
        return pronounce_number(v, lang, places=places, scale=scale,
                                digits=digits, gender=gender)

    imag = int(number.imag) if number.imag == int(number.imag) else number.imag
    if imag == 0:
        return _speak(number.real)

    magnitude = "" if abs(imag) == 1 else _speak(abs(imag)) + " "
    if number.real == 0:
        sign = "" if imag > 0 else minus_w + " "
        return f"{sign}{magnitude}{i_w}".strip()

    connective = plus_w if imag > 0 else minus_w
    return f"{_speak(number.real)} {connective} {magnitude}{i_w}"


#: By default CPython refuses ``str()`` of an int with more than 4300 digits
#: (``sys.int_info.default_max_str_digits``), and converting a value that long
#: to or from an int takes time that grows faster than its length. A magnitude
#: this large reads in the scientific form in every language, built from its
#: leading digits alone.
_READ_LIMIT = 10 ** 4300

#: the largest finite float, exactly; ``copy_abs()`` of a Decimal compares
#: with it without rounding to the context precision as ``abs()`` does
_FLOAT_MAX = Decimal(sys.float_info.max)


def _past_read_limit(number) -> bool:
    """
    Whether an int, Decimal or Fraction has more than 4300 integer digits.

    A Decimal is judged by the exponent of its leading digit: comparing it
    with the int ``_READ_LIMIT`` converts that 4301-digit int on every call.
    """
    if isinstance(number, Decimal):
        return number.is_finite() and bool(number) \
            and number.adjusted() >= 4300
    return isinstance(number, (int, Fraction)) \
        and not -_READ_LIMIT < number < _READ_LIMIT


def _from_other_real(number):
    """
    A ``numbers.Real`` that is not an int, float, Decimal or Fraction (numpy
    float32, numpy int64) as the Decimal its ``str()`` writes, so it reads as
    the float written with the same digits: ``str(numpy.float32(1.256))`` is
    "1.256", while its binary value is 1.25600004196...
    A value whose ``str()`` is not a decimal numeral becomes its float.
    Anything else is returned unchanged.
    """
    if isinstance(number, (int, float, Decimal, Fraction)) \
            or not isinstance(number, Real):
        return number
    try:
        return Decimal(str(number))
    except InvalidOperation:
        return float(number)


def _fraction_as_decimal(number: Fraction,
                         places: int) -> Union[int, Decimal]:
    """A Fraction as its int when it is integral, else as a Decimal.

    The Decimal holds two digits past each rounding ``pronounce_number``
    makes at ``places``: the decimals of a plain reading, the mantissa
    decimals of a scientific one and the first significant digit of a value
    below the quantum. Its last digit is made odd when the expansion goes
    on, so each rounding, half away from zero, rounds the Fraction exactly:
    1/3 at 2 places reads as 0.33, and 1/8 at 2 places as 0.13.
    """
    if number.denominator == 1:
        return number.numerator
    numerator, denominator = abs(number.numerator), number.denominator
    # the zeros after the decimal point before the first significant digit,
    # or more
    zeros = max(0, math.ceil((denominator.bit_length() - numerator.bit_length())
                             * math.log10(2)) + 1)
    shift = places + 2 + zeros
    kept, cut = divmod(numerator * 10 ** shift, denominator)
    return Decimal((int(number < 0),
                    Decimal(kept | bool(cut)).as_tuple().digits, -shift))


def _round_for_speech(number: Union[int, float, Decimal],
                      places: int) -> Union[int, float]:
    """Round a real number to ``places`` decimals, half away from zero (ISO 80000-1; NIST SP 811 B.7).

    The backends slice the decimal string, which truncates; rounding here lets
    each of them read a value already correct to ``places`` digits, and carries
    into the integer part (0.999999 at 2 places is 1). Integers and non-finite
    floats return unchanged, and -0.0 becomes 0.0. A non-zero value below the
    rounding quantum is left untouched, so its sub-quantum reading and sign
    survive. A finite Decimal reads as the int or float written with the same
    digits; one with more digits than a float holds reads as the nearest float.
    """
    if isinstance(number, Decimal):
        if number == number.to_integral_value() and (
                number.as_tuple().exponent >= 0 or float(number) != number):
            return int(number)
        exact, number = number, float(number)
        if not math.isfinite(number):
            # beyond the float range: the fraction is far below what is read
            return int(exact.to_integral_value(rounding=ROUND_HALF_UP))
    elif isinstance(number, float) and math.isfinite(number):
        exact = Decimal(str(number))
    else:
        return number
    if number == 0:
        # normalise -0.0 to 0.0 so no language speaks "minus zero"
        return 0.0
    if exact == exact.to_integral_value():
        # no fractional part to shorten; also avoids quantize overflow on very
        # large integer-valued floats (1e300)
        return number
    rounded = round_half_up(exact, places)
    if rounded == 0:
        # magnitude below the rounding quantum: hand the original value to the
        # backend so its sub-quantum reading and sign are preserved
        return number
    if rounded == rounded.to_integral_value():
        return int(rounded)
    return float(rounded)


# Words for positive / negative infinity, keyed by language prefix.
# Any language not listed falls back to the English default.
_INFINITY_WORDS = {
    "en": ("infinity", "negative infinity"),
    "es": ("infinito", "infinito negativo"),
    "pt": ("infinito", "infinito negativo"),
    "it": ("infinito", "meno infinito"),
    "fr": ("infini", "moins infini"),
    "de": ("unendlich", "minus unendlich"),
}


#: Spoken connective for a scientific reading, keyed by language prefix, as
#: "<mantissa> <connective> <exponent>". Languages absent from this table fall
#: back to English rather than to a crash; that is a known and deliberate
#: limitation, not a claim of coverage.
_SCIENTIFIC_WORDS = {
    "en": "times ten to the power of",
    "es": "por diez elevado a",
    "pt": "vezes dez elevado a",
    "it": "per dieci elevato alla",
    "fr": "fois dix puissance",
    "de": "mal zehn hoch",
    "nl": "maal tien tot de macht",
    "ca": "per deu elevat a",
    "gl": "veces dez elevado a",
    "ro": "ori zece la puterea",
    "da": "gange ti i",
    "sv": "gånger tio upphöjt till",
    "an": "por diez elevau a",
    "el": "επί δέκα στη δύναμη του",
    "he": "כפול עשר בחזקת",
    "id": "kali sepuluh pangkat",
    # the connective each backend speaks under scientific=True
    "az": "vurulsun on üstü",
    "bg": "по десет на степен",
    "cs": "krát deset na mocninu",
    "fa": "ضرب در ده به توان",
    "hr": "puta deset na",
    "pl": "razy dziesięć do potęgi",
    "ru": "на десять в степени",
    "sk": "krát desať na mocninu",
    "sl": "krat deset na",
    "tr": "çarpı on üzeri",
    "uk": "на десять у ступені",
    "ar": "في عشرة أس",
    "ms": "kali sepuluh pangkat",
}


#: the locales unicode_rbnf ships rules for: a bare language ("sr") or a
#: language with a script or region subtag ("sr_Latn", "zh_Hant", "de_CH")
_RBNF_LOCALES = frozenset(RbnfEngine.get_supported_languages())

#: the bare codes of the languages this module speaks or reads. A unicode_rbnf
#: code for a language that numtag names already ("no" for "nb") adds nothing.
#: The partition splits a unicode_rbnf locale id, not a user tag.
_SERVED_LANGS = sorted(numtag_readers.NUMTAG_LANGS | {
    language for language in (locale.partition("_")[0] for locale in _RBNF_LOCALES)
    if not closest_lang(language, sorted(numtag_readers.NUMTAG_LANGS), max_distance=1)})


@lru_cache(maxsize=4096)
def _base_lang(lang: str) -> str:
    """Bare code of the language ``lang`` names, as this module serves it:
    "pt-BR", "pt_BR" and "PT" are "pt" and "azj" is "az"."""
    language = standardize_lang(lang.strip()).partition("-")[0]
    return closest_lang(language, _SERVED_LANGS) or language


@lru_cache(maxsize=4096)
def _is_brazilian(lang: str) -> bool:
    return default_region(lang.strip()) == "BR"


@lru_cache(maxsize=4096)
def _is_arabic(lang: str) -> bool:
    return is_arabic_variety(lang.strip())


#: languages that read the decimal part one digit at a time by convention.
#: Everything else composes it. Keyed by bare language code.
_DEFAULT_DIGIT_PRONUNCIATION = {
    "es": DigitPronunciation.DIGIT_BY_DIGIT,
    "ca": DigitPronunciation.DIGIT_BY_DIGIT,
    "fr": DigitPronunciation.DIGIT_BY_DIGIT,
}


#: a run of digits this long in "spoken" output means a backend gave up and
#: handed back the numeral instead of reading it
_DIGIT_RUN = re.compile(r"\d{7,}")


def _has_padded_scale_words(spoken: str, lang: str) -> bool:
    """Whether a backend padded a magnitude by repeating its largest scale word.

    Some backends repeat the biggest scale word they know instead of raising
    ("trilioi trilioi trilioi"). No numeral repeats a scale word back to back.
    Digit words repeat legitimately in a scientific mantissa or a digit-by-digit
    decimal, so they do not count.
    """
    digit_words = {pronounce_number(digit, lang) for digit in range(10)}
    words = spoken.split()
    return any(a == b and a not in digit_words
               for a, b in zip(words, words[1:]))


def _has_unread_digits(spoken: str) -> bool:
    """Whether a backend gave up and returned the numeral instead of reading it."""
    return bool(_DIGIT_RUN.search(spoken))


def _pronounce_bignum_fallback(number: Union[int, float, Decimal, Fraction],
                               lang: str, places: int) -> str:
    """
    Spoken scientific reading for finite numbers a language's tables cannot
    name, computed from the decimal digits so it never leaves the float range.

    A language whose backend has a scientific mode reads the value in that
    mode, so the scientific form of one language has one wording. For any
    other language, mantissa, sign and exponent are pronounced by the target
    language. Only the connective joining them is looked up, and falls back
    to English for languages missing from _SCIENTIFIC_WORDS. Hungarian reads
    a negative exponent with its own words.

    Only the leading digits a rounding at ``places`` reads are computed, so
    a value past ``_READ_LIMIT`` never goes through ``str()`` of the whole
    number.
    """
    if not isinstance(number, Decimal):
        magnitude = abs(int(number))
        # bit_length() * log10(2) is the digit count to within one, so at
        # least places + 2 leading digits are kept
        cut = max(0, int(magnitude.bit_length() * math.log10(2)) - places - 3)
        number = Decimal((int(number < 0),
                          Decimal(magnitude // 10 ** cut).as_tuple().digits,
                          cut))
    if _has_scientific_mode(lang):
        scale = _resolve_scale(lang, None, None)
        return _pronounce_number_dispatch(
            number, lang, places, scale == Scale.SHORT, True, False,
            DigitPronunciation.FULL_NUMBER, GrammaticalGender.MASCULINE, scale)
    # the sign rides on the mantissa so each language speaks its own minus
    # word ("menos dois...") instead of an English prefix
    mantissa, exponent = scientific_parts(number, places)
    if _base_lang(lang) == "hu" and exponent < 0:
        return pronounce_scientific_hu(mantissa, exponent)
    mantissa_words = pronounce_number(mantissa, lang=lang, places=places)
    exponent_words = pronounce_number(exponent, lang=lang)
    connective = _SCIENTIFIC_WORDS.get("ar" if _is_arabic(lang) else _base_lang(lang),
                                       _SCIENTIFIC_WORDS["en"])
    return f"{mantissa_words} {connective} {exponent_words}"


#: languages whose backend reads ``scientific=True`` in a scientific form of
#: its own, keyed by bare language code; Arabic lects are matched by _is_arabic
_SCIENTIFIC_MODE = frozenset({
    "az", "bg", "cs", "el", "en", "fa", "he", "hr", "id", "it", "ms", "pl",
    "ru", "sk", "sl", "tr", "uk"})

#: a value below the quantum whose first significant digit lies further right
#: than this many decimals reads in scientific form: 10 ** -323 is the
#: smallest power of ten whose nine multiples a float holds digit for digit
_MOST_PLACES = 323


def _has_scientific_mode(lang: str) -> bool:
    """Whether the backend for ``lang`` honours ``scientific=True``."""
    return _is_arabic(lang) or _base_lang(lang) in _SCIENTIFIC_MODE


def _round_mantissa(number: Union[int, float, Decimal],
                    places: int) -> Union[int, float, Decimal]:
    """Round the scientific mantissa of ``number`` to ``places`` decimals.

    The mantissa rounds once, half away from zero, from the exact decimal
    digits, the same way as ``scientific_parts``: 12.3449 at 3 places is
    1.234 times ten. The rounded value comes back as an int when it has no
    fraction and as a float otherwise, so the backend reads the same mantissa
    again without a second rounding. A mantissa with more digits than a float
    holds reads as the nearest float, as a Decimal does in a plain reading.
    A value below the normal float range that a float cannot hold digit for
    digit comes back as a Decimal, which every backend with a scientific mode
    reads. An int has no fraction to round twice and comes back unchanged.
    """
    if isinstance(number, int):
        return number
    mantissa, exponent = scientific_parts(number, places)
    rounded = Decimal(str(mantissa)).scaleb(exponent)
    if rounded == rounded.to_integral_value():
        return int(rounded)
    value = float(rounded)
    if abs(value) >= sys.float_info.min or Decimal(repr(value)) == rounded:
        return value
    return rounded


def pronounce_number(number: Union[int, float], lang: str,
                     places: int = 3,
                     short_scale: Optional[bool] = None,  # DEPRECATED
                     scientific: bool = False,
                     ordinals: bool = False,
                     digits: Optional[DigitPronunciation] = None,
                     gender: GrammaticalGender = GrammaticalGender.MASCULINE,
                     scale: Optional[Scale] = None,
                     case: Optional[str] = None) -> str:
    """Return the spoken form of a number in ``lang``.

    ``places`` is the count of decimals read, rounded half away from zero.
    ``scientific`` reads a scientific form where the language has one, and
    ``ordinals`` reads an ordinal. ``scale`` overrides the language's short or long
    scale (``short_scale`` is deprecated). ``digits`` defaults to the language's
    way of reading decimals. ``case`` applies to Arabic only.

    A Decimal, Fraction or other ``numbers.Real`` reads as the value it writes. A
    number of more than 4300 integer digits reads in scientific form in every
    language except Kabyle, which raises OverflowError past 9999.

    Raises:
        ValueError: ``number`` is NaN, or negative in Kabyle.
        NotImplementedError: ``lang`` has no reading.
    """
    scale = _resolve_scale(lang, scale, short_scale)
    short_scale = scale == Scale.SHORT
    lang2 = _base_lang(lang)
    if isinstance(number, complex):
        return _pronounce_complex(number, lang, places, scale, digits, gender)
    number = _from_other_real(number)
    if isinstance(number, Decimal) and not number.is_finite():
        number = float("nan") if number.is_nan() else float(number)
    if isinstance(number, float) and number != number:
        raise ValueError("cannot pronounce NaN (not a number)")
    # Infinity is not tied to any named-scale table; handle it uniformly for
    # every language so no per-language path has to convert it to an integer.
    if isinstance(number, float) and math.isinf(number):
        pos, neg = _INFINITY_WORDS.get(lang2, _INFINITY_WORDS["en"])
        return neg if number < 0 else pos
    # How a language conventionally reads the digits after the decimal marker
    # is a property of the language, not of the caller: Spanish and Catalan
    # read them one by one ("tres coma uno cuatro") while Portuguese composes
    # them ("três vírgula catorze"). `digits=None` means "use the language's
    # convention"; an explicit value always wins.
    if digits is None:
        digits = _DEFAULT_DIGIT_PRONUNCIATION.get(
            lang2, DigitPronunciation.FULL_NUMBER)

    if _past_read_limit(number):
        if lang2 != "kab":
            return _pronounce_bignum_fallback(number, lang, places)
        # Kabyle reads up to 9999, and its backend raises for any int this
        # large without the cost of converting this one
        number = _READ_LIMIT if number > 0 else -_READ_LIMIT
    if isinstance(number, Fraction):
        number = _fraction_as_decimal(number, places)
    if scientific and _has_scientific_mode(lang):
        # places counts the mantissa decimals: round the mantissa once, from
        # the exact digits, and hand the backend the rounded value
        number = _round_mantissa(number, places)
    else:
        if isinstance(number, (float, Decimal)) and number:
            exact = Decimal(str(number))
            lead = exact.adjusted()
            if places <= 0 and not ordinals and abs(exact) < Decimal("0.5"):
                # rounds to zero, and the zero word alone takes no minus word
                number = 0
            elif places > 0 and abs(exact) < Decimal(5).scaleb(-places - 1):
                # rounds to zero at ``places``: read up to the first
                # significant digit, rounded half away from zero on the digits
                # after it
                if lead < -_MOST_PLACES:
                    return _pronounce_bignum_fallback(exact, lang, 0)
                exact = exact.quantize(Decimal(1).scaleb(lead), ROUND_HALF_UP)
                number, places = float(exact), -exact.adjusted()
        # Round to the spoken precision before dispatch so every backend
        # speaks a rounded value instead of a truncated one (see
        # _round_for_speech).
        number = _round_for_speech(number, places)
    if isinstance(number, float) and abs(number) >= 1e16:
        # Python writes a float this large in exponent form ("1e+22"). Read
        # the whole number of that shortest repr, the value the caller wrote,
        # rather than its binary expansion or the exponent string itself.
        number = int(Decimal(repr(float(number))))
    try:
        spoken = _pronounce_number_dispatch(
            number, lang, places, short_scale, scientific, ordinals,
            digits, gender, scale, case)
    except (IndexError, KeyError, OverflowError) as error:
        # A finite number overflowed a language's named-scale table. Kabyle
        # has a documented finite ceiling (raises above 9999), so keep that
        # contract; every other language falls back to a spoken scientific
        # reading rather than crashing. An index or key error on an
        # ordinary-magnitude number keeps its original error so genuine bugs
        # are not masked. An OverflowError from 10 ** 12 up is a whole part
        # past the largest scale compound (a million millions at the
        # smallest), read scientifically where the connective is localized.
        if lang2 != "kab" and (
                abs(number) >= 10 ** 15
                or (isinstance(error, OverflowError)
                    and abs(number) >= 10 ** 12
                    and lang2 in _SCIENTIFIC_WORDS)):
            return _pronounce_bignum_fallback(number, lang, places)
        raise
    # A backend that does not raise past its scale table returns padded or
    # unread output instead (see _is_spoken_reading). Only composed readings
    # of large numbers are checked: a digit-by-digit rendering repeats words
    # legitimately, and Kabyle's finite ceiling is a documented contract.
    if abs(number) >= 10 ** 15 and lang2 != "kab" and not scientific:
        # padded scale words are never a reading, so always replace them
        if (isinstance(number, int) or float(number).is_integer()) \
                and _has_padded_scale_words(spoken, lang):
            return _pronounce_bignum_fallback(number, lang, places)
        # a bare numeral is a legitimate fallback the TTS can read; only
        # improve on it where the scientific reading is fully localized
        if _has_unread_digits(spoken) and lang2 in _SCIENTIFIC_WORDS:
            return _pronounce_bignum_fallback(number, lang, places)
    return spoken


def _pronounce_number_dispatch(number, lang, places, short_scale, scientific,
                               ordinals, digits, gender, scale, case=None):
    lang2 = _base_lang(lang)
    if lang2 == "en":
        return pronounce_number_en(number, places, short_scale, scientific, ordinals)
    if lang2 == "az":
        return pronounce_number_az(number, places, short_scale, scientific, ordinals)
    if _is_arabic(lang):
        # a lect's default register applies to cardinals; an ordinal takes
        # the oblique only when the caller asks for it
        if case is None:
            case = "nominative" if ordinals else resolve_ar_lang(lang) or "nominative"
        return pronounce_number_ar(number, places, scientific, ordinals,
                                   case=case, lect=resolve_ar_lect(lang),
                                   gender=gender)
    if lang2 == "bg":
        return pronounce_number_bg(number, places, short_scale, scientific, ordinals)
    if lang2 == "ca":
        return CA.pronounce_number(number, places, scale, ordinals, digits, gender)
    if lang2 == "ast":
        return AST.pronounce_number(number, places, scale, ordinals, digits, gender)
    if lang2 == "oc":
        return OC.pronounce_number(number, places, scale, ordinals, digits, gender)
    if lang2 == "an":
        return AN.pronounce_number(number, places, scale, ordinals, digits, gender)
    if lang2 == "cs":
        return pronounce_number_cs(number, places, short_scale, scientific, ordinals,
                                   gender=gender)
    if lang2 == "da":
        return pronounce_number_da(number, places, short_scale, scientific, ordinals,
                                   gender=gender)
    if lang2 == "de":
        return pronounce_number_de(number, places, short_scale, scientific, ordinals,
                                   gender=gender)
    if lang2 == "gl":
        return GL.pronounce_number(number, places, scale, ordinals, digits, gender)
    if lang2 == "el":
        return pronounce_number_el(number, places, scientific, ordinals)
    if lang2 == "es":
        return ES.pronounce_number(number, places, scale, ordinals, digits, gender)
    if lang2 == "eu":
        return pronounce_number_eu(number, places)
    if lang2 == "et":
        return pronounce_number_et(number, places, short_scale, scientific, ordinals)
    if lang2 == "fa":
        return pronounce_number_fa(number, places, scientific, ordinals)
    if lang2 == "fi":
        return pronounce_number_fi(number, places, short_scale, scientific, ordinals)
    if lang2 == "fr":
        engine = {"fr_BE": FR_BE, "fr_CH": FR_CH}.get(_rbnf_locale(lang), FR)
        return engine.pronounce_number(number, places, scale, ordinals,
                                       digits, gender)
    if lang2 == "he":
        return pronounce_number_he(number, places, scientific, ordinals)
    if lang2 == "hr":
        return pronounce_number_hr(number, places, short_scale, scientific, ordinals)
    if lang2 == "hu":
        return pronounce_number_hu(number, places, short_scale, scientific, ordinals)
    if lang2 == "id":
        return pronounce_number_id(number, places, short_scale, scientific, ordinals)
    if lang2 == "ms":
        return pronounce_number_ms(number, places, short_scale, scientific, ordinals)
    if lang2 == "tr":
        return pronounce_number_tr(number, places, short_scale, scientific, ordinals)
    if lang2 == "it":
        # NOT routed through IT: the engine spaces the tens ("venti cinque")
        # where Italian elides them ("venticinque"). Legacy path until the
        # engine handles elision, so `digits` stays unused here.
        if ordinals and not scientific and number == int(number):
            return pronounce_ordinal_it(int(number), gender)
        return pronounce_number_it(number, places, short_scale, scientific,
                                   gender)
    if lang2 == "kab":
        return pronounce_number_kab(number, places, ordinals, gender)
    if lang2 == "fy":
        return pronounce_number_fy(number, places, short_scale, scientific, ordinals)
    if lang2 == "nn":
        return pronounce_number_nn(number, places, short_scale, scientific, ordinals)
    if lang2 == "nb":
        return pronounce_number_nb(number, places, short_scale, scientific, ordinals,
                                   gender=gender)
    if lang2 == "nl":
        return pronounce_number_nl(number, places, short_scale, scientific, ordinals)
    if lang2 == "pl":
        return pronounce_number_pl(number, places, short_scale, scientific, ordinals,
                                   gender=gender)
    if lang2 == "pt":
        if _is_brazilian(lang):
            return PT_BR.pronounce_number(number, places, scale, ordinals, digits, gender)
        return PT_PT.pronounce_number(number, places, scale, ordinals, digits, gender)
    if lang2 == "mwl":
        return MWL.pronounce_number(number, places, scale, ordinals, digits, gender)
    if lang2 == "ro":
        return RO.pronounce_number(number, places, scale, ordinals, digits, gender)
    if lang2 == "ru":
        return pronounce_number_ru(number, places, short_scale, scientific, ordinals,
                                   gender=gender)
    if lang2 == "sk":
        return pronounce_number_sk(number, places, short_scale, scientific, ordinals)
    if lang2 == "sl":
        return pronounce_number_sl(number, places, short_scale, scientific, ordinals)
    if lang2 == "sv":
        return pronounce_number_sv(number, places, short_scale, scientific, ordinals,
                                   gender=gender)
    if lang2 == "uk":
        return pronounce_number_uk(number, places, short_scale, scientific, ordinals,
                                   gender=gender)
    # fallback to unicode RBNF
    return _pronounce_rbnf(number, lang, ordinals, gender)


#: the word an ICU RBNF rule set name uses for each grammatical gender,
#: as in "spellout-ordinal-masculine" and "spellout-cardinal-neuter"
_RBNF_GENDER = {
    GrammaticalGender.MASCULINE: "masculine",
    GrammaticalGender.FEMININE: "feminine",
    GrammaticalGender.NEUTRAL: "neuter",
}

#: gendered rule sets whose CLDR data does not give the form the gender asks
#: for, so the language keeps the engine default for that gender:
#:
#: - bs cardinal feminine spells 1 as "jedinica", the noun for the digit; the
#:   feminine numeral is "jedna" (Wiktionary "jedan", Serbo-Croatian)
#: - lb ordinal feminine gives "éischter", the dative and independent form;
#:   after a determiner the feminine is "éischt" (Wiktionary "éischt", and the
#:   adjective table at Wiktionary "grouss")
_RBNF_UNUSABLE = {
    ("bs", "spellout-cardinal-feminine"),
    ("lb", "spellout-ordinal-feminine"),
}

#: gendered rule sets used only where their output is the engine default with
#: one word swapped, mapped to that swap: the mt cardinal feminine set holds
#: the forms before a noun ("tliet", "ħdax-il"), and only "waħda", the
#: feminine of "wieħed" (Wiktionary "wieħed"), inflects for gender
_RBNF_WORD_SWAP_ONLY = {
    ("mt", "spellout-cardinal-feminine"): ("wieħed", "waħda"),
}

#: words the CLDR data misspells, with the Wiktionary form. Belarusian: the
#: ordinals of en.wiktionary "Module:number list/data/be" ("трэці",
#: "чацвёрты", "пяцідзясяты", "шасцідзесяты", "сямідзясяты", "двухсоты",
#: "шасцісоты"); the feminine in -ая and the neuter in -ае follow the
#: Wiktionary declension tables of "трэці", "чацвёрты", "пяцідзясяты",
#: "двухсоты" and "шасцісоты"
_RBNF_WORD_FIXES = {
    "be": {
        "трэйці": "трэці", "трэццяя": "трэцяя", "трэццяе": "трэцяе",
        "чацьверты": "чацвёрты", "чацьвертая": "чацвёртая",
        "чацьвертае": "чацвёртае",
        "пяцідзесятая": "пяцідзясятая", "пяцьдзесятае": "пяцідзясятае",
        "шэсцьдзесяты": "шасцідзесяты", "шэсцідзесятая": "шасцідзесятая",
        "шэсцідзясятае": "шасцідзесятае",
        "семдзесяты": "сямідзясяты", "семдзесятая": "сямідзясятая",
        "сямдзясятае": "сямідзясятае",
        "дзвухсоты": "двухсоты", "дзвухсотая": "двухсотая",
        "дзвухсотае": "двухсотае",
        "шасьцісоты": "шасцісоты", "шасьцісотая": "шасцісотая",
        "шасьцісотае": "шасцісотае",
    },
}

#: words the CLDR data writes in the script of another language, with the
#: word of the language. The wrong script never occurs in a correct reading,
#: so each word is replaced wherever it occurs, also inside the fraction
#: digits a rule set writes with no separator. Lao: the rule sets keep the
#: Thai words for zero, minus, the decimal point, the scale words and the
#: ordinal prefix
_RBNF_SCRIPT_FIXES = {
    "lo": {
        "ศูนย์": "ສູນ", "ลบ": "ລົບ", "จุด": "ຈຸດ", "ร้อย": "ຮ້ອຍ",
        "พัน": "ພັນ", "หมื่น": "ໝື່ນ", "แสน": "ແສນ", "ล้าน": "ລ້ານ",
        "ที่": "ທີ່",
    },
}

#: the rule set ``spellout-numbering`` reads through, for languages where the
#: engine cannot use it for a fraction (``spellout-numbering`` has no "x.x"
#: rule) and takes the shortest rule set name instead: the cy feminine set
#: ("dwy") or the mt set of the forms before a noun ("tnax-il"), not the
#: counting form. The fraction digits are read with this set in every gender;
#: the whole part reads as the integer does for the gender
_RBNF_COUNTING = {
    "cy": "spellout-cardinal-masculine",
    "mt": "spellout-cardinal-type-b-masculine",
}

#: the decimal-point word and the rule set of languages whose "x.x" rule reads
#: the fraction as a numerator over a power of ten ("он екі бүтін жүзден
#: жиырма бес", twelve and twenty-five hundredths); the engine reads that rule
#: set digit by digit and gets "оннан нөл" for every digit. The rule set has
#: words up to hundred billionths, so a longer fraction is rounded to that
_RBNF_FRACTIONS = {
    "kk": ("бүтін", "fractions"),
    "ky": ("бүтүн", "z-spellout-fraction"),
}


#: characters the CLDR data writes in place of rule syntax, removed from every
#: reading of the locale. The sr_Latn ordinal rules open with "‘" (U+2018)
#: where sr has the ASCII apostrophe that makes the space after it part of the
#: text, so "dvadeset‘ i prvi" is "dvadeset i prvi". The "‘" follows any
#: hundreds word ("sto‘", "dvadesetsto‘", "hiljadusto‘"), so no word list
#: covers it.
_RBNF_CHARACTER_FIXES = {
    "sr_Latn": str.maketrans("", "", "\u2018"),
}


#: Building an engine parses the locale's rule file, so each locale builds one.
_rbnf_engine = lru_cache(maxsize=None)(RbnfEngine.for_language)

@lru_cache(maxsize=4096)
def _rbnf_locale(lang: str) -> str:
    """The unicode_rbnf locale that reads ``lang``.

    A script or region subtag selects its own rules where unicode_rbnf ships
    them, in either separator and any letter case ("sr-Latn", "sr_latn"); any
    other tag reads with the rules of its bare language.
    """
    return closest_lang(lang.strip(), sorted(_RBNF_LOCALES), max_distance=0) or _base_lang(lang)


def _pronounce_rbnf(number, lang, ordinals, gender):
    """Speak ``number`` with the Unicode RBNF rule set for ``gender``.

    ``FormatResult.text`` is the output of the shortest rule set name
    (``unicode_rbnf.engine.FormatResult``), so the gender is selected by name.
    A language with no rule set for the gender keeps the engine default. A
    masculine cardinal also keeps it: the default ``spellout-numbering`` is the
    counting form, and the Maltese and Venetian masculine sets are the forms
    before a noun ("żewġ", "du") and not the bare number ("tnejn", "do").
    Where the engine cannot read a fraction with ``spellout-numbering``,
    ``_RBNF_COUNTING`` names the rule set it reads through.

    A negative cardinal with a fraction is read as its magnitude with the
    minus word of the same rule set. The minus word is the reading of -1
    less the reading of 1, so it keeps the side and the spacing the rule set
    gives it. A language whose reading of -1 does not hold the reading of 1
    keeps the engine reading.

    A positive fraction in a language of ``_RBNF_FRACTIONS`` is read as the
    whole part, the decimal-point word, and the fraction digits as one number
    after the word for their power of ten. That word is the reading of the
    power of ten in the fraction rule set less the reading of 1. The fraction
    is first rounded half up to the longest power of ten the rule set has a
    word for; a fraction that rounds to zero reads as its whole part.

    A positive fraction in a language of ``_RBNF_COUNTING`` is read as the
    whole part for ``gender``, then the rest of the counting reading.

    The engine splits a fraction from ``str(Decimal)``, which writes a value
    below 1e-6 as "1E-7" and has no "." to split on. Such a value is read with
    five zeros after the point, and the zero that the reading with four zeros
    lacks is repeated for every further zero.
    """
    if (not ordinals and math.isfinite(number) and number < 0
            and number != int(number)):
        minus_one = _pronounce_rbnf(-1, lang, False, gender)
        one = _pronounce_rbnf(1, lang, False, gender)
        magnitude = _pronounce_rbnf(-number, lang, False, gender)
        if minus_one.endswith(one):
            return minus_one[:-len(one)] + magnitude
        if minus_one.startswith(one):
            return magnitude + minus_one[len(one):]
    if (not ordinals and math.isfinite(number) and 0 < number < 1e-6
            and _base_lang(lang) not in _RBNF_FRACTIONS):
        zeros = -Decimal(str(number)).adjusted() - 1
        significant = f"{Decimal(str(number)):f}".lstrip("0.")
        longer = _pronounce_rbnf(Decimal("0.00000" + significant), lang,
                                 False, gender)
        shorter = _pronounce_rbnf(Decimal("0.0000" + significant), lang,
                                  False, gender)
        cut = len(commonprefix([longer, shorter]))
        zero = longer[cut:cut + len(longer) - len(shorter)]
        return longer[:cut] + zero * (zeros - 5) + longer[cut:]
    form = FormatPurpose.ORDINAL if ordinals else FormatPurpose.CARDINAL
    base = _base_lang(lang)
    locale = _rbnf_locale(lang)
    try:
        engine = _rbnf_engine(locale)
        if (base in _RBNF_FRACTIONS and not ordinals and math.isfinite(number)
                and number > 0 and number != int(number)):
            point, fraction_set = _RBNF_FRACTIONS[base]
            one = _pronounce_rbnf(1, lang, False, gender)
            denominators = {}
            for value in engine.rulesets[fraction_set].numeric_rules:
                reading = engine.format_number(value, ruleset_names=[fraction_set]).text
                if reading.endswith(one):
                    denominators[len(str(value)) - 1] = reading[:-len(one)]
            rounded = Decimal(str(number)).quantize(
                Decimal(10) ** -max(denominators), ROUND_HALF_UP).normalize()
            whole, _, digits = f"{rounded:f}".partition(".")
            if not digits:
                return _pronounce_rbnf(int(whole), lang, False, gender)
            if len(digits) in denominators:
                return " ".join([_pronounce_rbnf(int(whole), lang, False, gender),
                                 point, denominators[len(digits)]
                                 + _pronounce_rbnf(int(digits), lang, False, gender)])
        if (base in _RBNF_COUNTING and not ordinals and math.isfinite(number)
                and number > 0 and number != int(number)):
            counting = [_RBNF_COUNTING[base]]
            whole = int(number)
            text = engine.format_number(number, ruleset_names=counting).text
            whole_text = engine.format_number(whole, ruleset_names=counting).text
            if text.startswith(whole_text + " "):
                return _pronounce_rbnf(whole, lang, False, gender) + text[len(whole_text):]
        ruleset = f"spellout-{form.name.lower()}-{_RBNF_GENDER.get(gender)}"
        if ruleset in engine.rulesets and (locale, ruleset) not in _RBNF_UNUSABLE \
                and (ordinals or gender != GrammaticalGender.MASCULINE):
            text = engine.format_number(number, ruleset_names=[ruleset]).text
            swap = _RBNF_WORD_SWAP_ONLY.get((locale, ruleset))
            if swap is not None:
                default = engine.format_number(number, form).text
                pairs = list(zip(default.split(" "), text.split(" ")))
                if default.count(" ") != text.count(" ") or \
                        not all(a == b or (a, b) == swap for a, b in pairs):
                    text = default
        else:
            text = engine.format_number(number, form).text
    except Exception as err:
        raise NotImplementedError(f"Unsupported language: '{lang}'") from err
    if ordinals and any(char.isdigit() for char in text):
        raise NotImplementedError(
            f"'{lang}' has no spoken ordinal for {number}")
    text = text.translate(_RBNF_CHARACTER_FIXES.get(locale, {}))
    for wrong, right in _RBNF_SCRIPT_FIXES.get(base, {}).items():
        text = text.replace(wrong, right)
    fixes = _RBNF_WORD_FIXES.get(locale, {})
    return " ".join(fixes.get(word, word) for word in text.split(" "))


def pronounce_fraction(fraction_word: str, lang: str, scale: Optional[Scale] = None) -> str:
    """Return the spoken form of a fraction string such as "1/2" in ``lang``.

    Raises:
        NotImplementedError: ``lang`` has no reading.
    """
    lang2 = _base_lang(lang)
    if lang2 == "pt":
        return PT_BR.pronounce_fraction(fraction_word, scale=scale) if _is_brazilian(lang) \
            else PT_PT.pronounce_fraction(fraction_word, scale=scale)
    elif lang2 == "ast":
        return AST.pronounce_fraction(fraction_word, scale=scale)
    elif lang2 == "ca":
        return CA.pronounce_fraction(fraction_word, scale=scale)
    elif lang2 == "oc":
        return OC.pronounce_fraction(fraction_word, scale=scale)
    elif lang2 == "an":
        return AN.pronounce_fraction(fraction_word, scale=scale)
    elif lang2 == "mwl":
        return MWL.pronounce_fraction(fraction_word, scale=scale)
    elif lang2 == "gl":
        return GL.pronounce_fraction(fraction_word, scale=scale)
    elif lang2 == "ro":
        return RO.pronounce_fraction(fraction_word, scale=scale)
    else:
        return _pronounce_fraction_generic(fraction_word, lang)


def pronounce_ordinal(number: Union[int, float], lang: str,
                      short_scale: Optional[bool] = None,  # DEPRECATED
                      gender: GrammaticalGender = GrammaticalGender.MASCULINE,
                      scale: Optional[Scale] = None,
                      case: Optional[str] = None) -> str:
    """Return the spoken ordinal of a number in ``lang``.

    A Decimal or Fraction reads as its int when integral and as its float
    otherwise. ``case`` applies to Arabic only.

    Raises:
        NotImplementedError: ``lang`` has no ordinal reading.
        ValueError: ``number`` is a Decimal of more than 4300 integer digits.
    """
    number = _from_other_real(number)
    if isinstance(number, Decimal) and _past_read_limit(number):
        # a language with no ordinals raises NotImplementedError first;
        # converting this Decimal to an int alone would take minutes
        pronounce_ordinal(1, lang, short_scale, gender, scale, case)
        raise ValueError("no ordinal reading for a Decimal of more "
                         "than 4300 digits")
    if isinstance(number, Decimal) and number.is_finite():
        # Decimal arithmetic throughout: a Fraction of a Decimal with a long
        # coefficient or a far negative exponent takes minutes to build
        whole = number.to_integral_value()
        if number == whole:
            number = int(whole)
        elif number.copy_abs() <= _FLOAT_MAX:
            number = float(number)
        else:
            # no float holds it: round half away from zero to its int
            number = int(number.to_integral_value(rounding=ROUND_HALF_UP))
    elif isinstance(number, Decimal):
        number = float(number)
    elif isinstance(number, Fraction):
        if number.denominator == 1:
            number = number.numerator
        elif abs(number) <= sys.float_info.max:
            number = float(number)
        else:
            # no float holds it: round half away from zero to its int
            whole = (2 * abs(number.numerator) + number.denominator) \
                // (2 * number.denominator)
            number = whole if number > 0 else -whole
    scale = _resolve_scale(lang, scale, short_scale)
    short_scale = scale == Scale.SHORT
    lang2 = _base_lang(lang)
    if lang2 == "pt":
        return PT_BR.pronounce_ordinal(number, scale=scale, gender=gender) if _is_brazilian(lang) \
            else PT_PT.pronounce_ordinal(number, scale=scale, gender=gender)
    if lang2 == "mwl":
        return MWL.pronounce_ordinal(number, scale=scale, gender=gender)
    if lang2 == "ro":
        return RO.pronounce_ordinal(number, scale=scale, gender=gender)
    if lang2 == "ast":
        return AST.pronounce_ordinal(number, scale=scale, gender=gender)
    if lang2 == "ca":
        return CA.pronounce_ordinal(number, scale=scale, gender=gender)
    if lang2 == "oc":
        return OC.pronounce_ordinal(number, scale=scale, gender=gender)
    if lang2 == "an":
        return AN.pronounce_ordinal(number, scale=scale, gender=gender)
    if lang2 == "az" and (isinstance(number, int) or number.is_integer()) \
            and abs(number) < 10 ** 24:
        # the Azerbaijani engine has no ordinal scale word from 10**24 up
        return pronounce_number(number, lang, ordinals=True, gender=gender, scale=scale)
    if _is_arabic(lang):
        return pronounce_ordinal_ar(number, gender=gender, case=case)
    if lang2 == "da":
        return pronounce_ordinal_da(number, gender)
    if lang2 == "de":
        return pronounce_ordinal_de(number)
    if lang2 == "et":
        return pronounce_ordinal_et(number)
    if lang2 == "es" and (isinstance(number, int) or number.is_integer()) \
            and abs(number) < (10 ** 18 if scale == Scale.SHORT else 10 ** 24):
        # the Castilian engine's last ordinal scale word is "trillonésimo":
        # 10**18 on the long scale, 10**12 on the short scale
        return pronounce_number(number, lang, ordinals=True, gender=gender, scale=scale)
    if lang2 == "fi":
        return pronounce_ordinal_fi(number)
    if lang2 == "fr" and number and (isinstance(number, int) or number.is_integer()) \
            and abs(number) < 10 ** 15:
        # from 10 ** 15 the French engine reads the cardinal scientifically
        return pronounce_number(number, lang, ordinals=True, gender=gender, scale=scale)
    if lang2 == "hr":
        return pronounce_ordinal_hr(number)
    if lang2 == "el":
        return pronounce_ordinal_el(number)
    if lang2 == "he":
        return pronounce_ordinal_he(number)
    if lang2 == "hu":
        return pronounce_ordinal_hu(number)
    if lang2 == "id":
        return pronounce_ordinal_id(number)
    if lang2 == "it" and number == int(number):
        return pronounce_number(number, lang, ordinals=True, gender=gender, scale=scale)
    if lang2 == "ms":
        return pronounce_ordinal_ms(number)
    if lang2 == "tr":
        return pronounce_ordinal_tr(number)
    if lang2 == "fy":
        return pronounce_ordinal_fy(number)
    if lang2 == "nn":
        return pronounce_ordinal_nn(number)
    if lang2 == "nb":
        return pronounce_ordinal_nb(number)
    if lang2 == "nl":
        return pronounce_ordinal_nl(number)
    if lang2 == "sv":
        return pronounce_ordinal_sv(number)
    if lang2 == "gl":
        return GL.pronounce_ordinal(number, scale=scale, gender=gender)
    if lang2 == "cs":
        return pronounce_ordinal_cs(number, gender, short_scale=short_scale)
    if lang2 == "sk":
        return pronounce_ordinal_sk(number)
    if lang2 == "pl":
        return pronounce_ordinal_pl(number, gender)
    if lang2 == "uk":
        return pronounce_ordinal_uk(number, gender)
    if lang2 == "eu":
        return pronounce_ordinal_eu(number)
    if lang2 == "fa":
        return pronounce_ordinal_fa(number)
    if lang2 == "bg":
        return pronounce_number_bg(number, ordinals=True)
    if lang2 == "sl":
        return pronounce_number_sl(number, ordinals=True)
    if lang2 == "kab":
        return pronounce_ordinal_kab(number, gender)
    if lang2 == "ru" and (
            isinstance(number, int) or isinstance(number, float) and number.is_integer()) \
            and _ordinal_ru(abs(int(number)), short_scale) is not None:
        # past the scale words of the Russian engine there is no ordinal
        return pronounce_number(number, lang, ordinals=True, gender=gender, scale=scale)
    # fallback to unicode RBNF
    return _pronounce_rbnf(number, lang, True, gender)


def extract_number(text: str, lang: str,
                   short_scale: Optional[bool] = None,  # DEPRECATED
                   ordinals: bool = False,
                   scale: Optional[Scale] = None) -> Union[int, float, bool]:
    """Read the number in ``text``, or False when it holds none.

    ``ordinals`` reads "third" as 3 instead of 1/3. ``short_scale`` is deprecated
    in favour of ``scale``. The text holds one number.
    """
    if numtag_readers.routed(lang):
        return numtag_readers.extract_number(text, lang, short_scale, ordinals, scale)
    raise NotImplementedError(f"Unsupported language: '{lang}'")


@dataclass(frozen=True)
class NumberSpan:
    """A number found in an utterance. ``start`` and ``end`` are half-open
    code-point offsets, so ``utterance[start:end] == surface``.
    """
    start: int
    end: int
    surface: str
    value: Union[int, float]


def extract_number_spans(text: str, lang: str,
                         short_scale: Optional[bool] = None,  # DEPRECATED
                         ordinals: bool = False,
                         scale: Optional[Scale] = None) -> List[NumberSpan]:
    """Return every number in ``text`` with the span it occupies, in the order written.

    Each span covers a whole number phrase ("two hundred and five", "3.5") and
    ``text[start:end]`` is its surface. ``short_scale`` is deprecated in favour of
    ``scale``.
    """
    if numtag_readers.routed(lang):
        return [NumberSpan(start, end, text[start:end], numtag_readers.number(m.value, m.kind))
                for m in numtag_readers.mentions(text, lang, short_scale, ordinals, scale)
                for start, end in [m.char_span]]
    raise NotImplementedError(f"Unsupported language: '{lang}'")


def is_fractional(input_str: str, lang: str,
                  short_scale: Optional[bool] = None,  # DEPRECATED
                  scale: Optional[Scale] = None) -> Union[bool, float]:
    """Return the fraction ``input_str`` spells, or False. The whole string must be the fraction."""
    if numtag_readers.routed(lang):
        return numtag_readers.is_fractional(input_str, lang, short_scale, scale)
    raise NotImplementedError(f"Unsupported language: '{lang}'")


def is_ordinal(input_str: str, lang: str) -> Union[bool, float]:
    """Return the number ``input_str`` spells as an ordinal, or False."""
    if numtag_readers.routed(lang):
        return numtag_readers.is_ordinal(input_str, lang)
    return _ordinal_reverse_table(lang).get(input_str.lower().strip(), False)
