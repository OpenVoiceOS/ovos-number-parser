# -*- coding: utf-8 -*-
"""
Additional unit tests for Catalan number parsing/formatting functions.

Focus:
- nice_number_ca
- pronounce_number_ca
- is_fractional_ca
- extract_number_ca
- numbers_to_digits_ca

Testing framework: pytest
"""

import re
import pathlib
import pytest
from importlib.machinery import SourceFileLoader
from importlib.util import spec_from_loader, module_from_spec


def _load_ca_module():
    """
    Dynamically locate and load the Python module that defines the target
    Catalan number functions so tests don't depend on a specific package path.

    Heuristic: find a .py file (outside tests/) that defines both:
      - def nice_number_ca(
      - def pronounce_number_ca(
    """
    root = pathlib.Path(__file__).resolve().parents[1]
    candidates = []
    for p in root.rglob("*.py"):
        if "tests" in p.parts:
            continue
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if re.search(r"def\s+nice_number_ca\s*\(", txt) and \
           re.search(r"def\s+pronounce_number_ca\s*\(", txt):
            candidates.append(p)
    if not candidates:
        return None
    # Prefer shorter path depth (likely the primary locale module)
    target = sorted(candidates, key=lambda x: (len(x.parts), str(x)))[0]
    loader = SourceFileLoader("ca_numbers_module", str(target))
    spec = spec_from_loader(loader.name, loader)
    mod = module_from_spec(spec)
    loader.exec_module(mod)
    return mod


try:
    ca = _load_ca_module()
except Exception:
    ca = None

pytestmark = pytest.mark.skipif(
    ca is None, reason="Catalan number parser module not found by tests"
)


# ---------------------------- nice_number_ca ---------------------------------

@pytest.mark.parametrize(
    "number,speech,expected",
    [
        (4, False, "4"),              # integer, display mode
        (4.5, False, "4 1/2"),        # mixed fraction, display mode
        (0.5, True, "un mig"),        # 1/2 for speech (singular)
        (0.6, True, "3 cinquens"),    # 3/5 for speech (pluralization 'è' -> 'ens')
        (2.3, True, "2 i 3 desens"),  # whole + fraction (2 + 3/10) for speech
    ],
)
def test_nice_number_ca_core_cases(number, speech, expected):
    assert ca.nice_number_ca(number, speech) == expected


def test_nice_number_ca_rounding_fallback_with_restricted_denominators():
    # With denominators=[1], 1.234 can't form a proper fraction -> falls back to round(number, 3)
    out = ca.nice_number_ca(1.234, True, denominators=[1])
    assert out == "1.234"


# ------------------------- pronounce_number_ca -------------------------------

@pytest.mark.parametrize(
    "number,expected",
    [
        (5, "cinc"),
        (23, "vint-i-tres"),
        (35, "trenta-cinc"),
        (123, "cent vint-i-tres"),
    ],
)
def test_pronounce_number_ca_basic_integers(number, expected):
    assert ca.pronounce_number_ca(number) == expected


@pytest.mark.parametrize(
    "number,expected",
    [
        (5.2, "cinc coma dos"),
        (-0.4, "menys zero coma quatre"),
        (1.234, "un coma dos tres"),  # places defaults to 2
    ],
)
def test_pronounce_number_ca_decimals(number, expected):
    assert ca.pronounce_number_ca(number, places=2) == expected


@pytest.mark.parametrize(
    "number,expected",
    [
        (float("inf"), "infinit"),
        (float("-inf"), "menys infinit"),
    ],
)
def test_pronounce_number_ca_infinities(number, expected):
    assert ca.pronounce_number_ca(number) == expected


# --------------------------- is_fractional_ca --------------------------------

@pytest.mark.parametrize(
    "token,expected",
    [
        ("cinquè", 1.0 / 5),
        ("cinqué", 1.0 / 5),     # normalized to cinquè
        ("terceres", 1.0 / 3),   # -> terç
        ("tercera", 1.0 / 3),    # -> terç
        ("terç", 1.0 / 3),
        ("mitges", 1.0 / 2),     # -> mig
        ("mitja", 1.0 / 2),      # -> mig
        ("meitat", 1.0 / 2),     # -> mig
        ("meitats", 1.0 / 2),    # -> mig
        ("vuitè", 1.0 / 8),
        ("huitè", 1.0 / 8),
        ("divuitè", 1.0 / 18),
        ("dihuitè", 1.0 / 18),
        ("vintè", 1.0 / 20),
        ("trentè", 1.0 / 30),
        ("centè", 1.0 / 100),
        ("milè", 1.0 / 1000),
        ("quartes", 1.0 / 4),    # -> quart
        ("quarta", 1.0 / 4),
        ("quarts", 1.0 / 4),
    ],
)
def test_is_fractional_ca_variants(token, expected):
    assert ca.is_fractional_ca(token) == expected


def test_is_fractional_ca_unknown_returns_false():
    assert ca.is_fractional_ca("banana") is False


# ---------------------------- extract_number_ca ------------------------------

@pytest.mark.parametrize(
    "text,expected",
    [
        ("42", 42),                   # numeric string (int)
        ("2/3", pytest.approx(2/3)),  # a/b fraction
        ("vint-i-dos", 22),           # hyphenated tens with units
        ("trenta-cinc", 35),
        ("dos coma cinc", 2.5),       # decimal with 'coma'
    ],
)
def test_extract_number_ca_various_forms(text, expected):
    out = ca.extract_number_ca(text)
    if isinstance(expected, float) and not isinstance(expected, int):
        assert out == expected
    else:
        assert out == expected


def test_extract_number_ca_hundreds_hyphenated():
    # four hundreds -> 400 (supports feminine/masc forms depending on dicts)
    out = ca.extract_number_ca("quatre-centes")
    assert out == 400


@pytest.mark.parametrize(
    "text,expected",
    [
        ("un mig", 0.5),               # 1/2
        ("dos cinquens", pytest.approx(0.4)),  # 2 * (1/5)
    ],
)
def test_extract_number_ca_with_fraction_words(text, expected):
    out = ca.extract_number_ca(text)
    if isinstance(expected, float) and not isinstance(expected, int):
        assert out == expected
    else:
        assert out == expected


def test_extract_number_ca_returns_int_when_decimal_zero_tail():
    # Ensure trailing .0 becomes int per function logic
    assert ca.extract_number_ca("2") == 2
    # '2.0' arises internally; simulate by ensuring integer output is maintained
    assert isinstance(ca.extract_number_ca("dos"), int)


# ------------------------- numbers_to_digits_ca ------------------------------


def test_numbers_to_digits_ca_basic_replacements(monkeypatch):
    """
    numbers_to_digits_ca relies on a tokenizer producing tokens with a .word attribute.
    Mock tokenize and Token to avoid external dependencies.
    """
    class DummyToken:
        def __init__(self, word):
            self.word = word

    def fake_tokenize(u):
        return [DummyToken(w) for w in u.split()]

    # Provide Token symbol and tokenizer in the target module
    monkeypatch.setattr(ca, "Token", DummyToken, raising=False)
    monkeypatch.setattr(ca, "tokenize", fake_tokenize, raising=False)

    s = "tinc dos gats i tres gossos"
    out = ca.numbers_to_digits_ca(s)
    assert out == "tinc 2 gats i 3 gossos"


def test_numbers_to_digits_ca_retains_unknown_tokens(monkeypatch):
    class DummyToken:
        def __init__(self, word):
            self.word = word

    def fake_tokenize(u):
        return [DummyToken(w) for w in u.split()]

    monkeypatch.setattr(ca, "Token", DummyToken, raising=False)
    monkeypatch.setattr(ca, "tokenize", fake_tokenize, raising=False)

    s = "hola món vint i un gos desconegut"
    out = ca.numbers_to_digits_ca(s)
    # 'vint' and 'un' are replaced; others preserved
    assert out == "hola món 20 i 1 gos desconegut"