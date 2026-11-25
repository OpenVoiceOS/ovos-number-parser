"""A language tag reads the language and region that linguatag says it names,
whatever its spelling."""
import unittest

import ovos_number_parser
from ovos_number_parser import (extract_number, numtag_readers, pronounce_fraction,
                                pronounce_number, pronounce_ordinal)

# ISO 639-2 and deprecated codes, and the two-letter code each stands for
OTHER_CODES = [("deu", "de"), ("eng", "en"), ("fra", "fr"), ("por", "pt"),
               ("spa", "es"), ("iw", "he"), ("in", "id"), ("nob", "nb"),
               ("nno", "nn")]


class TestOtherCodesOfALanguage(unittest.TestCase):
    def test_a_three_letter_or_deprecated_code_speaks_its_language(self):
        for code, language in OTHER_CODES:
            with self.subTest(code=code):
                self.assertEqual(pronounce_number(21, code),
                                 pronounce_number(21, language))
                self.assertEqual(pronounce_ordinal(3, code),
                                 pronounce_ordinal(3, language))

    def test_a_three_letter_code_reads_its_language(self):
        self.assertEqual(pronounce_number(21, "deu"), "einundzwanzig")
        self.assertEqual(extract_number("einundzwanzig", "deu"), 21)
        self.assertEqual(extract_number("vingt et un", "fra"), 21)


class TestArabicSpellings(unittest.TestCase):
    def test_an_extlang_tag_is_its_lect(self):
        for number in (2, 13, 2000000000):
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, "ar-arz-EG"),
                                 pronounce_number(number, "arz"))

    def test_the_retired_ajp_code_is_apc(self):
        self.assertEqual(pronounce_number(13, "ajp"), pronounce_number(13, "apc"))


class TestPortugueseRegion(unittest.TestCase):
    def test_a_private_use_word_is_no_region(self):
        self.assertEqual(pronounce_number(2 * 10 ** 9, "pt-x-brazil"),
                         pronounce_number(2 * 10 ** 9, "pt-PT"))
        self.assertEqual(pronounce_number(2 * 10 ** 9, "pt-BR"), "dois bilhões")

    def test_a_script_before_the_region_still_names_brazil(self):
        self.assertEqual(pronounce_number(2 * 10 ** 9, "pt-Latn-BR"),
                         pronounce_number(2 * 10 ** 9, "pt-BR"))


class TestChineseScript(unittest.TestCase):
    def test_taiwan_reads_traditional_characters(self):
        self.assertEqual(pronounce_number(2 * 10 ** 9, "zh-TW"),
                         pronounce_number(2 * 10 ** 9, "zh-Hant"))


class TestWhiteSpace(unittest.TestCase):
    def test_a_padded_tag_reads_as_the_tag(self):
        self.assertEqual(pronounce_number(2 * 10 ** 9, "pt-BR "), "dois bilhões")
        self.assertEqual(pronounce_number(2 * 10 ** 9, " pt-PT"),
                         pronounce_number(2 * 10 ** 9, "pt-PT"))
        self.assertEqual(pronounce_number(21, " de "), "einundzwanzig")
        self.assertEqual(extract_number("einundzwanzig", " de "), 21)
        self.assertEqual(pronounce_number(13, " arz "), pronounce_number(13, "arz"))


class TestArabicVarietiesRoute(unittest.TestCase):
    def test_every_arabic_variety_that_speaks_also_reads(self):
        for code in ("acy", "pga", "mey", "ar-Latn-x-buckwalt"):
            with self.subTest(code=code):
                self.assertTrue(numtag_readers.routed(code))
                self.assertEqual(extract_number(pronounce_number(13, code), code), 13)


class TestNorwegian(unittest.TestCase):
    def test_no_is_resolved_to_bokmal(self):
        self.assertEqual(ovos_number_parser._base_lang("no"), "nb")
        self.assertEqual(pronounce_number(21, "no"), pronounce_number(21, "nb"))

    def test_no_reads_one_half_as_bokmal_halv(self):
        # Bokmålsordboka, "halv", article 22016: "som utgjør den ene av to
        # (mer eller mindre) like store deler"; the example is "to og en halv"
        self.assertEqual(pronounce_fraction("1/2", "no"), "en halv")
        self.assertEqual(pronounce_fraction("1/2", "nb"), "en halv")


if __name__ == "__main__":
    unittest.main()
