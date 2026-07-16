# API reference

All public functions live in the top-level `ovos_number_parser` package and
take a BCP-47 language code (`lang`). Language dialects resolve by prefix, so
`"pt-BR"`, `"pt-PT"` and `"pt"` all reach the Portuguese parser (with variant
handling where it matters, e.g. Brazilian vs European Portuguese).

If a language is not supported by a function, `NotImplementedError` is raised.
`pronounce_number` and `pronounce_ordinal` fall back to
[unicode-rbnf](https://github.com/rhasspy/unicode-rbnf) before giving up.

## `pronounce_number(number, lang, places=3, short_scale=True, scientific=False, ordinals=False, digits=..., gender=...)`

Convert a numeric value to its spoken form.

```python
>>> pronounce_number(4.5, "en")
'four point five'
>>> pronounce_number(21, "cs")
'dvacet jedna'
>>> pronounce_number(2023, "gl")
'dous mil e vinte e tres'
```

- `places` — decimal places to speak.
- `short_scale` — short vs long scale for large numbers
  (https://en.wikipedia.org/wiki/Names_of_large_numbers).
- `scientific` — read `5e-6` style notation aloud.
- `ordinals` — speak `"first"` instead of `"one"`.
- `digits` — `DigitPronunciation` enum; digit-by-digit reading styles.
- `gender` — `GrammaticalGender` enum for languages whose numerals inflect
  (e.g. Portuguese `"uma hora"` vs `"um minuto"`).

## `pronounce_ordinal(number, lang, short_scale=True, gender=...)`

Spoken ordinal form (`1 -> "first"`). Languages without a handwritten
implementation use the unicode-rbnf fallback.

## `pronounce_fraction(fraction_word, lang, scale=Scale.LONG)`

Speak a fraction string such as `"3/4"`. Currently implemented for Portuguese
and Mirandese.

## `extract_number(text, lang, short_scale=True, ordinals=False)`

Extract the first number found in a phrase. Returns `int`, `float`, or
`False` when the text contains no number.

```python
>>> extract_number("set a timer for twenty one minutes", "en")
21
>>> extract_number("dos mil veintitrés", "es")
2023
>>> extract_number("einundzwanzig Katzen", "de")
21
```

Compound-written languages (German, Dutch, Danish, Swedish) split words such
as `einundzwanzig`, `eenentwintig`, `toogfyrre` or `tjugoen` automatically.

## `is_fractional(input_str, lang, short_scale=True)`

Exact-match test for a fraction word (`"half"` → `0.5`, otherwise `False`).
Use `extract_number` to pull fractions out of longer phrases.

## `is_ordinal(input_str, lang)`

Exact-match test for an ordinal word (`"third"` → `3`, otherwise `False`).
Implemented for `en`, `pt`, `mwl`, `de` and `da`.

## `numbers_to_digits(utterance, lang, scale=Scale.LONG)`

Rewrite the written numbers inside a phrase as digits, keeping the rest of
the text intact.

```python
>>> numbers_to_digits("set a timer for five minutes", "en")
'set a timer for 5 minutes'
```

## Enums

- `Scale` — `Scale.SHORT` / `Scale.LONG` large-number scales.
- `GrammaticalGender` — `MASCULINE` / `FEMININE` / `NEUTRAL`.
- `DigitPronunciation` — full-number vs digit-by-digit reading styles.
