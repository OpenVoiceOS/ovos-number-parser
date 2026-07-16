"""Indonesian and Malay share one implementation; these tests pin both the
common core and the points where the two standards diverge."""
import unittest

from ovos_number_parser import (extract_number, is_fractional, is_ordinal,
                                numbers_to_digits, pronounce_fraction,
                                pronounce_number, pronounce_ordinal)


class TestSharedCore(unittest.TestCase):
    def test_pronounce_number(self):
        expected = {1: 'satu', 2: 'dua', 5: 'lima', 10: 'sepuluh',
                    11: 'sebelas', 12: 'dua belas', 20: 'dua puluh',
                    21: 'dua puluh satu', 100: 'seratus',
                    200: 'dua ratus', 1000: 'seribu',
                    2500: 'dua ribu lima ratus'}
        for lang in ("id", "ms"):
            for number, spoken in expected.items():
                with self.subTest(lang=lang, number=number):
                    self.assertEqual(pronounce_number(number, lang=lang),
                                     spoken)

    def test_se_prefix(self):
        # the se- prefix replaces "satu" on 11, 100 and 1000
        for lang in ("id", "ms"):
            self.assertEqual(pronounce_number(11, lang=lang), 'sebelas')
            self.assertEqual(pronounce_number(100, lang=lang), 'seratus')
            self.assertEqual(pronounce_number(1000, lang=lang), 'seribu')

    def test_ordinals(self):
        for lang in ("id", "ms"):
            self.assertEqual(pronounce_ordinal(2, lang=lang), 'kedua')
            self.assertEqual(pronounce_ordinal(3, lang=lang), 'ketiga')

    def test_fractions(self):
        for lang in ("id", "ms"):
            self.assertEqual(pronounce_fraction("1/2", lang=lang),
                             'setengah')
            self.assertEqual(pronounce_fraction("2/3", lang=lang),
                             'dua pertiga')

    def test_extract(self):
        for lang in ("id", "ms"):
            self.assertEqual(extract_number('dua puluh satu', lang=lang), 21)
            self.assertEqual(extract_number('seribu', lang=lang), 1000)
            self.assertEqual(extract_number('setengah', lang=lang), 0.5)

    def test_no_number(self):
        for lang in ("id", "ms"):
            self.assertFalse(extract_number('selamat pagi', lang=lang))

    def test_round_trip_sweep(self):
        values = list(range(0, 121)) + [150, 500, 999, 1000, 1001, 2500,
                                        12345, 100000, 1000000]
        for lang in ("id", "ms"):
            for n in values:
                spoken = pronounce_number(n, lang=lang)
                self.assertEqual(extract_number(spoken, lang=lang), n,
                                 f"{lang}: {n} -> {spoken!r}")


class TestDivergences(unittest.TestCase):
    def test_eight(self):
        self.assertEqual(pronounce_number(8, lang="id"), 'delapan')
        self.assertEqual(pronounce_number(8, lang="ms"), 'lapan')

    def test_zero(self):
        self.assertEqual(pronounce_number(0, lang="id"), 'nol')
        self.assertEqual(pronounce_number(0, lang="ms"), 'sifar')

    def test_each_standard_keeps_its_own_spelling(self):
        # each language understands its own form; the other's is not assumed
        self.assertEqual(extract_number('delapan', lang="id"), 8)
        self.assertEqual(extract_number('lapan', lang="ms"), 8)

    def test_billion_scale_word(self):
        self.assertEqual(pronounce_number(1000000000, lang="id"),
                         'satu miliar')
        self.assertEqual(pronounce_number(1000000000, lang="ms"),
                         'satu bilion')


class TestHelpers(unittest.TestCase):
    def test_is_fractional(self):
        for lang in ("id", "ms"):
            self.assertEqual(is_fractional('setengah', lang=lang), 0.5)
            self.assertEqual(is_fractional('seperempat', lang=lang), 0.25)
            self.assertFalse(is_fractional('kucing', lang=lang))

    def test_is_ordinal(self):
        for lang in ("id", "ms"):
            self.assertEqual(is_ordinal('kedua', lang=lang), 2)
            self.assertFalse(is_ordinal('kucing', lang=lang))

    def test_numbers_to_digits(self):
        for lang in ("id", "ms"):
            self.assertEqual(
                numbers_to_digits('dua puluh satu kucing', lang=lang),
                '21 kucing')


if __name__ == "__main__":
    unittest.main()
