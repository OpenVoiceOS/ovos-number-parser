"""Hebrew reads a bare number in the feminine (abstract counting) form.

Hebrew number gender is inverted and famously confusing, but the rule for a
number with no noun -- arithmetic, phone numbers, counting aloud -- is settled:
it is the FEMININE form. Academy of the Hebrew Language, "4.3 השימוש בשם המספר":
abstract, unspecified numbers are expressed in the feminine, independent of any
noun's gender. So 3 recited alone is "שלוש", not the masculine "שלושה".

The library defaulted to the masculine citation forms. Both ICU RBNF and
num2words use the feminine, and every value here was cross-checked against ICU.

Parsing stays permissive: both genders are accepted on input, since a masculine
noun context produces the masculine forms.

"אפס" (zero) is genderless and spoken for a zero whole part ("אפס נקודה חמש")
and for a zero decimal digit ("חמש נקודה אפס חמש").
"""
import unittest

from ovos_number_parser import pronounce_number, extract_number


class TestFeminineIsDefault(unittest.TestCase):
    CASES = [
        (1, "אחת"), (2, "שתיים"), (3, "שלוש"), (5, "חמש"), (10, "עשר"),
        (11, "אחת עשרה"), (13, "שלוש עשרה"), (21, "עשרים ואחת"),
        (123, "מאה עשרים ושלוש"),
    ]

    def test_bare_number_is_feminine(self):
        for value, expected in self.CASES:
            with self.subTest(value=value):
                self.assertEqual(pronounce_number(value, "he"), expected)

    def test_not_masculine(self):
        # the masculine forms must no longer be produced
        for value, masc in [(1, "אחד"), (3, "שלושה"), (10, "עשרה")]:
            with self.subTest(value=value):
                self.assertNotEqual(pronounce_number(value, "he"), masc)


class TestZeroIsGenderless(unittest.TestCase):
    def test_zero_whole_part(self):
        self.assertEqual(pronounce_number(0, "he"), "אפס")
        self.assertEqual(pronounce_number(0.5, "he"), "אפס נקודה חמש")

    def test_zero_decimal_digit(self):
        self.assertEqual(pronounce_number(5.05, "he"), "חמש נקודה אפס חמש")


class TestParsingPermissive(unittest.TestCase):
    def test_both_genders_accepted(self):
        for spelled, value in [("שלוש", 3), ("שלושה", 3),
                              ("אחת", 1), ("אחד", 1),
                              ("שתיים", 2), ("שניים", 2)]:
            with self.subTest(spelled=spelled):
                self.assertEqual(extract_number(spelled, "he"), value)


class TestRoundTrip(unittest.TestCase):
    def test_round_trip(self):
        for value in list(range(0, 101)) + [
                123, 200, 999, 1000, 2023, 0.5, 3.5, 5.05]:
            with self.subTest(value=value):
                spoken = pronounce_number(value, "he")
                self.assertEqual(extract_number(spoken, "he"), value)
