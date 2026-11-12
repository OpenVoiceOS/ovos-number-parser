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

from ovos_number_parser import (GrammaticalGender, extract_number,
                                is_fractional, is_ordinal, numbers_to_digits,
                                pronounce_fraction, pronounce_number,
                                pronounce_ordinal)

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


def masculine_ordinal(locale, number):
    return RbnfEngine.for_language(locale).format_number(
        number, ruleset_names=["spellout-ordinal-masculine"]).text


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

    def test_fraction_does_not_borrow_a_module(self):
        for code in COLLIDING:
            if code in RBNF_LOCALES:
                continue
            with self.subTest(code=code):
                with self.assertRaises(NotImplementedError):
                    pronounce_fraction("1/2", code)

    def test_filipino_fraction_is_filipino(self):
        # numerator and ordinal denominator, both from the Filipino rules
        self.assertEqual(
            pronounce_fraction("1/2", "fil"),
            f"{rbnf('fil', 1, FormatPurpose.CARDINAL)} "
            f"{rbnf('fil', 2, FormatPurpose.ORDINAL)}")


class TestMacrolanguageMembers(unittest.TestCase):
    """An individual language inside a macrolanguage, with the same written
    standard, reads like the macrolanguage code (IANA Language Subtag
    Registry, "Macrolanguage" field)."""

    MEMBERS = {"azj": "az", "ekk": "et", "pes": "fa", "zsm": "ms"}

    def test_member_reads_like_macrolanguage(self):
        for member, macro in self.MEMBERS.items():
            for number in NUMBERS + [3.5, -21]:
                with self.subTest(member=member, number=number):
                    self.assertEqual(pronounce_number(number, member),
                                     pronounce_number(number, macro))
                    self.assertEqual(pronounce_ordinal(abs(int(number)) or 1, member),
                                     pronounce_ordinal(abs(int(number)) or 1, macro))
            for number in [7, 21, 1234]:
                spoken = pronounce_number(number, macro)
                with self.subTest(member=member, spoken=spoken):
                    self.assertEqual(extract_number(spoken, member),
                                     extract_number(spoken, macro))
                    self.assertEqual(numbers_to_digits(f"x {spoken} y", member),
                                     numbers_to_digits(f"x {spoken} y", macro))
            with self.subTest(member=member, fraction="3/4"):
                self.assertEqual(pronounce_fraction("3/4", member),
                                 pronounce_fraction("3/4", macro))
                self.assertEqual(is_fractional("x", member),
                                 is_fractional("x", macro))

    def test_member_with_region_subtag(self):
        self.assertEqual(pronounce_number(21, "azj-AZ"), pronounce_number(21, "az"))
        self.assertEqual(pronounce_number(21, "zsm_MY"), pronounce_number(21, "ms"))


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

    def test_serbian_latin_is_the_cyrillic_reading_transliterated(self):
        # Serbian Cyrillic and Latin letters map one to one (Wikipedia,
        # "Serbian Cyrillic alphabet", table of the 30 letters and their Latin
        # counterparts)
        cyrillic = "абвгдђежзијклљмнњопрстћуфхцчџш"
        latin = ["a", "b", "v", "g", "d", "đ", "e", "ž", "z", "i", "j", "k",
                 "l", "lj", "m", "n", "nj", "o", "p", "r", "s", "t", "ć", "u",
                 "f", "h", "c", "č", "dž", "š"]
        to_latin = {ord(c): l for c, l in zip(cyrillic, latin)}
        for gender in GrammaticalGender:
            for number in list(range(1, 1001)) + [2002, 100001]:
                with self.subTest(gender=gender, number=number):
                    self.assertEqual(
                        pronounce_ordinal(number, "sr-Latn", gender=gender),
                        pronounce_ordinal(number, "sr", gender=gender)
                        .translate(to_latin))

    def test_serbian_latin_ordinal_recognised(self):
        # the Cyrillic table is built first, so a table shared between "sr"
        # and "sr-Latn" would miss the Latin form
        self.assertEqual(is_ordinal("двадесет и први", "sr"), 21)
        self.assertEqual(is_ordinal("dvadeset i prvi", "sr-Latn"), 21)

    def test_regional_french_ordinals_recognised_leniently(self):
        # fr-BE and fr-CH speak the regional CLDR ordinals and read both
        # those and the forms of France
        for tag, locale in [("fr-BE", "fr_BE"), ("fr-CH", "fr_CH")]:
            for number in range(1, 101):
                regional = masculine_ordinal(locale, number)
                france = masculine_ordinal("fr", number)
                with self.subTest(tag=tag, number=number):
                    self.assertEqual(pronounce_ordinal(number, tag), regional)
                    self.assertEqual(is_ordinal(regional, tag), number)
                    self.assertEqual(is_ordinal(france, tag), number)
        self.assertEqual(pronounce_ordinal(70, "fr-BE"), "septantième")
        self.assertEqual(is_ordinal("soixante-dixième", "fr-BE"), 70)
        self.assertEqual(is_ordinal("quatre-vingt-dixième", "fr-CH"), 90)

    def test_complex_connectives_ignore_case(self):
        for tag, same in [("RU", "ru"), ("De", "de"), ("ru_RU", "ru")]:
            with self.subTest(tag=tag):
                self.assertEqual(pronounce_number(complex(2, -3), tag),
                                 pronounce_number(complex(2, -3), same))

    def test_hungarian_hyphen_kept_with_region(self):
        # "kétezer-ötszáz" is 2000 + 500; the hyphen marks the thousand
        # boundary and must not turn into a space
        for tag in ["hu", "hu-HU", "hu_HU", "HU"]:
            with self.subTest(tag=tag):
                self.assertEqual(extract_number("kétezer-ötszáz", tag), 2500)

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
