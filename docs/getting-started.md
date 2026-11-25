# Getting started

<!-- agent-hint
covers: the path from install to a first number read from text and a first number spoken as words, in five steps
source: ovos_number_parser/__init__.py (public functions), ovos_number_parser/numtag_readers.py (readers)
generated: no
verify: diff <(grep -E '^(from |import |print\()' docs/getting-started.md | .venv/bin/python -I -) <(grep -E '^print\(' docs/getting-started.md | sed 's/^print(.*)  *# //')
see: how-it-works.md, api.md, languages.md, ../README.md
-->

This page takes you from an empty directory to your first number read from text
and your first number spoken as words, in five steps. Each comment after a
`print` shows the output of a run in a fresh environment.

## Step 1: Install

Make an environment and install the package. It needs no voice assistant.

```bash
uv venv
uv pip install --prerelease=allow ovos-number-parser
```

## Step 2: Read a number from text

`extract_number` finds the first number in a text. It gives an `int` or a
`float`, or `False` when the text holds no number. `numbers_to_digits` rewrites
each number in a text as digits and keeps the other words.

```python
from ovos_number_parser import extract_number, numbers_to_digits

print(extract_number("set a timer for twenty one minutes", "en"))  # 21
print(numbers_to_digits("i need twenty three of them", "en"))  # i need 23 of them
print(extract_number("hello world", "en"))  # False
```

## Step 3: Speak a number as words

`pronounce_number` writes a number as words. `pronounce_ordinal` writes the
ordinal. `pronounce_fraction` writes a fraction that you give as text.

```python
from ovos_number_parser import pronounce_number, pronounce_ordinal, pronounce_fraction

print(pronounce_number(2023, "en"))  # two thousand, twenty three
print(pronounce_ordinal(21, "en"))  # twenty-first
print(pronounce_fraction("3/4", "en"))  # three quarters
```

## Step 4: Change the language

Each call takes a language code as its second argument. A code with a region,
such as `pt-BR`, selects the regional forms where the language has them.
European Portuguese says `dezasseis` for 16. Brazilian Portuguese says
`dezesseis`.

```python
from ovos_number_parser import extract_number, pronounce_number

print(pronounce_number(16, "pt-PT"), pronounce_number(16, "pt-BR"))  # dezasseis dezesseis
print(extract_number("einundzwanzig Katzen", "de"))  # 21
```

## Step 5: Find where each number sits

`extract_number_spans` gives every number in a text with its position. A span
holds the start and end offsets, the written form and the value.

```python
from ovos_number_parser import extract_number_spans

print([(s.start, s.end, s.surface, s.value) for s in extract_number_spans("I have two cats and 3 dogs", "en")])  # [(7, 10, 'two', 2), (20, 21, '3', 3)]
```

## Where to go next

[How it works](how-it-works.md) shows which calls read through numtag and which
code writes each language. The [API reference](api.md) lists every function with
its parameters.

---
[Index](index.md) · [← Home](../README.md) · [Adding a language →](adding-a-language.md)
