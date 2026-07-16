import unittest

from ovos_number_parser import (extract_number, is_fractional, is_ordinal,
                                numbers_to_digits, pronounce_fraction,
                                pronounce_number, pronounce_ordinal)


class TestTurkishPronounce(unittest.TestCase):
    def test_pronounce_number(self):
        expected = {0: 'sıfır', 1: 'bir', 2: 'iki', 5: 'beş', 10: 'on',
                    11: 'on bir', 20: 'yirmi', 21: 'yirmi bir',
                    40: 'kırk', 90: 'doksan', 100: 'yüz', 101: 'yüz bir',
                    200: 'iki yüz', 1000: 'bin', 2500: 'iki bin beş yüz',
                    1000000: 'bir milyon'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="tr"), spoken)

    def test_negative_and_decimal(self):
        self.assertEqual(pronounce_number(-5, lang="tr"), 'eksi beş')
        self.assertEqual(pronounce_number(5.2, lang="tr"), 'beş virgül iki')

    def test_ordinals(self):
        for n, spoken in {1: 'birinci', 2: 'ikinci', 3: 'üçüncü',
                          10: 'onuncu'}.items():
            with self.subTest(number=n):
                self.assertEqual(pronounce_ordinal(n, lang="tr"), spoken)

    def test_fractions(self):
        # Turkish builds fractions with the locative: "üçte iki" = 2/3
        self.assertEqual(pronounce_fraction("1/2", lang="tr"), 'yarım')
        self.assertEqual(pronounce_fraction("1/4", lang="tr"), 'çeyrek')
        self.assertEqual(pronounce_fraction("2/3", lang="tr"), 'üçte iki')
        self.assertEqual(pronounce_fraction("3/4", lang="tr"), 'dörtte üç')


class TestTurkishExtract(unittest.TestCase):
    def test_anchors(self):
        for spoken, expected in [('bir', 1), ('yirmi bir', 21), ('yüz', 100),
                                 ('bin', 1000), ('iki bin beş yüz', 2500)]:
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="tr"), expected)

    def test_bucuk_is_a_half_after_a_number(self):
        self.assertEqual(extract_number('bir buçuk', lang="tr"), 1.5)
        self.assertEqual(extract_number('yarım', lang="tr"), 0.5)

    def test_negative_and_decimal(self):
        self.assertEqual(extract_number('eksi beş', lang="tr"), -5)
        self.assertEqual(extract_number('beş virgül iki', lang="tr"), 5.2)

    def test_in_sentence(self):
        self.assertEqual(extract_number('yirmi bir kedim var', lang="tr"), 21)

    def test_no_number(self):
        self.assertFalse(extract_number('günaydın', lang="tr"))

    def test_round_trip_sweep(self):
        values = list(range(0, 121)) + [150, 500, 999, 1000, 1001, 2500,
                                        12345, 100000, 1000000]
        for n in values:
            spoken = pronounce_number(n, lang="tr")
            self.assertEqual(extract_number(spoken, lang="tr"), n,
                             f"{n} -> {spoken!r}")


class TestTurkishHelpers(unittest.TestCase):
    def test_is_fractional(self):
        self.assertEqual(is_fractional('yarım', lang="tr"), 0.5)
        self.assertEqual(is_fractional('çeyrek', lang="tr"), 0.25)
        self.assertFalse(is_fractional('kedi', lang="tr"))

    def test_is_ordinal(self):
        self.assertEqual(is_ordinal('birinci', lang="tr"), 1)
        self.assertEqual(is_ordinal('ikinci', lang="tr"), 2)
        self.assertFalse(is_ordinal('kedi', lang="tr"))

    def test_numbers_to_digits(self):
        self.assertEqual(numbers_to_digits('yirmi bir kedi', lang="tr"),
                         '21 kedi')


if __name__ == "__main__":
    unittest.main()
