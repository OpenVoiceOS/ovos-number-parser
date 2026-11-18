"""German ordinals take the ending of the last word, not of the whole number.

The writer tested the whole number for the irregular and -te endings, so every
number above 100 whose last two digits are 01 to 19 got "-ste" on the
cardinal: "einhunderteinsste", "einhundertsiebenste", "eine Million dreiste".

Sources for the expected values:

- ICU 78.3 (CLDR rbnf de.xml, %spellout-ordinal), a second engine. The rows
  below are its output with the spaces, hyphens and soft hyphens of the
  repo's spelling. A sweep of 1 to 100 000 gave 20 078 mismatches on the old
  writer and none on this one.
- de.wiktionary "einhunderterste" ("in einer Reihenfolge an Stelle
  hunderteins", 101.), "hundertste" (100.) and "siebte" (7.): the ordinals
  1 to 19 end in -te with "erste", "dritte", "siebte" and "achte" irregular,
  and from 20 the ending is -ste.
"""
import unittest

from ovos_number_parser import pronounce_ordinal

ROWS = [
    (1, "erste"), (3, "dritte"), (7, "siebte"), (8, "achte"), (12, "zwölfte"),
    (19, "neunzehnte"), (20, "zwanzigste"), (21, "einundzwanzigste"),
    (100, "einhundertste"),
    (101, "einhunderterste"), (102, "einhundertzweite"),
    (103, "einhundertdritte"), (107, "einhundertsiebte"),
    (108, "einhundertachte"), (111, "einhundertelfte"),
    (112, "einhundertzwölfte"), (119, "einhundertneunzehnte"),
    (120, "einhundertzwanzigste"), (121, "einhunderteinundzwanzigste"),
    (1001, "eintausenderste"), (1003, "eintausenddritte"),
    (1007, "eintausendsiebte"), (1011, "eintausendelfte"),
    (2019, "zweitausendneunzehnte"), (20001, "zwanzigtausenderste"),
    (100001, "einhunderttausenderste"),
    (1000001, "eine Million erste"), (1000003, "eine Million dritte"),
    (1000019, "eine Million neunzehnte"), (2000011, "zwei Millionen elfte"),
    (1000000, "eine Millionste"), (1000000007, "eine Milliarde siebte"),
]


class TestGermanOrdinalLastTwoDigits(unittest.TestCase):
    def test_rows(self):
        for number, expected in ROWS:
            with self.subTest(number=number):
                self.assertEqual(pronounce_ordinal(number, "de"), expected)

    def test_last_two_digits_one_to_nineteen_never_end_in_ste_after_a_unit(self):
        for hundreds in (100, 1000, 20000, 1000000):
            for last in range(1, 20):
                with self.subTest(number=hundreds + last):
                    spoken = pronounce_ordinal(hundreds + last, "de")
                    self.assertTrue(spoken.endswith(
                        pronounce_ordinal(last, "de")), spoken)


if __name__ == "__main__":
    unittest.main()
