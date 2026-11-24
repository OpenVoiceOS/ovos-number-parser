# Language notes

<!-- agent-hint
covers: the 40 languages, how their codes read through numtag, and the rules of single languages
source: ovos_number_parser/numtag_readers.py:NUMTAG_LANGS, ovos_number_parser/__init__.py (dispatchers), ovos_number_parser/numbers_<code>.py
generated: no
verify: sed '/^\x60\x60\x60/d' docs/languages.md | .venv/bin/python -I -m doctest -o ELLIPSIS -o NORMALIZE_WHITESPACE /dev/stdin
see: api.md, adding-a-language.md, ../README.md
-->

This page lists the 40 languages and shows how their codes are read and
spoken. It then gives the rules of single languages and the known gaps.

## Language table

All 40 languages read words through [numtag](https://github.com/TigreGotico/numtag). Their codes are in `NUMTAG_LANGS` in `ovos_number_parser/numtag_readers.py`. The ISO 639-3 codes of Modern Standard Arabic and its varieties (`arb`, `ars`, `acw`, `afb`, `arz`, `apc`, `ajp`, `acm`, `ary`, `aeb`, `ayl` and the other codes of `AR_DIALECT_DEFAULT_CASE`) read as `ar`, and `zsm` reads as `ms`. The functions `extract_number`, `extract_number_spans`, `numbers_to_digits`, `is_fractional` and `is_ordinal` follow this route.

Every language speaks numbers with a writer in this repository. Most have a `pronounce_number_<code>` function. Aragonese, Asturian, Occitan and Romanian speak through the `AN`, `AST`, `OC` and `RO` engine objects. English ordinals come from unicode-rbnf.

```text
ar Arabic, an Aragonese, ast Asturian, az Azerbaijani, eu Basque, bg Bulgarian
ca Catalan, hr Croatian, cs Czech, da Danish, nl Dutch, en English
et Estonian, fi Finnish, fr French, gl Galician, de German, el Greek
he Hebrew, hu Hungarian, id Indonesian, it Italian, kab Kabyle, ms Malay
mwl Mirandese, nb Norwegian Bokmål, nn Norwegian Nynorsk, oc Occitan, fa Persian, pl Polish
pt Portuguese, ro Romanian, ru Russian, sk Slovak, sl Slovenian, es Spanish
sv Swedish, tr Turkish, uk Ukrainian, fy West Frisian
```

The set has 40 codes.

```python
>>> from ovos_number_parser.numtag_readers import NUMTAG_LANGS
>>> len(NUMTAG_LANGS)
40
```

A code with a region (`pt-BR`, `fr-BE`) uses the language of its first
subtag. `no` reads as `nb`, `azj` as `az`, `ekk` as `et` and `pes` as `fa`.

## Germanic compound numbers (de, nl, da, sv, fy)

These languages write numbers as single compound words. numtag splits a
compound into its number words and evaluates the result, so the compound reads
as one number:

```python
>>> from ovos_number_parser import extract_number
>>> extract_number("einundzwanzig", "de"), extract_number("zweihundertdreiundvierzig", "de")
(21, 243)

>>> extract_number("eenentwintig", "nl"), extract_number("tweehonderddrieëntwintig", "nl")
(21, 223)
>>> extract_number("toogfyrre", "da"), extract_number("nihundredenioghalvfems", "da")
(42, 999)

>>> extract_number("tjugoen", "sv"), extract_number("etthundratjugotre", "sv"), extract_number("tvåtusen tjugotre", "sv")
(21, 123, 2023)
>>> extract_number("ienentweintich", "fy"), extract_number("twahûnderttrijeentweintich", "fy")
(21, 223)

```

Only Swedish also reads the spaced form (`tjugo en` is 21). In the other four,
numtag reads the spaced words as separate numbers, and `extract_number` gives
the first: `ein und zwanzig` (de) is 1, `een en twintig` (nl) is 1,
`to og fyrre` (da) is 2, `ien en tweintich` (fy) is 1 and
`zwei hundert drei und vierzig` (de) is 203.

```python
>>> from ovos_number_parser import extract_number
>>> extract_number("tjugo en", "sv")
21

>>> extract_number("ein und zwanzig", "de"), extract_number("een en twintig", "nl")
(1, 1)
>>> extract_number("to og fyrre", "da"), extract_number("ien en tweintich", "fy")
(2, 1)

>>> extract_number("zwei hundert drei und vierzig", "de")
203

```

Dutch diacritics (`één`, `drieëntwintig`) are normalized before parsing.
West Frisian diacritics (`sân`, `hûndert`, `tûzen`) are likewise normalized,
and the standard spellings `sechstjin` and `sechstich` read as 16 and 60.
Danish reads the standard spellings `elleve`, `halvtreds` and `halvfjerds`
as 11, 50 and 70.

```python
>>> from ovos_number_parser import extract_number
>>> extract_number("één", "nl"), extract_number("drieëntwintig", "nl")
(1, 23)

>>> extract_number("sân", "fy"), extract_number("hûndert", "fy"), extract_number("tûzen", "fy")
(7, 100, 1000)
>>> extract_number("sechstjin", "fy"), extract_number("sechstich", "fy")
(16, 60)

>>> extract_number("elleve", "da"), extract_number("halvtreds", "da"), extract_number("halvfjerds", "da")
(11, 50, 70)

```

## Czech declensions

Hundreds and thousands decline: `sto`, `dvě stě`, `tři sta`, `pět set`,
`dva tisíce`. Both pronouncing and extraction use the declined forms.

```python
>>> from ovos_number_parser import extract_number, pronounce_number
>>> [pronounce_number(n, "cs") for n in (100, 200, 300, 500, 2000)]
['sto', 'dvě stě', 'tři sta', 'pět set', 'dva tisíce']
>>> extract_number("dvě stě", "cs"), extract_number("dva tisíce", "cs")
(200, 2000)

```

## Basque vigesimal counting

Basque counts in twenties. The `-ta` joiner forms are understood when
extracting: `hogeita bat` (20 + 1 = 21), `berrogeita hamar` (40 + 10 = 50),
`laurogeita hemeretzi` (80 + 19 = 99).

```python
>>> from ovos_number_parser import extract_number
>>> extract_number("hogeita bat", "eu"), extract_number("berrogeita hamar", "eu"), extract_number("laurogeita hemeretzi", "eu")
(21, 50, 99)

```

## Romance languages (pt, gl, mwl, ast, an)

Portuguese, Galician, Mirandese, Asturian and Aragonese share a declarative `NumberVocabulary` + `RomanceNumberExtractor` implementation in `ovos_number_parser.util`. Each language is described by its vocabulary (units, tens, hundreds, scales, ordinals, fractions, gender rules and joiner placement). The shared engine does the speaking for all of them. Numtag reads their numbers.

Portuguese distinguishes European and Brazilian variants (`pt-PT` reads
16 as `dezasseis`, `pt-BR` as `dezesseis`) and inflects `um/uma`,
`dois/duas` and the hundreds (`duzentos/duzentas`) for grammatical gender.

```python
>>> from ovos_number_parser import pronounce_number
>>> pronounce_number(16, "pt-PT"), pronounce_number(16, "pt-BR")
('dezasseis', 'dezesseis')

```

Aragonese pronounces 4, 8, 16, 21, 35 and 100 as `cuatre`, `ueito`,
`deciséis`, `vintiún`, `trenta y cinco` and `cient`. It reads the variants
`quatre`, `vente` and `noranta` as 4, 20 and 90. Ordinals use the `-eno`
series (`cuatreno`, `cinqueno`).

```python
>>> from ovos_number_parser import extract_number, pronounce_number, pronounce_ordinal
>>> [pronounce_number(n, "an") for n in (4, 8, 16, 21, 35, 100)]
['cuatre', 'ueito', 'deciséis', 'vintiún', 'trenta y cinco', 'cient']

>>> [extract_number(word, "an") for word in ("quatre", "vente", "noranta")]
[4, 20, 90]
>>> pronounce_ordinal(4, "an"), pronounce_ordinal(5, "an")
('cuatreno', 'cinqueno')

```

## Spanish and Catalan

`es` and `ca` handle fused twenties (`veintiuno`, `vint-i-u`), the irregular
hundreds (`quinientos`, `setecientos`, `novecientos`), scale words including
`millón/millones` and `milió/milions`, and additive continuations such as
`dos mil veintitrés`.

```python
>>> from ovos_number_parser import extract_number
>>> [extract_number(text, "es") for text in ("veintiuno", "quinientos", "setecientos", "novecientos", "dos mil veintitrés")]
[21, 500, 700, 900, 2023]
>>> [extract_number(text, "ca") for text in ("vint-i-u", "dos mil vint-i-tres", "un milió")]
[21, 2023, 1000000]

```

## English

`extract_number` understands the `and` connector inside a number
(`one hundred and one` = 101) and digit grouping (`1,000,000`). A comma
between two number words ends the number: `two thousand, twenty three` reads
as 2000, and `two thousand twenty three` reads as 2023.

`extract_number("twenty twenty three", "en")` is 20. numtag reads the words as
two numbers, 20 and 23, and a year grammar that joins them is the job of the
caller.

```python
>>> from ovos_number_parser import extract_number
>>> extract_number("one hundred and one", "en"), extract_number("1,000,000", "en")
(101, 1000000)

>>> extract_number("two thousand, twenty three", "en"), extract_number("two thousand twenty three", "en")
(2000, 2023)
>>> extract_number("twenty twenty three", "en")
20

```

## Kabyle

Kabyle carries two numeral systems: the pan-Amazigh cardinals (`yiwen`, `sin`, `kṛaḍ`, ... `mraw`) and the Algerian-Arabic borrowed numerals used for everyday counting above ten (`ḥḍac` = 11, `ɛecrin` = 20, `mya` = 100, `alef` = 1000). Pronunciation uses the Amazigh forms for 0-10 and the Arabic-derived forms above ten, joining compounds with the conjunction `u` with the unit before the ten (`waḥed u ɛecrin` = 21). Extraction accepts both systems, feminine forms (`yiwet`, `snat`) and diacritic-stripped spellings (`hdac` = 11).

```python
>>> from ovos_number_parser import extract_number, pronounce_number
>>> [pronounce_number(n, "kab") for n in (1, 2, 11, 20, 21, 100, 1000)]
['yiwen', 'sin', 'ḥḍac', 'ɛecrin', 'waḥed u ɛecrin', 'mya', 'alef']
>>> [extract_number(word, "kab") for word in ("yiwet", "snat", "hdac", "ɛecrin", "mya", "alef")]
[1, 2, 11, 20, 100, 1000]

```

Ordinals use `amezwaru` (f. `tamezwarut`) for "first" and `wis`/`tis` +
cardinal otherwise. The only attested fraction noun is `azgen` (half).

Pronunciation spans 0 to 9999. A larger number raises `OverflowError`. The
minus word, a decimal-separator word, ordinal suffix forms, larger scale words
and further fraction nouns are not reliably attested, so the writer omits them.

## Persian

Numbers are written and parsed in Persian script (`بیست و یک` = 21). Both
extraction and pronunciation cover units through millions. Pronunciation reads
2.5 as `دو و نیم`.

```python
>>> from ovos_number_parser import extract_number, pronounce_number
>>> extract_number("بیست و یک", "fa"), pronounce_number(2.5, "fa")
(21, 'دو و نیم')

```

## Known gaps

Each reading gap below is a value that numtag reads wrong, with the issue that
tracks it. The examples that follow show the real output.

- A comma between two number words ends the number in English and Czech.
  `pronounce_number(2023, "en")` writes `two thousand, twenty three`, and
  `extract_number` reads that text as 2000. Czech `tisíc, dvě stě třicet čtyři`
  reads as 1000
  ([numtag#157](https://github.com/TigreGotico/numtag/issues/157)).

- Kabyle `mraw d yiwen` and `mraw u yiwen` read as 10, not 11
  ([numtag#168](https://github.com/TigreGotico/numtag/issues/168)).

- A denominator word without a count is no fraction. `is_fractional("quarter", "en")`
  is `False`, and so is `is_fractional("third", "en")`, which reads as the
  ordinal 3
  ([numtag#262](https://github.com/TigreGotico/numtag/issues/262)).

- Malay `dua koma lima` reads as 2, because numtag takes `perpuluhan` as the
  only spoken decimal marker
  ([numtag#265](https://github.com/TigreGotico/numtag/issues/265)).

- Danish `fire og tyve` reads as 4
  ([numtag#253](https://github.com/TigreGotico/numtag/issues/253)).

- The Arabic variety codes have no lexicon of their own
  ([numtag#266](https://github.com/TigreGotico/numtag/issues/266)).
  A homograph such as `ميتين` reads as a number
  ([ovos-number-parser#553](https://github.com/OpenVoiceOS/ovos-number-parser/issues/553)).

The writing gaps are:

- `pronounce_ordinal` gives a cardinal for the Slovenian and Turkish hundreds 200 to 900 and the Croatian 1000 ([ovos-number-parser#559](https://github.com/OpenVoiceOS/ovos-number-parser/issues/559)).
- Some rbnf values come back as digits ([ovos-number-parser#544](https://github.com/OpenVoiceOS/ovos-number-parser/issues/544)).
- A `Decimal` with more digits than a `float` holds speaks wrong last digits ([ovos-number-parser#409](https://github.com/OpenVoiceOS/ovos-number-parser/issues/409)).

```python
>>> from ovos_number_parser import extract_number, pronounce_number
>>> extract_number("two thousand, twenty three", "en")
2000

>>> extract_number(pronounce_number(1234, "cs"), "cs")
1000
>>> extract_number("mraw d yiwen", "kab"), extract_number("mraw u yiwen", "kab")
(10, 10)

>>> from ovos_number_parser import is_fractional
>>> is_fractional("quarter", "en"), is_fractional("third", "en")
(False, False)

>>> extract_number("dua koma lima", "ms"), extract_number("dua perpuluhan lima", "ms")
(2, 2.5)
>>> extract_number("fire og tyve", "da")
4

```

## Full function parity

Every supported language provides every public function. Where a language
has no hand-written implementation, a generic fallback fills in:

- `pronounce_fraction` reuses the language's `nice_number` fraction wording (which carries its plural/declension rules) and spells out any digits. The Slavic languages use feminine numerators (`dvě třetiny`, `две трети`) and Hungarian its `két` allomorph. Denominators outside the language's fraction vocabulary fall back to "cardinal numerator + ordinal denominator".

- `pronounce_ordinal` uses [unicode-rbnf](https://github.com/rhasspy/unicode-rbnf)
  for English and for a few values of other languages (see
  `pronounce_ordinal` in the [API reference](api.md)).
  `pronounce_number` reads a value past the scale table of a writer in
  scientific form: `pronounce_number(10**100, "de")` is
  `'eins mal zehn hoch einhundert'`.

The parity guarantee is enforced by `tests/test_lang_parity.py`, which runs
every public function against every supported language.

---
[Index](index.md) · [← API reference](api.md) · [Adding a language →](adding-a-language.md)
