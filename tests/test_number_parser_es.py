import unittest

from ovos_number_parser import extract_number, pronounce_number


class TestSpanishPronounce(unittest.TestCase):
    """Anchors for spoken Spanish numbers."""

    def test_pronounce_number(self):
        expected = {0: 'cero', 1: 'uno', 2: 'dos', 3: 'tres', 4: 'cuatro', 5: 'cinco', 6: 'seis', 7: 'siete', 8: 'ocho', 9: 'nueve', 10: 'diez', 11: 'once', 12: 'doce', 13: 'trece', 14: 'catorce', 15: 'quince', 16: 'dieciséis', 17: 'diecisiete', 18: 'dieciocho', 19: 'diecinueve', 20: 'veinte', 21: 'veintiuno', 30: 'treinta', 42: 'cuarenta y dos', 50: 'cincuenta', 66: 'sesenta y seis', 70: 'setenta', 80: 'ochenta', 90: 'noventa', 99: 'noventa y nueve', 100: 'cien', 101: 'ciento uno', 123: 'ciento veintitrés', 200: 'doscientos', 500: 'quinientos', 999: 'novecientos noventa y nueve', 1000: 'mil', 2000: 'dos mil', 2023: 'dos mil veintitrés', 1000000: 'un millón', 2000000: 'dos millones'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="es"), spoken)

    def test_pronounce_negative_and_decimal(self):
        expected = {-7: 'menos siete', -42: 'menos cuarenta y dos', 2.5: 'dos coma cinco', 3.14: 'tres coma uno cuatro', -3.5: 'menos tres coma cinco', 0.5: 'cero coma cinco'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="es"), spoken)


class TestSpanishExtract(unittest.TestCase):
    """Anchors for extracting numbers from Spanish text."""

    def test_extract_number(self):
        expected = {0: 'cero', 1: 'uno', 2: 'dos', 3: 'tres', 4: 'cuatro', 5: 'cinco', 6: 'seis', 7: 'siete', 8: 'ocho', 9: 'nueve', 10: 'diez', 11: 'once', 12: 'doce', 13: 'trece', 14: 'catorce', 15: 'quince', 16: 'dieciséis', 17: 'diecisiete', 18: 'dieciocho', 19: 'diecinueve', 20: 'veinte', 21: 'veintiuno', 30: 'treinta', 42: 'cuarenta y dos', 50: 'cincuenta', 66: 'sesenta y seis', 70: 'setenta', 80: 'ochenta', 90: 'noventa', 99: 'noventa y nueve', 100: 'cien', 101: 'ciento uno', 123: 'ciento veintitrés', 200: 'doscientos', 500: 'quinientos', 999: 'novecientos noventa y nueve', 1000: 'mil', 2000: 'dos mil', 2023: 'dos mil veintitrés', 1000000: 'un millón', 2000000: 'dos millones'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="es"), number)

    def test_extract_negative_and_decimal(self):
        expected = {-7: 'menos siete', -42: 'menos cuarenta y dos', 2.5: 'dos coma cinco', 3.14: 'tres coma uno cuatro', -3.5: 'menos tres coma cinco', 0.5: 'cero coma cinco'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="es"), number)

    def test_extract_from_sentence(self):
        self.assertEqual(extract_number('tengo veintiuno gatos', lang="es"),
                         21)

    def test_no_number(self):
        self.assertIn(extract_number("hola cómo estás", lang="es"), (False, None))


class TestSpanishRoundTrip(unittest.TestCase):
    """pronounce_number output must be understood by extract_number."""

    def test_round_trip(self):
        for number in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 201, 222, 300, 345, 400, 456, 500, 678, 700, 891, 900, 1000, 1001, 1234, 2000, 2023, 5000, 9999, 10000, 100000, 1000000, 2000000]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="es")
                self.assertEqual(extract_number(spoken, lang="es"), number)

    def test_round_trip_negative_and_decimal(self):
        for number in [-7, -42, 2.5, 3.14, -3.5, 0.5]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="es")
                self.assertEqual(extract_number(spoken, lang="es"), number)


if __name__ == "__main__":
    unittest.main()
