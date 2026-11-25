# Language writers

<!-- agent-hint
covers: the writer of each of the 40 languages, the functions and engine objects it exports, and the helper names of the package
source: ovos_number_parser/__init__.py (imports and dispatchers), ovos_number_parser/numbers_<code>.py, ovos_number_parser/util.py:NumberVocabulary,RomanceNumberExtractor
generated: no
verify: .venv/bin/python -I -c "import re, ovos_number_parser as p; t = open('docs/writers.md').read(); names = re.findall(r'^\| \x60[a-z]+\x60 \| [^|]+\| \x60[^|]+\x60 \| (.*) \|$', t, re.M); assert len(names) == 40; [getattr(p, n) for row in names for n in re.findall(r'\x60(\w+)\x60', row)]" && sed '/^\x60\x60\x60/d' docs/writers.md | .venv/bin/python -I -m doctest -o ELLIPSIS -o NORMALIZE_WHITESPACE /dev/stdin
see: how-it-works.md, api.md, languages.md, adding-a-language.md
-->

This page names the code that speaks each language. Read it when you need a
writer of one language, an engine object, or a helper that the top-level
functions do not expose.

The top-level `pronounce_number`, `pronounce_ordinal` and `pronounce_fraction`
call these writers for you. Call a writer directly to skip the language
dispatch.

## The writer of each language

Every language has a module `ovos_number_parser/numbers_<code>.py`. Malay shares
`numbers_id.py` with Indonesian. The last column lists the names that
`ovos_number_parser` exports for the language.

| Code | Language | Module | Top-level names |
|---|---|---|---|
| `an` | Aragonese | `numbers_an.py` | `AN` |
| `ar` | Arabic | `numbers_ar.py` | `nice_number_ar`, `pronounce_number_ar`, `pronounce_ordinal_ar` |
| `ast` | Asturian | `numbers_ast.py` | `AST` |
| `az` | Azerbaijani | `numbers_az.py` | `nice_number_az`, `pronounce_number_az` |
| `bg` | Bulgarian | `numbers_bg.py` | `nice_number_bg`, `pronounce_number_bg` |
| `ca` | Catalan | `numbers_ca.py` | `nice_number_ca`, `pronounce_number_ca`, `CA` |
| `cs` | Czech | `numbers_cs.py` | `nice_number_cs`, `pronounce_number_cs`, `pronounce_ordinal_cs` |
| `da` | Danish | `numbers_da.py` | `nice_number_da`, `pronounce_number_da`, `pronounce_ordinal_da` |
| `de` | German | `numbers_de.py` | `nice_number_de`, `pronounce_number_de`, `pronounce_ordinal_de` |
| `el` | Greek | `numbers_el.py` | `nice_number_el`, `pronounce_number_el`, `pronounce_ordinal_el` |
| `en` | English | `numbers_en.py` | `pronounce_number_en` |
| `es` | Spanish | `numbers_es.py` | `nice_number_es`, `pronounce_number_es`, `ES` |
| `et` | Estonian | `numbers_et.py` | `nice_number_et`, `pronounce_number_et`, `pronounce_ordinal_et` |
| `eu` | Basque | `numbers_eu.py` | `nice_number_eu`, `pronounce_number_eu`, `pronounce_ordinal_eu` |
| `fa` | Persian | `numbers_fa.py` | `nice_number_fa`, `pronounce_number_fa`, `pronounce_ordinal_fa` |
| `fi` | Finnish | `numbers_fi.py` | `nice_number_fi`, `pronounce_number_fi`, `pronounce_ordinal_fi` |
| `fr` | French | `numbers_fr.py` | `nice_number_fr`, `FR`, `FR_BE`, `FR_CH` |
| `fy` | West Frisian | `numbers_fy.py` | `nice_number_fy`, `pronounce_number_fy`, `pronounce_ordinal_fy` |
| `gl` | Galician | `numbers_gl.py` | `pronounce_fraction_gl`, `pronounce_number_gl`, `pronounce_ordinal_gl`, `GL` |
| `he` | Hebrew | `numbers_he.py` | `nice_number_he`, `pronounce_number_he`, `pronounce_ordinal_he` |
| `hr` | Croatian | `numbers_hr.py` | `nice_number_hr`, `pronounce_number_hr`, `pronounce_ordinal_hr` |
| `hu` | Hungarian | `numbers_hu.py` | `nice_number_hu`, `pronounce_number_hu`, `pronounce_ordinal_hu` |
| `id` | Indonesian | `numbers_id.py` | `nice_number_id`, `pronounce_number_id`, `pronounce_ordinal_id` |
| `it` | Italian | `numbers_it.py` | `nice_number_it`, `pronounce_number_it`, `pronounce_ordinal_it`, `IT` |
| `kab` | Kabyle | `numbers_kab.py` | `pronounce_number_kab`, `pronounce_ordinal_kab` |
| `ms` | Malay | `numbers_id.py` | `nice_number_ms`, `pronounce_number_ms`, `pronounce_ordinal_ms` |
| `mwl` | Mirandese | `numbers_mwl.py` | `MWL` |
| `nb` | Norwegian Bokmål | `numbers_nb.py` | `nice_number_nb`, `pronounce_number_nb`, `pronounce_ordinal_nb` |
| `nl` | Dutch | `numbers_nl.py` | `nice_number_nl`, `pronounce_number_nl`, `pronounce_ordinal_nl` |
| `nn` | Norwegian Nynorsk | `numbers_nn.py` | `nice_number_nn`, `pronounce_number_nn`, `pronounce_ordinal_nn` |
| `oc` | Occitan | `numbers_oc.py` | `OC` |
| `pl` | Polish | `numbers_pl.py` | `nice_number_pl`, `pronounce_number_pl`, `pronounce_ordinal_pl` |
| `pt` | Portuguese | `numbers_pt.py` | `PT_PT`, `PT_BR` |
| `ro` | Romanian | `numbers_ro.py` | `RO` |
| `ru` | Russian | `numbers_ru.py` | `nice_number_ru`, `pronounce_number_ru` |
| `sk` | Slovak | `numbers_sk.py` | `nice_number_sk`, `pronounce_number_sk`, `pronounce_ordinal_sk` |
| `sl` | Slovenian | `numbers_sl.py` | `nice_number_sl`, `pronounce_number_sl` |
| `sv` | Swedish | `numbers_sv.py` | `nice_number_sv`, `pronounce_number_sv`, `pronounce_ordinal_sv` |
| `tr` | Turkish | `numbers_tr.py` | `nice_number_tr`, `pronounce_number_tr`, `pronounce_ordinal_tr` |
| `uk` | Ukrainian | `numbers_uk.py` | `nice_number_uk`, `pronounce_number_uk`, `pronounce_ordinal_uk` |

A name in capitals is an engine object. A name in lower case is a function.
Three kinds of function exist per language.

## Writer functions

`pronounce_number_<code>(number, places=2, short_scale=True, scientific=False, ordinals=False)`
speaks a number. The signature of a language can differ from this base in the
defaults and in the arguments:

- `short_scale` defaults to `False` for ca, es, it, nb and nn. The functions for
  ar, el, fa and he have no `short_scale`.
- es takes `(number, places=2, short_scale=False)`. It has no `scientific` and
  no `ordinals`.
- ca takes `(number, places=2, short_scale=False, scientific=False)`. It has no
  `ordinals`.
- it has no `ordinals`. eu takes only `(num, places=2)`.
- `gender` is an extra argument for cs, da, de, it, nb, pl, ru, sv and uk, with
  a `GrammaticalGender` default. Arabic takes `gender` too, with the string
  default `"masculine"`.
- ar also takes `case` and `lect`. he takes `feminine`, fa takes `variant`, en
  takes `year` and pl takes `scientific_run`.
- gl follows the engine signature below, with `places=5`.
  `pronounce_number_kab` takes `(number, places=3, ordinals=False, gender)`.

`pronounce_ordinal_<code>(number)` speaks an ordinal. The versions for ar, cs,
da, gl, it, kab, pl and uk also take a `gender`. The Arabic version also takes a
`case`, and the Czech version a `short_scale`. The Galician version also takes
a `scale`. Basque names the first argument `num`.

```python
>>> from ovos_number_parser import pronounce_number_de, pronounce_ordinal_de, pronounce_number_ru
>>> from ovos_number_parser.util import GrammaticalGender
>>> pronounce_number_de(1234)
'eintausendzweihundertvierunddreißig'
>>> pronounce_ordinal_de(3)
'dritte'
>>> pronounce_number_ru(21, gender=GrammaticalGender.FEMININE)
'двадцать одна'

```

`nice_number_<code>(number, speech=True, denominators=range(1, 21))` writes a
mixed fraction. With `speech=True` the answer is words. With `speech=False`
it is digits. Catalan has no default for `speech`, so pass it. Arabic, Greek and Hebrew default to `range(1, 11)`, and Slovenian
defaults to `None`. The Arabic version takes a `case` and the Persian version a
`variant`. The top-level package has no `nice_number` dispatcher, so you reach
the function by its language name. `pronounce_fraction` uses these functions
for the languages that have no fraction writer of their own.

```python
>>> from ovos_number_parser import nice_number_de, nice_number_id
>>> nice_number_de(5.5), nice_number_de(5.5, speech=False)
('5 und ein halb', '5 1/2')
>>> nice_number_id(4.5)
'4 setengah'

```

Nine languages have no `nice_number_<code>` function: an, ast, en, gl, kab,
mwl, oc, pt and ro.

Hungarian has a third writer, `pronounce_scientific_hu(mantissa, exponent)`.
It reads a mantissa times a negative power of ten.

```python
>>> from ovos_number_parser import pronounce_scientific_hu
>>> pronounce_scientific_hu(15, -3)
'tizenötször tíz a mínusz harmadikon'

```

## Engine objects

An engine speaks numbers for a Romance language from a `NumberVocabulary`, a
dataclass that holds the units, tens, hundreds, scale words, ordinals,
fractions and joiner rules of one language. `RomanceNumberExtractor` in
`ovos_number_parser/util.py` turns a vocabulary into an object with three
methods:

- `pronounce_number(number, places=5, scale=None, ordinals=False, digits=DigitPronunciation.FULL_NUMBER, gender=GrammaticalGender.MASCULINE)`
- `pronounce_ordinal(number, gender=GrammaticalGender.MASCULINE, scale=None)`
- `pronounce_fraction(word, scale=None)`

`pronounce_number` also has three private keyword arguments that start with an
underscore. The top-level `pronounce_number` replaces `digits=None` with a value
for the language before it calls the engine.

```python
>>> from ovos_number_parser import ES, PT_PT, PT_BR, FR, FR_BE, FR_CH
>>> from ovos_number_parser.util import GrammaticalGender
>>> ES.pronounce_number(21), ES.pronounce_ordinal(3), ES.pronounce_fraction("3/4")
('veintiuno', 'tercero', 'tres cuartos')
>>> PT_PT.pronounce_number(16), PT_BR.pronounce_number(16)
('dezasseis', 'dezesseis')
>>> PT_BR.pronounce_ordinal(2, gender=GrammaticalGender.FEMININE)
'segunda'
>>> FR.pronounce_number(80), FR_BE.pronounce_number(70), FR_CH.pronounce_number(80)
('quatre-vingts', 'septante', 'huitante')

```

`PT_PT` and `PT_BR` are the two variants in `PortugueseVariant`, which has the
members `PT` and `BR`. `FR_BE` and `FR_CH` change the words for 70, 80 and 90.
The `AN`, `AST`, `CA`, `FR`, `GL`, `MWL`, `OC`, `PT_*`, `RO` and `ES` engines
answer `pronounce_number` for their language. The `IT` engine exists, and the
Italian dispatch uses the `pronounce_number_it` function for cardinals because
that function elides the tens (`ventuno`).

Each engine also has a `numbers_to_digits` method. That method is deprecated.
It warns and calls the numtag reader.

`fraction_noun_es(denominator, plural=False)` gives the masculine Spanish
fraction noun of a denominator. `pronounce_fraction` uses it for a Spanish
denominator that the `nice_number_es` wording does not cover.

```python
>>> from ovos_number_parser import fraction_noun_es, pronounce_fraction
>>> fraction_noun_es(5), fraction_noun_es(5, plural=True)
('quinto', 'quintos')
>>> pronounce_fraction("1/25", "es")
'un veinticincoavo'

```

## Arabic helpers

Arabic has regional lects with their own cardinals. `resolve_ar_lang(lang)`
gives the default register of the lect that a tag names, `"nominative"` or
`"oblique"`, or `None` for a tag that names no Arabic variety. `resolve_ar_lect(lang)`
gives the ISO 639-3 code of the lect, or `None` for a lect with no table of its
own, such as `ar`.

```python
>>> from ovos_number_parser import resolve_ar_lang, resolve_ar_lect
>>> resolve_ar_lang("arz"), resolve_ar_lect("arz")
('oblique', 'arz')
>>> resolve_ar_lang("ar"), resolve_ar_lect("ar")
('nominative', None)

```

## Number helpers

`scientific_parts(number, places)` splits a number into a mantissa and an
exponent. `round_half_up(value, places)` rounds a `Decimal` half away from zero.
The writers use both.

```python
>>> from decimal import Decimal
>>> from ovos_number_parser import round_half_up, scientific_parts
>>> round_half_up(Decimal("2.5"), 0)
Decimal('3')
>>> scientific_parts(12345, 3)
(1.235, 4)

```

## Deprecated writer names

`pronounce_number_ca`, and the names `pronounce_number_<code>`,
`pronounce_ordinal_<code>` and `pronounce_fraction_<code>` for `gl`, `mwl` and
`pt`, give a `DeprecationWarning`. Use the engine object or the top-level
function instead. [api.md](api.md#deprecated-reader-names) lists the deprecated
reader names.

---
[Index](index.md) · [← API reference](api.md) · [Language notes →](languages.md)
