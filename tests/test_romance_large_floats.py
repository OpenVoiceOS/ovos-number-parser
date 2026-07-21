"""Regression tests for the shared RomanceNumberExtractor.pronounce_number.

Very large floats and scientific-notation floats used to leak an exponent
(``"e"``) into the decimal-splitting / ``int()`` logic and raise ValueError for
every language that routes through the shared extractor (pt/ro/ast/oc/an/gl/mwl).
These tests pin the no-crash contract and guard against regressions in the
ordinary int/float/decimal behaviour.
"""
import math

import pytest

import ovos_number_parser as N
from ovos_number_parser import PT_PT

# languages that share RomanceNumberExtractor.pronounce_number in util.py
ROMANCE_LANGS = ("pt", "ro", "ast", "oc", "an", "gl", "mwl")

# large / scientific / near-zero floats that previously crashed
PATHOLOGICAL = (
    6.022e23,
    1e300,
    1.234e30,
    9.999e50,
    1e-5,
    1.5e-3,
    6.626e-34,
    1e-300,
    2.5e-10,
    -6.022e23,
    -1e-5,
)


@pytest.mark.parametrize("lang", ROMANCE_LANGS)
@pytest.mark.parametrize("value", PATHOLOGICAL)
def test_large_and_scientific_floats_do_not_crash(lang, value):
    result = N.pronounce_number(value, lang)
    assert isinstance(result, str)
    assert result  # non-empty spoken form


@pytest.mark.parametrize("value", PATHOLOGICAL)
def test_negative_scientific_keeps_sign_word(value):
    # sanity: negatives still route through the negative-sign branch
    if value < 0:
        assert N.pronounce_number(value, "pt").startswith(PT_PT.vocab.NEGATIVE_SIGN[0])


@pytest.mark.parametrize("nonfinite", [float("nan"), float("inf"), float("-inf")])
def test_extractor_nonfinite_returns_sentinel_not_crash(nonfinite):
    # the shared extractor must never raise on non-finite floats; it returns a
    # clean textual sentinel (the public API separately rejects NaN up front).
    result = PT_PT.pronounce_number(nonfinite)
    assert isinstance(result, str)
    assert result


@pytest.mark.parametrize("lang", ROMANCE_LANGS)
def test_ordinary_values_unchanged(lang):
    # normal ints/floats/decimals must be completely unaffected by the fix
    for v in (0, 1, 42, 100, 1000, 1234567, 0.0, 3.14, 0.5, 12.75):
        result = N.pronounce_number(v, lang)
        assert isinstance(result, str) and result


def test_specific_known_forms_pt():
    # exact spoken forms for representative ordinary values (regression pins)
    assert N.pronounce_number(3.14, "pt") == "três vírgula catorze"
    assert N.pronounce_number(42, "pt") == "quarenta e dois"


def test_scientific_integral_matches_plain_integer_pt():
    # a scientific literal whose repr uses exponent notation and is integral
    # pronounces like its integer value (str(1e16) == "1e+16")
    assert N.pronounce_number(1e16, "pt") == N.pronounce_number(10 ** 16, "pt")
    assert N.pronounce_number(1e17, "pt") == N.pronounce_number(10 ** 17, "pt")
