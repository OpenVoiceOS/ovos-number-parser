"""Values below 1e-4 read their digits, for both signs, at every ``places``.

French read such a value as the raw numeral "1e-05". Hungarian left the
numerator out when it rounds to zero and had no denominator past five
places. At places=0, a value that rounds to zero reads as the zero word
alone in every language, with no minus word, since no digit follows it. The
Unicode RBNF fallback raised for a value below 1e-6, because
``unicode_rbnf`` splits the fraction from ``str(Decimal)``, which writes
"1E-7". Each expected reading is composed from readings that do not pass
through the changed code: integer readings, and for RBNF the engine's own
reading of the same digits after a whole part of 1.
"""
from decimal import Decimal
from os.path import commonprefix

import pytest
from unicode_rbnf import RbnfEngine

from ovos_number_parser import pronounce_number

#: the languages with no native module that the RBNF data reads, except zu,
#: which has no rule for a fraction
FALLBACK_LANGS = (
    "af", "ak", "am", "be", "bs", "ccp", "chr", "cy", "ee", "eo", "ff", "fo",
    "ga", "hi", "hy", "is", "ja", "ka", "kk", "kl", "km", "ko", "ky", "lb",
    "lo", "lrc", "lt", "lv", "mk", "mt", "my", "ne", "qu", "se", "sq", "sr",
    "sr_Latn", "su", "sw", "ta", "th", "vec", "vi", "yue", "yue_Hans", "zh",
    "zh_Hant",
)


def _fr(*digits):
    return " ".join([pronounce_number(0, "fr"), "virgule"]
                    + [pronounce_number(int(d), "fr") for d in digits])


@pytest.mark.parametrize("value, places, digits", [
    (1e-05, 5, "00001"),
    (1e-05, 8, "00001"),
    (2e-05, 5, "00002"),
    (1.5e-05, 8, "000015"),
    (1e-07, 8, "0000001"),
])
def test_fr_small_value_reads_each_digit(value, places, digits):
    minus = pronounce_number(-1, "fr").rsplit(" ", 1)[0]
    assert pronounce_number(value, "fr", places=places) == _fr(*digits)
    assert pronounce_number(-value, "fr", places=places) == \
        minus + " " + _fr(*digits)


def _hu(whole, numerator, denominator):
    return " ".join([pronounce_number(whole, "hu"), "egész",
                     pronounce_number(numerator, "hu"), denominator])


@pytest.mark.parametrize("value, places, numerator, denominator", [
    (1e-07, 5, 1, "tízmilliomod"),
    (1e-05, 3, 1, "százezred"),
    (1e-05, 6, 10, "milliomod"),
    (1e-07, 7, 1, "tízmilliomod"),
    (1e-05, 8, 1000, "százmilliomod"),
    (2e-05, 8, 2000, "százmilliomod"),
    (1e-09, 9, 1, "milliárdod"),
    (0.5, 10, 5 * 10 ** 9, "tízmilliárdod"),
    (0.5, 12, 5 * 10 ** 11, "billiomod"),
    (0.25, 24, 25 * 10 ** 22, "kvadrilliomod"),
    (0.25, 30, 25 * 10 ** 22, "kvadrilliomod"),
])
def test_hu_small_value_names_numerator_and_denominator(
        value, places, numerator, denominator):
    expected = _hu(0, numerator, denominator)
    assert pronounce_number(value, "hu", places=places) == expected
    assert pronounce_number(-value, "hu", places=places) == \
        pronounce_number(-1, "hu").split()[0] + " " + expected


def test_hu_round_thousands_numerator_has_no_hyphen():
    assert pronounce_number(5.2, "hu", places=4) == \
        _hu(5, 2000, "tízezred")


#: every native language module and every RBNF fallback language
ALL_LANGS = (
    "an", "ar", "ast", "az", "bg", "ca", "cs", "da", "de", "el", "en", "es",
    "et", "eu", "fa", "fi", "fr", "fy", "gl", "he", "hr", "hu", "id", "it",
    "kab", "ms", "mwl", "nb", "nl", "nn", "oc", "pl", "pt-PT", "pt-BR", "ro",
    "ru", "sk", "sl", "sv", "tr", "uk") + FALLBACK_LANGS


@pytest.mark.parametrize("lang", ALL_LANGS)
@pytest.mark.parametrize("value", [
    1e-05, 1e-07, 0.4, 0.49, 5e-324, Decimal("1E-5000")])
def test_value_that_rounds_to_zero_at_no_places_reads_zero(lang, value):
    assert pronounce_number(value, lang, places=0) == pronounce_number(0, lang)
    assert pronounce_number(-value, lang, places=0) == \
        pronounce_number(0, lang)


@pytest.mark.parametrize("lang", ("ar", "de", "en", "es", "hu", "af"))
def test_negative_value_keeps_minus_word_before_digits(lang):
    minus = pronounce_number(-1, lang).split(pronounce_number(1, lang))[0]
    assert pronounce_number(-1e-05, lang, places=5) == \
        minus + pronounce_number(1e-05, lang, places=5)


def _rbnf(lang, number):
    return RbnfEngine.for_language(lang).format_number(number).text


def _rbnf_small(lang, digits):
    """The engine reading of 0.<digits>, from its reading of 1.<digits>.

    The engine reads 1.0000001 in positional form. The whole part is swapped
    for 0 through the part that 0.5 and 1.5 do not share.
    """
    shared = commonprefix([_rbnf(lang, Decimal("0.5"))[::-1],
                           _rbnf(lang, Decimal("1.5"))[::-1]])
    zero = _rbnf(lang, Decimal("0.5"))[:-len(shared)]
    one = _rbnf(lang, Decimal("1.5"))[:-len(shared)]
    reading = _rbnf(lang, Decimal("1." + digits))
    assert reading.startswith(one), (lang, reading, one)
    return zero + reading[len(one):]


#: the fallback languages whose decimals the parser reads with its own rules,
#: tested in test_rbnf_decimal_words, not as the engine reads them
_OWN_DECIMAL_RULES = ("cy", "kk", "ky", "lo", "mt")


@pytest.mark.parametrize(
    "lang", [lang for lang in FALLBACK_LANGS if lang not in _OWN_DECIMAL_RULES])
@pytest.mark.parametrize("value, digits", [
    (1e-07, "0000001"),
    (1.5e-07, "00000015"),
    (2.5e-08, "000000025"),
])
def test_rbnf_value_below_1e6_reads_each_digit(lang, value, digits):
    expected = _rbnf_small(lang, digits)
    assert pronounce_number(value, lang, places=9) == expected
    minus_one, one = _rbnf(lang, -1), _rbnf(lang, 1)
    negative = pronounce_number(-value, lang, places=9)
    if minus_one.endswith(one):
        assert negative == minus_one[:-len(one)] + expected
    else:
        assert negative == expected + minus_one[len(one):]


def test_rbnf_language_without_fraction_rule_still_refuses():
    with pytest.raises(NotImplementedError):
        pronounce_number(1e-07, "zu", places=8)
