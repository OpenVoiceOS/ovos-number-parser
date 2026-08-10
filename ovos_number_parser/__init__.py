import math
import re
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional
from typing import Union

from unicode_rbnf import RbnfEngine, FormatPurpose

from ovos_number_parser.numbers_ast import AST
from ovos_number_parser.numbers_an import AN
from ovos_number_parser.numbers_ar import pronounce_number_ar, pronounce_ordinal_ar, extract_number_ar, \
    is_fractional_ar, is_ordinal_ar, nice_number_ar, resolve_ar_lang
from ovos_number_parser.numbers_az import numbers_to_digits_az, extract_number_az, is_fractional_az, pronounce_number_az
from ovos_number_parser.numbers_bg import numbers_to_digits_bg, pronounce_number_bg, extract_number_bg, \
    is_fractional_bg, nice_number_bg
from ovos_number_parser.numbers_ca import (numbers_to_digits_ca, pronounce_number_ca,
    is_fractional_ca, extract_number_ca, CA)
from ovos_number_parser.numbers_cs import numbers_to_digits_cs, pronounce_number_cs, is_fractional_cs, \
    extract_number_cs, pronounce_ordinal_cs
from ovos_number_parser.numbers_da import numbers_to_digits_da, pronounce_number_da, is_fractional_da, is_ordinal_da, \
    pronounce_ordinal_da, extract_number_da
from ovos_number_parser.numbers_de import numbers_to_digits_de, pronounce_number_de, pronounce_ordinal_de, \
    is_ordinal_de, is_fractional_de, extract_number_de
from ovos_number_parser.numbers_en import numbers_to_digits_en, is_ordinal_en, pronounce_number_en, extract_number_en, \
    is_fractional_en
from ovos_number_parser.numbers_el import pronounce_number_el, pronounce_ordinal_el, \
    extract_number_el, is_fractional_el, is_ordinal_el
from ovos_number_parser.numbers_es import (numbers_to_digits_es, pronounce_number_es, extract_number_es,
                                           is_fractional_es, ES)
from ovos_number_parser.numbers_eu import pronounce_number_eu, extract_number_eu, is_fractional_eu, \
    pronounce_ordinal_eu, is_ordinal_eu
from ovos_number_parser.numbers_et import pronounce_number_et, pronounce_ordinal_et, extract_number_et, \
    is_fractional_et, is_ordinal_et, nice_number_et
from ovos_number_parser.numbers_fa import pronounce_number_fa, extract_number_fa, is_fractional_fa, \
    pronounce_ordinal_fa
from ovos_number_parser.numbers_fi import pronounce_number_fi, pronounce_ordinal_fi, extract_number_fi, \
    is_fractional_fi, is_ordinal_fi, nice_number_fi
from ovos_number_parser.numbers_fr import (extract_number_fr, is_fractional_fr, FR)
from ovos_number_parser.numbers_fy import numbers_to_digits_fy, pronounce_number_fy, pronounce_ordinal_fy, \
    extract_number_fy, is_fractional_fy, nice_number_fy
from ovos_number_parser.numbers_gl import GL, pronounce_number_gl, extract_number_gl, is_fractional_gl, \
    numbers_to_digits_gl, pronounce_ordinal_gl, is_ordinal_gl, pronounce_fraction_gl
from ovos_number_parser.numbers_hr import pronounce_number_hr, pronounce_ordinal_hr, extract_number_hr, \
    is_fractional_hr, nice_number_hr, numbers_to_digits_hr
from ovos_number_parser.numbers_he import pronounce_number_he, pronounce_ordinal_he, \
    extract_number_he, is_fractional_he, is_ordinal_he, nice_number_he
from ovos_number_parser.numbers_hu import pronounce_number_hu, pronounce_ordinal_hu, extract_number_hu, \
    is_fractional_hu, is_ordinal_hu, nice_number_hu
from ovos_number_parser.numbers_id import (pronounce_number_id, pronounce_number_ms,
                                           pronounce_ordinal_id, pronounce_ordinal_ms,
                                           extract_number_id, extract_number_ms,
                                           is_fractional_id, is_fractional_ms,
                                           nice_number_id, nice_number_ms,
                                           numbers_to_digits_id, numbers_to_digits_ms)
from ovos_number_parser.numbers_it import (extract_number_it, pronounce_number_it, is_fractional_it, IT)
from ovos_number_parser.numbers_kab import (pronounce_number_kab, pronounce_ordinal_kab, extract_number_kab,
                                             is_fractional_kab, is_ordinal_kab)
from ovos_number_parser.numbers_mwl import MWL
from ovos_number_parser.numbers_oc import OC
from ovos_number_parser.numbers_nb import (nice_number_nb, pronounce_number_nb,
                                           pronounce_ordinal_nb, is_ordinal_nb,
                                           is_fractional_nb, extract_number_nb,
                                           numbers_to_digits_nb)
from ovos_number_parser.numbers_nn import (nice_number_nn, pronounce_number_nn,
                                           pronounce_ordinal_nn, is_ordinal_nn,
                                           is_fractional_nn, extract_number_nn,
                                           numbers_to_digits_nn)
from ovos_number_parser.numbers_nl import numbers_to_digits_nl, pronounce_number_nl, pronounce_ordinal_nl, \
    extract_number_nl, is_fractional_nl
from ovos_number_parser.numbers_pl import numbers_to_digits_pl, pronounce_number_pl, extract_number_pl, \
    is_fractional_pl, pronounce_ordinal_pl
from ovos_number_parser.numbers_pt import PortugueseVariant, PT_PT, PT_BR
from ovos_number_parser.numbers_ro import RO
from ovos_number_parser.numbers_ru import numbers_to_digits_ru, pronounce_number_ru, extract_number_ru, is_fractional_ru
from ovos_number_parser.numbers_sk import numbers_to_digits_sk, pronounce_number_sk, is_fractional_sk, \
    extract_number_sk, pronounce_ordinal_sk, nice_number_sk
from ovos_number_parser.numbers_sl import pronounce_number_sl, extract_number_sl, is_fractional_sl, \
    is_ordinal_sl, nice_number_sl
from ovos_number_parser.numbers_sv import pronounce_number_sv, pronounce_ordinal_sv, extract_number_sv, \
    is_fractional_sv
from ovos_number_parser.numbers_tr import numbers_to_digits_tr, pronounce_number_tr, \
    pronounce_ordinal_tr, extract_number_tr, is_fractional_tr, nice_number_tr
from ovos_number_parser.numbers_uk import numbers_to_digits_uk, pronounce_number_uk, extract_number_uk, \
    is_fractional_uk, pronounce_ordinal_uk
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
from ovos_number_parser.util import Scale, GrammaticalGender, DigitPronunciation


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
    "de", "fr", "es", "it", "nl", "pl", "sv", "da", "nb", "nn", "no",
    "gl", "ca", "eu", "cs", "sl", "sk", "hr", "hu", "fi", "et", "ro",
    "ast", "oc", "an", "mwl", "fy",
}


def _canonical_scale(lang: str) -> Scale:
    """The scale convention a language uses when the caller specifies none.

    European Portuguese is long scale (10^9 = "mil milhões") while Brazilian
    Portuguese is short scale (10^9 = "um bilhão"), so ``pt`` is resolved by
    region rather than by the bare language code.
    """
    lang2 = lang.lower().split("-")[0]
    if lang2 == "pt":
        return Scale.SHORT if "br" in lang.lower() else Scale.LONG
    return Scale.LONG if lang2 in _LONG_SCALE_LANGS else Scale.SHORT


def _resolve_scale(lang: str,
                   scale: Optional[Scale],
                   short_scale: Optional[bool] = None) -> Scale:
    """Resolve the effective scale for a dispatch call.

    An explicit ``scale`` wins; the deprecated ``short_scale`` flag is honoured
    next for backward compatibility; otherwise the language's canonical
    convention applies. This keeps pronounce/extract/ordinal/numbers_to_digits
    consistent about what "no scale given" means.
    """
    if scale is not None:
        return scale
    if short_scale is not None:
        return Scale.SHORT if short_scale else Scale.LONG
    return _canonical_scale(lang)


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

# words that may join two spoken numbers ("vingt et un", "sto in ena")
_NUMBER_CONNECTORS = {
    "ar": {"و"}, "bg": {"и"}, "ca": {"i"}, "da": {"og"}, "en": {"and"}, "es": {"y"}, "eu": {"eta"},
    # standard Italian cardinals carry no conjunction ("venticinque", not
    # "venti e cinque"), so "e" separates two numbers rather than joining them
    "fr": {"et"}, "fy": {"en"}, "it": set(), "nl": {"en"}, "sv": {"och"},
    "fa": {"و"}, "hr": {"i"}, "sl": {"in"}, "hu": set(), "fi": set(),
    "et": set(), "kab": {"u", "d", "ed"},
}


def _minus_word(lang: str) -> str:
    """The language's spoken minus sign, derived from pronounce_number."""
    spoken = pronounce_number(-1, lang)
    return spoken.split()[0] if " " in spoken else ""


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
    lang2 = lang.lower().split("-")[0]

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
            (nice_number_ar if _is_ar(lang) else None)
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

    if result is None:
        # approximate: cardinal numerator + ordinal denominator
        result = f"{pronounce_number(n1, lang)} {pronounce_ordinal(n2, lang)}"
    if negative:
        minus = _minus_word(lang)
        result = f"{minus} {result}" if minus else f"-{result}"
    return result


_ORDINAL_REVERSE_CACHE = {}


def _is_ordinal_generic(input_str: str, lang: str):
    """Fallback ordinal detection via reverse lookup over pronounce_ordinal."""
    lang2 = lang.lower().split("-")[0]
    if lang2 not in _ORDINAL_REVERSE_CACHE:
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
        _ORDINAL_REVERSE_CACHE[lang2] = table
    return _ORDINAL_REVERSE_CACHE[lang2].get(input_str.lower().strip(), False)


def _numbers_to_digits_generic(utterance: str, lang: str) -> str:
    """Fallback that replaces spoken number spans with digits using
    extract_number over maximal runs of number words."""
    lang2 = lang.lower().split("-")[0]
    connectors = _NUMBER_CONNECTORS.get("ar" if _is_ar(lang) else lang2, set())
    tokens = utterance.split()
    # ASCII plus Arabic comma, semicolon and question mark, so a number glued
    # to punctuation ("٢٠٢٤،", "25.") is still recognised and the mark is
    # carried over onto the digits instead of being dropped
    punct = ".,!?;:؟،؛"

    def _clean(t):
        return t.strip(punct).lower()

    def _is_num(t):
        c = _clean(t)
        if not c:
            return False
        try:
            if extract_number(c, lang) is False:
                return False
        except NotImplementedError:
            return False
        # extract_number finds a number *inside* a token, so a numeral glued to
        # an ordinary word ("10-segundos") would otherwise be replaced whole and
        # the word lost. A hyphenated token only counts as one number when every
        # part is itself a numeral or a joiner ("vint-i-un", "quatre-vingt-dix").
        if "-" in c.strip("-"):
            for part in c.split("-"):
                if not part or part in connectors:
                    continue
                try:
                    if extract_number(part, lang) is False:
                        return False
                except NotImplementedError:
                    return False
        return True

    out = []
    i = 0
    while i < len(tokens):
        if not _is_num(tokens[i]):
            out.append(tokens[i])
            i += 1
            continue
        j = i

        def _continues(next_j, via_connector=False):
            """The span only grows if the combined words form one larger
            number ("vingt et un" = 21) rather than two separate numbers
            ("due e tre")."""
            extended = " ".join(_clean(t) for t in tokens[i:next_j + 1])
            current = " ".join(_clean(t) for t in tokens[i:j + 1])
            extended_val = extract_number(extended, lang)
            if extended_val is False or extended_val is None:
                return False
            current_val = extract_number(current, lang)
            next_val = extract_number(_clean(tokens[next_j]), lang)
            if current_val is False or current_val is None:
                return False
            if extended_val == current_val \
                    or abs(extended_val) <= abs(current_val):
                return False
            if extended_val != next_val:
                return True
            # "one hundred": multiplying a scale word by one leaves the value
            # unchanged, so the value comparison above cannot tell that the
            # multiplier is grammatically required. Directly adjacent to a
            # scale word it is, so the span must keep growing; behind a
            # connector ("one and three") it is a separate number and must
            # not be absorbed.
            return not via_connector and abs(current_val) == 1 \
                and next_val is not False and next_val is not None \
                and abs(next_val) >= 100

        while j + 1 < len(tokens):
            if _is_num(tokens[j + 1]) and _continues(j + 1):
                j += 1
            elif _clean(tokens[j + 1]) in connectors and j + 2 < len(tokens) \
                    and _is_num(tokens[j + 2]) \
                    and _continues(j + 2, via_connector=True):
                j += 2
            else:
                break
        span = " ".join(_clean(t) for t in tokens[i:j + 1])
        val = extract_number(span, lang)
        stripped = tokens[j].rstrip(punct)
        trail = tokens[j][len(stripped):]
        if isinstance(val, float) and val.is_integer():
            val = int(val)
        out.append(f"{val}{trail}")
        i = j + 1
    return " ".join(out)


def numbers_to_digits(utterance: str, lang: str, scale: Optional[Scale] = None) -> str:
    """
    Convert written numbers in a text string to their digit representations for the specified language and numerical scale.
    
    Parameters:
        utterance (str): Text potentially containing written numbers.
        lang (str): Language code used to determine parsing rules.
        scale (Scale, optional): Numerical scale (long or short) for languages that distinguish between them.
    
    Returns:
        str: The input text with written numbers replaced by their digit equivalents.
    
    Raises:
        NotImplementedError: If the specified language is not supported.
    """
    scale = _resolve_scale(lang, scale)
    if lang.startswith("en"):
        # English has its own converter, which reads compound ordinals
        # ("the twenty fifth" -> 25) and never mistakes a singular ordinal for a
        # fraction. The generic fallback did neither.
        return numbers_to_digits_en(utterance, short_scale=scale == Scale.SHORT)
    if lang.startswith("ast"):
        return AST.numbers_to_digits(utterance)
    if lang.startswith("oc"):
        return OC.numbers_to_digits(utterance, scale=scale)
    if lang.startswith("an"):
        return AN.numbers_to_digits(utterance)
    if lang.startswith("fy"):
        return numbers_to_digits_fy(utterance)
    if lang.startswith("gl"):
        return numbers_to_digits_gl(utterance)
    if lang.startswith("de"):
        return numbers_to_digits_de(utterance)
    if lang.startswith("pt"):
        return PT_PT.numbers_to_digits(utterance, scale=scale)
    if lang.startswith("mwl"):
        return MWL.numbers_to_digits(utterance, scale=scale)
    if lang.startswith("ro"):
        return RO.numbers_to_digits(utterance, scale=scale)
    if lang.startswith("bg"):
        return numbers_to_digits_bg(utterance)
    if lang.startswith("hr"):
        return numbers_to_digits_hr(utterance)
    if lang.startswith("ru"):
        return numbers_to_digits_ru(utterance)
    if lang.startswith("sk"):
        return numbers_to_digits_sk(utterance)
    if lang.startswith("id"):
        return numbers_to_digits_id(utterance)
    if lang.startswith("ms"):
        return numbers_to_digits_ms(utterance)
    if lang.startswith("tr"):
        return numbers_to_digits_tr(utterance)
    if lang.startswith("uk"):
        return numbers_to_digits_uk(utterance)
    return _numbers_to_digits_generic(utterance, lang)


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
        lang.split("-")[0].split("_")[0], _COMPLEX_CONNECTIVES["en"])

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


def _round_for_speech(number: Union[int, float], places: int) -> Union[int, float]:
    """Round a real number to ``places`` decimals, half away from zero.

    The per-language cardinal formatters keep only the first ``places``
    fractional digits by slicing the decimal string, which truncates rather
    than rounds: 3.14159 at 2 places would drop to "...one four" instead of the
    expected "...one four two". Rounding here, before dispatch, means every
    backend truncates a value that is already correct to ``places`` digits, so
    the spoken output is correctly rounded for every language at once and
    carries into the integer part where needed (0.999999 at 2 places -> 1).

    ROUND_HALF_UP is chosen over Python's default banker's rounding because
    half-away-from-zero is the convention people expect when a value is read
    aloud. Rounding of numerical values follows ISO 80000-1 (Quantities and
    units -- General) and NIST SP 811 (2008 ed.) Appendix B.7.

    Integers and non-finite floats (inf) are returned unchanged, and literal
    negative zero is normalised to plain zero so no language speaks "minus
    zero"; NaN and complex inputs are handled by the caller before reaching
    here. A non-zero value whose magnitude is smaller than the rounding quantum
    is left untouched, so its sub-quantum fractional reading and sign survive
    rather than collapsing to an unsigned zero.
    """
    if isinstance(number, int) or not isinstance(number, float):
        return number
    if not math.isfinite(number):
        return number
    if number == 0:
        # normalise -0.0 to 0.0 so no language speaks "minus zero"
        return 0.0
    if number.is_integer():
        # no fractional part to shorten; also avoids quantize overflow on very
        # large integer-valued floats (1e300)
        return number
    quantum = Decimal(1).scaleb(-places)
    try:
        rounded = Decimal(str(number)).quantize(quantum, rounding=ROUND_HALF_UP)
    except (ArithmeticError, ValueError):
        # a value too large to quantize at this precision is already far coarser
        # than ``places`` decimals; leave it untouched
        return number
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
    "it": "per dieci alla",
    "fr": "fois dix puissance",
    "de": "mal zehn hoch",
    "nl": "maal tien tot de macht",
    "ca": "per deu elevat a",
    "gl": "veces dez elevado a",
    "ro": "ori zece la puterea",
    "da": "gange ti i",
    "sv": "gånger tio upphöjt till",
}


def _base_lang(lang: str) -> str:
    """Bare language code, so "pt-BR" and "pt" resolve to the same entry."""
    return lang.lower().split("-")[0]


def _is_ar(lang: str) -> bool:
    """Whether ``lang`` names an Arabic variety this library serves.

    Covers the BCP-47 macrolanguage code (``ar``, ``ar-SA``, ``ar-EG``, ...)
    and the ISO 639-3 codes for Modern Standard Arabic and its spoken lects
    (``arb``, ``ars``, ``acw``, ``afb``, ``arz``, ``apc``, ``ajp``, ``acm``,
    ``ary``, ``aeb``, ``ayl``) -- see ``resolve_ar_lang`` for the table and
    citations. A plain ``lang.startswith("ar")`` check would miss lects
    whose code does not happen to start with "ar" (``acw``, ``afb``,
    ``apc``, ``ajp``, ``acm``).
    """
    return resolve_ar_lang(lang) is not None


def _ar_default_case(lang: str) -> str:
    """Default pronunciation register for an Arabic ``lang`` code."""
    return resolve_ar_lang(lang) or "nominative"


def _pronounce_infinity(number: float, lang: str) -> str:
    """Spoken form of +/-infinity for any language (English default)."""
    pos, neg = _INFINITY_WORDS.get(_base_lang(lang), _INFINITY_WORDS["en"])
    return neg if number < 0 else pos


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


def _has_padded_scale_words(spoken: str) -> bool:
    """
    Whether a backend padded a magnitude by repeating its largest scale word.

    Some backends do not raise past their named-scale table; they repeat the
    biggest word they know until the magnitude is covered
    ("trilioi trilioi trilioi", "sextiliões vigintiliões vigintiliões").
    No natural numeral repeats a scale word back to back, so two identical
    adjacent words mark output that is not a reading at all.

    Only sound for a whole number. A digit-by-digit decimal repeats words
    legitimately ("2.22" -> "dois vírgula dois dois"), so callers must scope
    this check to integral values -- which is what the oversized-number path
    deals with anyway.
    """
    words = spoken.split()
    return any(a == b for a, b in zip(words, words[1:]))


def _has_unread_digits(spoken: str) -> bool:
    """
    Whether a backend gave up and handed back the numeral instead of reading it.

    Unlike padded scale words this is not nonsense: a bare numeral is a
    documented fallback for some languages (Finnish and Estonian pin it), and
    a TTS engine will read the digits itself. It is only worth replacing when
    a localized scientific reading is available -- swapping it for one glued
    together with English words would be a downgrade, not a fix.
    """
    return bool(_DIGIT_RUN.search(spoken))


def _pronounce_bignum_fallback(number: Union[int, float], lang: str,
                               places: int) -> str:
    """
    Spoken scientific reading for finite numbers too large for a language's
    named-scale table, computed from the decimal string so it never overflows
    the float range.

    Mantissa, sign and exponent are all pronounced by the target language.
    Only the connective joining them is looked up, and falls back to English
    for languages missing from _SCIENTIFIC_WORDS.
    """
    digits = str(abs(int(number)))
    exponent = len(digits) - 1
    tail = digits[1:1 + places].rstrip("0")
    mantissa = float(digits[0] + ("." + tail if tail else ""))
    # the sign rides on the mantissa so each language speaks its own minus
    # word ("menos dois...") instead of an English prefix
    if number < 0:
        mantissa = -mantissa
    mantissa_words = pronounce_number(mantissa, lang=lang, places=places)
    exponent_words = pronounce_number(exponent, lang=lang)
    connective = _SCIENTIFIC_WORDS.get(_base_lang(lang),
                                       _SCIENTIFIC_WORDS["en"])
    return f"{mantissa_words} {connective} {exponent_words}"


def pronounce_number(number: Union[int, float], lang: str,
                     places: int = 3,
                     short_scale: Optional[bool] = None,  # DEPRECATED
                     scientific: bool = False,
                     ordinals: bool = False,
                     digits: Optional[DigitPronunciation] = None,
                     gender: GrammaticalGender = GrammaticalGender.MASCULINE,
                     scale: Optional[Scale] = None,
                     case: Optional[str] = None) -> str:
    """
    Return the spoken representation of a number in the specified language.
     
    Converts a numeric value to its pronounced form, supporting various languages, decimal precision, scale (short or long), scientific notation, ordinal forms, digit pronunciation styles, and grammatical gender where applicable. Falls back to Unicode RBNF for unsupported languages.
     
    Parameters:
        number (int or float): The number to pronounce.
        lang (str): BCP-47 language code specifying the language for pronunciation.
        places (int, optional): Number of decimal places to include (default is 3).
            The fractional part is rounded to this precision half away from zero
            before pronunciation, following ISO 80000-1 (Quantities and units --
            General) and NIST SP 811 (2008 ed.) Appendix B.7 on the rounding of
            numerical values; rounding that carries into the integer part is
            spoken as such (0.999999 at 2 places -> "one").
        short_scale (bool, optional): DEPRECATED, use the ``scale`` enum instead.
        scientific (bool, optional): If True, pronounce the number in scientific notation.
        ordinals (bool, optional): If True, pronounce the number as an ordinal (e.g., "first" instead of "one").
        digits (DigitPronunciation, optional): Style for pronouncing digits (default is FULL_NUMBER).
        gender (GrammaticalGender, optional): Grammatical gender for languages that require it (default is MASCULINE).
        scale (Scale, optional): Short or long scale for large numbers. When
            omitted, the language's canonical convention applies (see
            ``_canonical_scale``), per Wikipedia "Long and short scales"
            (https://en.wikipedia.org/wiki/Long_and_short_scales); an explicit
            value always overrides it.
        case (str, optional): Grammatical case/register, currently only
            meaningful for Arabic ("nominative" or "oblique", see
            ``pronounce_number_ar``). When omitted, the Arabic lect named by
            ``lang`` uses its own default register (see
            ``numbers_ar.resolve_ar_lang``); ignored for every other
            language.

    Returns:
        str: The pronounced form of the number.
     
    Raises:
        ValueError: If ``number`` is NaN, which has no cardinal spoken form.
        NotImplementedError: If the specified language is not supported.

    Note:
        NaN is rejected up front so every language fails the same way. IEEE 754
        defines NaN as a value that "does not represent any numeric quantity"
        (IEEE 754-2019, clause 6.2), so it has no cardinal reading. Without this
        guard each backend crashes differently while formatting it: scientific
        formatting does ``"%E" % nan`` -> ``"NAN"`` and then fails to split off an
        exponent, while cardinal formatting fails converting NaN to ``int``.
    """
    scale = _resolve_scale(lang, scale, short_scale)
    short_scale = scale == Scale.SHORT
    if isinstance(number, complex):
        return _pronounce_complex(number, lang, places, scale, digits, gender)
    if isinstance(number, float) and number != number:
        raise ValueError("cannot pronounce NaN (not a number)")
    # Infinity is not tied to any named-scale table; handle it uniformly for
    # every language so no per-language path has to convert it to an integer.
    if isinstance(number, float) and math.isinf(number):
        return _pronounce_infinity(number, lang)
    # How a language conventionally reads the digits after the decimal marker
    # is a property of the language, not of the caller: Spanish and Catalan
    # read them one by one ("tres coma uno cuatro") while Portuguese composes
    # them ("três vírgula catorze"). `digits=None` means "use the language's
    # convention"; an explicit value always wins.
    if digits is None:
        digits = _DEFAULT_DIGIT_PRONUNCIATION.get(
            _base_lang(lang), DigitPronunciation.FULL_NUMBER)

    # Round to the spoken precision before dispatch so every backend speaks a
    # rounded value instead of a truncated one (see _round_for_speech).
    number = _round_for_speech(number, places)
    try:
        spoken = _pronounce_number_dispatch(
            number, lang, places, short_scale, scientific, ordinals,
            digits, gender, scale, case)
    except (IndexError, KeyError, OverflowError):
        # A finite number overflowed a language's named-scale table. Kabyle
        # has a documented finite ceiling (raises above 9999), so keep that
        # contract; every other language falls back to a spoken scientific
        # reading rather than crashing. Ordinary-magnitude numbers keep their
        # original error so genuine bugs are not masked.
        if not lang.startswith("kab") and abs(number) >= 10 ** 15:
            return _pronounce_bignum_fallback(number, lang, places)
        raise
    # A backend that does not raise past its scale table returns padded or
    # unread output instead (see _is_spoken_reading). Only composed readings
    # of large numbers are checked: a digit-by-digit rendering repeats words
    # legitimately, and Kabyle's finite ceiling is a documented contract.
    if abs(number) >= 10 ** 15 and not lang.startswith("kab") \
            and not scientific and (isinstance(number, int)
                                    or float(number).is_integer()):
        # padded scale words are never a reading, so always replace them
        if _has_padded_scale_words(spoken):
            return _pronounce_bignum_fallback(number, lang, places)
        # a bare numeral is a legitimate fallback the TTS can read; only
        # improve on it where the scientific reading is fully localized
        if _has_unread_digits(spoken) and _base_lang(lang) in _SCIENTIFIC_WORDS:
            return _pronounce_bignum_fallback(number, lang, places)
    return spoken


def _pronounce_number_dispatch(number, lang, places, short_scale, scientific,
                               ordinals, digits, gender, scale, case=None):
    if lang.startswith("en"):
        return pronounce_number_en(number, places, short_scale, scientific, ordinals)
    if lang.startswith("az"):
        return pronounce_number_az(number, places, short_scale, scientific, ordinals)
    if _is_ar(lang):
        return pronounce_number_ar(number, places, scientific, ordinals,
                                   case=case if case is not None
                                   else _ar_default_case(lang))
    if lang.startswith("bg"):
        return pronounce_number_bg(number, places, short_scale, scientific, ordinals)
    if lang.startswith("ca"):
        return CA.pronounce_number(number, places, scale, ordinals, digits, gender)
    if lang.startswith("ast"):
        return AST.pronounce_number(number, places, scale, ordinals, digits, gender)
    if lang.startswith("oc"):
        return OC.pronounce_number(number, places, scale, ordinals, digits, gender)
    if lang.startswith("an"):
        return AN.pronounce_number(number, places, scale, ordinals, digits, gender)
    if lang.startswith("cs"):
        return pronounce_number_cs(number, places, short_scale, scientific, ordinals)
    if lang.startswith("da"):
        return pronounce_number_da(number, places, short_scale, scientific, ordinals)
    if lang.startswith("de"):
        return pronounce_number_de(number, places, short_scale, scientific, ordinals)
    if lang.startswith("gl"):
        return GL.pronounce_number(number, places, scale, ordinals, digits, gender)
    if lang.startswith("el"):
        return pronounce_number_el(number, places, scientific, ordinals)
    if lang.startswith("es"):
        return ES.pronounce_number(number, places, scale, ordinals, digits, gender)
    if lang.startswith("eu"):
        return pronounce_number_eu(number, places)
    if lang.startswith("et"):
        return pronounce_number_et(number, places, short_scale, scientific, ordinals)
    if lang.startswith("fa"):
        return pronounce_number_fa(number, places, scientific, ordinals)
    if lang.startswith("fi"):
        return pronounce_number_fi(number, places, short_scale, scientific, ordinals)
    if lang.startswith("fr"):
        return FR.pronounce_number(number, places, scale, ordinals, digits, gender)
    if lang.startswith("he"):
        return pronounce_number_he(number, places, scientific, ordinals)
    if lang.startswith("hr"):
        return pronounce_number_hr(number, places, short_scale, scientific, ordinals)
    if lang.startswith("hu"):
        return pronounce_number_hu(number, places, short_scale, scientific, ordinals)
    if lang.startswith("id"):
        return pronounce_number_id(number, places, short_scale, scientific, ordinals)
    if lang.startswith("ms"):
        return pronounce_number_ms(number, places, short_scale, scientific, ordinals)
    if lang.startswith("tr"):
        return pronounce_number_tr(number, places, short_scale, scientific, ordinals)
    if lang.startswith("it"):
        # NOT routed through IT: the engine spaces the tens ("venti cinque")
        # where Italian elides them ("venticinque"). Legacy path until the
        # engine handles elision, so `digits` stays unused here.
        return pronounce_number_it(number, places, short_scale, scientific)
    if lang.startswith("kab"):
        return pronounce_number_kab(number, places, ordinals, gender)
    if lang.startswith("fy"):
        return pronounce_number_fy(number, places, short_scale, scientific, ordinals)
    if lang.startswith("nn"):
        return pronounce_number_nn(number, places, short_scale, scientific, ordinals)
    if lang.startswith("nb") or lang.startswith("no"):
        return pronounce_number_nb(number, places, short_scale, scientific, ordinals)
    if lang.startswith("nl"):
        return pronounce_number_nl(number, places, short_scale, scientific, ordinals)
    if lang.startswith("pl"):
        return pronounce_number_pl(number, places, short_scale, scientific, ordinals)
    if lang.startswith("pt"):
        if "br" in lang.lower():
            return PT_BR.pronounce_number(number, places, scale, ordinals, digits, gender)
        return PT_PT.pronounce_number(number, places, scale, ordinals, digits, gender)
    if lang.startswith("mwl"):
        return MWL.pronounce_number(number, places, scale, ordinals, digits, gender)
    if lang.startswith("ro"):
        return RO.pronounce_number(number, places, scale, ordinals, digits, gender)
    if lang.startswith("ru"):
        return pronounce_number_ru(number, places, short_scale, scientific, ordinals)
    if lang.startswith("sk"):
        return pronounce_number_sk(number, places, short_scale, scientific, ordinals)
    if lang.startswith("sl"):
        return pronounce_number_sl(number, places, short_scale, scientific, ordinals)
    if lang.startswith("sv"):
        return pronounce_number_sv(number, places, short_scale, scientific, ordinals)
    if lang.startswith("uk"):
        return pronounce_number_uk(number, places, short_scale, scientific, ordinals)
    # fallback to unicode RBNF
    try:
        engine = RbnfEngine.for_language(lang.split("-")[0])
        fmt = FormatPurpose.ORDINAL if ordinals else FormatPurpose.CARDINAL
        return engine.format_number(number, fmt).text
    except Exception as err:
        raise NotImplementedError(f"Unsupported language: '{lang}'") from err


def pronounce_fraction(fraction_word: str, lang: str, scale: Optional[Scale] = None) -> str:
    """
    Return the spoken form of a fraction string (e.g., "1/2" as "one half") for the specified language and numerical scale.
    
    Parameters:
        fraction_word (str): The fraction to pronounce (e.g., "3/2").
        scale (Scale, optional): Numerical scale to use (SHORT or LONG). Defaults to LONG.
    
    Returns:
        str: The pronounced fraction.
    
    Raises:
        NotImplementedError: If the specified language is not supported.
    """
    if lang.startswith("pt"):
        return PT_BR.pronounce_fraction(fraction_word, scale=scale) if "br" in lang.lower() \
            else PT_PT.pronounce_fraction(fraction_word, scale=scale)
    elif lang.startswith("ast"):
        return AST.pronounce_fraction(fraction_word, scale=scale)
    elif lang.startswith("ca"):
        return CA.pronounce_fraction(fraction_word, scale=scale)
    elif lang.startswith("oc"):
        return OC.pronounce_fraction(fraction_word, scale=scale)
    elif lang.startswith("an"):
        return AN.pronounce_fraction(fraction_word, scale=scale)
    elif lang.startswith("mwl"):
        return MWL.pronounce_fraction(fraction_word, scale=scale)
    elif lang.startswith("gl"):
        return pronounce_fraction_gl(fraction_word, scale=scale)
    elif lang.startswith("ro"):
        return RO.pronounce_fraction(fraction_word, scale=scale)
    else:
        return _pronounce_fraction_generic(fraction_word, lang)


def pronounce_ordinal(number: Union[int, float], lang: str,
                      short_scale: Optional[bool] = None,  # DEPRECATED
                      gender: GrammaticalGender = GrammaticalGender.MASCULINE,
                      scale: Optional[Scale] = None) -> str:
    """
    Return the spoken ordinal form of a number in the specified language.
      
    Parameters:
        number (int or float): The number to convert to its ordinal spoken equivalent.
        lang (str): BCP-47 language code specifying the language for pronunciation.
        short_scale (bool, optional): Whether to use the short (True) or long (False) scale for large numbers. Defaults to True.
        gender (GrammaticalGender, optional): Grammatical gender to use for languages that require it. Defaults to masculine.
      
    Returns:
        str: The ordinal number pronounced in the specified language.
      
    Raises:
        NotImplementedError: If the language is not supported.
    """
    scale = _resolve_scale(lang, scale, short_scale)
    short_scale = scale == Scale.SHORT
    if lang.startswith("pt"):
        return PT_BR.pronounce_ordinal(number, scale=scale, gender=gender) if "br" in lang.lower() \
            else PT_PT.pronounce_ordinal(number, scale=scale, gender=gender)
    if lang.startswith("mwl"):
        return MWL.pronounce_ordinal(number, scale=scale, gender=gender)
    if lang.startswith("ro"):
        return RO.pronounce_ordinal(number, scale=scale, gender=gender)
    if lang.startswith("ast"):
        return AST.pronounce_ordinal(number, scale=scale, gender=gender)
    if lang.startswith("ca"):
        return CA.pronounce_ordinal(number, scale=scale, gender=gender)
    if lang.startswith("oc"):
        return OC.pronounce_ordinal(number, scale=scale, gender=gender)
    if lang.startswith("an"):
        return AN.pronounce_ordinal(number, scale=scale, gender=gender)
    if _is_ar(lang):
        return pronounce_ordinal_ar(number)
    if lang.startswith("da"):
        return pronounce_ordinal_da(number)
    if lang.startswith("de"):
        return pronounce_ordinal_de(number)
    if lang.startswith("et"):
        return pronounce_ordinal_et(number)
    if lang.startswith("fi"):
        return pronounce_ordinal_fi(number)
    if lang.startswith("hr"):
        return pronounce_ordinal_hr(number)
    if lang.startswith("el"):
        return pronounce_ordinal_el(number)
    if lang.startswith("he"):
        return pronounce_ordinal_he(number)
    if lang.startswith("hu"):
        return pronounce_ordinal_hu(number)
    if lang.startswith("id"):
        return pronounce_ordinal_id(number)
    if lang.startswith("ms"):
        return pronounce_ordinal_ms(number)
    if lang.startswith("tr"):
        return pronounce_ordinal_tr(number)
    if lang.startswith("fy"):
        return pronounce_ordinal_fy(number)
    if lang.startswith("nn"):
        return pronounce_ordinal_nn(number)
    if lang.startswith("nb") or lang.startswith("no"):
        return pronounce_ordinal_nb(number)
    if lang.startswith("nl"):
        return pronounce_ordinal_nl(number)
    if lang.startswith("sv"):
        return pronounce_ordinal_sv(number)
    if lang.startswith("gl"):
        return pronounce_ordinal_gl(number, gender=gender, scale=scale)
    if lang.startswith("cs"):
        return pronounce_ordinal_cs(number)
    if lang.startswith("sk"):
        return pronounce_ordinal_sk(number)
    if lang.startswith("pl"):
        return pronounce_ordinal_pl(number)
    if lang.startswith("uk"):
        return pronounce_ordinal_uk(number)
    if lang.startswith("eu"):
        return pronounce_ordinal_eu(number)
    if lang.startswith("fa"):
        return pronounce_ordinal_fa(number)
    if lang.startswith("bg"):
        return pronounce_number_bg(number, ordinals=True)
    if lang.startswith("sl"):
        return pronounce_number_sl(number, ordinals=True)
    if lang.startswith("kab"):
        return pronounce_ordinal_kab(number, gender)
    # fallback to unicode RBNF
    try:
        engine = RbnfEngine.for_language(lang.split("-")[0])
        fmt = FormatPurpose.ORDINAL
        return engine.format_number(number, fmt).text
    except Exception as err:
        raise NotImplementedError(f"Unsupported language: '{lang}'") from err


#: a hyphen or underscore sitting between two letters is just a spelling of the
#: space that joins a compound numeral, so "twenty-one", "twenty_one" and
#: "twenty one" must all read alike. Only letter-letter joins are rewritten: a
#: leading "-" is a minus sign, and a digit on either side means a range or a
#: numeral glued to a word ("10-15", "10-segundos"), which must survive intact.
_COMPOUND_NUMERAL_JOIN = re.compile(r"(?<=[^\W\d_])[-_](?=[^\W\d_])",
                                    re.UNICODE)

#: languages whose numerals carry a *meaningful* internal hyphen, where the
#: separator is not interchangeable with a space. Hungarian spells numbers
#: above two thousand with a hyphen at the thousand boundary
#: ("kétezer-ötszáz" = 2500), so rewriting it to a space loses the tail.
_HYPHENATED_NUMERAL_LANGS = ("hu",)


def _unglue_compound_numerals(text: str, lang: str) -> str:
    """Normalise "-"/"_" written between letters to a space."""
    if lang.lower().split("-")[0] in _HYPHENATED_NUMERAL_LANGS:
        return text
    return _COMPOUND_NUMERAL_JOIN.sub(" ", text)


def extract_number(text: str, lang: str,
                   short_scale: Optional[bool] = None,  # DEPRECATED
                   ordinals: bool = False,
                   scale: Optional[Scale] = None) -> Union[int, float, bool]:
    """Takes in a string and extracts a number.

    Assumes only 1 number is in the string, does NOT handle multiple numbers

    Args:
        text (str): the string to extract a number from
        short_scale (bool): DEPRECATED, use the ``scale`` enum instead.
            When neither ``scale`` nor this flag is given, the language's
            canonical short/long convention applies, per Wikipedia "Long and
            short scales" (https://en.wikipedia.org/wiki/Long_and_short_scales).
            Short scale: 10^9 = "billion". Long scale: 10^9 = "milliard",
            10^12 = "billion".
        ordinals (bool): consider ordinal numbers, e.g. third=3 instead of 1/3
        lang (str, optional): an optional BCP-47 language code, if omitted
                              the default language will be used.
    Returns:
        (int, float or False): The number extracted or False if the input
                               text contains no numbers
    """
    if not isinstance(text, str):
        # non-string input carries no number to extract
        return False
    text = _unglue_compound_numerals(text, lang)
    scale = _resolve_scale(lang, scale, short_scale)
    short_scale = scale == Scale.SHORT
    if lang.startswith("en"):
        return extract_number_en(text, short_scale, ordinals)
    if lang.startswith("az"):
        return extract_number_az(text, short_scale, ordinals)
    if _is_ar(lang):
        return extract_number_ar(text, ordinals)
    if lang.startswith("bg"):
        return extract_number_bg(text, short_scale, ordinals)
    if lang.startswith("ca"):
        return CA.extract_number(text, ordinals=ordinals, scale=scale)
    if lang.startswith("cs"):
        return extract_number_cs(text, short_scale, ordinals)
    if lang.startswith("da"):
        return extract_number_da(text, short_scale, ordinals)
    if lang.startswith("de"):
        return extract_number_de(text, short_scale, ordinals)
    if lang.startswith("el"):
        return extract_number_el(text, ordinals)
    if lang.startswith("es"):
        return extract_number_es(text, short_scale, ordinals)
    if lang.startswith("gl"):
        return extract_number_gl(text, short_scale, ordinals)
    if lang.startswith("eu"):
        return extract_number_eu(text, short_scale, ordinals)
    if lang.startswith("et"):
        return extract_number_et(text, short_scale, ordinals)
    if lang.startswith("fa"):
        return extract_number_fa(text, ordinals)
    if lang.startswith("fi"):
        return extract_number_fi(text, short_scale, ordinals)
    if lang.startswith("fr"):
        return extract_number_fr(text, short_scale, ordinals)
    if lang.startswith("id"):
        return extract_number_id(text, short_scale, ordinals)
    if lang.startswith("it"):
        return extract_number_it(text, short_scale, ordinals)
    if lang.startswith("ms"):
        return extract_number_ms(text, short_scale, ordinals)
    if lang.startswith("tr"):
        return extract_number_tr(text, short_scale, ordinals)
    if lang.startswith("kab"):
        return extract_number_kab(text, short_scale, ordinals)
    if lang.startswith("fy"):
        return extract_number_fy(text, short_scale, ordinals)
    if lang.startswith("nn"):
        return extract_number_nn(text, short_scale, ordinals)
    if lang.startswith("nb") or lang.startswith("no"):
        return extract_number_nb(text, short_scale, ordinals)
    if lang.startswith("nl"):
        return extract_number_nl(text, short_scale, ordinals)
    if lang.startswith("pl"):
        return extract_number_pl(text, short_scale, ordinals)
    if lang.startswith("pt"):
        return PT_BR.extract_number(text, scale=scale, ordinals=ordinals) if "br" in lang.lower() \
            else PT_PT.extract_number(text, scale=scale, ordinals=ordinals)
    if lang.startswith("mwl"):
        return MWL.extract_number(text, scale=scale, ordinals=ordinals)
    if lang.startswith("ro"):
        return RO.extract_number(text, scale=scale, ordinals=ordinals)
    if lang.startswith("ast"):
        return AST.extract_number(text, scale=scale, ordinals=ordinals)
    if lang.startswith("oc"):
        return OC.extract_number(text, scale=scale, ordinals=ordinals)
    if lang.startswith("an"):
        return AN.extract_number(text, scale=scale, ordinals=ordinals)
    if lang.startswith("ru"):
        return extract_number_ru(text, short_scale, ordinals)
    if lang.startswith("sk"):
        return extract_number_sk(text, short_scale, ordinals)
    if lang.startswith("sv"):
        return extract_number_sv(text, short_scale, ordinals)
    if lang.startswith("uk"):
        return extract_number_uk(text, short_scale, ordinals)
    if lang.startswith("hr"):
        return extract_number_hr(text, short_scale, ordinals)
    if lang.startswith("he"):
        return extract_number_he(text, ordinals)
    if lang.startswith("hu"):
        return extract_number_hu(text, short_scale, ordinals)
    if lang.startswith("sl"):
        return extract_number_sl(text, short_scale, ordinals)
    raise NotImplementedError(f"Unsupported language: '{lang}'")


def is_fractional(input_str: str, lang: str,
                  short_scale: Optional[bool] = None,  # DEPRECATED
                  scale: Optional[Scale] = None) -> Union[bool, float]:
    """
    This function takes the given text and checks if it is a fraction.
    Used by most of the number extractors.

    Will return False on phrases that *contain* a fraction. Only detects
    exact matches. To pull a fraction from a string, see extract_number()

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): DEPRECATED, use scale enum instead
        lang (str, optional): an optional BCP-47 language code, if omitted
                              the default language will be used.
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction
    """
    if not isinstance(input_str, str):
        # non-string input cannot be a fraction
        return False
    scale = _resolve_scale(lang, scale, short_scale)
    short_scale = scale == Scale.SHORT
    if lang.startswith("en"):
        return is_fractional_en(input_str, short_scale)
    if lang.startswith("az"):
        return is_fractional_az(input_str, short_scale)
    if _is_ar(lang):
        return is_fractional_ar(input_str, short_scale)
    if lang.startswith("bg"):
        return is_fractional_bg(input_str, short_scale)
    if lang.startswith("ca"):
        return CA.is_fractional(input_str)
    if lang.startswith("cs"):
        return is_fractional_cs(input_str, short_scale)
    if lang.startswith("da"):
        return is_fractional_da(input_str, short_scale)
    if lang.startswith("de"):
        return is_fractional_de(input_str, short_scale)
    if lang.startswith("el"):
        return is_fractional_el(input_str, short_scale)
    if lang.startswith("es"):
        return is_fractional_es(input_str, short_scale)
    if lang.startswith("gl"):
        return is_fractional_gl(input_str)
    if lang.startswith("eu"):
        return is_fractional_eu(input_str)
    if lang.startswith("et"):
        return is_fractional_et(input_str, short_scale)
    if lang.startswith("fi"):
        return is_fractional_fi(input_str, short_scale)
    if lang.startswith("fr"):
        return is_fractional_fr(input_str)
    if lang.startswith("id"):
        return is_fractional_id(input_str, short_scale)
    if lang.startswith("it"):
        return is_fractional_it(input_str, short_scale)
    if lang.startswith("ms"):
        return is_fractional_ms(input_str, short_scale)
    if lang.startswith("tr"):
        return is_fractional_tr(input_str, short_scale)
    if lang.startswith("kab"):
        return is_fractional_kab(input_str, short_scale)
    if lang.startswith("fy"):
        return is_fractional_fy(input_str, short_scale)
    if lang.startswith("nn"):
        return is_fractional_nn(input_str, short_scale)
    if lang.startswith("nb") or lang.startswith("no"):
        return is_fractional_nb(input_str, short_scale)
    if lang.startswith("nl"):
        return is_fractional_nl(input_str, short_scale)
    if lang.startswith("pl"):
        return is_fractional_pl(input_str, short_scale)
    if lang.startswith("pt"):
        return PT_PT.is_fractional(input_str)
    if lang.startswith("mwl"):
        return MWL.is_fractional(input_str)
    if lang.startswith("ro"):
        return RO.is_fractional(input_str)
    if lang.startswith("ast"):
        return AST.is_fractional(input_str)
    if lang.startswith("oc"):
        return OC.is_fractional(input_str)
    if lang.startswith("an"):
        return AN.is_fractional(input_str)
    if lang.startswith("ru"):
        return is_fractional_ru(input_str, short_scale)
    if lang.startswith("sk"):
        return is_fractional_sk(input_str, short_scale)
    if lang.startswith("sv"):
        return is_fractional_sv(input_str, short_scale)
    if lang.startswith("fa"):
        return is_fractional_fa(input_str, short_scale)
    if lang.startswith("hr"):
        return is_fractional_hr(input_str, short_scale)
    if lang.startswith("he"):
        return is_fractional_he(input_str, short_scale)
    if lang.startswith("hu"):
        return is_fractional_hu(input_str, short_scale)
    if lang.startswith("sl"):
        return is_fractional_sl(input_str, short_scale)
    if lang.startswith("uk"):
        return is_fractional_uk(input_str, short_scale)
    raise NotImplementedError(f"Unsupported language: '{lang}'")


def is_ordinal(input_str: str, lang: str) -> Union[bool, float]:
    """
    This function takes the given text and checks if it is an ordinal number.

    Args:
        input_str (str): the string to check if ordinal
        lang (str, optional): an optional BCP-47 language code, if omitted
                              the default language will be used.
    Returns:
        (bool) or (float): False if not an ordinal, otherwise the number
        corresponding to the ordinal
    """
    if lang.startswith("pt"):
        return PT_PT.is_ordinal(input_str)
    if lang.startswith("mwl"):
        return MWL.is_ordinal(input_str)
    if lang.startswith("ro"):
        return RO.is_ordinal(input_str)
    if lang.startswith("ast"):
        return AST.is_ordinal(input_str)
    if lang.startswith("ca"):
        return CA.is_ordinal(input_str)
    if lang.startswith("oc"):
        return OC.is_ordinal(input_str)
    if lang.startswith("an"):
        return AN.is_ordinal(input_str)
    if lang.startswith("en"):
        return is_ordinal_en(input_str)
    if _is_ar(lang):
        return is_ordinal_ar(input_str)
    if lang.startswith("de"):
        val = is_ordinal_de(input_str)
        if isinstance(val, str) and val.endswith("."):
            return int(val[:-1])
        return val
    if lang.startswith("da"):
        return is_ordinal_da(input_str)
    if lang.startswith("gl"):
        return is_ordinal_gl(input_str)
    if lang.startswith("et"):
        return is_ordinal_et(input_str)
    if lang.startswith("fi"):
        return is_ordinal_fi(input_str)
    if lang.startswith("el"):
        return is_ordinal_el(input_str)
    if lang.startswith("he"):
        return is_ordinal_he(input_str)
    if lang.startswith("eu"):
        return is_ordinal_eu(input_str)
    if lang.startswith("hu"):
        return is_ordinal_hu(input_str)
    if lang.startswith("nn"):
        return is_ordinal_nn(input_str)
    if lang.startswith("nb") or lang.startswith("no"):
        return is_ordinal_nb(input_str)
    if lang.startswith("kab"):
        return is_ordinal_kab(input_str)
    if lang.startswith("sl"):
        return is_ordinal_sl(input_str)
    return _is_ordinal_generic(input_str, lang)
