"""A lone ordinal in running text is a word, never the fraction 1/n.

Most languages spell a fraction's denominator with the ordinal ("two fifths",
"deux cinquièmes", "twee derde"), so the extractors read a lone ordinal as its
reciprocal. ``numbers_to_digits`` spliced that float into the text:
"le sixième sens" became "le 0.16666666666666666 sens". The ordinal is a
denominator only behind a numerator ("one sixth", "trois quarts").
"""
import unittest

from ovos_number_parser import extract_number, numbers_to_digits


class TestEnglish(unittest.TestCase):

    def test_titles_keep_their_ordinal(self):
        for line in ("the sixth sense", "the fifth element", "the third man",
                     "the second coming"):
            with self.subTest(line=line):
                self.assertEqual(numbers_to_digits(line, "en"), line)

    def test_one_and_a_singular_ordinal_is_a_fraction(self):
        # was "1 1": the ordinal restarted the number and kept the value 1
        self.assertEqual(numbers_to_digits("one sixth", "en"),
                         str(1 / 6))
        self.assertEqual(numbers_to_digits("one third of the cake", "en"),
                         f"{1 / 3} of the cake")
        self.assertEqual(numbers_to_digits("1 sixth", "en"), str(1 / 6))

    def test_quarter_and_plural_denominators_are_fractions(self):
        # "quarter" is no ordinal; English reads it as 1/4 on its own
        self.assertEqual(numbers_to_digits("a quarter", "en"), "a 0.25")
        self.assertEqual(numbers_to_digits("three quarters", "en"), "0.75")
        self.assertEqual(numbers_to_digits("two fifths", "en"), "0.4")

    def test_a_lone_ordinal_does_not_end_the_scan(self):
        # the numbers after it were left unconverted
        self.assertEqual(numbers_to_digits("the sixth day of five", "en"),
                         "the sixth day of 5")
        self.assertEqual(numbers_to_digits("the third of two cats", "en"),
                         "the third of 2 cats")

    def test_a_compound_ordinal_keeps_its_ordinal_word(self):
        self.assertEqual(numbers_to_digits("twenty one third", "en"),
                         "21 third")


class TestGenericPath(unittest.TestCase):
    """Languages served by the generic fallback."""

    TITLES = [("fr", "le sixième sens"), ("fr", "le cinquième élément"),
              ("fr", "le quart d'heure"), ("fr", "le tiers monde"),
              ("ca", "el sisè sentit"),
              ("es", "el quinto elemento"), ("es", "el sexto sentido"),
              ("nl", "het vijfde element"), ("nl", "de derde man")]

    def test_titles_keep_their_ordinal(self):
        for lang, line in self.TITLES:
            with self.subTest(lang=lang, line=line):
                self.assertEqual(numbers_to_digits(line, lang), line)

    def test_a_numerator_and_its_denominator_are_one_fraction(self):
        # was "3 0.25", "1 0.16666666666666666", "2 0.3333333333333333"
        for lang, line, value in [("fr", "un sixième", 1 / 6),
                                  ("fr", "trois quarts", 0.75),
                                  ("fr", "deux tiers", 2 / 3),
                                  ("fr", "deux cinquièmes", 0.4),
                                  ("fr", "un demi", 0.5),
                                  ("ca", "tres quarts", 0.75),
                                  ("es", "tres cuartos", 0.75),
                                  ("nl", "twee derde", 2 / 3),
                                  ("nl", "drie vierde", 0.75)]:
            with self.subTest(lang=lang, line=line):
                self.assertEqual(numbers_to_digits(line, lang), str(value))

    def test_the_fraction_keeps_the_words_around_it(self):
        self.assertEqual(numbers_to_digits("trois quarts d'heure", "fr"),
                         "0.75 d'heure")
        self.assertEqual(numbers_to_digits("kwart over drie", "nl"),
                         "kwart over 3")

    def test_a_tens_word_and_an_ordinal_are_no_fraction(self):
        # extract_number reads "vingt cinquième" as 20 * 1/5 = 4.0; the
        # numerator of a fraction is smaller than its denominator
        self.assertEqual(numbers_to_digits("vingt cinquième", "fr"),
                         "20 cinquième")

    def test_digits_are_untouched(self):
        self.assertEqual(numbers_to_digits("0.25", "fr"), "0.25")
        self.assertEqual(numbers_to_digits("1/4", "fr"), "0.25")


class TestFrisianAndBulgarian(unittest.TestCase):
    """fy and bg run the English pipeline's own copy of the fraction code."""

    def test_titles_keep_their_ordinal(self):
        for lang, line in [("fy", "de tredde man"), ("bg", "трети етаж"),
                           ("bg", "шеста глава"), ("bg", "стотна секунда")]:
            with self.subTest(lang=lang, line=line):
                self.assertEqual(numbers_to_digits(line, lang), line)
                self.assertFalse(extract_number(line, lang))

    def test_a_numerator_and_its_denominator_are_one_fraction(self):
        for lang, line, value in [("fy", "ien tredde", 1 / 3),
                                  ("fy", "twa tredde", 2 / 3),
                                  ("bg", "една трета", 1 / 3),
                                  ("bg", "една стотна", 0.01),
                                  ("bg", "две трети", 2 / 3),
                                  ("bg", "три четвърти", 0.75)]:
            with self.subTest(lang=lang, line=line):
                self.assertEqual(numbers_to_digits(line, lang), str(value))

    def test_words_that_are_no_ordinal_are_still_fractions(self):
        self.assertEqual(numbers_to_digits("in kwart", "fy"), "in 0.25")
        self.assertEqual(numbers_to_digits("половин час", "bg"), "0.5 час")
        self.assertEqual(numbers_to_digits("четвърт час", "bg"), "0.25 час")


if __name__ == "__main__":
    unittest.main()
