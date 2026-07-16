import unittest

from ovos_number_parser import (extract_number, is_fractional, is_ordinal,
                                numbers_to_digits, pronounce_number,
                                pronounce_ordinal)


class TestGreekPronounce(unittest.TestCase):
    def test_pronounce_number(self):
        expected = {
            0: 'μηδέν', 1: 'ένα', 2: 'δύο', 3: 'τρία', 4: 'τέσσερα',
            5: 'πέντε', 10: 'δέκα', 11: 'έντεκα', 12: 'δώδεκα',
            13: 'δεκατρία', 20: 'είκοσι', 21: 'είκοσι ένα',
            30: 'τριάντα', 40: 'σαράντα', 50: 'πενήντα', 60: 'εξήντα',
            70: 'εβδομήντα', 80: 'ογδόντα', 90: 'ενενήντα',
            100: 'εκατό', 200: 'διακόσια', 300: 'τριακόσια',
            1000: 'χίλια', 1234: 'χίλια διακόσια τριάντα τέσσερα',
            2500: 'δύο χιλιάδες πεντακόσια',
            1000000: 'ένα εκατομμύριο',
        }
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="el"), spoken)

    def test_pronounce_negative_and_decimal(self):
        self.assertEqual(pronounce_number(-5, lang="el"), 'μείον πέντε')
        self.assertEqual(pronounce_number(5.2, lang="el"),
                         'πέντε κόμμα δύο')

    def test_pronounce_ordinal(self):
        expected = {1: 'πρώτος', 2: 'δεύτερος', 3: 'τρίτος',
                    4: 'τέταρτος', 10: 'δέκατος', 21: 'εικοστός πρώτος'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_ordinal(number, lang="el"), spoken)


class TestGreekExtract(unittest.TestCase):
    def test_extract_anchors(self):
        cases = [('ένα', 1), ('τρία', 3), ('δεκατρία', 13),
                 ('είκοσι ένα', 21), ('εκατό', 100), ('διακόσια', 200),
                 ('χίλια', 1000), ('δύο χιλιάδες πεντακόσια', 2500)]
        for spoken, expected in cases:
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="el"), expected)

    def test_gender_variants(self):
        # the gendered forms of 3 and 4 are accepted alongside the neuter
        self.assertEqual(extract_number('τρεις', lang="el"), 3)
        self.assertEqual(extract_number('τέσσερις', lang="el"), 4)

    def test_accentless_input(self):
        # unaccented typing is common and must still parse
        self.assertEqual(extract_number('εικοσι ενα', lang="el"), 21)
        self.assertEqual(extract_number('πεντακοσια', lang="el"), 500)

    def test_spelling_variants(self):
        self.assertEqual(extract_number('εφτά', lang="el"), 7)
        self.assertEqual(extract_number('οχτώ', lang="el"), 8)
        self.assertEqual(extract_number('εννιά', lang="el"), 9)

    def test_digits(self):
        self.assertEqual(extract_number('5 γάτες', lang="el"), 5)

    def test_negative(self):
        self.assertEqual(extract_number('μείον πέντε', lang="el"), -5)

    def test_decimal(self):
        self.assertEqual(extract_number('πέντε κόμμα δύο', lang="el"), 5.2)

    def test_in_sentence(self):
        self.assertEqual(
            extract_number('έχω είκοσι ένα γάτες', lang="el"), 21)

    def test_no_number(self):
        self.assertFalse(extract_number('καλημέρα', lang="el"))

    def test_round_trip_sweep(self):
        values = list(range(0, 121)) + [150, 200, 345, 500, 999, 1000, 1001,
                                        2500, 12345, 100000, 1000000]
        for n in values:
            spoken = pronounce_number(n, lang="el")
            self.assertEqual(extract_number(spoken, lang="el"), n,
                             f"{n} -> {spoken!r}")

    def test_negative_round_trip(self):
        for n in (-1, -21, -100, -2500):
            spoken = pronounce_number(n, lang="el")
            self.assertEqual(extract_number(spoken, lang="el"), n,
                             f"{n} -> {spoken!r}")


class TestGreekHelpers(unittest.TestCase):
    def test_is_fractional(self):
        self.assertEqual(is_fractional('μισό', lang="el"), 0.5)
        self.assertAlmostEqual(is_fractional('τρίτο', lang="el"), 1 / 3)
        self.assertEqual(is_fractional('τέταρτο', lang="el"), 0.25)
        self.assertFalse(is_fractional('γάτα', lang="el"))

    def test_is_ordinal(self):
        self.assertEqual(is_ordinal('πρώτος', lang="el"), 1)
        self.assertEqual(is_ordinal('δεύτερος', lang="el"), 2)
        self.assertEqual(is_ordinal('τρίτος', lang="el"), 3)
        self.assertFalse(is_ordinal('γάτα', lang="el"))

    def test_numbers_to_digits(self):
        self.assertEqual(numbers_to_digits('έχω είκοσι ένα γάτες', lang="el"),
                         'έχω 21 γάτες')


if __name__ == "__main__":
    unittest.main()
