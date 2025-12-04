from typing import Union

from unicode_rbnf import RbnfEngine, FormatPurpose

from ovos_number_parser.numbers_az import numbers_to_digits_az, extract_number_az, is_fractional_az, pronounce_number_az
from ovos_number_parser.numbers_ca import numbers_to_digits_ca, pronounce_number_ca, is_fractional_ca, extract_number_ca
from ovos_number_parser.numbers_cs import numbers_to_digits_cs, pronounce_number_cs, is_fractional_cs, extract_number_cs
from ovos_number_parser.numbers_da import numbers_to_digits_da, pronounce_number_da, is_fractional_da, is_ordinal_da, \
    pronounce_ordinal_da, extract_number_da
from ovos_number_parser.numbers_de import numbers_to_digits_de, pronounce_number_de, pronounce_ordinal_de, \
    is_ordinal_de, is_fractional_de, extract_number_de
from ovos_number_parser.numbers_en import numbers_to_digits_en, is_ordinal_en, pronounce_number_en, extract_number_en, \
    is_fractional_en
from ovos_number_parser.numbers_es import numbers_to_digits_es, pronounce_number_es, extract_number_es, is_fractional_es
from ovos_number_parser.numbers_ast import AST
from ovos_number_parser.numbers_eu import pronounce_number_eu, extract_number_eu, is_fractional_eu
from ovos_number_parser.numbers_fa import pronounce_number_fa, extract_number_fa
from ovos_number_parser.numbers_fr import (pronounce_number_fr, extract_number_fr, is_fractional_fr)
from ovos_number_parser.numbers_gl import pronounce_number_gl, extract_number_gl, is_fractional_gl, numbers_to_digits_gl
from ovos_number_parser.numbers_hu import pronounce_number_hu, pronounce_ordinal_hu
from ovos_number_parser.numbers_it import (extract_number_it, pronounce_number_it, is_fractional_it)
from ovos_number_parser.numbers_nl import numbers_to_digits_nl, pronounce_number_nl, pronounce_ordinal_nl, \
    extract_number_nl, is_fractional_nl
from ovos_number_parser.numbers_pl import numbers_to_digits_pl, pronounce_number_pl, extract_number_pl, is_fractional_pl
from ovos_number_parser.numbers_pt import PortugueseVariant, PT_PT, PT_BR
from ovos_number_parser.numbers_mwl import MWL
from ovos_number_parser.numbers_ru import numbers_to_digits_ru, pronounce_number_ru, extract_number_ru, is_fractional_ru
from ovos_number_parser.numbers_sl import pronounce_number_sl
from ovos_number_parser.numbers_sv import pronounce_number_sv, pronounce_ordinal_sv, extract_number_sv, \
    is_fractional_sv
from ovos_number_parser.numbers_uk import numbers_to_digits_uk, pronounce_number_uk, extract_number_uk, is_fractional_uk
from ovos_number_parser.util import Scale, GrammaticalGender, DigitPronunciation


def numbers_to_digits(utterance: str, lang: str, scale: Scale = Scale.LONG) -> str:
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
    if lang.startswith("az"):
        return numbers_to_digits_az(utterance)
    if lang.startswith("ast"):
        return AST.numbers_to_digits(utterance)
    if lang.startswith("ca"):
        return numbers_to_digits_ca(utterance)
    if lang.startswith("gl"):
        return numbers_to_digits_gl(utterance)
    if lang.startswith("cs"):
        return numbers_to_digits_cs(utterance)
    if lang.startswith("da"):
        return numbers_to_digits_da(utterance)
    if lang.startswith("de"):
        return numbers_to_digits_de(utterance)
    if lang.startswith("en"):
        return numbers_to_digits_en(utterance)
    if lang.startswith("es"):
        return numbers_to_digits_es(utterance)
    if lang.startswith("nl"):
        return numbers_to_digits_nl(utterance)
    if lang.startswith("pl"):
        return numbers_to_digits_pl(utterance)
    if lang.startswith("pt"):
        return PT_PT.numbers_to_digits(utterance, scale=scale)
    if lang.startswith("mwl"):
        return MWL.numbers_to_digits(utterance, scale=scale)
    if lang.startswith("ru"):
        return numbers_to_digits_ru(utterance)
    if lang.startswith("uk"):
        return numbers_to_digits_uk(utterance)
    raise NotImplementedError(f"Unsupported language: '{lang}'")


def pronounce_number(number: Union[int, float], lang: str,
                     places: int = 3,
                     short_scale: bool = True,
                     scientific: bool = False, ordinals: bool = False,
                     digits: DigitPronunciation = DigitPronunciation.FULL_NUMBER,
                     gender: GrammaticalGender = GrammaticalGender.MASCULINE) -> str:
    """
                     Produce the spoken form of a number in the specified language.
                     
                     Parameters:
                         number (int | float): Number to be pronounced.
                         lang (str): BCP-47 language code selecting the pronunciation language/variant.
                         places (int): Maximum decimal places to include for fractional numbers (default 3).
                         short_scale (bool): Use short scale naming for large numbers when True, long scale when False.
                         scientific (bool): If True, format/pronounce the number in scientific notation when appropriate.
                         ordinals (bool): If True, produce the ordinal form (e.g., "first" instead of "one").
                         digits (DigitPronunciation): Controls how individual digits are spoken (e.g., full numbers vs digit-by-digit).
                         gender (GrammaticalGender): Grammatical gender to use for languages that require gendered forms.
                     
                     Returns:
                         str: The pronounced representation of the number in the target language.
                     
                     Raises:
                         NotImplementedError: If no implementation or fallback is available for the requested language.
                     """
    scale = Scale.SHORT if short_scale else Scale.LONG  # TODO migrate function kwarg to accept Scale enum
    if lang.startswith("en"):
        return pronounce_number_en(number, places, short_scale, scientific, ordinals)
    if lang.startswith("az"):
        return pronounce_number_az(number, places, short_scale, scientific, ordinals)
    if lang.startswith("ca"):
        return pronounce_number_ca(number, places)
    if lang.startswith("ast"):
        return AST.pronounce_number(number, places, scale, ordinals, digits, gender)
    if lang.startswith("cs"):
        return pronounce_number_en(number, places, short_scale, scientific, ordinals)
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
    if lang.startswith("fa"):
        return pronounce_number_fa(number, places, scientific, ordinals)
    if lang.startswith("fr"):
        return pronounce_number_fr(number, places)
    if lang.startswith("hu"):
        return pronounce_number_hu(number, places, short_scale, scientific, ordinals)
    if lang.startswith("it"):
        return pronounce_number_it(number, places, short_scale, scientific)
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
    if lang.startswith("ru"):
        return pronounce_number_ru(number, places, short_scale, scientific, ordinals)
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


def pronounce_fraction(fraction_word: str, lang: str, scale: Scale = Scale.LONG) -> str:
    """
    Produce the spoken form of a fraction (e.g., "3/2" -> "three halves") for the given language and numerical scale.
    
    Parameters:
        fraction_word (str): Fraction in "numerator/denominator" form.
        lang (str): Language code; supports Portuguese variants ("pt" with "br" for PT_BR or PT_PT), Asturian ("ast"), and Mirandese ("mwl").
        scale (Scale, optional): Numerical scale to use (SHORT or LONG). Defaults to LONG.
    
    Returns:
        str: The pronounced fraction.
    
    Raises:
        NotImplementedError: If the specified language is not supported.
    """
    if lang.startswith("pt"):
        return PT_BR.pronounce_fraction(fraction_word, scale=scale) if "br" in lang.lower() \
            else  PT_PT.pronounce_fraction(fraction_word, scale=scale)
    elif lang.startswith("ast"):
        return AST.pronounce_fraction(fraction_word, scale=scale)
    elif lang.startswith("mwl"):
        return MWL.pronounce_fraction(fraction_word, scale=scale)
    else:
        raise NotImplementedError(f"unsupported language: {lang}")


def pronounce_ordinal(number: Union[int, float], lang: str,
                      short_scale: bool = True,
                      gender: GrammaticalGender = GrammaticalGender.MASCULINE) -> str:
    """
                      Produce the spoken ordinal form of a number in the specified language.
                      
                      Parameters:
                          number (int | float): Number to convert to its ordinal spoken form.
                          lang (str): BCP-47 language code specifying the target language (may include region variants, e.g., "pt-BR").
                          short_scale (bool): Use short scale for large number names when True, long scale when False.
                          gender (GrammaticalGender): Grammatical gender to use for languages that inflect ordinals by gender.
                      
                      Returns:
                          str: The ordinal pronunciation of the number in the requested language.
                      
                      Raises:
                          NotImplementedError: If the language is not supported and no fallback is available.
                      """
    scale = Scale.SHORT if short_scale else Scale.LONG  # TODO migrate function kwarg to accept Scale enum
    if lang.startswith("pt"):
        return PT_BR.pronounce_ordinal(number, scale=scale, gender=gender) if "br" in lang.lower() \
            else  PT_PT.pronounce_ordinal(number, scale=scale, gender=gender)
    if lang.startswith("mwl"):
        return MWL.pronounce_ordinal(number, scale=scale, gender=gender)
    if lang.startswith("ast"):
        return AST.pronounce_ordinal(number, scale=scale, gender=gender)
    if lang.startswith("da"):
        return pronounce_ordinal_da(number)
    if lang.startswith("de"):
        return pronounce_ordinal_de(number)
    if lang.startswith("hu"):
        return pronounce_ordinal_hu(number)
    if lang.startswith("nl"):
        return pronounce_ordinal_nl(number)
    if lang.startswith("sv"):
        return pronounce_ordinal_sv(number)
    # fallback to unicode RBNF
    try:
        engine = RbnfEngine.for_language(lang.split("-")[0])
        fmt = FormatPurpose.ORDINAL
        return engine.format_number(number, fmt).text
    except Exception as err:
        raise NotImplementedError(f"Unsupported language: '{lang}'") from err


def extract_number(text: str, lang: str, short_scale: bool = True, ordinals: bool = False) -> Union[int, float, bool]:
    """
    Extracts a single numeric value from a text string for a given language.
    
    Parses the input text and returns the numeric value represented by the first (and assumed only) number in the string. Language-specific parsing rules are applied; use `short_scale=False` to interpret large-number names using the long scale. If `ordinals` is True, ordinal words (e.g., "third") are interpreted as their corresponding numbers.
    
    Parameters:
        text (str): The string to extract a number from.
        lang (str): BCP-47 language code used to select language-specific parsing.
        short_scale (bool): When True (default), interpret large-number names using the short scale; when False, use the long scale.
        ordinals (bool): When True, treat ordinal words as numbers (e.g., "third" -> 3).
    
    Returns:
        int, float, or bool: The extracted number as an int or float, or `False` if no number is found.
    
    Raises:
        NotImplementedError: If the specified language is not supported.
    """
    scale = Scale.SHORT if short_scale else Scale.LONG  # TODO migrate function kwarg to accept Scale enum
    if lang.startswith("en"):
        return extract_number_en(text, short_scale, ordinals)
    if lang.startswith("az"):
        return extract_number_az(text, short_scale, ordinals)
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
    if lang.startswith("fa"):
        return extract_number_fa(text, ordinals)
    if lang.startswith("fr"):
        return extract_number_fr(text, short_scale, ordinals)
    if lang.startswith("it"):
        return extract_number_it(text, short_scale, ordinals)
    if lang.startswith("nl"):
        return extract_number_nl(text, short_scale, ordinals)
    if lang.startswith("pl"):
        return extract_number_pl(text, short_scale, ordinals)
    if lang.startswith("pt"):
        return PT_BR.extract_number(text, scale=scale, ordinals=ordinals)  if "br" in lang.lower() \
            else PT_PT.extract_number(text, scale=scale, ordinals=ordinals)
    if lang.startswith("mwl"):
        return MWL.extract_number(text, scale=scale, ordinals=ordinals)
    if lang.startswith("ast"):
        return AST.extract_number(text, scale=scale, ordinals=ordinals)
    if lang.startswith("ru"):
        return extract_number_ru(text, short_scale, ordinals)
    if lang.startswith("sv"):
        return extract_number_sv(text, short_scale, ordinals)
    if lang.startswith("uk"):
        return extract_number_uk(text, short_scale, ordinals)
    raise NotImplementedError(f"Unsupported language: '{lang}'")


def is_fractional(input_str: str, lang: str, short_scale: bool = True) -> Union[bool, float]:
    """
    Determine whether the input string exactly represents a fraction for the given language.
    
    Parameters:
        input_str (str): Text to check for an exact fractional representation.
        lang (str): BCP-47 language code used to select language-specific parsing rules.
        short_scale (bool): Use short scale when interpreting large-number names; True for short scale, False for long scale.
    
    Returns:
        Union[bool, float]: `False` if the input is not an exact fraction; otherwise the numeric value of the fraction as a `float`.
    """
    if lang.startswith("en"):
        return is_fractional_en(input_str, short_scale)
    if lang.startswith("az"):
        return is_fractional_az(input_str, short_scale)
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
        return is_fractional_gl(input_str, short_scale)
    if lang.startswith("eu"):
        return is_fractional_eu(input_str)
    if lang.startswith("fr"):
        return is_fractional_fr(input_str)
    if lang.startswith("it"):
        return is_fractional_it(input_str, short_scale)
    if lang.startswith("nl"):
        return is_fractional_pl(input_str, short_scale)
    if lang.startswith("pl"):
        return is_fractional_pl(input_str, short_scale)
    if lang.startswith("pt"):
        return PT_PT.is_fractional(input_str)
    if lang.startswith("mwl"):
        return MWL.is_fractional(input_str)
    if lang.startswith("ast"):
        return AST.is_fractional(input_str)
    if lang.startswith("ru"):
        return is_fractional_ru(input_str, short_scale)
    if lang.startswith("sv"):
        return is_fractional_sv(input_str, short_scale)
    if lang.startswith("uk"):
        return is_fractional_uk(input_str, short_scale)
    raise NotImplementedError(f"Unsupported languags: '{lang}'")


def is_ordinal(input_str: str, lang: str) -> Union[bool, float]:
    """
    Determine whether a string represents an ordinal and return its numeric value.
    
    Parameters:
        input_str (str): Text to evaluate for ordinal form.
        lang (str): BCP-47 language code used to interpret the input.
    
    Returns:
        Union[bool, float]: The numeric value of the ordinal if recognized, `False` otherwise.
    """
    if lang.startswith("pt"):
        return PT_PT.is_ordinal(input_str)
    if lang.startswith("mwl"):
        return MWL.is_ordinal(input_str)
    if lang.startswith("ast"):
        return AST.is_ordinal(input_str)
    if lang.startswith("en"):
        return is_ordinal_en(input_str)
    if lang.startswith("de"):
        return is_ordinal_de(input_str)
    if lang.startswith("da"):
        return is_ordinal_da(input_str)
    raise NotImplementedError(f"Unsupported languags: '{lang}'")