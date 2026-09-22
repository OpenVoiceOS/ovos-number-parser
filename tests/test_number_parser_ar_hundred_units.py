"""Only the units three to nine build a hundred.

100 is مية on its own and 200 the dual ميتين; no unit comes before مية for
either (Qafisheh 1970, p. 59; Omar 1975, p. 69). "اتنين مية" is two numbers.
"""
import unittest

from ovos_number_parser import numbers_to_digits
from ovos_number_parser.numbers_ar import extract_numbers_ar


class TestHundredUnits(unittest.TestCase):
    def test_one_and_two_do_not_build_a_hundred(self):
        for text, values, converted in (
                ("اتنين مية ريال", [2, 100], "2 100 ريال"),
                ("اثنين مية ريال", [2, 100], "2 100 ريال"),
                ("واحد مية ريال", [1, 100], "1 100 ريال"),
                ("اثنين مئة", [2, 100], "2 100"),
                ("عشرين مية ريال", [20, 100], "20 100 ريال")):
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
