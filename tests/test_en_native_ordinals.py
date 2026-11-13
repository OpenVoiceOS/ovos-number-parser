"""English ordinals from the native engine: pronounce_number(..., ordinals=True).

Expected values come from CLDR RBNF ``en`` spellout-ordinal:

- ``0: zeroth;``
- ``100: ←%spellout-numbering← hundred→%%th→;`` with ``%%th`` giving "th" on
  a round hundred and the ordinal of the rest otherwise, so 200 is "two
  hundredth" and 1100 is "one thousand one hundredth".
- ``1000000: ←%spellout-numbering← million→%%th→;``: the count before a scale
  word stays a cardinal, "one" included.

The native engine keeps its own cardinal layout: a comma between groups,
"and" after "hundred", no hyphen, and the bare word for a round unit alone
("hundredth", "thousandth", "millionth", as test_number_parser_en already
asserts). Inside a longer number the unit keeps its "one", as the cardinal
does: 1100 is "one thousand, one hundred".
"""
import unittest

from ovos_number_parser import pronounce_number
from ovos_number_parser.util import Scale


class TestEnglishNativeOrdinals(unittest.TestCase):
    def assertOrdinals(self, cases, **kwargs):
        for number, expected in cases:
            with self.subTest(number=number, **{k: str(v) for k, v in kwargs.items()}):
                self.assertEqual(
                    pronounce_number(number, "en", ordinals=True, **kwargs),
                    expected)

    def test_zero(self):
        self.assertOrdinals([(0, "zeroth")])

    def test_round_hundreds(self):
        self.assertOrdinals([
            (200, "two hundredth"),
            (500, "five hundredth"),
            (900, "nine hundredth"),
            (1500, "one thousand, five hundredth"),
            (2200, "two thousand, two hundredth"),
        ])

    def test_unit_inside_a_longer_number_keeps_its_count(self):
        self.assertOrdinals([
            (1100, "one thousand, one hundredth"),
            (2100, "two thousand, one hundredth"),
            (1001000, "one million, one thousandth"),
            (10 ** 12 + 10 ** 6, "one trillion, one millionth"),
        ])

    def test_round_unit_alone(self):
        self.assertOrdinals([
            (100, "hundredth"),
            (1000, "thousandth"),
            (10 ** 6, "millionth"),
        ])

    def test_long_scale_marks_only_the_last_group(self):
        self.assertOrdinals([
            (1000500, "one million, five hundredth"),
            (10 ** 6 + 100, "one million, one hundredth"),
            (10 ** 12 + 10 ** 6, "one billion, one millionth"),
        ], scale=Scale.LONG)

    def test_cardinals_stay(self):
        for number, expected in ((0, "zero"), (100, "one hundred"),
                                 (200, "two hundred"),
                                 (1100, "one thousand, one hundred")):
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, "en"), expected)


if __name__ == "__main__":
    unittest.main()
