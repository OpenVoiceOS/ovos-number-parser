# Documentation

<!-- agent-hint
covers: the list of every page under docs/, in reading order, with what each page gives the reader
source: docs/*.md
generated: no
verify: diff <(ls docs/*.md | sed 's#docs/##' | grep -v '^index.md$' | sort) <(grep -o '^| \[[^]]*\]([a-z-]*\.md)' docs/index.md | sed 's/.*(\(.*\))/\1/' | sort)
see: ../README.md, getting-started.md, how-it-works.md, api.md, writers.md, languages.md, adding-a-language.md
-->

This page lists every page under `docs/` in reading order. How-to pages come
first, then the explanation, then the reference pages. Start with the
[README](../README.md) for the install step and a first example.

| Page | What you get there |
|------|--------------------|
| [Getting started](getting-started.md) | Install, then read a number from text, speak a number, change the language and find where each number sits, in five steps |
| [Adding a language](adding-a-language.md) | The steps to add reading and speaking for another language |
| [How it works](how-it-works.md) | The call path of each function, which calls pass to numtag, and a plot of the source behind each writer |
| [API reference](api.md) | Every public function with its parameters, defaults and an example, the engine that answers it, the enums and the numtag reader module |
| [Language writers](writers.md) | The writer functions, engine objects and helpers of each of the 40 languages |
| [Language notes](languages.md) | The 40 languages, the rules of single languages and the known gaps with their issues |

Runnable scripts are in [`examples/`](../examples/). The differential
harnesses against ICU and num2words are in
[`benchmarks/`](../benchmarks/README.md). The script that builds the plot is
[`plots/writer_sources.py`](plots/writer_sources.py). Rules for agents that
change this repository are in [AGENTS.md](../AGENTS.md).

---
[Home](../README.md) · [Getting started →](getting-started.md)
