"""A German number whose lower triplets are all zero ends on a scale word.

The speller joins a scale word ("Million", "Milliarde") to the lower triplets
with a space, and it kept that space when no lower triplet followed. The
expected strings are the output of the ICU RBNF ``de`` rule set
``spellout-cardinal-feminine`` (``unicode_rbnf``), which writes the scale words
with no trailing space.
"""
import unittest

from unicode_rbnf import RbnfEngine

from ovos_number_parser import pronounce_number


class TestGermanScaleNoTrailingSpace(unittest.TestCase):

    def test_round_scale_matches_rbnf(self):
        rbnf = RbnfEngine.for_language("de")
        for number in (10 ** 6, 2 * 10 ** 6, 10 ** 9, 3 * 10 ** 9, 10 ** 12):
            with self.subTest(number=number):
                expected = rbnf.format_number(
                    number, ruleset_names=["spellout-cardinal-feminine"]).text
                self.assertEqual(pronounce_number(number, lang="de"), expected)

    def test_literal_values(self):
        self.assertEqual(pronounce_number(10 ** 9, lang="de"), "eine Milliarde")
        self.assertEqual(pronounce_number(-10 ** 6, lang="de"),
                         "minus eine Million")

    def test_decimal_after_round_scale_has_one_space(self):
        self.assertEqual(pronounce_number(1000000.5, lang="de", places=1),
                         "eine Million Komma fünf")


if __name__ == "__main__":
    unittest.main()
