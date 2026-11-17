"""Algerian Arabic (ISO 639-3 arq) cardinals.

Every expected string is the Arabic script that Belkassem Ben Sedira prints beside
its transliteration in "Notions élémentaires de grammaire arabe", Nombres, of his
Dictionnaire français-arabe (dialecte d'Algérie), Algiers, 1882, pp. XLIII-XLV,
read on the page images. The transliteration is beside each form. The book
prints 300 and 400 as two words; they are written as one, as in the other lect
tables.
"""
import unittest

from ovos_number_parser import extract_number, pronounce_number, resolve_ar_lect

BEN_SEDIRA = {
    1: "واحد",             # ouah'ad
    3: "ثلاثة",            # thlatha
    8: "ثمانية",           # thmania
    9: "تسعة",             # tsâ
    10: "عشرة",            # âchra
    11: "احداش",           # h'adâch
    12: "اثناش",           # thnâch
    13: "ثلثاش",           # thelethâch
    14: "اربعتاش",         # arbâtâch
    15: "خمستاش",          # khamstâch
    16: "ستاش",            # settâch
    17: "سبعتاش",          # sebâtâch
    18: "ثمنتاش",          # thementâch
    19: "تسعتاش",          # tsâtâch
    20: "عشرين",           # âchrin
    21: "واحد وعشرين",     # ouah'ad ou âchrin
    30: "ثلاثين",          # thlathin
    35: "خمسة وثلاثين",    # khamsa ou thlathin
    70: "سبعين",           # sebâin
    80: "ثمانين",          # thmanin
    90: "تسعين",           # tsâin
    100: "مية",            # mia
    200: "ميتين",          # mitein
    300: "ثلثمية",         # thelth mia
    400: "اربعمية",        # arbâ mia
    1000: "ألف",           # alf
    2000: "ألفين",         # alfein
}


class TestAlgerianCardinals(unittest.TestCase):
    def test_ben_sedira_page_forms(self):
        for number, form in BEN_SEDIRA.items():
            self.assertEqual(pronounce_number(number, lang="arq"), form, number)

    def test_a_number_the_page_does_not_give_keeps_the_literary_word(self):
        self.assertEqual(pronounce_number(500, lang="arq"), "خمسمئة")
        self.assertEqual(pronounce_number(3000, lang="arq"), "ثلاثة آلاف")

    def test_arq_resolves_and_the_region_subtag_stays_standard(self):
        self.assertEqual(resolve_ar_lect("arq"), "arq")
        self.assertEqual(resolve_ar_lect("ARQ-DZ"), "arq")
        self.assertIsNone(resolve_ar_lect("ar-DZ"))
        self.assertEqual(pronounce_number(13, lang="ar-DZ"), "ثلاثة عشر")

    def test_other_lects_do_not_say_the_algerian_words(self):
        self.assertEqual(pronounce_number(13, lang="arz"), "تلتاشر")
        self.assertEqual(pronounce_number(13, lang="acm"), "ثلاثة عشر")

    def test_a_composed_number_reads_back(self):
        for value in (11, 13, 19, 300, 350, 400, 2018, 11000):
            spoken = pronounce_number(value, lang="arq")
            self.assertEqual(extract_number(spoken, lang="ar"), value, spoken)


if __name__ == "__main__":
    unittest.main()
