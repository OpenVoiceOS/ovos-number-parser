"""ميه is the hundred مية spelled with ه, and a homograph of water like it.

The SADA transcripts ("SADA - SBA & SDAIA Audio Dataset for Arabic", 2023,
transcribed by hand) write ميه for the hundred ("خمس ميه", "ميه وخمسين",
"ميه الف"); English Wiktionary gives it as the Egyptian spelling of مية
"water". It is read by the same context rules as مية, so no number is split.
"""
import re
import unittest

from ovos_number_parser import extract_number, numbers_to_digits
from ovos_number_parser.numbers_ar import extract_numbers_ar


def digits(text):
    return numbers_to_digits(text, lang="ar")


AS_WRITTEN = ("شربت ميه", "كباية ميه", "الميه سخنة", "الميه", "دفعت ميه",
              "ميه سيارة", "الست ميه ريال")

LICENSED = (
    ("ميه ريال", [100], "100 ريال"),
    ("خمس ميه", [500], "500"),
    ("خمسميه", [500], "500"),
    ("الف وميه", [1100], "1100"),
    ("ميه وخمسين", [150], "150"),
    ("ميه وخمسين الف", [150000], "150000"),
    ("السعر ميه وعشرين", [120], "السعر 120"),
    ("سبع ميه وخمسة", [705], "705"),
    ("ميه الف", [100000], "100000"),
    ("ميه في الميه", [100], "100 في الميه"),
    ("عشرة بالميه", [10], "10 بالميه"),
    ("ميه", [100], "100"),
)


class TestMeeh(unittest.TestCase):
    def test_water_stays_as_written(self):
        for text in AS_WRITTEN:
            with self.subTest(text=text):
                self.assertEqual(extract_numbers_ar(text), [])
                self.assertEqual(digits(text), text)

    def test_the_hundred_in_a_number_context(self):
        for text, values, converted in LICENSED:
            with self.subTest(text=text):
                self.assertEqual(extract_numbers_ar(text), values)
                self.assertEqual(digits(text), converted)

    def test_a_number_is_never_split(self):
        for text, values, _ in LICENSED:
            with self.subTest(text=text):
                found = [float(d) for d in re.findall(r"\d+", digits(text))]
                self.assertEqual(found, [float(v) for v in values])

    def test_a_word_ending_in_the_letters_is_no_number(self):
        for word in ("كميه", "اسلاميه", "علميه"):
            with self.subTest(word=word):
                self.assertFalse(extract_number(word, lang="ar"))


if __name__ == "__main__":
    unittest.main()
