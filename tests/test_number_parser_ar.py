import unittest

from ovos_number_parser import (extract_number, pronounce_number,
                                pronounce_ordinal, pronounce_fraction,
                                is_fractional, is_ordinal, numbers_to_digits)


class TestArabicPronounce(unittest.TestCase):
    """Anchors for spoken Modern Standard Arabic numbers (masculine forms)."""

    def test_pronounce_number(self):
        expected = {
            0: 'صفر', 1: 'واحد', 2: 'اثنان', 3: 'ثلاثة', 4: 'أربعة',
            5: 'خمسة', 6: 'ستة', 7: 'سبعة', 8: 'ثمانية', 9: 'تسعة',
            10: 'عشرة', 11: 'أحد عشر', 12: 'اثنا عشر', 13: 'ثلاثة عشر',
            14: 'أربعة عشر', 15: 'خمسة عشر', 16: 'ستة عشر', 17: 'سبعة عشر',
            18: 'ثمانية عشر', 19: 'تسعة عشر', 20: 'عشرون',
            # units come before tens, joined by the conjunction و
            21: 'واحد وعشرون', 25: 'خمسة وعشرون', 30: 'ثلاثون',
            42: 'اثنان وأربعون', 50: 'خمسون', 66: 'ستة وستون', 70: 'سبعون',
            80: 'ثمانون', 90: 'تسعون', 99: 'تسعة وتسعون', 100: 'مئة',
            101: 'مئة وواحد', 123: 'مئة وثلاثة وعشرون',
            # duals
            200: 'مئتان', 2000: 'ألفان', 2000000: 'مليونان',
            300: 'ثلاثمئة', 500: 'خمسمئة', 999: 'تسعمئة وتسعة وتسعون',
            1000: 'ألف', 1985: 'ألف وتسعمئة وخمسة وثمانون',
            2023: 'ألفان وثلاثة وعشرون',
            # scale nouns are masculine, 3-10 take the ة-marked numeral
            3000: 'ثلاثة آلاف', 10000: 'عشرة آلاف', 100000: 'مئة ألف',
            1000000: 'مليون', 3000000: 'ثلاثة ملايين',
            1000000000: 'مليار',
        }
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="ar"), spoken)

    def test_pronounce_negative_and_decimal(self):
        expected = {-7: 'سالب سبعة', -42: 'سالب اثنان وأربعون',
                    5.2: 'خمسة فاصلة اثنان',
                    5.25: 'خمسة فاصلة اثنان خمسة',
                    0.5: 'صفر فاصلة خمسة',
                    -3.5: 'سالب ثلاثة فاصلة خمسة'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="ar"), spoken)

    def test_pronounce_ordinal(self):
        expected = {1: 'الأول', 2: 'الثاني', 3: 'الثالث', 4: 'الرابع',
                    5: 'الخامس', 6: 'السادس', 7: 'السابع', 8: 'الثامن',
                    9: 'التاسع', 10: 'العاشر', 11: 'الحادي عشر',
                    12: 'الثاني عشر', 20: 'العشرون',
                    21: 'الحادي والعشرون', 25: 'الخامس والعشرون',
                    30: 'الثلاثون', 100: 'المئة', 1000: 'الألف'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_ordinal(number, lang="ar"), spoken)

    def test_pronounce_fraction(self):
        self.assertEqual(pronounce_fraction("1/2", lang="ar"), 'نصف')
        self.assertEqual(pronounce_fraction("1/3", lang="ar"), 'ثلث')
        self.assertEqual(pronounce_fraction("1/4", lang="ar"), 'ربع')
        self.assertEqual(pronounce_fraction("2/3", lang="ar"), 'ثلثان')
        self.assertEqual(pronounce_fraction("3/4", lang="ar"), 'ثلاثة أرباع')


class TestArabicExtract(unittest.TestCase):
    """Anchors for extracting numbers from Arabic text."""

    def test_extract_number(self):
        expected = {
            0: 'صفر', 1: 'واحد', 2: 'اثنان', 3: 'ثلاثة', 10: 'عشرة',
            11: 'أحد عشر', 12: 'اثنا عشر', 15: 'خمسة عشر', 20: 'عشرون',
            25: 'خمسة وعشرون', 99: 'تسعة وتسعون', 100: 'مئة',
            123: 'مئة وثلاثة وعشرون', 200: 'مئتان', 1000: 'ألف',
            2000: 'ألفان', 3000: 'ثلاثة آلاف', 1000000: 'مليون',
        }
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="ar"), number)

    def test_extract_gender_and_case_variants(self):
        # numbers 3-10 show gender polarity: both genders are accepted
        expected = {1: 'واحدة', 2: 'اثنتان', 3: 'ثلاث', 4: 'أربع',
                    5: 'خمس', 8: 'ثمان', 10: 'عشر',
                    # oblique case endings
                    22: 'اثنين وعشرين', 200: 'مئتين', 2000: 'ألفين',
                    # alternative hundred spelling and unfused hundreds
                    100: 'مائة', 300: 'ثلاث مئة', 400: 'أربعمائة',
                    # feminine teens
                    11: 'إحدى عشرة', 13: 'ثلاث عشرة'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="ar"), number)

    def test_extract_negative_and_decimal(self):
        expected = {-7: 'سالب سبعة', -9: 'ناقص تسعة',
                    -42: 'سالب اثنان وأربعون',
                    5.2: 'خمسة فاصلة اثنان',
                    5.25: 'خمسة فاصلة خمسة وعشرون',
                    3.14: 'ثلاثة فاصلة واحد أربعة',
                    5.5: 'خمسة ونصف', 2.25: 'اثنان وربع',
                    0.5: 'نصف', 0.25: 'ربع'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertAlmostEqual(extract_number(spoken, lang="ar"),
                                       number)

    def test_extract_eastern_digits(self):
        # Eastern Arabic-Indic digits and the ٫ decimal separator
        self.assertEqual(extract_number("٢٥", lang="ar"), 25)
        self.assertEqual(extract_number("لدي ٣ قطط", lang="ar"), 3)
        self.assertAlmostEqual(extract_number("٥٫٢", lang="ar"), 5.2)
        self.assertEqual(extract_number("١٩٨٥", lang="ar"), 1985)

    def test_extract_from_sentence(self):
        self.assertEqual(extract_number("لدي خمسة وعشرون كتاباً", lang="ar"),
                         25)
        self.assertEqual(extract_number("اشتريت ثلاث تفاحات", lang="ar"), 3)
        self.assertEqual(
            extract_number("هذا هو اليوم الثالث", lang="ar", ordinals=True), 3)
        self.assertEqual(
            extract_number("الخامس والعشرون", lang="ar", ordinals=True), 25)

    def test_no_number(self):
        self.assertIn(extract_number("مرحبا كيف حالك", lang="ar"),
                      (False, None))
        self.assertIn(extract_number("", lang="ar"), (False, None))

    def test_is_fractional(self):
        self.assertEqual(is_fractional("نصف", lang="ar"), 0.5)
        self.assertEqual(is_fractional("ربع", lang="ar"), 0.25)
        self.assertEqual(is_fractional("الربع", lang="ar"), 0.25)
        self.assertAlmostEqual(is_fractional("ثلث", lang="ar"), 1 / 3)
        self.assertAlmostEqual(is_fractional("خمس", lang="ar"), 0.2)
        self.assertAlmostEqual(is_fractional("عشر", lang="ar"), 0.1)
        self.assertFalse(is_fractional("كتاب", lang="ar"))

    def test_is_ordinal(self):
        self.assertEqual(is_ordinal("الأول", lang="ar"), 1)
        self.assertEqual(is_ordinal("الأولى", lang="ar"), 1)
        self.assertEqual(is_ordinal("الثالثة", lang="ar"), 3)
        self.assertEqual(is_ordinal("الحادي عشر", lang="ar"), 11)
        self.assertEqual(is_ordinal("الخامس والعشرون", lang="ar"), 25)
        self.assertFalse(is_ordinal("مرحبا", lang="ar"))

    def test_numbers_to_digits(self):
        self.assertEqual(
            numbers_to_digits("لدي خمسة وعشرون قطة", lang="ar"),
            "لدي 25 قطة")


class TestArabicRoundTrip(unittest.TestCase):
    """pronounce_number output must be understood by extract_number."""

    def test_round_trip(self):
        numbers = list(range(0, 200)) + [
            201, 222, 300, 345, 400, 456, 500, 678, 700, 891, 900, 999,
            1000, 1001, 1234, 1985, 2000, 2023, 3000, 5000, 9999, 10000,
            11000, 15000, 100000, 123456, 1000000, 2000000, 3000000,
            1000000000, 2000000000]
        for number in numbers:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="ar")
                self.assertEqual(extract_number(spoken, lang="ar"), number)

    def test_round_trip_negative_and_decimal(self):
        for number in [-7, -42, -100, 2.5, 3.14, 5.2, -3.5, 0.5, 5.25,
                       0.75, 12.34]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="ar")
                self.assertAlmostEqual(extract_number(spoken, lang="ar"),
                                       number)

    def test_round_trip_ordinals(self):
        for number in range(1, 100):
            with self.subTest(number=number):
                spoken = pronounce_ordinal(number, lang="ar")
                self.assertEqual(is_ordinal(spoken, lang="ar"), number)


if __name__ == "__main__":
    unittest.main()
