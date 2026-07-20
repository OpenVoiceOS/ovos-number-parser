import unittest

from ovos_number_parser import (extract_number, pronounce_number,
                                pronounce_ordinal, pronounce_fraction,
                                is_fractional, is_ordinal, numbers_to_digits)


class TestHebrewPronounce(unittest.TestCase):
    """Anchors for spoken Hebrew numbers (masculine citation forms)."""

    def test_pronounce_number(self):
        # feminine = the abstract counting form (Academy of the Hebrew
        # Language); every value below is cross-checked against ICU spellout
        expected = {
            0: 'אפס', 1: 'אחת', 2: 'שתיים', 3: 'שלוש', 4: 'ארבע',
            5: 'חמש', 6: 'שש', 7: 'שבע', 8: 'שמונה', 9: 'תשע',
            10: 'עשר', 11: 'אחת עשרה', 12: 'שתים עשרה', 13: 'שלוש עשרה',
            14: 'ארבע עשרה', 15: 'חמש עשרה', 16: 'שש עשרה',
            17: 'שבע עשרה', 18: 'שמונה עשרה', 19: 'תשע עשרה', 20: 'עשרים',
            # the conjunction ו attaches to the final component
            21: 'עשרים ואחת', 25: 'עשרים וחמש', 30: 'שלושים',
            42: 'ארבעים ושתיים', 50: 'חמישים', 66: 'שישים ושש',
            70: 'שבעים', 80: 'שמונים', 90: 'תשעים', 99: 'תשעים ותשע',
            100: 'מאה', 101: 'מאה ואחת', 110: 'מאה ועשר',
            123: 'מאה עשרים ושלוש',
            # dual forms encode value times two
            200: 'מאתיים', 2000: 'אלפיים',
            # 300-900 use the feminine unit + מאות
            300: 'שלוש מאות', 500: 'חמש מאות',
            999: 'תשע מאות תשעים ותשע',
            1000: 'אלף', 1985: 'אלף תשע מאות שמונים וחמש',
            2023: 'אלפיים עשרים ושלוש',
            # 3000-10000 use the construct-state unit + אלפים; the scale count
            # before מיליון agrees with the masculine noun (שלושה מיליון)
            3000: 'שלושת אלפים', 10000: 'עשרת אלפים', 11000: 'אחד עשר אלף',
            100000: 'מאה אלף', 1000000: 'מיליון', 2000000: 'שני מיליון',
            3000000: 'שלושה מיליון', 1000000000: 'מיליארד',
        }
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="he"), spoken)

    def test_pronounce_negative_and_decimal(self):
        expected = {-7: 'מינוס שבע', -42: 'מינוס ארבעים ושתיים',
                    5.2: 'חמש נקודה שתיים',
                    5.25: 'חמש נקודה שתיים חמש',
                    0.5: 'אפס נקודה חמש',
                    -3.5: 'מינוס שלוש נקודה חמש'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="he"), spoken)

    def test_pronounce_ordinal(self):
        expected = {1: 'ראשון', 2: 'שני', 3: 'שלישי', 4: 'רביעי',
                    5: 'חמישי', 6: 'שישי', 7: 'שביעי', 8: 'שמיני',
                    9: 'תשיעי', 10: 'עשירי',
                    # ordinals beyond 10 use the definite cardinal
                    11: 'האחד עשר', 12: 'השנים עשר', 20: 'העשרים',
                    21: 'העשרים ואחד', 25: 'העשרים וחמישה',
                    30: 'השלושים', 100: 'המאה', 1000: 'האלף'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_ordinal(number, lang="he"), spoken)

    def test_pronounce_fraction(self):
        self.assertEqual(pronounce_fraction("1/2", lang="he"), 'חצי')
        self.assertEqual(pronounce_fraction("1/3", lang="he"), 'שליש')
        self.assertEqual(pronounce_fraction("1/4", lang="he"), 'רבע')
        self.assertEqual(pronounce_fraction("2/3", lang="he"), 'שני שלישים')
        self.assertEqual(pronounce_fraction("3/4", lang="he"),
                         'שלושה רבעים')
        # feminine agreement of the ordinal-derived fraction nouns
        self.assertEqual(pronounce_fraction("2/5", lang="he"),
                         'שתי חמישיות')
        self.assertEqual(pronounce_fraction("3/10", lang="he"),
                         'שלוש עשיריות')


class TestHebrewExtract(unittest.TestCase):
    """Anchors for extracting numbers from Hebrew text."""

    def test_extract_number(self):
        expected = {
            0: 'אפס', 1: 'אחד', 2: 'שניים', 3: 'שלושה', 10: 'עשרה',
            11: 'אחד עשר', 12: 'שנים עשר', 15: 'חמישה עשר', 20: 'עשרים',
            25: 'עשרים וחמישה', 99: 'תשעים ותשעה', 100: 'מאה',
            123: 'מאה עשרים ושלושה', 1000: 'אלף', 3000: 'שלושת אלפים',
            1000000: 'מיליון',
        }
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="he"), number)

    def test_extract_gender_and_construct_variants(self):
        # feminine forms are accepted alongside the masculine ones
        expected = {1: 'אחת', 2: 'שתיים', 3: 'שלוש', 4: 'ארבע',
                    5: 'חמש', 6: 'שש', 7: 'שבע', 9: 'תשע', 10: 'עשר',
                    # construct-state forms
                    22: 'עשרים ושתיים', 32: 'שלושים ושתי',
                    # feminine teens
                    11: 'אחת עשרה', 12: 'שתים עשרה', 13: 'שלוש עשרה',
                    18: 'שמונה עשרה',
                    # duals
                    200: 'מאתיים', 2000: 'אלפיים',
                    # feminine compounds
                    21: 'עשרים ואחת', 400: 'ארבע מאות'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="he"), number)

    def test_extract_negative_and_decimal(self):
        expected = {-7: 'מינוס שבעה', -9: 'מינוס תשעה',
                    -42: 'מינוס ארבעים ושניים',
                    5.2: 'חמישה נקודה שניים',
                    3.14: 'שלושה נקודה אחד ארבעה',
                    5.5: 'חמישה וחצי', 2.25: 'שניים ורבע',
                    0.5: 'חצי', 0.25: 'רבע'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertAlmostEqual(extract_number(spoken, lang="he"),
                                       number)

    def test_extract_with_niqqud(self):
        # vowel points are stripped before matching
        self.assertEqual(extract_number("שְׁלוֹשָׁה", lang="he"), 3)
        self.assertEqual(extract_number("אַרְבַּע", lang="he"), 4)

    def test_extract_from_sentence(self):
        self.assertEqual(extract_number("יש לי עשרים וחמישה ספרים",
                                        lang="he"), 25)
        self.assertEqual(extract_number("קניתי שלוש בננות", lang="he"), 3)
        self.assertEqual(extract_number("זה היום השלישי", lang="he",
                                        ordinals=True), 3)
        self.assertEqual(extract_number("העשרים וחמישה", lang="he",
                                        ordinals=True), 25)

    def test_no_number(self):
        self.assertIn(extract_number("שלום מה שלומך", lang="he"),
                      (False, None))
        self.assertIn(extract_number("", lang="he"), (False, None))

    def test_is_fractional(self):
        self.assertEqual(is_fractional("חצי", lang="he"), 0.5)
        self.assertEqual(is_fractional("רבע", lang="he"), 0.25)
        self.assertEqual(is_fractional("הרבע", lang="he"), 0.25)
        self.assertAlmostEqual(is_fractional("שליש", lang="he"), 1 / 3)
        self.assertAlmostEqual(is_fractional("חמישית", lang="he"), 0.2)
        self.assertAlmostEqual(is_fractional("עשירית", lang="he"), 0.1)
        self.assertFalse(is_fractional("ספר", lang="he"))

    def test_is_ordinal(self):
        self.assertEqual(is_ordinal("ראשון", lang="he"), 1)
        self.assertEqual(is_ordinal("ראשונה", lang="he"), 1)
        self.assertEqual(is_ordinal("שלישית", lang="he"), 3)
        self.assertEqual(is_ordinal("האחד עשר", lang="he"), 11)
        self.assertEqual(is_ordinal("העשרים וחמישה", lang="he"), 25)
        self.assertFalse(is_ordinal("שלום", lang="he"))

    def test_numbers_to_digits(self):
        self.assertEqual(
            numbers_to_digits("יש לי עשרים וחמישה חתולים", lang="he"),
            "יש לי 25 חתולים")


class TestHebrewRoundTrip(unittest.TestCase):
    """pronounce_number output must be understood by extract_number."""

    def test_round_trip(self):
        numbers = list(range(0, 200)) + [
            201, 222, 300, 345, 400, 456, 500, 678, 700, 891, 900, 999,
            1000, 1001, 1234, 1985, 2000, 2023, 3000, 5000, 9999, 10000,
            11000, 15000, 100000, 123456, 1000000, 2000000, 3000000,
            1000000000, 2000000000]
        for number in numbers:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="he")
                self.assertEqual(extract_number(spoken, lang="he"), number)

    def test_round_trip_negative_and_decimal(self):
        for number in [-7, -42, -100, 2.5, 3.14, 5.2, -3.5, 0.5, 5.25,
                       0.75, 12.34]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="he")
                self.assertAlmostEqual(extract_number(spoken, lang="he"),
                                       number)

    def test_round_trip_ordinals(self):
        for number in range(1, 100):
            with self.subTest(number=number):
                spoken = pronounce_ordinal(number, lang="he")
                self.assertEqual(is_ordinal(spoken, lang="he"), number)


if __name__ == "__main__":
    unittest.main()
