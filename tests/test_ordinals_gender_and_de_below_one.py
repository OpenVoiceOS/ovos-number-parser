"""Gender on ``pronounce_number(..., ordinals=True)`` and German numbers below 1.

``pronounce_ordinal`` honoured ``gender=`` for ru, uk, pl and cs, but
``pronounce_number(..., ordinals=True)`` reads its own ordinal speller and
gave the masculine for every gender. Sources for the expected values:

- Russian: the ICU RBNF rule sets ``spellout-ordinal-feminine`` and
  ``-neuter``, read from ``unicode_rbnf``, for numbers whose masculine reading
  matches ``spellout-ordinal-masculine``;
- Ukrainian: Wiktionary "перший", "другий", "третій";
- Polish: Wiktionary "pierwszy", "drugi", "trzeci";
- Czech: Wiktionary "druhý" and "první".

A German number below 1 lost its integer word: 0.5 gave " Komma fünf". The
expected value is the ICU RBNF ``de`` output, "null Komma fünf".
"""
import unittest

from unicode_rbnf import RbnfEngine

from ovos_number_parser import pronounce_number
from ovos_number_parser.util import GrammaticalGender

M = GrammaticalGender.MASCULINE
F = GrammaticalGender.FEMININE
N = GrammaticalGender.NEUTRAL


def _ordinal(number, lang, gender):
    return pronounce_number(number, lang, ordinals=True, gender=gender)


class TestOrdinalsFlagGender(unittest.TestCase):

    def test_russian_matches_rbnf(self):
        engine = RbnfEngine.for_language("ru")
        for number in (1, 2, 3, 21, 22, 40, 100, 123, 1000):
            masculine = engine.format_number(
                number, ruleset_names=["spellout-ordinal-masculine"]).text
            self.assertEqual(_ordinal(number, "ru", M), masculine)
            for gender, name in ((F, "feminine"), (N, "neuter")):
                with self.subTest(number=number, gender=gender):
                    expected = engine.format_number(
                        number, ruleset_names=[f"spellout-ordinal-{name}"]).text
                    self.assertEqual(_ordinal(number, "ru", gender), expected)

    def test_ukrainian(self):
        cases = {
            (1, F): "перша", (1, N): "перше", (2, F): "друга",
            (3, F): "третя", (3, N): "третє", (21, F): "двадцять перша",
            (2, M): "другий",
        }
        for (number, gender), expected in cases.items():
            with self.subTest(number=number, gender=gender):
                self.assertEqual(_ordinal(number, "uk", gender), expected)

    def test_polish(self):
        cases = {
            (1, F): "pierwsza", (1, N): "pierwsze", (2, F): "druga",
            (2, N): "drugie", (3, F): "trzecia", (3, N): "trzecie",
            (21, F): "dwudziesta pierwsza", (2, M): "drugi",
        }
        for (number, gender), expected in cases.items():
            with self.subTest(number=number, gender=gender):
                self.assertEqual(_ordinal(number, "pl", gender), expected)

    def test_czech(self):
        cases = {
            (2, F): "druhá", (2, N): "druhé", (2, M): "druhý",
            (1, F): "první", (1, N): "první",
        }
        for (number, gender), expected in cases.items():
            with self.subTest(number=number, gender=gender):
                self.assertEqual(_ordinal(number, "cs", gender), expected)


class TestGermanBelowOne(unittest.TestCase):

    def test_matches_rbnf(self):
        rbnf = RbnfEngine.for_language("de")
        self.assertEqual(pronounce_number(0.5, "de", places=1),
                         rbnf.format_number(0.5).text)
        self.assertEqual(pronounce_number(-0.9, "de", places=1),
                         "minus " + rbnf.format_number(0.9).text)

    def test_literals(self):
        self.assertEqual(pronounce_number(0.5, "de", places=1),
                         "null Komma fünf")
        self.assertEqual(pronounce_number(-0.9, "de", places=1),
                         "minus null Komma neun")


if __name__ == "__main__":
    unittest.main()
