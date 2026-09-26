"""A unit before a hundred multiplies it; a ten before a hundred starts a second number.

The SADA transcripts write two hundred as a unit two and the hundred ("اثنين مية
واثنين", 202), so a unit before مية builds the hundred, as ثلاث to تسع do. A ten
never builds one: "تلاتين مية وعشرين" is 30 and 120.
"""
import unittest

from ovos_number_parser import numbers_to_digits
from ovos_number_parser.numbers_ar import extract_numbers_ar


class TestHundredUnits(unittest.TestCase):
    def test_a_unit_two_builds_two_hundred(self):
        for text, values in (("اثنين مية واثنين", [202]),
                             ("كم إثنين مئة ألف كفو كفو", [200000]),
                             ("واحدة إثنين إثنين مئة و سبعة و خمسين", [1, 2, 257])):
            with self.subTest(text=text):
                self.assertEqual(extract_numbers_ar(text), values)

    def test_a_ten_before_a_hundred_starts_a_second_number(self):
        for text, values in (("تلاتين مية وعشرين", [30, 120]),
                             ("سبعه وخمسين مية واربعه", [57, 104]),
                             ("عشرين مية ريال", [20, 100])):
            with self.subTest(text=text):
                self.assertEqual(extract_numbers_ar(text), values)

    def test_the_digits_cut_where_the_numbers_do(self):
        for text, converted in (("عشرين ست مية", "20 600"),
                                ("تسعين خمس مية", "90 500"),
                                ("خمس مية خمس مية", "500 500"),
                                ("أبي خمس ميه خمس ميه", "أبي 500 500")):
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, lang="ar"), converted)
        self.assertIn("622", numbers_to_digits(
            "وعشرين ست مية واثنين وعشرين", lang="ar"))

    def test_a_unit_after_a_filled_hundred_joins_it(self):
        for text, values, converted in (
                ("كم سعره؟ مية و اربعة مية و اربعة", [104, 104], "كم سعره؟ 104 104"),
                ("مية واثنين مية واثنين", [102, 102], "102 102"),
                ("مية وخمس مية", [100, 500], "100 و500"),
                ("خمس مية وثلاث مية", [500, 300], "500 و300"),
                ("الف وميتين وخمس مية ريال", [1200, 500], "1200 و500 ريال")):
            with self.subTest(text=text):
                self.assertEqual(extract_numbers_ar(text), values)
                self.assertEqual(numbers_to_digits(text, lang="ar"), converted)

    def test_three_to_nine_build_a_hundred(self):
        for text, value in (("ثلاث مية ريال", 300), ("تلات مية", 300),
                            ("خمس مية ريال", 500), ("تسع مئة", 900),
                            ("ميتين ريال", 200), ("مية ريال", 100)):
            with self.subTest(text=text):
                self.assertEqual(extract_numbers_ar(text), [value])


if __name__ == "__main__":
    unittest.main()
