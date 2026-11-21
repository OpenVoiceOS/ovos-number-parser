"""The public readers of a language in NUMTAG_LANGS read through numtag.

The routed set is patched in each test, so the tests hold whatever set the
package ships. Each expected value is hand arithmetic on the sentence.
"""
import sys
import unittest
from unittest.mock import patch

from ovos_number_parser import (NumberSpan, extract_number, extract_number_spans,
                                numbers_to_digits, numtag_readers)


def routed(*langs):
    return patch.object(numtag_readers, "NUMTAG_LANGS", frozenset(langs))


class TestRouting(unittest.TestCase):

    def test_a_routed_language_reads_through_numtag(self):
        # the joiner rule (Gulbenkian pp. 932-933): with no "e" before the
        # round last group, "mil duzentas dúzias" is 1000 and 200 x 12
        text = "Compraram mil duzentas dúzias de ovos."
        with routed("pt"):
            self.assertEqual(extract_number_spans(text, "pt-PT"),
                             [NumberSpan(10, 13, "mil", 1000),
                              NumberSpan(14, 29, "duzentas dúzias", 2400)])
            self.assertEqual(extract_number(text, "pt-PT"), 1000)
            self.assertEqual(numbers_to_digits(text, "pt-PT"),
                             "Compraram 1000 2400 de ovos.")

    def test_an_unrouted_language_keeps_its_reader(self):
        self.assertFalse(numtag_readers.routed("ms"))
        self.assertEqual(extract_number("dua puluh satu", "ms"), 21)

    def test_region_and_alias_tags_follow_the_language(self):
        with routed("pt", "nb"):
            for lang in ("pt", "pt-PT", "pt_BR", "PT-br", "nb", "no", "no-NO"):
                with self.subTest(lang=lang):
                    self.assertTrue(numtag_readers.routed(lang))
            self.assertFalse(numtag_readers.routed("nn"))


class TestValues(unittest.TestCase):
    """numtag values are digit strings; the API returns int, float or False."""

    def test_types(self):
        with routed("en"):
            self.assertIs(type(extract_number("two hundred and five", "en")), int)
            self.assertEqual(extract_number("two point five", "en"), 2.5)
            self.assertEqual(extract_number("one third", "en"), 1 / 3)
            self.assertIs(extract_number("no number here", "en"), False)
            self.assertIs(extract_number(None, "en"), False)

    def test_a_float_that_drops_the_point_rounds_half_up(self):
        # 12000000000000000345.5 has no float with the .5, so the value is
        # the whole number rounded half up, as the parser returns it
        self.assertEqual(numtag_readers.number("12000000000000000345.5"),
                         12000000000000000346)
        self.assertEqual(numtag_readers.number("-12000000000000000345.25"),
                         -12000000000000000345)

    def test_a_value_past_float_range_rounds_half_up_and_never_raises(self):
        # 400 nines and one half is 10**400 - 1/2, which rounds half up to 10**400
        nines = "9" * 400
        self.assertEqual(numtag_readers.number(nines + ".5"), 10 ** 400)
        self.assertEqual(numtag_readers.number("-" + nines + ".5"), -(10 ** 400))
        with routed("es"):
            self.assertEqual(extract_number(nines + " y medio", "es"), 10 ** 400)
            self.assertEqual(extract_number(nines + ".5", "es"), 10 ** 400)
            self.assertEqual(len(numbers_to_digits(nines + " y medio", "es")), 401)

    def test_a_digit_run_str_cannot_write_is_no_number_and_never_raises(self):
        for text in ("0." + "9" * 5000, "0," + "9" * 5000, "1/" + "9" * 5000):
            for lang in ("en", "pt"):
                with self.subTest(text=text[:3], lang=lang):
                    self.assertIs(extract_number(text, lang), False)
                    self.assertIs(extract_number(text, lang, ordinals=True), False)
                    self.assertEqual(extract_number_spans(text, lang), [])
                    self.assertEqual(numbers_to_digits(text, lang), text)

    def test_a_value_str_cannot_write_is_no_number(self):
        digits = "9" * (sys.get_int_max_str_digits() + 1)
        self.assertIsNone(numtag_readers.number(digits))

    def test_digits_of_other_scripts_and_underscores_keep_their_offsets(self):
        text = "twenty_one and ٣"
        with routed("en"):
            spans = extract_number_spans(text, "en")
        self.assertEqual([(s.surface, s.value) for s in spans],
                         [("twenty_one", 21), ("٣", 3)])
        for span in spans:
            self.assertEqual(text[span.start:span.end], span.surface)


class TestNumbersToDigits(unittest.TestCase):

    def test_digits_and_ordinals_stay_as_written(self):
        with routed("en"):
            self.assertEqual(numbers_to_digits("Version 2.0 is the third of five", "en"),
                             "Version 2.0 is the third of 5")

    def test_ordinals_become_digits_when_asked(self):
        text = "the twenty-first of march"
        self.assertEqual(numtag_readers.numbers_to_digits(text, "en", ordinals=True),
                         "the 21 of march")
        self.assertEqual(numtag_readers.numbers_to_digits(text, "en"), text)

    def test_portuguese_keeps_the_words_of_a_fraction(self):
        with routed("pt"):
            self.assertEqual(numbers_to_digits("dois e meio", "pt"), "2 e meio")
            self.assertEqual(numbers_to_digits("doze vinte e cinco avos", "pt"),
                             "12 25 avos")
            self.assertEqual(numbers_to_digits("dois milhões e meio de euros", "pt"),
                             "2500000 de euros")

    def test_other_languages_write_a_fraction_as_its_decimal(self):
        with routed("en"):
            self.assertEqual(numbers_to_digits("one third of the cake", "en"),
                             f"{1 / 3} of the cake")


if __name__ == "__main__":
    unittest.main()
