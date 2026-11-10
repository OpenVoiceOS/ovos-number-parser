"""Input types other than int and float, and magnitudes past 4300 digits.

Each expected reading comes from the int or float written with the same
digits, or from the scientific reading composed of ``pronounce_number`` of a
mantissa and an exponent worked out by hand.
"""
import json
import os
import struct
import subprocess
import sys
import timeit
from decimal import Decimal
from fractions import Fraction
from numbers import Real

import pytest

from ovos_number_parser import pronounce_number, pronounce_ordinal

LANGS = ["an", "ar", "ast", "az", "bg", "ca", "cs", "da", "de", "el", "en",
         "es", "et", "eu", "fa", "fi", "fr", "fy", "gl", "he", "hr", "hu",
         "id", "it", "kab", "ms", "mwl", "nb", "nl", "nn", "oc", "pl", "pt-PT",
         "pt-BR", "ro", "ru", "sk", "sl", "sv", "tr", "uk", "af", "hi", "is",
         "ja", "lt", "sw"]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: kab reads up to 9999 and raises above it by design
READING_LANGS = [lang for lang in LANGS if lang != "kab"]

#: the connective of each language's spoken scientific form
CONNECTIVE = {
    "ca": "per deu elevat a",
    "da": "gange ti i",
    "de": "mal zehn hoch",
    "en": "times ten to the power of",
    "es": "por diez elevado a",
    "gl": "veces dez elevado a",
    "nl": "maal tien tot de macht",
    "pt-BR": "vezes dez elevado a",
    "pt-PT": "vezes dez elevado a",
    "ro": "ori zece la puterea",
    "sv": "gånger tio upphöjt till",
}


def _reading(function, number, lang, **kwargs):
    try:
        return function(number, lang, **kwargs)
    except Exception as err:
        return type(err)


def _per_call(function, *args):
    """Seconds per call, the best of five runs of 200 calls, so a busy
    machine slows both sides of a comparison alike."""
    timer = timeit.Timer(lambda: function(*args))
    return min(timer.repeat(repeat=5, number=200)) / 200


def _scientific(mantissa, exponent, lang):
    return (f"{pronounce_number(mantissa, lang)} {CONNECTIVE[lang]} "
            f"{pronounce_number(exponent, lang)}")


class _Single:
    """A ``numbers.Real`` that is not a float, as ``numpy.float32`` is: its
    ``str()`` gives the digits written and its arithmetic runs on the
    single-precision value, 1.25600004196... for "1.256"."""

    def __init__(self, written):
        self.written = written
        self.value = struct.unpack("f", struct.pack("f", float(written)))[0]

    def __str__(self):
        return self.written

    def __float__(self):
        return self.value

    def __repr__(self):
        return f"_Single({self.written!r})"


for _name in (Real.__abstractmethods__ - {"__float__"}) \
        | {"__ge__", "__gt__", "__int__"}:
    setattr(_Single, _name,
            lambda self, *args, _name=_name: getattr(self.value, _name)(*args))
Real.register(_Single)


class TestBeyondTheStringLimit:
    """Past 4300 integer digits every language reads the scientific form."""

    # value, mantissa and exponent at the default 3 places
    VALUES = [
        (10 ** 4400, 1.0, 4400),
        (-123456 * 10 ** 4395, -1.235, 4400),
        (99995 * 10 ** 4396, 1.0, 4401),
        (Decimal("1E+4400"), 1.0, 4400),
        (Decimal("-1.23456E+4400"), -1.235, 4400),
        (Decimal("1" + "0" * 5000 + ".5"), 1.0, 5000),
        (Fraction(10 ** 4401 + 1, 10), 1.0, 4400),
    ]

    @pytest.mark.parametrize("lang", READING_LANGS)
    def test_reads_like_the_scientific_form_of_the_digits(self, lang):
        for value, mantissa, exponent in self.VALUES:
            expected = pronounce_number(mantissa, lang)
            reading = _reading(pronounce_number, value, lang)
            assert isinstance(reading, str), (lang, exponent, reading)
            assert reading.startswith(expected + " "), (lang, reading)
            assert reading.endswith(" " + pronounce_number(exponent, lang)), \
                (lang, reading)

    @pytest.mark.parametrize("lang", sorted(CONNECTIVE))
    def test_connective(self, lang):
        for value, mantissa, exponent in self.VALUES:
            assert pronounce_number(value, lang) == \
                _scientific(mantissa, exponent, lang), (lang, exponent)

    def test_huge_values_finish(self):
        code = ("import json; from decimal import Decimal; "
                "from ovos_number_parser import pronounce_number as p, "
                "pronounce_ordinal as o\n"
                "def r(f, *a):\n"
                "    try: return f(*a)\n"
                "    except Exception as e: return type(e).__name__\n"
                "print(json.dumps([r(p, Decimal(10) ** 999999, 'en'), "
                "r(p, Decimal('-1E+1000000'), 'pt-PT'), "
                "r(p, 10 ** 400000, 'de'), "
                "r(p, Decimal(10) ** 999999, 'kab'), "
                "r(p, -Decimal(10) ** 999999, 'kab'), "
                "r(o, Decimal(10) ** 999999, 'pt-PT'), "
                "r(o, Decimal(10) ** 999999, 'en')]))")
        env = dict(os.environ, PYTHONPATH=os.pathsep.join(
            [ROOT, os.environ.get("PYTHONPATH", "")]))
        done = subprocess.run([sys.executable, "-c", code], cwd=ROOT,
                              env=env, capture_output=True, text=True,
                              timeout=60, check=True)
        assert json.loads(done.stdout) == [
            _scientific(1.0, 999999, "en"),
            _scientific(-1.0, 1000000, "pt-PT"),
            _scientific(1.0, 400000, "de"),
            "OverflowError", "ValueError", "ValueError", "ValueError"]


@pytest.mark.parametrize("lang", sorted(CONNECTIVE))
def test_scientific_words_entry(lang):
    # 10 ** 1000 takes the dispatcher fallback in each of these languages;
    # ro pads its scale words without repeating one back to back, so only
    # the value past the string limit reaches the fallback there
    values = [(10 ** 4400, 4400)]
    if lang != "ro":
        values.append((10 ** 1000, 1000))
    for value, exponent in values:
        assert pronounce_number(value, lang) == \
            _scientific(1.0, exponent, lang)


@pytest.mark.parametrize("lang", LANGS)
def test_ordinal_of_decimal_and_fraction(lang):
    for value in (1, 3, 21, 100):
        expected = _reading(pronounce_ordinal, value, lang)
        for number in (Decimal(value), Decimal(f"{value}.0"),
                       Decimal(value).scaleb(1).scaleb(-1), Fraction(value),
                       _Single(f"{value}.0")):
            assert _reading(pronounce_ordinal, number, lang) == expected, \
                (lang, repr(number))
    for written in ("2.5", "0.25"):
        expected = _reading(pronounce_ordinal, float(written), lang)
        for number in (Decimal(written), Fraction(written), _Single(written)):
            assert _reading(pronounce_ordinal, number, lang) == expected, \
                (lang, repr(number))


@pytest.mark.parametrize("lang", LANGS)
def test_real_that_is_not_a_float(lang):
    # the single-precision 1.256 is 1.25600004196...; read from its str()
    # it rounds as the float 1.256 does
    for written in ("1.256", "0.1", "3.0", "-2.675", "44.29", "1e+20"):
        for places in (2, 3):
            assert _reading(pronounce_number, _Single(written), lang,
                            places=places) == \
                _reading(pronounce_number, float(written), lang,
                         places=places), (lang, written, places)


@pytest.mark.parametrize("lang", LANGS)
def test_fraction_reads_its_rounded_digits(lang):
    # fraction, places, the digits it rounds to, half away from zero
    cases = [
        (Fraction(1, 4), 3, "0.25"),
        (Fraction(1, 3), 2, "0.33"),
        (Fraction(2, 3), 3, "0.667"),
        (Fraction(1, 8), 2, "0.13"),
        (Fraction(-1, 8), 2, "-0.13"),
        (Fraction(2675, 1000), 2, "2.68"),
        (Fraction(267499999, 10 ** 8), 2, "2.67"),
        (Fraction(-7, 2), 0, "-4"),
        (Fraction(10 ** 20 + 1, 10 ** 20), 3, "1"),
        (Fraction(-41, 1), 3, "-41"),
    ]
    for fraction, places, digits in cases:
        expected = float(digits) if "." in digits else int(digits)
        assert _reading(pronounce_number, fraction, lang, places=places) == \
            _reading(pronounce_number, expected, lang, places=places), \
            (lang, fraction, places)
    # past the float's significant digits the reading follows the Decimal
    # written with the same digits
    assert _reading(pronounce_number, Fraction(10 ** 25 + 1, 2), lang) == \
        _reading(pronounce_number, Decimal("5000000000000000000000000.5"),
                 lang)
    # a value below the rounding quantum reads as its nearest float, as a
    # float that small does
    for fraction in (Fraction(1, 30000), Fraction(-1, 30000)):
        assert _reading(pronounce_number, fraction, lang) == \
            _reading(pronounce_number, float(fraction), lang), \
            (lang, fraction)


@pytest.mark.parametrize("function, decimal, same, lang", [
    (pronounce_number, Decimal("1.5"), 1.5, "en"),
    (pronounce_number, Decimal("12"), 12, "en"),
    (pronounce_ordinal, Decimal("3"), 3, "pt-PT"),
])
def test_decimal_costs_about_what_the_float_costs(function, decimal, same,
                                                  lang):
    # the check for a magnitude past 4300 digits must not convert the
    # 4301-digit bound for every Decimal
    assert _per_call(function, decimal, lang) < \
        4 * _per_call(function, same, lang)


ORDINAL_LANGS = ["ca", "da", "de", "en", "fr", "he", "hu", "pt-PT", "ro",
                 "tr"]


@pytest.mark.parametrize("lang", ORDINAL_LANGS)
def test_ordinal_past_the_float_range(lang):
    # no float holds these values: each one rounds half away from zero to
    # the int with the same digits
    for number, whole in (
            (Fraction(2 * 10 ** 400 + 1, 2), 10 ** 400 + 1),
            (Fraction(-(2 * 10 ** 400 + 1), 2), -(10 ** 400 + 1)),
            (Decimal("1" * 400 + ".5"), int("1" * 399 + "2")),
            (Decimal("1" * 400 + ".25"), int("1" * 400))):
        reading = _reading(pronounce_ordinal, number, lang)
        assert reading == _reading(pronounce_ordinal, whole, lang), \
            (lang, number)
        assert not isinstance(reading, str) or "inf" not in reading


@pytest.mark.parametrize("lang", ORDINAL_LANGS)
def test_ordinal_past_the_string_limit(lang):
    for number in (Decimal("1" * 5000 + ".5"), Decimal("1E+4300"),
                   -Decimal(10) ** 999999):
        with pytest.raises(ValueError):
            pronounce_ordinal(number, lang)


def test_unsupported_language_raises_before_the_size():
    for lang in ("br", "xx"):
        with pytest.raises(NotImplementedError):
            pronounce_ordinal(3, lang)
        with pytest.raises(NotImplementedError):
            pronounce_ordinal(Decimal("1E+4300"), lang)


#: Decimals whose conversion to a Fraction takes seconds to minutes, each
#: with the int or float that holds the same value
SLOW_FRACTIONS = [
    ("Decimal('1E-99999999')", 0.0),
    ("Decimal('-1E-99999999')", -0.0),
    ("Decimal('1E-999999999999')", 0.0),
    ("Decimal('0.' + '1' * 300000)", float("0." + "1" * 40)),
    ("Decimal('1' * 1000000 + 'E-999700')", float("1." + "1" * 40 + "e299")),
    ("Decimal('1' + '0' * 1000000 + 'E-999000')", 10 ** 1000),
    ("Decimal('1' * 4000 + 'E+100')", int("1" * 4000) * 10 ** 100),
    ("Decimal('1' * 1000000 + 'E+1000')", None),
]


@pytest.mark.parametrize("lang", ["pt-PT", "de"])
def test_ordinal_decimal_conversion_finishes(lang):
    code = ("import json; from decimal import Decimal; "
            "from ovos_number_parser import pronounce_ordinal as o\n"
            "def r(n):\n"
            "    try: return repr(o(n, %r))\n"
            "    except Exception as e: return type(e).__name__\n"
            "print(json.dumps([%s]))"
            % (lang, ", ".join(f"r({expr})" for expr, _ in SLOW_FRACTIONS)))
    env = dict(os.environ, PYTHONPATH=os.pathsep.join(
        [ROOT, os.environ.get("PYTHONPATH", "")]))
    done = subprocess.run([sys.executable, "-c", code], cwd=ROOT, env=env,
                          capture_output=True, text=True, timeout=60,
                          check=True)
    expected = []
    for _, same in SLOW_FRACTIONS:
        if same is None:
            expected.append("ValueError")
            continue
        reading = _reading(pronounce_ordinal, same, lang)
        expected.append(reading.__name__ if isinstance(reading, type)
                        else repr(reading))
    assert json.loads(done.stdout) == expected
