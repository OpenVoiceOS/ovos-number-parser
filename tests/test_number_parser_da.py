import unittest

from ovos_number_parser import extract_number, pronounce_number


class TestDanishPronounce(unittest.TestCase):
    """Anchors for spoken Danish numbers."""

    def test_pronounce_number(self):
        expected = {0: 'nul', 1: 'en', 2: 'to', 3: 'tre', 4: 'fire', 5: 'fem', 6: 'seks', 7: 'syv', 8: 'otte', 9: 'ni', 10: 'ti', 11: 'elve', 12: 'tolv', 13: 'tretten', 14: 'fjorten', 15: 'femten', 16: 'seksten', 17: 'sytten', 18: 'atten', 19: 'nitten', 20: 'tyve', 21: 'enogtyve', 30: 'tredive', 42: 'toogfyrre', 50: 'halvtreds', 66: 'seksogtres', 70: 'halvfjerds', 80: 'firs', 90: 'halvfems', 99: 'nioghalvfems', 100: 'ethundrede', 101: 'ethundredeet', 123: 'ethundredetreogtyve', 200: 'tohundrede', 500: 'femhundrede', 999: 'nihundredenioghalvfems', 1000: 'ettusinde', 2000: 'totusinde', 2023: 'totusindetreogtyve', 1000000: 'en million ', 2000000: 'to millioner '}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="da"), spoken)

    def test_pronounce_negative_and_decimal(self):
        expected = {-7: 'minus syv', -42: 'minus toogfyrre', 2.5: 'to komma fem nul nul', 3.14: 'tre komma en fire nul', -3.5: 'minus tre komma fem nul nul', 0.5: ' komma fem nul nul'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="da"), spoken)


class TestDanishExtract(unittest.TestCase):
    """Anchors for extracting numbers from Danish text."""

    def test_extract_number(self):
        expected = {0: 'nul', 1: 'en', 2: 'to', 3: 'tre', 4: 'fire', 5: 'fem', 6: 'seks', 7: 'syv', 8: 'otte', 9: 'ni', 10: 'ti', 11: 'elve', 12: 'tolv', 13: 'tretten', 14: 'fjorten', 15: 'femten', 16: 'seksten', 17: 'sytten', 18: 'atten', 19: 'nitten', 20: 'tyve', 21: 'enogtyve', 30: 'tredive', 42: 'toogfyrre', 50: 'halvtreds', 66: 'seksogtres', 70: 'halvfjerds', 80: 'firs', 90: 'halvfems', 99: 'nioghalvfems', 100: 'ethundrede', 101: 'ethundredeet', 123: 'ethundredetreogtyve', 200: 'tohundrede', 500: 'femhundrede', 999: 'nihundredenioghalvfems', 1000: 'ettusinde', 2000: 'totusinde', 2023: 'totusindetreogtyve', 1000000: 'en million ', 2000000: 'to millioner '}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="da"), number)

    def test_extract_negative_and_decimal(self):
        expected = {-7: 'minus syv', -42: 'minus toogfyrre', 2.5: 'to komma fem nul nul', 3.14: 'tre komma en fire nul', -3.5: 'minus tre komma fem nul nul', 0.5: ' komma fem nul nul'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="da"), number)

    def test_extract_from_sentence(self):
        self.assertEqual(extract_number('jeg har enogtyve katte', lang="da"),
                         21)

    def test_extract_concatenated_scale_groups(self):
        # Danish writes a whole number below a million as one spaceless word,
        # so a hundreds group runs straight into its scale word. The tens use
        # the vigesimal forms prescribed by Dansk Sprognævn (SV00000047):
        # halvtreds 50, tres 60, halvfjerds 70, firs 80, halvfems 90.
        expected = {
            'ethundredeettusinde': 101000,
            'firehundredefiretusinde': 404000,
            'otte millioner firehundredefiretusindeethundredefireogtyve':
                8404124,
            'to millioner femhundredetusinde': 2500000,
            'enogtyvetusinde': 21000,
            'nihundredenioghalvfems': 999,
            'halvtreds': 50,
            'halvfjerds': 70,
            'minus en million': -1000000,
            'minus to millioner femhundredetusinde': -2500000,
        }
        for spoken, number in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="da"), number)

    def test_no_number(self):
        self.assertIn(extract_number("hej hvordan går det", lang="da"), (False, None))


class TestDanishRoundTrip(unittest.TestCase):
    """pronounce_number output must be understood by extract_number."""

    def test_round_trip(self):
        for number in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 201, 222, 300, 345, 400, 456, 500, 678, 700, 891, 900, 1000, 1001, 1234, 2000, 2023, 5000, 9999, 10000, 100000, 101000, 1000000, 1001000, 2000000, 2500000,
                       8404124, 9999999]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="da")
                self.assertEqual(extract_number(spoken, lang="da"), number)

    def test_round_trip_negative_and_decimal(self):
        for number in [-7, -42, 2.5, 3.14, -3.5, 0.5, -101000, -1000000,
                       -2500000, -8404124]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="da")
                self.assertEqual(extract_number(spoken, lang="da"), number)


class TestDanishNaturalSentences(unittest.TestCase):
    """Numbers embedded in everyday Danish sentences."""

    def test_sentences(self):
        cases = {
            'jeg vil gerne have to øl': 2,
            'der er femten personer': 15,
            'jeg har enogtyve katte': 21,
            'giv mig fem æbler': 5,
            'der bor treogtredive mennesker her': 33,
        }
        for text, value in cases.items():
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, lang="da"), value)

    def test_negative_in_sentence(self):
        self.assertEqual(extract_number("temperaturen er minus fem grader",
                                        lang="da"), -5)

    def test_fractions(self):
        self.assertEqual(extract_number("giv mig en halv", lang="da"), 0.5)
        self.assertEqual(extract_number("en kvart", lang="da"), 0.25)
        self.assertEqual(extract_number("tre en halv", lang="da"), 3.5)
        self.assertEqual(extract_number("halvdelen", lang="da"), 0.5)


class TestDanishAdversarial(unittest.TestCase):
    """Malformed, boundary and mixed input must not misbehave."""

    def test_empty_and_junk(self):
        for text in ["", "   ", "!!!", "hej hvordan går det"]:
            with self.subTest(text=text):
                self.assertIn(extract_number(text, lang="da"), (False, None))

    def test_case_insensitive(self):
        self.assertEqual(extract_number("ENOGTYVE katte", lang="da"), 21)
        self.assertEqual(extract_number("Enogtyve Katte", lang="da"), 21)

    def test_lang_code_variants(self):
        self.assertEqual(extract_number("enogtyve", lang="da"), 21)
        self.assertEqual(extract_number("enogtyve", lang="da-dk"), 21)

    def test_boundaries(self):
        self.assertEqual(extract_number("nul", lang="da"), 0)
        self.assertEqual(extract_number("titusinde", lang="da"), 10000)
        self.assertEqual(extract_number("en million", lang="da"), 1000000)


class TestDanishSweep(unittest.TestCase):
    """Dense round-trip sweep to catch off-by-one and carry errors."""

    def test_sweep_0_200(self):
        for number in range(0, 201):
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="da")
                self.assertEqual(extract_number(spoken, lang="da"), number)

    def test_sweep_hundreds_and_thousands(self):
        for number in range(200, 10001, 137):
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="da")
                self.assertEqual(extract_number(spoken, lang="da"), number)


if __name__ == "__main__":
    unittest.main()
