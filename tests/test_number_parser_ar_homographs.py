"""A word that is also an everyday word is a number only when its context
makes it unambiguous; otherwise it is left as written.

English Wiktionary gives each everyday sense: مية "water" (Egyptian, South
Levantine), ميتين "plural of ميّت" dead (Egyptian), ميت "dead", الست "woman",
"lady" (Egyptian), التلات "Tuesday" (Moroccan) and الاثنين "Monday" (Arabic,
Hijazi).
"""
import re
import unittest

from ovos_number_parser import extract_number, numbers_to_digits
from ovos_number_parser.numbers_ar import extract_numbers_ar


def digits(text):
    return numbers_to_digits(text, lang="ar")


AS_WRITTEN = (
    "كباية مية", "المية سخنة", "شربت مية", "ناس ميتين", "الناس دول ميتين",
    "يوم التلات", "الاثنين الجاي", "الست جات", "دفعت مية", "مية سيارة",
    "مية شخص", "مية كاش", "الموعد يوم التلات الجاي", "يوم الاثنين",
    "يوم الاتنين", "ويوم التلاتة", "الست سيارات", "المية", "الميتين",
    "رجل ميت", "حي وميت", "الست مية", "ميت مية", "مية وميت",
    "التلات مية ريال", "الست مية ريال", "التلات مئة")

LICENSED = (
    ("مية ريال", [100], "100 ريال"),
    ("مية كيلو", [100], "100 كيلو"),
    ("مية متر", [100], "100 متر"),
    ("ميتين كيلو", [200], "200 كيلو"),
    ("مية بالمية", [100], "100 بالمية"),
    ("مية في المية", [100], "100 في المية"),
    ("مية %", [100], "100 %"),
    ("تمويل مية بالمية", [100], "تمويل 100 بالمية"),
    ("خمس مية", [500], "500"),
    ("مية الف", [100000], "100000"),
    ("الف ومية", [1100], "1100"),
    ("الف وميتين", [1200], "1200"),
    ("مية وخمسين", [150], "150"),
    ("التلات الف", [3000], "3000"),
    ("مية", [100], "100"),
    ("ميتين", [200], "200"),
    ("الست", [6], "6"),
    ("الاثنين", [2], "2"),
    ("المية الف", [100000], "100000"),
    ("دفعت الميتين الف", [200000], "دفعت 200000"),
    ("دفعت الميتين ريال", [200], "دفعت 200 ريال"),
    ("المية ريال اللي دفعتها", [100], "100 ريال اللي دفعتها"),
    ("الست ساعات", [6], "6 ساعات"),
    ("ميت الف", [100000], "100000"),
    ("ميت ريال", [100], "100 ريال"),
    ("ثلاث مية ريال", [300], "300 ريال"),
    ("الاتنين مية ريال", [100], "الاتنين 100 ريال"),
    ("يوم التلات مية ريال", [100], "يوم التلات 100 ريال"),
    ("ميت مية ريال", [100], "ميت 100 ريال"),
    ("ست مية او عشرة الف", [600, 10000], "600 او 10000"),
)


class TestLeftAsWritten(unittest.TestCase):
    def test_no_number(self):
        for text in AS_WRITTEN:
            with self.subTest(text=text):
                self.assertEqual(extract_numbers_ar(text), [])
                self.assertEqual(digits(text), text)
        self.assertEqual(digits("شربت مية ودفعت مية ريال"),
                         "شربت مية ودفعت 100 ريال")

    def test_or_joins_nothing(self):
        # او is "or": the number after it is read, the homograph is not.
        # "كباية مية او اثنين" is "a glass of water, or two".
        for text, converted in (("مية او اثنين", "مية او 2"),
                                ("كباية مية او اثنين", "كباية مية او 2")):
            with self.subTest(text=text):
                self.assertEqual(extract_numbers_ar(text), [2])
                self.assertEqual(digits(text), converted)


class TestLicensed(unittest.TestCase):
    def test_numbers(self):
        for text, values, converted in LICENSED:
            with self.subTest(text=text):
                self.assertEqual(extract_numbers_ar(text), values)
                self.assertEqual(digits(text), converted)
        self.assertEqual(extract_number("بمية", lang="ar"), 100)

    def test_a_number_is_never_split(self):
        # the digits of a licensed phrase are its whole amount, never a part
        # of it standing alone ("المية 1000")
        for text, values, _ in LICENSED:
            with self.subTest(text=text):
                found = [float(d) for d in re.findall(r"\d+", digits(text))]
                self.assertEqual(found, [float(v) for v in values])

    def test_a_scale_word_is_never_read_without_its_homograph(self):
        # a scale word after a homograph always makes the homograph a number,
        # so the scale word is never read alone as a smaller number
        for word, value in (("مية", 100), ("المية", 100), ("ميتين", 200),
                            ("الميتين", 200), ("ميت", 100), ("التلات", 3),
                            ("الاتنين", 2), ("الاثنين", 2), ("الست", 6)):
            for scale, factor in (("الف", 1000), ("مليون", 1000000)):
                text = f"دفعت {word} {scale}"
                with self.subTest(text=text):
                    self.assertEqual(extract_numbers_ar(text),
                                     [value * factor])
        self.assertEqual(extract_numbers_ar("يوم التلات الف"), [3000])


if __name__ == "__main__":
    unittest.main()
