# Adding a language

<!-- agent-hint
covers: the steps to add reading (words to digits) and speaking (digits to words) for a language
source: ovos_number_parser/numtag_readers.py:NUMTAG_LANGS, ovos_number_parser/__init__.py (dispatchers), ovos_number_parser/util.py:NumberVocabulary, tests/test_numtag_routed_languages.py, tests/test_lang_parity.py
generated: no
verify: diff <(sed -n '/^\x60\x60\x60python/,/^\x60\x60\x60$/p' docs/adding-a-language.md | sed -e 1d -e '$d' | python -) <(sed -n '/^\x60\x60\x60text/,/^\x60\x60\x60$/p' docs/adding-a-language.md | sed -e 1d -e '$d')
see: languages.md, api.md, https://github.com/TigreGotico/numtag/blob/dev/docs/adding-a-language.md
-->

This page tells you how to add a language to this library. Reading and
speaking are two separate jobs with two separate homes. Reading is done by
numtag. Speaking is done by a `pronounce_*` writer in this repository.

## Add reading

Reading means `extract_number`, `extract_number_spans`, `numbers_to_digits`,
`is_fractional` and `is_ordinal`.
A language reads through numtag when its code is in `NUMTAG_LANGS` in
`ovos_number_parser/numtag_readers.py`. Follow these steps.

1. Add a numtag lexicon for the language. Use the guide
   [Adding a language](https://github.com/TigreGotico/numtag/blob/dev/docs/adding-a-language.md)
   in the numtag repository. Release numtag, and raise the floor of `numtag` in
   `pyproject.toml` to the release that has the lexicon.
2. Add the language code to `NUMTAG_LANGS`.
3. Add the code to the set in `test_the_routed_languages` in
   `tests/test_numtag_routed_languages.py`. Add a case to `CASES` in that file
   with a sentence and its value from hand arithmetic on the words.
4. Run the check below. It must show the value of your case.

```python
from ovos_number_parser import extract_number
print(extract_number("hogeita bat", "eu"))
```

The output is:

```text
21
```

A test that numtag fails is a strict xfail. Add
its row to `tests/numtag_xfail.json` with the URL of the issue that tracks it.

The same lexicon answers `is_fractional` and `is_ordinal`. Neither function
needs code in this repository.

## Add speaking

Speaking means `pronounce_number`, `pronounce_ordinal`, `pronounce_fraction`
and the `nice_number_<code>` helper. A language with no writer of its own uses
[unicode-rbnf](https://github.com/rhasspy/unicode-rbnf). To write the forms by
hand, follow these steps.

1. Create `ovos_number_parser/numbers_<code>.py` with
   `pronounce_number_<code>(number, places=2, short_scale=True, scientific=False, ordinals=False)`.
   Add `pronounce_ordinal_<code>(number)` for ordinals.
2. Import the functions in `ovos_number_parser/__init__.py`.
3. Add `if lang2 == "<code>":` branches to `_pronounce_number_dispatch` and to
   `pronounce_ordinal`.
4. Add the code to `LANGS` in `tests/test_lang_parity.py`.
5. Add `tests/test_number_parser_<code>.py` with spoken forms for a fixed set
   of values (0 to 20, the tens, 100, 101, 123, 999, 1000, 2023). Take each
   expected form from a grammar or from native usage, never from the output
   of the code under test.

For a Romance language with unit, ten, hundred and scale words and joiner
words, describe the language with `NumberVocabulary` and
`RomanceNumberExtractor` from `ovos_number_parser/util.py`. `numbers_gl.py` and
`numbers_ast.py` are worked examples. `numbers_ro.py` shows the knobs for
articled scale groups, a linker word between count and scale, multiplicative
hundreds and particle ordinals. Other families use a module of the same family
as a template: `numbers_de.py` for compound words, `numbers_cs.py` or
`numbers_ru.py` for declension, `numbers_en.py` for plain summing.

## Check the result

Run the parity test. It calls every public function for every language in its
`LANGS` list.

```bash
python -m pytest tests/test_lang_parity.py tests/test_numtag_routed_languages.py
```

Add a row to the [language table](languages.md#language-table).

---
[Index](index.md) · [← Language notes](languages.md) · [Home →](../README.md)
