"""Every language reads the same value the same way.

A value below the ``places`` quantum reads up to its first significant digit,
rounded half away from zero, with its sign. A scientific mantissa rounds half
away from zero and carries into the exponent. Each expected reading comes from
a reading that does not pass through the changed code: the language's reading
of an equivalent value at enough places, integer readings of the digits, or
the reading of a value whose digits need no rounding.
"""
from unittest import mock

import pytest

import ovos_number_parser
from ovos_number_parser import pronounce_number
from ovos_number_parser.numbers_hu import pronounce_number_hu
from ovos_number_parser.numbers_pl import pronounce_number_pl

#: every native backend except kab, which raises for any decimal, and two
#: languages read by Unicode RBNF
LANGS = ("an", "ar", "ast", "az", "bg", "ca", "cs", "da", "de", "el", "en",
         "es", "et", "eu", "fa", "fi", "fr", "fy", "gl", "he", "hr", "hu",
         "id", "it", "ms", "mwl", "nb", "nl", "nn", "oc", "pl", "pt-PT",
         "pt-BR", "ro", "ru", "sk", "sl", "sv", "tr", "uk", "af", "ja")

#: backends with a scientific mode of their own
SCIENTIFIC_MODE = ("az", "bg", "cs", "en", "fa", "hr", "pl", "ru", "sk", "sl",
                   "tr", "uk")


def _minus(lang):
    return pronounce_number(-5, lang)[:-len(pronounce_number(5, lang))]


@pytest.mark.parametrize("lang", LANGS)
@pytest.mark.parametrize("value, places, equivalent, covering", [
    (0.0004, 3, 0.0004, 4),
    (-0.0004, 3, -0.0004, 4),
    (1e-07, 3, 1e-07, 7),
    (0.00012345, 3, 0.0001, 4),
    (0.000096, 3, 0.0001, 4),
    (1.5e-05, 3, 2e-05, 5),
    (-2.5e-08, 3, -3e-08, 8),
    (0.04, 1, 0.04, 2),
    (-0.04, 1, -0.04, 2),
])
def test_value_below_the_quantum_reads_its_first_digit(
        lang, value, places, equivalent, covering):
    assert pronounce_number(value, lang, places=places) == \
        pronounce_number(equivalent, lang, places=covering)


@pytest.mark.parametrize("lang, point", [
    ("en", "point"), ("ru", "точка"), ("cs", "tečka"), ("pl", "przecinek"),
    ("it", "virgola"), ("de", "Komma"), ("el", "κόμμα"), ("es", "coma"),
])
@pytest.mark.parametrize("value, digits", [
    (0.0004, "0004"), (0.00012345, "0001"), (0.000096, "0001"),
    (-1e-07, "0000001"),
])
def test_value_below_the_quantum_composed_from_digit_words(
        lang, point, value, digits):
    expected = " ".join([pronounce_number(0, lang), point]
                        + [pronounce_number(int(d), lang) for d in digits])
    if value < 0:
        expected = _minus(lang) + expected
    assert pronounce_number(value, lang, places=3) == expected


@pytest.mark.parametrize("value, mantissa, exponent", [
    (1e-12, 1, 12), (-1.5e-12, -2, 12), (5e-324, 5, 324),
])
def test_fa_fraction_finer_than_its_denominators_reads_scientifically(
        value, mantissa, exponent):
    # fa names denominators down to 10 ** -11 and reads a larger magnitude
    # with "ضرب در ده به توان" (times ten to the power)
    expected = f"{pronounce_number(abs(mantissa), 'fa')} ضرب در ده به توان " \
               f"{_minus('fa')}{pronounce_number(exponent, 'fa')}"
    if mantissa < 0:
        expected = _minus("fa") + expected
    assert pronounce_number(value, "fa", places=3) == expected


@pytest.mark.parametrize("lang", SCIENTIFIC_MODE)
@pytest.mark.parametrize("value, rounded", [
    (123456.0, 123500.0),
    (-123456.0, -123500.0),
    (1.2346e10, 1.235e10),
    (12346 * 10 ** 396, 1235 * 10 ** 397),
    (9.9996e10, 1e11),
    (99996 * 10 ** 396, 10 ** 401),
])
def test_scientific_mantissa_rounds_with_carry(lang, value, rounded):
    # the rounded value has three mantissa decimals, so no backend rounds it
    assert pronounce_number(value, lang, places=3, scientific=True) == \
        pronounce_number(rounded, lang, places=3, scientific=True)


def _hu(whole, numerator, denominator):
    return " ".join([pronounce_number(whole, "hu"), "egész",
                     pronounce_number(numerator, "hu"), denominator])


@pytest.mark.parametrize("value, places, whole, numerator, denominator", [
    (2000.5, 2, 2000, 50, "század"),
    (3000.25, 2, 3000, 25, "század"),
    (2000000.5, 1, 2000000, 5, "tized"),
])
def test_hu_round_thousands_whole_part_has_no_hyphen(
        value, places, whole, numerator, denominator):
    expected = _hu(whole, numerator, denominator)
    assert pronounce_number(value, "hu", places=places) == expected
    assert pronounce_number(-value, "hu", places=places) == \
        _minus("hu") + expected


@pytest.mark.parametrize("value, numerator", [(0.0025, 3), (0.0045, 5)])
def test_hu_direct_call_rounds_half_up(value, numerator):
    assert pronounce_number_hu(value, 3) == _hu(0, numerator, "ezred")


@pytest.mark.parametrize("lang", ("et", "fi", "fy"))
def test_ordinal_flag_on_a_non_ordinal_value_returns_words(lang):
    assert pronounce_number(-2.0, lang, ordinals=True) == \
        _minus(lang) + pronounce_number(2, lang, ordinals=True)
    assert pronounce_number(3.5, lang, ordinals=True) == \
        pronounce_number(3.5, lang)
    assert pronounce_number(-3.5, lang, ordinals=True) == \
        pronounce_number(-3.5, lang)
    assert pronounce_number(-1e16, lang, ordinals=True) == \
        pronounce_number(-10 ** 16, lang, ordinals=True)


def test_pl_direct_call_past_the_scale_words():
    expected = pronounce_number(-10 ** 300, "pl")
    assert pronounce_number_pl(-1e300) == expected
    assert pronounce_number_pl(-10 ** 300) == expected


@pytest.mark.parametrize("lang, connective", [
    ("an", "por diez elevau a"),
    ("ca", "per deu elevat a"),
    ("es", "por diez elevado a"),
    ("pt-PT", "vezes dez elevado a"),
])
def test_fallback_mantissa_without_fraction_has_no_decimal_word(
        lang, connective):
    for value, mantissa in ((10 ** 400, 1), (-2 * 10 ** 400, -2)):
        assert pronounce_number(value, lang) == \
            f"{pronounce_number(mantissa, lang)} {connective} " \
            f"{pronounce_number(400, lang)}"


@pytest.mark.parametrize("lang", ("uk", "ru"))
def test_ordinal_past_the_scale_words_reads_like_the_cardinal(lang):
    for value in (10 ** 100 + 5, 10 ** 100 + 21):
        assert pronounce_number(value, lang, ordinals=True) == \
            pronounce_number(value, lang)


@pytest.mark.parametrize("value, places", [(-0.25, 3), (-0.5, 1), (-0.04, 1)])
def test_negative_fraction_dispatches_once(value, places):
    dispatch = ovos_number_parser._pronounce_number_dispatch
    with mock.patch.object(ovos_number_parser, "_pronounce_number_dispatch",
                           side_effect=dispatch) as spy:
        pronounce_number(value, "en", places=places)
    assert spy.call_count == 1
