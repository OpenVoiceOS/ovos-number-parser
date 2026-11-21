"""Portuguese ``extract_number`` gives the number written first.

A sentence that holds two numbers answers the first one, the value that
``extract_number_spans`` gives for its first span: "ganhou mil euros e
comprou duas dúzias" is 1000. One number stays one number, whatever words it
spans. A half counts the unit before it (numbers_pt docstring): after a word
outside the number, such as "hora", it is half of that word, so "uma hora e
meia" is 1. Expected values are hand arithmetic.
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


class TestSignOfTheFirstNumber(unittest.TestCase):
    """The span holds no "menos", so the sign comes from the reader."""
    #: text, value, language tag
    ROWS = [("menos dois graus e três", -2, "pt-PT"),
            ("menos dois graus e três", -2, "pt-BR"),
            ("menos 5 graus e 10", -5, "pt-PT"),
            ("menos 5 graus e 10", -5, "pt-BR"),
            ("menos um milhão de euros e duas dúzias", -10 ** 6, "pt-PT"),
            ("a temperatura é de menos dez graus e amanhã será de cinco",
             -10, "pt-BR")]

    def test_the_minus_sign_stays(self):
        for text, value, lang in self.ROWS:
            with self.subTest(text=text, lang=lang):
                self.assertEqual(extract_number(text, lang=lang), value)
                self.assertEqual(len(extract_number_spans(text, lang)), 2)


class TestMarksAroundTheFirstNumber(unittest.TestCase):
    """The span leaves out a quote or a bracket glued to the number."""
    #: text, value
    ROWS = [("comprei (2) gatos e 3 cães", 2),
            ('"dois" gatos e três cães', 2),
            ("a palavra «cem» tem três letras", 100),
            ("ganhou (mil) euros e comprou duas dúzias", 1000),
            ("o código é 'vinte e dois' e a porta três", 20 + 2),
            ("'meia' hora e duas horas", 0.5),
            ("menos (2) graus e 3", -2),
            ("menos «dois» graus e três", -2)]

    def test_the_first_number_inside_marks(self):
        for text, value in self.ROWS:
            for lang in ("pt-PT", "pt-BR"):
                with self.subTest(text=text, lang=lang):
                    self.assertEqual(extract_number(text, lang=lang), value)


class TestDecimalMarkBeforeTheFirstNumber(unittest.TestCase):
    """The span leaves out a decimal mark before the digits, but the mark is
    part of the number: ",5" is 0.5. An ellipsis is no decimal mark."""
    #: text, value
    ROWS = [(",5 litros e 3 copos", 5 / 10),
            ("custa .99 euros e o outro 3", 99 / 100),
            ("menos .5 graus e 3", -5 / 10),
            ("(.5) e 3", 5 / 10),
            ("tomei ,5 mg e depois 3", 5 / 10),
            ("...5 gatos e 3", 5),
            (".dois gatos e três", 2)]

    def test_the_decimal_mark_stays(self):
        for text, value in self.ROWS:
            for lang in ("pt-PT", "pt-BR"):
                with self.subTest(text=text, lang=lang):
                    self.assertEqual(extract_number(text, lang=lang), value)


class TestOneNumberStaysWhole(unittest.TestCase):
    #: text, value, language tag
    ROWS = [("mil e duas dúzias", 1002 * 12, "pt-PT"),
            ("um milhão e duas dúzias", 10 ** 6 + 2 * 12, "pt-PT"),
            ("duas dúzias e meia", 2 * 12 + 12 // 2, "pt-BR"),
            ("vinte e um", 20 + 1, "pt-BR"),
            ("dois mil e vinte e cinco", 2 * 1000 + 20 + 5, "pt-PT"),
            ("um milhão e meio", 10 ** 6 + 10 ** 6 // 2, "pt-PT")]

    def test_a_half_after_a_noun_is_no_part_of_the_number(self):
        # "meia" agrees with the noun it halves: "uma hora e meia" is one
        # hour and half an hour, a duration, and the first number is 1
        for text, value in [("uma hora e meia", 1), ("daqui a duas horas e meia", 2),
                            ("duas horas e meia e três dias", 2),
                            ("uma hora e, meia", 1), ("uma hora, e meia", 1),
                            ("uma hora... e meia", 1), ("uma hora… e meia", 1),
                            ("uma hora; e meia", 1), ("uma hora (aprox.) e meia", 1),
                            ("Uma Hora E Meia", 1), ("uma hora? E meia", 1),
                            ("uma hora. E meia hora depois três", 1)]:
            for lang in ("pt-PT", "pt-BR"):
                with self.subTest(text=text, lang=lang):
                    self.assertEqual(extract_number(text, lang=lang), value)

    def test_a_half_after_marks_alone_counts_the_number(self):
        # only "e", marks or an aside in brackets stand between the number
        # and the half, so the unit is the number
        for text, value in [("dois e, meio", 2 + 0.5),
                            ("dois (aprox.) e meio", 2 + 0.5),
                            ("um. e meio", 1 + 0.5),
                            ("dois mil e quinhentos... e meio", 2500 + 0.5),
                            ("um milhão... e meio", 10 ** 6 + 10 ** 6 // 2),
                            # a mark that ends a number ends it before the half
                            ("dois, e meio", 2), ("dois; e meio", 2),
                            ("dois. E meio", 2),
                            # the ellipsis character ends a sentence as "..." does
                            ("um milhão… E meio", 10 ** 6),
                            ("um milhão... E meio", 10 ** 6),
                            ("um milhão… e meio", 10 ** 6 + 10 ** 6 // 2)]:
            for lang in ("pt-PT", "pt-BR"):
                with self.subTest(text=text, lang=lang):
                    self.assertEqual(extract_number(text, lang=lang), value)

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


class TestSpanValuesStayWritable(unittest.TestCase):
    """A span value is an integer that str() can write. 4000 digits fit the
    default limit of 4300; with "centiliões" (10 ** 600 in pt-PT) they do
    not, so the span ends before the scale word."""

    def test_the_span_stops_before_an_unwritable_value(self):
        digits = "9" * 4000
        for text in (digits + " centiliões", digits + " centiliões e dois"):
            with self.subTest(text=text[-20:]):
                spans = extract_number_spans(text, "pt-PT")
                self.assertTrue(spans)
                self.assertEqual(spans[0].surface, digits)
                self.assertEqual(spans[0].value, 10 ** 4000 - 1)
                for span in spans:
                    str(span.value)
                self.assertIs(extract_number(digits + " centiliões",
                                             lang="pt-PT"), False)


if __name__ == "__main__":
    unittest.main()
