import unittest

from ovos_number_parser.numbers_ru import (extract_number_ru,
                                           pronounce_number_ru)


class TestRussianNegativeCompound(unittest.TestCase):
    def test_negative_compound_numbers(self):
        # the sign must apply to the whole number, not just the first word
        self.assertEqual(
            extract_number_ru("минус тысяча двести тридцать четыре"), -1234)
        self.assertEqual(extract_number_ru("минус тысяча двести"), -1200)
        self.assertEqual(
            extract_number_ru("минус двести тридцать четыре"), -234)
        self.assertEqual(extract_number_ru("минус двести"), -200)

    def test_natural_sentence(self):
        self.assertEqual(
            extract_number_ru("температура минус двадцать один градус"), -21)

    def test_signed_roundtrip_to_one_million(self):
        bad = []
        for n in list(range(0, 3000)) + list(range(3000, 1000001, 997)):
            for m in (n, -n):
                if extract_number_ru(pronounce_number_ru(m)) != m:
                    bad.append(m)
        self.assertEqual(bad, [], f"round-trip failures: {bad[:10]}")


if __name__ == "__main__":
    unittest.main()
