"""Gulf and Saudi number joins in transcripts: او as the conjunction, the
construct hundred ميت, and a proclitic written onto a number word."""
import unittest

from ovos_number_parser import extract_number, numbers_to_digits
from ovos_number_parser.numbers_ar import extract_numbers_ar


def extract_number_ar(text):
    return extract_number(text, lang="ar")


class TestArabicGulfNumberJoins(unittest.TestCase):
    def test_transcript_rows(self):
        rows = {
            "ست مية او عشرة الف وميتين": 610200,
            "ثلاثمية او عشرة الف وميتين": 310200,
            "الف وميت ريال": 1100,
            "بالفين وستة وعشرين": 2026,
        }
        for text, value in rows.items():
            self.assertEqual(extract_number_ar(text), value, text)

    def test_or_joins_a_larger_place_before_a_smaller_one(self):
        self.assertEqual(extract_number_ar("خمسمية او عشرين الف"), 520000)

    def test_or_between_equal_magnitudes_stays_or(self):
        self.assertEqual(extract_number_ar("الف او الفين"), 1000)
        self.assertEqual(extract_number_ar("ثلاثة او اربعة"), 3)
        self.assertEqual(extract_number_ar("مية او مية وخمسين"), 100)
        self.assertEqual(extract_number_ar("عشرين او ثلاثين"), 20)
        self.assertEqual(extract_number_ar("ثلاثمية او اربعمية"), 300)

    def test_or_after_a_hundred_needs_a_scale_word_after_it(self):
        # "a hundred or two", "a hundred or twenty": two amounts
        self.assertEqual(extract_number_ar("مية او اثنين"), 100)
        self.assertEqual(extract_number_ar("مية او عشرين"), 100)

    def test_or_does_not_join_a_scale_that_is_not_smaller(self):
        # "two or three thousand"
        self.assertEqual(extract_number_ar("الفين او ثلاث الاف"), 2000)

    def test_or_after_a_scale_word_stays_or(self):
        # two price options, and "two or three thousand"
        self.assertEqual(extract_number_ar("الف او خمسمية"), 1000)
        self.assertEqual(extract_number_ar("الفين او ثلاثة"), 2000)

    def test_construct_hundred_after_the_conjunction(self):
        self.assertEqual(extract_number_ar("الفين وميت"), 2100)
        self.assertEqual(extract_number_ar("الف وميتين"), 1200)

    def test_construct_hundred_alone_is_no_number(self):
        self.assertFalse(extract_number_ar("رجل ميت"))
        self.assertFalse(extract_number_ar("ميت ريال"))
        self.assertFalse(extract_number_ar("حي وميت"))

    def test_proclitic_on_a_number_word(self):
        self.assertEqual(extract_number_ar("بخمسمية"), 500)
        self.assertEqual(extract_number_ar("بمية"), 100)
        self.assertEqual(extract_number_ar("لالف"), 1000)
        self.assertEqual(extract_number_ar("للالف"), 1000)
        self.assertEqual(extract_number_ar("فخمسة"), 5)
        self.assertEqual(extract_number_ar("والفين"), 2000)

    def test_proclitic_leaves_ordinary_words_alone(self):
        for word in ("ليرة", "بيت", "فلوس", "ولد", "لست", "بثمن"):
            self.assertFalse(extract_number_ar(word), word)

    def test_proclitic_leaves_water_and_per_cent_alone(self):
        # ميه is also "water": بميه is "with water"
        self.assertFalse(extract_number_ar("بميه"))
        # the hundred with the article after ب is "per cent"
        self.assertEqual(extract_numbers_ar("عشرة بالمية"), [10])
        self.assertEqual(extract_numbers_ar("عشرة بالمئة"), [10])

    def test_proclitic_stays_on_the_digits(self):
        self.assertEqual(numbers_to_digits("دفعت بالفين", lang="ar"),
                         "دفعت ب2000")
        self.assertEqual(numbers_to_digits("ما جاء لاحد", lang="ar"),
                         "ما جاء لاحد")

    def test_controls_keep_their_result(self):
        self.assertEqual(extract_number_ar("مية واربعين الف وسبعماية"),
                         140700)
        self.assertEqual(extract_number_ar("اربعماية الف"), 400000)


if __name__ == "__main__":
    unittest.main()
