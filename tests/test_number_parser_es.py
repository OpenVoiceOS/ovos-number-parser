import unittest

from ovos_number_parser import extract_number, pronounce_number, is_fractional
from ovos_number_parser.util import Scale


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


class TestSpanishMagnitudes(unittest.TestCase):
    """Compound scale numbers must combine, not multiply, across magnitudes."""

    def test_million_plus_thousand(self):
        cases = {
            "un millón dos mil": 1002000,
            "un millón dos mil quinientos": 1002500,
            "un millón cien mil": 1100000,
            "dos millones quinientos mil": 2500000,
            "tres millones dos mil": 3002000,
            "un millón uno": 1000001,
            "un millón dos mil trescientos cuarenta y cinco": 1002345,
        }
        for spoken, value in cases.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="es"), value)

    def test_thousands(self):
        cases = {
            "mil": 1000, "mil uno": 1001, "mil y uno": 1001,
            "dos mil veintitrés": 2023, "cien mil": 100000,
            "doscientos mil": 200000, "ciento cincuenta mil": 150000,
            "novecientos noventa y nueve mil novecientos noventa y nueve": 999999,
        }
        for spoken, value in cases.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="es"), value)

    def test_hundreds_gendered(self):
        for spoken in ("doscientos", "doscientas"):
            self.assertEqual(extract_number(spoken, lang="es"), 200)
        self.assertEqual(extract_number("doscientas cincuenta y dos", lang="es"), 252)


class TestSpanishFusedAndGendered(unittest.TestCase):
    def test_veintiuno_forms(self):
        for spoken in ("veintiuno", "veintiún", "veintiuna"):
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="es"), 21)

    def test_una(self):
        self.assertEqual(extract_number("una", lang="es"), 1)

    def test_cien_vs_ciento(self):
        self.assertEqual(extract_number("cien", lang="es"), 100)
        self.assertEqual(extract_number("ciento", lang="es"), 100)
        self.assertEqual(extract_number("ciento uno", lang="es"), 101)


class TestSpanishFractions(unittest.TestCase):
    def test_simple_fractions(self):
        self.assertEqual(extract_number("un cuarto", lang="es"), 0.25)
        self.assertEqual(extract_number("tres cuartos", lang="es"), 0.75)
        self.assertEqual(extract_number("medio", lang="es"), 0.5)

    def test_number_and_half(self):
        # nice_number renders 5.5 as "cinco y medio"
        self.assertEqual(extract_number("cinco y medio", lang="es"), 5.5)
        self.assertEqual(extract_number("dos y medio", lang="es"), 2.5)


class TestSpanishAdversarial(unittest.TestCase):
    def test_empty(self):
        self.assertFalse(extract_number("", lang="es"))

    def test_none(self):
        self.assertFalse(extract_number(None, lang="es"))

    def test_junk(self):
        self.assertIn(extract_number("hola qué tal amigo", lang="es"), (False, None))

    def test_mixed_case(self):
        self.assertEqual(extract_number("Cuarenta Y Dos", lang="es"), 42)

    def test_number_in_sentence(self):
        self.assertEqual(extract_number("quiero cuarenta y dos manzanas", lang="es"), 42)

    def test_negative_and_decimal(self):
        self.assertEqual(extract_number("menos cinco", lang="es"), -5)
        self.assertEqual(extract_number("tres coma uno cuatro", lang="es"), 3.14)


class TestSpanishRoundTripLarge(unittest.TestCase):
    """Sweep a wide integer range plus compound magnitudes."""

    def test_sweep(self):
        numbers = list(range(0, 3000, 7)) + [
            5000, 9999, 12345, 100000, 250000, 999999,
            1000000, 1000001, 1002000, 1002345, 2000000,
            2500000, 3002000, 1100000, 1234567,
        ]
        for number in numbers:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="es")
                got = extract_number(spoken, lang="es")
                if number == 0:
                    self.assertIn(got, (0, False))
                else:
                    self.assertEqual(got, number, spoken)


class TestSpanishFractions(unittest.TestCase):
    """Spanish fraction nouns, including gendered and capitalized forms."""

    def test_basic_and_gendered(self):
        self.assertEqual(is_fractional("medio", lang="es"), 0.5)
        self.assertEqual(is_fractional("media", lang="es"), 0.5)
        self.assertEqual(is_fractional("tercio", lang="es"), 1.0 / 3)
        self.assertEqual(is_fractional("cuarta", lang="es"), 0.25)
        self.assertEqual(is_fractional("centésima", lang="es"), 0.01)

    def test_capitalized_input_does_not_crash(self):
        # a sentence-initial or shouted fraction must not raise
        self.assertEqual(is_fractional("Medio", lang="es"), 0.5)
        self.assertEqual(is_fractional("MEDIO", lang="es"), 0.5)
        self.assertEqual(is_fractional("Centésimo", lang="es"), 0.01)

    def test_non_fraction_returns_false(self):
        for word in ["", "hola", "cinco"]:
            with self.subTest(word=word):
                self.assertFalse(is_fractional(word, lang="es"))


class TestSpanishLongScale(unittest.TestCase):
    """Spanish is a long-scale language: billón = 10^12, millardo = 10^9.

    See https://en.wikipedia.org/wiki/Long_and_short_scales.
    """

    def test_long_scale_words_extract(self):
        cases = {
            "un millón": 10 ** 6,
            "un millardo": 10 ** 9,
            "un billón": 10 ** 12,
            "dos billones": 2 * 10 ** 12,
            "tres billones": 3 * 10 ** 12,
        }
        for spoken, value in cases.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(
                    extract_number(spoken, lang="es", scale=Scale.LONG), value)

    def test_short_scale_billon_is_1e9(self):
        # under the short scale, "billón" means 10^9, not 10^12
        self.assertEqual(
            extract_number("un billón", lang="es", scale=Scale.SHORT), 10 ** 9)

    def test_pronounce_to_extract_roundtrip_long(self):
        for magnitude in (10 ** 6, 10 ** 9, 10 ** 12):
            with self.subTest(magnitude=magnitude):
                spoken = pronounce_number(magnitude, lang="es", scale=Scale.LONG)
                self.assertEqual(
                    extract_number(spoken, lang="es", scale=Scale.LONG),
                    magnitude, spoken)

    def test_extract_to_pronounce_roundtrip_long(self):
        for spoken in ("un millón", "un millardo", "un billón"):
            with self.subTest(spoken=spoken):
                value = extract_number(spoken, lang="es", scale=Scale.LONG)
                self.assertEqual(
                    pronounce_number(value, lang="es", scale=Scale.LONG), spoken)

    def test_scale_default_short_still_reads_million(self):
        # unrelated smaller magnitudes must not regress on either scale
        for scale in (Scale.SHORT, Scale.LONG):
            with self.subTest(scale=scale):
                self.assertEqual(
                    extract_number("un millón", lang="es", scale=scale), 10 ** 6)

    def test_boundary_billon_not_confused_with_millardo(self):
        # long scale: millardo (10^9) and billón (10^12) are distinct
        self.assertNotEqual(
            extract_number("un millardo", lang="es", scale=Scale.LONG),
            extract_number("un billón", lang="es", scale=Scale.LONG))

    def test_bare_scale_word_without_multiplier(self):
        # "billón" with no leading unit implies one
        self.assertEqual(
            extract_number("billón", lang="es", scale=Scale.LONG), 10 ** 12)


class TestSpanishTinyFloatNoCrash(unittest.TestCase):
    """Scientific-notation floats must not raise when pronounced."""

    def test_tiny_float_does_not_crash(self):
        for number in (1e-9, -1e-9, 1e-12, 1e20):
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="es")
                self.assertIsInstance(spoken, str)
                self.assertTrue(spoken)

    def test_ordinary_decimal_unregressed(self):
        self.assertEqual(pronounce_number(5.2, lang="es"), "cinco coma dos")


if __name__ == "__main__":
    unittest.main()
