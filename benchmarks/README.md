# Benchmarks

<!-- agent-hint
covers: the development harnesses that compare pronounce_number with ICU RBNF and num2words
source: benchmarks/icu_diff.py, benchmarks/multi_diff.py, ovos_number_parser/__init__.py:pronounce_number
generated: no
verify: python -m doctest benchmarks/README.md
see: ../docs/index.md, ../docs/api.md
-->

## `icu_diff.py`: differential harness against ICU RBNF

ICU's `RuleBasedNumberFormat` is the reference implementation for spelling
numbers out, so it is the natural yardstick for `pronounce_number`. The
harness round-trips a value set through both and reports a per-language
scoreboard plus the individual disagreements.

```bash
uv venv icuenv && uv pip install --python icuenv/bin/python PyICU -e .
icuenv/bin/python benchmarks/icu_diff.py          # all languages
icuenv/bin/python benchmarks/icu_diff.py pt es    # selected languages
```

PyICU needs the ICU development headers (`pkg-config --modversion icu-i18n`).
It is intentionally **not** a dependency of the library. It is a
development tool.

### ICU is a yardstick, not an oracle

A disagreement means one of the two is wrong, and which one is a question for
the language's canonical grammar, never for ICU. Expected values in tests are
justified by a cited source and are never pinned to ICU output. Real
divergences, all correct on both sides:

| language | ours | ICU | why |
| --- | --- | --- | --- |
| en | `one hundred and one` | `one hundred one` | British vs American convention |
| pt | `dezasseis` | `dezesseis` | we default to European, ICU's plain `pt` is Brazilian |
| pt | `mil milhões` (10^9) | `um bilhão` | long scale vs short scale |
| es | `un millardo` (10^9) | `mil millones` | both accepted; ICU prefers the common form |

### Locales ICU cannot judge

ICU resolves a locale it has no rules for by falling back to the default
locale of the process, and that is **not** necessarily English. It has no
rules for `gl`, `eu`, `oc`, `ast`, `an`, `mwl`, `kab` and `fy`. On a machine
with a Portuguese default locale it hands them a *Portuguese* formatter.
Scoring Galician against Portuguese spellings produces confident nonsense, so the harness asks
ICU which locale it actually resolved to (`ACTUAL_LOCALE`) and excludes any
language ICU is only pretending to support.

Those 8 languages are precisely where we offer coverage ICU does not, and they
must be validated against their own grammars instead.


### Check the rows yourself

Run these calls in the environment from the install step above. They need
PyICU. The block sets the default locale to English first, so the fallback
locale does not depend on the machine.

```python
>>> import icu
>>> from ovos_number_parser import pronounce_number
>>> icu.Locale.setDefault(icu.Locale("en"))
>>> def spell(code, number):
...     speller = icu.RuleBasedNumberFormat(icu.URBNFRuleSetTag.SPELLOUT, icu.Locale(code))
...     return pronounce_number(number, code), speller.format(number)
>>> spell("en", 101)
('one hundred and one', 'one hundred one')
>>> spell("pt", 16)
('dezasseis', 'dezesseis')
>>> spell("pt", 10**9)
('mil milhões', 'um bilhão')
>>> spell("es", 10**9)
('un millardo', 'mil millones')
>>> galician = icu.RuleBasedNumberFormat(icu.URBNFRuleSetTag.SPELLOUT, icu.Locale("gl"))
>>> galician.getLocale(icu.ULocDataLocaleType.ACTUAL_LOCALE).getName()
'en'

```

## `multi_diff.py`: three-way differential (ICU + num2words)

One reference can be wrong or absent for a language. `multi_diff.py` adds
[num2words](https://pypi.org/project/num2words/) as a second, independent
oracle and reads the two as a vote:

```bash
uv pip install --python icuenv/bin/python PyICU num2words -e .
icuenv/bin/python benchmarks/multi_diff.py          # all languages
icuenv/bin/python benchmarks/multi_diff.py pl nl    # selected
```

* both references agree with us → almost certainly correct.
* **both agree with each other but not us → the strongest bug signal**. This
  is what to hunt. It found the Dutch `eenhonderd`/`eenduizend` and the Polish
  `dwadzieścia jeden tysiące`/spurious-`jeden` bugs;
* the two references disagree with **each other** → the value is genuinely
  contested (dialect, scale, orthography, grammatical gender). Adjudicate
  against a cited grammar, never auto-trust either library. Known-contested,
  not bugs: ru/uk `тысяча` vs `одна тысяча`, da/sv `en` vs `et`/`ett`
  (gender of one), ar `مئة` vs `مائة`, he masculine vs feminine counting forms.

Neither library is ground truth. A disagreement is a lead. The expected value
in a test always comes from a cited canonical source. Both PyICU and num2words
stay development-only, never runtime dependencies.
