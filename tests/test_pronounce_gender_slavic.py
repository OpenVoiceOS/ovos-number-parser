"""Russian, Ukrainian, Polish and Czech numbers agree with the noun's gender.

``pronounce_number`` and ``pronounce_ordinal`` took ``gender=`` and gave the
same word for all three genders. Sources for the expected values:

- cardinals: the ICU RBNF rule sets ``spellout-cardinal-feminine`` and
  ``spellout-cardinal-neuter`` of each language, read from ``unicode_rbnf``;
- Ukrainian ordinals: Wiktionary "перший", "другий", "третій" (adjective
  declension, nominative singular);
- Polish ordinals: Wiktionary "pierwszy", "drugi", "trzeci" (``pl-adecl``);
- Czech ordinals: Wiktionary "druhý" and "první" (``cs-adecl``): the hard
  "druhý" has "druhá" and "druhé", the soft "první" has one form.
"""
import unittest

from unicode_rbnf import RbnfEngine

from ovos_number_parser import pronounce_number, pronounce_ordinal
from ovos_number_parser.util import GrammaticalGender

M = GrammaticalGender.MASCULINE
F = GrammaticalGender.FEMININE
N = GrammaticalGender.NEUTRAL

RULESET = {F: "spellout-cardinal-feminine", N: "spellout-cardinal-neuter"}


class TestSlavicCardinalGender(unittest.TestCase):

    def test_cardinal_matches_rbnf(self):
        for lang in ("ru", "uk", "pl", "cs"):
            engine = RbnfEngine.for_language(lang)
            for gender, ruleset in RULESET.items():
                for number in (1, 2, 3, 21, 22, 101, 102):
                    with self.subTest(lang=lang, gender=gender, number=number):
                        expected = engine.format_number(
                            number, ruleset_names=[ruleset]).text
                        self.assertEqual(
                            pronounce_number(number, lang, gender=gender),
                            expected)

    def test_last_group_after_scale(self):
        self.assertEqual(pronounce_number(2001, "ru", gender=F),
                         "две тысячи одна")
        self.assertEqual(pronounce_number(1002, "uk", gender=F), "тисяча дві")
        self.assertEqual(pronounce_number(1002, "pl", gender=F), "tysiąc dwie")

    def test_polish_compound_keeps_jeden(self):
        # a compound ending in 1 keeps "jeden" for every gender (RBNF pl)
        for gender in (F, N):
            with self.subTest(gender=gender):
                self.assertEqual(pronounce_number(21, "pl", gender=gender),
                                 "dwadzieścia jeden")

    def test_masculine_default_unchanged(self):
        self.assertEqual(pronounce_number(1, "ru"), "один")
        self.assertEqual(pronounce_number(2, "uk", gender=M), "два")
        self.assertEqual(pronounce_number(1, "pl"), "jeden")
        self.assertEqual(pronounce_number(1, "cs"), "jedna")

    def test_decimal_not_inflected(self):
        self.assertEqual(pronounce_number(1.5, "ru", gender=F),
                         pronounce_number(1.5, "ru"))


class TestSlavicOrdinalGender(unittest.TestCase):

    def test_ukrainian(self):
        cases = {
            (1, M): "перший", (1, F): "перша", (1, N): "перше",
            (2, F): "друга", (2, N): "друге",
            (3, M): "третій", (3, F): "третя", (3, N): "третє",
            (21, F): "двадцять перша",
        }
        for (number, gender), expected in cases.items():
            with self.subTest(number=number, gender=gender):
                self.assertEqual(pronounce_ordinal(number, "uk", gender=gender),
                                 expected)

    def test_polish(self):
        cases = {
            (1, M): "pierwszy", (1, F): "pierwsza", (1, N): "pierwsze",
            (2, F): "druga", (2, N): "drugie",
            (3, F): "trzecia", (3, N): "trzecie",
            (21, F): "dwudziesta pierwsza",
        }
        for (number, gender), expected in cases.items():
            with self.subTest(number=number, gender=gender):
                self.assertEqual(pronounce_ordinal(number, "pl", gender=gender),
                                 expected)

    def test_czech(self):
        cases = {
            (2, M): "druhý", (2, F): "druhá", (2, N): "druhé",
            (1, F): "první", (1, N): "první",
            (22, F): "dvacátá druhá",
        }
        for (number, gender), expected in cases.items():
            with self.subTest(number=number, gender=gender):
                self.assertEqual(pronounce_ordinal(number, "cs", gender=gender),
                                 expected)


if __name__ == "__main__":
    unittest.main()
