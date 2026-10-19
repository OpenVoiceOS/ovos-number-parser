"""The per-token readers in the generic numbers_to_digits are asked once.

``_numbers_to_digits_generic`` walks a run of number words twice for a
language that supplies ``first_number_words``: once in the pre-scan that
asks the language's own parser where the first number ends, and once in the
main loop that grows the span. Arabic is the only language that supplies it.

Both walks ask the same question about the same token, and the expensive
half of that question is ``extract_number``. Counting the calls is the
measurement, because a wall-clock threshold in CI measures the runner.

Baseline on dev before the cache, for the 16-token Arabic run of distinct
number words this file builds: 56 calls. With the per-token answers cached:
28. Both numbers are from the sorted input below, so they reproduce at any
PYTHONHASHSEED. An earlier pair, 148 and 35, was measured on hash-ordered
input and was one sample of a moving measurement.
"""
import itertools
import unittest

import ovos_number_parser
from ovos_number_parser.numbers_ar import _NUMBER_WORDS

TOKENS = 16


def _arabic_run(n=TOKENS):
    """A run of DISTINCT Arabic number words.

    Distinct on purpose: a run of one repeated word would let a cache look
    good by collapsing repetitions rather than by removing the second walk.
    """
    # sorted(), not list(): _NUMBER_WORDS is a set, so list() iterates it in
    # hash order and the run of words changes with PYTHONHASHSEED. The call
    # count changed with it, and the bound below was exceeded at seed 78 (50
    # calls against 48) while passing at seed 0. A benchmark whose INPUT moves
    # measures the seed.
    words = sorted(w for w in _NUMBER_WORDS if w)
    return " ".join(itertools.islice(itertools.cycle(words), n))


def _spanish_run(n=TOKENS):
    words = ["cinco", "seis", "siete", "ocho"]
    return " ".join(itertools.islice(itertools.cycle(words), n))


class _CountingExtractNumber:
    """Count calls to the module-level ``extract_number``."""

    def __init__(self):
        self.calls = 0
        self._real = ovos_number_parser.extract_number

    def __enter__(self):
        def counted(*args, **kwargs):
            self.calls += 1
            return self._real(*args, **kwargs)

        ovos_number_parser.extract_number = counted
        return self

    def __exit__(self, *exc):
        ovos_number_parser.extract_number = self._real
        return False


class TestTheRunIsReadOnce(unittest.TestCase):

    def test_arabic_reads_each_token_a_bounded_number_of_times(self):
        """Fewer than three reads per token over a 16-token run.

        The pre-scan and the main loop each used to read every token, so
        the old code spent 148 calls here, more than nine per token. The
        bound is deliberately loose: it pins the double walk being gone,
        not an exact number that any unrelated change would have to chase.
        """
        text = _arabic_run()
        with _CountingExtractNumber() as counter:
            ovos_number_parser.numbers_to_digits(text, "ar")
        self.assertLess(
            counter.calls, 3 * TOKENS,
            f"{counter.calls} extract_number calls for {TOKENS} tokens; the "
            f"pre-scan is reading the run a second time")

    def test_the_spanish_control_does_not_get_worse(self):
        """Spanish takes the same generic path with no pre-scan.

        It is the control for the cache itself: a cache that helped Arabic
        by breaking the shared reader would show up here.

        The bound is this branch's own measurement, 50, with a small margin.
        It was 62, which is what DEV spends exactly, so the control could not
        fail on dev and pinned nothing. The Spanish word list here is a
        literal, so this number does not move with PYTHONHASHSEED.
        """
        text = _spanish_run()
        with _CountingExtractNumber() as counter:
            ovos_number_parser.numbers_to_digits(text, "es")
        self.assertLessEqual(
            counter.calls, 52,
            f"{counter.calls} extract_number calls for {TOKENS} Spanish "
            f"tokens; this branch spends 50")


class TestTheAnswersAreUnchanged(unittest.TestCase):
    """The real control. A faster wrong answer is not a fix.

    Every expected value here was read off dev before the change, so this
    is a regression control and not a claim about what the answers ought
    to be. "cinco y tres" reads 8 on dev: the Spanish connector joins the
    two numbers. That is recorded, not endorsed.
    """

    CASES = (
        ("ar", "خمسة وعشرون", "25"),
        ("ar", "مية", "100"),
        ("es", "veinticinco", "25"),
        ("es", "cinco y tres", "8"),
        ("it", "venti", "20"),
    )

    def test_known_phrases_still_render(self):
        for lang, text, expected in self.CASES:
            with self.subTest(lang=lang, text=text):
                self.assertEqual(
                    ovos_number_parser.numbers_to_digits(text, lang),
                    expected)

    def test_a_long_run_renders_the_same_as_token_by_token_reading(self):
        """The cache is keyed on the token, so a token that appears twice
        in one utterance must still read the same both times."""
        text = "خمسة خمسة"
        out = ovos_number_parser.numbers_to_digits(text, "ar")
        self.assertEqual(out.split(), ["5", "5"])


if __name__ == "__main__":
    unittest.main()
