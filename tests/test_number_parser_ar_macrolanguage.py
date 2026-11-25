"""Every member of the ISO 639-3 macrolanguage ara is served by the Arabic engine.

The member list is the 30 rows with macrolanguage "ara" of the SIL ISO 639-3
macrolanguage mappings page,
https://iso639-3.sil.org/code_tables/macrolanguage_mappings/data.
"""
import unittest

from ovos_number_parser import pronounce_number

ARA_MEMBERS = [
    "aao", "abh", "abv", "acm", "acq", "acw", "acx", "acy", "adf", "aeb",
    "aec", "afb", "ajp", "apc", "apd", "arb", "arq", "ars", "ary", "arz",
    "auz", "avl", "ayh", "ayl", "ayn", "ayp", "bbz", "pga", "shu", "ssh",
]

# members with no table of their own: the literary words, oblique register
NO_TABLE = [c for c in ARA_MEMBERS
            if c not in ("acw", "afb", "arz", "ars", "apc", "ajp", "ary", "aeb", "arq", "arb")]


class TestArabicMacrolanguageMembers(unittest.TestCase):
    def test_the_list_has_30_distinct_codes(self):
        self.assertEqual(len(ARA_MEMBERS), 30)
        self.assertEqual(len(set(ARA_MEMBERS)), 30)

    def test_no_member_raises_and_each_says_an_arabic_word(self):
        for code in ARA_MEMBERS:
            for number in (0, 7, 13, 21, 100, 350, 2018, 1000000):
                said = pronounce_number(number, lang=code)
                self.assertTrue(said.strip(), (code, number))
                self.assertTrue(all("؀" <= c <= "ۿ" or c == " " for c in said),
                                (code, number, said))

    def test_a_member_with_no_table_speaks_the_literary_words_in_the_oblique(self):
        for code in NO_TABLE:
            self.assertEqual(pronounce_number(13, lang=code), "ثلاثة عشر", code)
            self.assertEqual(pronounce_number(350, lang=code), "ثلاثمئة وخمسين", code)
            self.assertEqual(pronounce_number(2, lang=code), "اثنين", code)

    def test_standard_arabic_keeps_the_nominative(self):
        for code in ("ar", "arb"):
            self.assertEqual(pronounce_number(350, lang=code), "ثلاثمئة وخمسون", code)

    def test_a_member_with_a_table_keeps_it(self):
        self.assertEqual(pronounce_number(13, lang="arz"), "تلتاشر")
        self.assertEqual(pronounce_number(15, lang="acw"), "خمسطعش")

    def test_region_subtags_and_case_stay_as_they_were(self):
        self.assertEqual(pronounce_number(13, lang="ar-EG"), "ثلاثة عشر")
        self.assertEqual(pronounce_number(350, lang="ar-DZ"), "ثلاثمئة وخمسون")
        self.assertEqual(pronounce_number(350, lang="AYL-LY"), "ثلاثمئة وخمسين")
        self.assertEqual(pronounce_number(350, lang="ayl_LY"), "ثلاثمئة وخمسين")


if __name__ == "__main__":
    unittest.main()
