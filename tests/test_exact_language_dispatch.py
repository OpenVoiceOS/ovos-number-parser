"""Language dispatch matches the primary language subtag exactly.

A code that only begins with the letters of a supported language names a
different language: "fil" is Filipino, not Finnish, and "rue" is Rusyn, not
Russian. Such a code is read by unicode_rbnf when it ships rules for the
language, and is otherwise unsupported. The codes below come from the IANA
Language Subtag Registry, one or more for each supported language they used to
reach.

Separator and letter case do not change the language: "pt_BR", "PT-br" and
"pt-BR" read alike (RFC 5646, section 2.1.1: subtags are case-insensitive), and
so do "sr-Latn" and "sr_Latn".
"""
import unittest

from unicode_rbnf import FormatPurpose, RbnfEngine

from ovos_number_parser import (extract_number, is_fractional, is_ordinal,
                                numbers_to_digits, pronounce_fraction,
                                pronounce_number, pronounce_ordinal)

#: registry code -> the supported language whose module used to read it
COLLIDING = {
    "ang": "an", "azb": "az", "bgc": "bg", "cak": "ca", "csb": "cs",
    "dar": "da", "del": "de", "elx": "el", "enm": "en", "ess": "es",
    "ett": "et", "euq": "eu", "fan": "fa", "fil": "fi", "fit": "fi",
    "frr": "fr", "glk": "gl", "hei": "he", "hrx": "hr", "hup": "hu",
    "idu": "id", "itl": "it", "msb": "ms", "nbe": "nb", "nla": "nl",
    "nnh": "nn", "nog": "no", "non": "no", "oca": "oc", "plt": "pl",
    "pta": "pt", "rom": "ro", "rue": "ru", "skr": "sk", "sli": "sl",
    "sva": "sv", "trv": "tr", "uka": "uk",
}

RBNF_LOCALES = set(RbnfEngine.get_supported_languages())
NUMBERS = [0, 1, 2, 7, 21, 99, 100, 1234, 10 ** 6]


def rbnf(locale, number, purpose):
    return RbnfEngine.for_language(locale).format_number(number, purpose).text


class TestCollidingCodes(unittest.TestCase):
    def test_cardinal_is_rbnf_or_unsupported(self):
        for code in COLLIDING:
            for number in NUMBERS:
                with self.subTest(code=code, number=number):
                    if code in RBNF_LOCALES:
                        self.assertEqual(
                            pronounce_number(number, code),
                            rbnf(code, number, FormatPurpose.CARDINAL))
                    else:
                        with self.assertRaises(NotImplementedError):
                            pronounce_number(number, code)

    def test_ordinal_is_rbnf_or_unsupported(self):
        for code in COLLIDING:
            for number in NUMBERS[1:]:
                with self.subTest(code=code, number=number):
                    if code in RBNF_LOCALES:
                        self.assertEqual(
                            pronounce_ordinal(number, code),
                            rbnf(code, number, FormatPurpose.ORDINAL))
                    else:
                        with self.assertRaises(NotImplementedError):
                            pronounce_ordinal(number, code)

    def test_extractors_do_not_borrow_a_module(self):
        for code in COLLIDING:
            with self.subTest(code=code):
                with self.assertRaises(NotImplementedError):
                    extract_number("21", code)
                with self.assertRaises(NotImplementedError):
                    is_fractional("1/2", code)

    def test_words_of_the_other_language_are_not_read(self):
        for code, other in COLLIDING.items():
            with self.subTest(code=code, other=other):
                spoken = pronounce_number(21, other)
                self.assertEqual(numbers_to_digits(f"x {spoken} y", code),
                                 f"x {spoken} y")
                self.assertFalse(is_ordinal(pronounce_ordinal(3, other), code))

    def test_filipino_fraction_is_filipino(self):
        # numerator and ordinal denominator, both from the Filipino rules
        self.assertEqual(
            pronounce_fraction("1/2", "fil"),
            f"{rbnf('fil', 1, FormatPurpose.CARDINAL)} "
            f"{rbnf('fil', 2, FormatPurpose.ORDINAL)}")


class TestTagSpelling(unittest.TestCase):
    #: tag -> the tag it must read exactly like
    SAME = {
        "pt_BR": "pt-BR", "PT-br": "pt-BR", "pt_PT": "pt-PT", "PT": "pt",
        "de_DE": "de-DE", "De": "de", "es_ES": "es-ES", "fr_FR": "fr-FR",
        "en_US": "en-US", "EN": "en", "no_NO": "no-NO", "ar_SA": "ar-SA",
        "arz_EG": "arz-EG", "sr-Latn": "sr_Latn", "sr_latn": "sr_Latn",
        "zh-Hant": "zh_Hant", "yue-Hans": "yue_Hans",
    }
    VALUES = NUMBERS + [10 ** 9, 10 ** 12, 3.5, -2.75, float("-inf")]

    def test_pronounce_number_agrees(self):
        for tag, same in self.SAME.items():
            for number in self.VALUES:
                with self.subTest(tag=tag, number=number):
                    self.assertEqual(pronounce_number(number, tag),
                                     pronounce_number(number, same))

    def test_pronounce_ordinal_agrees(self):
        for tag, same in self.SAME.items():
            for number in [1, 2, 3, 21, 70, 1000, 10 ** 9]:
                with self.subTest(tag=tag, number=number):
                    self.assertEqual(pronounce_ordinal(number, tag),
                                     pronounce_ordinal(number, same))

    def test_extract_number_agrees(self):
        for tag, same in self.SAME.items():
            if same.split("_")[0] in {"sr", "zh", "yue"}:
                continue  # no extractor for these languages
            for number in [7, 21, 1234, 10 ** 9]:
                spoken = pronounce_number(number, same)
                with self.subTest(tag=tag, spoken=spoken):
                    self.assertEqual(extract_number(spoken, tag),
                                     extract_number(spoken, same))

    def test_script_subtag_selects_its_rules(self):
        for tag, locale in [("sr-Latn", "sr_Latn"), ("zh-Hant", "zh_Hant"),
                            ("yue-Hans", "yue_Hans")]:
            for number in NUMBERS:
                with self.subTest(tag=tag, number=number):
                    self.assertEqual(
                        pronounce_number(number, tag),
                        rbnf(locale, number, FormatPurpose.CARDINAL))

    def test_region_branches_kept(self):
        # Brazilian Portuguese is short scale, European Portuguese long scale
        self.assertNotEqual(pronounce_number(10 ** 9, "pt-BR"),
                            pronounce_number(10 ** 9, "pt-PT"))
        self.assertEqual(pronounce_number(10 ** 9, "pt_BR"),
                         pronounce_number(10 ** 9, "pt-BR"))
        # "no" is read by the Bokmål module, "nn" by the Nynorsk one
        self.assertEqual(pronounce_number(21, "no"), pronounce_number(21, "nb"))
        self.assertEqual(pronounce_ordinal(3, "no"), pronounce_ordinal(3, "nb"))


if __name__ == "__main__":
    unittest.main()
