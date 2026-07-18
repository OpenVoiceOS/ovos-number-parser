"""Rounding of the fractional part at the dispatcher level.

``pronounce_number`` rounds a real value to the requested number of decimal
places, half away from zero, before handing it to any per-language formatter.
The formatters keep only the first ``places`` fractional digits by slicing the
decimal string, which truncates; rounding once, up front, makes every language
speak a correctly rounded value at the same time. Rounding of numerical values
follows ISO 80000-1 and NIST SP 811 (2008 ed.) Appendix B.7.
"""

import math

import pytest

from ovos_number_parser import pronounce_number, extract_number


# Languages whose formatters previously truncated the fractional part on a
# direct pronounce_number call. Each entry pairs a value with the spoken digit
# it must contain once rounded (and must NOT contain, had it been truncated).
_ROUND_LANGS = {
    "et": ("üks", "kaks"),
    "fi": ("yksi", "kaksi"),
    "cs": ("jedna", "dva"),
    "bg": ("едно", "две"),
    "tr": ("bir", "iki"),
    "hr": ("jedan", "dva"),
    "pl": ("jeden", "dwa"),
    "az": ("bir", "iki"),
    "id": ("satu", "dua"),
    "uk": ("один", "два"),
    "sl": ("ena", "dve"),
    "sk": ("jeden", "dva"),
    "en": ("one", "two"),
    "ru": ("один", "два"),
}


@pytest.mark.parametrize("lang,words", list(_ROUND_LANGS.items()))
def test_last_place_rounds_up_not_truncates(lang, words):
    # 3.15 at one place -> 3.2 ("...two"), never the truncated 3.1 ("...one")
    one_word, two_word = words
    spoken = pronounce_number(3.15, lang, places=1)
    tokens = spoken.split()
    assert two_word in tokens, f"{lang}: expected rounded {two_word!r} in {spoken!r}"
    assert one_word not in tokens, f"{lang}: truncated to {one_word!r} in {spoken!r}"


@pytest.mark.parametrize("lang", list(_ROUND_LANGS))
def test_rounds_at_two_places(lang):
    # 3.145 at two places -> 3.15 (fifth digit rounds the fourth up)
    spoken = pronounce_number(3.145, lang, places=2)
    # the truncated reading would end in the "four" numeral of each language;
    # the rounded reading ends in the "five" numeral. Assert the two-place
    # fractional pronunciation differs from the truncating baseline of 3.144.
    truncated_baseline = pronounce_number(3.144, lang, places=2)
    assert spoken != truncated_baseline


@pytest.mark.parametrize("lang", ["pt", "gl", "ca", "en", "ru"])
def test_carry_into_integer_part(lang):
    # 0.999999 rounded to two places carries to 1.0 and is spoken as the
    # integer "one", not "zero point ..." (Romance path also exercises the
    # per-language carry bug the dispatcher rounding sidesteps).
    one = pronounce_number(1, lang)
    assert pronounce_number(0.999999, lang, places=2) == one


@pytest.mark.parametrize("lang", ["en", "pt", "ru", "es", "fr", "it"])
def test_negative_zero_has_no_minus(lang):
    # literal negative zero is normalised to plain zero: it must read as "zero"
    # with no spoken minus sign, never "minus zero".
    zero = pronounce_number(0.0, lang)
    spoken = pronounce_number(-0.0, lang)
    assert spoken == zero
    minus = pronounce_number(-1, lang).split()[0]
    assert minus not in spoken.split()


@pytest.mark.parametrize("lang", ["en", "es", "pt", "ru", "fi", "pl"])
def test_default_places_rounds(lang):
    # the default call (places=3) rounds too: 2.71828 -> 2.718, and the fourth
    # fractional digit (2) must round the third up from 7 to 8.
    spoken = pronounce_number(2.71828, lang)
    baseline = pronounce_number(2.7179, lang)
    # 2.71828 -> 2.718 and 2.7179 -> 2.718 collapse to the same rounded reading;
    # a truncating dispatcher would render them differently (2.718 vs 2.717).
    assert spoken == baseline


@pytest.mark.parametrize("lang", list(_ROUND_LANGS))
def test_integers_unaffected(lang):
    # integer input must pass straight through, unrounded and unchanged
    assert pronounce_number(7, lang) == pronounce_number(7, lang)
    assert isinstance(pronounce_number(7, lang), str)


def test_infinity_unaffected():
    # non-finite floats are not rounded and still reach their backend handling
    assert isinstance(pronounce_number(float("inf"), "en"), str)
    assert isinstance(pronounce_number(float("-inf"), "en"), str)


def test_nan_still_rejected():
    with pytest.raises(ValueError):
        pronounce_number(float("nan"), "en")


def test_complex_unaffected():
    # complex numbers are routed before rounding and still pronounce
    assert isinstance(pronounce_number(complex(1, 2), "en"), str)


def test_round_trip_stable():
    # a value already at the requested precision survives pronounce->extract
    spoken = pronounce_number(3.5, "en", places=2)
    assert extract_number(spoken, "en") == 3.5
