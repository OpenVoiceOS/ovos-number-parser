import unittest

from ovos_number_parser import extract_number, pronounce_number, is_fractional


class TestRussianPronounce(unittest.TestCase):
    """Anchors for spoken Russian numbers."""

    def test_pronounce_number(self):
        expected = {0: 'ноль', 1: 'один', 2: 'два', 3: 'три', 4: 'четыре', 5: 'пять', 6: 'шесть', 7: 'семь', 8: 'восемь', 9: 'девять', 10: 'десять', 11: 'одиннадцать', 12: 'двенадцать', 13: 'тринадцать', 14: 'четырнадцать', 15: 'пятнадцать', 16: 'шестнадцать', 17: 'семнадцать', 18: 'восемнадцать', 19: 'девятнадцать', 20: 'двадцать', 21: 'двадцать один', 30: 'тридцать', 42: 'сорок два', 50: 'пятьдесят', 66: 'шестьдесят шесть', 70: 'семьдесят', 80: 'восемьдесят', 90: 'девяносто', 99: 'девяносто девять', 100: 'сто', 101: 'сто один', 123: 'сто двадцать три', 200: 'двести', 500: 'пятьсот', 999: 'девятьсот девяносто девять', 1000: 'тысяча', 2000: 'две тысячи', 2023: 'две тысячи двадцать три', 1000000: 'миллион', 2000000: 'два миллиона'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="ru"), spoken)

    def test_pronounce_negative_and_decimal(self):
        expected = {-7: 'минус семь', -42: 'минус сорок два', 2.5: 'два точка пять', 3.14: 'три точка один четыре', -3.5: 'минус три точка пять', 0.5: 'ноль точка пять'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="ru"), spoken)


class TestRussianExtract(unittest.TestCase):
    """Anchors for extracting numbers from Russian text."""

    def test_extract_number(self):
        expected = {0: 'ноль', 1: 'один', 2: 'два', 3: 'три', 4: 'четыре', 5: 'пять', 6: 'шесть', 7: 'семь', 8: 'восемь', 9: 'девять', 10: 'десять', 11: 'одиннадцать', 12: 'двенадцать', 13: 'тринадцать', 14: 'четырнадцать', 15: 'пятнадцать', 16: 'шестнадцать', 17: 'семнадцать', 18: 'восемнадцать', 19: 'девятнадцать', 20: 'двадцать', 21: 'двадцать один', 30: 'тридцать', 42: 'сорок два', 50: 'пятьдесят', 66: 'шестьдесят шесть', 70: 'семьдесят', 80: 'восемьдесят', 90: 'девяносто', 99: 'девяносто девять', 100: 'сто', 101: 'сто один', 123: 'сто двадцать три', 200: 'двести', 500: 'пятьсот', 999: 'девятьсот девяносто девять', 1000: 'тысяча', 2000: 'две тысячи', 2023: 'две тысячи двадцать три', 1000000: 'миллион', 2000000: 'два миллиона'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="ru"), number)

    def test_extract_negative_and_decimal(self):
        expected = {-7: 'минус семь', -42: 'минус сорок два', 2.5: 'два точка пять', 3.14: 'три точка один четыре', -3.5: 'минус три точка пять', 0.5: 'ноль точка пять'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="ru"), number)

    def test_extract_from_sentence(self):
        self.assertEqual(extract_number('у меня двадцать один кошек', lang="ru"),
                         21)

    def test_no_number(self):
        self.assertIn(extract_number("привет как дела", lang="ru"), (False, None))


class TestRussianRoundTrip(unittest.TestCase):
    """pronounce_number output must be understood by extract_number."""

    def test_round_trip(self):
        for number in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 201, 222, 300, 345, 400, 456, 500, 678, 700, 891, 900, 1000, 1001, 1234, 2000, 2023, 5000, 9999, 10000, 100000, 1000000, 2000000]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="ru")
                self.assertEqual(extract_number(spoken, lang="ru"), number)

    def test_round_trip_negative_and_decimal(self):
        for number in [-7, -42, 2.5, 3.14, -3.5, 0.5]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="ru")
                self.assertEqual(extract_number(spoken, lang="ru"), number)


class TestRussianDeclinedForms(unittest.TestCase):
    """Case-inflected number words as they appear in natural speech."""

    def test_one_declensions(self):
        # "один" declines by gender/case; all still mean the value 1
        for phrase in ["один", "одна", "одно", "одной", "одним",
                       "одну", "одною"]:
            with self.subTest(phrase=phrase):
                self.assertEqual(extract_number(phrase, lang="ru"), 1)

    def test_one_in_context(self):
        # accusative feminine "одну" is the common spoken form for durations
        self.assertEqual(
            extract_number("напомни через одну минуту", lang="ru"), 1)
        self.assertEqual(
            extract_number("подожди одну секунду", lang="ru"), 1)
        self.assertEqual(
            extract_number("у меня одна кошка", lang="ru"), 1)
        self.assertEqual(
            extract_number("дай мне одну книгу", lang="ru"), 1)

    def test_two_declensions(self):
        for phrase in ["два", "две", "двух", "двум", "двумя"]:
            with self.subTest(phrase=phrase):
                self.assertEqual(extract_number(phrase, lang="ru"), 2)

    def test_two_in_context(self):
        self.assertEqual(
            extract_number("около двух часов", lang="ru"), 2)
        self.assertEqual(
            extract_number("две тысячи двадцать четыре", lang="ru"), 2024)


class TestRussianAdversarial(unittest.TestCase):
    """Malformed, empty and junk inputs must never raise."""

    def test_empty_and_whitespace(self):
        for text in ["", "   ", "\n\t"]:
            with self.subTest(text=repr(text)):
                self.assertIn(extract_number(text, lang="ru"), (False, None))

    def test_junk_and_punctuation(self):
        for text in ["!!!", "@#$", "тест привет", "..."]:
            with self.subTest(text=text):
                self.assertIn(extract_number(text, lang="ru"), (False, None))

    def test_lang_code_variants(self):
        for lang in ["ru", "ru-ru", "ru-RU"]:
            with self.subTest(lang=lang):
                self.assertEqual(
                    extract_number("сорок два", lang=lang), 42)

    def test_number_among_words_keeps_value(self):
        # only part of the string is a number
        self.assertEqual(
            extract_number("поставь будильник на семь", lang="ru"), 7)
        self.assertEqual(
            extract_number("осталось двадцать три дня", lang="ru"), 23)


class TestRussianFractions(unittest.TestCase):
    """Fraction nouns, singular citation form and inflected plurals."""

    def test_singular_forms(self):
        self.assertEqual(is_fractional("целая", lang="ru"), 1.0)
        self.assertEqual(is_fractional("пятая", lang="ru"), 0.2)
        self.assertEqual(is_fractional("десятая", lang="ru"), 0.1)
        self.assertEqual(is_fractional("сотая", lang="ru"), 0.01)

    def test_plural_forms_normalize_to_singular(self):
        # "две пятые" = 2/5, "три пятых" = 3/5 -> each fifth is 1/5
        self.assertEqual(is_fractional("пятые", lang="ru"), 0.2)
        self.assertEqual(is_fractional("пятых", lang="ru"), 0.2)
        self.assertEqual(is_fractional("десятые", lang="ru"), 0.1)
        self.assertEqual(is_fractional("десятых", lang="ru"), 0.1)

    def test_non_fraction_returns_false(self):
        for word in ["", "привет", "пять", "целые", "тые"]:
            with self.subTest(word=word):
                self.assertFalse(is_fractional(word, lang="ru"))


if __name__ == "__main__":
    unittest.main()
