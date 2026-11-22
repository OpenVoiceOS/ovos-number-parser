"""The reader names that released ovos-date-parser versions import stay as
deprecation shims onto the numtag readers.

Each shim keeps the parameters its reader had, warns, and answers what the
public function answers. The expected value is the number whose spoken form
``pronounce_number`` wrote.
"""
import importlib
import inspect
import unittest

from ovos_number_parser import pronounce_number
from ovos_number_parser.numbers_ca import CA
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
