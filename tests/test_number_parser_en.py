import unittest

from ovos_number_parser.numbers_en import numbers_to_digits_en, pronounce_number_en


class TestNumberParserEN(unittest.TestCase):
    def test_numbers_to_digits_en(self):
        self.assertEqual(numbers_to_digits_en('three billions'), '3000000000.0')
        self.assertEqual(numbers_to_digits_en('two point five'), '2.5')
        self.assertEqual(numbers_to_digits_en('two point forty two'), '2.42')
        self.assertEqual(numbers_to_digits_en('march fifth two thousand twenty five', ordinals=False),
                         'march 0.2 2025')
        self.assertEqual(numbers_to_digits_en('march fifth', ordinals=True),
                         'march 5')

    @unittest.expectedFailure
    def test_failures_numbers_to_digits_en(self):
        # TODO: fix me
        self.assertEqual(numbers_to_digits_en('march fifth two thousand twenty five', ordinals=True),
                         'march 5 2025')
        self.assertEqual(numbers_to_digits_en('two point four two'), '2.42')

    def test_pronounce_number_en(self):
        self.assertEqual(pronounce_number_en(3840285766987249),
                         'three quadrillion, eight hundred and forty trillion, two hundred and eighty five billion, seven hundred '
                         'and sixty six million, nine hundred and eighty seven thousand, two hundred and forty nine')


if __name__ == "__main__":
    unittest.main()
