"""Algerian Arabic (ISO 639-3 arq) cardinals.

Every expected string is the Arabic script that Belkassem Ben Sedira prints beside
its transliteration in "Notions élémentaires de grammaire arabe", Nombres, of his
Dictionnaire français-arabe (dialecte d'Algérie), Algiers, 1882, pp. XLIII-XLV,
read on the page images. The transliteration is beside each form. The book
prints 300 and 400 as two words; they are written as one, as in the other lect
tables.
"""
import unittest

from ovos_number_parser import extract_number, numbers_to_digits, pronounce_number, resolve_ar_lect

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
            with self.subTest(value=value):
                spoken = pronounce_number(value, lang="arq")
                self.assertEqual(extract_number(spoken, lang="arq"), value, spoken)

    def test_ben_sedira_three_hundred_is_read_only_as_arq(self):
        """ثلثمية is the book's ثلث مية "thelth mia", "Trois cents". ثلث is also "a third"."""
        with self.subTest(case='extract_number("ثلثمية وخمسين", lang="arq")'):
            self.assertEqual(extract_number("ثلثمية وخمسين", lang="arq"), 350)
        for lang in ("ar", "ar-DZ", "arz"):
            with self.subTest(lang=lang):
                self.assertIs(extract_number("ثلثمية", lang=lang), False, lang)
                self.assertEqual(numbers_to_digits("ثلثمية", lang=lang), "ثلثمية", lang)

    def test_the_printed_two_word_three_hundred_reads_300_as_arq(self):
        """Ben Sedira p. XLV prints 300 as ثلث مية. ثلث alone stays "a third"."""
        with self.subTest(case='extract_number("ثلث مية", lang="arq")'):
            self.assertEqual(extract_number("ثلث مية", lang="arq"), 300)
        with self.subTest(case='extract_number("ثلث مية وخمسين", lang="arq")'):
            self.assertEqual(extract_number("ثلث مية وخمسين", lang="arq"), 350)
        with self.subTest(case='numbers_to_digits("عندي ثلث مية ريال", lang="arq")'):
            self.assertEqual(numbers_to_digits("عندي ثلث مية ريال", lang="arq"), "عندي 300 ريال")
        with self.subTest(case='extract_number("ثلث", lang="arq")'):
            self.assertEqual(extract_number("ثلث", lang="arq"), 1 / 3)
        with self.subTest(case='numbers_to_digits("أكلت ثلث الكعكة", lang="arq")'):
            self.assertEqual(numbers_to_digits("أكلت ثلث الكعكة", lang="arq"), "أكلت ثلث الكعكة")
        for lang in ("ar", "ar-DZ", "arz"):
            with self.subTest(lang=lang):
                self.assertEqual(extract_number("ثلث مية", lang=lang), 1 / 3, lang)

    def test_arq_keeps_the_conjunction_on_its_own_words(self):
        with self.subTest(case='numbers_to_digits("1 وثلثمية", lang="arq")'):
            self.assertEqual(numbers_to_digits("1 وثلثمية", lang="arq"), "1 و300")
        with self.subTest(case='numbers_to_digits("كتاب وثلثاش", lang="arq")'):
            self.assertEqual(numbers_to_digits("كتاب وثلثاش", lang="arq"), "كتاب و13")
        with self.subTest(case='numbers_to_digits("كتاب وأربعة", lang="ar")'):
            self.assertEqual(numbers_to_digits("كتاب وأربعة", lang="ar"), "كتاب و4")

    def test_other_lects_read_the_two_words_as_dev_does(self):
        """Only arq joins ثلث مية. Everywhere else the two words are "a third" and
        "a hundred", with the spacing and line break the shared converter gives."""
        for lang in ("ar", "ar-DZ", "arz", "apc"):
            self.assertEqual(numbers_to_digits("ثلث مية", lang=lang), "ثلث مية", lang)
            self.assertEqual(numbers_to_digits("ثلث\nمية", lang=lang), "ثلث مية", lang)
            self.assertEqual(numbers_to_digits("عندي ثلث مية ريال", lang=lang),
                             "عندي ثلث 100 ريال", lang)
            self.assertEqual(numbers_to_digits("وثلث مية", lang=lang), "و ثلث مية", lang)


if __name__ == "__main__":
    unittest.main()
