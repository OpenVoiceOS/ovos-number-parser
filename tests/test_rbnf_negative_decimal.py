"""The Unicode RBNF fallback keeps the fraction of a negative number.

``unicode_rbnf`` reads a negative number through the rule set's "-x" rule,
which formats ``int(-number)``, so -12.25 read as "minus twelve". The
expected reading of -x is the reading of x with the minus word of the rule
set on the side the rule set puts it. The minus word is the engine's reading
of -1 less its reading of 1, both read straight from ``unicode_rbnf``.
"""
import unittest
from decimal import Decimal

from unicode_rbnf import FormatPurpose, RbnfEngine

from ovos_number_parser import (_pronounce_rbnf, pronounce_number,
                                pronounce_ordinal)
from ovos_number_parser.util import GrammaticalGender

F = GrammaticalGender.FEMININE

#: the languages with no native module that the RBNF data reads; zu has no
#: rule for negative numbers and is tested on its own, and lo, whose RBNF
#: data has the Thai minus word, is tested in test_rbnf_decimal_words
FALLBACK_LANGS = (
    "af", "ak", "am", "be", "bs", "ccp", "chr", "cy", "ee", "eo", "ff", "fo",
    "ga", "hi", "hy", "is", "ja", "ka", "kk", "kl", "km", "ko", "ky", "lb",
    "lrc", "lt", "lv", "mk", "mt", "my", "ne", "qu", "se", "sq", "sr",
    "sr_Latn", "su", "sw", "ta", "th", "vec", "vi", "yue", "yue_Hans", "zh",
    "zh_Hant",
)

#: languages whose RBNF data has a feminine cardinal rule set
FEMININE_LANGS = ("be", "is", "lt", "lv", "mk", "sr", "vec")


def _rbnf(lang, number, ruleset=None):
    engine = RbnfEngine.for_language(lang)
    if ruleset is None:
        return engine.format_number(number).text
    return engine.format_number(number, ruleset_names=[ruleset]).text


def _minus_sides(lang, ruleset=None):
    """The text before and after the number in the reading of -1."""
    minus_one, one = _rbnf(lang, -1, ruleset), _rbnf(lang, 1, ruleset)
    if minus_one.endswith(one):
        return minus_one[:-len(one)], ""
    assert minus_one.startswith(one), (lang, minus_one, one)
    return "", minus_one[len(one):]


class TestRbnfNegativeDecimal(unittest.TestCase):

    def test_negative_decimal_keeps_fraction(self):
        for lang in FALLBACK_LANGS:
            before, after = _minus_sides(lang)
            for number in (12.25, 0.5, 3.75):
                with self.subTest(lang=lang, number=number):
                    positive = pronounce_number(number, lang)
                    negative = pronounce_number(-number, lang)
                    self.assertIn(positive, negative)
                    self.assertIn((before + after).strip(), negative)
                    self.assertEqual(negative, before + positive + after)

    def test_afrikaans_literal(self):
        self.assertEqual(pronounce_number(-12.25, "af"),
                         "min twaalf komma twee vyf")

    def test_minus_word_after_the_number(self):
        # the Ewe rule set puts the minus word after the number
        self.assertEqual(_minus_sides("ee"), ("", " xlẽyimegbee"))
        self.assertEqual(pronounce_number(-0.5, "ee"),
                         pronounce_number(0.5, "ee") + " xlẽyimegbee")

    def test_negative_decimal_keeps_gender_rule_set(self):
        for lang in FEMININE_LANGS:
            before, after = _minus_sides(lang, "spellout-cardinal-feminine")
            for number in (12.25, 0.5, 3.75):
                with self.subTest(lang=lang, number=number):
                    positive = pronounce_number(number, lang, gender=F)
                    self.assertEqual(pronounce_number(-number, lang, gender=F),
                                     before + positive + after)

    def test_negative_integer_unchanged(self):
        for lang in FALLBACK_LANGS:
            for number in (-1, -12, -300, -12.0):
                with self.subTest(lang=lang, number=number):
                    self.assertEqual(pronounce_number(number, lang),
                                     _rbnf(lang, number))
        for lang in FEMININE_LANGS:
            with self.subTest(lang=lang, gender=F):
                self.assertEqual(
                    pronounce_number(-21, lang, gender=F),
                    _rbnf(lang, -21, "spellout-cardinal-feminine"))

    def test_negative_ordinal_unchanged(self):
        for lang in ("af", "ko", "sw", "ta", "eo"):
            engine = RbnfEngine.for_language(lang)
            for number in (-3, -2.5):
                with self.subTest(lang=lang, number=number):
                    expected = engine.format_number(
                        number, FormatPurpose.ORDINAL).text
                    self.assertEqual(pronounce_ordinal(number, lang), expected)
                    self.assertEqual(
                        pronounce_number(number, lang, ordinals=True),
                        expected)
        self.assertEqual(pronounce_ordinal(-3, "hi", gender=F),
                         _rbnf("hi", -3, "spellout-ordinal-feminine"))

    def test_language_without_negative_rule_still_raises(self):
        for number in (-12, -12.25):
            with self.subTest(number=number):
                with self.assertRaises(NotImplementedError):
                    pronounce_number(number, "zu")

    def test_non_finite_values_keep_the_engine_error(self):
        for number in (Decimal("NaN"), Decimal("-Infinity")):
            with self.subTest(number=number):
                with self.assertRaises(NotImplementedError):
                    _pronounce_rbnf(number, "af", False,
                                    GrammaticalGender.MASCULINE)


if __name__ == "__main__":
    unittest.main()
