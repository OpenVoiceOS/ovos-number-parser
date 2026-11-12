"""Hebrew ו ("and") before a number word: one number or a new one.

A compound numeral names its components from the largest to the smallest and
puts ו before the last one, as the example in Hebrew Wikipedia, "שם מספר",
section "אבני יסוד", shows: "שלושת־אלפים שש־מאות ושבע־עשרה" = 3617. A ו before
a component that does not fit that order starts a new number, and
numbers_to_digits keeps it.
"""
import unittest

from ovos_number_parser import extract_number, numbers_to_digits
from ovos_number_parser.numbers_he import extract_numbers_he


class TestConjunctionBeforeANewNumber(unittest.TestCase):
    #: sentence, its numbers_to_digits form
    KEPT = [
        # "I have a car and three bicycles"
        ("יש לי מכונית ושלוש אופניים", "יש לי מכונית ו3 אופניים"),
        # "I bought a book and ten pens"
        ("קניתי ספר ועשרה עטים", "קניתי ספר ו10 עטים"),
        # "one book and two pens": two numbers, 1 and 2
        ("ספר אחד ושני עטים", "ספר 1 ו2 עטים"),
        # "three and four" are two numbers, not seven
        ("שלושה וארבעה", "3 ו4"),
    ]

    #: one number whose last component carries the ו
    JOINED = [("אלף וחמישים", "1050"),
              ("עשרים ושלוש", "23"),
              ("מאה ועשרים", "120"),
              ("אלפיים עשרים ושלוש", "2023"),
              ("שלוש מאות ושלושים", "330")]

    #: 300 to 900 are a unit and "מאות"; the converter reads them whole
    HUNDREDS = [("שלוש מאות", "300"),
                ("תשע מאות תשעים ותשע", "999"),
                ("אלף תשע מאות שמונים וחמש", "1985")]

    #: a ו word that the converter does not turn into digits: the text comes
    #: back as it was written
    UNCHANGED = ["והשלושה הלכו",  # "and the three went"
                 "ושנייה",  # "and a second"
                 "וראשון",  # "and first"
                 "ושליש",  # "and a third"
                 "ורבע"]  # "and a quarter"

    #: a ו typed as a word of its own: the converter did not split it off,
    #: so it stays where the writer put it
    OWN_WORD = ["ספר ו עט",  # "book and pen", no number
                "ספר ו 3 עטים"]  # the digits were already there

    def test_a_conjunction_typed_apart_stays_apart(self):
        for text in self.OWN_WORD:
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, lang="he"), text)

    def test_a_private_use_character_in_the_input_stays(self):
        # the converter holds a typed-apart ו in a private-use character; one
        # that is already in the text is not a held ו
        for text in ("ספר \ue000 עט", "ספר ו \ue000 שלוש"):
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, lang="he"),
                                 text.replace("שלוש", "3"))

    def test_a_word_that_stays_a_word_keeps_its_conjunction(self):
        for text in self.UNCHANGED:
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, lang="he"), text)

    def test_the_conjunction_stays_before_a_new_number(self):
        for text, expected in self.KEPT:
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, lang="he"), expected)

    def test_the_conjunction_joins_one_number(self):
        for text, expected in self.JOINED:
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, lang="he"), expected)

    def test_hundreds_three_to_nine_hundred(self):
        for text, expected in self.HUNDREDS:
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, lang="he"), expected)


class TestComponentsDescend(unittest.TestCase):
    #: text, the numbers it holds (hand-read: a component that is not smaller
    #: than the place left open starts a new number)
    CASES = [("שלושה וארבעה", [3, 4]),
             ("שלושה ארבעה", [3, 4]),
             ("שלוש ועשרים", [3, 20]),
             ("עשרים ושלושים", [20, 30]),
             ("מאה ומאתיים", [100, 200]),
             ("שלוש ארבע חמש", [3, 4, 5]),
             ("אלף ומאה", [1100]),
             ("מאה ושלוש עשרה", [113]),
             ("מאה עשרים ושלוש", [123]),
             ("אלף תשע מאות שמונים וחמש", [1985])]

    def test_each_number(self):
        for text, expected in self.CASES:
            with self.subTest(text=text):
                self.assertEqual(extract_numbers_he(text), expected)

    def test_extract_number_takes_the_first(self):
        self.assertEqual(extract_number("שלושה וארבעה", lang="he"), 3)


if __name__ == "__main__":
    unittest.main()
