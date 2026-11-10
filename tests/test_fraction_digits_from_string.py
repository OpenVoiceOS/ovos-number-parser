"""Fractional digits are read from the decimal string of the value.

Reading a digit as ``int(fraction * 10 ** k) % 10`` misreads values whose
binary float lies just below the decimal one: 44.29 - 44 is 0.2899999...,
so the second digit came out as eight and 44.28 and 44.29 sounded alike.
The expected readings are composed from ``pronounce_number`` of the whole
part and of each single digit, independently of the fractional reader.
"""

import pytest

from ovos_number_parser import pronounce_number

#: the word each language speaks for the decimal separator
_DECIMAL_WORD = {
    "da": "komma",
    "de": "Komma",
    "fy": "komma",
    "nb": "komma",
    "nn": "komma",
    "nl": "komma",
    "sv": "komma",
}

#: pairs that read alike when the digits come from float arithmetic
_PAIRS = [(0.28, 0.29), (0.56, 0.57), (1.28, 1.29), (1.56, 1.57),
          (44.28, 44.29), (44.56, 44.57), (999.28, 999.29), (999.57, 999.58)]

#: value, places and the fractional digits that must be read
_COMPOSED = [("44.28", 2, "28"), ("44.29", 2, "29"), ("44.56", 2, "56"),
             ("44.57", 2, "57"), ("999.57", 2, "57"), ("999.58", 2, "58"),
             ("44.29", 3, "290"), ("0.29", 4, "2900")]


def _tail(lang, digits):
    return " ".join([_DECIMAL_WORD[lang]]
                    + [pronounce_number(int(d), lang) for d in digits])


@pytest.mark.parametrize("lang", sorted(_DECIMAL_WORD))
@pytest.mark.parametrize("low,high", _PAIRS)
def test_neighbouring_decimals_read_differently(lang, low, high):
    assert pronounce_number(low, lang, places=2) != \
        pronounce_number(high, lang, places=2)


@pytest.mark.parametrize("lang", sorted(_DECIMAL_WORD))
@pytest.mark.parametrize("value,places,digits", _COMPOSED)
def test_reading_is_whole_part_then_each_digit(lang, value, places, digits):
    whole = int(value.split(".")[0])
    expected = pronounce_number(whole, lang) + " " + _tail(lang, digits)
    if whole == 0 and lang == "da":
        # Danish speaks no zero before the separator ("komma fem nul nul"
        # for 0.5, as test_number_parser_da pins)
        expected = _tail(lang, digits)
    assert pronounce_number(float(value), lang, places=places) == expected
