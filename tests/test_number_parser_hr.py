import unittest

from ovos_number_parser import (extract_number, is_fractional, is_ordinal,
                                numbers_to_digits, pronounce_fraction,
                                pronounce_number, pronounce_ordinal)

PRONOUNCE_ANCHORS = {
    0: 'nula', 1: 'jedan', 2: 'dva', 3: 'tri', 4: 'četiri', 5: 'pet',
    6: 'šest', 7: 'sedam', 8: 'osam', 9: 'devet', 10: 'deset',
    11: 'jedanaest', 12: 'dvanaest', 13: 'trinaest', 14: 'četrnaest',
    15: 'petnaest', 16: 'šesnaest', 17: 'sedamnaest', 18: 'osamnaest',
    19: 'devetnaest', 20: 'dvadeset', 21: 'dvadeset jedan', 30: 'trideset',
    42: 'četrdeset dva', 50: 'pedeset', 60: 'šezdeset', 66: 'šezdeset šest',
    70: 'sedamdeset', 80: 'osamdeset', 90: 'devedeset',
    99: 'devedeset devet', 100: 'sto', 101: 'sto jedan', 110: 'sto deset',
    123: 'sto dvadeset tri', 200: 'dvjesto', 300: 'tristo',
    400: 'četiristo', 500: 'petsto', 600: 'šesto', 700: 'sedamsto',
    800: 'osamsto', 900: 'devetsto', 999: 'devetsto devedeset devet',
    1000: 'tisuća', 1001: 'tisuću jedan', 2000: 'dvije tisuće',
    2023: 'dvije tisuće dvadeset tri', 5000: 'pet tisuća',
    21000: 'dvadeset jedna tisuća', 100000: 'sto tisuća',
    1000000: 'milijun', 2000000: 'dva milijuna', 5000000: 'pet milijuna',
    1000000000: 'milijarda', 2000000000: 'dvije milijarde',
}


class TestCroatianPronounce(unittest.TestCase):
    """Anchors for spoken Croatian numbers."""

    def test_pronounce_number(self):
        for number, spoken in PRONOUNCE_ANCHORS.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="hr"), spoken)

    def test_pronounce_negative_and_decimal(self):
        expected = {-7: 'minus sedam', -42: 'minus četrdeset dva',
                    2.5: 'dva zarez pet', 3.14: 'tri zarez jedan četiri',
                    -3.5: 'minus tri zarez pet', 0.5: 'nula zarez pet'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="hr"), spoken)


class TestCroatianExtract(unittest.TestCase):
    """Anchors for extracting numbers from Croatian text."""

    def test_extract_number(self):
        for number, spoken in PRONOUNCE_ANCHORS.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="hr"), number)

    def test_extract_negative_and_decimal(self):
        expected = {-7: 'minus sedam', -42: 'minus četrdeset dva',
                    2.5: 'dva zarez pet', 3.14: 'tri zarez jedan četiri',
                    -3.5: 'minus tri zarez pet', 0.5: 'nula zarez pet'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="hr"), number)

    def test_optional_i_connector(self):
        # "dvadeset i jedan" and "dvadeset jedan" both mean 21
        self.assertEqual(extract_number("dvadeset i jedan", lang="hr"), 21)
        self.assertEqual(extract_number("dvadeset jedan", lang="hr"), 21)
        self.assertEqual(extract_number("sto dvadeset i tri", lang="hr"), 123)

    def test_feminine_and_neuter_forms(self):
        self.assertEqual(extract_number("jedna", lang="hr"), 1)
        self.assertEqual(extract_number("jedno", lang="hr"), 1)
        self.assertEqual(extract_number("dvije", lang="hr"), 2)
        self.assertEqual(extract_number("dvjesta", lang="hr"), 200)
        self.assertEqual(extract_number("šeststo", lang="hr"), 600)

    def test_decimal_markers(self):
        self.assertEqual(extract_number("pet zarez dva", lang="hr"), 5.2)
        self.assertEqual(extract_number("dvije cijele pet", lang="hr"), 2.5)

    def test_fraction_words(self):
        self.assertEqual(extract_number("pola", lang="hr"), 0.5)
        self.assertEqual(extract_number("dva i pol", lang="hr"), 2.5)
        self.assertEqual(extract_number("trećina", lang="hr"), 1 / 3)

    def test_extract_from_sentence(self):
        self.assertEqual(extract_number('imam dvadeset jedan mačku', lang="hr"),
                         21)

    def test_ordinals_flag(self):
        self.assertEqual(extract_number("prvi", lang="hr", ordinals=True), 1)
        self.assertEqual(extract_number("dvadeset prvi", lang="hr",
                                        ordinals=True), 21)

    def test_no_number(self):
        self.assertIn(extract_number("bok kako si", lang="hr"), (False, None))


class TestCroatianOrdinals(unittest.TestCase):
    def test_pronounce_ordinal(self):
        expected = {1: 'prvi', 2: 'drugi', 3: 'treći', 4: 'četvrti',
                    5: 'peti', 6: 'šesti', 7: 'sedmi', 8: 'osmi',
                    9: 'deveti', 10: 'deseti', 20: 'dvadeseti',
                    21: 'dvadeset prvi', 45: 'četrdeset peti',
                    100: 'stoti', 200: 'dvjestoti', 1000: 'tisući',
                    1000000: 'milijunti'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_ordinal(number, lang="hr"), spoken)

    def test_invalid_ordinal_raises(self):
        with self.assertRaises(ValueError):
            pronounce_ordinal(0, lang="hr")

    def test_is_ordinal(self):
        self.assertEqual(is_ordinal("treći", lang="hr"), 3)
        self.assertEqual(is_ordinal("dvadeset prvi", lang="hr"), 21)
        self.assertFalse(is_ordinal("pas", lang="hr"))

    def test_ordinal_roundtrip_sweep(self):
        for n in list(range(1, 100)) + [100, 1000]:
            spoken = pronounce_ordinal(n, lang="hr")
            self.assertEqual(is_ordinal(spoken, lang="hr"), n,
                             f"{n}: {spoken!r}")


class TestCroatianFractions(unittest.TestCase):
    def test_pronounce_fraction(self):
        expected = {"1/2": "polovina", "2/3": "dvije trećine",
                    "3/4": "tri četvrtine", "1/3": "trećina",
                    "3/2": "jedan i pol", "1/4": "četvrtina"}
        for frac, spoken in expected.items():
            with self.subTest(frac=frac):
                self.assertEqual(pronounce_fraction(frac, lang="hr"), spoken)

    def test_is_fractional(self):
        self.assertEqual(is_fractional("polovina", lang="hr"), 0.5)
        self.assertEqual(is_fractional("pola", lang="hr"), 0.5)
        self.assertEqual(is_fractional("trećina", lang="hr"), 1 / 3)
        self.assertEqual(is_fractional("četvrtina", lang="hr"), 0.25)
        self.assertEqual(is_fractional("petina", lang="hr"), 0.2)
        self.assertEqual(is_fractional("trećine", lang="hr"), 1 / 3)
        self.assertFalse(is_fractional("xyzzy", lang="hr"))
        self.assertFalse(is_fractional("jedan", lang="hr"))


class TestCroatianNumbersToDigits(unittest.TestCase):
    def test_in_sentence(self):
        self.assertEqual(
            numbers_to_digits("imam dvadeset jedan mačku", lang="hr"),
            "imam 21 mačku")
        self.assertEqual(
            numbers_to_digits("imam dvadeset i jedan mačku", lang="hr"),
            "imam 21 mačku")

    def test_no_numbers(self):
        self.assertEqual(numbers_to_digits("bok kako si", lang="hr").strip(),
                         "bok kako si")


class TestCroatianRoundTrip(unittest.TestCase):
    """pronounce_number output must be understood by extract_number."""

    def test_round_trip(self):
        numbers = list(range(0, 200)) + \
            [201, 222, 300, 345, 400, 456, 500, 678, 700, 891, 900, 999,
             1000, 1001, 2000, 2023, 5000, 9999, 10000, 21000, 100000,
             1000000, 2000000, 1000000000, 2000000000]
        for number in numbers:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="hr")
                self.assertEqual(extract_number(spoken, lang="hr"), number)

    def test_round_trip_negative_and_decimal(self):
        for number in [-7, -42, 2.5, 3.14, -3.5, 0.5]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="hr")
                self.assertEqual(extract_number(spoken, lang="hr"), number)


if __name__ == "__main__":
    unittest.main()
