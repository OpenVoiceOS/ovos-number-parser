"""Portuguese ``extract_number`` gives the number written first.

A sentence that holds two numbers answers the first one, the value that
``extract_number_spans`` gives for its first span: "ganhou mil euros e
comprou duas dúzias" is 1000. One number stays one number, whatever words it
spans. A half after "e" counts the unit before it (numbers_pt docstring), so
"uma hora e meia" is 1.5. Expected values are hand arithmetic.
"""
import unittest

from ovos_number_parser import extract_number, extract_number_spans


class TestFirstNumber(unittest.TestCase):
    #: text, value, language tag, ordinals
    ROWS = [("ganhou mil euros e comprou duas dúzias", 1000, "pt-PT", False),
            ("um milhão e meio e duas dúzias", 10 ** 6 + 10 ** 6 // 2,
             "pt-PT", False),
            ("um milhão e meio e mil pessoas", 10 ** 6 + 10 ** 6 // 2,
             "pt-PT", False),
            ("ganhou dois bilhões e comprou três carros", 2 * 10 ** 9,
             "pt-BR", False),
            ("duzentas pessoas e trinta carros", 200, "pt-PT", False),
            ("vinte e dois gatos e três cães", 20 + 2, "pt-BR", False),
            ("cem euros, duzentos euros", 100, "pt-PT", False),
            ("dois mil e vinte e cinco pessoas e trinta",
             2 * 1000 + 20 + 5, "pt-PT", False),
            ("três horas ou meia hora", 3, "pt-PT", False),
            ("o terceiro e o quinto", 3, "pt-PT", True),
            ("a primeira e a segunda", 1, "pt-BR", True)]

    def test_the_first_number_answers(self):
        for text, value, lang, ordinals in self.ROWS:
            with self.subTest(text=text, lang=lang):
                self.assertEqual(
                    extract_number(text, lang=lang, ordinals=ordinals), value)

    def test_the_value_of_the_first_span(self):
        for text, value, lang, ordinals in self.ROWS:
            with self.subTest(text=text, lang=lang):
                spans = extract_number_spans(text, lang, ordinals=ordinals)
                self.assertEqual(len(spans), 2)
                self.assertEqual(spans[0].value, value)

    def test_the_first_number_also_when_it_is_the_smaller(self):
        self.assertEqual(extract_number(
            "comprou duas dúzias de ovos e ganhou um milhão de euros",
            lang="pt-BR"), 2 * 12)


class TestOneNumberStaysWhole(unittest.TestCase):
    #: text, value, language tag
    ROWS = [("mil e duas dúzias", 1002 * 12, "pt-PT"),
            ("um milhão e duas dúzias", 10 ** 6 + 2 * 12, "pt-PT"),
            ("duas dúzias e meia", 2 * 12 + 12 // 2, "pt-BR"),
            ("vinte e um", 20 + 1, "pt-BR"),
            ("dois mil e vinte e cinco", 2 * 1000 + 20 + 5, "pt-PT"),
            ("um milhão e meio", 10 ** 6 + 10 ** 6 // 2, "pt-PT"),
            # a half after "e" counts the unit before it
            ("uma hora e meia", 1 + 0.5, "pt-PT"),
            ("daqui a duas horas e meia", 2 + 0.5, "pt-BR"),
            ("duas horas e meia e três dias", 2 + 0.5, "pt-PT")]

    def test_one_number(self):
        for text, value, lang in self.ROWS:
            with self.subTest(text=text, lang=lang):
                self.assertEqual(extract_number(text, lang=lang), value)

    def test_the_type_and_the_no_number_answer(self):
        self.assertIsInstance(extract_number("três gatos e quatro cães",
                                             lang="pt-PT"), int)
        self.assertEqual(extract_number("três gatos e quatro cães",
                                        lang="pt-PT"), 3)
        self.assertIs(extract_number("não há nada aqui", lang="pt-PT"), False)
        self.assertIs(extract_number("", lang="pt-BR"), False)


if __name__ == "__main__":
    unittest.main()
