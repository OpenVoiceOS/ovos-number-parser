import unittest

from ovos_number_parser import extract_number, pronounce_number


class TestItalianPronounce(unittest.TestCase):
    """Anchors for spoken Italian numbers."""

    def test_pronounce_number(self):
        expected = {0: 'zero', 1: 'uno', 2: 'due', 3: 'tre', 4: 'quattro', 5: 'cinque', 6: 'sei', 7: 'sette', 8: 'otto', 9: 'nove', 10: 'dieci', 11: 'undici', 12: 'dodici', 13: 'tredici', 14: 'quattordici', 15: 'quindici', 16: 'sedici', 17: 'diciassette', 18: 'diciotto', 19: 'diciannove', 20: 'venti', 21: 'ventuno', 30: 'trenta', 42: 'quarantadue', 50: 'cinquanta', 66: 'sessantasei', 70: 'settanta', 80: 'ottanta', 90: 'novanta', 99: 'novantanove', 100: 'cento', 101: 'cento uno', 123: 'cento ventitré', 200: 'duecento', 500: 'cinquecento', 999: 'novecento novantanove', 1000: 'mille', 2000: 'duemila', 2023: 'duemila, ventitré', 1000000: 'un milione', 2000000: 'due milioni'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="it"), spoken)

    def test_pronounce_negative_and_decimal(self):
        expected = {-7: 'meno sette', -42: 'meno quarantadue', 2.5: 'due virgola cinque', 3.14: 'tre virgola uno quattro', -3.5: 'meno tre virgola cinque', 0.5: 'zero virgola cinque'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="it"), spoken)


class TestItalianExtract(unittest.TestCase):
    """Anchors for extracting numbers from Italian text."""

    def test_extract_number(self):
        expected = {0: 'zero', 1: 'uno', 2: 'due', 3: 'tre', 4: 'quattro', 5: 'cinque', 6: 'sei', 7: 'sette', 8: 'otto', 9: 'nove', 10: 'dieci', 11: 'undici', 12: 'dodici', 13: 'tredici', 14: 'quattordici', 15: 'quindici', 16: 'sedici', 17: 'diciassette', 18: 'diciotto', 19: 'diciannove', 20: 'venti', 21: 'ventuno', 30: 'trenta', 42: 'quarantadue', 50: 'cinquanta', 66: 'sessantasei', 70: 'settanta', 80: 'ottanta', 90: 'novanta', 99: 'novantanove', 100: 'cento', 101: 'cento uno', 123: 'cento ventitré', 200: 'duecento', 500: 'cinquecento', 999: 'novecento novantanove', 1000: 'mille', 2000: 'duemila', 2023: 'duemila, ventitré', 1000000: 'un milione', 2000000: 'due milioni'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="it"), number)

    def test_extract_negative_and_decimal(self):
        expected = {-7: 'meno sette', -42: 'meno quarantadue', 2.5: 'due virgola cinque', 3.14: 'tre virgola uno quattro', -3.5: 'meno tre virgola cinque', 0.5: 'zero virgola cinque'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="it"), number)

    def test_extract_from_sentence(self):
        self.assertEqual(extract_number('ho ventuno gatti', lang="it"),
                         21)

    def test_no_number(self):
        self.assertIn(extract_number("ciao come stai", lang="it"), (False, None))


class TestItalianRoundTrip(unittest.TestCase):
    """pronounce_number output must be understood by extract_number."""

    def test_round_trip(self):
        for number in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 201, 222, 300, 345, 400, 456, 500, 678, 700, 891, 900, 1000, 1001, 1234, 2000, 2023, 5000, 9999, 10000, 100000, 1000000, 2000000]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="it")
                self.assertEqual(extract_number(spoken, lang="it"), number)

    def test_round_trip_negative_and_decimal(self):
        for number in [-7, -42, 2.5, 3.14, -3.5, 0.5]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="it")
                self.assertEqual(extract_number(spoken, lang="it"), number)


class TestItalianFusedCompounds(unittest.TestCase):
    """Vowel elision and accented endings in fused Italian numerals."""

    def test_elided_units_in_tens(self):
        # -uno and -otto drop the tens vowel
        expected = {'ventuno': 21, 'ventotto': 28, 'trentuno': 31,
                    'trentotto': 38, 'quarantuno': 41, 'quarantotto': 48,
                    'cinquantuno': 51, 'cinquantotto': 58, 'sessantuno': 61,
                    'sessantotto': 68, 'settantuno': 71, 'settantotto': 78,
                    'ottantuno': 81, 'ottantotto': 88, 'novantuno': 91,
                    'novantotto': 98}
        for word, number in expected.items():
            with self.subTest(word=word):
                self.assertEqual(extract_number(word, lang="it"), number)

    def test_accented_tre_endings(self):
        # tré carries an accent in every fused form; both spellings are valid
        expected = {'ventitré': 23, 'trentatré': 33, 'quarantatré': 43,
                    'cinquantatré': 53, 'sessantatré': 63, 'settantatré': 73,
                    'ottantatré': 83, 'novantatré': 93, 'centotré': 103,
                    'duecentotré': 203}
        for word, number in expected.items():
            with self.subTest(word=word):
                self.assertEqual(extract_number(word, lang="it"), number)

    def test_accented_and_bare_agree(self):
        for bare, accented in [('ventitre', 'ventitré'),
                               ('trentatre', 'trentatré'),
                               ('novantatre', 'novantatré')]:
            with self.subTest(word=accented):
                self.assertEqual(extract_number(accented, lang="it"),
                                 extract_number(bare, lang="it"))

    def test_elided_units_in_hundreds(self):
        expected = {'centouno': 101, 'centuno': 101, 'centotto': 108,
                    'centootto': 108, 'centosette': 107, 'centoventuno': 121,
                    'duecentotto': 208, 'trecentotto': 308}
        for word, number in expected.items():
            with self.subTest(word=word):
                self.assertEqual(extract_number(word, lang="it"), number)

    def test_thousands_and_scale(self):
        expected = {'milleuno': 1001, 'duemila': 2000,
                    'duemilaventitre': 2023, 'duemilaventitré': 2023,
                    'centomila': 100000, 'ventitremila': 23000,
                    'tremiladuecentotrentotto': 3238,
                    'un milione': 1000000, 'due milioni': 2000000}
        for word, number in expected.items():
            with self.subTest(word=word):
                self.assertEqual(extract_number(word, lang="it"), number)


class TestItalianFractions(unittest.TestCase):
    """Spoken fractions and halves."""

    def test_fractions(self):
        expected = {'mezza': 0.5, 'mezzo': 0.5, 'un quarto': 0.25,
                    'tre quarti': 0.75, 'due terzi': 2 / 3}
        for word, number in expected.items():
            with self.subTest(word=word):
                self.assertAlmostEqual(extract_number(word, lang="it"), number)


class TestItalianAdversarial(unittest.TestCase):
    """Malformed, empty and junk input must not raise."""

    def test_empty_and_junk(self):
        for junk in ["", "   ", "ciao come stai", "!!!", "xyz",
                     "gattopardo", "trentini"]:
            with self.subTest(junk=junk):
                self.assertIn(extract_number(junk, lang="it"), (False, None))

    def test_number_in_noise(self):
        self.assertEqual(extract_number("allora ventotto mele", lang="it"), 28)
        self.assertEqual(extract_number("ne voglio quarantotto", lang="it"), 48)

    def test_zero(self):
        self.assertEqual(extract_number("zero", lang="it"), 0)


class TestItalianFusedRoundTrip(unittest.TestCase):
    """Sweep fused compounds that stress elision through a full round trip."""

    def test_sweep_all_tens(self):
        for number in range(0, 1001):
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="it")
                self.assertEqual(extract_number(spoken, lang="it"), number)

    def test_dense_fused_ranges_both_signs(self):
        # dense over the fused-compound ranges (20-99, 100-999, thousands) plus
        # a sampled sweep up to ten million, on both signs
        numbers = (list(range(0, 1000)) +
                   list(range(1000, 100000, 7)) +
                   list(range(100000, 10_000_001, 4001)))
        for n in numbers:
            for value in (n, -n):
                spoken = pronounce_number(value, lang="it")
                self.assertEqual(extract_number(spoken, lang="it"), value,
                                 f"{value} -> {spoken!r}")


if __name__ == "__main__":
    unittest.main()
