import unittest
from ovos_number_parser.numbers_da import numbers_to_digits_da, pronounce_number_da, pronounce_ordinal_da


class TestNumberParserDA(unittest.TestCase):
    def test_numbers_to_digits_da(self):
        self.assertEqual(numbers_to_digits_da('tre billiarder'), '3000000000000000.0')
        self.assertEqual(numbers_to_digits_da('den fjerde marts totusinde og femogtyve', ordinals=False),
                         'den fjerde marts 2025')
        self.assertEqual(numbers_to_digits_da('den fjerde marts totusinde og femogtyve', ordinals=True),
                         'den 4 marts 2025')
        self.assertEqual(numbers_to_digits_da('to komma fem'), '2.5')
        self.assertEqual(numbers_to_digits_da('to komma fire to'), '2.42')

    def test_pronounce_number_da(self):
        self.assertEqual(pronounce_number_da(3840285766987249),
            'tre billiarder ottehundredefyrre billioner tohundredefemogfirs milliarder '
            'syvhundredeseksogtres millioner nihundredesyvogfirstusindetohundredeniogfyrre')
        # test endings, singular vs plural
        self.assertEqual(pronounce_number_da(1000000), 'en million ')
        self.assertEqual(pronounce_number_da(2000000), 'to millioner ')


if __name__ == "__main__":
    unittest.main()
