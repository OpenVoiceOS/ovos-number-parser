"""Tunisian Arabic (ISO 639-3 aeb) cardinals.

Every expected string is an Arabic cell of English Wikipedia "Tunisian Arabic",
Numerals, Cardinals (revision 1384869026), or a form of its examples there, or a
form from "Tunisian Arabic morphology" (revision 1383344607), whichever is named
beside it. The table's own examples:
123456789 is "مية وثلاثة وعشرين مليون وأربعة مية وستّة وخمسين الف وسبعة ميه
وتسعة وثمانين" and 1956 is "الف وتسعة مية وستّة وخمسين".
"""
import unittest

from ovos_number_parser import extract_number, pronounce_number, resolve_ar_lect

TABLE_CELLS = {
    0: "صفر",                  # ṣfir صفر
    1: "واحد",                 # wāḥid واحد
    3: "ثلاثة",                # ŧlāŧa ثلاثة
    8: "ثمانية",               # ŧmanya ثمانية
    10: "عشرة",                # ɛacra عشرة
    11: "احداش",               # ḥdāc احداش
    12: "اثناش",               # ŧnāc اثناش
    13: "ثلطاش",               # morphology page "ثلطّاش θlaṭṭāš"; the table's cell has ظ
    14: "أربعطاش",             # morphology page "أربعطاش aṛbaʿṭāš"
    15: "خمسطاش",              # xumsṭāc خمسطاش
    16: "سطاش",                # morphology page "سطّاش sitṭāš"
    17: "سبعطاش",              # sbaɛṭāc سبعطاش
    18: "ثمنطاش",              # ŧmanṭāc ثمنطاش
    19: "تسعطاش",              # tsaɛṭāc تسعطاش
    20: "عشرين",               # ɛicrīn عشرين
    21: "واحد وعشرين",         # wāḥid w ɛicrīn واحد وعشرين
    30: "ثلاثين",              # ŧlāŧīn ثلاثين
    40: "أربعين",              # arbɛīn أربعين
    80: "ثمانين",              # ŧmanīn ثمانين
    100: "مية",                # mya مية
    101: "مية وواحد",          # mya w wāḥid مية وواحد
    110: "مية وعشرة",          # mya w ɛacra مية وعشرة
    200: "ميتين",              # mītīn ميتين
    300: "ثلاثة مية",          # ŧlāŧamya ثلاثة مية
    400: "أربعة مية",          # from the example 123456789
    700: "سبعة مية",           # from the example 123456789
    900: "تسعة مية",           # from the example 1956
    1000: "ألف",               # alf الف
    2000: "ألفين",             # alfīn الفين
    100000: "مية ألف",         # mya-t elf مية الف
    1000000: "مليون",          # malyūn مليون
}


class TestTunisianCardinals(unittest.TestCase):
    def test_wikipedia_table_cells(self):
        for number, cell in TABLE_CELLS.items():
            self.assertEqual(pronounce_number(number, lang="aeb"), cell, number)

    def test_the_two_worked_examples_of_the_table(self):
        self.assertEqual(pronounce_number(1956, lang="aeb"), "ألف وتسعة مية وستة وخمسين")
        self.assertEqual(
            pronounce_number(123456789, lang="aeb"),
            "مية وثلاثة وعشرين مليون وأربعة مية وستة وخمسين ألف وسبعة مية وتسعة وثمانين")

    def test_a_hundred_the_table_does_not_give_keeps_the_literary_word(self):
        for number, said in ((500, "خمسمئة"), (600, "ستمئة"), (800, "ثمانمئة")):
            self.assertEqual(pronounce_number(number, lang="aeb"), said, number)

    def test_aeb_resolves_and_the_region_subtag_stays_standard(self):
        self.assertEqual(resolve_ar_lect("aeb"), "aeb")
        self.assertEqual(resolve_ar_lect("AEB-TN"), "aeb")
        self.assertIsNone(resolve_ar_lect("ar-TN"))
        self.assertEqual(pronounce_number(13, lang="ar-TN"), "ثلاثة عشر")

    def test_other_lects_do_not_say_the_tunisian_words(self):
        self.assertEqual(pronounce_number(13, lang="ary"), "تلتاش")
        self.assertEqual(pronounce_number(13, lang="apc"), "تلتعش")
        self.assertEqual(pronounce_number(13, lang="acm"), "ثلاثة عشر")

    def test_a_composed_number_reads_back(self):
        for value in (11, 16, 300, 350, 1956, 2018):
            spoken = pronounce_number(value, lang="aeb")
            self.assertEqual(extract_number(spoken, lang="ar"), value, spoken)


if __name__ == "__main__":
    unittest.main()
