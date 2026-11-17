"""The languages in the shipped NUMTAG_LANGS read through numtag.

Each case is a sentence on which the legacy reader of the language gives a
different answer. The expected value is hand arithmetic on the words, and the
test patches nothing, so it holds whatever set the package ships.
"""
import unittest

from ovos_number_parser import (extract_number, extract_number_spans,
                                numbers_to_digits, numtag_readers)

#: language, sentence, the first number, hand arithmetic
CASES = [
    # one thousand
    ("el", "Ήρθαν χίλιοι θεατές.", 1000),
    # two and a half, times one thousand
    ("el", "Κόστισε δυόμισι χιλιάδες ευρώ.", 2500),
    # treinta y uno
    ("es", "Hay treintaiún alumnos en la clase.", 31),
    # two dozen, 2 x 12
    ("es", "Trajo dos docenas de rosas.", 24),
    # kolm, in the allative "kolmele"
    ("et", "Saatsin kutse kolmele sõbrale.", 3),
    # hogeita hamazortzi, 20 + 18 (Euskaltzaindia Araua 7: 38 "hogeita
    # hamazortzi")
    ("eu", "Herriak hogeita hamazortzi etxe ditu.", 38),
    # dva, in the genitive "dveh"
    ("sl", "Bilo jih je okoli dveh.", 2),
]


class TestShippedRoutes(unittest.TestCase):

    def test_the_routed_languages(self):
        self.assertEqual(numtag_readers.NUMTAG_LANGS,
                         frozenset({"el", "es", "et", "eu", "sl"}))

    def test_extract_number_reads_through_numtag(self):
        for lang, text, value in CASES:
            with self.subTest(lang=lang, text=text):
                self.assertEqual(extract_number(text, lang), value)

    def test_the_spans_hold_the_same_number(self):
        for lang, text, value in CASES:
            with self.subTest(lang=lang, text=text):
                spans = extract_number_spans(text, lang)
                self.assertEqual(spans[0].value, value)
                self.assertEqual(text[spans[0].start:spans[0].end],
                                 spans[0].surface)

    def test_numbers_to_digits_writes_the_value(self):
        self.assertEqual(numbers_to_digits("Trajo dos docenas de rosas.", "es"),
                         "Trajo 24 de rosas.")
        self.assertEqual(numbers_to_digits("Bilo jih je okoli dveh.", "sl"),
                         "Bilo jih je okoli 2.")

    def test_a_language_outside_the_set_keeps_its_reader(self):
        self.assertFalse(numtag_readers.routed("ru"))
        self.assertFalse(numtag_readers.routed("mwl"))
        self.assertFalse(numtag_readers.routed("oc"))


if __name__ == "__main__":
    unittest.main()
