import unittest

from ovos_number_parser import extract_number, pronounce_number


class TestPolishPronounce(unittest.TestCase):
    """Anchors for spoken Polish numbers."""

    def test_pronounce_number(self):
        expected = {0: 'zero', 1: 'jeden', 2: 'dwa', 3: 'trzy', 4: 'cztery', 5: 'pięć', 6: 'sześć', 7: 'siedem', 8: 'osiem', 9: 'dziewięć', 10: 'dziesięć', 11: 'jedenaście', 12: 'dwanaście', 13: 'trzynaście', 14: 'czternaście', 15: 'piętnaście', 16: 'szesnaście', 17: 'siedemnaście', 18: 'osiemnaście', 19: 'dziewiętnaście', 20: 'dwadzieścia', 21: 'dwadzieścia jeden', 30: 'trzydzieści', 42: 'czterdzieści dwa', 50: 'pięćdziesiąt', 66: 'sześćdziesiąt sześć', 70: 'siedemdziesiąt', 80: 'osiemdziesiąt', 90: 'dziewięćdziesiąt', 99: 'dziewięćdziesiąt dziewięć', 100: 'sto', 101: 'sto jeden', 123: 'sto dwadzieścia trzy', 200: 'dwieście', 500: 'pięćset', 999: 'dziewięćset dziewięćdziesiąt dziewięć', 1000: 'tysiąc', 2000: 'dwa tysiące', 2023: 'dwa tysiące, dwadzieścia trzy', 1000000: 'milion', 2000000: 'dwa miliony'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="pl"), spoken)

    def test_pronounce_negative_and_decimal(self):
        expected = {-7: 'minus siedem', -42: 'minus czterdzieści dwa', 2.5: 'dwa przecinek pięć', 3.14: 'trzy przecinek jeden cztery', -3.5: 'minus trzy przecinek pięć', 0.5: 'zero przecinek pięć'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="pl"), spoken)


class TestPolishExtract(unittest.TestCase):
    """Anchors for extracting numbers from Polish text."""

    def test_extract_number(self):
        expected = {0: 'zero', 1: 'jeden', 2: 'dwa', 3: 'trzy', 4: 'cztery', 5: 'pięć', 6: 'sześć', 7: 'siedem', 8: 'osiem', 9: 'dziewięć', 10: 'dziesięć', 11: 'jedenaście', 12: 'dwanaście', 13: 'trzynaście', 14: 'czternaście', 15: 'piętnaście', 16: 'szesnaście', 17: 'siedemnaście', 18: 'osiemnaście', 19: 'dziewiętnaście', 20: 'dwadzieścia', 21: 'dwadzieścia jeden', 30: 'trzydzieści', 42: 'czterdzieści dwa', 50: 'pięćdziesiąt', 66: 'sześćdziesiąt sześć', 70: 'siedemdziesiąt', 80: 'osiemdziesiąt', 90: 'dziewięćdziesiąt', 99: 'dziewięćdziesiąt dziewięć', 100: 'sto', 101: 'sto jeden', 123: 'sto dwadzieścia trzy', 200: 'dwieście', 500: 'pięćset', 999: 'dziewięćset dziewięćdziesiąt dziewięć', 1000: 'tysiąc', 2000: 'dwa tysiące', 2023: 'dwa tysiące, dwadzieścia trzy', 1000000: 'milion', 2000000: 'dwa miliony'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="pl"), number)

    def test_extract_negative_and_decimal(self):
        expected = {-7: 'minus siedem', -42: 'minus czterdzieści dwa', 2.5: 'dwa przecinek pięć', 3.14: 'trzy przecinek jeden cztery', -3.5: 'minus trzy przecinek pięć', 0.5: 'zero przecinek pięć'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="pl"), number)

    def test_extract_from_sentence(self):
        self.assertEqual(extract_number('mam dwadzieścia jeden kotów', lang="pl"),
                         21)

    def test_no_number(self):
        self.assertIn(extract_number("cześć jak się masz", lang="pl"), (False, None))


class TestPolishRoundTrip(unittest.TestCase):
    """pronounce_number output must be understood by extract_number."""

    def test_round_trip(self):
        for number in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 201, 222, 300, 345, 400, 456, 500, 678, 700, 891, 900, 1000, 2000, 2023, 5000, 9999, 10000, 100000, 1000000, 2000000]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="pl")
                self.assertEqual(extract_number(spoken, lang="pl"), number)

    def test_round_trip_negative_and_decimal(self):
        for number in [-7, -42, 2.5, 3.14, -3.5, 0.5]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="pl")
                self.assertEqual(extract_number(spoken, lang="pl"), number)


class TestPolishThousands(unittest.TestCase):
    """Singular scale words (tysiąc, milion) must sum with the remainder.

    'tysiąc sto' is one thousand one hundred, not one hundred.
    """

    def test_singular_thousand_with_hundreds(self):
        cases = {
            'tysiąc sto': 1100,
            'tysiąc dwieście trzydzieści cztery': 1234,
            'tysiąc dziewięćset dziewięćdziesiąt dziewięć': 1999,
            'jeden tysiąc sto': 1100,
            'jeden tysiąc dwadzieścia jeden': 1021,
        }
        for spoken, number in cases.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="pl"), number)

    def test_singular_million_with_remainder(self):
        cases = {
            'milion jeden': 1000001,
            'jeden milion jeden': 1000001,
            'milion dwadzieścia jeden': 1000021,
        }
        for spoken, number in cases.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="pl"), number)

    def test_plural_thousands_still_work(self):
        cases = {
            'dwa tysiące pięćset': 2500,
            'pięć tysięcy sześćset siedemdziesiąt osiem': 5678,
            'dwieście pięćdziesiąt tysięcy': 250000,
            'sto tysięcy pięćset': 100500,
            'dwa miliony pięćset tysięcy': 2500000,
        }
        for spoken, number in cases.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="pl"), number)

    def test_round_trip_thousands_sweep(self):
        numbers = list(range(1000, 2000, 7)) + \
            [1100, 1234, 1999, 3721, 12345, 100500, 123456, 1000001, 2500000]
        for number in numbers:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="pl")
                self.assertEqual(extract_number(spoken, lang="pl"), number)


class TestPolishDeclensions(unittest.TestCase):
    """Declined forms in natural spoken sentences."""

    def test_declined_units_in_context(self):
        self.assertEqual(extract_number('dwie godziny', lang="pl"), 2)
        self.assertEqual(extract_number('jedna minuta', lang="pl"), 1)
        self.assertEqual(
            extract_number('mam sto dwadzieścia trzy koty', lang="pl"), 123)

    def test_fractions_and_halves(self):
        self.assertEqual(extract_number('dwa i pół', lang="pl"), 2.5)
        self.assertEqual(extract_number('trzy i pół', lang="pl"), 3.5)
        self.assertEqual(extract_number('połowa', lang="pl"), 0.5)

    def test_negative_in_sentence(self):
        self.assertEqual(extract_number('minus pięć', lang="pl"), -5)


class TestPolishAdversarial(unittest.TestCase):
    """Malformed, empty and boundary inputs must not raise."""

    def test_empty_and_junk(self):
        for text in ["", "   ", "cześć jak się masz", "!!!", " + - /"]:
            with self.subTest(text=text):
                self.assertIn(extract_number(text, lang="pl"), (False, None))

    def test_repeated_tokens_do_not_crash(self):
        for text in ["jeden jeden", "sto sto", "tysiąc tysiąc", "dwa dwa"]:
            with self.subTest(text=text):
                # must return a number and not raise
                self.assertIsNotNone(extract_number(text, lang="pl"))

    def test_lang_code_variants(self):
        self.assertEqual(extract_number('tysiąc sto', lang="pl-pl"), 1100)
        self.assertEqual(extract_number('tysiąc sto', lang="pl-PL"), 1100)


if __name__ == "__main__":
    unittest.main()
