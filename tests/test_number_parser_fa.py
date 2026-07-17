import unittest

from ovos_number_parser import extract_number, pronounce_number
from ovos_number_parser.numbers_fa import (extract_numbers_fa,
                                           is_fractional_fa,
                                           pronounce_number_fa)


class TestPersianPronounce(unittest.TestCase):
    """Anchors for spoken Persian numbers."""

    def test_pronounce_number(self):
        expected = {0: 'صفر', 1: 'یک', 2: 'دو', 3: 'سه', 4: 'چهار', 5: 'پنج', 6: 'شش', 7: 'هفت', 8: 'هشت', 9: 'نه', 10: 'ده', 11: 'یازده', 12: 'دوازده', 13: 'سیزده', 14: 'چهارده', 15: 'پونزده', 16: 'شونزده', 17: 'هیفده', 18: 'هیجده', 19: 'نوزده', 20: 'بیست', 21: 'بیست و یک', 30: 'سی', 42: 'چهل و دو', 50: 'پنجاه', 66: 'شصت و شش', 70: 'هفتاد', 80: 'هشتاد', 90: 'نود', 99: 'نود و نه', 100: 'صد', 101: 'صد و یک', 123: 'صد و بیست و سه', 200: 'دویست', 500: 'پانصد', 999: 'نهصد و نود و نه', 1000: 'هزار', 2000: 'دو هزار', 2023: 'دو هزار و بیست و سه', 1000000: 'یک میلیون', 2000000: 'دو میلیون'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="fa"), spoken)

    def test_pronounce_negative_and_decimal(self):
        expected = {-7: 'منفی هفت', -42: 'منفی چهل و دو', 2.5: 'دو و نیم', 3.14: 'سه و چهارده صدم', -3.5: 'منفی سه و نیم', 0.5: 'نیم'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="fa"), spoken)


class TestPersianExtract(unittest.TestCase):
    """Anchors for extracting numbers from Persian text."""

    def test_extract_number(self):
        expected = {0: 'صفر', 1: 'یک', 2: 'دو', 3: 'سه', 4: 'چهار', 5: 'پنج', 6: 'شش', 7: 'هفت', 8: 'هشت', 9: 'نه', 10: 'ده', 11: 'یازده', 12: 'دوازده', 13: 'سیزده', 14: 'چهارده', 15: 'پونزده', 16: 'شونزده', 17: 'هیفده', 18: 'هیجده', 19: 'نوزده', 20: 'بیست', 21: 'بیست و یک', 30: 'سی', 42: 'چهل و دو', 50: 'پنجاه', 66: 'شصت و شش', 70: 'هفتاد', 80: 'هشتاد', 90: 'نود', 99: 'نود و نه', 100: 'صد', 101: 'صد و یک', 123: 'صد و بیست و سه', 200: 'دویست', 500: 'پانصد', 999: 'نهصد و نود و نه', 1000: 'هزار', 2000: 'دو هزار', 2023: 'دو هزار و بیست و سه', 1000000: 'یک میلیون', 2000000: 'دو میلیون'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="fa"), number)

    def test_extract_negative_and_decimal(self):
        expected = {-7: 'منفی هفت', -42: 'منفی چهل و دو', 2.5: 'دو و نیم', 3.14: 'سه و چهارده صدم', -3.5: 'منفی سه و نیم', 0.5: 'نیم'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="fa"), number)

    def test_extract_from_sentence(self):
        self.assertEqual(extract_number('من بیست و یک گربه دارم', lang="fa"),
                         21)

    def test_no_number(self):
        self.assertIn(extract_number("سلام چطوری", lang="fa"), (False, None))


class TestPersianRoundTrip(unittest.TestCase):
    """pronounce_number output must be understood by extract_number."""

    def test_round_trip(self):
        for number in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 201, 222, 300, 345, 400, 456, 500, 678, 700, 891, 900, 1000, 1001, 1234, 2000, 2023, 5000, 9999, 10000, 100000, 1000000, 2000000]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="fa")
                self.assertEqual(extract_number(spoken, lang="fa"), number)

    def test_round_trip_negative_and_decimal(self):
        for number in [-7, -42, 2.5, 3.14, -3.5, 0.5]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="fa")
                self.assertEqual(extract_number(spoken, lang="fa"), number)


class TestPersianEasternDigits(unittest.TestCase):
    """Persian (Eastern Arabic) digits must be understood."""

    def test_eastern_integer(self):
        self.assertEqual(extract_number("۲۱", lang="fa"), 21)

    def test_eastern_decimal(self):
        self.assertEqual(extract_number("۳.۱۴", lang="fa"), 3.14)

    def test_eastern_in_sentence(self):
        self.assertEqual(extract_number("من ۲۱ گربه دارم", lang="fa"), 21)

    def test_western_still_works(self):
        self.assertEqual(extract_number("21", lang="fa"), 21)


class TestPersianScientific(unittest.TestCase):
    """Scientific notation must not crash for a zero exponent."""

    def test_single_digit_exponent_zero(self):
        # mantissa 1..9 has exponent 0 -> value is just the mantissa
        self.assertEqual(pronounce_number_fa(5, scientific=True), "پنج")

    def test_one(self):
        self.assertEqual(pronounce_number_fa(1, scientific=True), "یک")

    def test_negative_exponent_zero(self):
        self.assertEqual(pronounce_number_fa(-3, scientific=True), "منفی سه")

    def test_zero(self):
        self.assertEqual(pronounce_number_fa(0, scientific=True), "صفر")

    def test_nonzero_exponent_unaffected(self):
        self.assertEqual(pronounce_number_fa(5000000, scientific=True),
                         "پنج ضرب در ده به توان شش")


class TestPersianNeverEmpty(unittest.TestCase):
    """pronounce_number must never yield an empty string."""

    def test_underflow_rounds_to_zero(self):
        # 0.001 underflows the default 2 decimal places
        self.assertEqual(pronounce_number_fa(0.001), "صفر")

    def test_exact_zero(self):
        self.assertEqual(pronounce_number_fa(0), "صفر")


class TestPersianExtractAdversarial(unittest.TestCase):
    """Boundary and malformed inputs."""

    def test_empty_string(self):
        self.assertIn(extract_number("", lang="fa"), (False, None))

    def test_only_junk(self):
        self.assertIn(extract_number("سلام دنیا", lang="fa"), (False, None))

    def test_multiple_numbers(self):
        self.assertEqual(extract_numbers_fa("دو گربه و سه سگ"), [2, 3])

    def test_negative_in_sentence(self):
        self.assertEqual(extract_number("منفی سه و چهارده صدم", lang="fa"),
                         -3.14)


class TestPersianFractional(unittest.TestCase):
    def test_third(self):
        self.assertAlmostEqual(is_fractional_fa("سوم"), 1.0 / 3.0)

    def test_half(self):
        self.assertEqual(is_fractional_fa("نیم"), 0.5)

    def test_not_a_fraction(self):
        self.assertIs(is_fractional_fa("گربه"), False)


class TestPersianBigRoundTrip(unittest.TestCase):
    def test_large_values(self):
        for number in [1234567, 1000000000, 1234567890, 999999999]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="fa")
                self.assertEqual(extract_number(spoken, lang="fa"), number)


if __name__ == "__main__":
    unittest.main()
