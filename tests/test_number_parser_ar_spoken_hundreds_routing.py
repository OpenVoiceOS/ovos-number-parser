"""The public Arabic readers read the spoken hundreds of the Gulf, Egyptian and
Levantine lects: ميتين, ثلاثمية .. تسعمية. Each expected value is hand
arithmetic on the words; the test patches nothing.
"""
import unittest

from ovos_number_parser import extract_number, numbers_to_digits

#: spoken text, its value: 200; 300 + 10000 + 200; 600 + 10000 + 200;
#: 500 + 20000; 900; 100 + 20 and 2 of "ميتين"
CASES = [
    ("ميتين", 200),
    ("ثلاثمية", 300),
    ("تسعمية", 900),
    ("ثلاثمية وعشرة الف وميتين", 310200),
    ("خمسمية وعشرين الف", 520000),
    ("ميتين وخمسين", 250),
]


class TestSpokenHundreds(unittest.TestCase):

    def test_extract_number_reads_the_spoken_hundred(self):
        for text, value in CASES:
            for lang in ("ar", "ar-SA"):
                with self.subTest(text=text, lang=lang):
                    self.assertEqual(extract_number(text, lang), value)

    def test_numbers_to_digits_writes_the_whole_number(self):
        for text, value in CASES:
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, "ar"), str(value))


if __name__ == "__main__":
    unittest.main()
