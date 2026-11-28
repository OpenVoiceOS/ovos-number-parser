"""Oblique-case regression for twelve.

Twelve is a compound numeral (اثنا عشر) that declines in its first element
only: nominative اثنا عشر, oblique (genitive/accusative) اثني عشر, exactly
like the dual اثنان -> اثنين it is built on. عشر itself never changes.
Citation: Karin C. Ryding, "A Reference Grammar of Modern Standard Arabic"
(Cambridge University Press, 2005), section 9.2 (the dual, -ān/-ayn) covers
the same element embedded in twelve. Reported by Athmane Mokraoui in an
external review of arbtok, which passes the case through to this parser.

Eleven (أحد عشر) does not decline in either case, and the teens 13-19
(ثلاثة عشر .. تسعة عشر) never decline for case in MSA -- only the closed
dual/tens sets ``_oblique`` documents inflect.
"""
import unittest

from ovos_number_parser import extract_number, pronounce_number
from ovos_number_parser.numbers_ar import pronounce_number_ar


class TestObliqueTwelve(unittest.TestCase):

    def test_twelve_oblique(self):
        self.assertEqual(pronounce_number_ar(12, case="oblique"), 'اثني عشر')

    def test_twelve_nominative_unchanged(self):
        self.assertEqual(pronounce_number_ar(12), 'اثنا عشر')
        self.assertEqual(pronounce_number_ar(12, case="nominative"),
                         'اثنا عشر')

    def test_compound_hundreds_and_thousands_with_twelve_oblique(self):
        expected = {112: 'مئة واثني عشر', 212: 'مئتين واثني عشر',
                    2012: 'ألفين واثني عشر', 1012: 'ألف واثني عشر'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(
                    pronounce_number_ar(number, case="oblique"), spoken)

    def test_compound_hundreds_and_thousands_with_twelve_nominative(self):
        expected = {112: 'مئة واثنا عشر', 212: 'مئتان واثنا عشر',
                    2012: 'ألفان واثنا عشر', 1012: 'ألف واثنا عشر'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number_ar(number), spoken)

    def test_other_teens_unchanged_in_both_cases(self):
        # 11 and 13-19 do not carry the nominative/oblique distinction; the
        # oblique register must produce byte-identical output for them
        for number in [11, 13, 14, 15, 16, 17, 18, 19]:
            with self.subTest(number=number):
                self.assertEqual(pronounce_number_ar(number, case="oblique"),
                                 pronounce_number_ar(number))

    def test_eleven_both_cases(self):
        self.assertEqual(pronounce_number_ar(11), 'أحد عشر')
        self.assertEqual(pronounce_number_ar(11, case="oblique"), 'أحد عشر')

    def test_top_level_pronounce_number_twelve_oblique(self):
        self.assertEqual(pronounce_number(12, lang="ar", case="oblique"),
                         'اثني عشر')
        self.assertEqual(pronounce_number(112, lang="ar", case="oblique"),
                         'مئة واثني عشر')
        self.assertEqual(pronounce_number(2012, lang="ar", case="oblique"),
                         'ألفين واثني عشر')

    def test_extract_number_reads_both_forms_of_twelve(self):
        self.assertEqual(extract_number("اثنا عشر", lang="ar"), 12)
        self.assertEqual(extract_number("اثني عشر", lang="ar"), 12)

    def test_extract_number_reads_both_forms_of_twelve_in_a_compound(self):
        self.assertEqual(extract_number("مئة واثنا عشر", lang="ar"), 112)
        self.assertEqual(extract_number("مئة واثني عشر", lang="ar"), 112)


if __name__ == "__main__":
    unittest.main()
