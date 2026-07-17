import unittest

from ovos_number_parser import extract_number, pronounce_number, is_fractional


class TestCatalanPronounce(unittest.TestCase):
    """Anchors for spoken Catalan numbers."""

    def test_pronounce_number(self):
        expected = {0: 'zero', 1: 'un', 2: 'dos', 3: 'tres', 4: 'quatre', 5: 'cinc', 6: 'sis', 7: 'set', 8: 'vuit', 9: 'nou', 10: 'deu', 11: 'onze', 12: 'dotze', 13: 'tretze', 14: 'catorze', 15: 'quinze', 16: 'setze', 17: 'disset', 18: 'divuit', 19: 'dinou', 20: 'vint', 21: 'vint-i-un', 30: 'trenta', 42: 'quaranta-dos', 50: 'cinquanta', 66: 'seixanta-sis', 70: 'setanta', 80: 'vuitanta', 90: 'noranta', 99: 'noranta-nou', 100: 'cent', 101: 'cent un', 123: 'cent vint-i-tres', 200: 'dos-cents', 500: 'cinc-cents', 999: 'nou-cents noranta-nou', 1000: 'mil', 2000: 'dos mil', 2023: 'dos mil vint-i-tres', 1000000: 'un milió', 2000000: 'dos milions'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="ca"), spoken)

    def test_pronounce_negative_and_decimal(self):
        expected = {-7: 'menys set', -42: 'menys quaranta-dos', 2.5: 'dos coma cinc', 3.14: 'tres coma un quatre', -3.5: 'menys tres coma cinc', 0.5: 'zero coma cinc'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="ca"), spoken)


class TestCatalanExtract(unittest.TestCase):
    """Anchors for extracting numbers from Catalan text."""

    def test_extract_number(self):
        expected = {0: 'zero', 1: 'un', 2: 'dos', 3: 'tres', 4: 'quatre', 5: 'cinc', 6: 'sis', 7: 'set', 8: 'vuit', 9: 'nou', 10: 'deu', 11: 'onze', 12: 'dotze', 13: 'tretze', 14: 'catorze', 15: 'quinze', 16: 'setze', 17: 'disset', 18: 'divuit', 19: 'dinou', 20: 'vint', 21: 'vint-i-un', 30: 'trenta', 42: 'quaranta-dos', 50: 'cinquanta', 66: 'seixanta-sis', 70: 'setanta', 80: 'vuitanta', 90: 'noranta', 99: 'noranta-nou', 100: 'cent', 101: 'cent un', 123: 'cent vint-i-tres', 200: 'dos-cents', 500: 'cinc-cents', 999: 'nou-cents noranta-nou', 1000: 'mil', 2000: 'dos mil', 2023: 'dos mil vint-i-tres', 1000000: 'un milió', 2000000: 'dos milions'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="ca"), number)

    def test_extract_negative_and_decimal(self):
        expected = {-7: 'menys set', -42: 'menys quaranta-dos', 2.5: 'dos coma cinc', 3.14: 'tres coma un quatre', -3.5: 'menys tres coma cinc', 0.5: 'zero coma cinc'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="ca"), number)

    def test_extract_from_sentence(self):
        self.assertEqual(extract_number('tinc vint-i-un gats', lang="ca"),
                         21)

    def test_extract_scale_groups(self):
        # Exact written forms taken from the Consorci per a la Normalització
        # Lingüística grammar "6. Els numerals" (IEC normativa) and the Optimot
        # fitxa "Guionet en els numerals compostos": a hundreds group before a
        # scale word multiplies that scale word and the products are summed.
        expected = {
            'cinc-cents mil': 500000,
            'cent mil': 100000,
            'dos milions cent mil': 2100000,
            'dos milions cinc-cents mil': 2500000,
            'un milió dos-cents trenta-quatre mil sis-cents': 1234600,
            'dos milions cinc-cents seixanta-nou mil vuit-cents setanta-cinc':
                2569875,
            'mil cent': 1100,
        }
        for spoken, number in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="ca"), number)

    def test_no_number(self):
        self.assertIn(extract_number("hola com estàs", lang="ca"), (False, None))


class TestCatalanRoundTrip(unittest.TestCase):
    """pronounce_number output must be understood by extract_number."""

    def test_round_trip(self):
        for number in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 201, 222, 300, 345, 400, 456, 500, 678, 700, 891, 900, 1000, 1001, 1234, 2000, 2023, 5000, 9999, 10000, 100000, 1000000, 2000000, 2100000, 2500000, 3400000, 1500000,
                       2001500, 1234600, 2569875, 9999999]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="ca")
                self.assertEqual(extract_number(spoken, lang="ca"), number)

    def test_round_trip_negative_and_decimal(self):
        for number in [-7, -42, 2.5, 3.14, -3.5, 0.5]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="ca")
                self.assertEqual(extract_number(spoken, lang="ca"), number)


class TestCatalanFractions(unittest.TestCase):
    """Catalan fraction nouns, gendered/plural and capitalized forms."""

    def test_basic_and_inflected(self):
        self.assertEqual(is_fractional("mig", lang="ca"), 0.5)
        self.assertEqual(is_fractional("mitja", lang="ca"), 0.5)
        self.assertEqual(is_fractional("terç", lang="ca"), 1.0 / 3)
        self.assertEqual(is_fractional("quart", lang="ca"), 0.25)
        self.assertEqual(is_fractional("quarta", lang="ca"), 0.25)
        self.assertEqual(is_fractional("centè", lang="ca"), 0.01)

    def test_capitalized_input_does_not_crash(self):
        self.assertEqual(is_fractional("Mig", lang="ca"), 0.5)
        self.assertEqual(is_fractional("QUART", lang="ca"), 0.25)
        self.assertEqual(is_fractional("Centè", lang="ca"), 0.01)

    def test_non_fraction_returns_false(self):
        for word in ["", "hola", "cinc"]:
            with self.subTest(word=word):
                self.assertFalse(is_fractional(word, lang="ca"))


if __name__ == "__main__":
    unittest.main()
