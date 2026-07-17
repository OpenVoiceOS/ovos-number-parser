import unittest

from ovos_number_parser import extract_number, pronounce_number


class TestCzechPronounce(unittest.TestCase):
    """Anchors for spoken Czech numbers."""

    def test_pronounce_number(self):
        expected = {0: 'nula', 1: 'jedna', 2: 'dva', 3: 'tři', 4: 'čtyři', 5: 'pět', 6: 'šest', 7: 'sedm', 8: 'osm', 9: 'devět', 10: 'deset', 11: 'jedenáct', 12: 'dvanáct', 13: 'třináct', 14: 'čtrnáct', 15: 'patnáct', 16: 'šestnáct', 17: 'sedmnáct', 18: 'osmnáct', 19: 'devatenáct', 20: 'dvacet', 21: 'dvacet jedna', 30: 'třicet', 42: 'čtyřicet dva', 50: 'padesát', 66: 'šedesát šest', 70: 'sedmdesát', 80: 'osmdesát', 90: 'devadesát', 99: 'devadesát devět', 100: 'sto', 101: 'sto jedna', 123: 'sto dvacet tři', 200: 'dvě stě', 500: 'pět set', 999: 'devět set devadesát devět', 1000: 'tisíc', 2000: 'dva tisíc', 2023: 'dva tisíc, dvacet tři', 1000000: 'million', 2000000: 'dva million'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="cs"), spoken)

    def test_pronounce_negative_and_decimal(self):
        expected = {-7: 'mínus sedm', -42: 'mínus čtyřicet dva', 2.5: 'dva tečka pět', 3.14: 'tři tečka jedna čtyři', -3.5: 'mínus tři tečka pět', 0.5: 'nula tečka pět'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="cs"), spoken)


class TestCzechExtract(unittest.TestCase):
    """Anchors for extracting numbers from Czech text."""

    def test_extract_number(self):
        expected = {0: 'nula', 1: 'jedna', 2: 'dva', 3: 'tři', 4: 'čtyři', 5: 'pět', 6: 'šest', 7: 'sedm', 8: 'osm', 9: 'devět', 10: 'deset', 11: 'jedenáct', 12: 'dvanáct', 13: 'třináct', 14: 'čtrnáct', 15: 'patnáct', 16: 'šestnáct', 17: 'sedmnáct', 18: 'osmnáct', 19: 'devatenáct', 20: 'dvacet', 21: 'dvacet jedna', 30: 'třicet', 42: 'čtyřicet dva', 50: 'padesát', 66: 'šedesát šest', 70: 'sedmdesát', 80: 'osmdesát', 90: 'devadesát', 99: 'devadesát devět', 100: 'sto', 101: 'sto jedna', 123: 'sto dvacet tři', 200: 'dvě stě', 500: 'pět set', 999: 'devět set devadesát devět', 1000: 'tisíc', 2000: 'dva tisíc', 2023: 'dva tisíc, dvacet tři', 1000000: 'million', 2000000: 'dva million'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="cs"), number)

    def test_extract_negative_and_decimal(self):
        expected = {-7: 'mínus sedm', -42: 'mínus čtyřicet dva', 2.5: 'dva tečka pět', 3.14: 'tři tečka jedna čtyři', -3.5: 'mínus tři tečka pět', 0.5: 'nula tečka pět'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="cs"), number)

    def test_extract_from_sentence(self):
        self.assertEqual(extract_number('mám dvacet jedna koček', lang="cs"),
                         21)

    def test_no_number(self):
        self.assertIn(extract_number("ahoj jak se máš", lang="cs"), (False, None))


class TestCzechRoundTrip(unittest.TestCase):
    """pronounce_number output must be understood by extract_number."""

    def test_round_trip(self):
        for number in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 201, 222, 300, 345, 400, 456, 500, 678, 700, 891, 900, 1000, 1001, 2000, 2023, 5000, 9999, 10000, 100000, 1000000, 2000000]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="cs")
                self.assertEqual(extract_number(spoken, lang="cs"), number)

    def test_round_trip_negative_and_decimal(self):
        for number in [-7, -42, 2.5, 3.14, -3.5, 0.5]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="cs")
                self.assertEqual(extract_number(spoken, lang="cs"), number)


class TestCzechScaleWords(unittest.TestCase):
    """Descending scale words must add, not multiply."""

    def test_thousand_then_hundred(self):
        # "tisíc sto" = 1000 + 100, not 1000 * 100
        self.assertEqual(extract_number("tisíc sto", lang="cs"), 1100)
        self.assertEqual(extract_number("dva tisíce sto", lang="cs"), 2100)
        self.assertEqual(extract_number("dva tisíce sto dvacet tři", lang="cs"),
                         2123)
        self.assertEqual(extract_number("pět tisíc dvě stě", lang="cs"), 5200)

    def test_ascending_scale_still_multiplies(self):
        # "dvě stě" = 2 * 100, "sto tisíc" = 100 * 1000
        self.assertEqual(extract_number("dvě stě", lang="cs"), 200)
        self.assertEqual(extract_number("tři sta", lang="cs"), 300)
        self.assertEqual(extract_number("pět set", lang="cs"), 500)
        self.assertEqual(extract_number("sto tisíc", lang="cs"), 100000)
        self.assertEqual(extract_number("dva tisíce", lang="cs"), 2000)

    def test_declined_units_in_context(self):
        self.assertEqual(extract_number("mám dvě kočky", lang="cs"), 2)
        self.assertEqual(extract_number("nastav budík na pět hodin",
                                        lang="cs"), 5)
        self.assertEqual(extract_number("za deset minut", lang="cs"), 10)
        self.assertEqual(extract_number("jeden den", lang="cs"), 1)


class TestCzechNegatives(unittest.TestCase):
    """Both the diacritic and ASCII spellings of minus negate."""

    def test_minus_variants(self):
        self.assertEqual(extract_number("mínus pět", lang="cs"), -5)
        self.assertEqual(extract_number("minus pět", lang="cs"), -5)
        self.assertEqual(extract_number("záporné tři", lang="cs"), -3)
        self.assertEqual(extract_number("minus čtyřicet dva", lang="cs"), -42)


class TestCzechYearPronunciation(unittest.TestCase):
    """Czech speaks four-digit numbers with scale words, never digit pairs."""

    def test_no_digit_pair_years(self):
        # English "nineteen seventy two" style must not leak into Czech
        for number in (1010, 1100, 1234, 1972, 1999):
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="cs")
                self.assertIn("tisíc", spoken)
                self.assertEqual(extract_number(spoken, lang="cs"), number)


class TestCzechRoundTripSweep(unittest.TestCase):
    """A dense sweep guards the pronounce/extract contract."""

    def test_dense_sweep(self):
        for number in range(0, 3000):
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="cs")
                self.assertEqual(extract_number(spoken, lang="cs"), number)

    def test_sparse_large_sweep(self):
        for number in range(3000, 200001, 137):
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="cs")
                self.assertEqual(extract_number(spoken, lang="cs"), number)


class TestCzechAdversarial(unittest.TestCase):
    """Malformed and boundary inputs must not crash."""

    def test_empty_and_junk(self):
        for text in ("", "   ", "?!.", "žžž qwerty"):
            with self.subTest(text=text):
                self.assertIn(extract_number(text, lang="cs"), (False, None))

    def test_lang_code_variants(self):
        self.assertEqual(extract_number("dvacet jedna", lang="cs-cz"), 21)
        self.assertEqual(extract_number("dvacet jedna", lang="cs-CZ"), 21)

    def test_mixed_case(self):
        self.assertEqual(extract_number("Dvacet Jedna", lang="cs"), 21)


class TestCzechScaleAccumulation(unittest.TestCase):
    """Millions combined with thousands must accumulate correctly.

    Anchored on the Internetová jazyková příručka (ÚJČ AV ČR, §791): each
    numeral group is written as separate words and forms its own portion.
    """

    def test_million_plus_thousands_anchor(self):
        spoken = pronounce_number(8186976, lang="cs")
        self.assertEqual(extract_number(spoken, lang="cs"), 8186976)

    def test_million_thousand_hundred_round_trip(self):
        for number in [1000500, 1100000, 1200000, 1500000, 8186976,
                       2500000, 8100000, 9999999, 10000000, 1186976]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="cs")
                self.assertEqual(extract_number(spoken, lang="cs"), number)

    def test_negative_scale_round_trip(self):
        for number in [-9997, -1499, -1500000, -8186976, -104979, -1000500]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="cs")
                self.assertEqual(extract_number(spoken, lang="cs"), number)

    def test_property_round_trip_both_signs(self):
        for base in range(0, 10000001, 5417):
            for number in (base, -base):
                spoken = pronounce_number(number, lang="cs")
                self.assertEqual(extract_number(spoken, lang="cs"), number,
                                 msg=f"round-trip failed for {number}: {spoken!r}")


if __name__ == "__main__":
    unittest.main()
