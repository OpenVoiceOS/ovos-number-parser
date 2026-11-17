"""Levantine Arabic (ISO 639-3 apc) cardinals.

Every expected string is a cell of a published table, copied from its raw wikitext:

- W: English Wikipedia "Levantine Arabic grammar", Numerals, revision 1368977674.
  Its table cites Elihai 2011 pp. 57-59, 107-108 and Brustad & Zuniga 2019 pp. 414-415.
- B: English Wikibooks "Levantine Arabic/Numbers", revision 4672979.
"""
import unittest

from ovos_number_parser import extract_number, numbers_to_digits, pronounce_number, resolve_ar_lect

# number -> the Arabic cell, with the table it comes from
WIKIPEDIA_CELLS = {
    0: "صفر",              # W "صفر ṣifr"
    1: "واحد",             # W "واحد wāḥad"
    2: "تنين",             # W "تنين tnēn"
    3: "تلاتة",            # W "تلاتة talāte (South) / tlēte (North)"
    4: "أربعة",            # W "أربعة ʾarbaʕa"
    5: "خمسة",             # W "خمسة ḵamse"
    6: "ستة",              # W "ستة sitte"
    7: "سبعة",             # W "سبعة sabʕa"
    8: "تمانية",           # W "تمانية tamānye (South)"
    10: "عشرة",            # W "عشرة ʕašara"
    11: "حدعش",            # B "حدعش ḥdaʕš"; W has the spelling احدعش
    12: "تنعش",            # W "تنعش tnaʕš"
    20: "عشرين",           # W "عشرين ʕišrīn"
    21: "واحد وعشرين",     # W "واحد وعشرين wāhad w-ʕišrīn"
    30: "تلاتين",          # W "تلاتين talatīn (South) / tlētīn (North)"
    100: "مية",            # W "مية miyye"
    101: "مية وواحد",      # W "مية وواحد miyye u-wāḥad"
    102: "مية وتنين",      # W "مية وتنين miyye u-tnēn"
    103: "مية وتلاتة",     # W "مية وتلاتة miyye u-talāte"
    200: "ميتين",          # W "ميتين mītēn"
    300: "تلتمية",         # W "تلتمية t(a)lat-miyye"
    1000: "ألف",           # W "ألف ʾalf"
    2000: "ألفين",         # W "ألفين ʾalfēn"
    3000: "تلتة آلاف",     # W "تلتة آلاف t(a)latt‿ālāf"
    10000: "عشرة آلاف",    # W "عشرة آلاف ʕašert‿ālāf"
    100000: "مية ألف",     # W "مية ألف mīt ʾalf"
}

WIKIBOOKS_CELLS = {
    9: "تسعة",             # B "تسعة tisʕa"
    13: "تلتعش",           # B "تلتّعش t(a)lattaʕš"
    14: "أربعتعش",         # B romanisation "'arbaʕtaʕš"
    15: "خمستعش",          # B "خمستعش ḫamᵉstaʕš"
    16: "ستعش",            # B "ستّعش sittaʕš"
    17: "سبعتعش",          # B "سبعتعش sabᵉʕtaʕš"
    18: "تمنتعش",          # B "تمنتعش t(a)mantaʕš"
    19: "تسعتعش",          # B "تسعتعش tisᵉʕtaʕš"
    40: "أربعين",          # B "أربعين 'arbaʕīn"
    50: "خمسين",           # B "خمسين ḫamsīn"
    60: "ستين",            # B "ستّين sittīn"
    70: "سبعين",           # B "سبعين sabʕīn"
    80: "تمانين",          # B "تمانين t(a)mānīn"
    90: "تسعين",           # B "تسعين tisʕīn"
    # 400-900: "attributive form + ميّة", the attributive forms being
    # أربع, خمس, ست, سبع, تمن, تسع in the Wikipedia column "Followed by noun"
    400: "أربعمية",        # B "أربع ميّة 'arbaʕ-miyye", joined as W joins 300
    500: "خمسمية",
    600: "ستمية",
    700: "سبعمية",
    800: "تمنمية",
    900: "تسعمية",
    # B: "the numbers 11,000-999,000 are created with attributive form of the
    # number followed by ألف", the attributive forms being listed in the table
    11000: "حدعشر ألف",    # B "حدعشر ḥdaʕšar"
    12000: "تنعشر ألف",    # B "تنعشر tnaʕšar"
    13000: "تلتعشر ألف",   # B "تلتّعشر t(a)lattaʕšar"
    14000: "أربعتعشر ألف",  # B "'arbaʕtaʕšar"
    15000: "خمستعشر ألف",  # B "خمستعشر ḫamᵉstaʕšar"
    16000: "ستعشر ألف",    # B "ستّعشر sittaʕšar"
    17000: "سبعتعشر ألف",  # B "سبعتعشر sabᵉʕtaʕšar"
    18000: "تمنتعشر ألف",  # B "تمنتعشر t(a)mantaʕšar"
    19000: "تسعتعشر ألف",  # B "تسعتعشر tisᵉʕtaʕšar"
}


class TestLevantineCardinals(unittest.TestCase):
    def test_wikipedia_table_cells(self):
        for number, cell in WIKIPEDIA_CELLS.items():
            self.assertEqual(pronounce_number(number, lang="apc"), cell, number)

    def test_wikibooks_table_cells(self):
        for number, cell in WIKIBOOKS_CELLS.items():
            self.assertEqual(pronounce_number(number, lang="apc"), cell, number)

    def test_joiner_before_units_and_inside_larger_numbers(self):
        """W 21 "واحد وعشرين" and 101-103 "مية و" + unit: the conjunction is و."""
        self.assertEqual(pronounce_number(22, lang="apc"), "تنين وعشرين")
        self.assertEqual(pronounce_number(33, lang="apc"), "تلاتة وتلاتين")
        self.assertEqual(pronounce_number(350, lang="apc"), "تلتمية وخمسين")
        self.assertEqual(pronounce_number(1002, lang="apc"), "ألف وتنين")
        self.assertEqual(pronounce_number(3500, lang="apc"), "تلتة آلاف وخمسمية")
        self.assertEqual(pronounce_number(13500, lang="apc"), "تلتعشر ألف وخمسمية")

    def test_a_number_no_source_gives_keeps_the_literary_word(self):
        self.assertEqual(pronounce_number(1000000, lang="apc"), "مليون")

    def test_apc_resolves_and_a_region_subtag_does_not_pick_the_lect(self):
        self.assertEqual(resolve_ar_lect("apc"), "apc")
        self.assertEqual(resolve_ar_lect("APC-LB"), "apc")
        for code in ("ar", "ar-EG", "ar-LB", "ar-SY"):
            self.assertIsNone(resolve_ar_lect(code), code)
            self.assertEqual(pronounce_number(13, lang=code), "ثلاثة عشر")

    def test_other_lects_do_not_change(self):
        self.assertEqual(pronounce_number(13, lang="arz"), "تلتاشر")
        self.assertEqual(pronounce_number(13, lang="ar"), "ثلاثة عشر")
        self.assertEqual(pronounce_number(13, lang="acm"), "ثلاثة عشر")

    def test_a_composed_number_reads_back(self):
        for value in (13, 22, 33, 350, 3500, 13500, 2018):
            spoken = pronounce_number(value, lang="apc")
            self.assertEqual(extract_number(spoken, lang="ar"), value, spoken)

    def test_tnen_is_two_only_in_context(self):
        """تنين is also "dragon" (English Wiktionary, تنين, Arabic, Etymology 1)."""
        self.assertEqual(extract_number("عندي تنين ريال", lang="ar"), 2)
        self.assertEqual(numbers_to_digits("عندي تنين ريال", lang="ar"), "عندي 2 ريال")
        self.assertEqual(numbers_to_digits("رأيت تنين في الفيلم", lang="ar"), "رأيت تنين في الفيلم")

    def test_feminine_keeps_the_literary_words_below_twenty(self):
        self.assertEqual(pronounce_number(3, lang="apc", gender="feminine"), "ثلاث")
        self.assertEqual(pronounce_number(100, lang="apc", gender="feminine"), "مية")


if __name__ == "__main__":
    unittest.main()
