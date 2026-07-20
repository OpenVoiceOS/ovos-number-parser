import unittest

from ovos_number_parser import extract_number, pronounce_number


class TestDutchPronounce(unittest.TestCase):
    """Anchors for spoken Dutch numbers."""

    def test_pronounce_number(self):
        expected = {0: 'nul', 1: 'één', 2: 'twee', 3: 'drie', 4: 'vier', 5: 'vijf', 6: 'zes', 7: 'zeven', 8: 'acht', 9: 'negen', 10: 'tien', 11: 'elf', 12: 'twaalf', 13: 'dertien', 14: 'veertien', 15: 'vijftien', 16: 'zestien', 17: 'zeventien', 18: 'achttien', 19: 'negentien', 20: 'twintig', 21: 'eenentwintig', 30: 'dertig', 42: 'tweeënveertig', 50: 'vijftig', 66: 'zesenzestig', 70: 'zeventig', 80: 'tachtig', 90: 'negentig', 99: 'negenennegentig', 100: 'eenhonderd', 101: 'eenhonderdeen', 123: 'eenhonderddrieëntwintig', 200: 'tweehonderd', 500: 'vijfhonderd', 999: 'negenhonderdnegenennegentig', 1000: 'eenduizend', 2000: 'tweeduizend', 2023: 'tweeduizenddrieëntwintig', 1000000: 'één miljoen ', 2000000: 'twee miljoen '}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="nl"), spoken)

    def test_pronounce_negative_and_decimal(self):
        expected = {-7: 'min zeven', -42: 'min tweeënveertig', 2.5: 'twee komma vijf nul nul', 3.14: 'drie komma een vier nul', -3.5: 'min drie komma vijf nul nul', 0.5: 'nul komma vijf nul nul'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="nl"), spoken)


class TestDutchExtract(unittest.TestCase):
    """Anchors for extracting numbers from Dutch text."""

    def test_extract_number(self):
        expected = {0: 'nul', 1: 'één', 2: 'twee', 3: 'drie', 4: 'vier', 5: 'vijf', 6: 'zes', 7: 'zeven', 8: 'acht', 9: 'negen', 10: 'tien', 11: 'elf', 12: 'twaalf', 13: 'dertien', 14: 'veertien', 15: 'vijftien', 16: 'zestien', 17: 'zeventien', 18: 'achttien', 19: 'negentien', 20: 'twintig', 21: 'eenentwintig', 30: 'dertig', 42: 'tweeënveertig', 50: 'vijftig', 66: 'zesenzestig', 70: 'zeventig', 80: 'tachtig', 90: 'negentig', 99: 'negenennegentig', 100: 'eenhonderd', 101: 'eenhonderdeen', 123: 'eenhonderddrieëntwintig', 200: 'tweehonderd', 500: 'vijfhonderd', 999: 'negenhonderdnegenennegentig', 1000: 'eenduizend', 2000: 'tweeduizend', 2023: 'tweeduizenddrieëntwintig', 1000000: 'één miljoen ', 2000000: 'twee miljoen '}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="nl"), number)

    def test_extract_negative_and_decimal(self):
        expected = {-7: 'min zeven', -42: 'min tweeënveertig', 2.5: 'twee komma vijf nul nul', 3.14: 'drie komma een vier nul', -3.5: 'min drie komma vijf nul nul', 0.5: 'nul komma vijf nul nul'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="nl"), number)

    def test_extract_from_sentence(self):
        self.assertEqual(extract_number('ik heb éénentwintig katten', lang="nl"),
                         21)

    def test_no_number(self):
        self.assertIn(extract_number("hallo hoe gaat het", lang="nl"), (False, None))


class TestDutchRoundTrip(unittest.TestCase):
    """pronounce_number output must be understood by extract_number."""

    def test_round_trip(self):
        for number in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 201, 222, 300, 345, 400, 456, 500, 678, 700, 891, 900, 1000, 1001, 1234, 2000, 2023, 5000, 9999, 10000, 100000, 1000000, 2000000]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="nl")
                self.assertEqual(extract_number(spoken, lang="nl"), number)

    def test_round_trip_negative_and_decimal(self):
        for number in [-7, -42, 2.5, 3.14, -3.5, 0.5]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="nl")
                self.assertEqual(extract_number(spoken, lang="nl"), number)


class TestDutchFractions(unittest.TestCase):
    """Spoken Dutch fractions and 'and a half' compounds."""

    def test_half_compounds(self):
        # "tweeëneenhalf" == "twee en een half" == 2.5; the "een" before
        # "half" is the article, it must not add a whole unit
        self.assertEqual(extract_number("tweeeneenhalf", lang="nl"), 2.5)
        self.assertEqual(extract_number("tweeenhalf", lang="nl"), 2.5)
        self.assertEqual(extract_number("drieeneenhalf", lang="nl"), 3.5)
        self.assertEqual(extract_number("vijfeneenhalf", lang="nl"), 5.5)
        self.assertEqual(extract_number("eenhalf", lang="nl"), 0.5)

    def test_half_compound_matches_spaced_form(self):
        for word, spaced in [("tweeeneenhalf", "twee en een half"),
                             ("drieeneenhalf", "drie en een half")]:
            with self.subTest(word=word):
                self.assertEqual(extract_number(word, lang="nl"),
                                 extract_number(spaced, lang="nl"))

    def test_natural_fraction_sentences(self):
        self.assertEqual(
            extract_number("over tweeeneenhalf uur", lang="nl"), 2.5)
        self.assertEqual(
            extract_number("ik wil twee en een half koekjes", lang="nl"), 2.5)
        self.assertEqual(extract_number("anderhalf", lang="nl"), 1.5)
        self.assertEqual(extract_number("driekwart liter", lang="nl"), 0.75)
        self.assertEqual(extract_number("een paar appels", lang="nl"), 2)

    def test_lang_code_variants(self):
        for lang in ("nl", "nl-nl"):
            with self.subTest(lang=lang):
                self.assertEqual(
                    extract_number("tweeeneenhalf", lang=lang), 2.5)


class TestDutchOrdinalsAndSentences(unittest.TestCase):

    def test_ordinal_words(self):
        expected = {"eerste": 1, "tweede": 2, "derde": 3, "vierde": 4,
                    "vijfde": 5, "achtste": 8, "negende": 9,
                    "twintigste": 20}
        for word, value in expected.items():
            with self.subTest(word=word):
                self.assertEqual(
                    extract_number(word, lang="nl", ordinals=True), value)

    def test_ordinal_in_sentence(self):
        self.assertEqual(
            extract_number("de derde deur", lang="nl", ordinals=True), 3)


class TestDutchAdversarial(unittest.TestCase):

    def test_empty_and_junk(self):
        for text in ["", "   ", "hallo wereld", "abcdef", "!!!"]:
            with self.subTest(text=text):
                self.assertIn(extract_number(text, lang="nl"), (False, None))

    def test_mixed_case(self):
        self.assertEqual(extract_number("MIN ZEVEN", lang="nl"), -7)
        self.assertEqual(extract_number("TWINTIG", lang="nl"), 20)

    def test_zero_and_negatives(self):
        self.assertEqual(extract_number("nul", lang="nl"), 0)
        self.assertEqual(extract_number("min eenhonderd", lang="nl"), -100)


class TestDutchWideRoundTrip(unittest.TestCase):
    """pronounce_number output must survive extract_number over a wide range."""

    def test_round_trip_sweep(self):
        for number in list(range(0, 2000)) + \
                [2500, 3333, 5000, 9999, 12345, 100000, 999999,
                 1000000, 1234567]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="nl")
                self.assertEqual(extract_number(spoken, lang="nl"), number)

    def test_round_trip_negatives(self):
        for number in [-1, -7, -21, -100, -999, -1000]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="nl")
                self.assertEqual(extract_number(spoken, lang="nl"), number)

    def test_round_trip_negative_millions_with_remainder(self):
        # the negative marker only reaches the first scale group, so the
        # trailing groups of "min ... miljoen ..." must still inherit the sign
        for number in [-1500000, -1225280, -2540830, -5443013, -6634040,
                       -1001710]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="nl")
                self.assertEqual(extract_number(spoken, lang="nl"), number)


if __name__ == "__main__":
    unittest.main()
