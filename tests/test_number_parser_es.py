# -*- coding: utf-8 -*-
"""
Tests for Spanish number parsing and formatting utilities.

Testing library/framework:
- unittest (standard library), consistent with existing tests in this repository.

Focus:
- Functions defined in ovos_number_parser/numbers_es.py as per the provided diff:
  is_fractional_es, extract_number_es, _es_number_parse, nice_number_es,
  pronounce_number_es, numbers_to_digits_es.

Notes:
- Some behaviors reflect known TODOs/limitations in the implementation
  (e.g., parsing 'cero' in certain paths), and tests document these explicitly.
"""

import unittest

from ovos_number_parser.numbers_es import (
    is_fractional_es,
    extract_number_es,
    nice_number_es,
    pronounce_number_es,
    numbers_to_digits_es,
    _es_number_parse,
)


class TestIsFractionalEs(unittest.TestCase):
    def test_basic_and_plural_forms(self):
        # Basic singulars
        self.assertEqual(is_fractional_es("medio"), 0.5)
        self.assertEqual(is_fractional_es("tercio"), 1 / 3)
        self.assertEqual(is_fractional_es("cuarto"), 0.25)
        self.assertEqual(is_fractional_es("quinta"), 0.2)
        self.assertEqual(is_fractional_es("sexta"), 1 / 6)
        self.assertEqual(is_fractional_es("séptimo"), 1 / 7)
        self.assertEqual(is_fractional_es("octava"), 1 / 8)
        self.assertEqual(is_fractional_es("noveno"), 1 / 9)
        self.assertEqual(is_fractional_es("décimo"), 0.1)
        self.assertEqual(is_fractional_es("onceavo"), 1 / 11)
        self.assertEqual(is_fractional_es("doceava"), 1 / 12)

        # Plural handling via trailing 's' trimming
        self.assertEqual(is_fractional_es("medios"), 0.5)
        self.assertEqual(is_fractional_es("quintos"), 0.2)
        self.assertEqual(is_fractional_es("cuartas"), 0.25)

    def test_extended_ordinals(self):
        self.assertEqual(is_fractional_es("vigésimo"), 1 / 20)
        self.assertEqual(is_fractional_es("trigésimo"), 1 / 30)
        self.assertEqual(is_fractional_es("centésimo"), 1 / 100)
        self.assertEqual(is_fractional_es("milésima"), 1 / 1000)

    def test_unknown_returns_false(self):
        self.assertFalse(is_fractional_es("noesfraccion"))

    def test_case_sensitivity_current_behavior(self):
        # Current implementation uses input_str.lower() for membership but indexes with original key.
        # Uppercase input currently raises KeyError; document this failure mode.
        with self.assertRaises(KeyError):
            is_fractional_es("Medio")


class TestExtractNumberEs(unittest.TestCase):
    def test_integers_and_zero(self):
        self.assertEqual(extract_number_es("dos"), 2)
        self.assertEqual(extract_number_es("123"), 123)

        # Known limitation: zero returns False due to current logic
        self.assertFalse(extract_number_es("cero"))

    def test_simple_fractions_and_plural_words(self):
        self.assertAlmostEqual(extract_number_es("medio"), 0.5)
        self.assertAlmostEqual(extract_number_es("dos quintos"), 2 * (1 / 5))  # 0.4
        self.assertAlmostEqual(extract_number_es("3/4"), 0.75, places=7)
        self.assertAlmostEqual(extract_number_es("2/3"), 2 / 3, places=7)

    def test_decimals_with_words_and_leading_zeros(self):
        self.assertEqual(extract_number_es("tres punto cinco"), 3.5)
        # "tres coma cero cinco" should be interpreted as 3.05
        self.assertEqual(extract_number_es("tres coma cero cinco"), 3.05)

    def test_conjunction_y_for_tens_and_units(self):
        self.assertEqual(extract_number_es("treinta y cuatro"), 34)
        self.assertEqual(extract_number_es("veinte y dos"), 22)


class TestEsNumberParseInternals(unittest.TestCase):
    def test_parse_basic_ranges(self):
        # 34 -> ['treinta', 'y', 'cuatro']
        self.assertEqual(_es_number_parse(["treinta", "y", "cuatro"], 0), (34, 3))

        # 2003 -> ['dos', 'mil', 'tres']
        self.assertEqual(_es_number_parse(["dos", "mil", "tres"], 0), (2003, 3))

        # 999 -> ['novecientos', 'noventa', 'y', 'nueve']
        self.assertEqual(
            _es_number_parse(["novecientos", "noventa", "y", "nueve"], 0), (999, 4)
        )

    def test_cero_known_limitation(self):
        # Document current limitation: 'cero' isn't parsed by _es_number_parse due to truthiness checks
        self.assertIsNone(_es_number_parse(["cero"], 0))


class TestNiceNumberEs(unittest.TestCase):
    def test_speech_format_basic(self):
        self.assertEqual(nice_number_es(4.5, speech=True), "4 y medio")
        self.assertEqual(nice_number_es(0.5, speech=True), "un medio")
        self.assertEqual(nice_number_es(2.75, speech=True), "2 y 3 cuartos")
        # Denominator 3 uses singular form per current implementation
        self.assertEqual(nice_number_es(1 + 1 / 3, speech=True), "1 y 1 tercio")

    def test_text_format_and_thousands_separator(self):
        self.assertEqual(nice_number_es(4.5, speech=False), "4 1/2")
        # Thousands separator should be a non-breaking space and decimal comma for integers
        self.assertEqual(nice_number_es(1234, speech=False), "1 234")


class TestPronounceNumberEs(unittest.TestCase):
    def test_basics_and_sign(self):
        self.assertEqual(pronounce_number_es(5), "cinco")
        self.assertEqual(pronounce_number_es(-3), "menos tres")

    def test_tens_with_uno_variants(self):
        self.assertEqual(pronounce_number_es(21), "veintiuno")
        self.assertEqual(pronounce_number_es(22), "veintidós")
        self.assertEqual(pronounce_number_es(23), "veintitrés")
        self.assertEqual(pronounce_number_es(26), "veintiséis")

    def test_hundreds_and_thousands(self):
        self.assertEqual(pronounce_number_es(100), "cien")
        self.assertEqual(pronounce_number_es(101), "ciento uno")
        self.assertEqual(pronounce_number_es(200), "doscientos")
        self.assertEqual(pronounce_number_es(1000), "mil")
        self.assertEqual(pronounce_number_es(2000), "dos mil")
        self.assertEqual(pronounce_number_es(2100), "dos mil cien")

    def test_millions_and_decimals(self):
        self.assertEqual(pronounce_number_es(1_000_000), "un millón")
        self.assertEqual(pronounce_number_es(5.2), "cinco coma dos")
        # Leading zero in decimal part should be spoken as 'cero'
        self.assertEqual(pronounce_number_es(0.07, places=2), "cero coma cero siete")

    def test_short_scale_flag_still_produces_valid_small_numbers(self):
        # For small numbers, short_scale has no effect; ensure result is as expected.
        self.assertEqual(pronounce_number_es(42, short_scale=True), "cuarenta y dos")


class TestNumbersToDigitsEs(unittest.TestCase):
    def test_basic_replacements(self):
        self.assertEqual(numbers_to_digits_es("uno dos tres"), "1 2 3")
        self.assertEqual(numbers_to_digits_es("dieciséis"), "16")
        self.assertEqual(
            numbers_to_digits_es("tengo dos manzanas y tres peras"),
            "tengo 2 manzanas y 3 peras",
        )

    def test_compound_simple_phrase(self):
        # Above twenty is ambiguous and not fully resolved; function performs per-token replacement.
        self.assertEqual(numbers_to_digits_es("veinte y uno"), "20 y 1")


if __name__ == "__main__":
    unittest.main()