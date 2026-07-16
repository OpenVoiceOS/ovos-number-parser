from typing import Optional
from typing import Union

from unicode_rbnf import RbnfEngine, FormatPurpose

from ovos_number_parser.numbers_ast import AST
from ovos_number_parser.numbers_an import AN
from ovos_number_parser.numbers_ar import pronounce_number_ar, pronounce_ordinal_ar, extract_number_ar, \
    is_fractional_ar, is_ordinal_ar, nice_number_ar
from ovos_number_parser.numbers_az import numbers_to_digits_az, extract_number_az, is_fractional_az, pronounce_number_az
from ovos_number_parser.numbers_ca import numbers_to_digits_ca, pronounce_number_ca, is_fractional_ca, extract_number_ca
from ovos_number_parser.numbers_cs import numbers_to_digits_cs, pronounce_number_cs, is_fractional_cs, \
    extract_number_cs, pronounce_ordinal_cs
from ovos_number_parser.numbers_da import numbers_to_digits_da, pronounce_number_da, is_fractional_da, is_ordinal_da, \
    pronounce_ordinal_da, extract_number_da
from ovos_number_parser.numbers_de import numbers_to_digits_de, pronounce_number_de, pronounce_ordinal_de, \
    is_ordinal_de, is_fractional_de, extract_number_de
from ovos_number_parser.numbers_en import numbers_to_digits_en, is_ordinal_en, pronounce_number_en, extract_number_en, \
    is_fractional_en
from ovos_number_parser.numbers_es import numbers_to_digits_es, pronounce_number_es, extract_number_es, is_fractional_es
from ovos_number_parser.numbers_eu import pronounce_number_eu, extract_number_eu, is_fractional_eu, \
    pronounce_ordinal_eu
from ovos_number_parser.numbers_et import pronounce_number_et, pronounce_ordinal_et, extract_number_et, \
    is_fractional_et, is_ordinal_et, nice_number_et
from ovos_number_parser.numbers_fa import pronounce_number_fa, extract_number_fa, is_fractional_fa, \
    pronounce_ordinal_fa
from ovos_number_parser.numbers_fi import pronounce_number_fi, pronounce_ordinal_fi, extract_number_fi, \
    is_fractional_fi, is_ordinal_fi, nice_number_fi
from ovos_number_parser.numbers_fr import (pronounce_number_fr, extract_number_fr, is_fractional_fr)
from ovos_number_parser.numbers_fy import numbers_to_digits_fy, pronounce_number_fy, pronounce_ordinal_fy, \
    extract_number_fy, is_fractional_fy, nice_number_fy
from ovos_number_parser.numbers_gl import pronounce_number_gl, extract_number_gl, is_fractional_gl, \
    numbers_to_digits_gl, pronounce_ordinal_gl, is_ordinal_gl, pronounce_fraction_gl
from ovos_number_parser.numbers_hu import pronounce_number_hu, pronounce_ordinal_hu, extract_number_hu, \
    is_fractional_hu, is_ordinal_hu, nice_number_hu
from ovos_number_parser.numbers_it import (extract_number_it, pronounce_number_it, is_fractional_it)
from ovos_number_parser.numbers_kab import (pronounce_number_kab, pronounce_ordinal_kab, extract_number_kab,
                                             is_fractional_kab, is_ordinal_kab)
from ovos_number_parser.numbers_mwl import MWL
from ovos_number_parser.numbers_oc import OC
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
from ovos_number_parser.numbers_uk import numbers_to_digits_uk, pronounce_number_uk, extract_number_uk, \
    is_fractional_uk, pronounce_ordinal_uk
from ovos_number_parser.numbers_az import nice_number_az
from ovos_number_parser.numbers_ca import nice_number_ca
from ovos_number_parser.numbers_cs import nice_number_cs
from ovos_number_parser.numbers_da import nice_number_da
from ovos_number_parser.numbers_de import nice_number_de
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




# --- generic language fallbacks -------------------------------------------

_NICE_NUMBER_FNS = {
    "ar": nice_number_ar, "az": nice_number_az, "ca": nice_number_ca, "cs": nice_number_cs,
    "da": nice_number_da, "de": nice_number_de, "es": nice_number_es,
    "et": nice_number_et, "eu": nice_number_eu, "fa": nice_number_fa,
    "fi": nice_number_fi, "fr": nice_number_fr, "fy": nice_number_fy,
    "hu": nice_number_hu, "it": nice_number_it, "nl": nice_number_nl,
    "pl": nice_number_pl, "ru": nice_number_ru, "sk": nice_number_sk, "sl": nice_number_sl,
    "sv": nice_number_sv, "uk": nice_number_uk,
}

# fraction nouns take feminine numerals in the Slavic languages and the
# "két" allomorph in Hungarian
_FRACTION_NUMERATOR_OVERRIDES = {
    "ru": {1: "одна", 2: "две"},
    "uk": {1: "одна", 2: "дві"},
    "cs": {1: "jedna", 2: "dvě"},
    "sk": {1: "jedna", 2: "dve"},
    "pl": {1: "jedna", 2: "dwie"},
    "hu": {2: "két"},
}

# words that may join two spoken numbers ("vingt et un", "sto in ena")
_NUMBER_CONNECTORS = {
    "ar": {"و"}, "ca": {"i"}, "da": {"og"}, "en": {"and"}, "es": {"y"}, "eu": {"eta"},
    "fr": {"et"}, "fy": {"en"}, "it": {"e"}, "nl": {"en"}, "sv": {"och"},
    "fa": {"و"}, "sl": {"in"}, "hu": set(), "fi": set(), "et": set(),
    "kab": {"u", "d", "ed"},
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
        nice_fn = _NICE_NUMBER_FNS.get(lang2)
        if nice_fn and 2 <= n2 <= 20:
            spoken = nice_fn(n1 / n2, speech=True, denominators=[n2])
            tokens = spoken.split()
            if "/" not in spoken and \
                    not all(t.replace(",", "").replace(".", "").isdigit() for t in tokens):
                overrides = _FRACTION_NUMERATOR_OVERRIDES.get(lang2, {})
                result = " ".join(
                    overrides.get(int(t), pronounce_number(int(t), lang))
                    if t.isdigit() else t
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
    connectors = _NUMBER_CONNECTORS.get(lang2, set())
    tokens = utterance.split()

    def _clean(t):
        return t.strip(".,!?;:").lower()

    def _is_num(t):
        c = _clean(t)
        if not c:
            return False
        try:
            return extract_number(c, lang) is not False
        except NotImplementedError:
            return False

    out = []
    i = 0
    while i < len(tokens):
        if not _is_num(tokens[i]):
            out.append(tokens[i])
            i += 1
            continue
        j = i

        def _continues(next_j):
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
            return extended_val != current_val and extended_val != next_val \
                and abs(extended_val) > abs(current_val)

        while j + 1 < len(tokens):
            if _is_num(tokens[j + 1]) and _continues(j + 1):
                j += 1
            elif _clean(tokens[j + 1]) in connectors and j + 2 < len(tokens) \
                    and _is_num(tokens[j + 2]) and _continues(j + 2):
                j += 2
            else:
                break
        span = " ".join(_clean(t) for t in tokens[i:j + 1])
        val = extract_number(span, lang)
        stripped = tokens[j].rstrip(".,!?;:")
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
    if lang.startswith("ru"):
        return numbers_to_digits_ru(utterance)
    if lang.startswith("sk"):
        return numbers_to_digits_sk(utterance)
    if lang.startswith("uk"):
        return numbers_to_digits_uk(utterance)
    return _numbers_to_digits_generic(utterance, lang)


def pronounce_number(number: Union[int, float], lang: str,
                     places: int = 3,
                     short_scale: Optional[bool] = None,  # DEPRECATED
                     scientific: bool = False,
                     ordinals: bool = False,
                     digits: DigitPronunciation = DigitPronunciation.FULL_NUMBER,
                     gender: GrammaticalGender = GrammaticalGender.MASCULINE,
                     scale: Optional[Scale] = None) -> str:
    """
    Return the spoken representation of a number in the specified language.
     
    Converts a numeric value to its pronounced form, supporting various languages, decimal precision, scale (short or long), scientific notation, ordinal forms, digit pronunciation styles, and grammatical gender where applicable. Falls back to Unicode RBNF for unsupported languages.
     
    Parameters:
        number (int or float): The number to pronounce.
        lang (str): BCP-47 language code specifying the language for pronunciation.
        places (int, optional): Number of decimal places to include (default is 3).
        short_scale (bool, optional): Whether to use the short scale for large numbers (default is True).
        scientific (bool, optional): If True, pronounce the number in scientific notation.
        ordinals (bool, optional): If True, pronounce the number as an ordinal (e.g., "first" instead of "one").
        digits (DigitPronunciation, optional): Style for pronouncing digits (default is FULL_NUMBER).
        gender (GrammaticalGender, optional): Grammatical gender for languages that require it (default is MASCULINE).
     
    Returns:
        str: The pronounced form of the number.
     
    Raises:
        NotImplementedError: If the specified language is not supported.
    """
    scale = scale or Scale.SHORT
    if short_scale is not None:
        # TODO log warning
        pass
    short_scale = scale == Scale.SHORT
    if lang.startswith("en"):
        return pronounce_number_en(number, places, short_scale, scientific, ordinals)
    if lang.startswith("az"):
        return pronounce_number_az(number, places, short_scale, scientific, ordinals)
    if lang.startswith("ar"):
        return pronounce_number_ar(number, places, scientific, ordinals)
    if lang.startswith("ca"):
        return pronounce_number_ca(number, places)
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
        return pronounce_number_gl(number, places)
    if lang.startswith("es"):
        return pronounce_number_es(number, places)
    if lang.startswith("eu"):
        return pronounce_number_eu(number, places)
    if lang.startswith("et"):
        return pronounce_number_et(number, places, short_scale, scientific, ordinals)
    if lang.startswith("fa"):
        return pronounce_number_fa(number, places, scientific, ordinals)
    if lang.startswith("fi"):
        return pronounce_number_fi(number, places, short_scale, scientific, ordinals)
    if lang.startswith("fr"):
        return pronounce_number_fr(number, places)
    if lang.startswith("hu"):
        return pronounce_number_hu(number, places, short_scale, scientific, ordinals)
    if lang.startswith("it"):
        return pronounce_number_it(number, places, short_scale, scientific)
    if lang.startswith("kab"):
        return pronounce_number_kab(number, places, ordinals, gender)
    if lang.startswith("fy"):
        return pronounce_number_fy(number, places, short_scale, scientific, ordinals)
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
    scale = scale or Scale.SHORT
    if short_scale is not None:
        # TODO log warning
        pass
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
    if lang.startswith("oc"):
        return OC.pronounce_ordinal(number, scale=scale, gender=gender)
    if lang.startswith("an"):
        return AN.pronounce_ordinal(number, scale=scale, gender=gender)
    if lang.startswith("ar"):
        return pronounce_ordinal_ar(number)
    if lang.startswith("da"):
        return pronounce_ordinal_da(number)
    if lang.startswith("de"):
        return pronounce_ordinal_de(number)
    if lang.startswith("et"):
        return pronounce_ordinal_et(number)
    if lang.startswith("fi"):
        return pronounce_ordinal_fi(number)
    if lang.startswith("hu"):
        return pronounce_ordinal_hu(number)
    if lang.startswith("fy"):
        return pronounce_ordinal_fy(number)
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


def extract_number(text: str, lang: str,
                   short_scale: Optional[bool] = None,  # DEPRECATED
                   ordinals: bool = False,
                   scale: Optional[Scale] = None) -> Union[int, float, bool]:
    """Takes in a string and extracts a number.

    Assumes only 1 number is in the string, does NOT handle multiple numbers

    Args:
        text (str): the string to extract a number from
        short_scale (bool): Use "short scale" or "long scale" for large
            numbers -- over a million.  The default is short scale, which
            is now common in most English speaking countries.
            See https://en.wikipedia.org/wiki/Names_of_large_numbers
        ordinals (bool): consider ordinal numbers, e.g. third=3 instead of 1/3
        lang (str, optional): an optional BCP-47 language code, if omitted
                              the default language will be used.
    Returns:
        (int, float or False): The number extracted or False if the input
                               text contains no numbers
    """
    scale = scale or Scale.SHORT
    if short_scale is not None:
        # TODO log warning
        pass
    short_scale = scale == Scale.SHORT
    if lang.startswith("en"):
        return extract_number_en(text, short_scale, ordinals)
    if lang.startswith("az"):
        return extract_number_az(text, short_scale, ordinals)
    if lang.startswith("ar"):
        return extract_number_ar(text, ordinals)
    if lang.startswith("ca"):
        return extract_number_ca(text, short_scale, ordinals)
    if lang.startswith("cs"):
        return extract_number_cs(text, short_scale, ordinals)
    if lang.startswith("da"):
        return extract_number_da(text, short_scale, ordinals)
    if lang.startswith("de"):
        return extract_number_de(text, short_scale, ordinals)
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
    if lang.startswith("it"):
        return extract_number_it(text, short_scale, ordinals)
    if lang.startswith("kab"):
        return extract_number_kab(text, short_scale, ordinals)
    if lang.startswith("fy"):
        return extract_number_fy(text, short_scale, ordinals)
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
    scale = scale or Scale.SHORT
    if short_scale is not None:
        # TODO log warning
        pass
    short_scale = scale == Scale.SHORT
    if lang.startswith("en"):
        return is_fractional_en(input_str, short_scale)
    if lang.startswith("az"):
        return is_fractional_az(input_str, short_scale)
    if lang.startswith("ar"):
        return is_fractional_ar(input_str, short_scale)
    if lang.startswith("ca"):
        return is_fractional_ca(input_str, short_scale)
    if lang.startswith("cs"):
        return is_fractional_cs(input_str, short_scale)
    if lang.startswith("da"):
        return is_fractional_da(input_str, short_scale)
    if lang.startswith("de"):
        return is_fractional_de(input_str, short_scale)
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
    if lang.startswith("it"):
        return is_fractional_it(input_str, short_scale)
    if lang.startswith("kab"):
        return is_fractional_kab(input_str, short_scale)
    if lang.startswith("fy"):
        return is_fractional_fy(input_str, short_scale)
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
    if lang.startswith("oc"):
        return OC.is_ordinal(input_str)
    if lang.startswith("an"):
        return AN.is_ordinal(input_str)
    if lang.startswith("en"):
        return is_ordinal_en(input_str)
    if lang.startswith("ar"):
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
    if lang.startswith("hu"):
        return is_ordinal_hu(input_str)
    if lang.startswith("kab"):
        return is_ordinal_kab(input_str)
    if lang.startswith("sl"):
        return is_ordinal_sl(input_str)
    return _is_ordinal_generic(input_str, lang)
