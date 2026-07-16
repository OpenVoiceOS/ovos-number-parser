"""Norwegian Bokmål and Nynorsk share one engine; these tests pin the shared
core, the variant divergences and the two counting traditions."""
import unittest

from ovos_number_parser import (extract_number, is_fractional, is_ordinal,
                                numbers_to_digits, pronounce_number,
                                pronounce_ordinal)


class TestBokmaal(unittest.TestCase):
    def test_pronounce_number(self):
        expected = {0: 'null', 1: 'en', 2: 'to', 7: 'sju', 10: 'ti',
                    11: 'elleve', 12: 'tolv', 20: 'tjue', 21: 'tjueen',
                    30: 'tretti', 40: 'førti', 90: 'nitti',
                    100: 'hundre', 101: 'hundre og en', 1000: 'tusen',
                    2500: 'to tusen fem hundre'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="nb"), spoken)

    def test_modern_forms_are_pronounced(self):
        # Språkrådet's modern norm: sju/tjue rather than syv/tyve
        self.assertEqual(pronounce_number(7, lang="nb"), 'sju')
        self.assertEqual(pronounce_number(20, lang="nb"), 'tjue')

    def test_traditional_forms_still_extract(self):
        # the older norm remains in wide use and must parse
        self.assertEqual(extract_number('syv', lang="nb"), 7)
        self.assertEqual(extract_number('tyve', lang="nb"), 20)
        self.assertEqual(extract_number('enogtyve', lang="nb"), 21)

    def test_negative_and_decimal(self):
        self.assertEqual(extract_number('minus fem', lang="nb"), -5)
        self.assertEqual(extract_number('fem komma to', lang="nb"), 5.2)

    def test_round_trip_sweep(self):
        values = list(range(0, 121)) + [150, 500, 999, 1000, 1001, 2500,
                                        12345, 100000, 1000000]
        for n in values:
            spoken = pronounce_number(n, lang="nb")
            self.assertEqual(extract_number(spoken, lang="nb"), n,
                             f"{n} -> {spoken!r}")


class TestNynorsk(unittest.TestCase):
    def test_one_is_ein(self):
        self.assertEqual(pronounce_number(1, lang="nn"), 'ein')
        self.assertEqual(pronounce_number(21, lang="nn"), 'tjueein')

    def test_shared_core(self):
        for n, spoken in {7: 'sju', 20: 'tjue', 100: 'hundre',
                          1000: 'tusen'}.items():
            with self.subTest(number=n):
                self.assertEqual(pronounce_number(n, lang="nn"), spoken)

    def test_round_trip_sweep(self):
        values = list(range(0, 121)) + [150, 500, 1000, 2500, 12345]
        for n in values:
            spoken = pronounce_number(n, lang="nn")
            self.assertEqual(extract_number(spoken, lang="nn"), n,
                             f"{n} -> {spoken!r}")


class TestMacrolanguageCode(unittest.TestCase):
    def test_no_resolves_to_bokmaal(self):
        for n in (1, 7, 21, 2500):
            self.assertEqual(pronounce_number(n, lang="no"),
                             pronounce_number(n, lang="nb"))
        self.assertEqual(extract_number('tjueen', lang="no"), 21)


class TestHelpers(unittest.TestCase):
    def test_is_ordinal(self):
        self.assertEqual(is_ordinal('første', lang="nb"), 1)
        self.assertEqual(is_ordinal('andre', lang="nb"), 2)
        self.assertFalse(is_ordinal('katt', lang="nb"))

    def test_pronounce_ordinal(self):
        self.assertEqual(pronounce_ordinal(1, lang="nb"), 'første')
        self.assertEqual(pronounce_ordinal(2, lang="nb"), 'andre')

    def test_is_fractional(self):
        self.assertEqual(is_fractional('halv', lang="nb"), 0.5)
        self.assertFalse(is_fractional('katt', lang="nb"))

    def test_numbers_to_digits(self):
        self.assertEqual(numbers_to_digits('tjueen katter', lang="nb"),
                         '21 katter')

    def test_no_number(self):
        for lang in ("nb", "nn"):
            self.assertFalse(extract_number('god morgen', lang=lang))


if __name__ == "__main__":
    unittest.main()
