import unittest

from ovos_number_parser.util import GrammaticalGender
from ovos_number_parser.numbers_an import AN


# ============================================================
# Pronunciation Tests
# ============================================================

class TestPronunciationAN(unittest.TestCase):

    # --- Cardinal Pronunciation (up to 999) ---
    def test_units(self):
        self.assertEqual(AN.pronounce_number(0), "zero")
        self.assertEqual(AN.pronounce_number(1), "un")
        self.assertEqual(AN.pronounce_number(1, gender=GrammaticalGender.FEMININE), "una")
        self.assertEqual(AN.pronounce_number(4), "cuatre")
        self.assertEqual(AN.pronounce_number(7), "siet")
        self.assertEqual(AN.pronounce_number(8), "ueito")
        self.assertEqual(AN.pronounce_number(9), "nueu")

    def test_teens(self):
        self.assertEqual(AN.pronounce_number(12), "doce")
        self.assertEqual(AN.pronounce_number(14), "catorze")
        self.assertEqual(AN.pronounce_number(16), "deciséis")
        self.assertEqual(AN.pronounce_number(18), "deciueito")
        self.assertEqual(AN.pronounce_number(19), "decinueu")

    def test_composite_numbers(self):
        # 21-29 are written as one word
        self.assertEqual(AN.pronounce_number(21), "vintiún")
        self.assertEqual(AN.pronounce_number(25), "vinticinco")
        # from 30 on, tens and units join with "y"
        self.assertEqual(AN.pronounce_number(35), "trenta y cinco")
        self.assertEqual(AN.pronounce_number(48), "cuaranta y ueito")
        self.assertEqual(AN.pronounce_number(67), "sixanta y siet")
        self.assertEqual(AN.pronounce_number(99), "novanta y nueu")

    def test_hundreds(self):
        self.assertEqual(AN.pronounce_number(100), "cient")
        self.assertEqual(AN.pronounce_number(101), "ciento un")
        self.assertEqual(AN.pronounce_number(200), "docientos")
        self.assertEqual(AN.pronounce_number(500), "cincocientos")
        self.assertEqual(AN.pronounce_number(900), "noucientos")

    def test_thousands(self):
        self.assertEqual(AN.pronounce_number(1000), "mil")
        self.assertEqual(AN.pronounce_number(2000), "dos mil")

    def test_millions(self):
        self.assertEqual(AN.pronounce_number(1_000_000), "un millón")
        self.assertEqual(AN.pronounce_number(2_000_000), "dos millones")

    # --- Decimals and Negatives ---
    def test_decimals(self):
        self.assertEqual(AN.pronounce_number(10.05), "diez coma zero cinco")

    def test_negative(self):
        self.assertEqual(AN.pronounce_number(-7), "menos siet")

    # --- Ordinal Pronunciation ---
    def test_ordinals(self):
        self.assertEqual(AN.pronounce_ordinal(1), "primero")
        self.assertEqual(AN.pronounce_ordinal(1, GrammaticalGender.FEMININE), "primera")
        self.assertEqual(AN.pronounce_ordinal(2), "segundo")
        self.assertEqual(AN.pronounce_ordinal(3), "tercero")
        self.assertEqual(AN.pronounce_ordinal(4), "cuatreno")
        self.assertEqual(AN.pronounce_ordinal(5), "cinqueno")
        self.assertEqual(AN.pronounce_ordinal(8), "uiteno")
        self.assertEqual(AN.pronounce_ordinal(10), "deceno")

    # --- Fractions ---
    def test_fractions(self):
        self.assertEqual(AN.pronounce_fraction('1/2'), "un meyo")
        self.assertEqual(AN.pronounce_fraction('2/3'), "dos tercios")
        self.assertEqual(AN.pronounce_fraction('3/4'), "tres cuartos")


# ============================================================
# Extraction and Conversion Tests
# ============================================================

class TestExtractionAN(unittest.TestCase):

    def test_extraction_cardinal_gender(self):
        self.assertEqual(AN.extract_number('un'), 1)
        self.assertEqual(AN.extract_number('una'), 1)

    def test_extraction_composite(self):
        self.assertEqual(AN.extract_number('vintiún'), 21)
        self.assertEqual(AN.extract_number('trenta y cinco'), 35)
        self.assertEqual(AN.extract_number('novanta y nueu'), 99)

    def test_extraction_variant_spellings(self):
        # dialectal / variant spellings understood on extraction
        self.assertEqual(AN.extract_number('quatre'), 4)
        self.assertEqual(AN.extract_number('güeito'), 8)
        self.assertEqual(AN.extract_number('nou'), 9)
        self.assertEqual(AN.extract_number('vente'), 20)
        self.assertEqual(AN.extract_number('setse'), 16)
        self.assertEqual(AN.extract_number('noranta'), 90)

    def test_extraction_large_numbers(self):
        self.assertEqual(AN.extract_number('un millón'), 1_000_000)
        self.assertEqual(AN.extract_number('dos millones cincocientos'), 2_000_500)
        self.assertEqual(AN.extract_number('mil vinte y tres'), 1023)

    def test_extraction_ordinals(self):
        self.assertEqual(AN.extract_number('o segundo coche', ordinals=True), 2)
        self.assertEqual(AN.extract_number('a primera vegada', ordinals=True), 1)
        self.assertEqual(AN.extract_number('o cuatreno puesto', ordinals=True), 4)

    def test_no_number(self):
        self.assertFalse(AN.extract_number('xyzzy'))

    # --- Text to Digits Conversion ---
    def test_numbers_to_digits(self):
        self.assertEqual(AN.numbers_to_digits('docientos cincuanta'), '250')
        self.assertEqual(AN.numbers_to_digits('un millón'), '1000000')
        self.assertEqual(
            AN.numbers_to_digits('bi ha docientos cincuanta coches'),
            'bi ha 250 coches')


class TestRoundTripAN(unittest.TestCase):
    """pronounce_number output must be understood by extract_number."""

    def test_round_trip(self):
        numbers = list(range(0, 200)) + [
            201, 222, 300, 345, 400, 456, 500, 678, 700, 891, 900, 1000,
            1001, 1234, 2000, 2023, 5000, 9999, 10000, 100000, 1000000,
            2000000]
        for number in numbers:
            with self.subTest(number=number):
                spoken = AN.pronounce_number(number)
                self.assertEqual(AN.extract_number(spoken), number)


if __name__ == '__main__':
    unittest.main()
