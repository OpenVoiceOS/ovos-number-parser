"""German extract_number answers False, as documented, when a line holds no
number it reads, and reads a spoken ordinal under ordinals=True."""
import unittest

from ovos_number_parser import extract_number
from ovos_number_parser.numbers_de import extract_number_de


class TestNoNumberIsFalse(unittest.TestCase):
    #: lines with no cardinal: an ordinal is read only under ordinals=True
    LINES = [("nimm den siebten eintrag", 7),   # take the seventh entry
             ("die erste reihe", 1),             # the first row
             ("am einundzwanzigsten mai", 21)]   # on the twenty-first of May

    def test_no_number_is_false(self):
        for line, _ in self.LINES + [("hallo wie geht es dir", None)]:
            with self.subTest(line=line):
                self.assertIs(extract_number(line, lang="de"), False)
                self.assertIs(extract_number_de(line), False)

    def test_the_ordinal_reads_under_the_flag(self):
        for line, value in self.LINES:
            with self.subTest(line=line):
                self.assertEqual(extract_number(line, lang="de",
                                                ordinals=True), value)

    def test_a_cardinal_still_reads(self):
        self.assertEqual(extract_number("nimm sieben einträge", lang="de"), 7)


if __name__ == "__main__":
    unittest.main()
