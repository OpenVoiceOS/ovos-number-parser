import unittest

from ovos_number_parser import extract_number, pronounce_number, is_fractional
from ovos_number_parser.numbers_sv import pronounce_ordinal_sv


class TestSwedishFractions(unittest.TestCase):
    """Swedish fraction nouns, including inflected and capitalized forms."""

    def test_basic_and_inflected(self):
        self.assertEqual(is_fractional("halv", lang="sv"), 0.5)
        self.assertEqual(is_fractional("halva", lang="sv"), 0.5)
        self.assertEqual(is_fractional("tredjedel", lang="sv"), 1.0 / 3)
        self.assertEqual(is_fractional("fjärdedel", lang="sv"), 0.25)
        self.assertEqual(is_fractional("kvart", lang="sv"), 0.25)
        self.assertEqual(is_fractional("trekvart", lang="sv"), 0.75)

    def test_capitalized_input_does_not_crash(self):
        self.assertEqual(is_fractional("Halv", lang="sv"), 0.5)
        self.assertEqual(is_fractional("HALV", lang="sv"), 0.5)
        self.assertEqual(is_fractional("Kvart", lang="sv"), 0.25)

    def test_non_fraction_returns_false(self):
        for word in ["", "hej", "fem"]:
            with self.subTest(word=word):
                self.assertFalse(is_fractional(word, lang="sv"))


class TestSwedishOrdinals(unittest.TestCase):
    """Anchors for spoken Swedish ordinals.

    Reference: standard Swedish grammar / Svenska Akademiens ordlista. Only the
    final element of a compound inflects as an ordinal; the preceding magnitude
    words keep their cardinal form.
    """

    def test_units_and_teens(self):
        expected = {
            0: 'nollte', 1: 'första', 2: 'andra', 3: 'tredje', 4: 'fjärde',
            5: 'femte', 6: 'sjätte', 7: 'sjunde', 8: 'åttonde', 9: 'nionde',
            10: 'tionde', 11: 'elfte', 12: 'tolfte', 13: 'trettonde',
            14: 'fjortonde', 15: 'femtonde', 16: 'sextonde', 17: 'sjuttonde',
            18: 'artonde', 19: 'nittonde',
        }
        for n, spoken in expected.items():
            with self.subTest(number=n):
                self.assertEqual(pronounce_ordinal_sv(n), spoken)

    def test_tens(self):
        expected = {
            20: 'tjugonde', 30: 'trettionde', 40: 'fyrtionde',
            50: 'femtionde', 60: 'sextionde', 70: 'sjuttionde',
            80: 'åttionde', 90: 'nittionde',
        }
        for n, spoken in expected.items():
            with self.subTest(number=n):
                self.assertEqual(pronounce_ordinal_sv(n), spoken)

    def test_compound_tens(self):
        expected = {
            21: 'tjugoförsta', 22: 'tjugoandra', 23: 'tjugotredje',
            25: 'tjugofemte', 33: 'trettiotredje', 48: 'fyrtioåttonde',
            99: 'nittionionde',
        }
        for n, spoken in expected.items():
            with self.subTest(number=n):
                self.assertEqual(pronounce_ordinal_sv(n), spoken)

    def test_hundreds_and_thousands(self):
        expected = {
            100: 'hundrade', 101: 'hundraförsta', 111: 'hundraelfte',
            121: 'hundratjugoförsta', 150: 'hundrafemtionde',
            200: 'tvåhundrade', 203: 'tvåhundratredje',
            999: 'niohundranittionionde',
            1000: 'tusende', 1001: 'tusenförsta', 2000: 'tvåtusende',
        }
        for n, spoken in expected.items():
            with self.subTest(number=n):
                self.assertEqual(pronounce_ordinal_sv(n), spoken)

    def test_large_scale(self):
        expected = {
            1000000: 'miljonte',
            2000000: 'tvåmiljonte',
            1000000000: 'miljardte',
        }
        for n, spoken in expected.items():
            with self.subTest(number=n):
                self.assertEqual(pronounce_ordinal_sv(n), spoken)

    def test_no_bare_de_suffix_regression(self):
        # regression: multiples of ten used to yield "tjugode"/"trettiode"
        # and teens "tioförsta"; the ten must inflect to "-nde".
        for n in (20, 30, 40, 50, 60, 70, 80, 90):
            self.assertTrue(pronounce_ordinal_sv(n).endswith('nde'), n)
        self.assertNotIn('tio', pronounce_ordinal_sv(11))

    def test_rejects_non_integer_and_negative(self):
        self.assertEqual(pronounce_ordinal_sv(-3), -3)
        self.assertEqual(pronounce_ordinal_sv(2.5), 2.5)


class TestSwedishPronounce(unittest.TestCase):
    """Anchors for spoken Swedish numbers."""

    def test_pronounce_number(self):
        expected = {0: 'noll', 1: 'en', 2: 'två', 3: 'tre', 4: 'fyra', 5: 'fem', 6: 'sex', 7: 'sju', 8: 'åtta', 9: 'nio', 10: 'tio', 11: 'elva', 12: 'tolv', 13: 'tretton', 14: 'fjorton', 15: 'femton', 16: 'sexton', 17: 'sjutton', 18: 'arton', 19: 'nitton', 20: 'tjugo', 21: 'tjugoen', 30: 'trettio', 42: 'fyrtiotvå', 50: 'femtio', 66: 'sextiosex', 70: 'sjuttio', 80: 'åttio', 90: 'nittio', 99: 'nittionio', 100: 'etthundra', 101: 'etthundraett', 123: 'etthundratjugotre', 200: 'tvåhundra', 500: 'femhundra', 999: 'niohundranittionio', 1000: 'ettusen ', 2000: 'tvåtusen ', 2023: 'tvåtusen tjugotre', 1000000: 'en miljon ', 2000000: 'tvåmiljoner '}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="sv"), spoken)

    def test_pronounce_negative_and_decimal(self):
        expected = {-7: 'minus sju', -42: 'minus fyrtiotvå', 2.5: 'två komma fem noll noll', 3.14: 'tre komma en fyra noll', -3.5: 'minus tre komma fem noll noll', 0.5: 'noll komma fem noll noll'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="sv"), spoken)


class TestSwedishExtract(unittest.TestCase):
    """Anchors for extracting numbers from Swedish text."""

    def test_extract_number(self):
        expected = {0: 'noll', 1: 'en', 2: 'två', 3: 'tre', 4: 'fyra', 5: 'fem', 6: 'sex', 7: 'sju', 8: 'åtta', 9: 'nio', 10: 'tio', 11: 'elva', 12: 'tolv', 13: 'tretton', 14: 'fjorton', 15: 'femton', 16: 'sexton', 17: 'sjutton', 18: 'arton', 19: 'nitton', 20: 'tjugo', 21: 'tjugoen', 30: 'trettio', 42: 'fyrtiotvå', 50: 'femtio', 66: 'sextiosex', 70: 'sjuttio', 80: 'åttio', 90: 'nittio', 99: 'nittionio', 100: 'etthundra', 101: 'etthundraett', 123: 'etthundratjugotre', 200: 'tvåhundra', 500: 'femhundra', 999: 'niohundranittionio', 1000: 'ettusen ', 2000: 'tvåtusen ', 2023: 'tvåtusen tjugotre', 1000000: 'en miljon ', 2000000: 'tvåmiljoner '}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="sv"), number)

    def test_extract_negative_and_decimal(self):
        expected = {-7: 'minus sju', -42: 'minus fyrtiotvå', 2.5: 'två komma fem noll noll', 3.14: 'tre komma en fyra noll', -3.5: 'minus tre komma fem noll noll', 0.5: 'noll komma fem noll noll'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="sv"), number)

    def test_extract_from_sentence(self):
        self.assertEqual(extract_number('jag har tjugoen katter', lang="sv"),
                         21)

    def test_no_number(self):
        self.assertIn(extract_number("hej hur mår du", lang="sv"), (False, None))


class TestSwedishRoundTrip(unittest.TestCase):
    """pronounce_number output must be understood by extract_number."""

    def test_round_trip(self):
        for number in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 201, 222, 300, 345, 400, 456, 500, 678, 700, 891, 900, 1000, 1001, 1234, 2000, 2023, 5000, 9999, 10000, 100000, 1000000, 2000000]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="sv")
                self.assertEqual(extract_number(spoken, lang="sv"), number)

    def test_round_trip_negative_and_decimal(self):
        for number in [-7, -42, 2.5, 3.14, -3.5, 0.5]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="sv")
                self.assertEqual(extract_number(spoken, lang="sv"), number)


class TestSwedishNaturalSentences(unittest.TestCase):
    """Numbers embedded in natural spoken Swedish."""

    def test_sentences(self):
        cases = {
            "jag har tjugoen katter": 21,
            "det kostar etthundra kronor": 100,
            "tre och en halv": 3.5,
            "en och en halv": 1.5,
            "två komma fem": 2.5,
            "minus sju grader": -7,
            "året tvåtusen tjugotre": 2023,
        }
        for text, val in cases.items():
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, lang="sv"), val)

    def test_fractions_words(self):
        # "halv fyra" is not a number phrase on its own: "halv" -> 0.5
        self.assertEqual(extract_number("halv", lang="sv"), 0.5)
        self.assertEqual(extract_number("en kvart", lang="sv"), 0.25)
        self.assertEqual(extract_number("trekvart", lang="sv"), 0.75)


class TestSwedishAdversarial(unittest.TestCase):
    """Malformed / boundary / contract-violation inputs must not crash."""

    def test_non_string_input(self):
        for bad in (None, 42, 3.5, [], {}):
            with self.subTest(bad=bad):
                self.assertIn(extract_number(bad, lang="sv"), (False, None))

    def test_empty_and_junk(self):
        for text in ("", "   ", "hej hur mår du", "!!!", "minus"):
            with self.subTest(text=text):
                self.assertIn(extract_number(text, lang="sv"), (False, None))

    def test_mixed_case(self):
        self.assertEqual(extract_number("TJUGOEN", lang="sv"), 21)
        self.assertEqual(extract_number("Fyrtiotvå", lang="sv"), 42)

    def test_boundaries(self):
        self.assertEqual(extract_number("2/3", lang="sv"), 2 / 3)
        self.assertEqual(extract_number("minus fyrtiotvå", lang="sv"), -42)


class TestSwedishLargeSweep(unittest.TestCase):
    """Round-trip a dense range to guard pronounce/extract symmetry."""

    def test_dense_sweep(self):
        for n in list(range(0, 2000)) + list(range(2000, 100000, 137)):
            with self.subTest(number=n):
                spoken = pronounce_number(n, lang="sv")
                got = extract_number(spoken, lang="sv")
                if n == 0:
                    self.assertIn(got, (0, False))
                else:
                    self.assertEqual(got, n)


if __name__ == "__main__":
    unittest.main()
