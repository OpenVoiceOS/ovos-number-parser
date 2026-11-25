# ovos-number-parser: agent guide

<!-- agent-hint
covers: the purpose, repository map, setup, test commands and hard rules for a change to ovos-number-parser
source: ovos_number_parser/__init__.py, ovos_number_parser/numtag_readers.py:NUMTAG_LANGS, tests/test_deprecated_readers.py, tests/test_lang_parity.py, tests/numtag_xfail.json
generated: no
verify: grep -oP '^\| \x60\K[^\x60]*' AGENTS.md | grep -v '<' | xargs ls -d > /dev/null || exit 1
see: docs/index.md, docs/how-it-works.md, docs/api.md, docs/writers.md, docs/languages.md, docs/adding-a-language.md
-->

Read this file before you change anything in the repository. The
documentation index is [docs/index.md](docs/index.md).

`ovos-number-parser` reads spoken numbers as digits and speaks digits as
words, in 40 languages. All 40 languages read through numtag. The writers
live here ([docs/how-it-works.md](docs/how-it-works.md)).

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
| `docs/plots/` | The script that builds the plot in `docs/img/` |

## Setup

```bash
unset VIRTUAL_ENV
uv venv .venv
uv pip install -p .venv/bin/python --prerelease=allow -e . pytest matplotlib
```

Build the venv inside the checkout. matplotlib is for the plot script only.

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
   its issue ([api.md](docs/api.md#readers-backed-by-numtag)).

3. Every language provides every public function. `tests/test_lang_parity.py`
   enforces this ([languages.md](docs/languages.md#full-function-parity)).

4. Take each expected form in a test from reference material or native usage,
   never from the output of the code under test
   ([adding-a-language.md](docs/adding-a-language.md#add-speaking)).

5. A deprecated reader name in a `numbers_<code>` module keeps its parameters,
   warns with a removal version and answers what the public function answers.
   `tests/test_deprecated_readers.py` enforces this
   ([api.md](docs/api.md#deprecated-reader-names)).

6. Never edit `ovos_number_parser/version.py`. The release workflow bumps it
   ([release_workflow.yml](.github/workflows/release_workflow.yml)).

7. Write the pull request title as a Conventional Commits message.
   [conventional-label.yaml](.github/workflows/conventional-label.yaml) labels
   the pull request from it.

8. Rebuild the plot with `.venv/bin/python docs/plots/writer_sources.py` when
   a writer changes its source ([how-it-works.md](docs/how-it-works.md)).

## Before you push

Run the full test suite. If you changed a page under `docs/`, check that
`docs/index.md` lists it and that every relative link resolves. Run the
`verify` command in the agent hint of each page that you changed.
