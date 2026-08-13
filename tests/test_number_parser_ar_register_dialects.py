"""Register-aware Arabic pronunciation and Arabic dialect language-code
routing.

Gold strings for the oblique (genitive/accusative) forms are hand-derived
from the closed-set substitution documented on ``numbers_ar._oblique``: the
nominative dual ending -ān and the nominative sound-masculine-plural (tens)
ending -ūn are both spelled with two letters (``ان``/``ون``) and are both
replaced by the two-letter oblique ending -īn (``ين``). Citation: Karin C.
Ryding, "A Reference Grammar of Modern Standard Arabic" (Cambridge
University Press, 2005), section 9.2 (the dual) and section 9.5.2 (the
sound masculine plural / tens) on the nominative vs oblique case endings.

ISO 639-3 code meanings used below are from the SIL code table,
https://iso639-3.sil.org/code_tables/639/data, cross-checked against
Glottolog (https://glottolog.org).
"""
import unittest

from ovos_number_parser import (extract_number, pronounce_number,
                                pronounce_ordinal, is_fractional, is_ordinal)
from ovos_number_parser.numbers_ar import (pronounce_number_ar,
                                           nice_number_ar, resolve_ar_lang)


class TestArabicRegisterPronunciation(unittest.TestCase):
    """pronounce_number_ar(case=...) / pronounce_number(..., case=...)."""

    def test_default_is_byte_identical_to_pre_existing_behaviour(self):
        # case defaults to "nominative"; omitting it must not change a
        # single output versus the pre-existing (pre-feature) behaviour.
        for number in [0, 1, 2, 11, 12, 20, 22, 25, 42, 50, 99, 100, 123,
                       200, 223, 999, 1000, 1985, 2000, 2023, 2000000,
                       2000000000, -42, 5.2, 5.25]:
            with self.subTest(number=number):
                self.assertEqual(pronounce_number_ar(number),
                                 pronounce_number_ar(number, case="nominative"))
                self.assertEqual(pronounce_number(number, lang="ar"),
                                 pronounce_number_ar(number))

    def test_tens_oblique(self):
        expected = {20: 'عشرين', 30: 'ثلاثين', 40: 'أربعين', 50: 'خمسين',
                    60: 'ستين', 70: 'سبعين', 80: 'ثمانين', 90: 'تسعين'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(
                    pronounce_number_ar(number, case="oblique"), spoken)

    def test_compound_tens_oblique(self):
        expected = {21: 'واحد وعشرين', 22: 'اثنين وعشرين',
                    25: 'خمسة وعشرين', 42: 'اثنين وأربعين',
                    66: 'ستة وستين', 99: 'تسعة وتسعين'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(
                    pronounce_number_ar(number, case="oblique"), spoken)

    def test_duals_oblique(self):
        expected = {2: 'اثنين', 200: 'مئتين', 2000: 'ألفين',
                    2000000: 'مليونين', 2000000000: 'مليارين'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(
                    pronounce_number_ar(number, case="oblique"), spoken)

    def test_hundreds_compounds_oblique(self):
        expected = {123: 'مئة وثلاثة وعشرين',
                    223: 'مئتين وثلاثة وعشرين',
                    999: 'تسعمئة وتسعة وتسعين',
                    1985: 'ألف وتسعمئة وخمسة وثمانين',
                    2023: 'ألفين وثلاثة وعشرين'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(
                    pronounce_number_ar(number, case="oblique"), spoken)

    def test_scales_oblique(self):
        # 3-10 counted scale nouns and single/plural scale words are outside
        # the dual/tens closed set and are unaffected by case
        self.assertEqual(pronounce_number_ar(3000, case="oblique"),
                         'ثلاثة آلاف')
        self.assertEqual(pronounce_number_ar(1000000, case="oblique"),
                         'مليون')
        self.assertEqual(pronounce_number_ar(1000000000, case="oblique"),
                         'مليار')

    def test_fractions_dual_oblique(self):
        self.assertEqual(nice_number_ar(2 / 3, denominators=[3]), 'ثلثان')
        self.assertEqual(
            nice_number_ar(2 / 3, denominators=[3], case="oblique"),
            'ثلثين')
        self.assertEqual(nice_number_ar(2 / 2, denominators=[2]), '1')
        # 1 whole + 2/4ths, numerator 2 -> dual of ربع (ربعان / ربعين)
        self.assertEqual(nice_number_ar(1 + 2 / 4, denominators=[4]),
                         '1 وربعان')
        self.assertEqual(
            nice_number_ar(1 + 2 / 4, denominators=[4], case="oblique"),
            '1 وربعين')

    def test_decimals_unaffected_by_case(self):
        # decimal digits are read one at a time in their citation form
        # regardless of register; only the closed dual/tens sets inflect
        for number in [5.2, 5.25, 0.5, -3.5]:
            with self.subTest(number=number):
                self.assertEqual(
                    pronounce_number_ar(number, case="oblique"),
                    pronounce_number_ar(number))

    def test_negative_oblique(self):
        self.assertEqual(pronounce_number_ar(-42, case="oblique"),
                         'سالب اثنين وأربعين')
        self.assertEqual(pronounce_number_ar(-7, case="oblique"),
                         'سالب سبعة')

    def test_ordinals_unaffected_by_case(self):
        # ordinals do not carry the nominative/oblique case distinction
        # this feature adds; case is accepted but has no effect
        for number in [1, 2, 12, 20, 21, 25, 100]:
            with self.subTest(number=number):
                self.assertEqual(
                    pronounce_number_ar(number, ordinals=True, case="oblique"),
                    pronounce_number_ar(number, ordinals=True))
                self.assertEqual(
                    pronounce_ordinal(number, lang="ar"),
                    pronounce_number_ar(number, ordinals=True))

    def test_top_level_pronounce_number_case_kwarg(self):
        self.assertEqual(pronounce_number(55, lang="ar", case="oblique"),
                         'خمسة وخمسين')
        self.assertEqual(pronounce_number(55, lang="ar"), 'خمسة وخمسون')
        self.assertEqual(pronounce_number(55, lang="ar", case="nominative"),
                         'خمسة وخمسون')


class TestArabicDialectResolution(unittest.TestCase):
    """resolve_ar_lang and the dialect-aware dispatch it drives."""

    def test_resolve_ar_lang_table(self):
        # arb (Standard Arabic) and the ar macrolanguage default nominative
        self.assertEqual(resolve_ar_lang("ar"), "nominative")
        self.assertEqual(resolve_ar_lang("arb"), "nominative")
        # spoken lects default to the oblique case, per grammatical
        # description of these varieties (colloquial Arabic has lost the
        # nominative -ūn/-ān as productive case marking in most contexts and
        # generalizes the oblique -īn form; see e.g. Kristen Brustad, "The
        # Syntax of Spoken Arabic" (Georgetown UP, 2000), ch. 2)
        for code in ["ars", "acw", "afb", "arz", "apc", "ajp", "acm", "ary",
                     "aeb", "ayl"]:
            with self.subTest(code=code):
                self.assertEqual(resolve_ar_lang(code), "oblique")

    def test_resolve_ar_lang_bcp47_forms(self):
        for code in ["ar-SA", "ar-EG", "AR", "ar-x-something"]:
            with self.subTest(code=code):
                self.assertEqual(resolve_ar_lang(code), "nominative")
        for code in ["ars-SA", "ARZ", "afb-KW"]:
            with self.subTest(code=code):
                self.assertEqual(resolve_ar_lang(code), "oblique")

    def test_resolve_ar_lang_rejects_non_arabic_ar_prefixed_codes(self):
        # "arn" (Mapudungun) and "arc" (Official Aramaic) both start with
        # "ar" but are not Arabic; a lang.startswith("ar") check would
        # wrongly route them to this engine, resolve_ar_lang must not
        self.assertIsNone(resolve_ar_lang("arn"))
        self.assertIsNone(resolve_ar_lang("arc"))
        self.assertIsNone(resolve_ar_lang("en"))
        self.assertIsNone(resolve_ar_lang(""))

    def test_dialects_pronounce_with_their_default_register(self):
        # a code missed by "startswith('ar')" (does not begin with "ar")
        for code in ["acw", "afb", "apc", "ajp", "acm"]:
            with self.subTest(code=code):
                self.assertEqual(pronounce_number(55, lang=code),
                                 'خمسة وخمسين')
                self.assertEqual(pronounce_number(2, lang=code), 'اثنين')
                self.assertEqual(pronounce_number(200, lang=code), 'مئتين')

        # codes that DID already start with "ar" (ars, arz, ary, aeb, ayl)
        for code in ["ars", "arz", "ary", "aeb", "ayl"]:
            with self.subTest(code=code):
                self.assertEqual(pronounce_number(55, lang=code),
                                 'خمسة وخمسين')

        # the literary standard keeps the nominative default
        for code in ["ar", "arb"]:
            with self.subTest(code=code):
                self.assertEqual(pronounce_number(55, lang=code),
                                 'خمسة وخمسون')

    def test_explicit_case_overrides_dialect_default(self):
        self.assertEqual(
            pronounce_number(55, lang="afb", case="nominative"),
            'خمسة وخمسون')
        self.assertEqual(
            pronounce_number(55, lang="ar", case="oblique"),
            'خمسة وخمسين')

    def test_extract_number_dispatch(self):
        for code in ["acw", "afb", "apc", "ajp", "acm", "ars", "arz", "ary",
                     "aeb", "ayl", "arb"]:
            with self.subTest(code=code):
                self.assertEqual(
                    extract_number("خمسة وعشرون", lang=code), 25)
                # extraction already accepted both cases as input before
                # this change; dialect routing must not break that
                self.assertEqual(
                    extract_number("خمسة وعشرين", lang=code), 25)

    def test_pronounce_ordinal_dispatch(self):
        for code in ["acw", "afb", "apc", "ajp", "acm"]:
            with self.subTest(code=code):
                self.assertEqual(pronounce_ordinal(25, lang=code),
                                 'الخامس والعشرون')

    def test_is_fractional_dispatch(self):
        for code in ["acw", "afb", "apc", "ajp", "acm"]:
            with self.subTest(code=code):
                self.assertEqual(is_fractional("نصف", lang=code), 0.5)

    def test_is_ordinal_dispatch(self):
        for code in ["acw", "afb", "apc", "ajp", "acm"]:
            with self.subTest(code=code):
                self.assertEqual(is_ordinal("الخامس", lang=code), 5)


if __name__ == "__main__":
    unittest.main()
