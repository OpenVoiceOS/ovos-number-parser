from typing import Union

from ovos_number_parser.numbers_az import numbers_to_digits_az, extract_number_az, is_fractional_az, pronounce_number_az
from ovos_number_parser.numbers_ca import pronounce_number_ca, is_fractional_ca, extract_number_ca
from ovos_number_parser.numbers_cs import numbers_to_digits_cs, pronounce_number_cs, is_fractional_cs, extract_number_cs
from ovos_number_parser.numbers_da import is_fractional_da, is_ordinal_da, pronounce_number_da, \
    pronounce_ordinal_da, extract_number_da
from ovos_number_parser.numbers_de import numbers_to_digits_de, pronounce_number_de, pronounce_ordinal_de, \
    is_ordinal_de, is_fractional_de, extract_number_de
from ovos_number_parser.numbers_en import numbers_to_digits_en, is_ordinal_en, pronounce_number_en, extract_number_en, \
    is_fractional_en
from ovos_number_parser.numbers_es import numbers_to_digits_es, pronounce_number_es, extract_number_es, is_fractional_es
from ovos_number_parser.numbers_eu import pronounce_number_eu, extract_number_eu, is_fractional_eu
from ovos_number_parser.numbers_fa import pronounce_number_fa, extract_number_fa
from ovos_number_parser.numbers_fr import (pronounce_number_fr, extract_number_fr, is_fractional_fr)
from ovos_number_parser.numbers_hu import pronounce_number_hu, pronounce_ordinal_hu
from ovos_number_parser.numbers_it import (extract_number_it, pronounce_number_it, is_fractional_it)
from ovos_number_parser.numbers_nl import numbers_to_digits_nl, pronounce_number_nl, pronounce_ordinal_nl, \
    extract_number_nl, is_fractional_nl
from ovos_number_parser.numbers_pl import numbers_to_digits_pl, pronounce_number_pl, extract_number_pl, is_fractional_pl
from ovos_number_parser.numbers_pt import numbers_to_digits_pt, pronounce_number_pt, is_fractional_pt, extract_number_pt
from ovos_number_parser.numbers_ru import numbers_to_digits_ru, pronounce_number_ru, extract_number_ru, is_fractional_ru
from ovos_number_parser.numbers_sv import pronounce_number_sv, pronounce_ordinal_sv, extract_number_sv, \
    is_fractional_sv
from ovos_number_parser.numbers_uk import numbers_to_digits_uk, pronounce_number_uk, extract_number_uk, is_fractional_uk
from ovos_number_parser.numbers_sl import nice_number_sl, pronounce_number_sl


def numbers_to_digits(utterance: str, lang: str) -> str:
    """
    Replace written numbers in text with their digit equivalents.

    Args:
        utterance (str): Input string possibly containing written numbers.

    Returns:
        str: Text with written numbers replaced by digits.
    """
    if lang.startswith("az"):
        return numbers_to_digits_az(utterance)
    if lang.startswith("cs"):
        return numbers_to_digits_cs(utterance)
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
        return numbers_to_digits_pt(utterance)
    if lang.startswith("ru"):
        return numbers_to_digits_ru(utterance)
    if lang.startswith("uk"):
        return numbers_to_digits_uk(utterance)
    raise NotImplementedError(f"Unsupported language: '{lang}'")


def pronounce_number(number: Union[int, float], lang: str, places: int = 2, short_scale: bool = True,
                     scientific: bool = False, ordinals: bool = False) -> str:
    """
    Convert a number to it's spoken equivalent

    For example, '5' would be 'five'

    Args:
        number: the number to pronounce
        lang (str, optional): an optional BCP-47 language code, if omitted
                              the default language will be used.
        places (int): number of decimal places to express, default 2
        short_scale (bool) : use short (True) or long scale (False)
            https://en.wikipedia.org/wiki/Names_of_large_numbers
        scientific (bool) : convert and pronounce in scientific notation
        ordinals (bool): pronounce in ordinal form "first" instead of "one"
    Returns:
        (str): The pronounced number
    """
    if lang.startswith("en"):
        return pronounce_number_en(number, places, short_scale, scientific, ordinals)
    if lang.startswith("az"):
        return pronounce_number_az(number, places, short_scale, scientific, ordinals)
    if lang.startswith("ca"):
        return pronounce_number_ca(number, places)
    if lang.startswith("cs"):
        return pronounce_number_en(number, places, short_scale, scientific, ordinals)
    if lang.startswith("da"):
        return pronounce_number_da(number, places, short_scale, scientific, ordinals)
    if lang.startswith("de"):
        return pronounce_number_de(number, places, short_scale, scientific, ordinals)
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
        return pronounce_number_pt(number, places)
    if lang.startswith("ru"):
        return pronounce_number_ru(number, places, short_scale, scientific, ordinals)
    if lang.startswith("sl"):
        return pronounce_number_sl(number, places, short_scale, scientific, ordinals)
    if lang.startswith("sv"):
        return pronounce_number_sv(number, places, short_scale, scientific, ordinals)
    if lang.startswith("uk"):
        return pronounce_number_uk(number, places, short_scale, scientific, ordinals)
    raise NotImplementedError(f"Unsupported language: '{lang}'")


def pronounce_ordinal(number: Union[int, float], lang: str, short_scale: bool = True) -> str:
    """
    Convert an ordinal number to it's spoken equivalent

    For example, '5' would be 'fifth'

    Args:
        number: the number to pronounce
        lang (str, optional): an optional BCP-47 language code, if omitted
                              the default language will be used.
        short_scale (bool) : use short (True) or long scale (False)
            https://en.wikipedia.org/wiki/Names_of_large_numbers
    Returns:
        (str): The pronounced number
    """
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
    raise NotImplementedError(f"Unsupported language: '{lang}'")


def extract_number(text: str, lang: str, short_scale: bool = True, ordinals: bool = False) -> Union[int, float, bool]:
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
        return extract_number_pt(text, short_scale, ordinals)
    if lang.startswith("ru"):
        return extract_number_ru(text, short_scale, ordinals)
    if lang.startswith("sv"):
        return extract_number_sv(text, short_scale, ordinals)
    if lang.startswith("uk"):
        return extract_number_uk(text, short_scale, ordinals)
    raise NotImplementedError(f"Unsupported language: '{lang}'")


def is_fractional(input_str: str, lang: str, short_scale: bool = True) -> Union[bool, float]:
    """
    This function takes the given text and checks if it is a fraction.
    Used by most of the number exractors.

    Will return False on phrases that *contain* a fraction. Only detects
    exact matches. To pull a fraction from a string, see extract_number()

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): use short scale if True, long scale if False
        lang (str, optional): an optional BCP-47 language code, if omitted
                              the default language will be used.
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction
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
        return is_fractional_pt(input_str, short_scale)
    if lang.startswith("ru"):
        return is_fractional_ru(input_str, short_scale)
    if lang.startswith("sv"):
        return is_fractional_sv(input_str, short_scale)
    if lang.startswith("uk"):
        return is_fractional_uk(input_str, short_scale)
    raise NotImplementedError(f"Unsupported languags: '{lang}'")


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
    if lang.startswith("en"):
        return is_ordinal_en(input_str)
    if lang.startswith("de"):
        return is_ordinal_de(input_str)
    if lang.startswith("da"):
        return is_ordinal_da(input_str)
    raise NotImplementedError(f"Unsupported languags: '{lang}'")
