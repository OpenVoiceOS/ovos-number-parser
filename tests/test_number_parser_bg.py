import unittest

from ovos_number_parser import (extract_number, is_fractional, is_ordinal,
                                numbers_to_digits, pronounce_fraction,
                                pronounce_number, pronounce_ordinal)

ANCHORS = {
    0: 'нула', 1: 'едно', 2: 'две', 3: 'три', 4: 'четири', 5: 'пет',
    6: 'шест', 7: 'седем', 8: 'осем', 9: 'девет', 10: 'десет',
    11: 'единадесет', 12: 'дванадесет', 13: 'тринадесет',
    14: 'четиринадесет', 15: 'петнадесет', 16: 'шестнадесет',
    17: 'седемнадесет', 18: 'осемнадесет', 19: 'деветнадесет',
    20: 'двадесет', 21: 'двадесет и едно', 30: 'тридесет',
    42: 'четиридесет и две', 50: 'петдесет', 60: 'шестдесет',
    66: 'шестдесет и шест', 70: 'седемдесет', 80: 'осемдесет',
    90: 'деветдесет', 99: 'деветдесет и девет', 100: 'сто',
    101: 'сто и едно', 105: 'сто и пет', 110: 'сто и десет',
    123: 'сто двадесет и три', 145: 'сто четиридесет и пет',
    200: 'двеста', 300: 'триста', 400: 'четиристотин', 500: 'петстотин',
    600: 'шестстотин', 700: 'седемстотин', 800: 'осемстотин',
    900: 'деветстотин', 999: 'деветстотин деветдесет и девет',
    1000: 'хиляда', 1001: 'хиляда и едно', 1100: 'хиляда и сто',
    2000: 'две хиляди', 2023: 'две хиляди двадесет и три',
    100000: 'сто хиляди', 1000000: 'един милион', 2000000: 'два милиона',
    1000000000: 'един милиард', 2000000000: 'два милиарда',
}

NEG_AND_DECIMAL = {
    -7: 'минус седем', -42: 'минус четиридесет и две',
    2.5: 'две запетая пет', 3.14: 'три запетая едно четири',
    -3.5: 'минус три запетая пет', 0.5: 'нула запетая пет',
}


class TestBulgarianPronounce(unittest.TestCase):
    """Anchors for spoken Bulgarian numbers."""

    def test_pronounce_number(self):
        for number, spoken in ANCHORS.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="bg"), spoken)

    def test_pronounce_negative_and_decimal(self):
        for number, spoken in NEG_AND_DECIMAL.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="bg"), spoken)

    def test_pronounce_ordinal(self):
        expected = {1: 'първи', 2: 'втори', 3: 'трети', 4: 'четвърти',
                    5: 'пети', 6: 'шести', 7: 'седми', 8: 'осми',
                    9: 'девети', 10: 'десети', 11: 'единадесети',
                    20: 'двадесети', 21: 'двадесет и първи',
                    45: 'четиридесет и пети', 100: 'стотен',
                    105: 'сто и пети', 121: 'сто двадесет и първи',
                    1000: 'хиляден', 1000000: 'милионен'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_ordinal(number, lang="bg"), spoken)

    def test_invalid_ordinal_raises(self):
        with self.assertRaises(ValueError):
            pronounce_ordinal(0, lang="bg")

    def test_pronounce_fraction(self):
        expected = {"1/2": "половина", "2/3": "две трети",
                    "3/4": "три четвърти", "1/3": "една трета",
                    "1/4": "една четвърт", "1/5": "една пета",
                    "2/5": "две пети"}
        for frac, spoken in expected.items():
            with self.subTest(frac=frac):
                self.assertEqual(pronounce_fraction(frac, lang="bg"), spoken)


class TestBulgarianExtract(unittest.TestCase):
    """Anchors for extracting numbers from Bulgarian text."""

    def test_extract_number(self):
        for number, spoken in ANCHORS.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="bg"), number)

    def test_extract_negative_and_decimal(self):
        for number, spoken in NEG_AND_DECIMAL.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="bg"), number)

    def test_both_spelling_variants_parse(self):
        # contracted colloquial spellings parse to the same values as the
        # full standard forms
        variants = {
            11: ('единадесет', 'единайсет'),
            12: ('дванадесет', 'дванайсет'),
            13: ('тринадесет', 'тринайсет'),
            14: ('четиринадесет', 'четиринайсет'),
            15: ('петнадесет', 'петнайсет'),
            16: ('шестнадесет', 'шестнайсет'),
            17: ('седемнадесет', 'седемнайсет'),
            18: ('осемнадесет', 'осемнайсет'),
            19: ('деветнадесет', 'деветнайсет'),
            20: ('двадесет', 'двайсет'),
            23: ('двадесет и три', 'двайсет и три'),
            30: ('тридесет', 'трийсет'),
            40: ('четиридесет', 'четирийсет'),
            45: ('четиридесет и пет', 'четирийсет и пет'),
            60: ('шестдесет', 'шейсет'),
            66: ('шестдесет и шест', 'шейсет и шест'),
        }
        for number, spellings in variants.items():
            for spoken in spellings:
                with self.subTest(spoken=spoken):
                    self.assertEqual(extract_number(spoken, lang="bg"),
                                     number)

    def test_gender_variants_parse(self):
        for spoken, number in [('един', 1), ('една', 1), ('едно', 1),
                               ('два', 2), ('две', 2),
                               ('двадесет и един', 21),
                               ('двадесет и една', 21)]:
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="bg"), number)

    def test_extract_fractions(self):
        self.assertEqual(extract_number('две и половина', lang="bg"), 2.5)
        self.assertEqual(extract_number('половин час', lang="bg"), 0.5)
        self.assertAlmostEqual(extract_number('две трети', lang="bg"), 2 / 3)
        self.assertEqual(extract_number('три четвърти', lang="bg"), 0.75)

    def test_extract_decimal_variants(self):
        # both "запетая" and "цяло" mark the decimal part
        self.assertEqual(extract_number('пет запетая две', lang="bg"), 5.2)
        self.assertEqual(extract_number('пет цяло и две', lang="bg"), 5.2)

    def test_extract_ordinals(self):
        self.assertEqual(
            extract_number('това е третият път', lang="bg", ordinals=True),
            False)  # inflected form is out of scope
        self.assertEqual(extract_number('трети', lang="bg", ordinals=True), 3)
        self.assertEqual(
            extract_number('двадесет и първи', lang="bg", ordinals=True), 21)

    def test_extract_from_sentence(self):
        self.assertEqual(
            extract_number('имам двадесет и една котки', lang="bg"), 21)
        self.assertEqual(
            extract_number('поръчай две хиляди двадесет и три бройки',
                           lang="bg"), 2023)

    def test_no_number(self):
        self.assertIn(extract_number('здравей как си', lang="bg"),
                      (False, None))


class TestBulgarianHelpers(unittest.TestCase):

    def test_is_fractional(self):
        self.assertEqual(is_fractional('половина', lang="bg"), 0.5)
        self.assertEqual(is_fractional('половин', lang="bg"), 0.5)
        self.assertEqual(is_fractional('трета', lang="bg"), 1 / 3)
        self.assertEqual(is_fractional('третина', lang="bg"), 1 / 3)
        self.assertEqual(is_fractional('четвърт', lang="bg"), 0.25)
        self.assertEqual(is_fractional('четвъртина', lang="bg"), 0.25)
        self.assertEqual(is_fractional('пета', lang="bg"), 0.2)
        self.assertEqual(is_fractional('пети', lang="bg"), 0.2)
        self.assertEqual(is_fractional('стотна', lang="bg"), 0.01)
        self.assertFalse(is_fractional('котка', lang="bg"))

    def test_is_ordinal(self):
        self.assertEqual(is_ordinal('първи', lang="bg"), 1)
        self.assertEqual(is_ordinal('втори', lang="bg"), 2)
        self.assertEqual(is_ordinal('десети', lang="bg"), 10)
        self.assertEqual(is_ordinal('двадесет и първи', lang="bg"), 21)
        self.assertFalse(is_ordinal('котка', lang="bg"))

    def test_numbers_to_digits(self):
        self.assertEqual(
            numbers_to_digits('имам двадесет и една котки', lang="bg"),
            'имам 21 котки')
        self.assertEqual(
            numbers_to_digits('двайсет и пет къщи', lang="bg"),
            '25 къщи')
        self.assertEqual(
            numbers_to_digits('здравей как си', lang="bg").strip(),
            'здравей как си')


class TestBulgarianRoundTrip(unittest.TestCase):
    """pronounce_number output must be understood by extract_number."""

    def test_round_trip(self):
        numbers = list(range(0, 200)) + \
            [201, 222, 300, 345, 400, 456, 500, 678, 700, 891, 900,
             1000, 1001, 1234, 2000, 2023, 5000, 9999, 10000, 100000,
             123456, 1000000, 2000000, 2500000, 1000000000]
        for number in numbers:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="bg")
                self.assertEqual(extract_number(spoken, lang="bg"), number)

    def test_round_trip_negative_and_decimal(self):
        for number in [-7, -42, 2.5, 3.14, -3.5, 0.5]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="bg")
                self.assertEqual(extract_number(spoken, lang="bg"), number)


if __name__ == "__main__":
    unittest.main()
