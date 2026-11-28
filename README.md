# OVOS Number Parser

<!-- agent-hint
covers: what ovos-number-parser does, how to install it, a first example and where the docs are
source: ovos_number_parser/__init__.py (public functions), ovos_number_parser/numtag_readers.py:NUMTAG_LANGS, pyproject.toml
generated: no
verify: diff <(grep -E '^(from |import |print\()' README.md | .venv/bin/python -I -) <(grep -E '^print\(' README.md | sed 's/^print(.*)  *# //')
see: docs/index.md, docs/api.md, docs/languages.md, docs/adding-a-language.md, AGENTS.md
-->

`ovos-number-parser` turns spoken numbers into digits and digits into spoken
words, in 40 languages. It needs no voice assistant.

```text
   "two thousand twenty three"  →  2023  →  "two thousand, twenty three"
```

Words to digits (`extract_number`, `numbers_to_digits`) serves speech
recognition output and number extraction. Digits to words (`pronounce_number`,
`pronounce_ordinal`, `pronounce_fraction`) prepares text for speech synthesis.

[numtag](https://github.com/TigreGotico/numtag) reads the words in all 40
languages. The `pronounce_*` and `nice_number_*` writers live in this package.

## Install

```bash
uv pip install ovos-number-parser
```

## Quick start

Each call takes a text or a number and a language code. The comment after
`print` shows the real output.

```python
from ovos_number_parser import pronounce_number, pronounce_ordinal, extract_number, numbers_to_digits, is_fractional, is_ordinal

# digits -> words
print(pronounce_number(3.5, "en"))  # three point five
print(pronounce_number(2023, "en"))  # two thousand, twenty three
print(pronounce_ordinal(21, "en"))  # twenty-first

# words -> digits
print(extract_number("three point five liters", "en"))  # 3.5
print(extract_number("dos mil veintitrés", "es"))  # 2023
print(numbers_to_digits("set a timer for five minutes", "en"))  # set a timer for 5 minutes

# classification helpers
print(is_fractional("half", "en"))  # 0.5
print(is_ordinal("third", "en"))  # 3

# no number in the text -> False
print(extract_number("hello world", "en"))  # False
```

Pass another language code and the same calls work. A code with a region
(`pt-BR`, `pt-PT`) reads the language of the tag, and the region where the language has regional forms.

## Uses

Four common uses each have a runnable script in [`examples/`](examples/).

### ASR post-processing

Speech to text writes numbers as words. Most downstream systems want digits
([`examples/asr_itn.py`](examples/asr_itn.py)).

```python
from ovos_number_parser import numbers_to_digits, extract_number

print(numbers_to_digits("i need twenty three of them", "en"))  # i need 23 of them
print(extract_number("three point five liters", "en"))  # 3.5
```

### TTS normalization

Write numbers as words before synthesis, so the voice says "one thousand"
and not "one two three four dot five six"
([`examples/tts_normalization.py`](examples/tts_normalization.py)).

```python
from ovos_number_parser import pronounce_number

print(pronounce_number(1234.56, "en", places=2))  # one thousand, two hundred and thirty four point five six
print(pronounce_number(-3.5, "en"))  # minus three point five
```

### Numeric entity extraction

Pull cardinal, ordinal and fractional mentions out of free text without an ML
model ([`examples/ner.py`](examples/ner.py)).

```python
from ovos_number_parser import extract_number, is_fractional, is_ordinal

print(extract_number("shipped in three boxes", "en"))  # 3
print(is_ordinal("second", "en"))  # 2
print(is_fractional("a quarter", "en"))  # 0.25
```

With `ordinals=True`, a line that holds several numbers with other words
between them answers with the number written first. That number can be an
ordinal or a cardinal: `extract_number("zwei von dem dritten", "de",
ordinals=True)` is 2. Two adjacent number words are how a fraction is
written, so they keep the reading of the language.

### Multilingual round trips

The same functions cover 40 languages
([`examples/multilingual.py`](examples/multilingual.py)).

### In an OVOS skill and standalone

The API is the same in both cases. Only the source of the language code
differs. A standalone program passes the code itself. A skill passes the
session language.

```python
# Standalone Python
from ovos_number_parser import extract_number
n = extract_number(text, "en")

# Inside an OVOS skill
class MySkill(OVOSSkill):
    def handle_intent(self, message):
        n = extract_number(message.data["utterance"], self.lang)
```

## Supported languages

The 40 language codes are:

```text
an ar ast az bg ca cs da de el en es et eu fa fi fr fy gl he hr hu id it kab ms mwl nb nl nn oc pl pt ro ru sk sl sv tr uk
```

Every language supports every public function (see [Full function parity](docs/languages.md#full-function-parity)). numtag reads all of them. The [language table](docs/languages.md#language-table) lists the codes and the rules of single languages.

## Grammatical gender

A language whose numerals inflect accepts a `gender` argument.

```python
from ovos_number_parser import pronounce_number
from ovos_number_parser.util import GrammaticalGender

print(pronounce_number(2, "pt", gender=GrammaticalGender.FEMININE))  # duas
```

## Documentation

The [documentation index](docs/index.md) lists every page.

- [API reference](docs/api.md): every public function, the engine that answers it and its parameters
- [Language notes](docs/languages.md): the rules of single languages and the known limits
- [Adding a language](docs/adding-a-language.md): the steps for reading and speaking
- [examples/](examples/): runnable scripts
- [AGENTS.md](AGENTS.md): the guide for agents that change this repository

## Related projects

- [ovos-date-parser](https://github.com/OpenVoiceOS/ovos-date-parser): dates and times
- [ovos-lang-parser](https://github.com/OVOSHatchery/ovos-lang-parser): languages
- [ovos-color-parser](https://github.com/OVOSHatchery/ovos-color-parser): colors

## License

Apache License 2.0.
