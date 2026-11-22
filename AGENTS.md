# ovos-number-parser: agent guide

Read this file before you change anything in the repository. The
documentation index is [docs/index.md](docs/index.md).

`ovos-number-parser` reads spoken numbers as digits and speaks digits as
words, in 40 languages. All 40 languages read through numtag. The
`pronounce_*` writers live here.

## Repository map

| Path | Holds |
|---|---|
| `ovos_number_parser/__init__.py` | The public functions and their per-language dispatch |
| `ovos_number_parser/numtag_readers.py` | `NUMTAG_LANGS` and the numtag readers |
| `ovos_number_parser/numbers_<code>.py` | The writers of one language, and the deprecated reader shims |
| `ovos_number_parser/util.py` | `NumberVocabulary`, `RomanceNumberExtractor` and the enums |
| `tests/` | The test suite. `tests/numtag_xfail.json` lists strict xfails with issue URLs |
| `benchmarks/` | The ICU differential harness ([benchmarks/README.md](benchmarks/README.md)) |
| `examples/` | Runnable scripts |
| `docs/` | The documentation. [docs/index.md](docs/index.md) sets the reading order |

## Setup

```bash
unset VIRTUAL_ENV
uv venv .venv
uv pip install -p .venv/bin/python --prerelease=allow -e . pytest
```

Build the venv inside the checkout.

## Run the tests

```bash
.venv/bin/python -m pytest tests
```

Language data is Python code in `numbers_<code>.py`. The numtag lexicons are in
the [numtag](https://github.com/TigreGotico/numtag) repository.

## Hard rules

1. A language reads through numtag when its code is in `NUMTAG_LANGS`. Add
   reading as a numtag lexicon, not as a reader here
   ([adding-a-language.md](docs/adding-a-language.md)).
2. A test where numtag reads differently from the expected value, and numtag
   is wrong, is a strict xfail in `tests/numtag_xfail.json`, with the URL of
   its issue
   ([api.md](docs/api.md#readers-backed-by-numtag)).
3. Every language provides every public function. `tests/test_lang_parity.py`
   enforces this ([languages.md](docs/languages.md#full-function-parity)).
4. Take each expected form in a test from reference material or native usage,
   never from the output of the code under test
   ([adding-a-language.md](docs/adding-a-language.md#add-speaking)).
5. `is_fractional` and `is_ordinal` read through numtag like `extract_number`
   ([api.md](docs/api.md#readers-backed-by-numtag)).
6. Never edit `ovos_number_parser/version.py`. The release workflow bumps it
   ([release_workflow.yml](.github/workflows/release_workflow.yml)).
7. Write the pull request title as a Conventional Commits message.
   [conventional-label.yaml](.github/workflows/conventional-label.yaml) labels
   the pull request from it.

## Before you push

Run the full test suite. If you changed a page under `docs/`, check that
`docs/index.md` lists it and that every relative link resolves.
