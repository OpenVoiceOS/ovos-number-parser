"""Values whose ``str()`` uses exponent notation read their digits in full.

``str(1e-05)`` is ``"1e-05"`` and ``str(1e16)`` is ``"1e+16"``, so a backend
that splits ``str(number)`` on the decimal point finds no fractional part, or
reads the letter "e" as a digit. The expected readings are composed from the
integer readings of each digit, which do not pass through that code.
"""
import pytest

from ovos_number_parser import pronounce_number

#: the word each language speaks for the decimal separator after a zero
_DECIMAL_WORD = {
    "az": "nöqtə",
    "bg": "запетая",
    "cs": "tečka",
    "en": "point",
    "et": "koma",
    "fi": "pilkku",
    "hr": "zarez",
    "id": "koma",
    "it": "virgola",
    "ms": "koma",
    "pl": "przecinek",
    "ru": "точка",
    "sk": "celá",
    "sl": "celih",
    "tr": "virgül",
    "uk": "крапка",
}

#: languages that read a positive value below 1e-4 digit by digit; the others
#: read it scientifically and only their negative reading is digit by digit
_DIGIT_READING = ("bg", "en", "et", "fi", "id", "it", "ms", "ru")


def _minus(lang):
    return pronounce_number(-1, lang).rsplit(" ", 1)[0]


def _reading(lang, whole, digits):
    return " ".join([pronounce_number(whole, lang), _DECIMAL_WORD[lang]]
                    + [pronounce_number(int(d), lang) for d in digits])


@pytest.mark.parametrize("lang", _DIGIT_READING)
@pytest.mark.parametrize("value, places, digits", [
    (1e-05, 5, "00001"),
    (1e-05, 8, "00001"),
    (1.5e-05, 6, "000015"),
    (1e-07, 7, "0000001"),
])
def test_small_fraction_reads_each_digit(lang, value, places, digits):
    assert pronounce_number(value, lang, places=places) == \
        _reading(lang, 0, digits)


@pytest.mark.parametrize("lang", sorted(_DECIMAL_WORD))
def test_small_negative_fraction_reads_each_digit(lang):
    assert pronounce_number(-1e-05, lang, places=5) == \
        _minus(lang) + " " + _reading(lang, 0, "00001")


@pytest.mark.parametrize("lang", ("et", "fi"))
def test_whole_part_with_small_fraction(lang):
    assert pronounce_number(3.00001, lang, places=5) == \
        _reading(lang, 3, "00001")


@pytest.mark.parametrize("lang", ("et", "fi"))
@pytest.mark.parametrize("value", [10 ** 16, 15 * 10 ** 16, 10 ** 22])
def test_large_float_matches_integer_reading(lang, value):
    assert pronounce_number(float(value), lang) == pronounce_number(value, lang)
