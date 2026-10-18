"""Saudi colloquial cardinals and the spoken half, keyed by the Najdi code ars.

The forms and their sources are in AR_LECT_FORMS["ars"] and on
_SPOKEN_HALF_LOOKUP. A caller selects them with lang="ars"; the BCP-47 code
ar-SA names the macrolanguage and keeps the literary words.
"""
import unittest

from ovos_number_parser import extract_number, numbers_to_digits, pronounce_number
from ovos_number_parser.numbers_ar import extract_numbers_ar


def say(number):
    return pronounce_number(number, lang="ars")


def read(text):
    return extract_number(text, lang="ars")


class TestNajdiCardinals(unittest.TestCase):
    def test_the_cited_words(self):
        for number, words in ((11, "احدعش"), (12, "ثنعش"), (13, "ثلاثطعش"),
                              (14, "اربعطعش"), (15, "خمسطعش"), (16, "ستطعش"),
                              (17, "سبعطعش"), (18, "ثمانطعش"), (19, "تسعطعش"),
                              (100, "مية"), (200, "ميتين"),
                              (300, "ثلاث مية"), (400, "اربع مية"),
                              (500, "خمس مية"), (600, "ست مية"),
                              (700, "سبع مية"), (800, "ثمان مية"),
                              (900, "تسع مية")):
            with self.subTest(number=number):
                self.assertEqual(say(number), words)

    def test_the_words_inside_a_composed_number(self):
        for number, words in ((112, "مية وثنعش"), (350, "ثلاث مية وخمسين"),
                              (2018, "ألفين وثمانطعش"),
                              (1200, "ألف وميتين"),
                              (2026, "ألفين وستة وعشرين"),
                              (1990, "ألف وتسع مية وتسعين"),
                              (100000, "مية ألف")):
            with self.subTest(number=number):
                self.assertEqual(say(number), words)

    def test_a_value_no_source_gives_keeps_the_literary_word(self):
        self.assertEqual(say(10), "عشرة")
        self.assertEqual(say(1000), "ألف")
        self.assertEqual(pronounce_number(15, lang="ars", gender="feminine"), "خمس عشرة")

    def test_the_macrolanguage_keeps_the_literary_words(self):
        for code in ("ar", "ar-SA", "arb"):
            with self.subTest(code=code):
                self.assertEqual(pronounce_number(12, lang=code), "اثنا عشر")
                self.assertEqual(pronounce_number(300, lang=code), "ثلاثمئة")

    def test_every_whole_number_to_ten_thousand_reads_back(self):
        for number in range(10001):
            spoken = say(number)
            self.assertEqual(read(spoken), number, spoken)

    def test_every_year_from_1990_to_2100_reads_back(self):
        for year in range(1990, 2101):
            spoken = say(year)
            self.assertEqual(read(spoken), year, spoken)


class TestSpokenHalf(unittest.TestCase):
    def test_after_and_a_unit_or_ten_it_is_a_half(self):
        for text, value in (("خمسة ونص", 5.5), ("ساعتين ونص", 2.5),
                            ("واحد وستين ونص", 61.5), ("خمسة و نص", 5.5),
                            ("خمسة ونص ريال", 5.5), ("ثنعش ونص", 12.5)):
            with self.subTest(text=text):
                self.assertEqual(read(text), value)

    def test_it_converts_to_digits(self):
        self.assertEqual(numbers_to_digits("خمسة ونص ريال", lang="ars"), "5.5 ريال")
        self.assertEqual(numbers_to_digits("الساعة ثلاثة ونص", lang="ars"), "الساعة 3.5")

    def test_after_a_hundred_or_a_thousand_it_is_left_unread(self):
        """Spoken, "مية ونص" is 150 and "الف ونص" 1500; no source read says so,
        so the half is not read rather than read as 100.5."""
        for text in ("مية ونص", "الف ونص", "ثلاثة الاف ونص", "خمس مية ونص",
                     "الف ومية ونص"):
            with self.subTest(text=text):
                values = extract_numbers_ar(text, lect="ars")
                self.assertTrue(all(v == int(v) for v in values), values)
                digits = numbers_to_digits(text, lang="ars")
                self.assertTrue(digits.endswith(" ونص"), digits)
                self.assertNotIn(".5", digits)

    def test_before_another_word_it_is_the_word_text(self):
        for text, values in (("خمسة ونص الكتاب", [5]), ("ثلاثة، ونص الكتاب", [3]),
                             ("خمسة ونص كتاب", [5]), ("نص", []), ("نص الرسالة", []),
                             ("الكتاب ونص المقال", []), ("خمسة نص", [5])):
            with self.subTest(text=text):
                self.assertEqual(extract_numbers_ar(text, lect="ars"), values)
        for text in ("نص الرسالة", "الكتاب ونص المقال", "خمسة ونص الكتاب"):
            with self.subTest(text=text):
                self.assertNotIn("5.5", numbers_to_digits(text, lang="ars"))

    def test_the_literary_standard_does_not_read_it(self):
        for text, value in (("خمسة ونص", 5), ("ثلاثة، ونص الكتاب", 3),
                            ("خمسة ونص الكتاب", 5)):
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, lang="ar"), value)
        self.assertEqual(numbers_to_digits("خمسة ونص", lang="ar"), "5 ونص")


class TestAndEleven(unittest.TestCase):
    def test_and_one_before_ten_after_a_conjunction_is_one_number(self):
        for text in ("مئة وواحد عشر", "مية وواحد عشر", "مية و واحد عشر",
                     "مئة و واحد عشر"):
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, lang="ar"), 111)
                self.assertEqual(numbers_to_digits(text, lang="ar"), "111")
        for text, value in (("ثلاثمية وواحد عشر", 311), ("الف وواحد عشر", 1011)):
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, lang="ar"), value)
                self.assertEqual(numbers_to_digits(text, lang="ar"), str(value))


if __name__ == "__main__":
    unittest.main()
