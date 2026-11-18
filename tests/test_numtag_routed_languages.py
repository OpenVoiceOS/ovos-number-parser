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
    # kolm, in the allative "kolmele"
    ("et", "Saatsin kutse kolmele sõbrale.", 3),
    # viisi, in the genitive "viiden"
    ("fi", "Meillä on viiden hengen perhe.", 5),
    # viisitoista, in the inessive "viidessätoista"
    ("fi", "Kokous alkaa viidessätoista minuutissa.", 15),
    # dva, in the genitive "dveh"
    ("sl", "Bilo jih je okoli dveh.", 2),
    # one word below a million: 100 + 20 + 3 (Pravidlá slovenského pravopisu,
    # "sedemstodvadsať")
    ("sk", "Mám stodvadsaťtri jabĺk.", 123),
    # dvetisíc is 2 000 (Jazyková poradňa JÚĽŠ)
    ("sk", "Bolo ich dvetisíc.", 2000),
]


class TestShippedRoutes(unittest.TestCase):

    def test_the_routed_languages(self):
        self.assertEqual(numtag_readers.NUMTAG_LANGS,
                         frozenset({"et", "fi", "sk", "sl"}))

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
        self.assertEqual(numbers_to_digits("Meillä on viiden hengen perhe.", "fi"),
                         "Meillä on 5 hengen perhe.")
        self.assertEqual(numbers_to_digits("Bilo jih je okoli dveh.", "sl"),
                         "Bilo jih je okoli 2.")

    def test_a_language_outside_the_set_keeps_its_reader(self):
        for lang in ("el", "es", "eu", "mwl", "oc", "ru", "tr"):
            with self.subTest(lang=lang):
                self.assertFalse(numtag_readers.routed(lang))


if __name__ == "__main__":
    unittest.main()
