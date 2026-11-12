import difflib
import math
import re
import sys
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from fractions import Fraction
from numbers import Real
from os.path import commonprefix
from typing import List
from typing import Optional
from typing import Union

from unicode_rbnf import RbnfEngine, FormatPurpose

from ovos_number_parser.numbers_ast import AST
from ovos_number_parser.numbers_an import AN
from ovos_number_parser.numbers_ar import pronounce_number_ar, pronounce_ordinal_ar, extract_number_ar, \
    extract_numbers_ar, numbers_to_digits_ar, \
    is_fractional_ar, is_ordinal_ar, nice_number_ar, resolve_ar_lang, resolve_ar_lect
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
                                           is_fractional_es, fraction_noun_es, ES)
from ovos_number_parser.numbers_eu import pronounce_number_eu, extract_number_eu, is_fractional_eu, \
    pronounce_ordinal_eu, is_ordinal_eu
from ovos_number_parser.numbers_et import pronounce_number_et, pronounce_ordinal_et, extract_number_et, \
    is_fractional_et, is_ordinal_et, nice_number_et
from ovos_number_parser.numbers_fa import pronounce_number_fa, extract_number_fa, is_fractional_fa, \
    pronounce_ordinal_fa
from ovos_number_parser.numbers_fi import pronounce_number_fi, pronounce_ordinal_fi, extract_number_fi, \
    is_fractional_fi, is_ordinal_fi, nice_number_fi
from ovos_number_parser.numbers_fr import (extract_number_fr, is_fractional_fr, FR,
                                             FR_BE, FR_CH)
from ovos_number_parser.numbers_fy import numbers_to_digits_fy, pronounce_number_fy, pronounce_ordinal_fy, \
    extract_number_fy, is_fractional_fy, nice_number_fy
from ovos_number_parser.numbers_gl import GL, pronounce_number_gl, extract_number_gl, is_fractional_gl, \
    numbers_to_digits_gl, pronounce_ordinal_gl, is_ordinal_gl, pronounce_fraction_gl
from ovos_number_parser.numbers_hr import pronounce_number_hr, pronounce_ordinal_hr, extract_number_hr, \
    is_fractional_hr, nice_number_hr, numbers_to_digits_hr
from ovos_number_parser.numbers_he import pronounce_number_he, pronounce_ordinal_he, \
    extract_number_he, is_fractional_he, is_ordinal_he, nice_number_he, numbers_to_digits_he
from ovos_number_parser.numbers_hu import pronounce_number_hu, pronounce_ordinal_hu, extract_number_hu, \
    is_fractional_hu, is_ordinal_hu, nice_number_hu, pronounce_scientific_hu
from ovos_number_parser.numbers_id import (pronounce_number_id, pronounce_number_ms,
                                           pronounce_ordinal_id, pronounce_ordinal_ms,
                                           extract_number_id, extract_number_ms,
                                           is_fractional_id, is_fractional_ms,
                                           nice_number_id, nice_number_ms,
                                           numbers_to_digits_id, numbers_to_digits_ms)
from ovos_number_parser.numbers_it import (extract_number_it, pronounce_number_it, is_fractional_it, IT)
from ovos_number_parser.numbers_kab import (pronounce_number_kab, pronounce_ordinal_kab, extract_number_kab,
                                             is_fractional_kab, is_ordinal_kab, numbers_to_digits_kab)
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
from ovos_number_parser.util import Scale, GrammaticalGender, DigitPronunciation, fits_str_limit, \
    scientific_parts, round_half_up


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
    lang2 = _base_lang(lang)
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
    "et": set(), "kab": {"u", "d", "ed"}, "he": {"ו"},
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
        minus = _minus_word(lang)
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


def _is_ordinal_generic(input_str: str, lang: str):
    """Fallback ordinal detection via reverse lookup over pronounce_ordinal."""
    return _ordinal_reverse_table(lang).get(input_str.lower().strip(), False)


_WESTERN_DIGITS = "0123456789"
_EASTERN_ARABIC_DIGITS = "٠١٢٣٤٥٦٧٨٩"
_PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
# numbers_to_digits emits Western digits, so the two non-Western scripts are
# translated character-for-character — never through int(), which would
# destroy leading zeros.
_TO_WESTERN_DIGITS = str.maketrans(_EASTERN_ARABIC_DIGITS + _PERSIAN_DIGITS,
                                   _WESTERN_DIGITS * 2)
_DIGIT_CHARS = frozenset(_WESTERN_DIGITS + _EASTERN_ARABIC_DIGITS + _PERSIAN_DIGITS)


def _is_digit_run(token: str) -> bool:
    """True if the token is one or more digit characters and nothing else."""
    return bool(token) and all(c in _DIGIT_CHARS for c in token)


def _numbers_to_digits_generic(utterance: str, lang: str,
                               continues=None, first_number_words=None) -> str:
    """Fallback that replaces spoken number spans with digits using
    extract_number over maximal runs of number words.

    ``continues`` is an optional predicate for a word that is no number by
    itself but can extend a number already started; the span takes it only
    when the value of the span grows.

    ``first_number_words`` is an optional reader for a language whose own parser
    says where one number ends and the next begins: handed the words of a run of
    number words, it returns how many of them the first number covers, or None.
    The span never grows past it, since growth by value alone joins two numbers
    whenever the joined value happens to be larger ("عشرين ست مية" is 20 and 600,
    not 26 and 100).
    """
    lang2 = _base_lang(lang)
    connectors = _NUMBER_CONNECTORS.get("ar" if _is_ar(lang) else lang2, set())
    tokens = utterance.split()
    # ASCII plus Arabic comma, semicolon and question mark, so a number glued
    # to punctuation ("٢٠٢٤،", "25.") is still recognised and the mark is
    # carried over onto the digits instead of being dropped
    punct = ".,!?;:؟،؛"

    def _clean(t):
        return t.strip(punct).lower()

    #: token -> answer, for the two readers below. Both are pure functions
    #: of the token, and both are asked the same question about the same
    #: token more than once: the Arabic pre-scan walks a run of number words
    #: with ``_may_extend`` before the main loop walks the same run again.
    #: Without this every token in an Arabic number run is read twice, and
    #: ``extract_number`` is the expensive half of each read.
    _is_num_cache = {}
    #: token -> extract_number of the whole token, kept by ``_is_num``
    _value_cache = {}
    _may_extend_cache = {}

    def _is_num(t):
        cached = _is_num_cache.get(t)
        if cached is not None:
            return cached
        _is_num_cache[t] = answer = _is_num_uncached(t)
        return answer

    def _is_num_uncached(t):
        c = _clean(t)
        if not c:
            return False
        try:
            _value_cache[t] = extract_number(c, lang)
            if _value_cache[t] is False:
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

    _denominator_cache = {}

    def _denominator(t):
        """The n of a word read as the reciprocal 1/n, n >= 2, else None.

        Most languages spell the denominator of a fraction with the ordinal
        ("un sixième", "drie vierde"), so ``extract_number`` reads a lone
        ordinal as its reciprocal: "le sixième sens" would become
        "le 0.16666666666666666 sens". Digits ("0.25", "1/4") are no word.
        """
        if t in _denominator_cache:
            return _denominator_cache[t]
        answer = None
        c = _clean(t)
        if _is_num(t) and not any(ch.isdigit() for ch in c):
            val = _value_cache.get(t)
            if isinstance(val, (int, float)) and not isinstance(val, bool) \
                    and 0 < val < 1:
                n = round(1 / val)
                if n >= 2 and abs(1 / val - n) < 1e-9:
                    answer = n
        _denominator_cache[t] = answer
        return answer

    def _is_denominator_of(i, j, next_j):
        """tokens[next_j] is the denominator of a proper fraction whose
        numerator is the cardinal tokens[i:j + 1] ("trois quarts" = 0.75).

        The numerator must be a whole number smaller than the denominator:
        "vingt cinquième" is the twenty-fifth, not 20 * 1/5.
        """
        n = _denominator(tokens[next_j])
        if n is None:
            return False
        current = " ".join(_clean(t) for t in tokens[i:j + 1])
        current_val = extract_number(current, lang)
        if isinstance(current_val, bool) or \
                not isinstance(current_val, (int, float)) or \
                current_val != int(current_val) or not 0 < current_val < n:
            return False
        extended = " ".join(_clean(t) for t in tokens[i:next_j + 1])
        extended_val = extract_number(extended, lang)
        return isinstance(extended_val, (int, float)) \
            and not isinstance(extended_val, bool) \
            and abs(extended_val - current_val / n) < 1e-9

    out = []
    i = 0
    while i < len(tokens):
        # a lone ordinal or denominator ("sixième", "derde") is a word, not
        # the fraction 1/n; one half is still 0.5
        if not _is_num(tokens[i]) or (_denominator(tokens[i]) or 0) >= 3:
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

        def _may_extend(t):
            cached = _may_extend_cache.get(t)
            if cached is not None:
                return cached
            answer = _is_num(t) or bool(continues and continues(_clean(t)))
            _may_extend_cache[t] = answer
            return answer

        limit = len(tokens) - 1
        if first_number_words:
            end = i
            while end + 1 < len(tokens) and (
                    _may_extend(tokens[end + 1]) or
                    _clean(tokens[end + 1]) in connectors and end + 2 < len(tokens)
                    and _may_extend(tokens[end + 2])):
                end += 1
            covered = first_number_words([_clean(t) for t in tokens[i:end + 1]])
            if covered:
                limit = i + covered - 1

        while j + 1 < len(tokens):
            if j + 1 > limit:
                break
            if _denominator(tokens[j + 1]) is not None:
                # a denominator joins only as such, and ends the number
                if _is_denominator_of(i, j, j + 1):
                    j += 1
                break
            if _may_extend(tokens[j + 1]) and _continues(j + 1):
                j += 1
            elif _clean(tokens[j + 1]) in connectors and j + 2 <= limit \
                    and _may_extend(tokens[j + 2]) \
                    and _continues(j + 2, via_connector=True):
                j += 2
            else:
                break
        stripped = tokens[j].rstrip(punct)
        trail = tokens[j][len(stripped):]
        single_token = i == j
        if single_token and _is_digit_run(_clean(tokens[i])):
            # Already digits ("007", "٠٥٥٣١٧٥٨١٧"): keep every character.
            # Re-reading through extract_number would go via int() and strip
            # leading zeros — corrupting phone numbers, OTP codes and other
            # zero-padded identifiers. Digit runs are only re-read when they
            # combine with neighbouring number words ("355 ألف" → 355000),
            # which is the multi-token branch below.
            out.append(_clean(tokens[i]).translate(_TO_WESTERN_DIGITS) + trail)
        else:
            span = " ".join(_clean(t) for t in tokens[i:j + 1])
            val = extract_number(span, lang)
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
    converted = _number_words_to_digits(utterance, lang, scale)
    if _base_lang(lang) in ("nb", "nn", "no"):
        # nb and nn keep the output of their converter
        return converted
    return _keep_digit_strings(utterance, converted, lang, scale)


#: a number already written in digits, with the punctuation that may follow it
_DIGIT_STRING = re.compile(r"[-+]?(?:[0-9][0-9.,]*|[.,][0-9]+)(?:[eE][-+]?[0-9]+)?[.,!?;:]*")
_DIGIT_VALUE = re.compile(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")


def _keep_digit_strings(original: str, converted: str, lang: str,
                        scale: Optional[Scale]) -> str:
    """Put back the digit strings that a converter rewrote.

    Only number words become digits: "Version 2.0" and "10.000 Euro" stay as
    written. A rewritten stretch is restored when it held digit strings and
    no number word, and the rewrite added no sign ("5 og 20" stays, "minus 5"
    becomes "-5", "5 tusen," becomes "5000,", "2 point 5" becomes "2.5").
    """
    old, new = original.split(), converted.split()
    out = []
    matcher = difflib.SequenceMatcher(
        a=[w.casefold() for w in old], b=[w.casefold() for w in new],
        autojunk=False)
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        before, after = old[i1:i2], new[j1:j2]
        digits = [w for w in before if _DIGIT_STRING.fullmatch(w)]
        values = [w.rstrip(".,!?;:") for w in after]
        if op == "replace" and digits and \
                all(_DIGIT_VALUE.fullmatch(v) for v in values) and \
                (float(values[0]) < 0) == digits[0].startswith("-") and \
                not any(w not in digits and _is_number_word(w, lang, scale)
                        for w in before):
            out += before
        else:
            out += after
    return " ".join(out)


def _is_number_word(word: str, lang: str, scale: Optional[Scale]) -> bool:
    """Whether a word reads as a number, or joins two digits into one
    decimal ("point" in "2 point 5")."""
    word = word.strip(_SPAN_PUNCTUATION)
    return _numeric_value(word, lang, None, True, scale) is not None or \
        _numeric_value(f"2 {word} 5", lang, None, False, scale) == 2.5


def _number_words_to_digits(utterance: str, lang: str,
                            scale: Optional[Scale]) -> str:
    """Dispatch to the converter of the language."""
    scale = _resolve_scale(lang, scale)
    lang2 = _base_lang(lang)
    if lang2 == "en":
        # English has its own converter, which reads compound ordinals
        # ("the twenty fifth" -> 25) and never mistakes a singular ordinal for a
        # fraction. The generic fallback did neither.
        return numbers_to_digits_en(utterance, short_scale=scale == Scale.SHORT)
    if lang2 == "ast":
        return AST.numbers_to_digits(utterance)
    if lang2 == "oc":
        return OC.numbers_to_digits(utterance, scale=scale)
    if lang2 == "an":
        return AN.numbers_to_digits(utterance)
    if lang2 == "fy":
        return numbers_to_digits_fy(utterance)
    if lang2 == "gl":
        return numbers_to_digits_gl(utterance)
    if lang2 == "de":
        return numbers_to_digits_de(utterance)
    if lang2 == "pt":
        return PT_BR.numbers_to_digits(utterance, scale=scale) if "br" in lang.lower() \
            else PT_PT.numbers_to_digits(utterance, scale=scale)
    if lang2 == "mwl":
        return MWL.numbers_to_digits(utterance, scale=scale)
    if lang2 == "ro":
        return RO.numbers_to_digits(utterance, scale=scale)
    if lang2 == "bg":
        return numbers_to_digits_bg(utterance)
    if lang2 == "hr":
        return numbers_to_digits_hr(utterance)
    if lang2 == "ru":
        return numbers_to_digits_ru(utterance)
    if lang2 == "sk":
        return numbers_to_digits_sk(utterance)
    if lang2 == "id":
        return numbers_to_digits_id(utterance)
    if lang2 == "ms":
        return numbers_to_digits_ms(utterance)
    if lang2 == "tr":
        return numbers_to_digits_tr(utterance)
    if lang2 == "uk":
        return numbers_to_digits_uk(utterance)
    if _is_ar(lang):
        return numbers_to_digits_ar(utterance, lang)
    if lang2 == "kab":
        return numbers_to_digits_kab(utterance)
    if lang2 == "he":
        return numbers_to_digits_he(utterance)
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

    A finite ``Decimal`` is rounded from its own digits and comes back as the
    int or float the backends read, so it reads as the float written with the
    same digits. A Decimal with no fraction digits ("12", "1E+30"), or an
    integral one a float cannot hold exactly, becomes an int with every digit.
    A non-integral Decimal with more significant digits than a float holds
    after rounding reads as the nearest float.
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


#: individual languages that the IANA Language Subtag Registry places inside a
#: macrolanguage and that share the written standard of its module
_MACROLANGUAGE_MEMBERS = {"azj": "az", "ekk": "et", "pes": "fa", "zsm": "ms"}


def _base_lang(lang: str) -> str:
    """Bare language code, so "pt-BR", "pt_BR" and "PT" resolve to "pt"."""
    base = lang.lower().replace("_", "-").split("-")[0]
    return _MACROLANGUAGE_MEMBERS.get(base, base)


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


def _has_padded_scale_words(spoken: str, lang: str) -> bool:
    """
    Whether a backend padded a magnitude by repeating its largest scale word.

    Some backends do not raise past their named-scale table; they repeat the
    biggest word they know until the magnitude is covered
    ("trilioi trilioi trilioi", "sextiliões vigintiliões vigintiliões").
    No natural numeral repeats a scale word back to back, so two identical
    adjacent words other than digit words mark output that is not a reading.

    A digit word repeats legitimately where digits are read one by one: the
    mantissa of a scientific reading ("jedan zarez jedan jedan puta deset na
    četiristo") or a digit-by-digit decimal ("dois vírgula dois dois").
    """
    digit_words = {pronounce_number(digit, lang) for digit in range(10)}
    words = spoken.split()
    return any(a == b and a not in digit_words
               for a, b in zip(words, words[1:]))


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
    connective = _SCIENTIFIC_WORDS.get("ar" if _is_ar(lang) else _base_lang(lang),
                                       _SCIENTIFIC_WORDS["en"])
    return f"{mantissa_words} {connective} {exponent_words}"


#: languages whose backend reads ``scientific=True`` in a scientific form of
#: its own, keyed by bare language code; Arabic lects are matched by _is_ar
_SCIENTIFIC_MODE = frozenset({
    "az", "bg", "cs", "el", "en", "fa", "he", "hr", "id", "it", "ms", "pl",
    "ru", "sk", "sl", "tr", "uk"})

#: a value below the quantum whose first significant digit lies further right
#: than this many decimals reads in scientific form: 10 ** -323 is the
#: smallest power of ten whose nine multiples a float holds digit for digit
_MOST_PLACES = 323


def _has_scientific_mode(lang: str) -> bool:
    """Whether the backend for ``lang`` honours ``scientific=True``."""
    return _is_ar(lang) or _base_lang(lang) in _SCIENTIFIC_MODE


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
    """
    Return the spoken representation of a number in the specified language.
     
    Converts a numeric value to its pronounced form, supporting various languages, decimal precision, scale (short or long), scientific notation, ordinal forms, digit pronunciation styles, and grammatical gender where applicable. Falls back to Unicode RBNF for unsupported languages.
     
    Parameters:
        number (int or float): The number to pronounce. A ``decimal.Decimal``
            reads as the float written with the same digits, and an integral
            one as the int with the same digits, and a Decimal below the
            float range keeps its digit and its sign. Any other
            ``numbers.Real`` (numpy float32) reads as the float its ``str()``
            writes, and a ``fractions.Fraction`` is rounded from its exact
            value. A number with more than 4300 integer digits reads in the
            scientific form in every language except Kabyle, which raises
            OverflowError past its ceiling of 9999, and ValueError for a
            negative number.
        lang (str): BCP-47 language code specifying the language for pronunciation.
        places (int, optional): Number of decimal places to include (default is 3).
            The fractional part is rounded to this precision half away from zero
            before pronunciation, following ISO 80000-1 (Quantities and units --
            General) and NIST SP 811 (2008 ed.) Appendix B.7 on the rounding of
            numerical values; rounding that carries into the integer part is
            spoken as such (0.999999 at 2 places -> "one"). A non-zero value
            that would round to zero reads up to its first significant digit,
            rounded the same way, with its sign (0.00012 at 3 places -> "zero
            point zero zero zero one"). When that digit lies past the 323rd
            decimal, the value reads in scientific form ("five times ten to
            the power of minus three hundred and twenty four" for 5e-324). At
            0 places a value that rounds to zero reads as the zero word alone.
        short_scale (bool, optional): DEPRECATED, use the ``scale`` enum instead.
        scientific (bool, optional): If True, pronounce the number in
            scientific notation where the language has a scientific reading
            (ar az bg cs el en fa he hr id it ms pl ru sk sl tr uk); other
            languages ignore it. ``places`` then counts the mantissa decimals,
            rounded once, half away from zero, from the exact digits (12.3449
            at 3 places -> "one point two three four times ten to the power
            of one").
        ordinals (bool, optional): If True, pronounce the number as an ordinal (e.g., "first" instead of "one").
        digits (DigitPronunciation, optional): Style for pronouncing digits (default is FULL_NUMBER).
        gender (GrammaticalGender, optional): Grammatical gender for languages that require it (default is MASCULINE).
        scale (Scale, optional): Short or long scale for large numbers. When
            omitted, the language's canonical convention applies (see
            ``_canonical_scale``), per Wikipedia "Long and short scales"
            (https://en.wikipedia.org/wiki/Long_and_short_scales); an explicit
            value always overrides it.
        case (str, optional): Grammatical case/register, currently only
            meaningful for Arabic ("nominative" or "oblique", with
            "genitive" and "accusative" as names for the oblique; any other
            value raises ValueError, see ``pronounce_number_ar``). When
            omitted, a cardinal in the Arabic lect named by ``lang`` uses
            that lect's default register (see
            ``numbers_ar.resolve_ar_lang``) and an ordinal the nominative;
            ignored for every other language.

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
        return _pronounce_infinity(number, lang)
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
    if _is_ar(lang):
        # a lect's default register applies to cardinals; an ordinal takes
        # the oblique only when the caller asks for it
        if case is None:
            case = "nominative" if ordinals else _ar_default_case(lang)
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
        return pronounce_number_it(number, places, short_scale, scientific)
    if lang2 == "kab":
        return pronounce_number_kab(number, places, ordinals, gender)
    if lang2 == "fy":
        return pronounce_number_fy(number, places, short_scale, scientific, ordinals)
    if lang2 == "nn":
        return pronounce_number_nn(number, places, short_scale, scientific, ordinals)
    if lang2 in ("nb", "no"):
        return pronounce_number_nb(number, places, short_scale, scientific, ordinals,
                                   gender=gender)
    if lang2 == "nl":
        return pronounce_number_nl(number, places, short_scale, scientific, ordinals)
    if lang2 == "pl":
        return pronounce_number_pl(number, places, short_scale, scientific, ordinals,
                                   gender=gender)
    if lang2 == "pt":
        if "br" in lang.lower():
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


#: the locales unicode_rbnf ships rules for: a bare language ("sr") or a
#: language with a script or region subtag ("sr_Latn", "zh_Hant", "de_CH")
_RBNF_LOCALES = frozenset(RbnfEngine.get_supported_languages())


def _rbnf_locale(lang: str) -> str:
    """The unicode_rbnf locale that reads ``lang``.

    A script or region subtag selects its own rules where unicode_rbnf ships
    them, in either separator and any letter case ("sr-Latn", "sr_latn"); any
    other tag reads with the rules of its bare language.
    """
    base = _base_lang(lang)
    for subtag in lang.replace("_", "-").split("-")[1:]:
        locale = f"{base}_{subtag.title() if len(subtag) == 4 else subtag.upper()}"
        if locale in _RBNF_LOCALES:
            return locale
    return base


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
    minus word of the same rule set, because the engine reads only the
    integer part of a negative number (``int(-number)`` in
    ``RbnfEngine.iter_format_number``). The minus word is the reading of -1
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
        engine = RbnfEngine.for_language(locale)
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
    text = text.translate(_RBNF_CHARACTER_FIXES.get(locale, {}))
    for wrong, right in _RBNF_SCRIPT_FIXES.get(base, {}).items():
        text = text.replace(wrong, right)
    fixes = _RBNF_WORD_FIXES.get(locale, {})
    return " ".join(fixes.get(word, word) for word in text.split(" "))


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
    lang2 = _base_lang(lang)
    if lang2 == "pt":
        return PT_BR.pronounce_fraction(fraction_word, scale=scale) if "br" in lang.lower() \
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
        return pronounce_fraction_gl(fraction_word, scale=scale)
    elif lang2 == "ro":
        return RO.pronounce_fraction(fraction_word, scale=scale)
    else:
        return _pronounce_fraction_generic(fraction_word, lang)


def pronounce_ordinal(number: Union[int, float], lang: str,
                      short_scale: Optional[bool] = None,  # DEPRECATED
                      gender: GrammaticalGender = GrammaticalGender.MASCULINE,
                      scale: Optional[Scale] = None,
                      case: Optional[str] = None) -> str:
    """
    Return the spoken ordinal form of a number in the specified language.
      
    Parameters:
        number (int or float): The number to convert to its ordinal spoken equivalent.
            A ``decimal.Decimal`` or ``fractions.Fraction`` reads as its int
            when it is integral and as its float otherwise; one past the
            float range is rounded half away from zero to its int. Any other
            ``numbers.Real`` (numpy float32) reads as the number its ``str()``
            writes.
        lang (str): BCP-47 language code specifying the language for pronunciation.
        short_scale (bool, optional): Whether to use the short (True) or long (False) scale for large numbers. Defaults to True.
        gender (GrammaticalGender, optional): Grammatical gender to use for languages that require it. Defaults to masculine.
        case (str, optional): Grammatical case, only meaningful for Arabic
            (None or "nominative", "oblique", "genitive", "accusative"; see
            ``numbers_ar.pronounce_ordinal_ar``); ignored for every other
            language.
      
    Returns:
        str: The ordinal number pronounced in the specified language.
      
    Raises:
        NotImplementedError: If the language is not supported.
        ValueError: If ``number`` is a Decimal of more than 4300 integer
            digits, which no int conversion reaches in reasonable time.
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
        return PT_BR.pronounce_ordinal(number, scale=scale, gender=gender) if "br" in lang.lower() \
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
    if _is_ar(lang):
        return pronounce_ordinal_ar(number, gender=gender, case=case)
    if lang2 == "da":
        return pronounce_ordinal_da(number, gender)
    if lang2 == "de":
        return pronounce_ordinal_de(number)
    if lang2 == "et":
        return pronounce_ordinal_et(number)
    if lang2 == "es" and (isinstance(number, int) or number.is_integer()) \
            and abs(number) < 10 ** 24:
        # the Castilian engine has no ordinal scale word from 10**24 up
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
    if lang2 == "ms":
        return pronounce_ordinal_ms(number)
    if lang2 == "tr":
        return pronounce_ordinal_tr(number)
    if lang2 == "fy":
        return pronounce_ordinal_fy(number)
    if lang2 == "nn":
        return pronounce_ordinal_nn(number)
    if lang2 in ("nb", "no"):
        return pronounce_ordinal_nb(number)
    if lang2 == "nl":
        return pronounce_ordinal_nl(number)
    if lang2 == "sv":
        return pronounce_ordinal_sv(number)
    if lang2 == "gl":
        return pronounce_ordinal_gl(number, gender=gender, scale=scale)
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
    if lang2 == "ru" and number and (
            isinstance(number, int) or isinstance(number, float) and number.is_integer()) \
            and abs(number) < 10 ** 24:
        # the Russian engine has no ordinal scale word from 10**24 up
        return pronounce_number(number, lang, ordinals=True, gender=gender, scale=scale)
    # fallback to unicode RBNF
    return _pronounce_rbnf(number, lang, True, gender)


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
    if _base_lang(lang) in _HYPHENATED_NUMERAL_LANGS:
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
    value = _extract_number(text, lang, short_scale, ordinals, scale)
    # an integer that str() cannot write is no number, as a digit string
    # longer than the integer string conversion limit is none
    return value if fits_str_limit(value) else False


def _extract_number(text: str, lang: str, short_scale: Optional[bool],
                    ordinals: bool, scale: Optional[Scale]) -> Union[int, float, bool]:
    """The number ``extract_number`` reads, before the integer size check."""
    if not isinstance(text, str):
        # non-string input carries no number to extract
        return False
    text = _unglue_compound_numerals(text, lang)
    scale = _resolve_scale(lang, scale, short_scale)
    short_scale = scale == Scale.SHORT
    lang2 = _base_lang(lang)
    if lang2 == "en":
        return extract_number_en(text, short_scale, ordinals)
    if lang2 == "az":
        return extract_number_az(text, short_scale, ordinals)
    if _is_ar(lang):
        return extract_number_ar(text, ordinals, lect=resolve_ar_lect(lang))
    if lang2 == "bg":
        return extract_number_bg(text, short_scale, ordinals)
    if lang2 == "ca":
        return CA.extract_number(text, ordinals=ordinals, scale=scale)
    if lang2 == "cs":
        return extract_number_cs(text, short_scale, ordinals)
    if lang2 == "da":
        return extract_number_da(text, short_scale, ordinals)
    if lang2 == "de":
        return extract_number_de(text, short_scale, ordinals)
    if lang2 == "el":
        return extract_number_el(text, ordinals)
    if lang2 == "es":
        return extract_number_es(text, short_scale, ordinals)
    if lang2 == "gl":
        return extract_number_gl(text, short_scale, ordinals)
    if lang2 == "eu":
        return extract_number_eu(text, short_scale, ordinals)
    if lang2 == "et":
        return extract_number_et(text, short_scale, ordinals)
    if lang2 == "fa":
        return extract_number_fa(text, ordinals)
    if lang2 == "fi":
        return extract_number_fi(text, short_scale, ordinals)
    if lang2 == "fr":
        return extract_number_fr(text, short_scale, ordinals)
    if lang2 == "id":
        return extract_number_id(text, short_scale, ordinals)
    if lang2 == "it":
        return extract_number_it(text, short_scale, ordinals)
    if lang2 == "ms":
        return extract_number_ms(text, short_scale, ordinals)
    if lang2 == "tr":
        return extract_number_tr(text, short_scale, ordinals)
    if lang2 == "kab":
        return extract_number_kab(text, short_scale, ordinals)
    if lang2 == "fy":
        return extract_number_fy(text, short_scale, ordinals)
    if lang2 == "nn":
        return extract_number_nn(text, short_scale, ordinals)
    if lang2 in ("nb", "no"):
        return extract_number_nb(text, short_scale, ordinals)
    if lang2 == "nl":
        return extract_number_nl(text, short_scale, ordinals)
    if lang2 == "pl":
        return extract_number_pl(text, short_scale, ordinals)
    if lang2 == "pt":
        return PT_BR.extract_number(text, scale=scale, ordinals=ordinals) if "br" in lang.lower() \
            else PT_PT.extract_number(text, scale=scale, ordinals=ordinals)
    if lang2 == "mwl":
        return MWL.extract_number(text, scale=scale, ordinals=ordinals)
    if lang2 == "ro":
        return RO.extract_number(text, scale=scale, ordinals=ordinals)
    if lang2 == "ast":
        return AST.extract_number(text, scale=scale, ordinals=ordinals)
    if lang2 == "oc":
        return OC.extract_number(text, scale=scale, ordinals=ordinals)
    if lang2 == "an":
        return AN.extract_number(text, scale=scale, ordinals=ordinals)
    if lang2 == "ru":
        return extract_number_ru(text, short_scale, ordinals)
    if lang2 == "sk":
        return extract_number_sk(text, short_scale, ordinals)
    if lang2 == "sv":
        return extract_number_sv(text, short_scale, ordinals)
    if lang2 == "uk":
        return extract_number_uk(text, short_scale, ordinals)
    if lang2 == "hr":
        return extract_number_hr(text, short_scale, ordinals)
    if lang2 == "he":
        return extract_number_he(text, ordinals)
    if lang2 == "hu":
        return extract_number_hu(text, short_scale, ordinals)
    if lang2 == "sl":
        return extract_number_sl(text, short_scale, ordinals)
    raise NotImplementedError(f"Unsupported language: '{lang}'")


@dataclass(frozen=True)
class NumberSpan:
    """A number found in an utterance, together with where it was written.

    ``start`` and ``end`` are half-open code-point offsets into the utterance
    the span was extracted from, so ``utterance[start:end] == surface`` holds.
    """
    start: int
    end: int
    surface: str
    value: Union[int, float]


#: characters that punctuate a word without belonging to it; a leading or
#: trailing run of these is not part of a number's surface ("at 7," -> "7")
_SPAN_PUNCTUATION = "\"'`´.,;:!?¡¿…()[]{}<>«»“”‘’"


def _word_spans(text: str) -> List[tuple]:
    """Offsets of the whitespace separated words, stripped of edge punctuation."""
    spans = []
    for match in re.finditer(r"\S+", text):
        start, end = match.span()
        while start < end and text[end - 1] in _SPAN_PUNCTUATION:
            end -= 1
        while start < end and text[start] in _SPAN_PUNCTUATION:
            start += 1
        if start < end:
            spans.append((start, end))
    return spans


def _numeric_value(fragment: str, lang: str, short_scale: Optional[bool],
                   ordinals: bool, scale: Optional[Scale]) -> Optional[Union[int, float]]:
    """The number a fragment spells, or None when it spells none.

    Extractors report "no number" as either ``False`` or ``None`` depending on
    the language, and ``0`` is a legitimate value, so the falsiness of the
    return value cannot be used to tell the two apart.
    """
    value = extract_number(fragment, lang, short_scale=short_scale,
                           ordinals=ordinals, scale=scale)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return value


def _reads_as_one_number(fragment: str, lang: str,
                         scale: Optional[Scale]) -> bool:
    """Whether a fragment spells a single number rather than several.

    A fragment whose value is fully explained by its tail is ambiguous: the
    tail may be the whole number, with the leading word absorbed into it
    ("one hundred"), or a second number that the extractor happened to answer
    with ("two three"). Rewriting the fragment to digits tells the two apart,
    because the rewrite keeps every number it recognises: "one hundred"
    becomes "100" and "two three" becomes "2 3".

    The Arabic converter glues the conjunction onto the digits after it
    ("7 و500"), where the count cannot see the second number, so across
    "و" the Arabic extractor decides how many numbers the fragment holds.
    """
    numbers = glued = 0
    for token in numbers_to_digits(fragment, lang, scale=scale).split():
        token = token.strip(_SPAN_PUNCTUATION)
        if _is_ar(lang) and token[:1] == "و":
            token, glued = token[1:], True
        try:
            float(token)
        except ValueError:
            continue
        numbers += 1
    if glued:
        return len(extract_numbers_ar(fragment,
                                      lect=resolve_ar_lect(lang))) == 1
    return numbers == 1


def extract_number_spans(text: str, lang: str,
                         short_scale: Optional[bool] = None,  # DEPRECATED
                         ordinals: bool = False,
                         scale: Optional[Scale] = None) -> List[NumberSpan]:
    """Extract every number in a text together with the text it occupies.

    Each span covers a whole number phrase, so "two hundred and five", "3.5"
    and "twenty-two" are one span each, and two numbers in one sentence are
    two spans. Spans never overlap and come back sorted by ``start``.

    Words are grown into a number phrase greedily: starting from a word that
    spells a number on its own, the next word joins the phrase while the
    language's extractor keeps reading a *different* value out of the longer
    phrase. A word that leaves the value unchanged joins only as a single
    connector ("two hundred *and* five"), and only when it does not spell a
    number itself, which is what keeps "seven and nine" two spans. The first
    word must also keep contributing: an extractor asked to read an incoherent
    fragment such as "two three" answers with one of the numbers in it, so a
    longer phrase whose value is fully explained by its own tail is rejected
    and the first word becomes a span of its own ("two three hundred" is 2 and
    300). A phrase stops at any punctuation between two words. Each word takes
    part in a bounded number of extractor calls, making the whole scan linear
    in the length of the text in practice.

    Args:
        text: the utterance to scan.
        lang: BCP-47 language code.
        short_scale: DEPRECATED, use the ``scale`` enum instead.
        ordinals: also read ordinals as numbers, e.g. third=3.
        scale: short/long scale convention; defaults to the language's own.

    Returns:
        The numbers found, in the order they are written.
    """
    if not isinstance(text, str):
        return []

    words = _word_spans(text)
    spans = []
    index = 0
    while index < len(words):
        start = words[index][0]
        value = _numeric_value(text[start:words[index][1]], lang, short_scale,
                               ordinals, scale)
        if value is None:
            index += 1
            continue

        last = index
        cursor = index
        connector_used = crossed_connector = False
        while cursor + 1 < len(words) and \
                not text[words[cursor][1]:words[cursor + 1][0]].strip():
            nxt = words[cursor + 1]
            grown = _numeric_value(text[start:nxt[1]], lang, short_scale,
                                   ordinals, scale)
            word = _numeric_value(text[nxt[0]:nxt[1]], lang, short_scale,
                                  ordinals, scale)
            suffix = _numeric_value(text[words[index + 1][0]:nxt[1]], lang,
                                    short_scale, ordinals, scale)
            if grown is not None and grown != value and \
                    not (connector_used and grown == word) and \
                    (grown != suffix or _reads_as_one_number(text[start:nxt[1]],
                                                             lang, scale)):
                crossed_connector = crossed_connector or connector_used
                value, last, connector_used = grown, cursor + 1, False
            elif connector_used or word is not None:
                # in a span that holds a connector, a number word that
                # leaves the value unchanged may open the rest of a mixed
                # number: "two and three quarters" is 2 + 3/4. The whole
                # stretch must convert to one number, so "two hundred and one
                # one third" ("201 0.333…") stays two numbers. Arabic
                # writes its "و" onto the next word ("سبعة وخمسة مئة").
                after = words[cursor + 2] if cursor + 2 < len(words) else None
                glued_and = _is_ar(lang) and text.startswith("و", nxt[0])
                if not (connector_used or crossed_connector or glued_and) or \
                        word is None or grown != value or \
                        after is None or text[nxt[1]:after[0]].strip():
                    break
                whole = text[start:after[1]]
                longer = _numeric_value(whole, lang, short_scale, ordinals,
                                        scale)
                if longer is None or longer == value:
                    break
                if _is_ar(lang):
                    if not _reads_as_one_number(whole, lang, scale):
                        break
                elif len(numbers_to_digits(whole, lang, scale=scale).split()) != 1:
                    break
                crossed_connector = crossed_connector or connector_used
                value, last, connector_used = longer, cursor + 2, False
                cursor += 1
            else:
                connector_used = True
            cursor += 1

        end = words[last][1]
        spans.append(NumberSpan(start, end, text[start:end], value))
        index = last + 1
    return spans


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
    lang2 = _base_lang(lang)
    if lang2 == "en":
        return is_fractional_en(input_str, short_scale)
    if lang2 == "az":
        return is_fractional_az(input_str, short_scale)
    if _is_ar(lang):
        return is_fractional_ar(input_str, short_scale)
    if lang2 == "bg":
        return is_fractional_bg(input_str, short_scale)
    if lang2 == "ca":
        return CA.is_fractional(input_str)
    if lang2 == "cs":
        return is_fractional_cs(input_str, short_scale)
    if lang2 == "da":
        return is_fractional_da(input_str, short_scale)
    if lang2 == "de":
        return is_fractional_de(input_str, short_scale)
    if lang2 == "el":
        return is_fractional_el(input_str, short_scale)
    if lang2 == "es":
        return is_fractional_es(input_str, short_scale)
    if lang2 == "gl":
        return is_fractional_gl(input_str)
    if lang2 == "eu":
        return is_fractional_eu(input_str)
    if lang2 == "et":
        return is_fractional_et(input_str, short_scale)
    if lang2 == "fi":
        return is_fractional_fi(input_str, short_scale)
    if lang2 == "fr":
        return is_fractional_fr(input_str)
    if lang2 == "id":
        return is_fractional_id(input_str, short_scale)
    if lang2 == "it":
        return is_fractional_it(input_str, short_scale)
    if lang2 == "ms":
        return is_fractional_ms(input_str, short_scale)
    if lang2 == "tr":
        return is_fractional_tr(input_str, short_scale)
    if lang2 == "kab":
        return is_fractional_kab(input_str, short_scale)
    if lang2 == "fy":
        return is_fractional_fy(input_str, short_scale)
    if lang2 == "nn":
        return is_fractional_nn(input_str, short_scale)
    if lang2 in ("nb", "no"):
        return is_fractional_nb(input_str, short_scale)
    if lang2 == "nl":
        return is_fractional_nl(input_str, short_scale)
    if lang2 == "pl":
        return is_fractional_pl(input_str, short_scale)
    if lang2 == "pt":
        return PT_PT.is_fractional(input_str)
    if lang2 == "mwl":
        return MWL.is_fractional(input_str)
    if lang2 == "ro":
        return RO.is_fractional(input_str)
    if lang2 == "ast":
        return AST.is_fractional(input_str)
    if lang2 == "oc":
        return OC.is_fractional(input_str)
    if lang2 == "an":
        return AN.is_fractional(input_str)
    if lang2 == "ru":
        return is_fractional_ru(input_str, short_scale)
    if lang2 == "sk":
        return is_fractional_sk(input_str, short_scale)
    if lang2 == "sv":
        return is_fractional_sv(input_str, short_scale)
    if lang2 == "fa":
        return is_fractional_fa(input_str, short_scale)
    if lang2 == "hr":
        return is_fractional_hr(input_str, short_scale)
    if lang2 == "he":
        return is_fractional_he(input_str, short_scale)
    if lang2 == "hu":
        return is_fractional_hu(input_str, short_scale)
    if lang2 == "sl":
        return is_fractional_sl(input_str, short_scale)
    if lang2 == "uk":
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
    lang2 = _base_lang(lang)
    if lang2 == "pt":
        return PT_PT.is_ordinal(input_str)
    if lang2 == "mwl":
        return MWL.is_ordinal(input_str)
    if lang2 == "ro":
        return RO.is_ordinal(input_str)
    if lang2 == "ast":
        return AST.is_ordinal(input_str)
    if lang2 == "ca":
        return CA.is_ordinal(input_str)
    if lang2 == "oc":
        return OC.is_ordinal(input_str)
    if lang2 == "an":
        return AN.is_ordinal(input_str)
    if lang2 == "en":
        return is_ordinal_en(input_str)
    if _is_ar(lang):
        return is_ordinal_ar(input_str)
    if lang2 == "de":
        val = is_ordinal_de(input_str)
        if isinstance(val, str) and val.endswith("."):
            return int(val[:-1])
        return val
    if lang2 == "da":
        return is_ordinal_da(input_str)
    if lang2 == "gl":
        return is_ordinal_gl(input_str)
    if lang2 == "et":
        return is_ordinal_et(input_str)
    if lang2 == "fi":
        return is_ordinal_fi(input_str)
    if lang2 == "el":
        return is_ordinal_el(input_str)
    if lang2 == "he":
        return is_ordinal_he(input_str)
    if lang2 == "eu":
        return is_ordinal_eu(input_str)
    if lang2 == "hu":
        return is_ordinal_hu(input_str)
    if lang2 == "nn":
        return is_ordinal_nn(input_str)
    if lang2 in ("nb", "no"):
        return is_ordinal_nb(input_str)
    if lang2 == "kab":
        return is_ordinal_kab(input_str)
    if lang2 == "sl":
        return is_ordinal_sl(input_str)
    return _is_ordinal_generic(input_str, lang)
