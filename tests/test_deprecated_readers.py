"""The reader names that released ovos-date-parser versions import stay as
deprecation shims onto the numtag readers.

Each shim keeps the parameters its reader had, warns, and answers what the
public function answers. The expected value is the number whose spoken form
``pronounce_number`` wrote.
"""
import importlib
import inspect
import unittest
import warnings

import pytest

from ovos_number_parser import pronounce_fraction, pronounce_number, pronounce_ordinal
from ovos_number_parser.numbers_de import _get_ordinal_index
from ovos_number_parser.numbers_kab import extract_number_kab
from ovos_number_parser.numbers_sv import _find_numbers_in_text
from ovos_number_parser.util import Token
from ovos_number_parser.numbers_ca import CA, pronounce_number_ca
from ovos_number_parser.numbers_es import ES
from ovos_number_parser.numbers_fr import FR
from ovos_number_parser.numbers_it import IT
from ovos_number_parser.numbers_pt import PT_BR, PT_PT
from ovos_number_parser.version import VERSION_MAJOR

#: shim name -> (parameter, default) pairs of the reader it replaces
SIGNATURES = {
    **{f"extract_number_{c}": (("text", None), ("short_scale", True), ("ordinals", False))
       for c in "az bg cs en et fi fy hr nl pl ru sk uk hu".split()},
    "extract_number_it": (("text", None), ("short_scale", False), ("ordinals", False)),
    **{f"numbers_to_digits_{c}": (("text", None), ("short_scale", True), ("ordinals", False))
       for c in "az cs en nl pl ru uk".split()},
    **{f"numbers_to_digits_{c}": (("text", None), ("short_scale", False), ("ordinals", False), ("fractions", True))
       for c in "da de nb nn".split()},
    "numbers_to_digits_ca": (("utterance", None),),
    "numbers_to_digits_es": (("utterance", None),),
    "numbers_to_digits_pt": (("utterance", None), ("scale", None), ("variant", "PT")),
}

ORDINAL_SHIMS = {"is_ordinal_da": "da", "is_ordinal_et": "et", "is_ordinal_fi": "fi",
                 "is_ordinal_nb": "nb", "is_ordinal_nn": "nn"}


def shim(name):
    return getattr(importlib.import_module(f"ovos_number_parser.numbers_{name.rsplit('_', 1)[1]}"), name)


class TestShims(unittest.TestCase):

    def test_each_shim_keeps_the_parameters_of_its_reader(self):
        for name, expected in SIGNATURES.items():
            with self.subTest(name=name):
                got = tuple((p.name, None if p.default is p.empty else getattr(p.default, "name", p.default))
                            for p in inspect.signature(shim(name)).parameters.values())
                self.assertEqual(got, expected)

    def test_a_reader_shim_warns_and_reads_the_number(self):
        for name in SIGNATURES:
            if not name.startswith("extract_number_"):
                continue
            lang = name.rsplit("_", 1)[1]
            with self.subTest(name=name), self.assertWarnsRegex(DeprecationWarning, name):
                self.assertEqual(shim(name)(pronounce_number(7, lang=lang)), 7)

    def test_a_digits_shim_warns_and_writes_the_number(self):
        for name in SIGNATURES:
            if not name.startswith("numbers_to_digits_"):
                continue
            lang = name.rsplit("_", 1)[1]
            with self.subTest(name=name), self.assertWarnsRegex(DeprecationWarning, name):
                self.assertEqual(shim(name)(pronounce_number(7, lang=lang)), "7")

    def test_the_engine_shim_warns_and_writes_the_number(self):
        for lang, engine in (("ca", CA), ("es", ES), ("fr", FR), ("it", IT), ("pt-PT", PT_PT), ("pt-BR", PT_BR)):
            with self.subTest(lang=lang), self.assertWarnsRegex(DeprecationWarning, "numbers_to_digits"):
                self.assertEqual(engine.numbers_to_digits(pronounce_number(7, lang=lang)), "7")

    def test_the_removal_version_is_the_next_major(self):
        with self.assertWarnsRegex(DeprecationWarning, rf"removed in {VERSION_MAJOR + 1}\.0\.0"):
            shim("extract_number_hu")("hét")

    def test_a_keyword_the_reader_took_is_accepted(self):
        with self.assertWarns(DeprecationWarning):
            self.assertEqual(shim("numbers_to_digits_de")("zwei", fractions=False), "2")


if __name__ == "__main__":
    unittest.main()


class TestOrdinalAndHelperShims(unittest.TestCase):
    """The is_ordinal readers, extract_number_kab and two helpers that released
    ovos-date-parser versions import answer through numtag and warn."""

    def test_an_ordinal_shim_reads_the_ordinal_it_was_written_from(self):
        for name, lang in ORDINAL_SHIMS.items():
            with self.subTest(name=name), self.assertWarnsRegex(DeprecationWarning, name):
                self.assertEqual(shim(name)(pronounce_ordinal(3, lang=lang)), 3)

    def test_an_ordinal_shim_keeps_its_parameter(self):
        for name in ORDINAL_SHIMS:
            with self.subTest(name=name):
                self.assertEqual(list(inspect.signature(shim(name)).parameters), ["input_str"])

    def test_extract_number_kab_keeps_its_parameters_and_reads_a_number(self):
        self.assertEqual([(p.name, p.default) for p in inspect.signature(extract_number_kab).parameters.values()],
                         [("text", inspect.Parameter.empty), ("short_scale", False), ("ordinals", False)])
        with self.assertWarnsRegex(DeprecationWarning, "extract_number_kab"):
            self.assertEqual(extract_number_kab(pronounce_number(7, lang="kab")), 7)

    def test_get_ordinal_index_returns_the_value_as_the_type_asked(self):
        with self.assertWarnsRegex(DeprecationWarning, "_get_ordinal_index"):
            self.assertEqual(_get_ordinal_index("dritte"), "3")
        self.assertEqual(_get_ordinal_index("dritte", int), 3)
        self.assertIs(_get_ordinal_index("Haus"), False)

    def test_get_ordinal_index_keeps_a_day_written_with_a_dot(self):
        # "am 15. Juni": ovos-date-parser 0.29.0 passes each word, "15." included
        self.assertEqual(_get_ordinal_index("15."), "15")
        self.assertEqual(_get_ordinal_index("15.", int), 15)
        self.assertEqual(_get_ordinal_index("3."), "3")
        self.assertIs(_get_ordinal_index("15"), False)

    def test_find_numbers_in_text_pairs_each_token_with_its_number(self):
        # tokens come back in reverse order; "sju" is 7
        tokens = [Token("sju", 0), Token("dagar", 1)]
        with self.assertWarnsRegex(DeprecationWarning, "_find_numbers_in_text"):
            parts = _find_numbers_in_text(tokens)
        self.assertEqual([(value, token.word) for value, token in parts], [(None, "dagar"), (7, "sju")])

    def test_find_numbers_in_text_reads_kvart_as_a_quarter_of_an_hour(self):
        # "om en kvart": a quarter, and the unit "timmar" in front of it
        tokens = [Token("en", 0), Token("kvart", 1)]
        parts = _find_numbers_in_text(tokens)
        self.assertEqual([(value, token.word) for value, token in parts],
                         [(None, "timmar"), (0.25, "kvart"), (1, "en")])


class TestPublicCallsDoNotWarn(unittest.TestCase):

    def test_pronounce_fraction_gl_does_not_warn(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            spoken = pronounce_fraction("3/4", "gl")
        self.assertEqual(spoken, "tres cuartos")
        self.assertEqual([str(w.message) for w in caught], [])

    def test_pronounce_ordinal_gl_does_not_warn(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            spoken = pronounce_ordinal(5, "gl")
        self.assertEqual(spoken, "quinto")
        self.assertEqual([str(w.message) for w in caught], [])


class TestDeprecationNamesTheRemovalVersion(unittest.TestCase):

    @pytest.mark.xfail(strict=True, reason="https://github.com/OpenVoiceOS/ovos-number-parser/issues/573")
    def test_pronounce_number_ca_names_the_removal_version(self):
        with self.assertWarnsRegex(DeprecationWarning, rf"removed in {VERSION_MAJOR + 1}\.0\.0"):
            spoken = pronounce_number_ca(21)
        self.assertEqual(spoken, "vint-i-un")
