# Documentation

<!-- agent-hint
covers: the list of every page under docs/, in reading order, with what each page gives the reader
source: docs/*.md
generated: no
verify: diff <(ls docs/*.md | sed 's#docs/##' | grep -v '^index.md$' | sort) <(grep -o '^| \[[^]]*\]([a-z-]*\.md)' docs/index.md | sed 's/.*(\(.*\))/\1/' | sort)
see: ../README.md, api.md, languages.md, adding-a-language.md
-->

This page lists every page under `docs/` in reading order. Start with the
[README](../README.md) for the install step and a first example.

| Page | What you get there |
|------|--------------------|
| [API reference](api.md) | Every public function with its parameters, defaults and an example |
| [Language notes](languages.md) | Which languages read through numtag, how codes map to them, and the rules of single languages |
| [Adding a language](adding-a-language.md) | The steps to add reading and speaking for another language |

Runnable scripts are in [`examples/`](../examples/). The differential
harnesses against ICU and num2words are in
[`benchmarks/`](../benchmarks/README.md). Rules for agents that
change this repository are in [AGENTS.md](../AGENTS.md).

---
[Home](../README.md) · [API reference →](api.md)
