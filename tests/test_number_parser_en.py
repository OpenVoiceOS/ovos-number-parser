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

    def test_hundred_and_units_combine(self):
        # "X hundred and Y" is a single number: hundreds and units must fuse
        # into one value, never split into "1 101" style fragments
        self.assertEqual(numbers_to_digits_en("one hundred and one"), "101")
        self.assertEqual(extract_number_en("one hundred and one"), 101)
        cases = {
            "two hundred and five": ("205", 205),
            "nine hundred and ninety nine": ("999", 999),
            "one hundred and twenty one": ("121", 121),
            "three hundred and forty two": ("342", 342),
            "one thousand one hundred and one": ("1101", 1101),
        }
        for text, (digits, value) in cases.items():
            self.assertEqual(numbers_to_digits_en(text), digits, text)
            self.assertEqual(extract_number_en(text), value, text)

    def test_hundred_and_units_in_context(self):
        self.assertEqual(
            numbers_to_digits_en("it was one hundred and one degrees"),
            "it was 101 degrees")


if __name__ == "__main__":
    unittest.main()
