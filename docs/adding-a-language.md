# Adding a language

Every language lives in its own module, `ovos_number_parser/numbers_<code>.py`,
and is wired into the dispatcher functions in `ovos_number_parser/__init__.py`.

## 1. Pick the implementation style

**Romance languages** (or any language with unit/ten/hundred/scale structure
and joiner words) should use the declarative vocabulary engine — describe the
language, don't reimplement the algorithm:

```python
from ovos_number_parser.util import NumberVocabulary, RomanceNumberExtractor, Scale

_XX = NumberVocabulary(
    LANG="xx-XX",
    JOIN_WORD=["e"],
    JOINER_ON_TWENTYS=True,
    JOINER_ON_HUNDREDS=False,
    JOINER_ON_THOUSANDS=False,
    DECIMAL_MARKER=["coma", ".", ","],
    NEGATIVE_SIGN=["menos"],
    HUNDRED_PARTICLE="cento",
    UNITS={0: "...", 1: "...", ...},
    TENS={...},
    HUNDREDS={...},
    SHORT_SCALE={...},
    LONG_SCALE={...},
    ORDINAL_UNITS={...},
    FRACTION={...},
    ...
)
XX = RomanceNumberExtractor(_XX)
```

See `numbers_gl.py` or `numbers_ast.py` for complete worked examples, and the
`NumberVocabulary` docstrings in `util.py` for every knob. Languages with
articled scale groups ("o mie"), a count-to-scale linker word
("douăzeci **de** mii"), multiplicative hundreds words ("două sute" = 200)
or particle-based ordinals ("al doilea"/"a doua") can describe those with
`SCALE_ONE`, `SCALE_LINKER`, `SCALE_GENDERS`, `MULTIPLY_HUNDREDS`,
`FRACTION_ONE`, `JOINER_ON_SCALE_REMAINDER` and the `ORDINAL_PREFIX` family —
see `numbers_ro.py` for a worked example.

**Other language families** implement the functions directly. Use an existing
module of the same family as a template:

- Germanic compound-word languages: `numbers_de.py` (includes the
  compound-splitting helpers).
- Slavic languages with declension: `numbers_cs.py` or `numbers_ru.py`.
- Token-based summing parsers: `numbers_en.py`.

## 2. Functions to provide

At minimum:

- `pronounce_number_<code>(number, places=2, ...)`
- `extract_number_<code>(text, short_scale=True, ordinals=False)`

Nice to have:

- `is_fractional_<code>`, `is_ordinal_<code>`
- `pronounce_ordinal_<code>`
- `numbers_to_digits_<code>`

## 3. Wire the dispatcher

Add the language-prefix branch to each matching top-level function in
`__init__.py` (`pronounce_number`, `extract_number`, `is_fractional`, ...).

## 4. Tests

Add `tests/test_number_parser_<code>.py` with three parts (see any existing
language test for the pattern):

1. **Pronounce anchors** — hand-verified spoken forms for a fixed set of
   values (0-20, tens, 100, 101, 123, 999, 1000, 2023, 1e6, ...).
2. **Extract anchors** — the same table driven in reverse.
3. **Round-trip sweep** — `extract_number(pronounce_number(n))` must return
   `n` over a wide range. This catches vocabulary typos and asymmetries
   cheaply.

Anchor expectations must come from reference material or native usage —
never trust engine output you haven't verified; a wrong anchor locks the
bug in.

## 5. README

Add the language row to the support matrix in `README.md`.
