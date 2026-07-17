import unittest
from ovos_number_parser.util import Scale, GrammaticalGender
from ovos_number_parser.numbers_gl import GL


# ============================================================
# Pronunciation Tests
# ============================================================

class TestPronunciationGL(unittest.TestCase):

    # --- Cardinal Pronunciation (up to 999) ---
    def test_units(self):
        self.assertEqual(GL.pronounce_number(1), "un")
        self.assertEqual(GL.pronounce_number(1, gender=GrammaticalGender.FEMININE), "unha")
        self.assertEqual(GL.pronounce_number(2), "dous")
        self.assertEqual(GL.pronounce_number(2, gender=GrammaticalGender.FEMININE), "dúas")

    def test_composite_numbers(self):
        self.assertEqual(GL.pronounce_number(16), "dezaseis")
        self.assertEqual(GL.pronounce_number(21), "vinte e un")
        self.assertEqual(GL.pronounce_number(22), "vinte e dous")
        self.assertEqual(GL.pronounce_number(22, gender=GrammaticalGender.FEMININE), "vinte e dúas")
        self.assertEqual(GL.pronounce_number(35), "trinta e cinco")
        self.assertEqual(GL.pronounce_number(99), "noventa e nove")

    def test_hundreds(self):
        # 100 uses different form for multiples
        self.assertEqual(GL.pronounce_number(100), "cen")
        # 101 uses a composite form
        self.assertEqual(GL.pronounce_number(101), "cento e un")
        # Multiples of 100 are gendered
        self.assertEqual(GL.pronounce_number(200), "douscentos")
        self.assertEqual(GL.pronounce_number(200, gender=GrammaticalGender.FEMININE), "douscentas")
        self.assertEqual(GL.pronounce_number(547), "cincocentos corenta e sete")
        self.assertEqual(GL.pronounce_number(999), "novecentos noventa e nove")

    # --- Large Number Pronunciation (Galician is Long Scale) ---
    def test_thousands(self):
        self.assertEqual(GL.pronounce_number(1000), "mil")
        self.assertEqual(GL.pronounce_number(2000), "dous mil")
        self.assertEqual(GL.pronounce_number(1234), "mil douscentos e trinta e catro")
        self.assertEqual(GL.pronounce_number(2001), "dous mil e un")

    def test_millions(self):
        # 1,000,000 should be 'un millón'
        self.assertEqual(GL.pronounce_number(1_000_000), "un millón")
        # 1,234,567 should be 'un millón...'
        self.assertEqual(GL.pronounce_number(1_234_567),
                         "un millón douscentos trinta e catro mil cincocentos sesenta e sete")
        self.assertEqual(GL.pronounce_number(2_000_000), "dous millóns")

    def test_long_scale_billions_trillions(self):
        # 10^9 (Galician: Mil millóns)
        self.assertEqual(GL.pronounce_number(1_000_000_000), "mil millóns")
        # 2,500,123,456
        expected = "dous mil cincocentos millóns cento vinte e tres mil catrocentos cincuenta e seis"
        self.assertEqual(GL.pronounce_number(2_500_123_456), expected)

        # 10^12 (Galician: Un billón)
        self.assertEqual(GL.pronounce_number(1_000_000_000_000), "un billón")

    # --- Decimals and Negatives ---
    def test_decimals(self):
        # Galician uses 'coma' (comma) for the decimal separator
        self.assertEqual(GL.pronounce_number(10.05), "dez coma cero cinco")
        self.assertEqual(GL.pronounce_number(123.45), "cento e vinte e tres coma corenta e cinco")

    def test_negative(self):
        self.assertEqual(GL.pronounce_number(-123.45),
                         "menos cento e vinte e tres coma corenta e cinco")

    # --- Ordinal Pronunciation ---
    def test_ordinals(self):
        self.assertEqual(GL.pronounce_number(1, ordinals=True, gender=GrammaticalGender.MASCULINE), "primeiro")
        self.assertEqual(GL.pronounce_number(1, ordinals=True, gender=GrammaticalGender.FEMININE), "primeira")
        self.assertEqual(GL.pronounce_number(23, ordinals=True), "vixésimo terceiro")
        self.assertEqual(GL.pronounce_number(23, ordinals=True, gender=GrammaticalGender.FEMININE), "vixésima terceira")
        self.assertEqual(GL.pronounce_number(100, ordinals=True), "centésimo")
        self.assertEqual(GL.pronounce_number(1_000_000, ordinals=True), "millonésimo")
        self.assertEqual(GL.pronounce_number(1_000_000_000_000, ordinals=True), "billonésimo")

    # --- Fractions ---
    def test_fractions(self):
        # $1/2$
        self.assertEqual(GL.pronounce_fraction('1/2'), "un medio")
        # $5/3$
        self.assertEqual(GL.pronounce_fraction('5/3'), "cinco terzos")
        # $7/10$
        self.assertEqual(GL.pronounce_fraction('7/10'), "sete décimos")
        # $0/20$
        self.assertEqual(GL.pronounce_fraction('0/20'), "cero vinteavos")


# ============================================================
# Extraction and Conversion Tests
# ============================================================

class TestExtractionGL(unittest.TestCase):

    # --- Cardinal Extraction ---
    def test_extraction_cardinal_gender(self):
        # 'un' -> 1
        self.assertEqual(GL.extract_number('un'), 1)
        # 'unha' -> 1 (Fixes the current 'False' error)
        self.assertEqual(GL.extract_number('unha'), 1)

    def test_extraction_composite(self):
        # 'vinte e un' -> 21
        self.assertEqual(GL.extract_number('vinte e un'), 21)
        # 'vinte e unha' -> 21 (Fixes the current '20' error)
        self.assertEqual(GL.extract_number('vinte e unha'), 21)
        # 'vinte e dúas' -> 22 (Fixes the current '20' error)
        self.assertEqual(GL.extract_number('vinte e dúas'), 22)

    def test_extraction_large_numbers(self):
        # 'un millón' -> 1000000
        self.assertEqual(GL.extract_number('un millón'), 1_000_000)
        # 'dous millóns cincocentos' -> 2,000,500 (Fixes the current '502' error)
        self.assertEqual(GL.extract_number('dous millóns cincocentos'), 2_000_500)
        # 'mil vinte e tres' -> 1023
        self.assertEqual(GL.extract_number('mil vinte e tres'), 1023)
        # 'trinta e cinco coma catro' -> 35.4
        self.assertEqual(GL.extract_number('trinta e cinco coma catro'), 35.4)

    # --- Ordinal Extraction ---
    def test_extraction_ordinals(self):
        # 'a sexagésima cuarta vez' -> 64 (Fixes the current '4' error)
        self.assertEqual(GL.extract_number('a sexaxésima cuarta vez', ordinals=True), 64)
        self.assertEqual(GL.extract_number('o segundo carro', ordinals=True), 2)
        self.assertEqual(GL.extract_number('a primeira vez', ordinals=True), 1)
        self.assertEqual(GL.extract_number('o milésimo día', ordinals=True), 1000)

    # --- Text to Digits Conversion ---
    def test_numbers_to_digits(self):
        # Simple numbers
        self.assertEqual(GL.numbers_to_digits('douscentos cincuenta'), '250')
        self.assertEqual(GL.numbers_to_digits('un millón'), '1000000')

        # Numbers within a phrase
        phrase = 'hai douscentos cincuenta carros'
        self.assertEqual(GL.numbers_to_digits(phrase), 'hai 250 carros')

        # Test large numbers in phrase
        phrase_large = 'atopamos dous millóns cincocentos insectos'
        self.assertEqual(GL.numbers_to_digits(phrase_large), 'atopamos 2000500 insectos')


# ============================================================
# Adversarial / robustness tests
# ============================================================

class TestAdversarialGL(unittest.TestCase):

    def test_empty_and_junk(self):
        self.assertFalse(GL.extract_number(''))
        self.assertFalse(GL.extract_number('   '))
        self.assertFalse(GL.extract_number('lalala'))
        self.assertFalse(GL.extract_number('pon a mesa'))

    def test_zero(self):
        self.assertEqual(GL.pronounce_number(0), "cero")
        self.assertEqual(GL.extract_number('cero'), 0)

    def test_mixed_case(self):
        self.assertEqual(GL.extract_number('VINTE E UN'), 21)
        self.assertEqual(GL.extract_number('Vinte E Un'), 21)
        self.assertEqual(GL.extract_number('MAIÚSCULAS vinte e dous'), 22)

    def test_number_in_sentence(self):
        self.assertEqual(GL.extract_number('hai corenta e dous carros'), 42)
        self.assertEqual(GL.extract_number('quero cen mil euros'), 100000)

    def test_divided_by_zero_is_galician(self):
        # Galician zero is "cero", never Portuguese "zero"
        self.assertEqual(GL.pronounce_fraction('1/0'), "un a dividir por cero")
        self.assertEqual(GL.pronounce_fraction('5/0'), "cinco a dividir por cero")

    def test_gender_two_swap(self):
        self.assertEqual(GL.pronounce_number(2), "dous")
        self.assertEqual(GL.pronounce_number(2, gender=GrammaticalGender.FEMININE), "dúas")


class TestGalicianQuirksGL(unittest.TestCase):

    def test_cen_vs_cento(self):
        # bare hundred is "cen", composite uses "cento"
        self.assertEqual(GL.pronounce_number(100), "cen")
        self.assertEqual(GL.pronounce_number(101), "cento e un")
        self.assertEqual(GL.extract_number('cen'), 100)
        self.assertEqual(GL.extract_number('cento e un'), 101)

    def test_e_joiner_forties(self):
        self.assertEqual(GL.pronounce_number(42), "corenta e dous")
        self.assertEqual(GL.extract_number('corenta e dous'), 42)

    def test_gendered_hundreds(self):
        self.assertEqual(GL.pronounce_number(200), "douscentos")
        self.assertEqual(GL.pronounce_number(200, gender=GrammaticalGender.FEMININE), "douscentas")
        self.assertEqual(GL.extract_number('douscentas'), 200)

    def test_million_plural(self):
        self.assertEqual(GL.pronounce_number(1_000_000), "un millón")
        self.assertEqual(GL.pronounce_number(2_000_000), "dous millóns")
        self.assertEqual(GL.extract_number('dous millóns'), 2_000_000)

    def test_half_and_fractions_in_text(self):
        self.assertEqual(GL.extract_number('un millón e medio'), 1_000_000.5)
        self.assertEqual(GL.extract_number('tres cuartos'), 0.75)


class TestRoundTripGL(unittest.TestCase):

    def test_cardinal_sweep(self):
        for n in range(0, 1001):
            spoken = GL.pronounce_number(n)
            self.assertEqual(GL.extract_number(spoken), n,
                             f"round-trip failed for {n}: {spoken!r}")

    def test_large_round_trip(self):
        for n in [1000, 2000, 10000, 100000, 999999, 1_000_000,
                  2_000_000, 1_234_567, 1_000_000_000, 1_000_000_000_000,
                  3_000_500, 1_000_001]:
            spoken = GL.pronounce_number(n)
            self.assertEqual(GL.extract_number(spoken), n,
                             f"round-trip failed for {n}: {spoken!r}")

    def test_ordinal_round_trip(self):
        for n in [1, 2, 3, 10, 20, 21, 23, 100, 1000, 1_000_000]:
            spoken = GL.pronounce_number(n, ordinals=True)
            self.assertEqual(GL.extract_number(spoken, ordinals=True), n,
                             f"ordinal round-trip failed for {n}: {spoken!r}")

    def test_feminine_round_trip(self):
        for n in [1, 2, 21, 22, 200]:
            spoken = GL.pronounce_number(n, gender=GrammaticalGender.FEMININE)
            self.assertEqual(GL.extract_number(spoken), n,
                             f"feminine round-trip failed for {n}: {spoken!r}")

    def test_decimal_round_trip(self):
        for v in [0.5, 1.5, 3.14, 10.05, 100.001]:
            spoken = GL.pronounce_number(v)
            self.assertAlmostEqual(GL.extract_number(spoken), v, places=5,
                                   msg=f"decimal round-trip failed for {v}: {spoken!r}")

    def test_negative_round_trip(self):
        for v in [-7, -42, -123.45]:
            spoken = GL.pronounce_number(v)
            self.assertAlmostEqual(GL.extract_number(spoken), v, places=5,
                                   msg=f"negative round-trip failed for {v}: {spoken!r}")


if __name__ == '__main__':
    unittest.main()