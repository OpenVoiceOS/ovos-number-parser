"""Whole numbers built from scale words extract as exact integers.

A float holds 53 bits of mantissa. A value above 2 ** 53 that is summed
through float scale constants loses its low digits, so "twelve quintillion
three hundred forty five" comes back as 1.2e+19 and numbers_to_digits writes
the string "1.2e+19". Every expected value here is integer arithmetic on the
scale value the language gives the word.
"""
import unittest

from ovos_number_parser import extract_number, numbers_to_digits

#: one whole number above 2 ** 53 per language, spoken with its own scale
#: words; the long-scale languages read "trillion" as 10 ** 18
CASES = [
    ("az", "on iki kvintilyon üç yüz qırx beş", 12 * 10 ** 18 + 345),
    ("bg", "двадесет квадрилиона едно", 20 * 10 ** 15 + 1),
    ("cs", "jeden trilion jedna", 10 ** 18 + 1),
    ("da", "tolv trillioner tre hundrede og femogfyrre", 12 * 10 ** 18 + 345),
    ("de", "zwölf Trillionen dreihundertfünfundvierzig", 12 * 10 ** 18 + 345),
    ("en", "twelve quintillion three hundred forty five", 12 * 10 ** 18 + 345),
    ("fy", "tolve triljoen trijehûndertfiifenfjirtich", 12 * 10 ** 18 + 345),
    ("hr", "dvanaest trilijuna tristo četrdeset pet", 12 * 10 ** 18 + 345),
    ("nb", "tolv trillioner tre hundre og førtifem", 12 * 10 ** 18 + 345),
    ("nl", "twaalf triljoen driehonderdvijfenveertig", 12 * 10 ** 18 + 345),
    ("nn", "tolv trillionar tre hundre og førtifem", 12 * 10 ** 18 + 345),
    ("pl", "dwanaście trylionów trzysta czterdzieści pięć", 12 * 10 ** 18 + 345),
    ("ru", "двенадцать квинтиллионов триста сорок пять", 12 * 10 ** 18 + 345),
    ("sv", "tiotusen biljoner sju", 10 ** 4 * 10 ** 12 + 7),
    ("tr", "on iki kentilyon üç yüz kırk beş", 12 * 10 ** 18 + 345),
    ("uk", "дванадцять трильйонів триста сорок п'ять", 12 * 10 ** 18 + 345),
]

#: languages whose numbers_to_digits keeps each of these phrases as one number
N2D_LANGS = {"az", "bg", "cs", "da", "en", "fy", "nl", "pl", "sv", "tr"}


class TestScaleWordsExtractExactly(unittest.TestCase):
    def test_above_float_precision(self):
        for lang, text, expected in CASES:
            with self.subTest(lang=lang, text=text):
                self.assertGreater(expected, 2 ** 53)
                result = extract_number(text, lang)
                self.assertEqual(result, expected)
                self.assertIs(type(result), int)

    def test_numbers_to_digits_writes_every_digit(self):
        for lang, text, expected in CASES:
            if lang not in N2D_LANGS:
                continue
            with self.subTest(lang=lang, text=text):
                self.assertEqual(numbers_to_digits(text, lang), str(expected))


if __name__ == "__main__":
    unittest.main()
