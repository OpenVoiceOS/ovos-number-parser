"""``decimal.Decimal`` input to ``pronounce_number``.

A finite Decimal reads exactly as the float written with the same digits, in
every language and at every ``places``. The float reading is the oracle: it
is computed by the float path, which this input type must not diverge from.
An integral Decimal reads as the int with the same digits, at any size. NaN is
rejected with ValueError and an infinite Decimal reads as the float infinity.
"""

from decimal import Decimal

import pytest

from ovos_number_parser import pronounce_number

NATIVE_LANGS = ["an", "ar", "ast", "az", "bg", "ca", "cs", "da", "de", "el",
                "en", "es", "et", "eu", "fa", "fi", "fr", "fy", "gl", "he",
                "hr", "hu", "id", "it", "kab", "ms", "mwl", "nb", "nl", "nn",
                "oc", "pl", "pt-PT", "pt-BR", "ro", "ru", "sk", "sl", "sv",
                "tr", "uk"]
RBNF_LANGS = ["af", "hi", "is", "ja", "lt", "sw"]
LANGS = NATIVE_LANGS + RBNF_LANGS

# decimal strings a float holds faithfully: repr(float(s)) gives back s
VALUES = ["0.5", "44.25", "-3.75", "1.999", "3.14159", "0.999", "2.675",
          "-0.125", "3.0", "-0.0", "0.0001"]
PLACES = [1, 2, 3]

BIG_INTS = ["123456789012345678901", "-98765432109876543210987"]


def _reading(number, lang, places):
    try:
        return pronounce_number(number, lang, places=places)
    except Exception as err:
        return type(err)


@pytest.mark.parametrize("lang", LANGS)
def test_decimal_reads_as_float_with_same_digits(lang):
    for s in VALUES:
        assert Decimal(repr(float(s))) == Decimal(s)
        for places in PLACES:
            expected = _reading(float(s), lang, places)
            assert _reading(Decimal(s), lang, places) == expected, \
                f"{lang} {s} places={places}"


@pytest.mark.parametrize("lang", LANGS)
def test_integral_decimal_reads_as_int(lang):
    for s in BIG_INTS + ["7", "-40", "1E+3"]:
        assert _reading(Decimal(s), lang, 3) == _reading(int(Decimal(s)), lang, 3), \
            f"{lang} {s}"


@pytest.mark.parametrize("lang", ["en", "pt-PT", "es", "da", "ar"])
def test_decimal_rounds_half_away_from_zero(lang):
    # 3.14159 at two places is 3.14; 3.145 at two places is 3.15, not 3.14
    assert pronounce_number(Decimal("3.15"), lang, places=2) != \
        pronounce_number(Decimal("3.14"), lang, places=2)
    assert pronounce_number(Decimal("3.145"), lang, places=2) == \
        pronounce_number(Decimal("3.15"), lang, places=2)
    assert pronounce_number(Decimal("-3.145"), lang, places=2) == \
        pronounce_number(Decimal("-3.15"), lang, places=2)
    assert pronounce_number(Decimal("3.14159"), lang, places=2) == \
        pronounce_number(Decimal("3.14"), lang, places=2)


@pytest.mark.parametrize("lang", ["en", "pt-PT", "da", "ar", "fr"])
def test_decimal_rounding_carries_into_whole_part(lang):
    assert pronounce_number(Decimal("0.999"), lang, places=2) == \
        pronounce_number(1, lang)
    assert pronounce_number(Decimal("-41.9996"), lang, places=3) == \
        pronounce_number(-42, lang)


@pytest.mark.parametrize("lang", ["ar", "el", "he"])
def test_decimal_fraction_is_read(lang):
    # the whole-number reading must not stand for a value with a fraction
    assert pronounce_number(Decimal("44.25"), lang, places=2) != \
        pronounce_number(44, lang)


@pytest.mark.parametrize("s", ["NaN", "-NaN", "sNaN"])
@pytest.mark.parametrize("lang", ["en", "pt-PT", "da", "ja"])
def test_decimal_nan_raises_value_error(lang, s):
    with pytest.raises(ValueError):
        pronounce_number(Decimal(s), lang)


@pytest.mark.parametrize("lang", ["en", "pt-PT", "de", "ar", "ja"])
def test_infinite_decimal_reads_as_float_infinity(lang):
    assert pronounce_number(Decimal("Infinity"), lang) == \
        pronounce_number(float("inf"), lang)
    assert pronounce_number(Decimal("-Infinity"), lang) == \
        pronounce_number(float("-inf"), lang)


@pytest.mark.parametrize("lang", ["en", "pt-PT", "es", "de", "fr", "da"])
def test_decimal_beyond_float_range_reads_as_rounded_int(lang):
    huge = Decimal("1" + "0" * 400 + ".5")
    assert pronounce_number(huge, lang) == pronounce_number(10 ** 400 + 1, lang)


@pytest.mark.parametrize("lang", ["en", "pt-PT", "de", "ar"])
def test_integral_decimal_with_fraction_digits_beyond_float(lang):
    assert pronounce_number(Decimal("12345678901234567890.0"), lang) == \
        pronounce_number(12345678901234567890, lang)


@pytest.mark.parametrize("lang", ["en", "pt-PT", "de", "ar"])
def test_decimal_rounds_from_its_own_digits(lang):
    # the nearest float of 2.67499999999999999999 is 2.675, which rounds up
    assert pronounce_number(Decimal("2.67499999999999999999"), lang,
                            places=2) == \
        pronounce_number(Decimal("2.67"), lang, places=2)
