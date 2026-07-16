import unittest

from ovos_number_parser import extract_number, pronounce_number


class TestGermanPronounce(unittest.TestCase):
    """Anchors for spoken German numbers."""

    def test_pronounce_number(self):
        expected = {0: 'null', 1: 'eins', 2: 'zwei', 3: 'drei', 4: 'vier', 5: 'fünf', 6: 'sechs', 7: 'sieben', 8: 'acht', 9: 'neun', 10: 'zehn', 11: 'elf', 12: 'zwölf', 13: 'dreizehn', 14: 'vierzehn', 15: 'fünfzehn', 16: 'sechzehn', 17: 'siebzehn', 18: 'achtzehn', 19: 'neunzehn', 20: 'zwanzig', 21: 'einundzwanzig', 30: 'dreißig', 42: 'zweiundvierzig', 50: 'fünfzig', 66: 'sechsundsechzig', 70: 'siebzig', 80: 'achtzig', 90: 'neunzig', 99: 'neunundneunzig', 100: 'einhundert', 101: 'einhunderteins', 123: 'einhundertdreiundzwanzig', 200: 'zweihundert', 500: 'fünfhundert', 999: 'neunhundertneunundneunzig', 1000: 'eintausend', 2000: 'zweitausend', 2023: 'zweitausenddreiundzwanzig', 1000000: 'eine Million ', 2000000: 'zwei Millionen '}
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

    def test_no_number(self):
        self.assertIn(extract_number("hallo wie geht es dir", lang="de"), (False, None))


class TestGermanRoundTrip(unittest.TestCase):
    """pronounce_number output must be understood by extract_number."""

    def test_round_trip(self):
        for number in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 201, 222, 300, 345, 400, 456, 500, 678, 700, 891, 900, 1000, 1001, 1234, 2000, 2023, 5000, 9999, 10000, 100000, 1000000, 2000000]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="de")
                self.assertEqual(extract_number(spoken, lang="de"), number)


if __name__ == "__main__":
    unittest.main()
