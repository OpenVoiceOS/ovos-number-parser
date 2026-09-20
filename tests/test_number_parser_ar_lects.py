"""Cardinals in the words an Arabic lect uses, keyed by its ISO 639-3 code."""
import unittest

from ovos_number_parser import pronounce_number, resolve_ar_lect
from ovos_number_parser.numbers_ar import AR_LECT_FORMS, pronounce_number_ar


class TestArabicLectCardinals(unittest.TestCase):
    def test_a_lect_says_a_teen_its_own_way(self):
        self.assertEqual(pronounce_number(15, lang="ar"), "خمسة عشر")
        self.assertEqual(pronounce_number(15, lang="acw"), "خمسطعش")
        self.assertEqual(pronounce_number(15, lang="afb"), "خمسطعش")
        self.assertEqual(pronounce_number(15, lang="arz"), "خمستاشر")

    def test_the_lects_do_not_all_say_it_alike(self):
        """A table earns its place by differing from the others, not only from the
        literary form."""
        said = {code: pronounce_number(12, lang=code) for code in ("ar", "acw", "afb", "arz")}
        self.assertEqual(len(set(said.values())), 4, said)

    def test_a_word_inside_a_composed_number_is_replaced_and_the_rest_is_not(self):
        self.assertEqual(pronounce_number(2018, lang="ar"), "ألفان وثمانية عشر")
        self.assertEqual(pronounce_number(2018, lang="acw"), "ألفين وتمنطعش")
        self.assertEqual(pronounce_number(350, lang="afb"), "ثلاثمية وخمسين")

    def test_a_lect_with_no_table_keeps_the_literary_words(self):
        """Najdi has no table because no source has been read for it. It still takes
        the oblique register every spoken lect takes."""
        self.assertIsNone(resolve_ar_lect("ars"))
        self.assertEqual(pronounce_number(15, lang="ars"), "خمسة عشر")
        self.assertEqual(pronounce_number(350, lang="ars"), "ثلاثمئة وخمسين")

    def test_the_literary_codes_are_untouched(self):
        for code in ("ar", "arb"):
            self.assertIsNone(resolve_ar_lect(code))
            self.assertEqual(pronounce_number(15, lang=code), "خمسة عشر")
            self.assertEqual(pronounce_number(350, lang=code), "ثلاثمئة وخمسون")

    def test_only_a_lect_with_a_table_resolves(self):
        for code in ("acw", "afb", "arz", "ACW", "acw-x-anything"):
            self.assertIsNotNone(resolve_ar_lect(code))
        for code in ("ar", "arb", "ars", "ar-EG", "en", "arc"):
            self.assertIsNone(resolve_ar_lect(code), code)

    def test_a_negative_number_keeps_the_lects_words(self):
        self.assertEqual(pronounce_number(-15, lang="acw"), "سالب خمسطعش")

    def test_ordinals_are_untouched_by_a_lect(self):
        """The tables hold cardinals; an ordinal has no entry and must not be rewritten."""
        for code in ("ar", "acw", "afb", "arz"):
            self.assertEqual(pronounce_number(15, lang=code, ordinals=True), "الخامس عشر")

    def test_every_table_names_only_values_whose_word_really_differs(self):
        """A row whose form equals the literary word is dead weight and hides a typo."""
        for code, forms in AR_LECT_FORMS.items():
            for value, form in forms.items():
                for case in ("nominative", "oblique"):
                    literary = pronounce_number_ar(value, case=case)
                    self.assertNotEqual(form, literary, f"{code} {value} {case}")

    def test_every_form_is_arabic_script_and_no_table_is_empty(self):
        for code, forms in AR_LECT_FORMS.items():
            self.assertTrue(forms, code)
            self.assertRegex(code, r"^[a-z]{3}$")
            for value, form in forms.items():
                self.assertIsInstance(value, int)
                self.assertTrue(form.strip(), (code, value))
                self.assertTrue(all("؀" <= c <= "ۿ" or c == " " for c in form),
                                (code, value, form))

    def test_every_form_a_lect_can_say_can_also_be_read(self):
        """A library that says a word and then cannot recognise it is two libraries.

        This is the invariant that pays for the tables: whatever `pronounce` emits for a
        lect, `extract` reads back to the same value. Seventeen spellings failed this when
        the tables were first written, which is how the extract side learned them.
        """
        from ovos_number_parser import extract_number
        for code, forms in AR_LECT_FORMS.items():
            for value, form in forms.items():
                self.assertEqual(extract_number(form, lang="ar"), value, f"{code} {value} {form}")

    def test_a_whole_composed_number_reads_back_too(self):
        from ovos_number_parser import extract_number
        for code in ("acw", "afb", "arz"):
            for value in (12, 15, 18, 350, 2018):
                spoken = pronounce_number(value, lang=code)
                self.assertEqual(extract_number(spoken, lang="ar"), value,
                                 f"{code} {value} {spoken}")


if __name__ == "__main__":
    unittest.main()
