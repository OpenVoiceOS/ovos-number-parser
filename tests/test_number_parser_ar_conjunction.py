import unittest

from ovos_number_parser import numbers_to_digits


class TestArabicNumbersToDigitsKeepsConjunction(unittest.TestCase):
    """The conjunction و attached to a number word that starts a new number
    means "and" and stays in the text, written onto the digits. Inside one
    number it joins the parts and the digits replace it."""

    def assertDigits(self, text, expected):
        self.assertEqual(numbers_to_digits(text, lang="ar"), expected)

    def test_new_number_keeps_conjunction(self):
        self.assertDigits("عندي سيارة وثلاث دراجات", "عندي سيارة و3 دراجات")
        self.assertDigits("جاء احمد وخمسين شخص", "جاء احمد و50 شخص")
        self.assertDigits("اشتريت كتاب وعشرة اقلام", "اشتريت كتاب و10 اقلام")

    def test_new_compound_number_keeps_conjunction(self):
        self.assertDigits("عندي كتاب وخمسة وعشرين قلم",
                          "عندي كتاب و25 قلم")

    def test_conjunction_at_start_of_text(self):
        self.assertDigits("وخمسة", "و5")

    def test_conjunction_before_trailing_punctuation(self):
        self.assertDigits("عندي وثلاث.", "عندي و3.")

    def test_two_numbers_joined_by_conjunction(self):
        self.assertDigits("ثلاثة وخمسة", "3 و5")
        self.assertDigits("ثلاثة و خمسة", "3 و5")

    def test_conjunction_inside_one_number_is_dropped(self):
        self.assertDigits("الف وخمسين", "1050")
        self.assertDigits("خمسة وعشرين", "25")
        self.assertDigits("الف وميت ريال", "1100 ريال")

    def test_eastern_digits_keep_conjunction(self):
        self.assertDigits("عندي سيارة و٣ دراجات", "عندي سيارة و3 دراجات")

    def test_word_starting_with_waw_is_not_split(self):
        self.assertDigits("قلم وواحد", "قلم و1")
        self.assertDigits("وصلت ومعي ثلاثة", "وصلت ومعي 3")


if __name__ == "__main__":
    unittest.main()
