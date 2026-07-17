import unittest

from ovos_number_parser.numbers_en import (
    numbers_to_digits_en,
    pronounce_number_en,
    extract_number_en,
    is_fractional_en,
    is_ordinal_en,
)


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


    def test_extract_number_spoken_en(self):
        self.assertEqual(extract_number_en("half"), 0.5)
        self.assertEqual(extract_number_en("three quarters"), 0.75)
        self.assertEqual(extract_number_en("a hundred"), 100)
        self.assertEqual(extract_number_en("one hundred and five"), 105)
        self.assertEqual(extract_number_en("two thousand and one"), 2001)
        self.assertEqual(extract_number_en("nine hundred and ninety nine"), 999)
        self.assertEqual(extract_number_en("two million five hundred thousand"),
                         2500000)

    def test_extract_number_negative_en(self):
        # a negative sign must cover every place of a compound number,
        # not just the leading one
        self.assertEqual(extract_number_en("minus five"), -5)
        self.assertEqual(extract_number_en("minus twenty three"), -23)
        self.assertEqual(extract_number_en("minus one hundred"), -100)
        self.assertEqual(extract_number_en("minus one hundred and five"), -105)
        self.assertEqual(extract_number_en("minus nine hundred and ninety nine"),
                         -999)
        self.assertEqual(extract_number_en("negative two million five hundred thousand"),
                         -2500000)
        self.assertEqual(extract_number_en("minus one thousand nine"), -1009)

    def test_extract_number_adversarial_en(self):
        self.assertFalse(extract_number_en(""))
        self.assertFalse(extract_number_en("   "))
        self.assertFalse(extract_number_en("no digits here"))
        # leading/trailing junk around a real number
        self.assertEqual(extract_number_en("set it to forty two please"), 42)
        self.assertEqual(extract_number_en("MINUS FIVE"), -5)

    def test_extract_number_roundtrip_en(self):
        # pronounce_number -> extract_number must recover the original integer.
        # 4-digit values in 1000..1999 are intentionally spoken in date style
        # ("nineteen seventy two"), so they are excluded from the sweep.
        def date_styled(n):
            s = str(abs(n))
            return (len(s) == 4 and
                    not (s[1:4] == '000' or s[1:3] == '00' or int(s[0:2]) >= 20))

        for n in list(range(-1050, 1050)) + [
                2001, 2020, 5678, 12345, 999999, 1000000, -1000000,
                -12345, 87654321]:
            if date_styled(n):
                continue
            spoken = pronounce_number_en(n)
            self.assertEqual(extract_number_en(spoken), n,
                             f"roundtrip failed for {n} -> {spoken!r}")

    def test_pronounce_number_boundaries_en(self):
        self.assertEqual(pronounce_number_en(0), "zero")
        self.assertEqual(pronounce_number_en(-1), "minus one")
        self.assertEqual(pronounce_number_en(1000000), "one million")
        self.assertEqual(pronounce_number_en(0.5), "zero point five")
        self.assertEqual(pronounce_number_en(-3.5), "minus three point five")

    def test_fractional_and_ordinal_en(self):
        self.assertEqual(is_fractional_en("half"), 0.5)
        self.assertEqual(is_fractional_en("quarter"), 0.25)
        self.assertFalse(is_fractional_en("banana"))
        self.assertEqual(is_ordinal_en("first"), 1)
        self.assertEqual(is_ordinal_en("fifth"), 5)
        self.assertFalse(is_ordinal_en("seven"))

    def test_large_ordinals_short_scale(self):
        # scale words must be looked up by place value (1000**group), not by
        # group index times 1000 — otherwise groups above thousands crash or
        # name the wrong scale
        cases = {
            1000000: "millionth",
            2000000: "two millionth",
            3000000: "three millionth",
            5000000: "five millionth",
            21000000: "twenty one millionth",
            1000000000: "billionth",
            2000000000: "two billionth",
            1000000000000: "trillionth",
        }
        for n, expected in cases.items():
            self.assertEqual(
                pronounce_number_en(n, ordinals=True, short_scale=True),
                expected, n)

    def test_large_ordinals_long_scale(self):
        cases = {
            1000000: "millionth",
            2000000: "two millionth",
            1000000000000: "billionth",
            2000000000000: "two billionth",
        }
        for n, expected in cases.items():
            self.assertEqual(
                pronounce_number_en(n, ordinals=True, short_scale=False),
                expected, n)

    def test_large_ordinals_do_not_raise(self):
        for n in range(1000000, 40000000, 1000000):
            pronounce_number_en(n, ordinals=True, short_scale=True)
            pronounce_number_en(n, ordinals=True, short_scale=False)


if __name__ == "__main__":
    unittest.main()
