import unittest

from ovos_number_parser import extract_number

from ovos_number_parser.numbers_it import pronounce_number_it


class TestItalianHundredsMultiplier(unittest.TestCase):
    def test_bare_cento_after_thousand_adds(self):
        # "mille cento" is 1000 + 100, not 1000 * 100
        self.assertEqual(extract_number("mille cento", lang="it"), 1100)
        self.assertEqual(extract_number("mille cento uno", lang="it"), 1101)
        self.assertEqual(extract_number("duemila cento", lang="it"), 2100)
        self.assertEqual(extract_number("tremila cento cinquanta", lang="it"), 3150)

    def test_solid_and_spaced_agree(self):
        self.assertEqual(extract_number("millecento", lang="it"),
                         extract_number("mille cento", lang="it"))
        self.assertEqual(extract_number("milleduecento", lang="it"), 1200)

    def test_cento_as_multiplier_still_works(self):
        # a hundreds multiplier still scales a smaller preceding value
        self.assertEqual(extract_number("due cento", lang="it"), 200)
        self.assertEqual(extract_number("cinque cento", lang="it"), 500)
        self.assertEqual(extract_number("cento", lang="it"), 100)
        self.assertEqual(extract_number("cento mila", lang="it"), 100000)
        self.assertEqual(extract_number("duecentomila", lang="it"), 200000)

    def test_natural_sentences(self):
        self.assertEqual(
            extract_number("ho bisogno di mille cento pezzi", lang="it"), 1100)
        self.assertEqual(
            extract_number("il costo è di duemila cento euro", lang="it"), 2100)

    def test_roundtrip_up_to_100000(self):
        # every value the engine can pronounce must extract back to itself
        bad = []
        for n in list(range(0, 3000)) + list(range(3000, 100001, 331)):
            if extract_number(pronounce_number_it(n), lang="it") != n:
                bad.append(n)
        self.assertEqual(bad, [], f"round-trip failures: {bad[:10]}")


if __name__ == "__main__":
    unittest.main()
