"""Every teen spelling a fetched source attests reads as its number.

Qafisheh, Basic Gulf Arabic (1970), p. 153: "arbaʕtaʕʃ 14". English
Wiktionary, the numeral entries of Egyptian, Gulf, Iraqi, South and North
Levantine and Moroccan Arabic, with the alternative and attributive forms
each lists. Which lect wrote a spelling does not change its value.
"""
import unittest

from ovos_number_parser import extract_number, numbers_to_digits


class TestAttestedTeens(unittest.TestCase):
    def test_every_attested_spelling(self):
        expected = {
            11: ["هدعش", "إدعش", "إدعشر", "إيدعش", "حداش", "حداشل"],
            12: ["اثنعش", "تنعش", "إطنو", "اطنعش", "اطنو", "طنعش", "طنعشر", "تناش", "تناشر", "تناشل"],
            13: ["تلاتاشر", "تلتعش", "تلتطعش", "تلتطعشر", "تلتاش", "تلتاشل", "تلطاش"],
            14: ["اربعتعش", "أربعتعش", "أربعتاش", "أربعطاش", "ربعتاش", "ربعتاشر", "ربعتاشل", "ربعطاش"],
            15: ["خمستعش", "خمستاش", "خمستاشل", "خمسطاش"],
            16: ["ستعش", "ستاش", "ستاشل", "سطاش"],
            17: ["سبعتعش", "سبعتاش", "سبعتاشل", "سبعطاش"],
            18: ["تمنتعش", "تمنتاش", "تمنتاشل", "تمنطاش"],
            19: ["تسعتعش", "تسعتاش", "تسعتاشل", "تسعطاش"],
        }
        for value, spellings in expected.items():
            for text in spellings:
                with self.subTest(text=text):
                    self.assertEqual(extract_number(text, lang="ar"), value)

    def test_in_a_number_and_a_sentence(self):
        for text, value in (("باربعتعش", 14), ("الف وخمستعش", 1015),
                            ("خمستعش الف", 15000), ("عمره هدعش سنة", 11),
                            ("خمستاش", 15), ("مية وتلتعش", 113)):
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, lang="ar"), value)
        self.assertEqual(numbers_to_digits("الساعة خمستعش", lang="ar"),
                         "الساعة 15")
        self.assertEqual(numbers_to_digits("عنده ستعش سنة", lang="ar"),
                         "عنده 16 سنة")

    def test_the_table_spellings_still_read(self):
        # Qafisheh 1970, glossary: 'arbaʕṭaʕʃ, xamsṭaʕʃ
        self.assertEqual(extract_number("اربعطعش", lang="ar"), 14)
        self.assertEqual(extract_number("خمسطعش", lang="ar"), 15)

    def test_the_long_vowel_spelling_of_the_sada_transcripts(self):
        # اربعطاعش is written 9 times in the SADA transcripts
        for text in ("اربعطاعش", "باربعطاعش"):
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, lang="ar"), 14)

    def test_a_spelling_no_source_gives_stays_unread(self):
        for text in ("اربعطوعش", "اتنااشر"):
            with self.subTest(text=text):
                self.assertFalse(extract_number(text, lang="ar"))


if __name__ == "__main__":
    unittest.main()
