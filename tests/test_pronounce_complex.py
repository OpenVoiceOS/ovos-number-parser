import unittest

from ovos_number_parser import pronounce_number, extract_number


class TestPronounceComplex(unittest.TestCase):
    def test_rectangular_form(self):
        self.assertEqual(pronounce_number(3 + 4j, "en"), "three plus four i")
        self.assertEqual(pronounce_number(3 - 4j, "en"), "three minus four i")

    def test_pure_imaginary(self):
        self.assertEqual(pronounce_number(0 + 1j, "en"), "i")
        self.assertEqual(pronounce_number(2j, "en"), "two i")
        self.assertEqual(pronounce_number(-0 - 1j, "en"), "minus i")
        self.assertEqual(pronounce_number(0 - 2j, "en"), "minus two i")

    def test_pure_real(self):
        self.assertEqual(pronounce_number(5 + 0j, "en"), "five")
        self.assertEqual(pronounce_number(complex(3, 0), "en"), "three")

    def test_pure_real_roundtrips(self):
        spoken = pronounce_number(5 + 0j, "en")
        self.assertEqual(extract_number(spoken, "en"), 5)

    def test_never_raises_typeerror(self):
        for value in [3 + 4j, 2j, 1j, complex(3, 4), complex(0, -1)]:
            try:
                pronounce_number(value, "en")
            except TypeError:
                self.fail(f"opaque TypeError for {value!r}")

    def test_language_specific_connectives(self):
        self.assertEqual(pronounce_number(3 + 4j, "ru"), "три плюс четыре и")


if __name__ == "__main__":
    unittest.main()
