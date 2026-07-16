import unittest

from ovos_number_parser import (extract_number, is_fractional, is_ordinal,
                                pronounce_fraction, pronounce_number,
                                pronounce_ordinal)


class TestSlovakPronounce(unittest.TestCase):
    """Anchors for spoken Slovak numbers."""

    def test_pronounce_number(self):
        expected = {0: 'nula', 1: 'jeden', 2: 'dva', 3: 'tri', 4: 'štyri',
                    5: 'päť', 6: 'šesť', 7: 'sedem', 8: 'osem', 9: 'deväť',
                    10: 'desať', 11: 'jedenásť', 12: 'dvanásť', 13: 'trinásť',
                    14: 'štrnásť', 15: 'pätnásť', 16: 'šestnásť',
                    17: 'sedemnásť', 18: 'osemnásť', 19: 'devätnásť',
                    20: 'dvadsať', 21: 'dvadsaťjeden', 30: 'tridsať',
                    42: 'štyridsaťdva', 50: 'päťdesiat',
                    66: 'šesťdesiatšesť', 70: 'sedemdesiat',
                    80: 'osemdesiat', 90: 'deväťdesiat',
                    99: 'deväťdesiatdeväť', 100: 'sto', 101: 'sto jeden',
                    123: 'sto dvadsaťtri', 200: 'dvesto', 500: 'päťsto',
                    999: 'deväťsto deväťdesiatdeväť', 1000: 'tisíc',
                    2000: 'dva tisíce', 2023: 'dva tisíce dvadsaťtri',
                    5000: 'päť tisíc', 1000000: 'milión',
                    2000000: 'dva milióny', 5000000: 'päť miliónov'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="sk"), spoken)

    def test_pronounce_negative_and_decimal(self):
        expected = {-7: 'mínus sedem', -42: 'mínus štyridsaťdva',
                    2.5: 'dva celá päť', 3.14: 'tri celá jeden štyri',
                    -3.5: 'mínus tri celá päť', 0.5: 'nula celá päť'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="sk"), spoken)

    def test_pronounce_ordinal(self):
        expected = {1: 'prvý', 2: 'druhý', 3: 'tretí', 4: 'štvrtý',
                    5: 'piaty', 6: 'šiesty', 7: 'siedmy', 8: 'ôsmy',
                    9: 'deviaty', 10: 'desiaty', 20: 'dvadsiaty',
                    21: 'dvadsiaty prvý', 45: 'štyridsiaty piaty',
                    100: 'stý', 200: 'dvojstý', 1000: 'tisíci',
                    1000000: 'miliónty'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_ordinal(number, lang="sk"), spoken)

    def test_invalid_ordinal_raises(self):
        with self.assertRaises(ValueError):
            pronounce_ordinal(0, lang="sk")

    def test_pronounce_fraction(self):
        expected = {"1/2": "polovica", "2/3": "dve tretiny",
                    "3/4": "tri štvrtiny", "2/5": "dve pätiny"}
        for frac, spoken in expected.items():
            with self.subTest(frac=frac):
                self.assertEqual(pronounce_fraction(frac, lang="sk"), spoken)


class TestSlovakExtract(unittest.TestCase):
    """Anchors for extracting numbers from Slovak text."""

    def test_extract_number(self):
        expected = {0: 'nula', 1: 'jeden', 2: 'dva', 3: 'tri', 4: 'štyri',
                    5: 'päť', 6: 'šesť', 7: 'sedem', 8: 'osem', 9: 'deväť',
                    10: 'desať', 15: 'pätnásť', 19: 'devätnásť',
                    20: 'dvadsať', 21: 'dvadsaťjeden', 42: 'štyridsaťdva',
                    99: 'deväťdesiatdeväť', 100: 'sto', 101: 'sto jeden',
                    123: 'sto dvadsaťtri', 200: 'dvesto', 500: 'päťsto',
                    999: 'deväťsto deväťdesiatdeväť', 1000: 'tisíc',
                    2000: 'dva tisíce', 2023: 'dva tisíce dvadsaťtri',
                    5000: 'päť tisíc', 1000000: 'milión',
                    2000000: 'dva milióny', 5000000: 'päť miliónov'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="sk"), number)

    def test_extract_inflected_forms(self):
        # feminine/neuter forms of "one" and "two"
        self.assertEqual(extract_number("jedna", lang="sk"), 1)
        self.assertEqual(extract_number("jedno", lang="sk"), 1)
        self.assertEqual(extract_number("dve", lang="sk"), 2)

    def test_extract_negative_and_decimal(self):
        expected = {-7: 'mínus sedem', -42: 'mínus štyridsaťdva',
                    2.5: 'dva celá päť', 3.14: 'tri celá jeden štyri',
                    -3.5: 'mínus tri celá päť', 0.5: 'nula celá päť',
                    5.2: 'päť celá dva'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="sk"), number)

    def test_extract_decimal_comma(self):
        # "čiarka" (comma) is also accepted as a decimal marker
        self.assertEqual(extract_number("päť čiarka dva", lang="sk"), 5.2)

    def test_extract_from_sentence(self):
        self.assertEqual(extract_number('mám dvadsaťjeden mačiek', lang="sk"),
                         21)

    def test_no_number(self):
        self.assertIn(extract_number("ahoj ako sa máš", lang="sk"),
                      (False, None))

    def test_is_fractional(self):
        self.assertEqual(is_fractional("polovica", lang="sk"), 0.5)
        self.assertEqual(is_fractional("tretina", lang="sk"), 1.0 / 3)
        self.assertEqual(is_fractional("štvrtina", lang="sk"), 0.25)
        self.assertEqual(is_fractional("pätina", lang="sk"), 0.2)
        self.assertEqual(is_fractional("tretiny", lang="sk"), 1.0 / 3)
        self.assertFalse(is_fractional("mačka", lang="sk"))

    def test_is_ordinal(self):
        self.assertEqual(is_ordinal("prvý", lang="sk"), 1)
        self.assertEqual(is_ordinal("druhý", lang="sk"), 2)
        self.assertEqual(is_ordinal("tretí", lang="sk"), 3)
        self.assertEqual(is_ordinal("dvadsiaty prvý", lang="sk"), 21)
        self.assertFalse(is_ordinal("mačka", lang="sk"))


class TestSlovakRoundTrip(unittest.TestCase):
    """pronounce_number output must be understood by extract_number."""

    def test_round_trip(self):
        numbers = list(range(0, 200)) + \
            [201, 222, 300, 345, 400, 456, 500, 678, 700, 891, 900,
             1000, 1001, 2000, 2023, 5000, 9999, 10000, 100000,
             1000000, 2000000]
        for number in numbers:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="sk")
                self.assertEqual(extract_number(spoken, lang="sk"), number)

    def test_round_trip_negative_and_decimal(self):
        for number in [-7, -42, 2.5, 3.14, -3.5, 0.5, 5.2]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="sk")
                self.assertEqual(extract_number(spoken, lang="sk"), number)


if __name__ == "__main__":
    unittest.main()
