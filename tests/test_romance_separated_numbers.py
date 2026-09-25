"""T-4415: two numbers with a word between them are two numbers.

The shared Romance extractor skipped any word its vocabulary did not know
and kept accumulating, so a filler word between two numbers added them
together: ``dos qzx tercero`` answered 5 rather than 2, in ca, es, fr, gl
and it. That is the census line from
``knowledge/wiki/audits/spec-adoption/t3982-number-parser-ordinals-leftmost.md``.

An unknown word now ends the number, under the same descending test the
joiner branch already uses, with one carve-out: it carries on when the next
word is a number word smaller than what is pending, which is a number still
being read rather than a second one. Romanian needs that carve-out and is
the control below.

Adjacent number words and fractions are not touched: those are the shape a
fraction is written in, and what they mean under ``ordinals=True`` is
architecture's T-4416.
"""
import unittest

from ovos_number_parser import (extract_number_ca, extract_number_es,
                                extract_number_fr, extract_number_gl,
                                extract_number_it)
from ovos_number_parser.numbers_ro import RO

#: lang, extract, the word for 2, the word for 3 as an ordinal
LOCALES = [
    ("ca", extract_number_ca, "dos", "tercer"),
    ("es", extract_number_es, "dos", "tercero"),
    ("fr", extract_number_fr, "deux", "troisième"),
    ("gl", extract_number_gl, "dous", "terceiro"),
    ("it", extract_number_it, "due", "terzo"),
]

#: spells no number in any of these languages, so it only keeps the two
#: numbers apart
FILLER = "qzx"


class TestSeparatedNumbersAreNotAdded(unittest.TestCase):

    def test_the_cardinal_first_answers_the_cardinal(self):
        for lang, extract, card, ordinal in LOCALES:
            with self.subTest(lang=lang):
                line = f"{card} {FILLER} {ordinal}"
                self.assertEqual(extract(line, ordinals=True), 2, line)

    def test_the_ordinal_first_answers_the_ordinal(self):
        for lang, extract, card, ordinal in LOCALES:
            with self.subTest(lang=lang):
                line = f"{ordinal} {FILLER} {card}"
                self.assertEqual(extract(line, ordinals=True), 3, line)

    def test_two_cardinals_are_two_numbers(self):
        """The same defect without an ordinal in it, so the fix cannot be
        read as being about ordinals."""
        for lang, extract, card, _ in LOCALES:
            with self.subTest(lang=lang):
                line = f"{card} {FILLER} {card}"
                self.assertEqual(extract(line), 2, line)

    def test_neither_sum_survives(self):
        """Fail-before control, stated as the value the defect produced.
        Every line above answered 5 (or 4 for the two cardinals) by adding
        the two numbers together."""
        for lang, extract, card, ordinal in LOCALES:
            with self.subTest(lang=lang):
                for line in (f"{card} {FILLER} {ordinal}",
                             f"{ordinal} {FILLER} {card}"):
                    self.assertNotEqual(extract(line, ordinals=True), 5, line)
                self.assertNotEqual(extract(f"{card} {FILLER} {card}"), 4)


class TestWhatTheFixMustNotMove(unittest.TestCase):

    def test_adjacent_number_words_are_untouched(self):
        """The pair with nothing between them keeps the reading it had.
        That shape is how a fraction is written, and T-4416 owns what it
        means under the flag."""
        for lang, extract, card, ordinal in LOCALES:
            with self.subTest(lang=lang):
                self.assertEqual(extract(f"{card} {ordinal}",
                                         ordinals=True), 5)
                self.assertEqual(extract(f"{ordinal} {card}",
                                         ordinals=True), 5)

    def test_the_flag_off_reading_is_untouched(self):
        for lang, extract, card, ordinal in LOCALES:
            with self.subTest(lang=lang):
                self.assertEqual(extract(f"{card} {FILLER} {ordinal}"), 2)

    def test_leading_context_still_reaches_the_number(self):
        """An unknown word BEFORE the first number is context, not a
        separator: the rule only runs once a number has been read."""
        for lang, extract, card, _ in LOCALES:
            with self.subTest(lang=lang):
                self.assertEqual(extract(f"{FILLER} {FILLER} {card}"), 2)

    def test_romanian_keeps_the_words_its_map_does_not_hold(self):
        """The control that shaped the rule. Romanian writes its feminine
        "one" as ``o``, which the number map does not hold, and links a
        scale word with a particle in "cinci sute de mii". Both sit inside
        one number, and both would be cut by a plain stop-on-unknown rule.
        """
        self.assertEqual(
            RO.extract_number("o sută douăzeci și trei"), 123)
        self.assertEqual(
            RO.extract_number("cinci sute de mii"), 500000)
        self.assertEqual(
            RO.extract_number(
                "două milioane cinci sute de mii o sută douăzeci și trei"),
            2500123)

    def test_a_long_composed_number_is_still_one_number(self):
        self.assertEqual(extract_number_es("dos mil quinientos"), 2500)
        self.assertEqual(extract_number_it("due milioni"), 2000000)


if __name__ == "__main__":
    unittest.main()
