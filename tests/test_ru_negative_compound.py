import unittest

from ovos_number_parser import extract_number


class TestRussianNegativeCompound(unittest.TestCase):
    def test_negative_compound_numbers(self):
        # the sign must apply to the whole number, not just the first word
        self.assertEqual(
            extract_number("минус тысяча двести тридцать четыре", lang="ru"), -1234)
        self.assertEqual(extract_number("минус тысяча двести", lang="ru"), -1200)
        self.assertEqual(
            extract_number("минус двести тридцать четыре", lang="ru"), -234)
        self.assertEqual(extract_number("минус двести", lang="ru"), -200)

    def test_natural_sentence(self):
        self.assertEqual(
            extract_number("температура минус двадцать один градус", lang="ru"), -21)


if __name__ == "__main__":
    unittest.main()
