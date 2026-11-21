import unittest

from ovos_number_parser import extract_number, numbers_to_digits, numtag_readers

from ovos_number_parser.numbers_en import (pronounce_number_en, is_fractional_en, is_ordinal_en)


class TestNumberParserEN(unittest.TestCase):
    def test_numbers_to_digits_en(self):
        self.assertEqual(numbers_to_digits('three billions', lang="en"), '3000000000')
        self.assertEqual(numbers_to_digits('two point five', lang="en"), '2.5')
        self.assertEqual(numbers_to_digits('two point forty two', lang="en"), '2.42')
        # with ordinals off, "fifth" is left as a word: it must never be
        # reinterpreted as the reciprocal 1/5 (this used to read "march 0.2")
        self.assertEqual(numtag_readers.numbers_to_digits('march fifth two thousand twenty five', "en", ordinals=False),
                         'march fifth 2025')
        self.assertEqual(numtag_readers.numbers_to_digits('march fifth', "en", ordinals=True),
                         'march 5')

    def test_numbers_to_digits_en_preserves_leading_zeros(self):
        # live bug: a standalone digit run that is already digits must pass
        # through byte-for-byte, not get re-parsed and lose leading zeros
        self.assertEqual(numbers_to_digits('code 007', lang="en"), 'code 007')
        self.assertEqual(
            numbers_to_digits('otp 4729 backup 007', lang="en"),
            'otp 4729 backup 007')


    def test_pronounce_number_en(self):
        self.assertEqual(pronounce_number_en(3840285766987249),
                         'three quadrillion, eight hundred and forty trillion, two hundred and eighty five billion, seven hundred '
                         'and sixty six million, nine hundred and eighty seven thousand, two hundred and forty nine')


    def test_extract_number_negative_en(self):
        # a negative sign must cover every place of a compound number,
        # not just the leading one
        self.assertEqual(extract_number("minus five", lang="en"), -5)
        self.assertEqual(extract_number("minus twenty three", lang="en"), -23)
        self.assertEqual(extract_number("minus one hundred", lang="en"), -100)
        self.assertEqual(extract_number("minus one hundred and five", lang="en"), -105)
        self.assertEqual(extract_number("minus nine hundred and ninety nine", lang="en"),
                         -999)
        self.assertEqual(extract_number("negative two million five hundred thousand", lang="en"),
                         -2500000)
        self.assertEqual(extract_number("minus one thousand nine", lang="en"), -1009)

    def test_extract_number_adversarial_en(self):
        self.assertFalse(extract_number("", lang="en"))
        self.assertFalse(extract_number("   ", lang="en"))
        self.assertFalse(extract_number("no digits here", lang="en"))
        # leading/trailing junk around a real number
        self.assertEqual(extract_number("set it to forty two please", lang="en"), 42)
        self.assertEqual(extract_number("MINUS FIVE", lang="en"), -5)


    def test_pronounce_number_default_cardinal_en(self):
        # 4-digit numbers pronounce as plain cardinals by default so they
        # round-trip; the year-style forms must not leak in.
        self.assertEqual(pronounce_number_en(1234),
                         "one thousand, two hundred and thirty four")
        self.assertEqual(pronounce_number_en(1010),
                         "one thousand, ten")
        self.assertEqual(pronounce_number_en(1900),
                         "one thousand, nine hundred")
        self.assertEqual(pronounce_number_en(1972),
                         "one thousand, nine hundred and seventy two")

    def test_pronounce_number_year_style_en(self):
        # date style is available on demand behind the explicit year flag.
        self.assertEqual(pronounce_number_en(1972, year=True),
                         "nineteen seventy two")
        self.assertEqual(pronounce_number_en(1010, year=True),
                         "ten ten")
        self.assertEqual(pronounce_number_en(1900, year=True),
                         "nineteen hundred")
        self.assertEqual(pronounce_number_en(1960, year=True),
                         "nineteen sixty")
        # values outside the date-styled band fall back to cardinal
        self.assertEqual(pronounce_number_en(2001, year=True),
                         "two thousand, one")

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
        self.assertEqual(numbers_to_digits("one hundred and one", lang="en"), "101")
        self.assertEqual(extract_number("one hundred and one", lang="en"), 101)
        cases = {
            "two hundred and five": ("205", 205),
            "nine hundred and ninety nine": ("999", 999),
            "one hundred and twenty one": ("121", 121),
            "three hundred and forty two": ("342", 342),
            "one thousand one hundred and one": ("1101", 1101),
        }
        for text, (digits, value) in cases.items():
            self.assertEqual(numbers_to_digits(text, lang="en"), digits, text)
            self.assertEqual(extract_number(text, lang="en"), value, text)

    def test_hundred_and_units_in_context(self):
        self.assertEqual(
            numbers_to_digits("it was one hundred and one degrees", lang="en"),
            "it was 101 degrees")

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
