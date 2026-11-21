# OVOS Number Parser

<!-- agent-hint
covers: what ovos-number-parser does, how to install it, a first example and where the docs are
source: ovos_number_parser/__init__.py (public functions), ovos_number_parser/numtag_readers.py:NUMTAG_LANGS, pyproject.toml
generated: no
verify: python -I examples/extract.py
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
Thirty-nine languages read numbers through
[numtag](https://github.com/TigreGotico/numtag). The `pronounce_*` writers are
in this package.

## Install

```bash
uv pip install ovos-number-parser
```

## 30-second quickstart

```python
from ovos_number_parser import (pronounce_number, pronounce_ordinal,
                                 extract_number, numbers_to_digits,
                                 is_fractional, is_ordinal)

# digits -> words
pronounce_number(3.5, "en")               # 'three point five'
pronounce_number(2023, "en")              # 'two thousand, twenty three'
pronounce_ordinal(21, "en")               # 'twenty-first'

# words -> digits
extract_number("three point five liters", "en")          # 3.5
extract_number("dos mil veintitrés", "es")               # 2023
numbers_to_digits("set a timer for five minutes", "en")  # 'set a timer for 5 minutes'

# classification helpers
is_fractional("half", "en")               # 0.5
is_ordinal("third", "en")                 # 3

# no number in the text -> False
extract_number("hello world", "en")       # False
```

Pass a different language code and the same calls work. See
[Supported languages](#supported-languages) for the 40 codes.

## What it's good for (beyond voice assistants)

The library is a standalone text/number utility. Four common uses, each with a
runnable script in [`examples/`](examples/):

### 1. ASR post-processing / inverse text normalization

Speech-to-text emits numbers as words. Most downstream systems want digits.

```python
from ovos_number_parser import numbers_to_digits, extract_number

numbers_to_digits("i need twenty three of them", "en")   # 'i need 23 of them'
extract_number("three point five liters", "en")          # 3.5
```

→ [`examples/asr_itn.py`](examples/asr_itn.py)

### 2. TTS normalization

Expand numbers into words *before* synthesis so the voice reads them naturally
("one thousand..." instead of "one-two-three-four dot five six").

```python
from ovos_number_parser import pronounce_number

pronounce_number(1234.56, "en", places=2)
# 'one thousand, two hundred and thirty four point five six'
pronounce_number(-3.5, "en")               # 'minus three point five'
```

→ [`examples/tts_normalization.py`](examples/tts_normalization.py)

### 3. Numeric entity extraction (NER)

Pull cardinal, ordinal and fractional mentions out of free text without an ML
model.

```python
from ovos_number_parser import extract_number, is_fractional, is_ordinal

extract_number("shipped in three boxes", "en")   # 3
is_ordinal("second", "en")                        # 2
is_fractional("quarter", "en")                    # 0.25
```

With `ordinals=True`, a line that holds several numbers with other words
between them answers with the number written first, whether that number is
the ordinal or the cardinal (`extract_number("zwei von dem dritten", "de",
ordinals=True)` is 2). Two adjacent number words are how a fraction is
written, so they keep the language's own reading.

→ [`examples/ner.py`](examples/ner.py)

### 4. Multilingual round-trips

The same functions cover 40 languages. A code with a region (`pt-BR`,
`pt-PT`) uses the language of its first subtag.

→ [`examples/multilingual.py`](examples/multilingual.py)

### In an OVOS skill vs. standalone

The API is the same in both cases. Only where you get the language code differs.

```python
# Standalone Python: you pass the language yourself
from ovos_number_parser import extract_number
n = extract_number(text, "en")

# Inside an OVOS skill: the framework already knows the session language
class MySkill(OVOSSkill):
    def handle_intent(self, message):
        n = extract_number(message.data["utterance"], self.lang)
```

## Supported languages

The 40 supported language codes are: an, ar, ast, az, bg, ca, cs, da, de, el,
en, es, et, eu, fa, fi, fr, fy, gl, he, hr, hu, id, it, kab, ms, mwl, nb, nl,
nn, oc, pl, pt, ro, ru, sk, sl, sv, tr and uk. Every language supports every
public function. Where a language has no hand-written implementation of a
function, a generic fallback answers (see
[Full function parity](docs/languages.md#full-function-parity)).

All of them except Malay (`ms`) read words through numtag. The
[language table](docs/languages.md#language-table) shows the reader of each
language and the rules of single languages.

## Grammatical gender

Languages whose numerals inflect accept a `gender` argument:

```python
from ovos_number_parser import pronounce_number
from ovos_number_parser.util import GrammaticalGender

pronounce_number(2, "pt", gender=GrammaticalGender.FEMININE)  # 'duas'
```

## Documentation

The [documentation index](docs/index.md) lists every page.

- [API reference](docs/api.md): every public function and its parameters
- [Language notes](docs/languages.md): the reader of each language, rules and known gaps
- [Adding a language](docs/adding-a-language.md): the steps for reading and speaking
- [examples/](examples/): runnable scripts
- [AGENTS.md](AGENTS.md): the guide for agents that change this repository

## Related projects

- [ovos-date-parser](https://github.com/OpenVoiceOS/ovos-date-parser): dates and times
- [ovos-lang-parser](https://github.com/OVOSHatchery/ovos-lang-parser): languages
- [ovos-color-parser](https://github.com/OVOSHatchery/ovos-color-parser): colors

## License

Apache License 2.0.
