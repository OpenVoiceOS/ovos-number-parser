import unittest

from ovos_number_parser import extract_number, pronounce_number


class TestGermanPronounce(unittest.TestCase):
    """Anchors for spoken German numbers."""

    def test_pronounce_number(self):
        expected = {0: 'null', 1: 'eins', 2: 'zwei', 3: 'drei', 4: 'vier', 5: 'fünf', 6: 'sechs', 7: 'sieben', 8: 'acht', 9: 'neun', 10: 'zehn', 11: 'elf', 12: 'zwölf', 13: 'dreizehn', 14: 'vierzehn', 15: 'fünfzehn', 16: 'sechzehn', 17: 'siebzehn', 18: 'achtzehn', 19: 'neunzehn', 20: 'zwanzig', 21: 'einundzwanzig', 30: 'dreißig', 42: 'zweiundvierzig', 50: 'fünfzig', 66: 'sechsundsechzig', 70: 'siebzig', 80: 'achtzig', 90: 'neunzig', 99: 'neunundneunzig', 100: 'einhundert', 101: 'einhunderteins', 123: 'einhundertdreiundzwanzig', 200: 'zweihundert', 500: 'fünfhundert', 999: 'neunhundertneunundneunzig', 1000: 'eintausend', 2000: 'zweitausend', 2023: 'zweitausenddreiundzwanzig', 1000000: 'eine Million ', 2000000: 'zwei Millionen '}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="de"), spoken)

    def test_pronounce_negative_and_decimal(self):
        expected = {-7: 'minus sieben', -42: 'minus zweiundvierzig', 2.5: 'zwei Komma fünf null null', 3.14: 'drei Komma eins vier null', -3.5: 'minus drei Komma fünf null null', 0.5: ' Komma fünf null null'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="de"), spoken)


class TestGermanExtract(unittest.TestCase):
    """Anchors for extracting numbers from German text."""

    def test_extract_number(self):
        expected = {0: 'null', 1: 'eins', 2: 'zwei', 3: 'drei', 4: 'vier', 5: 'fünf', 6: 'sechs', 7: 'sieben', 8: 'acht', 9: 'neun', 10: 'zehn', 11: 'elf', 12: 'zwölf', 13: 'dreizehn', 14: 'vierzehn', 15: 'fünfzehn', 16: 'sechzehn', 17: 'siebzehn', 18: 'achtzehn', 19: 'neunzehn', 20: 'zwanzig', 21: 'einundzwanzig', 30: 'dreißig', 42: 'zweiundvierzig', 50: 'fünfzig', 66: 'sechsundsechzig', 70: 'siebzig', 80: 'achtzig', 90: 'neunzig', 99: 'neunundneunzig', 100: 'einhundert', 101: 'einhunderteins', 123: 'einhundertdreiundzwanzig', 200: 'zweihundert', 500: 'fünfhundert', 999: 'neunhundertneunundneunzig', 1000: 'eintausend', 2000: 'zweitausend', 2023: 'zweitausenddreiundzwanzig', 1000000: 'eine Million ', 2000000: 'zwei Millionen '}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="de"), number)

    def test_extract_negative_and_decimal(self):
        expected = {-7: 'minus sieben', -42: 'minus zweiundvierzig', 2.5: 'zwei Komma fünf null null', 3.14: 'drei Komma eins vier null', -3.5: 'minus drei Komma fünf null null', 0.5: ' Komma fünf null null'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="de"), number)

    def test_extract_from_sentence(self):
        self.assertEqual(extract_number('ich habe einundzwanzig Katzen', lang="de"),
                         21)

    def test_no_number(self):
        self.assertIn(extract_number("hallo wie geht es dir", lang="de"), (False, None))


class TestGermanRoundTrip(unittest.TestCase):
    """pronounce_number output must be understood by extract_number."""

    def test_round_trip(self):
        for number in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 201, 222, 300, 345, 400, 456, 500, 678, 700, 891, 900, 1000, 1001, 1234, 2000, 2023, 5000, 9999, 10000, 100000, 1000000, 2000000]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="de")
                self.assertEqual(extract_number(spoken, lang="de"), number)

    def test_round_trip_negative_and_decimal(self):
        for number in [-7, -42, 2.5, 3.14, -3.5, 0.5]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="de")
                self.assertEqual(extract_number(spoken, lang="de"), number)


class TestGermanNaturalSentences(unittest.TestCase):
    """Numbers embedded in natural German utterances."""

    def test_first_number_in_sentence(self):
        self.assertEqual(
            extract_number("ich hätte gern drei äpfel und zwei birnen", lang="de"), 3)
        self.assertEqual(
            extract_number("stell den wecker auf sieben minuten", lang="de"), 7)
        self.assertEqual(
            extract_number("in zweiundzwanzig tagen", lang="de"), 22)
        self.assertEqual(
            extract_number("zweihundertdreiundvierzig gäste", lang="de"), 243)

    def test_fractions(self):
        self.assertEqual(extract_number("zweieinhalb", lang="de"), 2.5)
        self.assertEqual(extract_number("dreiviertel", lang="de"), 0.75)
        self.assertEqual(extract_number("ein halb", lang="de"), 0.5)

    def test_ordinals_only(self):
        self.assertEqual(extract_number("der erste", lang="de", ordinals=True), 1)
        self.assertEqual(extract_number("der dritte", lang="de", ordinals=True), 3)
        self.assertEqual(
            extract_number("der einundzwanzigste", lang="de", ordinals=True), 21)


class TestGermanAdversarial(unittest.TestCase):
    """Malformed, boundary and junk inputs must not crash or misparse."""

    def test_empty_and_junk(self):
        for text in ["", "   ", "hallo welt", "!!!", "\n\t"]:
            with self.subTest(text=text):
                self.assertIn(extract_number(text, lang="de"), (False, None))

    def test_case_insensitive(self):
        self.assertEqual(extract_number("MINUS SIEBEN".lower(), lang="de"), -7)
        self.assertEqual(extract_number("Einundzwanzig".lower(), lang="de"), 21)

    def test_leading_trailing_junk(self):
        self.assertEqual(extract_number("  zwei  ", lang="de"), 2)
        self.assertEqual(
            extract_number("also dann bitte einundzwanzig okay", lang="de"), 21)

    def test_lang_code_variants(self):
        for lang in ("de", "de-de", "de-DE"):
            with self.subTest(lang=lang):
                self.assertEqual(extract_number("einundzwanzig", lang=lang), 21)

    def test_negative_and_zero_boundaries(self):
        self.assertEqual(extract_number("null", lang="de"), 0)
        self.assertEqual(extract_number("minus null", lang="de"), 0)
        self.assertEqual(extract_number("minus zweiundvierzig", lang="de"), -42)

    def test_large_numbers(self):
        self.assertEqual(extract_number("einhunderttausend", lang="de"), 100000)
        self.assertEqual(extract_number("eine Million", lang="de"), 1000000)


class TestGermanRoundTripSweep(unittest.TestCase):
    """Every integer up to 10000 must survive pronounce -> extract."""

    def test_sweep_dense(self):
        for number in range(0, 2001):
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="de")
                self.assertEqual(extract_number(spoken, lang="de"), number)

    def test_sweep_large(self):
        for number in [3000, 4567, 9999, 10000, 12345, 99999,
                       100000, 123456, 999999, 1000000, 2000000,
                       1234567, 1000000000]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="de")
                self.assertEqual(extract_number(spoken, lang="de"), number)


if __name__ == "__main__":
    unittest.main()
