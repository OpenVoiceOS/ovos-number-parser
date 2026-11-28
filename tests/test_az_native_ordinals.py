"""Azerbaijani ordinals: the native engine, and pronounce_ordinal through it.

Expected values:

- The suffix: en.wiktionary "-inci" (Azerbaijani), "Suffix creating ordinal
  numbers", with the forms -ıncı / -inci / -uncu / -üncü after a consonant
  and -ncı / -nci / -ncu / -ncü after a vowel; "-ıncı" is the form "after the
  vowels A / I". Only the last word of a compound numeral takes it.
- en.wiktionary "yetmişinci" ("Morphologically yetmiş + -inci", "seventieth",
  next to "altmış doqquzuncu" and "yetmiş birinci"), "doxsanıncı" ("doxsan +
  -ıncı", "ninetieth", next to "səksən doqquzuncu" and "doxsan birinci") and
  "yüzüncü" ("yüz + -üncü", "hundredth", next to "doxsan doqquzuncu" and
  "yüz birinci"). The "yüzüncü" entry cites, under "Further reading",
  Orucov (ed.), *Azərbaycan dilinin izahlı lüğəti*, 2nd ed., Baku:
  Şərq-Qərb, 2006, vol. 4, p. 636. That locator is en.wiktionary's; the
  scan was not read.
- CLDR RBNF ``az`` spellout-ordinal: ``0: sıfırıncı;`` and
  ``100: ←%spellout-numbering← yüz→%%uncu2→;`` with ``%%uncu2`` giving
  "üncü" on a round hundred, so 200 is "iki yüzüncü".
- The last word takes the suffix and the words before it stay cardinal, so a
  scale word keeps its count when other words come before it: 1100 is "min,
  yüzüncü" ("min, yüz" as a cardinal) and 10^12 + 10^6 is "bir trilyon, bir
  milyonuncu" ("bir trilyon, bir milyon"). On the long scale the same
  number is "bir milyard, bir milyonuncu" ("bir milyard, bir milyon").
- Open: a bare round scale word drops its count ("milyonuncu" for 10^6,
  "trilyonuncu" for 10^12), as dev's tests/test_number_parser_az.py
  expects. No source here rules on "bir milyonuncu" against "milyonuncu".
- From 10^24 up the engine has no ordinal scale word and falls back to a
  scientific cardinal, so pronounce_ordinal raises NotImplementedError
  there, as it did before the route.
"""
import unittest

from ovos_number_parser import pronounce_number, pronounce_ordinal
from ovos_number_parser.util import Scale


class TestAzerbaijaniOrdinals(unittest.TestCase):
    CASES = [
        (0, "sıfırıncı"),
        (69, "altmış doqquzuncu"),
        (70, "yetmişinci"),
        (71, "yetmiş birinci"),
        (89, "səksən doqquzuncu"),
        (90, "doxsanıncı"),
        (91, "doxsan birinci"),
        (99, "doxsan doqquzuncu"),
        (100, "yüzüncü"),
        (101, "yüz birinci"),
        (200, "iki yüzüncü"),
        (500, "beş yüzüncü"),
        (900, "doqquz yüzüncü"),
        (1100, "min, yüzüncü"),
        (1500, "min, beş yüzüncü"),
        (2000, "iki mininci"),
        (10 ** 12 + 10 ** 6, "bir trilyon, bir milyonuncu"),
    ]

    def test_native_ordinal(self):
        for number, expected in self.CASES:
            with self.subTest(number=number):
                self.assertEqual(
                    pronounce_number(number, "az", ordinals=True), expected)

    def test_pronounce_ordinal(self):
        for number, expected in self.CASES:
            with self.subTest(number=number):
                self.assertEqual(pronounce_ordinal(number, "az"), expected)

    def test_long_scale_marks_only_the_last_group(self):
        # 1000500: "bir milyon, beş yüz" as a cardinal
        self.assertEqual(
            pronounce_number(1000500, "az", ordinals=True, scale=Scale.LONG),
            "bir milyon, beş yüzüncü")

    def test_long_scale_keeps_the_count_before_the_last_group(self):
        # 10^12 + 10^6 on the long scale ends in "bir milyon" plus the
        # suffix. Only the ending is asserted: the engine's long-scale
        # table names 10^12 "milyard", which ADIL gives as 10^9.
        for call in (
                lambda: pronounce_number(10 ** 12 + 10 ** 6, "az",
                                         ordinals=True, scale=Scale.LONG),
                lambda: pronounce_ordinal(10 ** 12 + 10 ** 6, "az",
                                          scale=Scale.LONG)):
            self.assertTrue(call().endswith(", bir milyonuncu"), call())

    def test_no_ordinal_from_ten_to_the_24(self):
        for number in (10 ** 24, 10 ** 30, -10 ** 24):
            for scale in (Scale.SHORT, Scale.LONG):
                with self.subTest(number=number, scale=scale):
                    with self.assertRaises(NotImplementedError):
                        pronounce_ordinal(number, "az", scale=scale)

    def test_cardinals_stay(self):
        for number, expected in ((0, "sıfır"), (70, "yetmiş"),
                                 (90, "doxsan"), (200, "iki yüz")):
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, "az"), expected)


if __name__ == "__main__":
    unittest.main()
