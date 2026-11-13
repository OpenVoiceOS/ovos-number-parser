"""Every teen spelling the SADA transcripts write reads as its number.

SADA is Saudi Broadcasting Authority television, transcribed by hand ("SADA - SBA &
SDAIA Audio Dataset for Arabic", 2023). The spellings below are the one-word teens its
transcripts write that no grammar or dictionary table held.
"""
import unittest

from ovos_number_parser import extract_number, numbers_to_digits


class TestSadaTeens(unittest.TestCase):
    def test_every_sada_spelling(self):
        expected = {
            11: ["احداعش", "إحدعشر", "احدعشر", "حدعشر", "حداعش", "احداعشر", "احدش", "إحداعش", "هداعش", "احداش", "أحداش", "إحداش", "إحداعشر", "إحدش", "احداشر", "اهداش"],
            12: ["اثنعشر", "اثناعش", "اثناعشر", "إثنعشر", "إثناعشر", "اثناشر", "اثناش", "إثناعش", "ثناعش", "أثناش", "ثناش", "ثناشر", "ثنعشر"],
            13: ["ثلتعش", "ثلاطاعش", "ثلاثطعش", "ثلاطعشر", "ثلاتعش", "ثلاثعش", "ثلاتاعش", "ثلاثطعشر", "ثلتاشر", "ثلطاعش", "ثلطاعشر", "ثلطعش", "ثلاطاش", "ثلاطاعشر", "ثلتعشر", "ثلطاش", "ثلطعشر", "تلاتاعشر", "تلاتعش", "تلتاعشر", "ثلاتاشر", "ثلاتاعشر", "ثلاتعشر", "ثلاثتاعش", "ثلاثتعش", "ثلاثطاش", "ثلاثطاعش", "ثلاطش", "ثلتاعش", "ثلثطعش"],
            14: ["اربعطعشر", "أربعطعشر", "اربعطاعش", "أربعطاعش", "اربعطاشر", "أربعطاشر", "أربعطاعشر", "اربعتعشر", "اربعتاعش", "اربعتش", "اربعطش", "أربعتش", "أربعتشر", "اربعتشر"],
            15: ["خمستعشر", "خمسطعشر", "خمسطاعشر", "خمسطاعش", "خمستاعش", "خمستاعشر", "خمسطاشر", "خمسطش"],
            16: ["ستعشر", "ستاعش", "ستطعش", "ستطعشر", "سطاعش", "ستطاعش", "ستطاعشر", "سطعشر", "ستاعشر", "ستش", "ستطاشر", "سطاشر"],
            17: ["سبعطاعش", "سبعطعشر", "سبعتعشر", "سبعتش", "سبعطاعشر", "سبعطاشر", "سبعطشر", "سبعتاعش", "سبعتاعشر", "سبعتشر", "سبعطش"],
            18: ["ثمنتعشر", "ثمنطعشر", "ثمنطاعش", "ثمنتعش", "ثمنتاعش", "ثمانطاعش", "ثمانطعش", "ثمنطاش", "ثمنطاشر", "ثمانطعشر", "تمنطعشر", "ثمنتاعشر"],
            19: ["تسعطاعش", "تسعتاعش", "تسعطعشر", "تسعتعشر", "تسعطاعشر", "تسعطاشر"],
        }
        for value, spellings in expected.items():
            for text in spellings:
                with self.subTest(text=text):
                    self.assertEqual(extract_number(text, lang="ar"), value)

    def test_the_egyptian_nobody_stays_a_word(self):
        self.assertEqual(numbers_to_digits("ما حدش جا", lang="ar"), "ما حدش جا")

    def test_may_god_guide_you_stays_a_word(self):
        self.assertEqual(numbers_to_digits("الله هداش شفيك", lang="ar"), "الله هداش شفيك")

    def test_in_a_sentence(self):
        self.assertEqual(numbers_to_digits("عمره خمستعشر سنة", lang="ar"),
                         "عمره 15 سنة")
        self.assertEqual(numbers_to_digits("الساعة اربعطاعش", lang="ar"),
                         "الساعة 14")


if __name__ == "__main__":
    unittest.main()
