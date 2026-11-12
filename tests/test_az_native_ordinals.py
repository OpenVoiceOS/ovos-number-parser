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
  "yüz birinci"; Azərbaycan dilinin izahlı lüğəti, p. 636).
- CLDR RBNF ``az`` spellout-ordinal: ``0: sıfırıncı;`` and
  ``100: ←%spellout-numbering← yüz→%%uncu2→;`` with ``%%uncu2`` giving
  "üncü" on a round hundred, so 200 is "iki yüzüncü".
- The last word takes the suffix and the words before it stay cardinal, so a
  scale word keeps its count when other words come before it: 1100 is "min,
  yüzüncü" ("min, yüz" as a cardinal) and 10^12 + 10^6 is "bir trilyon, bir
  milyonuncu" ("bir trilyon, bir milyon").
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

    def test_cardinals_stay(self):
        for number, expected in ((0, "sıfır"), (70, "yetmiş"),
                                 (90, "doxsan"), (200, "iki yüz")):
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, "az"), expected)


if __name__ == "__main__":
    unittest.main()
