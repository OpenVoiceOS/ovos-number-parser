"""Moroccan Arabic (ISO 639-3 ary) cardinals.

Every expected string is a headword of an English Wiktionary Moroccan Arabic
number entry, or the headword of the compound entry for the number, quoted from
the raw wikitext (Appendix:Moroccan Arabic numerals, revision 75382086, lists
them). The transliteration of the entry is beside each.
"""
import unittest

from ovos_number_parser import (extract_number, nice_number, numbers_to_digits,
                                pronounce_number, resolve_ar_lect)

WIKTIONARY_ENTRIES = {
    0: "صفر",                  # not an ary numeral entry: the literary word stays
    1: "واحد",                 # واحد wāḥid
    2: "تنين",                 # تنين tnīn
    3: "تلاتة",                # تلاتة tlāta
    4: "ربعة",                 # ربعة rabʕa
    5: "خمسة",                 # خمسة ḵamsa
    6: "ستة",                  # ستة sitta
    7: "سبعة",                 # سبعة sabʕa
    8: "تمنية",                # تمنية tmanya
    9: "تسعة",                 # تسعة tisʕa
    10: "عشرة",                # عشرة ʕašra
    11: "حداش",                # حداش ḥdāš
    12: "تناش",                # تناش tnāš
    13: "تلتاش",               # تلتاش tlattāš
    14: "ربعتاش",              # ربعتاش rbaʕtāš
    15: "خمستاش",              # خمستاش ḵmastāš
    16: "ستاش",                # ستاش sittāš
    17: "سبعتاش",              # سبعتاش sbaʕtāš
    18: "تمنتاش",              # تمنتاش tmantāš
    19: "تسعتاش",              # تسعتاش tsaʕtāš
    20: "عشرين",               # عشرين ʕašrīn
    21: "واحد وعشرين",         # واحد وعشرين wāḥed u ʕašrīn
    22: "تنين وعشرين",         # تنين وعشرين tnīn u ʕašrīn
    30: "تلاتين",              # تلاتين tlātīn
    33: "تلاتة وتلاتين",       # تلاتة وتلاتين tlāta w tlātīn
    40: "ربعين",               # ربعين rabʕīn
    50: "خمسين",               # خمسين ḵamsīn
    60: "ستين",                # ستين sittīn
    70: "سبعين",               # سبعين sabʕīn
    80: "تمانين",              # تمانين tmānīn
    90: "تسعين",               # تسعين tisʕīn
    100: "مية",                # مية myā
    200: "ميتين",              # ميتين myatayn, myatīn, mītīn
    300: "تلتمية",             # تلتمية taltimya
    400: "ربعمية",             # ربعمية rabʕamya
    500: "خمسمية",             # خمسمية xamsamya
    600: "ستمية",              # ستمية sittimya
    700: "سبعمية",             # سبعمية sabʕamya
    800: "تمنمية",             # تمنمية tamnamya
    900: "تسعمية",             # تسعمية tisʕamya
    1000: "ألف",               # ألف ʔalf
    2000: "ألفين",             # ألفين ʔalfayn, ʔalfīn
    10000: "عشر آلاف",         # عشر آلاف ʕašr ʔālāf
    100000: "مية ألف",         # مية ألف myat ʔalf
    1000000: "مليون",          # مليون malyūn
}


class TestMoroccanCardinals(unittest.TestCase):
    def test_wiktionary_entries(self):
        for number, headword in WIKTIONARY_ENTRIES.items():
            self.assertEqual(pronounce_number(number, lang="ary"), headword, number)

    def test_joiner_is_wa_before_the_unit_and_the_ten(self):
        self.assertEqual(pronounce_number(44, lang="ary"), "ربعة وربعين")
        self.assertEqual(pronounce_number(102, lang="ary"), "مية وتنين")
        self.assertEqual(pronounce_number(350, lang="ary"), "تلتمية وخمسين")

    def test_ary_resolves_and_the_region_subtag_stays_standard(self):
        self.assertEqual(resolve_ar_lect("ary"), "ary")
        self.assertEqual(resolve_ar_lect("ARY-MA"), "ary")
        self.assertIsNone(resolve_ar_lect("ar-MA"))
        self.assertEqual(pronounce_number(13, lang="ar-MA"), "ثلاثة عشر")

    def test_other_lects_do_not_say_the_moroccan_words(self):
        self.assertEqual(pronounce_number(13, lang="arz"), "تلتاشر")
        self.assertEqual(pronounce_number(13, lang="apc"), "تلتعش")
        self.assertEqual(pronounce_number(13, lang="aeb"), "ثلاثة عشر")

    def test_a_composed_number_reads_back(self):
        for value in (4, 14, 40, 44, 350, 2018, 12000):
            spoken = pronounce_number(value, lang="ary")
            self.assertEqual(extract_number(spoken, lang="ary"), value, spoken)

    def test_ary_reads_its_own_four_and_forty(self):
        self.assertEqual(extract_number("ربعة", lang="ary"), 4)
        self.assertEqual(extract_number("ربعين", lang="ary"), 40)
        self.assertEqual(extract_number("تنين", lang="ary"), 2)

    def test_the_quarter_stays_a_quarter_in_standard_arabic(self):
        """ربعين is the oblique dual of ربع "quarter", which the library writes itself."""
        spoken = nice_number(1.5, lang="ar", denominators=[4], case="oblique")
        self.assertEqual(spoken, "1 وربعين")
        for lang in ("ar", "ar-MA", "arz", "apc"):
            self.assertEqual(extract_number("واحد وربعين", lang=lang), 1, lang)
            self.assertIs(extract_number("قطع الكعكة إلى ربعين", lang=lang), False, lang)
            self.assertEqual(numbers_to_digits("1 وربعين", lang=lang), "1 وربعين", lang)
            self.assertEqual(numbers_to_digits("ساعة وربعين", lang=lang), "ساعة وربعين", lang)

    def test_ribaa_of_medium_build_is_no_number_in_standard_arabic(self):
        for text in ("كان رسول الله صلى الله عليه وسلم ربعة من القوم ليس بالطويل ولا بالقصير",
                     "رجل ربعة القامة", "كان ربعة من القوم"):
            for lang in ("ar", "ar-MA", "arz", "apc"):
                self.assertIs(extract_number(text, lang=lang), False, (lang, text))
                self.assertEqual(numbers_to_digits(text, lang=lang), text, (lang, text))


if __name__ == "__main__":
    unittest.main()
