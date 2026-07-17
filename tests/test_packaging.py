import ast
import unittest
from importlib.metadata import version as installed_version
from pathlib import Path

from ovos_number_parser.version import (VERSION_ALPHA, VERSION_BUILD,
                                        VERSION_MAJOR, VERSION_MINOR,
                                        __version__)

VERSION_FILE = Path(__file__).parent.parent / "ovos_number_parser" / "version.py"


class TestVersionBlock(unittest.TestCase):
    """The release automation rewrites version.py by pattern, and the build
    backend reads __version__ from it. Both contracts are asserted here."""

    def test_version_block_markers_present(self):
        text = VERSION_FILE.read_text()
        self.assertIn("# START_VERSION_BLOCK", text)
        self.assertIn("# END_VERSION_BLOCK", text)

    def test_version_block_holds_four_plain_integers(self):
        # the bumper rewrites these by regex; they must stay bare int literals
        block = VERSION_FILE.read_text().split("# END_VERSION_BLOCK")[0]
        assigned = {
            node.targets[0].id: node.value
            for node in ast.parse(block).body
            if isinstance(node, ast.Assign)
        }
        self.assertEqual(
            sorted(assigned),
            ["VERSION_ALPHA", "VERSION_BUILD", "VERSION_MAJOR", "VERSION_MINOR"],
        )
        for name, value in assigned.items():
            self.assertIsInstance(value, ast.Constant, f"{name} must be a literal")
            self.assertIsInstance(value.value, int, f"{name} must be an int")

    def test_version_string_matches_version_block(self):
        expected = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_BUILD}"
        if VERSION_ALPHA:
            expected += f"a{VERSION_ALPHA}"
        self.assertEqual(__version__, expected)

    def test_alpha_suffix_only_when_alpha_is_set(self):
        self.assertEqual("a" in __version__, bool(VERSION_ALPHA))

    def test_installed_metadata_matches_source(self):
        # catches a pyproject that stops tracking version.py
        self.assertEqual(installed_version("ovos-number-parser"), __version__)


if __name__ == "__main__":
    unittest.main()
