import unittest

from ovos_number_parser import extract_number, pronounce_number
from ovos_number_parser.numbers_az import (
    pronounce_number_az,
    extract_number_az,
    nice_number_az,
    is_fractional_az,
    _get_ordinal_ak,
)


class TestAzerbaijaniPronounce(unittest.TestCase):
    """Anchors for spoken Azerbaijani numbers."""

    def test_pronounce_number(self):
        expected = {0: 'sıfır', 1: 'bir', 2: 'iki', 3: 'üç', 4: 'dörd', 5: 'beş', 6: 'altı', 7: 'yeddi', 8: 'səkkiz', 9: 'doqquz', 10: 'on', 11: 'on bir', 12: 'on iki', 13: 'on üç', 14: 'on dörd', 15: 'on beş', 16: 'on altı', 17: 'on yeddi', 18: 'on səkkiz', 19: 'on doqquz', 20: 'iyirmi', 21: 'iyirmi bir', 30: 'otuz', 42: 'qırx iki', 50: 'əlli', 66: 'altmış altı', 70: 'yetmiş', 80: 'səksən', 90: 'doxsan', 99: 'doxsan doqquz', 100: 'yüz', 101: 'yüz bir', 123: 'yüz iyirmi üç', 200: 'iki yüz', 500: 'beş yüz', 999: 'doqquz yüz doxsan doqquz', 1000: 'min', 2000: 'iki min', 2023: 'iki min, iyirmi üç', 1000000: 'bir milyon', 2000000: 'iki milyon'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="az"), spoken)

    def test_pronounce_negative_and_decimal(self):
        expected = {-7: 'mənfi yeddi', -42: 'mənfi qırx iki', 2.5: 'iki nöqtə beş', 3.14: 'üç nöqtə bir dörd', -3.5: 'mənfi üç nöqtə beş', 0.5: 'sıfır nöqtə beş'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="az"), spoken)


class TestAzerbaijaniExtract(unittest.TestCase):
    """Anchors for extracting numbers from Azerbaijani text."""

    def test_extract_number(self):
        expected = {0: 'sıfır', 1: 'bir', 2: 'iki', 3: 'üç', 4: 'dörd', 5: 'beş', 6: 'altı', 7: 'yeddi', 8: 'səkkiz', 9: 'doqquz', 10: 'on', 11: 'on bir', 12: 'on iki', 13: 'on üç', 14: 'on dörd', 15: 'on beş', 16: 'on altı', 17: 'on yeddi', 18: 'on səkkiz', 19: 'on doqquz', 20: 'iyirmi', 21: 'iyirmi bir', 30: 'otuz', 42: 'qırx iki', 50: 'əlli', 66: 'altmış altı', 70: 'yetmiş', 80: 'səksən', 90: 'doxsan', 99: 'doxsan doqquz', 100: 'yüz', 101: 'yüz bir', 123: 'yüz iyirmi üç', 200: 'iki yüz', 500: 'beş yüz', 999: 'doqquz yüz doxsan doqquz', 1000: 'min', 2000: 'iki min', 2023: 'iki min, iyirmi üç', 1000000: 'bir milyon', 2000000: 'iki milyon'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="az"), number)

    def test_extract_negative_and_decimal(self):
        expected = {-7: 'mənfi yeddi', -42: 'mənfi qırx iki', 2.5: 'iki nöqtə beş', 3.14: 'üç nöqtə bir dörd', -3.5: 'mənfi üç nöqtə beş', 0.5: 'sıfır nöqtə beş'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="az"), number)

    def test_extract_from_sentence(self):
        self.assertEqual(extract_number('mənim iyirmi bir pişiyim var', lang="az"),
                         21)

    def test_no_number(self):
        self.assertIn(extract_number("salam necəsən", lang="az"), (False, None))


class TestAzerbaijaniRoundTrip(unittest.TestCase):
    """pronounce_number output must be understood by extract_number."""

    def test_round_trip(self):
        for number in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 201, 222, 300, 345, 400, 456, 500, 678, 700, 891, 900, 1000, 1001, 1234, 2000, 2023, 5000, 9999, 10000, 100000, 1000000, 2000000]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="az")
                self.assertEqual(extract_number(spoken, lang="az"), number)

    def test_round_trip_negative_and_decimal(self):
        for number in [-7, -42, 2.5, 3.14, -3.5, 0.5]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="az")
                self.assertEqual(extract_number(spoken, lang="az"), number)


class TestAzerbaijaniOrdinals(unittest.TestCase):
    """Ordinal (sıra sayı) pronunciation and extraction."""

    def test_pronounce_ordinal_base(self):
        # ordinal suffix follows vowel harmony of the numeral stem
        expected = {
            1: 'birinci', 2: 'ikinci', 3: 'üçüncü', 4: 'dördüncü',
            5: 'beşinci', 6: 'altıncı', 7: 'yeddinci', 8: 'səkkizinci',
            9: 'doqquzuncu', 10: 'onuncu', 11: 'on birinci', 20: 'iyirminci',
            21: 'iyirmi birinci', 100: 'yüzüncü', 1000: 'mininci',
        }
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number_az(number, ordinals=True),
                                 spoken)

    def test_pronounce_ordinal_large_no_crash(self):
        # regression: large ordinals used to raise KeyError
        expected_short = {
            1000000: 'milyonuncu',
            2000000: 'iki milyonuncu',
            3000000: 'üç milyonuncu',
            1000000000: 'milyardıncı',
            2000000000: 'iki milyardıncı',
        }
        for number, spoken in expected_short.items():
            with self.subTest(number=number, scale="short"):
                self.assertEqual(
                    pronounce_number_az(number, ordinals=True), spoken)

    def test_pronounce_ordinal_large_long_scale_no_crash(self):
        # long scale must also not raise for millions and beyond
        for number in [1000000, 2000000, 1000000000, 1000000000000]:
            with self.subTest(number=number, scale="long"):
                result = pronounce_number_az(
                    number, ordinals=True, short_scale=False)
                self.assertIsInstance(result, str)
                self.assertTrue(result)

    def test_extract_ordinal(self):
        expected = {
            'birinci': 1, 'ikinci': 2, 'üçüncü': 3, 'onuncu': 10,
            'iyirminci': 20,
        }
        for spoken, number in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(
                    extract_number_az(spoken, ordinals=True), number)

    def test_ordinal_ignored_without_flag(self):
        # without ordinals flag, a lone ordinal is not read as a number
        self.assertIn(extract_number_az('birinci'), (False, None, 1))


class TestAzerbaijaniHelpers(unittest.TestCase):
    """Direct checks of the vowel-harmony helper used for ordinal suffixes."""

    def test_get_ordinal_ak_vowel_harmony(self):
        # suffix chosen by the last vowel class of the stem
        self.assertEqual(_get_ordinal_ak('min'), 'inci')    # i -> inci
        self.assertEqual(_get_ordinal_ak('yüz'), 'üncü')    # ü -> üncü
        self.assertEqual(_get_ordinal_ak('altmış'), 'ıncı')  # ı -> ıncı
        self.assertEqual(_get_ordinal_ak('doqquz'), 'uncu')  # u -> uncu

    def test_get_ordinal_ak_no_vowel(self):
        self.assertEqual(_get_ordinal_ak(''), '')


class TestAzerbaijaniNiceNumber(unittest.TestCase):
    """Human-friendly fraction rendering."""

    def test_nice_number_speech(self):
        expected = {
            4.5: '4 yarım',
            0.5: 'yarım',
            1.5: '1 yarım',
            3.25: '3 və dörddə 1',
            6.0: '6',
        }
        for number, text in expected.items():
            with self.subTest(number=number):
                self.assertEqual(nice_number_az(number), text)

    def test_nice_number_display(self):
        self.assertEqual(nice_number_az(4.5, speech=False), '4 1/2')
        self.assertEqual(nice_number_az(3.25, speech=False), '3 1/4')
        self.assertEqual(nice_number_az(6.0, speech=False), '6')


class TestAzerbaijaniSentences(unittest.TestCase):
    """Numbers embedded in natural Azerbaijani sentences."""

    def test_sentences(self):
        expected = {
            'mənim iyirmi bir pişiyim var': 21,
            'saat üç oldu': 3,
            'yüz iyirmi üç manat lazımdır': 123,
            'iki min iyirmi üç il': 2023,
            'səbətdə altmış altı alma var': 66,
            'doqquz yüz doxsan doqquz nəfər': 999,
            'beş yüz metr qaç': 500,
        }
        for text, number in expected.items():
            with self.subTest(text=text):
                self.assertEqual(extract_number_az(text), number)

    def test_fraction_words(self):
        # "dörddə üç" = in four, three = three quarters
        self.assertEqual(extract_number_az('dörddə üç'), 0.75)
        self.assertEqual(extract_number_az('dörddə bir'), 0.25)

    def test_half_word(self):
        self.assertEqual(extract_number_az('yarım'), 0.5)
        self.assertEqual(extract_number_az('iki yarım'), 2.5)

    def test_slash_fraction(self):
        self.assertEqual(extract_number_az('1/2'), 0.5)
        self.assertEqual(extract_number_az('3/4'), 0.75)


class TestAzerbaijaniAdversarial(unittest.TestCase):
    """Malformed, empty, boundary and junk input must not crash or over-read."""

    def test_empty_and_whitespace(self):
        for text in ['', '   ', '\t\n']:
            with self.subTest(text=repr(text)):
                self.assertIn(extract_number_az(text), (False, None))

    def test_junk(self):
        for text in ['salam necəsən', 'xyz', 'foo bar baz', '!!!', '.,;']:
            with self.subTest(text=text):
                self.assertIn(extract_number_az(text), (False, None))

    def test_none_raises_type_error(self):
        # None is not a valid input; it must fail loudly rather than silently
        with self.assertRaises((TypeError, AttributeError)):
            extract_number_az(None)

    def test_mixed_case(self):
        self.assertEqual(extract_number_az('Iyirmi Bir'), 21)
        self.assertEqual(extract_number_az('Doqquz Yüz'), 900)

    def test_lang_code_variants(self):
        for lang in ['az', 'az-az', 'az-AZ']:
            with self.subTest(lang=lang):
                self.assertEqual(
                    extract_number('iyirmi bir', lang=lang), 21)

    def test_zero(self):
        self.assertEqual(extract_number_az('sıfır'), 0)
        self.assertEqual(pronounce_number_az(0), 'sıfır')

    def test_boundary_pronounce_no_crash(self):
        # sweep a wide range including boundaries in both scales
        for number in [0, 99, 100, 999, 1000, 9999, 10 ** 6, 10 ** 12,
                       10 ** 33, -1, -1000000]:
            for short in (True, False):
                with self.subTest(number=number, short=short):
                    result = pronounce_number_az(number, short_scale=short)
                    self.assertIsInstance(result, str)
                    self.assertTrue(result)

    def test_decimal_places(self):
        # extra decimal digits truncated to requested places
        self.assertEqual(pronounce_number_az(3.14159, places=2),
                         'üç nöqtə bir dörd')
        self.assertEqual(pronounce_number_az(1.5, places=0), 'bir')


class TestAzerbaijaniRoundTripSweep(unittest.TestCase):
    """Exhaustive round trip over a wide range and both scales."""

    def test_round_trip_dense(self):
        numbers = list(range(0, 1000)) + [
            1000, 1001, 1234, 2023, 9999, 12345, 54321, 100000, 999999,
            1000000, 2000000, 2500000, 1000000000]
        for number in numbers:
            with self.subTest(number=number):
                spoken = pronounce_number_az(number)
                self.assertEqual(extract_number_az(spoken), number)

    def test_round_trip_long_scale(self):
        for number in [0, 1, 42, 100, 999, 1000, 2023, 1000000, 2000000]:
            with self.subTest(number=number):
                spoken = pronounce_number_az(number, short_scale=False)
                self.assertEqual(
                    extract_number_az(spoken, short_scale=False), number)

    def test_round_trip_negatives(self):
        for number in range(-99, 0):
            with self.subTest(number=number):
                spoken = pronounce_number_az(number)
                self.assertEqual(extract_number_az(spoken), number)


class TestAzerbaijaniScaleAccumulation(unittest.TestCase):
    """Millions combined with thousands must accumulate correctly.

    Anchored on standard Azerbaijani cardinal structure (yüz, min, milyon as
    separate words; "Say (dilçilik)", az.wikipedia).
    """

    def test_million_plus_thousands_anchor(self):
        spoken = pronounce_number_az(8186976)
        self.assertEqual(extract_number_az(spoken), 8186976)

    def test_million_thousand_hundred_round_trip(self):
        for number in [1000976, 1100000, 1200000, 1500000, 8186976,
                       2500000, 8100000, 9999999, 10000000, 1186976]:
            with self.subTest(number=number):
                spoken = pronounce_number_az(number)
                self.assertEqual(extract_number_az(spoken), number)

    def test_negative_scale_round_trip(self):
        for number in [-9997, -104979, -1500000, -8186976, -1000976]:
            with self.subTest(number=number):
                spoken = pronounce_number_az(number)
                self.assertEqual(extract_number_az(spoken), number)

    def test_property_round_trip_both_signs(self):
        for base in range(0, 10000001, 5417):
            for number in (base, -base):
                spoken = pronounce_number_az(number)
                self.assertEqual(extract_number_az(spoken), number,
                                 msg=f"round-trip failed for {number}: {spoken!r}")


if __name__ == "__main__":
    unittest.main()
